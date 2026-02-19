"""
Motion Graphics MCP Server — Extended
Adds three capability layers to the base server:

1. CODE GENERATION (Layer 2.5): Emit runnable Three.js HTML from mapped parameters
2. POST-PROCESSING: New EFFECT dimension extending OBJECT × LOOK × ACTION → O × L × A × E
3. SCENE GRAPH: Multi-object composition with spatial relationships and staggered timing

Orbit Composer Integration:
- Phase position → keyframe timing / effect intensity
- Domain dominance → which OLA parameters are emphasized
- Beat frequencies → scene transition timing
- orbit_affinity fields on post-processing → phase-driven effect modulation

Three-Layer Architecture:
Layer 1 (Foundation - 0 tokens): Pure taxonomy lookup from olog files
Layer 2 (Structure - 0 tokens): Deterministic parameter mapping + code generation
Layer 3 (Contextual - varies): Creative synthesis by Claude
"""

from fastmcp import FastMCP
import yaml
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Optional

mcp = FastMCP("Motion Graphics MCP")

# Load taxonomy from olog files
OLOG_DIR = Path(__file__).parent / "ologs"


def load_olog(filename: str) -> Dict[str, Any]:
    """Load YAML olog file"""
    with open(OLOG_DIR / filename, 'r') as f:
        return yaml.safe_load(f)


# Layer 1: Load all taxonomies (happens once at startup, zero runtime cost)
GEOMETRIC_PRIMITIVES = load_olog("geometric_primitives.yaml")
MATERIAL_SYSTEMS = load_olog("material_systems.yaml")
MOTION_PATTERNS = load_olog("motion_patterns.yaml")
COLORS_LIGHTING = load_olog("colors_lighting_composition.yaml")
POST_PROCESSING = load_olog("post_processing.yaml")
CAMERA_MOVEMENTS = load_olog("camera_movements.yaml")

# Text primitives extension
from text_primitives_ext import register_text_primitive_tools, TEXT_PRIMITIVES
register_text_primitive_tools(mcp)

# ========== LOOKUP HELPERS ==========

def find_primitive(primitive_name: str) -> Optional[Dict[str, Any]]:
    for category in GEOMETRIC_PRIMITIVES.values():
        if isinstance(category, dict) and primitive_name in category:
            return category[primitive_name]
    return None


def find_material(material_name: str) -> Optional[Dict[str, Any]]:
    for category in MATERIAL_SYSTEMS.values():
        if isinstance(category, dict) and material_name in category:
            return category[material_name]
    return None


def find_motion(motion_name: str) -> Optional[Dict[str, Any]]:
    for category in MOTION_PATTERNS.values():
        if isinstance(category, dict) and motion_name in category:
            return category[motion_name]
    return None


def find_effect(effect_name: str) -> Optional[Dict[str, Any]]:
    if effect_name in POST_PROCESSING and effect_name != "intentionality":
        return POST_PROCESSING[effect_name]
    return None


def find_camera(camera_name: str) -> Optional[Dict[str, Any]]:
    if camera_name in CAMERA_MOVEMENTS and camera_name != "intentionality":
        return CAMERA_MOVEMENTS[camera_name]
    return None


# ========== LAYER 1 TOOLS — Pure Taxonomy Enumeration ==========

@mcp.tool()
def list_geometric_primitives() -> str:
    """List all available geometric primitives with descriptions.

    Returns formatted overview of OBJECT options — the foundational
    geometric forms available for motion graphics.
    """
    result = ["# Available Geometric Primitives\n"]
    for category_name, category_data in GEOMETRIC_PRIMITIVES.items():
        if category_name == "intentionality":
            continue
        result.append(f"\n## {category_name.replace('_', ' ').title()}\n")
        for prim_name, prim_data in category_data.items():
            result.append(f"**{prim_name}**: {prim_data['name']}")
            result.append(f"  - {prim_data['description']}")
            result.append(f"  - Complexity: {prim_data['complexity']}")
            result.append(f"  - Character: {prim_data['visual_character']}\n")
    return "\n".join(result)


@mcp.tool()
def list_material_systems() -> str:
    """List all available material systems with descriptions.

    Returns formatted overview of LOOK options — material/surface
    treatments that define visual appearance.
    """
    result = ["# Available Material Systems\n"]
    for category_name, category_data in MATERIAL_SYSTEMS.items():
        if category_name == "intentionality":
            continue
        result.append(f"\n## {category_name.replace('_', ' ').title()}\n")
        for mat_name, mat_data in category_data.items():
            result.append(f"**{mat_name}**: {mat_data['name']}")
            result.append(f"  - {mat_data['description']}")
            result.append(f"  - Character: {mat_data['visual_character']}")
            result.append(f"  - Lighting: {mat_data['lighting_response']}\n")
    return "\n".join(result)


@mcp.tool()
def list_motion_patterns() -> str:
    """List all available motion patterns with descriptions.

    Returns formatted overview of ACTION options — movement behaviors
    that create temporal dynamics.
    """
    result = ["# Available Motion Patterns\n"]
    for category_name, category_data in MOTION_PATTERNS.items():
        if category_name == "intentionality":
            continue
        result.append(f"\n## {category_name.replace('_', ' ').title()}\n")
        for motion_name, motion_data in category_data.items():
            result.append(f"**{motion_name}**: {motion_data['name']}")
            result.append(f"  - {motion_data['description']}")
            result.append(f"  - Character: {motion_data['visual_character']}")
            result.append(f"  - Pattern: {motion_data['temporal_pattern']}\n")
    return "\n".join(result)


@mcp.tool()
def list_color_palettes() -> str:
    """List all available color palettes."""
    result = ["# Available Color Palettes\n"]
    for palette_name, palette_data in COLORS_LIGHTING["color_palettes"].items():
        result.append(f"\n**{palette_name}**: {palette_data['name']}")
        result.append(f"  - Mood: {palette_data['mood']}")
        result.append(f"  - Colors: {', '.join(palette_data['colors'])}")
        result.append(f"  - Use cases: {', '.join(palette_data['use_cases'])}\n")
    return "\n".join(result)


@mcp.tool()
def list_lighting_moods() -> str:
    """List all available lighting configurations."""
    result = ["# Available Lighting Moods\n"]
    for lighting_name, lighting_data in COLORS_LIGHTING["lighting_moods"].items():
        result.append(f"\n**{lighting_name}**: {lighting_data['name']}")
        result.append(f"  - {lighting_data['description']}")
        result.append(f"  - Mood: {lighting_data['mood']}")
        result.append(f"  - Shadows: {lighting_data['shadow_quality']}")
        result.append(f"  - Lights: {len(lighting_data['lights'])} sources\n")
    return "\n".join(result)


@mcp.tool()
def list_spatial_compositions() -> str:
    """List all available spatial composition patterns."""
    result = ["# Available Spatial Compositions\n"]
    for comp_name, comp_data in COLORS_LIGHTING["spatial_compositions"].items():
        result.append(f"\n**{comp_name}**: {comp_data['name']}")
        result.append(f"  - {comp_data['description']}")
        result.append(f"  - Objects: {comp_data['object_count']}")
        result.append(f"  - Balance: {comp_data['visual_balance']}\n")
    return "\n".join(result)


@mcp.tool()
def list_post_processing_effects() -> str:
    """List all available post-processing effects.

    Returns formatted overview of EFFECT options — the fourth dimension
    extending OBJECT × LOOK × ACTION into O × L × A × E.

    Each effect includes orbit_affinity indicating which orbit phase
    and parameter it responds to most naturally.
    """
    result = ["# Available Post-Processing Effects\n"]
    for effect_name, effect_data in POST_PROCESSING.items():
        if effect_name == "intentionality":
            continue
        affinity = effect_data.get("orbit_affinity", {})
        result.append(f"\n**{effect_name}**: {effect_data['name']}")
        result.append(f"  - {effect_data['description']}")
        result.append(f"  - Character: {effect_data['visual_character']}")
        result.append(f"  - Three.js pass: {effect_data['threejs_pass']}")
        if affinity:
            result.append(f"  - Orbit affinity: peaks at {affinity.get('peaks_at', '?')}, "
                          f"driven by {affinity.get('driven_by', '?')}")
        result.append("")
    return "\n".join(result)


@mcp.tool()
def list_camera_movements() -> str:
    """List all available camera movement patterns.

    Returns formatted overview of CAMERA options — the narrative dimension
    describing the viewer's emotional relationship to the scene.

    Independent from ACTION (object motion). These compose:
    a pulsing object + dolly_in ≠ pulsing object + crane_up.

    Each movement includes orbit_affinity for phase-driven selection.
    """
    result = ["# Available Camera Movements\n"]
    for cam_name, cam_data in CAMERA_MOVEMENTS.items():
        if cam_name == "intentionality":
            continue
        affinity = cam_data.get("orbit_affinity", {})
        result.append(f"\n**{cam_name}**: {cam_data['name']}")
        result.append(f"  - {cam_data['description']}")
        result.append(f"  - Character: {cam_data['visual_character']}")
        result.append(f"  - Mood: {', '.join(cam_data.get('narrative_mood', []))}")
        result.append(f"  - Type: {cam_data['animation_type']}")
        if affinity:
            result.append(f"  - Orbit affinity: peaks at {affinity.get('peaks_at', '?')}, "
                          f"driven by {affinity.get('driven_by', '?')}")
        result.append("")
    return "\n".join(result)


