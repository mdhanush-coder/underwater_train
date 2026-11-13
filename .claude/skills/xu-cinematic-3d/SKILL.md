---
name: xu-cinematic-3d
description: XplainedUnseen Blender/Unreal cinematic journey method: additive modules on existing assets, continuous camera paths with hold keys, 3D labels attached to components, CPU frame-fit checks, small contact-sheet reviews, and render-safety rules. Use after xu-research-first when building cutaways, camera journeys, landing stations, underground, cable, repeater or data-centre sequences.
argument-hint: "[the 3D sequence/asset to build or fix]"
---

# XU cinematic 3D

Run **xu-research-first** first (real mechanism, real references, best-practice camera grammar). Then:

## Method (learned building EP002 journey Stages B and C)
- **Inspect before building** (`blender/script` + bpy: collections, cameras, animation, polygon count). `blender/inspect` failed with an engine error on .blend input; use bpy.
- **Additive modules, never destructive:** open the existing .blend (or exec the existing build scripts read-only) and add new objects in a new collection; save under a new version name in `out`; keep merged objects untouched. Keep everything under the asset's own folder (e.g. `production/assets/journey/`), versioned.
- **Reference lessons beat generic assets:** real landing stations are plain, fenced low sheds with roof air-conditioning and no visible cable; a 40 mm duct is tiny, so show it by getting the camera within about 0.7 m and by a leader callout, not by scaling it.
- **Booleans:** Exact booleans on meshes built from overlapping boxes drop geometry. Rebuild from clean manifold pieces or construct the cut shape directly (half-shell). Curves cannot take Boolean modifiers. Do not leave solids coplanar with a cut face (set the face back about 3 cm so the cut part stands proud).
- **Camera:** continuous path with a TRACK_TO target empty; Bezier easing; **hold keys** (duplicate the key) wherever a label must be read; keep speed plausible (about 15 m/s max for fly-throughs; extend frames instead of rushing).
- **Labels:** text object + dark plate + thin leader + anchor dot, anchored to the real component position (read the build script for coordinates); emission fades in over 10 frames; `hide_render` keyed outside the label window; white text on pale sand is unreadable, so always use a dark plate.
- **Colour meaning:** cyan = optical signal, amber = electrical power; illustrative pulses carry an "ILLUSTRATIVE" caption (camera-parented plate about 0.45 m in front of the camera).

## Visual grammar from reference studies
Before designing scale, number or label visuals, read [references/branch-visual-grammar.md](references/branch-visual-grammar.md): 30 rules from a frame study of Branch Education (scale gaps, count-ups, magnifier inserts, roadmap card, analogy worlds, label hierarchy), with evidence timestamps and which ones conflict with a project's no-box rule.

## Verification without a render
1. CPU projection check: `production/assets/journey/check_labels.py <build script>` (reads KEYS and LABELS/CALLOUTS, sweeps every easing position; limit 0.92 of the frame).
2. Build-only Blender job measuring real plates through the real animation with `bpy_extras.object_utils.world_to_camera_view` (no render).
3. Contact sheets only: 640x360, 24 spp, 8 tiles via numpy in the script (`xstack` locally); view with Read. Never start full renders as part of review.

## Render-safety rules (user)
- Do not queue GPU renders while another session (`ListAgents`) is busy or the queue is unverified (queue depth is not exposed; `get_job` `waitMs` > 0 shows contention). Build-only and contact-sheet jobs are short; full renders wait for the user.
- Never overwrite another session's outputs (`renders/edit_work_v008/`, `renders/roughcut/*_v008.mp4`, motion-graphics outputs).
- Poll jobs sparingly; two Blender GPU pods only.

## Checklist
Reused existing assets · new collection and version · labels inside frame at their window (check_labels + bpy check) · cable never visible above ground in exterior shots · optical vs power colours correct · NOTES.md has research, files, verification, remaining issues.
