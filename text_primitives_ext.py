"""
Text Primitives Extension — Motion Graphics MCP Server
=======================================================

Adds text/emoji as production primitive types with a semantic inference layer.

Key architectural difference from geometric primitives:
  Geometric primitives are meaning-neutral → acquire meaning through LOOK + ACTION + EFFECT
  Text primitives are meaning-loaded → carry default OLAE specifications semantically

The semantic inference engine is Layer 2 (deterministic, 0 tokens):
  Given a glyph → returns complete default OLAE configuration.
  Users override selectively. System fills gaps with coherent defaults.

New tools:
  Layer 1:
    list_text_primitives()         — Enumerate all glyphs with semantic profiles
    list_text_render_modes()       — Enumerate rendering strategies

  Layer 2:
    get_text_primitive_parameters() — Full spec for a named glyph
    infer_emoji_semantics()        — Core inference: glyph → OLAE defaults
    map_emoji_to_olae()            — Single emoji → complete mapped parameters
    compose_emoji_scene()          — Multiple emoji → scene graph with auto-layout

  Layer 2.5 (code gen):
    generate_emoji_threejs_html()  — Self-contained HTML from emoji specification

Integration points:
  - Extends geometric_primitives taxonomy with text_primitives category
  - Compatible with existing compose_scene() via emoji_glyph primitive type
  - Compatible with orbit composer via standard OLAE mapping
  - Glyph-native colors preserved or overridden by palette system
"""

import yaml
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


# ---------------------------------------------------------------------------
# OLOG LOADING
# ---------------------------------------------------------------------------

OLOG_DIR = Path(__file__).parent / "ologs"


def load_text_primitives() -> Dict[str, Any]:
    """Load and index the text primitives taxonomy."""
    with open(OLOG_DIR / "text_primitives.yaml", 'r') as f:
        data = yaml.safe_load(f)

    # Build runtime glyph index: glyph_char → (category_name, entry_name, entry_data)
    glyph_index = {}
    skip_keys = {
        "intentionality", "render_modes", "glyph_index",
        "role_compatibility", "tag_affinities",
    }
    for category_name, category_data in data.items():
        if category_name in skip_keys:
            continue
        if not isinstance(category_data, dict):
            continue
        for entry_name, entry_data in category_data.items():
            if isinstance(entry_data, dict) and "glyph" in entry_data:
                glyph_index[entry_data["glyph"]] = (category_name, entry_name, entry_data)

    return data, glyph_index


TEXT_PRIMITIVES, GLYPH_INDEX = load_text_primitives()


# ---------------------------------------------------------------------------
# LOOKUP HELPERS
# ---------------------------------------------------------------------------

