# Motion Graphics Aesthetics MCP Server

**Categorical foundation for procedural motion graphics generation with Three.js/WebGL**

## What This Is

A Model Context Protocol (MCP) server that provides **deterministic aesthetic parameters** for generating procedural motion graphics. Built on Lushy's three-layer olog architecture, this server separates structural knowledge (taxonomy) from creative synthesis, achieving **60-85% token savings** compared to pure LLM approaches.

## The Problem It Solves

**Current workflow (pure Gemini 3):**
```
User describes motion → Gemini generates full code → Screen record
```

**Issues:**
- Every iteration burns tokens regenerating structural knowledge
- No taxonomic foundation = inconsistent results
- Hard to version control aesthetic parameters
- Can't systematically compose aesthetic domains

**Lushy workflow:**
```
User describes intent → MCP maps to parameters (0 tokens) →
Gemini synthesizes structure with parameters (~200 tokens) →
Execute in browser → Screen record
```

**Benefits:**
- 60-85% token cost reduction
- Taxonomic foundation ensures reproducibility
- Explicit, version-controllable parameters
- Categorical structure enables domain mixing

## Architecture

### The Semantic Bridge: OBJECT/LOOK/ACTION

Maps naturally to Three.js/WebGL structure:
- **OBJECT** = geometric_primitive + spatial_composition
- **LOOK** = material_system + color_palette + lighting_mood
- **ACTION** = motion_pattern + temporal_rhythm

### Three-Layer Olog Pattern

**Layer 1 (Foundation - 0 tokens):**
- Geometric primitives: sphere, cube, torus, cylinder, plane, text_3d, icosahedron, particle_system
- Material systems: metallic, glass, neon, matte, holographic, plastic
- Motion patterns: rotate, pulse, float, spiral, expand, wave, flicker, orbit
- Color palettes: cyberpunk, warm_gold, cool_blue, monochrome, fire, forest
- Lighting moods: dramatic_side, soft_ambient, neon_glow, rim_light, studio
- Spatial compositions: centered, grid_array, spiral_path, random_scatter, orbital_ring

**Layer 2 (Deterministic Mapping - 0 tokens):**
- Primitive → Three.js geometry configuration
- Material → shader/material parameters
- Motion → animation function specification
- Palette → exact hex color values
- Lighting → WebGL light setup
- All mappings are deterministic lookups (zero LLM cost)

**Layer 3 (Synthesis Interface - ~200 tokens):**
- Provides structured parameters to Gemini/Claude
- LLM synthesizes final HTML/CSS/JavaScript
- Code generation only, not parameter discovery

## Usage

### 1. Browse Available Options

```python
# See what geometric primitives are available
list_geometric_primitives()

# Browse material systems
list_material_systems()

# Check motion patterns
list_motion_patterns()

# View color palettes
list_color_palettes()

# See lighting configurations
list_lighting_moods()
```

### 2. Map Parameters (Layer 2 - Deterministic)

```python
# Map OBJECT/LOOK/ACTION to Three.js parameters
map_object_look_action(
    primitive="sphere",
    material="neon",
    motion="pulse",
    color_palette="cyberpunk",
    lighting="neon_glow",
    composition="centered"
)
```

Returns complete Three.js parameter specification (0 tokens).

### 3. Generate Synthesis Context (Layer 3 Interface)

```python
generate_synthesis_context(
    primitive="torus",
    material="metallic",
    motion="rotate",
    color_palette="warm_gold",
    lighting="dramatic_side",
    composition="centered",
    user_intent="A luxurious rotating golden ring with warm lighting"
)
```

Returns:
- All deterministic parameters from Layer 1-2
- Synthesis instructions for Gemini/Claude
- Intentionality explanation
- Cost analysis

### 4. Synthesize with Gemini 3

Take the synthesis context and pass to Gemini 3:

```
Prompt: [Paste complete synthesis context]
```

Gemini generates self-contained HTML file with Three.js animation.

### 5. Execute & Capture

- Save HTML file
- Open in browser
- Screen record the live animation
- Use in your video projects

## Domain Functors (Composability)

### Cocktail Aesthetics → Motion Graphics

```python
apply_cocktail_aesthetic(
    base_primitive="sphere",
    base_motion="pulse",
    cocktail_name="old_fashioned"
)
```