@mcp.tool()
def get_camera_parameters(camera_name: str) -> str:
    """Get complete parameters for a camera movement.

    Layer 2 deterministic lookup — maps camera name to animation
    configuration and narrative metadata.

    Args:
        camera_name: Name of camera movement (e.g., "dolly_in", "flythrough", "orbit")

    Returns:
        Complete camera specification including parameters, narrative mood,
        and orbit affinity.
    """
    cam = find_camera(camera_name)
    if not cam:
        available = [k for k in CAMERA_MOVEMENTS.keys() if k != "intentionality"]
        return f"Error: Camera movement '{camera_name}' not found. Available: {available}"
    result = {
        "camera_movement": camera_name,
        "name": cam["name"],
        "description": cam["description"],
        "animation_type": cam["animation_type"],
        "parameters": cam["parameters"],
        "narrative_mood": cam.get("narrative_mood", []),
        "visual_character": cam["visual_character"],
        "orbit_affinity": cam.get("orbit_affinity", {}),
    }
    return json.dumps(result, indent=2)


# ========== LAYER 2 TOOLS — Deterministic Mapping ==========

@mcp.tool()
def get_primitive_parameters(primitive_name: str) -> str:
    """Get complete Three.js parameters for a geometric primitive.
    Layer 2 deterministic lookup."""
    prim = find_primitive(primitive_name)
    if not prim:
        return f"Error: Primitive '{primitive_name}' not found in taxonomy"
    result = {
        "primitive": primitive_name,
        "name": prim["name"],
        "description": prim["description"],
        "geometry_type": prim.get("threejs_geometry") or prim.get("custom_geometry"),
        "parameters": prim["parameters"],
        "complexity": prim["complexity"],
        "visual_character": prim["visual_character"]
    }
    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def get_material_parameters(material_name: str) -> str:
    """Get complete Three.js material parameters.
    Layer 2 deterministic lookup."""
    mat = find_material(material_name)
    if not mat:
        return f"Error: Material '{material_name}' not found in taxonomy"
    result = {
        "material": material_name,
        "name": mat["name"],
        "description": mat["description"],
        "material_type": mat.get("threejs_material") or mat.get("custom_material"),
        "parameters": mat["parameters"],
        "visual_character": mat["visual_character"],
        "lighting_response": mat["lighting_response"]
    }
    if "use_cases" in mat:
        result["use_cases"] = mat["use_cases"]
    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def get_motion_parameters(motion_name: str) -> str:
    """Get complete animation parameters for a motion pattern.
    Layer 2 deterministic lookup."""
    motion = find_motion(motion_name)
    if not motion:
        return f"Error: Motion '{motion_name}' not found in taxonomy"
    result = {
        "motion": motion_name,
        "name": motion["name"],
        "description": motion["description"],
        "animation_type": motion["animation_type"],
        "parameters": motion["parameters"],
        "visual_character": motion["visual_character"],
        "temporal_pattern": motion["temporal_pattern"]
    }
    if "physics_model" in motion:
        result["physics_model"] = motion["physics_model"]
    if "mathematical_form" in motion:
        result["mathematical_form"] = motion["mathematical_form"]
    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def get_effect_parameters(effect_name: str) -> str:
    """Get complete post-processing effect parameters.

    Layer 2 deterministic lookup — maps effect name to Three.js
    EffectComposer pass configuration.

    Args:
        effect_name: Name of effect (e.g., "bloom", "chromatic_aberration", "film_grain")

    Returns:
        Complete effect specification including orbit affinity
    """
    effect = find_effect(effect_name)
    if not effect:
        available = [k for k in POST_PROCESSING.keys() if k != "intentionality"]
        return f"Error: Effect '{effect_name}' not found. Available: {available}"
    result = {
        "effect": effect_name,
        "name": effect["name"],
        "description": effect["description"],
        "threejs_pass": effect["threejs_pass"],
        "parameters": effect["parameters"],
        "visual_character": effect["visual_character"],
        "intensity_range": effect["intensity_range"],
        "orbit_affinity": effect.get("orbit_affinity", {})
    }
    if "shader" in effect:
        result["shader"] = effect["shader"]
    if "import_path" in effect:
        result["import_path"] = effect["import_path"]
    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def map_object_look_action(
    primitive: str,
    material: str,
    motion: str,
    color_palette: str = "cyberpunk",
    lighting: str = "dramatic_side",
    composition: str = "centered"
) -> str:
    """Map OBJECT/LOOK/ACTION to complete Three.js parameters.
    Layer 2 deterministic assembly."""
    prim = find_primitive(primitive)
    mat = find_material(material)
    mot = find_motion(motion)
    if not prim:
        return f"Error: Primitive '{primitive}' not found"
    if not mat:
        return f"Error: Material '{material}' not found"
    if not mot:
        return f"Error: Motion '{motion}' not found"

    palette = COLORS_LIGHTING["color_palettes"].get(color_palette)
    lights = COLORS_LIGHTING["lighting_moods"].get(lighting)
    comp = COLORS_LIGHTING["spatial_compositions"].get(composition)

    result = {
        "object": {
            "primitive": primitive,
            "geometry_type": prim.get("threejs_geometry") or prim.get("custom_geometry"),
            "parameters": prim["parameters"],
            "complexity": prim["complexity"]
        },
        "look": {
            "material": material,
            "material_type": mat.get("threejs_material") or mat.get("custom_material"),
            "parameters": mat["parameters"]
        },
        "action": {
            "motion": motion,
            "animation_type": mot["animation_type"],
            "parameters": mot["parameters"]
        },
        "colors": {
            "palette": color_palette,
            "values": palette["colors"] if palette else []
        },
        "lighting": {
            "mood": lighting,
            "lights": lights["lights"] if lights else []
        },
        "composition": {
            "arrangement": composition,
            "details": comp if comp else {}
        }
    }
    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def map_object_look_action_effect(
    primitive: str,
    material: str,
    motion: str,
    effects: list[str] = [],
    color_palette: str = "cyberpunk",
    lighting: str = "dramatic_side",
    composition: str = "centered",
    effect_intensities: dict = {}
) -> str:
    """Map OBJECT/LOOK/ACTION/EFFECT to complete Three.js parameters.

    Extended Layer 2 — adds post-processing effects as fourth dimension.
    Effects compose additively in the EffectComposer pipeline.

    Args:
        primitive: Geometric primitive name
        material: Material system name
        motion: Motion pattern name
        effects: List of post-processing effect names (e.g., ["bloom", "film_grain"])
        color_palette: Color scheme (default: "cyberpunk")
        lighting: Lighting mood (default: "dramatic_side")
        composition: Spatial composition (default: "centered")
        effect_intensities: Optional intensity overrides {effect_name: 0.0-1.0}

    Returns:
        Complete OLAE mapped parameters
    """
    # Get base OLA mapping
    base_yaml = map_object_look_action(
        primitive, material, motion,
        color_palette, lighting, composition
    )
    if base_yaml.startswith("Error"):
        return base_yaml

    base = yaml.safe_load(base_yaml)

    # Add effects
    effect_specs = []
    for effect_name in effects:
        effect = find_effect(effect_name)
        if not effect:
            continue

        intensity = effect_intensities.get(effect_name, 1.0)
        params = dict(effect["parameters"])

        # Scale numeric parameters by intensity
        for key, val in params.items():
            if isinstance(val, (int, float)):
                lo, hi = effect["intensity_range"]
                params[key] = val * intensity

        effect_specs.append({
            "effect": effect_name,
            "threejs_pass": effect["threejs_pass"],
            "parameters": params,
            "orbit_affinity": effect.get("orbit_affinity", {}),
            "import_path": effect.get("import_path")
        })

    base["effects"] = effect_specs
    return yaml.dump(base, default_flow_style=False)


# ========== SCENE GRAPH — Multi-Object Composition ==========