def find_text_primitive_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Find a text primitive entry by its taxonomy name (e.g., 'fire', 'earth')."""
    skip_keys = {
        "intentionality", "render_modes", "glyph_index",
        "role_compatibility", "tag_affinities",
    }
    for category_name, category_data in TEXT_PRIMITIVES.items():
        if category_name in skip_keys:
            continue
        if isinstance(category_data, dict) and name in category_data:
            return category_data[name]
    return None


def find_text_primitive_by_glyph(glyph: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    """Find a text primitive by its Unicode glyph character.
    Returns (category_name, entry_name, entry_data) or None."""
    # Direct lookup
    if glyph in GLYPH_INDEX:
        return GLYPH_INDEX[glyph]
    # Strip variation selectors for fuzzy match
    stripped = glyph.replace('\ufe0f', '').replace('\ufe0e', '')
    for key, val in GLYPH_INDEX.items():
        if key.replace('\ufe0f', '').replace('\ufe0e', '') == stripped:
            return val
    return None


def get_render_mode(mode_name: str) -> Optional[Dict[str, Any]]:
    """Get render mode specification."""
    return TEXT_PRIMITIVES.get("render_modes", {}).get(mode_name)


def get_role_spec(role_name: str) -> Optional[Dict[str, Any]]:
    """Get compositional role specification."""
    return TEXT_PRIMITIVES.get("role_compatibility", {}).get(role_name)


def get_tag_affinity(tag: str) -> Optional[Dict[str, Any]]:
    """Get semantic tag affinity for palette/lighting/effect inference."""
    return TEXT_PRIMITIVES.get("tag_affinities", {}).get(tag)


# ---------------------------------------------------------------------------
# TOOL REGISTRATION
#
# These functions are designed to be registered on the FastMCP instance.
# In your main server file, import and register:
#
#   from text_primitives_ext import register_text_primitive_tools
#   register_text_primitive_tools(mcp)
# ---------------------------------------------------------------------------

def register_text_primitive_tools(mcp):
    """Register all text primitive tools on a FastMCP instance."""

    # ===== LAYER 1 — TAXONOMY ENUMERATION =====

    @mcp.tool()
    def list_text_primitives() -> str:
        """List all text/emoji primitives with their semantic profiles.

        Layer 1: Pure taxonomy enumeration. Returns all available glyphs
        organized by semantic category, with implied motion, material,
        and compositional role for each.

        Returns:
            Formatted overview of all emoji primitives and their semantics.
        """
        skip_keys = {
            "intentionality", "render_modes", "glyph_index",
            "role_compatibility", "tag_affinities",
        }
        result = ["# Text Primitives — Emoji as Motion Graphics Objects\n"]

        for category_name, category_data in TEXT_PRIMITIVES.items():
            if category_name in skip_keys:
                continue
            if not isinstance(category_data, dict):
                continue

            result.append(f"\n## {category_name.replace('_', ' ').title()}\n")
            for entry_name, entry_data in category_data.items():
                if not isinstance(entry_data, dict) or "glyph" not in entry_data:
                    continue
                sp = entry_data.get("semantic_profile", {})
                action = sp.get("implied_action", {})
                look = sp.get("implied_look", {})
                result.append(
                    f"**{entry_data['glyph']} {entry_name}**: {entry_data['name']}"
                )
                result.append(f"  - {entry_data['description']}")
                result.append(f"  - Motion: {action.get('motion', '—')}")
                result.append(f"  - Material: {look.get('material', '—')}")
                result.append(f"  - Role: {sp.get('compositional_role', '—')}")
                result.append(f"  - Physics: {sp.get('physics_model', '—')}")
                result.append(f"  - Render: {entry_data.get('render_mode', '—')}")
                result.append(f"  - Tags: {', '.join(sp.get('semantic_tags', []))}")
                result.append("")

        return "\n".join(result)

    @mcp.tool()
    def list_text_render_modes() -> str:
        """List available rendering strategies for text primitives.

        Layer 1: Pure taxonomy enumeration.

        Modes:
          billboard  — CanvasTexture sprite, always faces camera, instancable
          extruded   — 3D letterform, full material interaction
          sdf        — Signed Distance Field, resolution-independent
          particle   — Instanced billboard swarm
        """
        modes = TEXT_PRIMITIVES.get("render_modes", {})
        result = ["# Text Primitive Render Modes\n"]
        for mode_name, mode_data in modes.items():
            result.append(f"\n**{mode_name}**: {mode_data['name']}")
            result.append(f"  - {mode_data['description']}")
            result.append(f"  - Geometry: {mode_data['threejs_geometry']}")
            result.append(f"  - Material interaction: {mode_data['material_interaction']}")
            result.append(f"  - Instancable: {mode_data['supports_instancing']}")
            result.append(f"  - Complexity: {mode_data['complexity']}")
            result.append(f"  - Use cases: {', '.join(mode_data['use_cases'])}")
            result.append("")
        return "\n".join(result)

    # ===== LAYER 2 — DETERMINISTIC INFERENCE =====

    @mcp.tool()
    def get_text_primitive_parameters(name: str) -> str:
        """Get complete parameters for a text primitive by name.

        Layer 2 deterministic lookup. Returns the full semantic profile
        including implied OLAE defaults, physics model, and scene behavior.

        Args:
            name: Taxonomy name (e.g., 'fire', 'earth', 'sparkles')
                  OR a glyph character (e.g., '🔥', '🌍', '✨')
        """
        # Try by name first, then by glyph
        entry = find_text_primitive_by_name(name)
        if entry:
            return yaml.dump(entry, default_flow_style=False, allow_unicode=True)

        result = find_text_primitive_by_glyph(name)
        if result:
            _, _, entry = result
            return yaml.dump(entry, default_flow_style=False, allow_unicode=True)

        return f"Error: Text primitive '{name}' not found by name or glyph"

    @mcp.tool()
    def infer_emoji_semantics(glyph: str) -> str:
        """Core semantic inference engine — glyph to complete OLAE defaults.

        Layer 2: Deterministic, 0 tokens. Given a single emoji character,
        returns the full implied OBJECT, LOOK, ACTION, and EFFECT
        configuration derived from the glyph's semantic profile.

        This is the key production tool. The semantic_profile encodes:
          - implied_action: default motion pattern + parameters
          - implied_look: default material + color handling
          - implied_effects: default post-processing chain
          - physics_model: how the glyph wants to move
          - compositional_role: how it relates to other scene elements
          - implied_scene_behavior: particle emission, gravity wells, etc.

        Args:
            glyph: Single emoji character (e.g., '🔥')

        Returns:
            Complete semantic inference result with all OLAE defaults,
            or guidance for unknown glyphs.
        """
        result = find_text_primitive_by_glyph(glyph)
        if not result:
            # Unknown glyph — return sensible generic defaults
            return yaml.dump({
                "glyph": glyph,
                "known": False,
                "inference": "generic_defaults",
                "semantic_profile": {
                    "implied_object": {
                        "primitive": "emoji_glyph",
                        "render_mode": "billboard",
                    },
                    "implied_look": {
                        "material": "matte",
                        "color_mode": "glyph_native",
                        "fallback_palette": "monochrome",
                    },
                    "implied_action": {
                        "motion": "rotate",
                        "parameters": {"speed": 0.3, "axis": "y"},
                    },
                    "implied_effects": [],
                    "physics_model": "rigid",
                    "compositional_role": "anchor",
                    "semantic_tags": [],
                },
                "note": (
                    "This glyph is not in the taxonomy. Generic defaults applied. "
                    "Override any field to customize. Consider adding this glyph "
                    "to text_primitives.yaml if it's used frequently."
                ),
            }, default_flow_style=False, allow_unicode=True)

        category_name, entry_name, entry_data = result
        sp = entry_data.get("semantic_profile", {})

        return yaml.dump({
            "glyph": glyph,
            "known": True,
            "name": entry_data.get("name"),
            "category": category_name,
            "entry": entry_name,
            "description": entry_data.get("description"),
            "render_mode": entry_data.get("render_mode"),
            "semantic_profile": sp,
        }, default_flow_style=False, allow_unicode=True)

    @mcp.tool()
    def map_emoji_to_olae(
        glyph: str,
        material_override: str = "",
        motion_override: str = "",
        effects_override: str = "[]",
        color_palette_override: str = "",
        lighting_override: str = "",
        composition: str = "centered"
    ) -> str:
        """Map a single emoji to complete OLAE parameters, ready for rendering.

        Layer 2: Deterministic. Resolves the glyph's semantic profile into
        concrete Three.js-compatible parameters. User overrides replace
        inferred defaults selectively.

        This is the emoji equivalent of map_object_look_action_effect() —
        but starts from semantic inference rather than explicit specification.

        Args:
            glyph: Emoji character (e.g., '🔥')
            material_override: Replace inferred material (empty = use default)
            motion_override: Replace inferred motion (empty = use default)
            effects_override: JSON array of effect names to replace defaults
            color_palette_override: Replace inferred palette (empty = use default)
            lighting_override: Replace inferred lighting (empty = use default)
            composition: Spatial composition (default: "centered")

        Returns:
            Complete OLAE mapped parameters with render configuration.
        """
        # Get semantic profile
        lookup = find_text_primitive_by_glyph(glyph)
        if lookup:
            category_name, entry_name, entry_data = lookup
            sp = entry_data.get("semantic_profile", {})
        else:
            entry_data = {"glyph": glyph, "name": glyph, "render_mode": "billboard"}
            sp = {
                "implied_look": {"material": "matte", "color_mode": "glyph_native", "fallback_palette": "monochrome"},
                "implied_action": {"motion": "rotate", "parameters": {"speed": 0.3}},
                "implied_effects": [],
                "effect_intensities": {},
                "physics_model": "rigid",
                "compositional_role": "anchor",
                "semantic_tags": [],
            }

        # Resolve with overrides
        look = sp.get("implied_look", {})
        action = sp.get("implied_action", {})

        material = material_override or look.get("material", "matte")
        motion = motion_override or action.get("motion", "rotate")
        motion_params = action.get("parameters", {})

        color_mode = look.get("color_mode", "glyph_native")
        palette = color_palette_override or look.get("fallback_palette", "monochrome")

        # Resolve lighting from semantic tags if not overridden
        if not lighting_override:
            tags = sp.get("semantic_tags", [])
            lighting = "dramatic_side"  # default
            for tag in tags:
                affinity = get_tag_affinity(tag)
                if affinity and "preferred_lighting" in affinity:
                    lighting = affinity["preferred_lighting"]
                    break
        else:
            lighting = lighting_override

        # Resolve effects
        try:
            user_effects = json.loads(effects_override)
        except (json.JSONDecodeError, TypeError):
            user_effects = []

        if user_effects:
            effects = user_effects
            effect_intensities = {}
        else:
            effects = sp.get("implied_effects", [])
            effect_intensities = sp.get("effect_intensities", {})

        # Build result
        render_mode_name = entry_data.get("render_mode", "billboard")
        render_mode = get_render_mode(render_mode_name) or {}

        result = {
            "text_primitive": {
                "glyph": glyph,
                "name": entry_data.get("name", glyph),
                "render_mode": render_mode_name,
                "render_config": {
                    "geometry": render_mode.get("threejs_geometry", "PlaneGeometry"),
                    "texture_source": render_mode.get("texture_source", "canvas_2d"),
                    "canvas_resolution": render_mode.get("parameters", {}).get("canvas_resolution", 512),
                    "face_camera": render_mode.get("face_camera", True),
                    "material_interaction": render_mode.get("material_interaction", "limited"),
                },
            },
            "object": {
                "primitive": "emoji_glyph",
                "geometry_type": render_mode.get("threejs_geometry", "PlaneGeometry"),
                "parameters": {
                    "glyph": glyph,
                    "render_mode": render_mode_name,
                    "canvas_resolution": render_mode.get("parameters", {}).get("canvas_resolution", 512),
                },
            },
            "look": {
                "material": material,
                "color_mode": color_mode,
                "palette": palette,
            },
            "action": {
                "motion": motion,
                "parameters": motion_params,
                "secondary_motion": action.get("secondary_motion"),
                "secondary_parameters": action.get("secondary_parameters"),
            },
            "effects": [
                {
                    "effect": eff,
                    "intensity": effect_intensities.get(eff, 1.0),
                }
                for eff in effects
            ],
            "colors": {
                "palette": palette,
                "color_mode": color_mode,
            },
            "lighting": {
                "mood": lighting,
            },
            "composition": {
                "arrangement": composition,
            },
            "semantics": {
                "physics_model": sp.get("physics_model", "rigid"),
                "compositional_role": sp.get("compositional_role", "anchor"),
                "tags": sp.get("semantic_tags", []),
                "scene_behavior": sp.get("implied_scene_behavior", {}),
            },
        }

        return yaml.dump(result, default_flow_style=False, allow_unicode=True)

    @mcp.tool()
    def compose_emoji_scene(
        glyphs: str,
        auto_layout: bool = True,
        color_palette_override: str = "",
        lighting_override: str = ""
    ) -> str:
        """Compose multiple emoji into a scene graph with automatic layout.

        Layer 2: Deterministic. Takes a list of emoji and builds a complete
        scene graph using semantic inference for each glyph's role, position,
        motion, and relationships.

        The auto_layout system uses compositional_role from each glyph's
        semantic profile:
          anchor    → placed at scene center, scale 1.5
          satellite → orbits nearest anchor
          particle  → instanced swarm with cascade_delay
          background → placed behind, larger, lower opacity
          trigger   → initially hidden, timed appearance

        Args:
            glyphs: JSON array of glyph specs. Each spec is either:
                - A string (just the emoji, all defaults inferred):
                  ["🌍", "🚀", "✨"]
                - An object with overrides:
                  [{"glyph": "🌍", "scale": 2.0}, {"glyph": "🚀", "motion": "lissajous"}]
            auto_layout: Use role-based automatic positioning (default: true)
            color_palette_override: Override palette for entire scene
            lighting_override: Override lighting for entire scene

        Returns:
            Complete scene graph compatible with compose_scene() and
            generate_threejs_html().
        """
        try:
            specs = json.loads(glyphs)
        except json.JSONDecodeError as e:
            return f"Error parsing glyphs JSON: {e}"

        # Normalize specs
        normalized = []
        for spec in specs:
            if isinstance(spec, str):
                normalized.append({"glyph": spec})
            elif isinstance(spec, dict):
                normalized.append(spec)
            else:
                continue

        # Phase 1: Resolve semantics for each glyph
        resolved = []
        for i, spec in enumerate(normalized):
            glyph = spec.get("glyph", "❓")
            lookup = find_text_primitive_by_glyph(glyph)

            if lookup:
                _, entry_name, entry_data = lookup
                sp = entry_data.get("semantic_profile", {})
            else:
                entry_name = f"unknown_{i}"
                entry_data = {"glyph": glyph, "name": glyph, "render_mode": "billboard"}
                sp = {
                    "implied_action": {"motion": "rotate", "parameters": {"speed": 0.3}},
                    "implied_look": {"material": "matte"},
                    "implied_effects": [],
                    "physics_model": "rigid",
                    "compositional_role": "anchor",
                    "semantic_tags": [],
                }

            # Apply user overrides
            action = dict(sp.get("implied_action", {}))
            if "motion" in spec:
                action["motion"] = spec["motion"]
            if "speed" in spec:
                action.setdefault("parameters", {})["speed"] = spec["speed"]

            look = dict(sp.get("implied_look", {}))
            if "material" in spec:
                look["material"] = spec["material"]

            resolved.append({
                "id": spec.get("id", f"{entry_name}_{i}"),
                "glyph": glyph,
                "name": entry_data.get("name", glyph),
                "render_mode": spec.get("render_mode", entry_data.get("render_mode", "billboard")),
                "role": spec.get("role", sp.get("compositional_role", "anchor")),
                "physics": sp.get("physics_model", "rigid"),
                "tags": sp.get("semantic_tags", []),
                "action": action,
                "look": look,
                "effects": sp.get("implied_effects", []),
                "effect_intensities": sp.get("effect_intensities", {}),
                "scene_behavior": sp.get("implied_scene_behavior", {}),
                "user_position": spec.get("position"),
                "user_scale": spec.get("scale"),
                "user_rotation": spec.get("rotation"),
                "user_delay": spec.get("animation_delay"),
                "user_parent": spec.get("parent"),
            })

        # Phase 2: Auto-layout based on roles
        scene_nodes = []
        relationships = []
        anchor_ids = []

        for item in resolved:
            role = item["role"]
            role_spec = get_role_spec(role) or {}

            # Position
            if item["user_position"] is not None:
                position = item["user_position"]
            elif auto_layout:
                if role == "anchor":
                    # Stack anchors slightly apart if multiple
                    idx = len(anchor_ids)
                    offset = idx * 3.0  # 3 units apart
                    position = [offset - (len([r for r in resolved if r["role"] == "anchor"]) - 1) * 1.5, 0, 0]
                elif role == "background":
                    position = [0, 1.0, role_spec.get("default_position_z", -5.0)]
                elif role == "trigger":
                    position = [0, 2.0, 0]
                else:
                    position = [0, 0, 0]  # satellites/particles positioned by relationships
            else:
                position = [0, 0, 0]

            # Scale
            if item["user_scale"] is not None:
                scale = item["user_scale"]
            elif auto_layout:
                scale = role_spec.get("default_scale", 1.0)
            else:
                scale = 1.0

            if isinstance(scale, (int, float)):
                scale = [scale, scale, scale]

            node = {
                "id": item["id"],
                "text_primitive": {
                    "glyph": item["glyph"],
                    "name": item["name"],
                    "render_mode": item["render_mode"],
                },
                "object": {
                    "primitive": "emoji_glyph",
                    "parameters": {
                        "glyph": item["glyph"],
                        "render_mode": item["render_mode"],
                        "canvas_resolution": 512 if item["render_mode"] != "particle" else 256,
                    },
                },
                "look": {
                    "material": item["look"].get("material", "matte"),
                    "color_mode": item["look"].get("color_mode", "glyph_native"),
                    "palette": color_palette_override or item["look"].get("fallback_palette", "monochrome"),
                },
                "action": {
                    "motion": item["action"].get("motion", "rotate"),
                    "parameters": item["action"].get("parameters", {}),
                    "secondary_motion": item["action"].get("secondary_motion"),
                    "secondary_parameters": item["action"].get("secondary_parameters"),
                },
                "effects": [
                    {"effect": e, "intensity": item["effect_intensities"].get(e, 1.0)}
                    for e in item["effects"]
                ],
                "transform": {
                    "position": position,
                    "scale": scale,
                    "rotation": item.get("user_rotation", [0, 0, 0]),
                },
                "animation_delay": item.get("user_delay", 0.0),
                "parent": item.get("user_parent"),
                "semantics": {
                    "role": role,
                    "physics": item["physics"],
                    "tags": item["tags"],
                    "scene_behavior": item["scene_behavior"],
                },
            }

            scene_nodes.append(node)

            if role == "anchor":
                anchor_ids.append(item["id"])

        # Phase 3: Auto-generate relationships
        if auto_layout and anchor_ids:
            primary_anchor = anchor_ids[0]
            satellite_idx = 0

            for node in scene_nodes:
                role = node["semantics"]["role"]

                if role == "satellite" and not node.get("parent"):
                    # Orbit nearest anchor
                    target = primary_anchor
                    orbit_radius = 2.5 + satellite_idx * 0.8
                    orbit_speed = 0.5 - satellite_idx * 0.05

                    relationships.append({
                        "type": "orbit_around",
                        "source": node["id"],
                        "target": target,
                        "parameters": {
                            "radius": orbit_radius,
                            "speed": max(0.1, orbit_speed),
                        },
                    })

                    # Update position to orbit start
                    angle = satellite_idx * (2 * math.pi / max(1, len([
                        n for n in scene_nodes if n["semantics"]["role"] == "satellite"
                    ])))
                    node["transform"]["position"] = [
                        math.cos(angle) * orbit_radius,
                        0,
                        math.sin(angle) * orbit_radius,
                    ]
                    satellite_idx += 1

                elif role == "particle":
                    # Cascade delay swarm
                    behavior = node["semantics"].get("scene_behavior", {})
                    count = behavior.get("emission_rate", 12)
                    count = min(count, 30)  # cap for performance

                    relationships.append({
                        "type": "cascade_delay",
                        "source": node["id"],
                        "parameters": {
                            "count": count,
                            "delay_step": 0.2,
                            "arrangement": "radial",
                            "radius": 3.0,
                        },
                    })

        # Phase 4: Resolve scene-wide lighting from dominant tags
        if not lighting_override:
            all_tags = []
            for node in scene_nodes:
                all_tags.extend(node["semantics"].get("tags", []))
            # Most frequent tag wins
            tag_counts = {}
            for tag in all_tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            dominant_tag = max(tag_counts, key=tag_counts.get) if tag_counts else None
            if dominant_tag:
                affinity = get_tag_affinity(dominant_tag)
                scene_lighting = affinity.get("preferred_lighting", "dramatic_side") if affinity else "dramatic_side"
            else:
                scene_lighting = "dramatic_side"
        else:
            scene_lighting = lighting_override

        result = {
            "scene_graph": {
                "node_count": len(scene_nodes),
                "nodes": scene_nodes,
                "relationships": relationships,
                "scene_lighting": scene_lighting,
                "scene_palette": color_palette_override or "inferred_per_glyph",
            },
            "composition_summary": {
                "anchors": [n["id"] for n in scene_nodes if n["semantics"]["role"] == "anchor"],
                "satellites": [n["id"] for n in scene_nodes if n["semantics"]["role"] == "satellite"],
                "particles": [n["id"] for n in scene_nodes if n["semantics"]["role"] == "particle"],
                "backgrounds": [n["id"] for n in scene_nodes if n["semantics"]["role"] == "background"],
                "triggers": [n["id"] for n in scene_nodes if n["semantics"]["role"] == "trigger"],
            },
        }

        return yaml.dump(result, default_flow_style=False, allow_unicode=True)

    # ===== LAYER 2.5 — CODE GENERATION =====

    @mcp.tool()
    def generate_emoji_threejs_html(
        glyph: str,
        material_override: str = "",
        motion_override: str = "",
        effects: list[str] = [],
        color_palette: str = "",
        lighting: str = "",
        camera_distance: float = 5.0,
        animation_duration: float = 4.0,
        background_color: str = "#0a0a0a",
        background_type: str = "color",
        background_image_url: str = "",
        background_blur: float = 0.0,
        background_opacity: float = 1.0,
        camera_motion: str = "orbit",
        autoplay: bool = True
    ) -> str:
        """Generate self-contained Three.js HTML for an emoji primitive.

        Layer 2.5: Deterministic code generation. Combines semantic inference
        with the text primitive renderer to produce runnable HTML.

        The emoji is rendered as a CanvasTexture billboard with the inferred
        motion pattern, effects, and lighting applied.

        Args:
            glyph: Emoji character (e.g., '🔥')
            material_override: Override inferred material
            motion_override: Override inferred motion
            effects: Override inferred effects
            color_palette: Override inferred palette
            lighting: Override inferred lighting
            camera_distance: Camera distance from origin
            animation_duration: Loop duration in seconds
            background_color: CSS hex color (used for "color" type, fallback for others)
            background_type: Background rendering mode:
                "color" — solid CSS color (default, opaque canvas)
                "transparent" — alpha channel compositing (for layering over other content)
                "image" — background_image_url loaded as textured back-plane
            background_image_url: URL for background image (only used when background_type="image")
            background_blur: Blur amount for background image, 0.0-1.0 (0=sharp, 1=heavy blur)
            background_opacity: Background image opacity, 0.0-1.0
            camera_motion: Camera movement pattern (e.g., "orbit", "dolly_in",
                "flythrough", "crane_up", "static", "vertigo", "breathing").
                Independent from object motion.
            autoplay: Start animation immediately

        Returns:
            Complete self-contained HTML string.
        """
        # Resolve semantics
        lookup = find_text_primitive_by_glyph(glyph)
        if lookup:
            _, entry_name, entry_data = lookup
            sp = entry_data.get("semantic_profile", {})
        else:
            entry_data = {"glyph": glyph, "name": glyph, "render_mode": "billboard"}
            sp = {
                "implied_action": {"motion": "rotate", "parameters": {"speed": 0.3}},
                "implied_look": {"material": "matte", "fallback_palette": "monochrome"},
                "implied_effects": [],
                "effect_intensities": {},
                "semantic_tags": [],
            }

        action = sp.get("implied_action", {})
        look = sp.get("implied_look", {})

        motion_name = motion_override or action.get("motion", "rotate")
        motion_params = action.get("parameters", {})
        secondary = action.get("secondary_motion")
        secondary_params = action.get("secondary_parameters", {})

        resolved_effects = effects if effects else sp.get("implied_effects", [])
        effect_intensities = sp.get("effect_intensities", {})

        # Build motion JS
        motion_js = _build_emoji_motion_js(
            motion_name, motion_params, secondary, secondary_params, animation_duration
        )

        # Build camera JS (deferred import — avoid circular dependency)
        from motion_graphics_mcp import find_camera, _build_camera_js
        cam_data = find_camera(camera_motion)
        camera_js = _build_camera_js(cam_data, animation_duration)

        # Build effects JS
        has_bloom = "bloom" in resolved_effects
        bloom_intensity = effect_intensities.get("bloom", 0.5) if has_bloom else 0
        is_transparent = background_type == "transparent"
        is_image_bg = background_type == "image" and background_image_url

        # Determine lighting
        resolved_lighting = lighting
        if not resolved_lighting:
            for tag in sp.get("semantic_tags", []):
                aff = get_tag_affinity(tag)
                if aff and "preferred_lighting" in aff:
                    resolved_lighting = aff["preferred_lighting"]
                    break
        if not resolved_lighting:
            resolved_lighting = "dramatic_side"

        name = entry_data.get("name", glyph)
        canvas_res = 512

        # --- Background-dependent configuration ---

        # CSS body
        if is_transparent:
            body_css = "background: transparent;"
        else:
            body_css = f"background: {background_color};"

        # Renderer
        if is_transparent:
            renderer_js = "const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, premultipliedAlpha: false });"
            renderer_clear_js = "renderer.setClearColor(0x000000, 0);"
        else:
            renderer_js = "const renderer = new THREE.WebGLRenderer({ antialias: true });"
            renderer_clear_js = ""

        # Scene background
        if is_transparent:
            scene_bg_js = "// scene.background omitted — transparent compositing mode"
        elif is_image_bg:
            scene_bg_js = "// scene.background set by image loader below"
        else:
            scene_bg_js = f"scene.background = new THREE.Color('{background_color}');"

        # Ground plane
        if is_transparent:
            ground_js = "// Ground plane omitted — transparent compositing mode"
        else:
            ground_js = f"""const groundGeo = new THREE.PlaneGeometry(30, 30);
