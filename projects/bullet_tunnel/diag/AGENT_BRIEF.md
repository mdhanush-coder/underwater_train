# Brief for chapter agents (bullet-train undersea tunnel, Hinglish explainer, 1920x1080, 30 fps)

Project: `projects/bullet_tunnel/`. Voice is final (`audio/vo_hinglish_arnav_v3.wav`); per-line timings + visual notes
are in `shots.json` (fields ch, n, start, end, text, meta). Chapter plate length = chapter's first line start to the next
chapter's first line start (ch4 130.294-184.818 = 54.52 s, ch5 184.818-233.903 = 49.09 s, ch6 233.903-275.905 = 42.0 s,
ch7 275.905-end 310.5 = 34.6 s).

## Your job
Build ONE Blender set script `blender/<name>.py` for your chapter, preview it on EngineX, look at the frames, fix, and
return. Do NOT render the full animation unless your prompt says so. Do NOT build overlays (the lead does text).

## How a job is built and run (exact)
1. Read `blender/d_tbm.py` (chapter 3, the template: `build()`, `PATH` of (t, cam, target, lens) keys, `path_camera`,
   `anchors()`, `run(args)` with preview/anim modes) and `blender/bt_model.py` (shared helpers: `mat`, `noisy`, `Acc`
   box/cyl/beam/lattice/sphere, `build_tbm(name, gantries)` (local +Z = dig direction, root rotated so +Z -> world +X;
   inside the TBM local up = -x), `strata`, `path_camera`, `rigged_worker`). Reuse them; do not edit bt_model.py
   (another agent may be using it). Put chapter-only helpers in your own file.
2. Concatenate: `cat .claude/skills/blender-animation/scripts/skilllib.py projects/bullet_tunnel/blender/bt_model.py
   projects/bullet_tunnel/blender/<name>.py > projects/bullet_tunnel/blender/_job_<name>.py`
3. VALIDATE LOCALLY FIRST (user rule: no failed EngineX runs): `python -c "import ast;ast.parse(open(...).read())"`,
   re-read for Blender 5.2 API mistakes (below). Failed runs pause the engine.
4. `mcp__editor-api__create_upload_url` -> `curl -T` the job file -> key.
5. `mcp__editor-api__run_operation` engine `blender`, operation `script`, params
   `{"code": "exec(open(inputs['job.py']).read(), globals())", "files": {"job.py": "<key>"}, "args": {"mode": "preview", "pct": 50}}`
   (check `describe_operation blender script` once for exact param names), with an `idempotencyKey` and `waitMs: 0`,
   then `get_job` to poll (waitMs <= 110000). Outputs land in `out` (PNG stills t_XX.X.png).
6. `image/montage` of the stills (input list, columns 4, tileWidth 640, tileHeight 360) -> `sign_output` -> curl to
   `diag/<name>_sheet.jpg` -> Read it and LOOK. Load tools with ToolSearch ("select:mcp__editor-api__run_operation,...").

## Blender 5.2 gotchas (all real failures)
- Sky: `sky_type='SINGLE_SCATTERING'` (NISHITA fails). No world volume haze (turned scenes black).
- Mix node: pick sockets by `.type == 'RGBA'`. Layered actions: use `fcurves_of(obj)` not `obj.animation_data.action.fcurves`.
- Headless: no `selected_objects` after operators; use the returned/active object.
- Eevee: `BLENDER_EEVEE`, `taa_render_samples` 32, view_transform 'Standard', exposure ~0.1.
- Emission above ~5 clips to white: keep glows <= 4 (arrows, LEDs).
- Exact boolean on overlapping boxes drops geometry; build manifold pieces.

## Quality bar (user: "perfect geometry, production level, max 3D")
- Realistic materials (steel, concrete segments, wet rock, grey slurry, blue water). No default grey. Use `noisy()`.
- Detailed geometry, real proportions in metres: TBM 13.6 m cutterhead, lining 13.1 m OD, segments ~2 m wide, 0.5 m
  thick, 9 + 1 key per ring (check `01_research.md`).
- ONE continuous camera per chapter (no cuts inside the plate), eased keys, the camera slow and nearly still while a
  line is being read, a new view per idea (~every 4-5 s) following the `meta` notes line by line.
- Things move: machines, arms, fluids, lights. Nothing pops in without a reason.
- No text in 3D (overlays are 2D, added later). Leave clear dark space (left third or top-left) for text, never cover
  the subject.
- Charcoal-gold is for overlays only; 3D uses realistic colours. Illustrative arrows: gold (#F5B700-ish, emission <= 4)
  outward, cyan-blue inward.
- MG-map lines in the notes (ch6 line 65, ch7 lines 78-79) are NOT yours: keep a calm 3D view there (the lead overlays a map).

## Return (short)
Script path, job id, sheet path, what you checked in the frames and fixed, any open issue, and `anchors` (screen 0-1
positions of the parts the text will point at, from your `anchors()` call) for each line's subject.
