---
name: enginex-image-to-3d-workflows
description: "EngineX image-to-3D: run_workflow 3d-shapeForge (17.5M verts, flat-oriented, ~90 s) or 3d-pixelsculpt (5.2M verts, keeps photo tilt, ~57 s); both give textured GLB"
metadata:
  type: reference
---

Tested 2026-11-12 with a generated chip-on-board photo (Imagine-Pro, plain grey bg, single object). `run_workflow` takes `workflow` (not `name`) and `images:[key]`. Output is a ~60-70 MB GLB (not an image, despite the listing), with textures. Preview with blender/preview (workbench, ~5 s).
- 3d-shapeForge v1: 17.54M verts, ~91 s, re-orients the model flat, sharper pin/pad geometry.
- 3d-pixelsculpt v2: 5.24M verts, ~57 s, keeps the photo's tilt, truer photo texture, lighter.
Both need blender/optimize before animating. Best input: one object, plain background, three-quarter view.
**User rule (2026-11-12): use 3d-shapeForge only** for every image-to-3D generation ("it is giving better results").
**Why:** user asked to test image-to-3D for the missile-chips video hero chip.
**How to apply:** use for props/hero assets; always preview, then optimize/convert before a Blender scene. See [[enginex-blender-capabilities]], [[enginex-no-failed-runs]].
