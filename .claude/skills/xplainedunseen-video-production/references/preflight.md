# Pre-flight: run BEFORE acting, state the result in the reply

Rule (user, 2026-11-06): lessons are not enough, the next action must not repeat a past mistake. Before each action below, read its row,
run the check, and say in the reply "pre-flight: <checks run>, <result>". A FAIL blocks the action. When a new mistake happens, add a row here
AND an automated check to `blender/scripts/preflight.py` in the same turn, and test that the checker has no false positives (it did once).

## Automated check for any .blend (run first, costs 2 seconds)
`blender/script` with the .blend as `input`, `files: {"preflight.py": <uploaded script>}`, code `exec(compile(open(inputs['preflight.py']).read(),'preflight','exec'),globals())`,
args `{"expect": {"hero_verts": 446157, "range": [1, 744]}}`. Reads: images packed, no strong volume emission, no sky plane, world photo sky is camera-only with Mirror,
wings have no motion of their own, hero vertex total unchanged, fps/step/markers/range, no material override, AgX and exposure, scanned textures on hero materials,
rig root and scale exist, few volume objects. Verdict `BLOCK` = do not render. Last result on the 840-frame `pushpak_viman_v001.blend`: all 16 PASS (2026-11-06); it correctly BLOCKED the first bake (unpacked images).

## Before each kind of action
| About to... | Check first (mistake it prevents) |
|---|---|
| Light a scene with an HDRI | Measure the sun with a panorama probe at 2 rotations; never assume azimuth or rotation sign (was 180 deg off). |
| Put a photo behind the scene | Use a world-shader projection (Light Path Is Camera Ray, Mirror), never a plane (edge visible). Render the extreme frames of every shot to check coverage. |
| Add clouds or fog | No volume emission; height-ramped noise with boosted contrast; floor extent must match the horizon dip; budget about 12 s per 720p frame, abort the idea if a test frame costs more than 3x that. |
| Judge colour of metal | If gold looks silver, test constant gold and grey override renders before touching lights; then exposure. A change with no visible effect means the hypothesis is wrong. |
| Save a .blend for another job | Pack every image (`im.pack()`) INSIDE the script that saves (stage-7 tail does it); run the automated pre-flight on the saved file, expect about 62 MB. |
| Accept user-chosen cameras | Review stills of EVERY shot (start, middle, end) with the real sky: the plate covers only +-32 deg of azimuth, so check the shots that look away from the sun; the preflight now requires the photo-to-HDRI fade. |
| Add clouds or volumes | Test cost on 12 frames first; each extra volume box was about 3x per frame. Use world-shader clouds for the far field. |
| Frame a camera move | Compute both end frames from the subject size (hull 8.5 m long and tall) and check stills at both ends before the clip; state that persists (yaw) must continue into the next shot. |
| Change camera moves | Edit `SHOTS` in `stage5_block.txt`, re-run assemble_stage5, patch_stage6, patch_stage7; plan first in `production/motion-plan.md`; review stills at move start/middle/end and hold end. |
| Render an animation on EngineX | Ask for `format: png` (one zip) and encode locally; verify frame count and duration of any mp4 (a 72-frame mp4 came back with 1 frame). |
| Call EngineX tools | Upload scripts and zips once and exec them; `get_job waitMs` at most about 60000; use `idempotencyKey`; one zip, not many signed URLs; copy signatures exactly. |
| Write a Blender script | `import os`/numpy yourself (only bpy, bmesh, mathutils, math exist); JSON-safe result keys (strings); set properties through names verified on the pod (Musgrave does not exist; FFMPEG format does not exist). |
| Write text or scripts from the shell | Use the Write tool, then `py -I file.py`; heredocs break on quote patterns. |
| Texture a hero asset | Triplanar locked to the root empty (`TexCoord.object`), bump from displacement (no tangent normal maps with box projection); keep imported hierarchy; never animate the wings. |
| Choose assets from the web | CC0 or CC BY only (not BY-SA); write CREDITS immediately; verify licence on the page metadata. |
| Report a frame or clip | View it first (contact sheet for motion); say what is still wrong; never say "photoreal" while a known weakness exists. |
| Start a long job | Estimate from the last cost per frame, set a timer, do not poll; cancel only when far past the estimate. |
| The user shows a defect | Find the root cause in the manual page, fix the cause, add the check, run it, then show the frames that failed before. |