const groundMat = new THREE.MeshStandardMaterial({{
  color: new THREE.Color('{background_color}').multiplyScalar(0.8),
  metalness: 0.05,
  roughness: 0.9,
}});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -2.0;
scene.add(ground);"""

        # Background image loader
        if is_image_bg:
            bg_loader_js = f"""// — Background image (back-plane) —
const _bgLoader = new THREE.TextureLoader();
_bgLoader.load('{background_image_url}', function(_bgTex) {{
  _bgTex.encoding = THREE.sRGBEncoding;
  _bgTex.minFilter = THREE.LinearMipmapLinearFilter;
  _bgTex.generateMipmaps = true;
  const _bgGeo = new THREE.PlaneGeometry(80, 45);
  const _bgMat = new THREE.MeshBasicMaterial({{
    map: _bgTex,
    transparent: {str(background_opacity < 1.0).lower()},
    opacity: {background_opacity:.2f},
    depthWrite: false,
  }});
  const _bgMesh = new THREE.Mesh(_bgGeo, _bgMat);
  _bgMesh.position.z = -20;
  _bgMesh.renderOrder = -1;
  scene.add(_bgMesh);
}}, undefined, function(_err) {{
  console.warn('Background image failed to load:', _err);
  scene.background = new THREE.Color('{background_color}');
}});"""
        else:
            bg_loader_js = ""

        # --- Alpha-preserving bloom shader (transparent + bloom only) ---
        if is_transparent and has_bloom:
            bloom_setup_js = f"""// — Alpha-preserving bloom (render-target + shader) —