@mcp.tool()
def compose_scene(
    elements: str,
    relationships: str = "[]"
) -> str:
    """Compose multiple OLA(E) triples into a scene graph.

    Layer 2: Builds a scene tree from taxonomy entries with spatial
    relationships and staggered animation timing.

    Each element is an OLA specification with position/scale/rotation.
    Relationships define how elements interact spatially and temporally.

    Args:
        elements: JSON array of element specs, each with:
            - id: unique string identifier
            - primitive, material, motion: taxonomy names
            - effects: optional list of effect names
            - position: [x, y, z] (default: [0, 0, 0])
            - scale: [x, y, z] or float (default: 1.0)
            - rotation: [x, y, z] in radians (default: [0, 0, 0])
            - animation_delay: seconds offset (default: 0.0)
            - parent: id of parent element (optional)

        relationships: JSON array of relationship specs:
            - type: "orbit_around" | "mirror" | "cascade_delay" | "face_toward" | "array_radial"
            - source: element id
            - target: element id (or parameters)
            - parameters: relationship-specific config

    Returns:
        Complete scene graph with resolved parameters

    Example elements:
        [
            {"id": "core", "primitive": "icosahedron", "material": "metallic",
             "motion": "rotate", "position": [0, 0, 0]},
            {"id": "ring1", "primitive": "torus", "material": "glass",
             "motion": "orbit", "parent": "core", "animation_delay": 0.5}
        ]

    Example relationships:
        [
            {"type": "orbit_around", "source": "ring1", "target": "core",
             "parameters": {"radius": 3.0, "speed": 0.5}},
            {"type": "cascade_delay", "source": "ring1",
             "parameters": {"count": 5, "delay_step": 0.3, "arrangement": "radial"}}
        ]
    """
    try:
        elems = json.loads(elements)
        rels = json.loads(relationships)
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {e}"

    scene_nodes = []
    errors = []

    for elem in elems:
        eid = elem.get("id", f"elem_{len(scene_nodes)}")

        # Look up taxonomy entries
        prim = find_primitive(elem.get("primitive", "sphere"))
        mat = find_material(elem.get("material", "metallic"))
        mot = find_motion(elem.get("motion", "rotate"))

        if not prim:
            errors.append(f"{eid}: primitive '{elem.get('primitive')}' not found")
            continue
        if not mat:
            errors.append(f"{eid}: material '{elem.get('material')}' not found")
            continue
        if not mot:
            errors.append(f"{eid}: motion '{elem.get('motion')}' not found")
            continue

        # Resolve effects
        effect_specs = []
        for eff_name in elem.get("effects", []):
            eff = find_effect(eff_name)
            if eff:
                effect_specs.append({
                    "effect": eff_name,
                    "threejs_pass": eff["threejs_pass"],
                    "parameters": eff["parameters"]
                })

        # Normalize scale
        scale = elem.get("scale", 1.0)
        if isinstance(scale, (int, float)):
            scale = [scale, scale, scale]

        node = {
            "id": eid,
            "object": {
                "primitive": elem.get("primitive"),
                "geometry_type": prim.get("threejs_geometry") or prim.get("custom_geometry"),
                "parameters": prim["parameters"],
            },
            "look": {
                "material": elem.get("material"),
                "material_type": mat.get("threejs_material") or mat.get("custom_material"),
                "parameters": mat["parameters"],
            },
            "action": {
                "motion": elem.get("motion"),
                "animation_type": mot["animation_type"],
                "parameters": mot["parameters"],
            },
            "transform": {
                "position": elem.get("position", [0, 0, 0]),
                "scale": scale,
                "rotation": elem.get("rotation", [0, 0, 0]),
            },
            "animation_delay": elem.get("animation_delay", 0.0),
            "parent": elem.get("parent"),
            "effects": effect_specs,
        }
        scene_nodes.append(node)

    # Expand relationships
    expanded_relationships = []
    generated_nodes = []

    for rel in rels:
        rel_type = rel.get("type")
        source = rel.get("source")
        target = rel.get("target")
        params = rel.get("parameters", {})

        if rel_type == "cascade_delay":
            # Generate copies of source element with staggered timing
            count = params.get("count", 5)
            delay_step = params.get("delay_step", 0.3)
            arrangement = params.get("arrangement", "radial")

            source_node = next((n for n in scene_nodes if n["id"] == source), None)
            if not source_node:
                errors.append(f"cascade_delay: source '{source}' not found")
                continue

            for i in range(1, count):
                clone = json.loads(json.dumps(source_node))
                clone["id"] = f"{source}_cascade_{i}"
                clone["animation_delay"] = source_node["animation_delay"] + delay_step * i

                if arrangement == "radial":
                    angle = (2 * math.pi * i) / count
                    radius = params.get("radius", 2.0)
                    clone["transform"]["position"] = [
                        math.cos(angle) * radius,
                        0,
                        math.sin(angle) * radius
                    ]
                elif arrangement == "linear":
                    spacing = params.get("spacing", 1.5)
                    clone["transform"]["position"] = [spacing * i, 0, 0]

                generated_nodes.append(clone)

            expanded_relationships.append({
                "type": "cascade_delay",
                "source": source,
                "generated_count": count - 1,
                "generated_ids": [f"{source}_cascade_{i}" for i in range(1, count)],
            })

        elif rel_type == "orbit_around":
            expanded_relationships.append({
                "type": "orbit_around",
                "source": source,
                "target": target,
                "orbit_radius": params.get("radius", 3.0),
                "orbit_speed": params.get("speed", 0.5),
                "orbit_axis": params.get("axis", [0, 1, 0]),
            })

        elif rel_type == "mirror":
            source_node = next((n for n in scene_nodes if n["id"] == source), None)
            if source_node:
                clone = json.loads(json.dumps(source_node))
                clone["id"] = f"{source}_mirror"
                axis = params.get("axis", "x")
                pos = list(clone["transform"]["position"])
                idx = {"x": 0, "y": 1, "z": 2}.get(axis, 0)
                pos[idx] = -pos[idx]
                clone["transform"]["position"] = pos
                generated_nodes.append(clone)
                expanded_relationships.append({
                    "type": "mirror",
                    "source": source,
                    "mirror_id": clone["id"],
                    "axis": axis,
                })

        elif rel_type == "face_toward":
            expanded_relationships.append({
                "type": "face_toward",
                "source": source,
                "target": target,
                "continuous": params.get("continuous", True),
            })

    scene_nodes.extend(generated_nodes)

    result = {
        "scene_graph": {
            "node_count": len(scene_nodes),
            "nodes": scene_nodes,
            "relationships": expanded_relationships,
        },
        "errors": errors if errors else None,
    }

    return yaml.dump(result, default_flow_style=False)


# ========== CODE GENERATION — Layer 2.5 ==========

@mcp.tool()
def generate_threejs_html(
    primitive: str,
    material: str,
    motion: str,
    effects: list[str] = [],
    color_palette: str = "cyberpunk",
    lighting: str = "dramatic_side",
    camera_distance: float = 5.0,
    animation_duration: float = 4.0,
    background_color: str = "#0a0a0a",
    background_type: str = "color",
    background_image_url: str = "",
    background_blur: float = 0.0,
    background_opacity: float = 1.0,
    camera_motion: str = "orbit",
    resolution: str = "1080p",
    autoplay: bool = True
) -> str:
    """Generate self-contained Three.js HTML from mapped parameters.

    Layer 2.5: Deterministic code generation — templates taxonomy values
    into runnable HTML. Zero LLM cost. Output renders in browser or
    Claude artifact preview.

    Args:
        primitive: Geometric primitive name
        material: Material system name
        motion: Motion pattern name
        effects: Post-processing effects to apply
        color_palette: Color scheme name
        lighting: Lighting mood name
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
        camera_motion: Camera movement pattern from taxonomy (e.g., "orbit",
            "dolly_in", "flythrough", "crane_up", "whip_pan", "static",
            "vertigo", "breathing"). Independent from object motion (ACTION).
        resolution: "720p", "1080p", or "4k"
        autoplay: Start animation immediately

    Returns:
        Complete self-contained HTML string ready to save and open
    """
    prim = find_primitive(primitive)
    mat = find_material(material)
    mot = find_motion(motion)

    if not prim:
        return f"Error: Primitive '{primitive}' not found"
    if not mat:
        return f"Error: Material '{material}' not found"
    if not mot:
        return f"Error: Motion '{motion}' not found"

    palette = COLORS_LIGHTING["color_palettes"].get(color_palette, {})
    lights_config = COLORS_LIGHTING["lighting_moods"].get(lighting, {})

    res_map = {"720p": (1280, 720), "1080p": (1920, 1080), "4k": (3840, 2160)}
    width, height = res_map.get(resolution, (1920, 1080))

    # Build geometry JS
    geom_type = prim.get("threejs_geometry", "SphereGeometry")
    geom_params = prim.get("parameters", {})
    geometry_js = _build_geometry_js(geom_type, geom_params)

    # Build material JS
    mat_type = mat.get("threejs_material", "MeshStandardMaterial")
    mat_params = mat.get("parameters", {})
    palette_colors = palette.get("colors", ["#ffffff"])
    material_js = _build_material_js(mat_type, mat_params, palette_colors)

    # Build animation JS
    motion_js = _build_motion_js(mot, animation_duration)

    # Build lights JS
    lights_js = _build_lights_js(lights_config)

    # Build camera JS
    cam_data = find_camera(camera_motion)
    camera_js = _build_camera_js(cam_data, animation_duration)

    # Build post-processing JS (transparent mode gets alpha-preserving bloom shader)
    effects_data = []
    for eff_name in effects:
        eff = find_effect(eff_name)
        if eff:
            effects_data.append((eff_name, eff))
    is_transparent = background_type == "transparent"
    postproc_imports, postproc_setup, postproc_render = _build_postprocessing_js(
        effects_data, transparent=is_transparent)

    # Determine if material needs envmap (metallic or physical with reflectivity)
    needs_envmap = mat_type in ("MeshStandardMaterial", "MeshPhysicalMaterial")

    # Background-dependent configuration
    is_image_bg = background_type == "image" and background_image_url

    # --- CSS body ---
    if is_transparent:
        body_css = "background: transparent;"
    else:
        body_css = f"background: {background_color};"

    # --- Renderer options ---
    if is_transparent:
        renderer_js = """const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, premultipliedAlpha: false });"""
        renderer_clear_js = "renderer.setClearColor(0x000000, 0);"
    else:
        renderer_js = "const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });"
        renderer_clear_js = ""

    # --- Scene background ---
    if is_transparent:
        scene_bg_js = "// scene.background omitted — transparent compositing mode"
    elif is_image_bg:
        scene_bg_js = "// scene.background set by image loader below"
    else:
        scene_bg_js = f"scene.background = new THREE.Color('{background_color}');"

    # --- Ground plane (skip for transparent — fills alpha channel) ---
    if is_transparent:
        ground_js = "// Ground plane omitted — transparent compositing mode"
    else:
        ground_js = f"""const groundGeo = new THREE.PlaneGeometry(40, 40);
const groundMat = new THREE.MeshStandardMaterial({{
  color: new THREE.Color('{background_color}').multiplyScalar(0.85),
  metalness: 0.1,
  roughness: 0.85,
}});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -1.8;
ground.receiveShadow = true;
scene.add(ground);"""

    # --- Background image loader ---
    background_loader_js = _build_background_js(
        background_type, background_color, background_image_url,
        background_blur, background_opacity)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Motion Graphics — {primitive} + {material} + {motion}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ {body_css} overflow: hidden; }}
  canvas {{ display: block; width: 100%; height: 100vh; }}