Maps cocktail lighting mood and color to Three.js parameters:
- Old Fashioned → warm tungsten glow, amber tones, dramatic side lighting
- Daiquiri → cool diffused light, crisp blues
- Negroni → dramatic red glow, bitter intensity

### Future Functors

- **Origami → Geometry**: Fold patterns → structural composition
- **Jazz → Rhythm**: Temporal structure → animation timing
- **Wine → Material**: Tasting notes → surface qualities

## Cost Analysis

### Pure LLM Approach
```
User: "Create a glowing sphere that pulses"
→ Gemini generates full code: ~800 tokens

User: "Make it gold instead of purple"
→ Gemini regenerates: ~800 tokens

User: "Add rotation"
→ Gemini regenerates: ~800 tokens

Total: ~2400 tokens for 3 iterations
```

### Lushy MCP Approach
```
User: "Create a glowing sphere that pulses"
→ MCP maps parameters: 0 tokens
→ Gemini synthesis: ~200 tokens

User: "Make it gold instead of purple"
→ MCP updates palette: 0 tokens
→ Gemini synthesis: ~200 tokens

User: "Add rotation"
→ MCP adds motion: 0 tokens
→ Gemini synthesis: ~200 tokens

Total: ~600 tokens for 3 iterations (75% savings)
```

## Example Compositions

### Cyberpunk Sphere
```python
generate_synthesis_context(
    primitive="icosahedron",
    material="neon",
    motion="rotate",
    color_palette="cyberpunk",
    lighting="neon_glow"
)
```

### Elegant Gold Ring
```python
generate_synthesis_context(
    primitive="torus",
    material="metallic",
    motion="rotate",
    color_palette="warm_gold",
    lighting="dramatic_side"
)
```

### Ethereal Particle Cloud
```python
generate_synthesis_context(
    primitive="particle_system",
    material="holographic",
    motion="float",
    color_palette="pastel_dream",
    lighting="soft_ambient",
    composition="random_scatter"
)
```

## Installation

### Local Development

```bash
cd motion-graphics-mcp
pip install -e .
python -m motion_graphics_mcp
```

### FastMCP Cloud Deployment

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial motion graphics MCP"
git push

# Deploy via FastMCP Cloud
# Entrypoint: server.py:mcp
```

## Tools Reference

### Layer 1 (Foundation)
- `list_geometric_primitives()` - Browse OBJECT options
- `list_material_systems()` - Browse LOOK options
- `list_motion_patterns()` - Browse ACTION options
- `list_color_palettes()` - View color schemes
- `list_lighting_moods()` - View lighting configurations
- `list_spatial_compositions()` - View layout patterns

### Layer 2 (Deterministic Mapping)
- `get_primitive_parameters(name)` - Get Three.js geometry config
- `get_material_parameters(name)` - Get shader/material config
- `get_motion_parameters(name)` - Get animation function config
- `map_object_look_action(...)` - Complete OBJECT/LOOK/ACTION mapping

### Layer 3 (Synthesis Interface)
- `generate_synthesis_context(...)` - Main tool for preparing specifications

### Domain Functors
- `apply_cocktail_aesthetic(...)` - Compose with cocktail aesthetics
- `list_domain_functors()` - See available domain compositions

### Meta
- `get_intentionality()` - Understand why this approach works
- `get_server_info()` - Server architecture and usage

## Philosophy

**Procedural motion graphics (code-driven) is superior to manual keyframing:**

1. **Mathematical smoothness**: Functions create organic movement impossible to fake manually
2. **Infinite iteration**: Change parameters, not keyframes
3. **Deterministic**: Same parameters = same result
4. **Compositional**: Systematic domain mixing via functors
5. **Efficient**: 60-85% token savings vs pure LLM 

**Your ability to describe a visual is more important than your ability to manipulate a timeline.**

## Categorical Structure

This MCP server is a **Lushy Brick** - a categorically-verified aesthetic module that:
- Defines a complete taxonomy (olog)
- Provides deterministic mappings (functors)
- Composes with other domains (natural transformations)
- Guarantees structural coherence (commutative diagrams)

The OBJECT/LOOK/ACTION pattern is a natural functor from aesthetic intent to executable code.

## License

MIT

## Contact

Built by Lushy AI - categorical infrastructure for the AI creator economy.
- Web: https://lushy.ai
- Email: dal@lushy.ai
