---
name: enginex-unreal-glb-placement
description: "EngineX Unreal - unreal/scene re-centres the model's bbox (cameras miss once a site/sea is added); use unreal/script + ex.import_model, UE = (x, -y, z) of Blender in metres"
metadata:
  node_type: memory
  type: reference
  originSessionId: 29ecb82e-471d-450e-b0e8-b97186813c0b
  modified: 2026-11-11T11:10:41.075Z
---

Tested 2026-11-11 (Thorium, Unreal 5.8.4 on EngineX):
- `unreal/scene` stands the model on the floor centred on its bounding box. Adding a site (2 km sea, hall) moved the
  centre, so camera keys pointed at the sea / a wall. Do not use it for multi-part scenes.
- Use `unreal/script`: `acts = ex.import_model(inputs['x.glb'])` keeps every node where Blender put it.
  Measured exactly: UE metres = (Bx, -By, Bz); actor locations are in cm (divide by 100). Then
  `ex.environment('outdoor', sun_elevation, sun_azimuth, ground=False)` (our GLB has its own ground; the default
  ground at z=0 would cover a below-ground cutaway) and `film(acts, keys=[{time, location, lookAt}], duration=0.04,
  fps=25, format='png')` for a still. Script: projects/thorium/ue_still.py (solves the map from 3 landmarks).
- glTF cannot carry procedural (noise/ColorRamp) materials: flatten them before export or they import white.
- Cost: ~35-55 s per 720p still (build ~15 s + render). Blender GLB export with booleans applied ~15 s.
Related: [[enginex-blender-capabilities]], [[enginex-render-timeline-assembly]].
- 2026-11-13 (bullet tunnel): an open one-sided sheet (terrain) imported via import_model rendered INVISIBLE from above:
  the import flips winding, so only back-facing slopes showed; closed meshes (buildings, trees, boats) looked fine.
  Fix: export open surfaces with a reversed twin (bmesh duplicate + reverse_faces) or as closed solids.
  ExponentialHeightFogComponent in 5.8 has no 'fog_inscattering_color' or 'volumetric_fog' property (use fog_density,
  fog_height_falloff, start_distance). Unreal jobs are capped at 60 per day; a 110 MB GLB takes ~60-80 s to build.