</style>
</head>
<body>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
{postproc_imports}

<script>
// — Scene setup —
const scene = new THREE.Scene();
{scene_bg_js}

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
const camDist = {camera_distance:.1f};
camera.position.set(0, camDist * 0.35, camDist);
camera.lookAt(0, 0, 0);

{renderer_js}
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
{renderer_clear_js}
document.body.appendChild(renderer.domElement);

{background_loader_js}

{'// — Procedural environment map for reflections —' if needs_envmap else ''}
{_build_envmap_js() if needs_envmap else ''}

// — Geometry —
{geometry_js}

// — Material —
{material_js}

const mesh = new THREE.Mesh(geometry, material);
mesh.castShadow = true;
scene.add(mesh);

// — Ground plane —
{ground_js}

// — Lighting —
{lights_js}

// — Post-processing —
{postproc_setup}

// — Animation —
const clock = new THREE.Clock();
const duration = {animation_duration};
{'clock.start();' if autoplay else '// clock.start(); // autoplay disabled'}

function animate() {{
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();
  const t = (elapsed % duration) / duration;

  // Camera motion
{camera_js}

  // Object motion
{motion_js}

  {postproc_render}
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


# ========== CODE GENERATION HELPERS ==========

def _build_envmap_js() -> str:
    """Generate procedural environment map for reflective materials.
    Uses PMREMGenerator with a hemisphere light scene — r128 compatible."""
    return """const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const envScene = new THREE.Scene();
envScene.add(new THREE.HemisphereLight(0x6688cc, 0x223344, 1.0));
const envDirLight = new THREE.DirectionalLight(0xffeedd, 0.8);
envDirLight.position.set(5, 8, 3);
envScene.add(envDirLight);
const envFillLight = new THREE.PointLight(0xff8844, 0.4, 20);
envFillLight.position.set(-4, 2, -3);
envScene.add(envFillLight);
const envRT = pmremGenerator.fromScene(envScene, 0.04);
scene.environment = envRT.texture;
pmremGenerator.dispose();"""


def _build_background_js(bg_type: str, bg_color: str, bg_image_url: str,
                          bg_blur: float, bg_opacity: float) -> str:
    """Generate background setup JS based on background_type.

    Three modes:
      color:       Handled by scene.background in template — nothing extra needed.
      transparent: Handled by renderer alpha config — nothing extra needed.
      image:       Loads image onto a textured back-plane behind the scene.
                   Back-plane approach (vs scene.background) gives control over
                   blur, opacity, and parallax that scene.background doesn't.
    """
    if bg_type in ("color", "transparent"):
        return ""

    if bg_type == "image" and bg_image_url:
        return f"""// — Background image (back-plane for blur/opacity control) —
const _bgLoader = new THREE.TextureLoader();
_bgLoader.load('{bg_image_url}', function(_bgTex) {{
  _bgTex.encoding = THREE.sRGBEncoding;
  _bgTex.minFilter = THREE.LinearMipmapLinearFilter;
  _bgTex.generateMipmaps = true;

  const _bgGeo = new THREE.PlaneGeometry(80, 45);  // 16:9 aspect
  const _bgMat = new THREE.MeshBasicMaterial({{
    map: _bgTex,
    transparent: {str(bg_opacity < 1.0).lower()},
    opacity: {bg_opacity:.2f},
    depthWrite: false,
  }});
  const _bgMesh = new THREE.Mesh(_bgGeo, _bgMat);
  _bgMesh.position.z = -20;
  _bgMesh.renderOrder = -1;
  scene.add(_bgMesh);
}}, undefined, function(_err) {{
  console.warn('Background image failed to load:', _err);
  scene.background = new THREE.Color('{bg_color}');
}});"""

    return ""


def _build_camera_js(camera_movement: dict, duration: float) -> str:
    """Generate camera animation JS from taxonomy.

    Replaces the hardcoded orbit block in the animation loop.
    Each animation_type maps to a distinct camera behavior.

    The camera code runs inside the animate() loop with access to:
      elapsed  — total seconds since start
      t        — normalized loop position [0,1]
      camDist  — base camera distance
      duration — loop duration in seconds
      camera   — THREE.PerspectiveCamera

    Returns JS code for the camera section of the animation loop.
    """
    if not camera_movement:
        return _camera_orbit({"speed": 0.15, "height_oscillation": 0.3, "height_base": 0.35})

    anim_type = camera_movement.get("animation_type", "orbit")
    params = camera_movement.get("parameters", {})

    dispatch = {
        "none": lambda: _camera_static(),
        "orbit": lambda: _camera_orbit(params),
        "distance_lerp": lambda: _camera_dolly(params, duration),
        "vertical_arc": lambda: _camera_crane(params, duration),
        "bezier_path": lambda: _camera_flythrough(params, duration),
        "rotation_snap": lambda: _camera_whip_pan(params),
        "roll": lambda: _camera_barrel_roll(params),
        "vertigo": lambda: _camera_vertigo(params, duration),
        "arc_path": lambda: _camera_arc(params, duration),
        "distance_oscillate": lambda: _camera_breathing(params),
    }

    builder = dispatch.get(anim_type, lambda: _camera_orbit(params))
    return builder()


def _camera_static() -> str:
    return "  // Camera: static (locked off)"


def _camera_orbit(params: dict) -> str:
    speed = params.get("speed", 0.15)
    h_osc = params.get("height_oscillation", 0.3)
    h_base = params.get("height_base", 0.35)
    r_mult = params.get("radius_multiplier", 1.0)
    return f"""  // Camera: orbit
  const _camAngle = elapsed * {speed};
  const _camR = camDist * {r_mult};
  camera.position.x = _camR * Math.sin(_camAngle);
  camera.position.z = _camR * Math.cos(_camAngle);
  camera.position.y = camDist * {h_base} + Math.sin(elapsed * 0.2) * {h_osc};
  camera.lookAt(0, 0, 0);"""


def _camera_dolly(params: dict, duration: float) -> str:
    start_mult = params.get("start_distance_multiplier", 2.5)
    end_mult = params.get("end_distance_multiplier", 0.4)
    easing = params.get("easing", "ease_in_out")
    orbit_during = params.get("orbit_during", True)
    orbit_speed = params.get("orbit_speed", 0.08)
    h_drift = params.get("height_drift", 0.0)

    ease_fn = _ease_function(easing)
    lines = [
        f"  // Camera: dolly ({start_mult}x → {end_mult}x)",
        f"  const _dollyT = {ease_fn};",
        f"  const _dollyDist = camDist * ({start_mult} + ({end_mult} - {start_mult}) * _dollyT);",
    ]
    if orbit_during:
        lines.append(f"  const _dollyAngle = elapsed * {orbit_speed};")
        lines.append(f"  camera.position.x = _dollyDist * Math.sin(_dollyAngle);")
        lines.append(f"  camera.position.z = _dollyDist * Math.cos(_dollyAngle);")
    else:
        lines.append(f"  camera.position.x = 0;")
        lines.append(f"  camera.position.z = _dollyDist;")
    lines.append(f"  camera.position.y = camDist * 0.35 + _dollyT * camDist * {h_drift};")
    lines.append(f"  camera.lookAt(0, 0, 0);")
    return "\n".join(lines)


def _camera_crane(params: dict, duration: float) -> str:
    start_h = params.get("start_height_offset", -1.0)
    end_h = params.get("end_height_offset", 2.5)
    tilt_follow = params.get("tilt_follow", True)
    orbit_during = params.get("orbit_during", True)
    orbit_speed = params.get("orbit_speed", 0.06)
    easing = params.get("easing", "ease_out")

    ease_fn = _ease_function(easing)
    lines = [
        f"  // Camera: crane ({start_h} → {end_h})",
        f"  const _craneT = {ease_fn};",
        f"  const _craneH = {start_h} + ({end_h} - ({start_h})) * _craneT;",
    ]
    if orbit_during:
        lines.append(f"  const _craneAngle = elapsed * {orbit_speed};")
        lines.append(f"  camera.position.x = camDist * Math.sin(_craneAngle);")
        lines.append(f"  camera.position.z = camDist * Math.cos(_craneAngle);")
    else:
        lines.append(f"  camera.position.x = 0;")
        lines.append(f"  camera.position.z = camDist;")
    lines.append(f"  camera.position.y = camDist * 0.35 + _craneH;")
    lines.append(f"  camera.lookAt(0, {('0' if tilt_follow else 'camera.position.y')}, 0);")
    return "\n".join(lines)


def _camera_flythrough(params: dict, duration: float) -> str:
    start_mult = params.get("start_distance_multiplier", 3.0)
    closest = params.get("closest_approach", 0.15)
    end_mult = params.get("end_distance_multiplier", 3.0)
    curvature = params.get("path_curvature", 0.6)
    h_var = params.get("height_variation", 0.8)
    easing = params.get("speed_profile", "ease_in_out")

    ease_fn = _ease_function(easing)
    return f"""  // Camera: flythrough (bezier path)
  const _ftT = {ease_fn};
  const _ftOneMinusT = 1.0 - _ftT;
  const _p0z = camDist * {start_mult};
  const _p1z = camDist * {closest};
  const _p2z = -camDist * {end_mult};
  const _p1x = camDist * {curvature};
  camera.position.z = _ftOneMinusT * _ftOneMinusT * _p0z + 2 * _ftOneMinusT * _ftT * _p1z + _ftT * _ftT * _p2z;
  camera.position.x = 2 * _ftOneMinusT * _ftT * _p1x;
  camera.position.y = camDist * 0.35 + Math.sin(_ftT * Math.PI) * camDist * {h_var};
  camera.lookAt(0, 0, 0);"""


def _camera_whip_pan(params: dict) -> str:
    snap_angle = params.get("snap_angle", 90)
    snap_dur = params.get("snap_duration", 0.3)
    hold_dur = params.get("hold_duration", 2.0)
    h_base = params.get("height_base", 0.35)
    cycle = snap_dur + hold_dur
    snap_rad = math.radians(snap_angle)

    return f"""  // Camera: whip pan ({snap_angle}° snaps)
  const _wpCycle = {cycle};
  const _wpPhase = (elapsed % _wpCycle) / _wpCycle;
  const _wpSnapFrac = {snap_dur} / _wpCycle;
  const _wpSegment = Math.floor(elapsed / _wpCycle);
  let _wpAngle;
  if (_wpPhase < _wpSnapFrac) {{
    const _wpSnapT = _wpPhase / _wpSnapFrac;
    const _wpEased = 1.0 - Math.pow(1.0 - _wpSnapT, 3.0);
    _wpAngle = (_wpSegment + _wpEased) * {snap_rad};
  }} else {{
    _wpAngle = (_wpSegment + 1.0) * {snap_rad};
  }}
  camera.position.x = camDist * Math.sin(_wpAngle);
  camera.position.z = camDist * Math.cos(_wpAngle);
  camera.position.y = camDist * {h_base};
  camera.lookAt(0, 0, 0);"""


def _camera_barrel_roll(params: dict) -> str:
    roll_speed = params.get("roll_speed", 0.3)
    orbit_during = params.get("orbit_during", True)
    orbit_speed = params.get("orbit_speed", 0.08)
    roll_amp = params.get("roll_amplitude", 1.0)

    lines = [f"  // Camera: barrel roll"]
    if orbit_during:
        lines.append(f"  const _brAngle = elapsed * {orbit_speed};")
        lines.append(f"  camera.position.x = camDist * Math.sin(_brAngle);")
        lines.append(f"  camera.position.z = camDist * Math.cos(_brAngle);")
        lines.append(f"  camera.position.y = camDist * 0.35;")
    else:
        lines.append(f"  camera.position.set(0, camDist * 0.35, camDist);")
    lines.append(f"  camera.lookAt(0, 0, 0);")
    lines.append(f"  camera.rotation.z = elapsed * {roll_speed} * Math.PI * 2 * {roll_amp};")
    return "\n".join(lines)


def _camera_vertigo(params: dict, duration: float) -> str:
    start_mult = params.get("start_distance_multiplier", 1.5)
    end_mult = params.get("end_distance_multiplier", 0.5)
    start_fov = params.get("start_fov", 30)
    end_fov = params.get("end_fov", 80)
    easing = params.get("easing", "ease_in_out")

    ease_fn = _ease_function(easing)
    return f"""  // Camera: vertigo (dolly zoom)
  const _vzT = {ease_fn};
  const _vzDist = camDist * ({start_mult} + ({end_mult} - {start_mult}) * _vzT);
  const _vzFov = {start_fov} + ({end_fov} - {start_fov}) * _vzT;
  camera.fov = _vzFov;
  camera.updateProjectionMatrix();
  camera.position.set(0, camDist * 0.35, _vzDist);
  camera.lookAt(0, 0, 0);"""


def _camera_arc(params: dict, duration: float) -> str:
    start_pos = params.get("start_position", [-2.0, -0.5, 2.0])
    end_pos = params.get("end_position", [0.5, 1.5, 0.8])
    easing = params.get("easing", "ease_out")
    look_offset = params.get("look_at_offset", [0, 0, 0])

    ease_fn = _ease_function(easing)
    return f"""  // Camera: arc path
  const _arcT = {ease_fn};
  camera.position.x = camDist * ({start_pos[0]} + ({end_pos[0]} - ({start_pos[0]})) * _arcT);
  camera.position.y = camDist * ({start_pos[1]} + ({end_pos[1]} - ({start_pos[1]})) * _arcT);
  camera.position.z = camDist * ({start_pos[2]} + ({end_pos[2]} - ({start_pos[2]})) * _arcT);
  camera.lookAt({look_offset[0]}, {look_offset[1]}, {look_offset[2]});"""


def _camera_breathing(params: dict) -> str:
    osc_amp = params.get("oscillation_amplitude", 0.15)
    osc_speed = params.get("oscillation_speed", 0.4)
    h_osc = params.get("height_oscillation", 0.08)
    orbit_during = params.get("orbit_during", True)
    orbit_speed = params.get("orbit_speed", 0.04)

    lines = [f"  // Camera: breathing"]
    lines.append(f"  const _brthDist = camDist * (1.0 + Math.sin(elapsed * {osc_speed} * Math.PI * 2) * {osc_amp});")
    if orbit_during:
        lines.append(f"  const _brthAngle = elapsed * {orbit_speed};")
        lines.append(f"  camera.position.x = _brthDist * Math.sin(_brthAngle);")
        lines.append(f"  camera.position.z = _brthDist * Math.cos(_brthAngle);")
    else:
        lines.append(f"  camera.position.x = 0;")
        lines.append(f"  camera.position.z = _brthDist;")
    lines.append(f"  camera.position.y = camDist * 0.35 + Math.sin(elapsed * {osc_speed} * Math.PI * 2 + 0.5) * camDist * {h_osc};")
    lines.append(f"  camera.lookAt(0, 0, 0);")
    return "\n".join(lines)


def _ease_function(easing: str) -> str:
    """Return JS expression for easing applied to t (normalized loop position)."""
    ease_map = {
        "ease_in": "t * t",
        "ease_out": "(1.0 - (1.0 - t) * (1.0 - t))",
        "ease_in_out": "(t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2)",
        "linear": "t",
    }
    return ease_map.get(easing, ease_map["ease_in_out"])


def _build_geometry_js(geom_type: str, params: dict) -> str:
    """Generate Three.js geometry constructor from taxonomy."""
    # Map common taxonomy geometry types to Three.js constructors
    geom_map = {
        "SphereGeometry": lambda p: f"new THREE.SphereGeometry({p.get('radius', 1)}, {p.get('widthSegments', 64)}, {p.get('heightSegments', 64)})",
        "BoxGeometry": lambda p: f"new THREE.BoxGeometry({p.get('width', 1)}, {p.get('height', 1)}, {p.get('depth', 1)})",
        "TorusGeometry": lambda p: f"new THREE.TorusGeometry({p.get('radius', 1)}, {p.get('tube', 0.3)}, {p.get('radialSegments', 32)}, {p.get('tubularSegments', 64)})",
        "TorusKnotGeometry": lambda p: f"new THREE.TorusKnotGeometry({p.get('radius', 1)}, {p.get('tube', 0.3)}, {p.get('tubularSegments', 128)}, {p.get('radialSegments', 16)}, {p.get('p', 2)}, {p.get('q', 3)})",
        "IcosahedronGeometry": lambda p: f"new THREE.IcosahedronGeometry({p.get('radius', 1)}, {p.get('detail', 0)})",
        "OctahedronGeometry": lambda p: f"new THREE.OctahedronGeometry({p.get('radius', 1)}, {p.get('detail', 0)})",
        "DodecahedronGeometry": lambda p: f"new THREE.DodecahedronGeometry({p.get('radius', 1)}, {p.get('detail', 0)})",
        "ConeGeometry": lambda p: f"new THREE.ConeGeometry({p.get('radius', 1)}, {p.get('height', 2)}, {p.get('radialSegments', 32)})",
        "CylinderGeometry": lambda p: f"new THREE.CylinderGeometry({p.get('radiusTop', 1)}, {p.get('radiusBottom', 1)}, {p.get('height', 2)}, {p.get('radialSegments', 32)})",
        "PlaneGeometry": lambda p: f"new THREE.PlaneGeometry({p.get('width', 2)}, {p.get('height', 2)}, {p.get('widthSegments', 32)}, {p.get('heightSegments', 32)})",
        "RingGeometry": lambda p: f"new THREE.RingGeometry({p.get('innerRadius', 0.5)}, {p.get('outerRadius', 1)}, {p.get('thetaSegments', 32)})",
    }

    builder = geom_map.get(geom_type)
    if builder:
        return f"const geometry = {builder(params)};"

    # Fallback: sphere
    return f"// Custom geometry '{geom_type}' — using sphere fallback\nconst geometry = new THREE.SphereGeometry(1, 64, 64);"


def _build_material_js(mat_type: str, params: dict, palette_colors: list) -> str:
    """Generate Three.js material from taxonomy."""
    primary_color = palette_colors[0] if palette_colors else "#ffffff"

    mat_map = {
        "MeshStandardMaterial": lambda: f"""const material = new THREE.MeshStandardMaterial({{
  color: new THREE.Color('{primary_color}'),
  metalness: {params.get('metalness', 0.5)},
  roughness: {params.get('roughness', 0.5)},
  envMapIntensity: {params.get('envMapIntensity', 1.0)},
}});""",
        "MeshPhysicalMaterial": lambda: f"""const material = new THREE.MeshPhysicalMaterial({{
  color: new THREE.Color('{primary_color}'),
  metalness: {params.get('metalness', 0.0)},
  roughness: {params.get('roughness', 0.1)},
  clearcoat: {params.get('clearcoat', 1.0)},
  clearcoatRoughness: {params.get('clearcoatRoughness', 0.1)},
  reflectivity: {params.get('reflectivity', 0.9)},
  transparent: {str(params.get('transmission', 0) > 0.1).lower()},
  opacity: {max(0.15, 1.0 - params.get('transmission', 0.0))},
}});""",
        "MeshNormalMaterial": lambda: "const material = new THREE.MeshNormalMaterial({ flatShading: false });",
        "MeshBasicMaterial": lambda: f"const material = new THREE.MeshBasicMaterial({{ color: new THREE.Color('{primary_color}') }});",
        "MeshToonMaterial": lambda: f"const material = new THREE.MeshToonMaterial({{ color: new THREE.Color('{primary_color}') }});",
    }

    builder = mat_map.get(mat_type)
    if builder:
        return builder()

    # Wireframe / fallback
    if "wireframe" in mat_type.lower() or "wire" in params.get("description", "").lower():
        return f"""const material = new THREE.MeshStandardMaterial({{
  color: new THREE.Color('{primary_color}'),
  wireframe: true,
  metalness: 0.8,
  roughness: 0.2,
}});"""

    return f"""// Material '{mat_type}' mapped to MeshStandardMaterial
const material = new THREE.MeshStandardMaterial({{
  color: new THREE.Color('{primary_color}'),
  metalness: {params.get('metalness', 0.5)},
  roughness: {params.get('roughness', 0.5)},
}});"""


def _build_motion_js(motion: dict, duration: float) -> str:
    """Generate animation loop body from motion taxonomy."""
    anim_type = motion.get("animation_type", "rotation")
    params = motion.get("parameters", {})

    speed = params.get("speed", 1.0)
    if isinstance(speed, dict):
        speed = speed.get("default", 1.0)

    amplitude = params.get("amplitude", 1.0)
    if isinstance(amplitude, dict):
        amplitude = amplitude.get("default", 1.0)

    lines = []

    if "rotat" in anim_type.lower():
        lines.append(f"  mesh.rotation.y = elapsed * {speed} * 0.5;")
        lines.append(f"  mesh.rotation.x = Math.sin(elapsed * 0.3) * 0.2;")

    elif "oscillat" in anim_type.lower() or "bounce" in anim_type.lower():
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {speed} * Math.PI * 2) * {amplitude};")
        lines.append(f"  mesh.rotation.y = elapsed * 0.3;")

    elif "orbit" in anim_type.lower():
        radius = params.get("radius", 2.0)
        if isinstance(radius, dict):
            radius = radius.get("default", 2.0)
        lines.append(f"  mesh.position.x = Math.cos(elapsed * {speed}) * {radius};")
        lines.append(f"  mesh.position.z = Math.sin(elapsed * {speed}) * {radius};")
        lines.append(f"  mesh.rotation.y = elapsed * 0.5;")

    elif "pulse" in anim_type.lower() or "scale" in anim_type.lower():
        lines.append(f"  const s = 1.0 + Math.sin(elapsed * {speed} * Math.PI * 2) * {amplitude * 0.3};")
        lines.append(f"  mesh.scale.set(s, s, s);")
        lines.append(f"  mesh.rotation.y = elapsed * 0.2;")

    elif "lissajous" in anim_type.lower():
        freq_a = params.get("frequency_a", 3)
        freq_b = params.get("frequency_b", 2)
        if isinstance(freq_a, dict):
            freq_a = freq_a.get("default", 3)
        if isinstance(freq_b, dict):
            freq_b = freq_b.get("default", 2)
        lines.append(f"  mesh.position.x = Math.sin(elapsed * {freq_a}) * {amplitude};")
        lines.append(f"  mesh.position.y = Math.sin(elapsed * {freq_b}) * {amplitude};")
        lines.append(f"  mesh.rotation.z = elapsed * 0.3;")

    elif "morph" in anim_type.lower() or "deform" in anim_type.lower():
        lines.append(f"  const positions = geometry.attributes.position;")
        lines.append(f"  for (let i = 0; i < positions.count; i++) {{")
        lines.append(f"    const x = positions.getX(i);")
        lines.append(f"    const y = positions.getY(i);")
        lines.append(f"    const z = positions.getZ(i);")
        lines.append(f"    const offset = Math.sin(x * 3 + elapsed * {speed}) * {amplitude * 0.1};")
        lines.append(f"    positions.setZ(i, z + offset * 0.01);")
        lines.append(f"  }}")
        lines.append(f"  positions.needsUpdate = true;")
        lines.append(f"  mesh.rotation.y = elapsed * 0.2;")

    else:
        # Generic: gentle rotation + float
        lines.append(f"  mesh.rotation.y = elapsed * {speed} * 0.5;")
        lines.append(f"  mesh.rotation.x = Math.sin(elapsed * 0.5) * 0.15;")
        lines.append(f"  mesh.position.y = Math.sin(elapsed * 0.7) * 0.2;")

    return "\n".join(lines)


def _build_lights_js(lights_config: dict) -> str:
    """Generate Three.js lighting from taxonomy."""
    if not lights_config or "lights" not in lights_config:
        return """const ambientLight = new THREE.HemisphereLight(0x6688cc, 0x223344, 0.6);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.0);
dirLight.position.set(5, 8, 5);
dirLight.castShadow = true;
dirLight.shadow.mapSize.set(1024, 1024);
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 30;
scene.add(dirLight);
const rimLight = new THREE.PointLight(0x4488ff, 0.5, 15);
rimLight.position.set(-4, 3, -4);
scene.add(rimLight);"""

    lines = []
    for i, light in enumerate(lights_config["lights"]):
        light_type = light.get("type", "DirectionalLight")
        color = light.get("color", "#ffffff")
        intensity = light.get("intensity", 1.0)
        position = light.get("position", [5, 5, 5])

        if light_type == "AmbientLight":
            lines.append(f"const light{i} = new THREE.AmbientLight('{color}', {intensity});")
            lines.append(f"scene.add(light{i});")
        elif light_type == "PointLight":
            lines.append(f"const light{i} = new THREE.PointLight('{color}', {intensity}, 50);")
            lines.append(f"light{i}.position.set({position[0]}, {position[1]}, {position[2]});")
            lines.append(f"scene.add(light{i});")
        elif light_type == "SpotLight":
            lines.append(f"const light{i} = new THREE.SpotLight('{color}', {intensity});")
            lines.append(f"light{i}.position.set({position[0]}, {position[1]}, {position[2]});")
            lines.append(f"light{i}.angle = {light.get('angle', 0.5)};")
            lines.append(f"light{i}.penumbra = {light.get('penumbra', 0.5)};")
            lines.append(f"light{i}.castShadow = true;")
            lines.append(f"scene.add(light{i});")
        else:
            lines.append(f"const light{i} = new THREE.DirectionalLight('{color}', {intensity});")
            lines.append(f"light{i}.position.set({position[0]}, {position[1]}, {position[2]});")
            lines.append(f"light{i}.castShadow = true;")
            lines.append(f"light{i}.shadow.mapSize.set(1024, 1024);")
            lines.append(f"scene.add(light{i});")

    return "\n".join(lines)


def _build_postprocessing_js(effects: list, transparent: bool = False) -> tuple:
    """Generate Three.js post-processing setup.

    Returns (imports_html, setup_js, render_js) strings.

    When transparent=False (default): Uses emissive approximation for bloom
    and inline comments for other effects. Simple, zero-dependency.

    When transparent=True: Generates a real render-target + shader pipeline
    with alpha-preserving bloom. The bloom glow must carry alpha so it
    composites correctly over other layers — otherwise you get hard-edged
    sprites with no soft halo when layered.

    The alpha-preserving bloom works by:
    1. Rendering scene to an RGBA WebGLRenderTarget
    2. Running a Gaussian blur to extract bright regions
    3. Compositing bloom RGB additively while deriving output alpha from
       both the original particle alpha AND the bloom brightness, so the
       glow halo extends into neighboring transparent pixels.
    """
    if not effects and not transparent:
        return ("", "", "renderer.render(scene, camera);")

    if not effects and transparent:
        # Transparent but no effects — just render with clear alpha
        return ("", "", """renderer.setClearColor(0x000000, 0);
  renderer.clear();
  renderer.render(scene, camera);""")

    imports_html = ""

    # Detect which effects are requested
    has_bloom = False
    bloom_strength = 0.4
    other_effects = []

    for eff_name, eff_data in effects:
        params = eff_data["parameters"]
        if eff_name == "bloom":
            has_bloom = True
            bloom_strength = params.get("strength", params.get("intensity", 0.4))
        else:
            other_effects.append((eff_name, eff_data))

    # --- TRANSPARENT MODE: real shader pipeline ---
    if transparent and has_bloom:
        setup_lines = [
            "// — Alpha-preserving bloom (render-target + shader) —",
            f"const _bloomStrength = {bloom_strength};",
            "",
            "const _rtOpts = {",
            "  format: THREE.RGBAFormat,",
            "  type: THREE.UnsignedByteType,",
            "  stencilBuffer: false,",
            "  depthBuffer: true,",
            "};",
            "const _bloomRT = new THREE.WebGLRenderTarget(",
            "  window.innerWidth, window.innerHeight, _rtOpts);",
            "",
            "// Bloom shader: Gaussian blur extracts bright regions,",
            "// output alpha derived from particle alpha + bloom luminance.",
            "const _bloomMat = new THREE.ShaderMaterial({",
            "  uniforms: {",
            "    tDiffuse: { value: null },",
            "    bloomStrength: { value: _bloomStrength },",
            "    resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },",
            "  },",
            "  vertexShader: `",
            "    varying vec2 vUv;",
            "    void main() {",
            "      vUv = uv;",
            "      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);",
            "    }",
            "  `,",
            "  fragmentShader: `",
            "    uniform sampler2D tDiffuse;",
            "    uniform float bloomStrength;",
            "    uniform vec2 resolution;",
            "    varying vec2 vUv;",
            "",
            "    void main() {",
            "      vec4 center = texture2D(tDiffuse, vUv);",
            "      vec2 texel = 1.0 / resolution;",
            "",
            "      // 7x7 Gaussian for bloom halo",
            "      vec4 bloom = vec4(0.0);",
            "      float total = 0.0;",
            "      for (float x = -3.0; x <= 3.0; x += 1.0) {",
            "        for (float y = -3.0; y <= 3.0; y += 1.0) {",
            "          float w = exp(-(x*x + y*y) / 8.0);",
            "          bloom += texture2D(tDiffuse, vUv + vec2(x, y) * texel * 3.0) * w;",
            "          total += w;",
            "        }",
            "      }",
            "      bloom /= total;",
            "",
            "      // Threshold bright pixels",
            "      vec3 bright = max(bloom.rgb - vec3(0.3), vec3(0.0));",
            "",
            "      // RGB: original + bloom glow",
            "      vec3 finalRGB = center.rgb + bright * bloomStrength * 1.5;",
            "",
            "      // Alpha: particle alpha + bloom spread alpha",
            "      // Without bloom alpha, glow gets clipped to hard sprite edges",
            "      float bloomAlpha = max(max(bright.r, bright.g), bright.b) * bloomStrength * 2.0;",
            "      float finalAlpha = min(center.a + bloomAlpha, 1.0);",
            "",
            "      gl_FragColor = vec4(finalRGB, finalAlpha);",
            "    }",
            "  `,",
            "  transparent: true,",
            "});",
            "",
            "const _postScene = new THREE.Scene();",
            "const _postCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);",
            "_postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), _bloomMat));",
        ]

        # Also handle other effects as comments (same as opaque mode)
        for eff_name, eff_data in other_effects:
            param_str = json.dumps(eff_data["parameters"])
            setup_lines.append(f"// {eff_data['name']}: {eff_name} — {param_str}")

        # Resize handler for render target
        setup_lines.append("")
        setup_lines.append("window.addEventListener('resize', () => {")
        setup_lines.append("  _bloomRT.setSize(window.innerWidth, window.innerHeight);")
        setup_lines.append("  _bloomMat.uniforms.resolution.value.set(window.innerWidth, window.innerHeight);")
        setup_lines.append("});")

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

        return (imports_html, "\n".join(setup_lines), render_js)

    # --- TRANSPARENT MODE without bloom: just render with alpha ---
    if transparent:
        setup_lines = [
            "// -- Post-processing (transparent, no bloom) --",
        ]
        for eff_name, eff_data in effects:
            param_str = json.dumps(eff_data["parameters"])
            setup_lines.append(f"// {eff_data['name']}: {eff_name} — {param_str}")

        render_js = """renderer.setClearColor(0x000000, 0);
  renderer.clear();
  renderer.render(scene, camera);"""

        return (imports_html, "\n".join(setup_lines), render_js)

    # --- OPAQUE MODE (original behavior): emissive approximation ---
    setup_lines = [
        "// -- Post-processing (emissive approximation, no EffectComposer) --",
    ]

    for eff_name, eff_data in effects:
        params = eff_data["parameters"]
        if eff_name == "bloom":
            setup_lines.append(f"// Bloom via emissive: intensity {bloom_strength}")
        else:
            param_str = json.dumps(params)
            setup_lines.append(f"// {eff_data['name']}: {eff_name} — {param_str}")

    if has_bloom:
        setup_lines.append(f"mesh.material.emissive = mesh.material.color.clone().multiplyScalar(0.3);")
        setup_lines.append(f"mesh.material.emissiveIntensity = {bloom_strength};")

    render_js = "renderer.render(scene, camera);"

    return (imports_html, "\n".join(setup_lines), render_js)


# ========== ORBIT COMPOSER INTEGRATION ==========

@mcp.tool()
def map_orbit_state_to_olae(
    dominant_domain: str,
    phase_pct: float,
    domain_descriptors: str = "{}",
    orbit_mood: str = "neutral"
) -> str:
    """Map Orbit Composer state to OLAE parameters.

    Bridge tool: translates the orbit's phase portrait state into
    motion graphics taxonomy selections. Used by the Orbit Composer's
    output rack to drive Three.js scene generation.

    The mapping is deterministic — given the same orbit state,
    you always get the same OLAE configuration. This preserves
    the orbit's temporal structure in the visual output.

    Args:
        dominant_domain: Which aesthetic domain is strongest
            (e.g., "catastrophe_morph", "surface_design", "diatom_morph")
        phase_pct: Position in orbit cycle, 0.0 to 1.0
        domain_descriptors: JSON of vocabulary descriptors from orbit state
        orbit_mood: Mood arc position ("opening", "tension", "climax", "reversal", "resolution")

    Returns:
        Recommended OLAE configuration with rationale
    """
    try:
        descriptors = json.loads(domain_descriptors)
    except json.JSONDecodeError:
        descriptors = {}

    # Domain → primitive/material affinity mapping
    domain_affinities = {
        "catastrophe_morph": {
            "primitives": ["torus_knot", "klein_bottle", "mobius_strip", "icosahedron"],
            "materials": ["glass", "iridescent", "holographic", "metallic"],
            "motions": ["morph", "bifurcation", "snap", "spring_bounce"],
        },
        "surface_design": {
            "primitives": ["sphere", "torus", "plane", "cylinder"],
            "materials": ["metallic", "ceramic", "frosted_glass", "matte"],
            "motions": ["rotate", "breathe", "pulse", "float"],
        },
        "diatom_morph": {
            "primitives": ["dodecahedron", "icosahedron", "voronoi_mesh", "geodesic"],
            "materials": ["glass", "translucent", "pearlescent", "normal"],
            "motions": ["rotate", "orbit", "lissajous", "spiral"],
        },
    }

    # Phase → effect intensity mapping
    phase_effects = {
        "opening": {"bloom": 0.3, "vignette": 0.6, "depth_of_field": 0.8},
        "tension": {"film_grain": 0.7, "chromatic_aberration": 0.4, "ambient_occlusion": 0.6},
        "climax": {"bloom": 1.0, "glitch": 0.3, "chromatic_aberration": 0.6},
        "reversal": {"chromatic_aberration": 0.8, "pixelation": 0.2, "glitch": 0.5},
        "resolution": {"bloom": 0.5, "vignette": 0.4, "depth_of_field": 0.5},
        "neutral": {"bloom": 0.4, "film_grain": 0.2},
    }

    # Phase → lighting mapping
    phase_lighting = {
        "opening": "soft_ambient",
        "tension": "dramatic_side",
        "climax": "high_contrast",
        "reversal": "neon_glow",
        "resolution": "warm_ambient",
        "neutral": "studio_clean",
    }

    # Phase → color palette tendency
    phase_palettes = {
        "opening": "pastel",
        "tension": "monochrome",
        "climax": "cyberpunk",
        "reversal": "sunset",
        "resolution": "earth",
        "neutral": "ocean",
    }

    affinity = domain_affinities.get(dominant_domain, domain_affinities["surface_design"])
    effects_map = phase_effects.get(orbit_mood, phase_effects["neutral"])

    # Select from affinity lists based on phase position
    idx = int(phase_pct * (len(affinity["primitives"]) - 1))
    recommended_primitive = affinity["primitives"][min(idx, len(affinity["primitives"]) - 1)]
    recommended_material = affinity["materials"][min(idx, len(affinity["materials"]) - 1)]
    recommended_motion = affinity["motions"][min(idx, len(affinity["motions"]) - 1)]

    result = {
        "orbit_input": {
            "dominant_domain": dominant_domain,
            "phase_pct": phase_pct,
            "mood": orbit_mood,
        },
        "recommended_olae": {
            "primitive": recommended_primitive,
            "material": recommended_material,
            "motion": recommended_motion,
            "effects": list(effects_map.keys()),
            "effect_intensities": effects_map,
            "color_palette": phase_palettes.get(orbit_mood, "cyberpunk"),
            "lighting": phase_lighting.get(orbit_mood, "studio_clean"),
        },
        "rationale": {
            "domain_affinity": f"{dominant_domain} maps to {recommended_primitive}/{recommended_material} "
                               f"for structural congruence",
            "phase_effects": f"Orbit mood '{orbit_mood}' at {phase_pct:.0%} drives "
                             f"{', '.join(effects_map.keys())} at mapped intensities",
            "temporal_coherence": "Phase-driven selection ensures visual transitions "
                                  "track orbit dynamics rather than random switching",
        },
    }

    return yaml.dump(result, default_flow_style=False)


@mcp.tool()
def generate_orbit_keyframes(
    phases: str,
    domain_ids: str = "[]",
    keyframe_count: int = 8,
    total_duration: float = 8.0
) -> str:
    """Generate Three.js keyframe sequence from orbit phase portrait.

    Maps an array of orbit phases (from Orbit Composer's phase portrait)
    into a timed sequence of OLAE configurations. Each keyframe is a
    complete motion graphics specification at a timestamp.

    Args:
        phases: JSON array of phase objects, each with:
            - phasePct: 0.0-1.0 position in orbit
            - dominantDomain: string
            - mood: "opening" | "tension" | "climax" | "reversal" | "resolution"
            - descriptors: optional domain vocabulary
        domain_ids: JSON array of active domain identifiers
        keyframe_count: Number of keyframes to extract (evenly spaced)
        total_duration: Total animation duration in seconds

    Returns:
        Timed keyframe sequence ready for Three.js animation system
    """
    try:
        phase_list = json.loads(phases)
        domains = json.loads(domain_ids)
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {e}"

    if not phase_list:
        return "Error: Empty phase array"

    # Sample evenly spaced keyframes
    step = max(1, len(phase_list) // keyframe_count)
    sampled = [phase_list[i * step] for i in range(keyframe_count)
               if i * step < len(phase_list)]

    keyframes = []
    for i, phase in enumerate(sampled):
        timestamp = (i / max(len(sampled) - 1, 1)) * total_duration

        # Map each phase to OLAE via the bridge tool
        olae_yaml = map_orbit_state_to_olae(
            dominant_domain=phase.get("dominantDomain", "surface_design"),
            phase_pct=phase.get("phasePct", 0.0),
            domain_descriptors=json.dumps(phase.get("descriptors", {})),
            orbit_mood=phase.get("mood", "neutral"),
        )
        olae = yaml.safe_load(olae_yaml)

        keyframes.append({
            "index": i,
            "timestamp": round(timestamp, 2),
            "phase_pct": phase.get("phasePct", 0.0),
            "mood": phase.get("mood", "neutral"),
            "dominant_domain": phase.get("dominantDomain", "surface_design"),
            "olae": olae.get("recommended_olae", {}),
        })

    result = {
        "keyframe_count": len(keyframes),
        "total_duration": total_duration,
        "active_domains": domains,
        "keyframes": keyframes,
        "interpolation_notes": {
            "geometry": "Cross-fade via morph targets or geometry swap at keyframe boundaries",
            "material": "Lerp material properties (metalness, roughness, transmission)",
            "motion": "Blend motion vectors with configurable easing",
            "effects": "Smooth effect intensity transitions via linear interpolation",
        },
    }

    return yaml.dump(result, default_flow_style=False)


# ========== EXISTING TOOLS (kept from original) ==========

@mcp.tool()
def generate_synthesis_context(
    primitive: str,
    material: str,
    motion: str,
    color_palette: str = "cyberpunk",
    lighting: str = "dramatic_side",
    composition: str = "centered",
    user_intent: str = ""
) -> str:
    """Generate complete context for Claude synthesis.

    Layer 3 interface — provides all deterministic parameters plus
    instructions for creative synthesis.
    """
    mapped_yaml = map_object_look_action(
        primitive, material, motion,
        color_palette, lighting, composition
    )
    prim = find_primitive(primitive)
    mat = find_material(material)
    mot = find_motion(motion)

    result = f"""# Motion Graphics Synthesis Context

## User Intent
{user_intent if user_intent else "Not specified"}

## Deterministic Parameters (Layers 1-2)

{mapped_yaml}

## Visual Characteristics for Synthesis

### Geometric Form
- **Visual Character**: {prim['visual_character']}
- **Complexity**: {prim['complexity']}

### Surface Treatment
- **Visual Character**: {mat['visual_character']}
- **Lighting Response**: {mat['lighting_response']}

### Temporal Dynamics
- **Visual Character**: {mot['visual_character']}
- **Temporal Pattern**: {mot['temporal_pattern']}

## Synthesis Instructions for Claude

You are receiving complete Three.js parameters from deterministic taxonomy lookup.
Your role (Layer 3) is to:

1. **Integrate Context**: If user_intent provided, ensure parameters align with their vision
2. **Synthesize Naturally**: Describe the motion graphic in natural language
3. **Add Nuance**: Consider how OBJECT + LOOK + ACTION combine expressively
4. **Provide Implementation Guidance**: Camera angles, render settings, post-processing

DO NOT repeat the raw parameters — transform them into aesthetic vision.
"""
    return result


@mcp.tool()
def apply_cocktail_aesthetic(
    base_primitive: str,
    base_motion: str,
    cocktail_name: str
) -> str:
    """Apply cocktail aesthetic to motion graphics parameters.

    Functor: Cocktail domain → Motion graphics domain
    """
    cocktail_mappings = {
        "old_fashioned": {"color_palette": "gold_silver", "lighting": "warm_ambient", "material": "glass"},
        "martini": {"color_palette": "monochrome", "lighting": "studio_clean", "material": "glass"},
        "mojito": {"color_palette": "ocean", "lighting": "soft_ambient", "material": "frosted_glass"},
    }
    mapping = cocktail_mappings.get(cocktail_name.lower())
    if not mapping:
        return f"Cocktail '{cocktail_name}' not in mapping table. Available: {list(cocktail_mappings.keys())}"

    return f"""# Cocktail Aesthetic Applied

## Source
- **Cocktail**: {cocktail_name}
- **Base Primitive**: {base_primitive}
- **Base Motion**: {base_motion}

## Mapped Parameters
- **Color Palette**: {mapping['color_palette']}
- **Lighting**: {mapping['lighting']}
- **Suggested Material**: {mapping['material']}

## Recommended Configuration
Call `map_object_look_action_effect()` with:
- primitive: "{base_primitive}"
- material: "{mapping['material']}"
- motion: "{base_motion}"
- color_palette: "{mapping['color_palette']}"
- lighting: "{mapping['lighting']}"
"""


@mcp.tool()
def get_intentionality() -> str:
    """Get the core intentionality explaining why this approach works."""
    result = []
    result.append("# Motion Graphics MCP — Intentionality\n")
    result.append("## Geometric Primitives")
    result.append(GEOMETRIC_PRIMITIVES["intentionality"])
    result.append("\n## Material Systems")
    result.append(MATERIAL_SYSTEMS["intentionality"])
    result.append("\n## Motion Patterns")
    result.append(MOTION_PATTERNS["intentionality"])
    result.append("\n## Colors, Lighting, Composition")
    result.append(COLORS_LIGHTING["intentionality"])
    result.append("\n## Post-Processing Effects")
    result.append(POST_PROCESSING["intentionality"])
    return "\n".join(result)


@mcp.tool()
def list_domain_functors() -> str:
    """List available functors to other Lushy domains."""
    return """# Available Domain Functors

Motion graphics can compose with other Lushy domains:

## Currently Implemented

### cocktail-aesthetics → motion-graphics
- Maps cocktail color/mood to color palette and lighting
- Use `apply_cocktail_aesthetic()` tool

### Orbit Composer → motion-graphics (NEW)
- Maps orbit phase portrait to OLAE configurations
- Use `map_orbit_state_to_olae()` for single-frame mapping
- Use `generate_orbit_keyframes()` for animated sequences
- Phase position drives effect intensities via orbit_affinity
- Domain dominance selects primitive/material families

## Potential Functors (not yet implemented)

### catastrophe-morph → motion-graphics
- Map catastrophe type → motion pattern (fold=smooth, cusp=snap)
- Map control parameters → geometric complexity
- Map optical intensity → post-processing bloom

### surface-design → motion-graphics
- Map surface type → Three.js material properties
- Map specularity → metalness/roughness
- Map micro_texture_density → displacement map intensity

### diatom-morph → motion-graphics
- Map diatom shape → parametric geometry
- Map symmetry order → radial array count
- Map optical effects → post-processing chain

Each functor preserves structure while translating between domains.
"""


@mcp.tool()
def get_server_info() -> str:
    """Get information about this MCP server."""
    return """# Motion Graphics MCP Server — Extended

## Architecture

**Three-Layer Pattern (Lushy Standard):**

Layer 1 (Foundation) - 0 tokens:
- Pure taxonomy enumeration from YAML ologs
- 30+ geometric primitives, 30+ materials, 40+ motions
- 10 color palettes, 10 lighting moods, 6 compositions
- 10 post-processing effects (NEW)

Layer 2 (Structure) - 0 tokens:
- Deterministic parameter mapping (OLA and OLAE)
- Scene graph composition with spatial relationships
- Code generation (self-contained Three.js HTML)
- Orbit Composer bridge (phase → OLAE mapping)

Layer 3 (Contextual) - variable tokens:
- Creative synthesis by Claude
- Natural language aesthetic description

## New Capabilities

### Code Generation (Layer 2.5)
`generate_threejs_html()` — emits runnable HTML from taxonomy.
Zero LLM cost. Output renders in browser or Claude artifact.

### Post-Processing (EFFECT dimension)
Extends OBJECT × LOOK × ACTION → O × L × A × E
Each effect has orbit_affinity for phase-driven modulation.

### Scene Graph
`compose_scene()` — multi-object with parent-child, cascade,
mirror, orbit relationships and staggered animation timing.

### Orbit Composer Integration
`map_orbit_state_to_olae()` — single-frame orbit → OLAE bridge
`generate_orbit_keyframes()` — full phase portrait → keyframe sequence

## Cost Profile

- List/get/map operations: 0 tokens (pure taxonomy)
- Code generation: 0 tokens (deterministic template)
- Scene graph composition: 0 tokens (deterministic assembly)
- Orbit mapping: 0 tokens (deterministic bridge)
- Claude synthesis: ~500-1500 tokens (creative expression)

**Savings: 60-80% token reduction vs pure LLM**

## Version
2.2.0 — Added camera movements (O×L×A×E×C), background modes, alpha-preserving bloom
"""


if __name__ == "__main__":
    mcp.run()