const _bloomStrength = {bloom_intensity};

const _rtOpts = {{
  format: THREE.RGBAFormat,
  type: THREE.UnsignedByteType,
  stencilBuffer: false,
  depthBuffer: true,
}};
const _bloomRT = new THREE.WebGLRenderTarget(
  window.innerWidth, window.innerHeight, _rtOpts);

const _bloomMat = new THREE.ShaderMaterial({{
  uniforms: {{
    tDiffuse: {{ value: null }},
    bloomStrength: {{ value: _bloomStrength }},
    resolution: {{ value: new THREE.Vector2(window.innerWidth, window.innerHeight) }},
  }},
  vertexShader: `
    varying vec2 vUv;
    void main() {{
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }}
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float bloomStrength;
    uniform vec2 resolution;
    varying vec2 vUv;

    void main() {{
      vec4 center = texture2D(tDiffuse, vUv);
      vec2 texel = 1.0 / resolution;

      // 7x7 Gaussian for bloom halo
      vec4 bloom = vec4(0.0);
      float total = 0.0;
      for (float x = -3.0; x <= 3.0; x += 1.0) {{
        for (float y = -3.0; y <= 3.0; y += 1.0) {{
          float w = exp(-(x*x + y*y) / 8.0);
          bloom += texture2D(tDiffuse, vUv + vec2(x, y) * texel * 3.0) * w;
          total += w;
        }}
      }}
      bloom /= total;

      vec3 bright = max(bloom.rgb - vec3(0.3), vec3(0.0));
      vec3 finalRGB = center.rgb + bright * bloomStrength * 1.5;

      // Alpha from particle sprite + bloom spread
      float bloomAlpha = max(max(bright.r, bright.g), bright.b) * bloomStrength * 2.0;
      float finalAlpha = min(center.a + bloomAlpha, 1.0);

      gl_FragColor = vec4(finalRGB, finalAlpha);
    }}
  `,
  transparent: true,
}});

