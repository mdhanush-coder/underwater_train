---
name: enginex-blender-capabilities
description: Tested 2026-11-10 - which Blender techniques work headless on EngineX blender/script (5.2.3 LTS) and the gotchas
metadata:
  node_type: memory
  type: reference
  originSessionId: 6fa48d2f-fdcf-4fda-8f2e-18db0d37df07
  modified: 2026-11-10T12:31:19.410Z
---

Probed EngineX blender/script (Blender 5.2.3 LTS, OptiX GPU, OpenVDB/fluid/USD/Alembic built in) on 2026-11-10 with real bakes/renders.

Works headless: Cycles, EEVEE (engine id 'BLENDER_EEVEE', not _NEXT), Freestyle (lineset needs `bpy.data.linestyles.new` in a factory scene), compositor (5.x: `scene.compositing_node_group` + NodeGroupOutput, no scene.node_tree), Keying/chroma key, colour balance/AgX looks, GN procedural city, GN simulation-zone swarm, Mantaflow liquid (64 res, 30 fr = 5.3 s) and smoke -> .vdb, VDB load + render, cloth, soft body, rigid body, particles, dynamic paint (`dpaint.bake` image sequence), keyframes, drivers (python expressions), constraints, shape keys, armature + IK + auto weights, Rigify generate (706 bones), PBR + texture maps, UV smart project, Cycles baking, vertex colour attributes, grease pencil v3 (`bpy.data.grease_pencils_v3`), motion tracking (`clip.track_markers` works via temp_override on the job's window area; solve_camera present).

Not available / broken: texture-paint brush stroke operator CRASHES Blender (segfault) -> paint via image pixels, bake, or projected image instead. CloudRig not installed (only rigify among rigging addons; no cell_fracture); worker can reach extensions.blender.org, so it could be installed per job.

Gotchas: operators need the target as `view_layer.objects.active` (temp_override alone did not enter edit mode); read GN point clouds via a Points-to-Vertices node + to_mesh.
