---
name: enginex-no-failed-runs
description: "EngineX now pauses an engine after failed jobs in a row; never submit a run that can fail, check everything locally first"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 29ecb82e-471d-450e-b0e8-b97186813c0b
  modified: 2026-11-11T15:47:43.937Z
---

Do not let EngineX runs fail. EngineX rule (get_usage pauseAfter, checked 2026-11-12): 3 failed jobs in a row (cancelled ones count) pause that engine for 10 minutes; each workflow (Imagine-Pro, 3d-shapeForge) and the Generation engine keep their own failedInARow count, visible in get_usage (Blender paused 10 min on 2026-11-11).

**Why:** user said "do not make the runs failed on the enginex, new rules are implemented". On 2026-11-11 two cancels + two NameError crashes (job file built without science_s3s4/pfbr_model) blocked Blender.

**How to apply:**
- Before any blender/script submit: build the job file with every module it needs (thorium: `build_job.py science_s3s4.py pfbr_model.py dune_scene.py <shot>.py`), syntax-check it, and AST-check that no used name is undefined.
- describe_operation / list_workflows first and pass only the inputs the operation takes (e.g. text-to-music has no `seed`).
- Keep scenes light enough that you never have to cancel them: test with a cheap review (few frames, low samples) before a full anim.
- Avoid cancelling where you can. If a job hangs, say so to the user before cancelling.
- See [[enginex-blender-capabilities]].