const _postScene = new THREE.Scene();
const _postCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
_postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), _bloomMat));

window.addEventListener('resize', () => {{
  _bloomRT.setSize(window.innerWidth, window.innerHeight);
  _bloomMat.uniforms.resolution.value.set(window.innerWidth, window.innerHeight);
}});"""

            render_js = """// Render to offscreen target (preserves alpha)
  renderer.setRenderTarget(_bloomRT);
  renderer.setClearColor(0x000000, 0);
  renderer.clear();
  renderer.render(scene, camera);
  renderer.setRenderTarget(null);

  // Post-process with alpha-preserving bloom
  renderer.setClearColor(0x000000, 0);
  renderer.clear();
  _bloomMat.uniforms.tDiffuse.value = _bloomRT.texture;
  renderer.render(_postScene, _postCamera);"""

        elif is_transparent:
            bloom_setup_js = ""
            render_js = """renderer.setClearColor(0x000000, 0);
  renderer.clear();
  renderer.render(scene, camera);"""

        else:
            # Opaque mode — emissive approximation for bloom (original behavior)
            bloom_setup_js = ""
            render_js = "renderer.render(scene, camera);"

        # Emissive bloom (opaque mode only — transparent uses shader)
        if has_bloom and not is_transparent:
            emissive_js = f"""material.emissive = new THREE.Color(0xffffff);
