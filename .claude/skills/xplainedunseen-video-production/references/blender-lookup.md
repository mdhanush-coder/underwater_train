# Blender documentation lookup (documentation first, implementation second)

**Primary manual: Blender 5.3 (official), local plain-text copy, 2,425 pages, built 2026-11-06 from
`https://docs.blender.org/manual/en/5.3/blender_manual_html.zip`:**
`C:/Users/dinot/OneDrive/Pictures/Documents/Deepsoch/enginex_ideas/.claude/blender_manual_v530_en_text/`
- `INDEX.md` lists every page as `path | title | size`, grouped by section. Grep it by topic first.
- `text/<section>/<page>.txt` holds the page (first lines: `TITLE:` and `PATH:`). Images are not stored; the page URL is
  `https://docs.blender.org/manual/en/5.3/<PATH>`.
- The full HTML zip (387 MB, with images) is kept in the session scratch folder only; re-download from the URL above if images are needed.

**Fallback / older copy:** Blender 5.2 LTS XHTML at `.../enginex_ideas/.claude/blender_manual_v520_en.epub/`.

**VERSION CAVEAT (important):** EngineX Blender pods have run **Blender 5.2**. The 5.3 manual can describe features, node
options or UI that the pods do not have. Before using anything that looks new, run a tiny `blender/script` job that prints
`bpy.app.version_string` and checks the feature exists (`hasattr`, node type in `bpy.types`), log the result in
`ep001-lessons.md`, and fall back to the 5.2 manual page if it is missing. Treat a feature as unverified until then.

## Lookup hierarchy (token-cheap)
1. This file + `ep001-lessons.md` (cached answers).
2. `Grep -i` `INDEX.md` for the topic, then `Grep -i` the `text/` folder for the exact term; Read only the hit page (use `offset`/`limit`).
3. 5.2 manual or other sources only if 5.3 lacks it; say so.
Never read whole sections; never re-read a page already summarized here. If a feature is not in the manual: state it, mark the value unverified, test on a tiny scene before scaling.
**Do this before every model, material, light, camera, simulation or animation build** (section 32 of SKILL.md): name the manual page(s) you used in the shot or asset notes.

## Topic -> manual path (under `text/`, page counts in brackets)
- **Meshes and topology**: `modeling/meshes/` [139] (editing, tools, structure, primitives, UVs, retopology, selecting); **modifiers**: `modeling/modifiers/` [68] (generate, deform, normals, physics); curves `modeling/curves/` [21]; new curves `modeling/curves_new/` [14]; surfaces `modeling/surfaces/` [14]; text objects `modeling/texts/` [5]; metaballs `modeling/metas/` [7]; volumes `modeling/volumes/`; point cloud `modeling/point_cloud/`.
- **Geometry Nodes** (procedural models, instancing, fields, simulation, baking): `modeling/geometry_nodes/` [508] — `introduction.txt`, `fields.txt`, `instances.txt`, `baking.txt`, `performance.txt`, `attributes_reference.txt`, and node folders `mesh/ curve/ geometry/ instances/ simulation/ attribute/ input/ output/ utilities/ volume/ hair/ texture/ color/ point/ normals/ grease_pencil/`.
- **Materials / shaders / textures**: `render/materials/` [25], `render/shader_nodes/` [151]; **lights**: `render/lights/` [4]; cameras: under `render/` (see INDEX for `cameras`); **Cycles** `render/cycles/` [25]; **EEVEE** `render/eevee/` [25]; **Workbench** `render/workbench/` [8]; **color management (AgX)** `render/color_management/` [5]; **output / render settings** `render/output/` [16]; render layers `render/layers/`; Freestyle `render/freestyle/` [59].
- **Rigging and animation**: armatures `animation/armatures/` [63], constraints `animation/constraints/` [39], drivers `animation/drivers/`, shape keys `animation/shape_keys/`, keyframes `animation/keyframes/`; top-level `animation/` [124] pages (graph editor, NLA, dope sheet, motion paths).
- **Physics and simulation**: `physics/` — cloth, fluid [20], particles [29], rigid_body [19], soft_body [15], forces [18], dynamic_paint.
- **Compositing**: `compositing/types/` [226]; **video editing (VSE)**: `video_editing/` [66]; movie clip / tracking: `movie_clip/` [35].
- **Sculpt / paint**: `sculpt_paint/sculpting/` [73], brush, texture_paint, vertex_paint, weight_paint, curves_sculpting.
- **Scene / objects / collections**: `scene_layout/` [object 57, collections 3, scene 3]; **editors and UI**: `editors/` [192], `interface/` [59]; **files / I-O / linking / packing**: `files/` [33]; add-ons: `addons/` [19]; Grease Pencil: `grease_pencil/` [117]; getting started: `getting_started/`; advanced (Python API intro, command line, scripting): `advanced/` [32]; troubleshooting: `troubleshooting/`.
- The **Python API is not in this manual**: confirm `bpy` names with a tiny test (`blender/script`, `inspect`) and log the result in `ep001-lessons.md`.

## Priority areas
Meshes and topology, materials and texturing, Geometry Nodes, lighting and rendering, rigging and animation, cameras, physics, compositing, procedural workflows.

## Blender build rules
Real scale and applied transforms; descriptive names (never Cube.001); collections per section 9 of SKILL.md; bevels / weighted normals for highlights; instancing for repeats; pivots at real axes; ease curves, not linear; AgX, 24 fps; preview low-res / low spp before final; Cycles for hero shots.