material.emissiveIntensity = {bloom_intensity};"""
        else:
            emissive_js = ""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Emoji Motion — {glyph} {name}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ {body_css} overflow: hidden; }}
  canvas {{ display: block; width: 100%; height: 100vh; }}
</style>
</head>
<body>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
// — Scene setup —
const scene = new THREE.Scene();
{scene_bg_js}

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
const camDist = {camera_distance:.1f};
camera.position.set(0, camDist * 0.3, camDist);
camera.lookAt(0, 0, 0);

{renderer_js}
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
renderer.outputEncoding = THREE.sRGBEncoding;
{renderer_clear_js}
document.body.appendChild(renderer.domElement);

{bg_loader_js}

// — Emoji Canvas Texture —
const emojiCanvas = document.createElement('canvas');
emojiCanvas.width = {canvas_res};
emojiCanvas.height = {canvas_res};
const ctx = emojiCanvas.getContext('2d');

// Render emoji to canvas
ctx.clearRect(0, 0, {canvas_res}, {canvas_res});
ctx.font = '{int(canvas_res * 0.78)}px serif';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText('{glyph}', {canvas_res // 2}, {canvas_res // 2});

const emojiTexture = new THREE.CanvasTexture(emojiCanvas);
emojiTexture.minFilter = THREE.LinearFilter;
emojiTexture.magFilter = THREE.LinearFilter;

// — Emoji Mesh —
const geometry = new THREE.PlaneGeometry(2, 2);
const material = new THREE.MeshBasicMaterial({{
  map: emojiTexture,
  transparent: true,
  alphaTest: 0.01,
  side: THREE.DoubleSide,
}});
{emissive_js}

const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// — Lighting —
const hemiLight = new THREE.HemisphereLight(0x8888cc, 0x222244, 0.6);
scene.add(hemiLight);
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.0);
dirLight.position.set(5, 8, 5);
scene.add(dirLight);
const rimLight = new THREE.PointLight(0x4488ff, 0.4, 15);
rimLight.position.set(-4, 3, -4);
scene.add(rimLight);

// — Ground plane —
{ground_js}

{bloom_setup_js}

// — Animation —
const clock = new THREE.Clock();
const duration = {animation_duration};
{'clock.start();' if autoplay else ''}

function animate() {{
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();
  const t = (elapsed % duration) / duration;

  // Billboard: always face camera
  mesh.lookAt(camera.position);

  // Camera motion
{camera_js}

  // Semantic motion
{motion_js}

  {render_js}
}}

animate();

// — Responsive —
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});
</script>
</body>
</html>"""

        return html


# ---------------------------------------------------------------------------
# CODE GENERATION HELPERS (module-level)
# ---------------------------------------------------------------------------

def _build_emoji_motion_js(
    motion: str,
    params: dict,
    secondary: Optional[str],
    secondary_params: Optional[dict],
    duration: float
) -> str:
    """Generate animation JS for emoji primitives.

    Similar to _build_motion_js but adapted for billboard meshes
    where rotation.y doesn't make visual sense (they face camera).
    Motion is expressed through position, scale, and opacity.
    """
    speed = params.get("speed", 1.0)
    if isinstance(speed, dict):
        speed = speed.get("default", 1.0)
    amplitude = params.get("amplitude", 0.5)
    if isinstance(amplitude, dict):
        amplitude = amplitude.get("default", 0.5)

    lines = []

    # Primary motion
    if "oscillat" in motion or "float" in motion or "bounce" in motion:
        drift_x = params.get("drift_x", 0)
        drift_y = params.get("drift_y", 0)
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {speed} * Math.PI * 2) * {amplitude};")
        if drift_x:
            lines.append(f"  mesh.position.x += {drift_x} * 0.016;")  # per-frame drift
        if drift_y and drift_y < 0:
            lines.append(f"  mesh.position.y += {drift_y} * elapsed;")  # descent

    elif "orbit" in motion:
        radius = params.get("radius", 2.0)
        if isinstance(radius, dict):
            radius = radius.get("default", 2.0)
        lines.append(f"  mesh.position.x = Math.cos(elapsed * {speed}) * {radius};")
        lines.append(f"  mesh.position.z = Math.sin(elapsed * {speed}) * {radius};")

    elif "lissajous" in motion:
        freq_a = params.get("frequency_a", 3)
        freq_b = params.get("frequency_b", 2)
        if isinstance(freq_a, dict):
            freq_a = freq_a.get("default", 3)
        if isinstance(freq_b, dict):
            freq_b = freq_b.get("default", 2)
        lines.append(f"  mesh.position.x = Math.sin(elapsed * {freq_a} * {speed}) * {amplitude};")
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {freq_b} * {speed}) * {amplitude};")

    elif "scale_pulse" in motion or "pulse" in motion:
        lines.append(f"  const s = 1.0 + Math.sin(elapsed * {speed} * Math.PI * 2) * {amplitude};")
        lines.append(f"  mesh.scale.set(s, s, s);")

    elif "wave" in motion:
        wavelength = params.get("wavelength", 3.0)
        direction = params.get("direction", "x")
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {speed} * Math.PI * 2) * {amplitude};")
        if direction == "x":
            lines.append(f"  mesh.position.x = Math.sin(elapsed * {speed} * 0.5) * {wavelength * 0.3};")

    elif "snap" in motion:
        sharpness = params.get("snap_sharpness", 0.9)
        rest = params.get("rest_fraction", 0.7)
        lines.append(f"  const snapT = (elapsed * {speed}) % 1.0;")
        lines.append(f"  const snapScale = snapT < {rest} ? 1.0 : 1.0 + Math.pow((snapT - {rest}) / (1.0 - {rest}), 0.3) * {amplitude};")
        lines.append(f"  mesh.scale.set(snapScale, snapScale, snapScale);")

    elif "rotat" in motion:
        # For billboards, express rotation as gentle position oscillation
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {speed} * 0.5) * 0.15;")
        lines.append(f"  mesh.position.x = Math.sin(elapsed * {speed} * 0.3) * 0.1;")

    else:
        # Generic gentle float
        lines.append(f"  mesh.position.y = Math.sin(elapsed * 0.7) * 0.2;")

    # Secondary motion (additive)
    if secondary and secondary_params:
        sec_speed = secondary_params.get("speed", 1.0)
        sec_amp = secondary_params.get("amplitude", 0.1)

        if "scale" in secondary or "pulse" in secondary:
            lines.append(f"  // Secondary: {secondary}")
            lines.append(f"  const s2 = 1.0 + Math.sin(elapsed * {sec_speed} * Math.PI * 2) * {sec_amp};")
            lines.append(f"  mesh.scale.multiplyScalar(s2);")
        elif "oscillat" in secondary:
            axis = secondary_params.get("axis", "x")
            if axis == "x":
                lines.append(f"  mesh.position.x += Math.sin(elapsed * {sec_speed}) * {sec_amp};")
            elif axis == "y":
                lines.append(f"  mesh.position.y += Math.sin(elapsed * {sec_speed}) * {sec_amp};")
        elif "rotat" in secondary:
            # Slight tilt oscillation for extruded mode
            lines.append(f"  // Secondary rotation (visual tilt)")
            lines.append(f"  mesh.rotation.z = Math.sin(elapsed * {sec_speed}) * 0.1;")

    return "\n".join(lines)
