# Cached production lessons (from EP001; append, don't repeat lookups)

## Blender / render
- Drivers: use `pow()`, not `**`, or headless plasma stays dark.
- Lathe profiles must start at r=0 (r=0.5 mm leaves an axis "needle"); run the geometry check for loose edges.
- Per-shot exposure and light overrides; macro shots need their own light rig (out-of-focus metal washes the frame).
- Titanium under a warm key reads beige: keep it cool, dark metallic.
- Clay pass: dark clay (~0.24) with lights x0.3 beats a white override; keep real materials (`textured:true`).
- Facility / large halls read grey: colour-code and material-separate TF/PF/vessel/divertor, vary roughness.
- Preview 720p / low spp first, then 1080p at 48-384 spp; cancel jobs built on a known defect.
- Repeating the same clip (hero, exploded, nuclei, field lines) is a defect; use exploded view only where parts are the point.

## Motion graphics (GSAP)
- A canvas page needs a literal `window.__timelines = {"id": tl}` whose onUpdate calls draw(t); otherwise only frame 0 renders.
- `fromTo` renders its from-state at t=0: use `immediateRender:false` for later overlays.
- `composition` can't combine with `at`; one zip per page with the page as index.html.

## Captions / audio / ops
- Word timing comes from `transcribe/align`, never estimated. Align one chapter per call and save only [word,start,end] (~10k tokens inline otherwise).
- No system ffmpeg/Blender: Blender work goes through EngineX (two Blender GPU pods, `fleet_status` once). A local ffmpeg exists via `py -m pip install imageio-ffmpeg` (`imageio_ffmpeg.get_ffmpeg_exe()`), and yt-dlp via pip; use `py -I` for scripts that read downloaded data.
- Windows Python writing text: `python -X utf8`, and encode before opening the file for write (a cp1252 error once emptied a file).
- Never let a caption linger into the next phrase.

# Lessons from the Pushpaka documentary (2026-11-06). Rule: whenever you learn something new or make a mistake, append it HERE in the same turn.

## Verified facts about the EngineX Blender pod (5.2.3 LTS)
- AgX and Cycles (OptiX) work; EEVEE props include `use_raytracing`, `volumetric_samples`; there is NO Musgrave node (merged into Noise); Sky Texture `sky_type` is SINGLE_SCATTERING / MULTIPLE_SCATTERING / PREETHAM / HOSEK_WILKIE; actions are layered (`action.layers[].strips[].channelbags[].fcurves`; `fcurves` is None on the action itself).
- `blender/script` cannot write video: `FFMPEG` is not an image-format enum value here. `blender/render format=mp4` returned a ONE-frame MP4 for a 72-frame range (it reported frames:72, the file was 0.08 s): re-test before trusting it. `format=png` returns ONE zip of frames; encode locally.
- A `.blend` saved by a script must have its images PACKED (`im.pack()` for every FILE image), or a separate render job loses textures and HDRIs.
- Script result dicts must have string keys (tuple keys crash `json.dumps`); wrap them with `str(...)`.
- `get_job waitMs` above about 60 s times out the tool; `idempotencyKey` returns the existing job (`status: existing`) when a call times out; poll with timers (background `sleep`), not loops.
- Token-cheap pattern: upload the script and zips once (`create_upload_url` + curl), then run `exec(compile(open(inputs['x.py']).read(), ...), globals())` with `args`; otherwise every job echoes the whole code in its params.
- `sign_output` takes at most 50 keys and every signed URL is long: ask for ONE zip of frames, never download frames one by one; copy signatures exactly (one typo gave a 403).

## Lighting, sky and exposure (mistake, cause, fix)
- NEVER assume an HDRI's orientation or a Mapping rotation sign. Measure with a panorama probe (equirect camera, tiny exposure, brightest pixel) at rotation 0 and 30 deg. The analytic guess was 180 deg off with the sign inverted.
- A photo on a flat plane has edges and the camera sees past it (the user caught a pale bar). Project the photo in the WORLD shader by view direction (Math ARCTAN2 / ARCSINE / WRAP into UV, Image Texture extension Mirror, clamp v) and show it to camera rays only with Light Path > Is Camera Ray, while the HDRI lights the scene. Check coverage at the extreme frames of every shot before showing it.
- Volume emission accumulates through the whole thickness and blows a cloud floor to white: do not use it. Cloud tops need density = noise minus a height ramp, with the noise contrast boosted first; plain noise times a spherical mask gives a flat slab.
- A floor at depth h below the eye reaches only h / tan(dip) before it crosses the horizon dip: match the dip to the floor extent (40 m deep and 2 km long means about 1 deg) or the far floor shows as a white wall above the horizon.
- Procedural 3D cloud towers with distortion looked like brown dust and cost about 77 s per 720p frame against 12 s: rejected. A photo sky plus a structured floor is the efficient answer.
- Gold that clips pale silver is usually AgX roll-off of very bright sky reflections, not texture or normals. Prove it with constant-gold and grey override renders (`view_layer.material_override`), then lower exposure and raise the camera-visible photo to compensate. If a parameter change has zero visible effect, the hypothesis is wrong.
- Metal reflecting a blue sky turns olive/grey-green: warm the lighting HDRI (multiply, stronger toward the zenith with a Z gradient) to get golden-hour gold.

## Materials and texturing
- Triplanar projection that stays consistent across 300+ parts and moves with the vehicle: Texture Coordinate node `.object` = the asset's scale/root empty, Object output, Mapping scale = root scale / tile size in metres. Tangent-space normal maps do not work with box projection: use the displacement map through a Bump node.
- CC0 sources that worked: Poly Haven API `https://api.polyhaven.com/files/<id>` (maps by resolution); ambientCG `https://ambientcg.com/get?file=<ID>_2K-JPG.zip` (real scanned gold: Metal048A); Wikimedia Commons API for photos. Prefer CC0 or CC BY over CC BY-SA (share-alike risk when baked into a video) and write attributions to a CREDITS file immediately.
- Never destroy the imported hierarchy: add a parent scale empty and a rig root, sort objects into collections by material, and clear imported animation only after recording what it moved (it animated the wings, which must never flap).

## Camera and shots
- A backplate or HDRI with limited angular coverage constrains camera moves: turn the vehicle (yaw) with the camera held instead of orbiting, or project the photo into the world so any direction is covered.
- Define shot poses as functions of t with smootherstep and hold keys, review 2-3 frames per shot on a contact sheet, and bake to keyframes plus timeline markers (a camera per marker) only after approval.

## Process and review discipline
- View every frame before reporting. Reject regressions out loud and revert (the towers, the glowing floor). Change one thing per round and say why.
- When the user shows a defect in a screenshot, find the root cause in the manual (`blender_manual_v530_en_text`) before patching the symptom.
- Heredocs in the Bash tool break on some quote patterns (a lesson containing triple quotes broke one while recording it): write scripts and long text with the Write tool and run them with `py -I script.py`.
- A long job with no output is not a hung job: estimate from the previous cost per frame, set a timer, and cancel only when it is far past the estimate.

- Checker false positive (2026-11-06): the first pre-flight flagged the whole-vehicle hover on PUSHPAK_RIG_ROOT as "wing animation". A new automated check must be run once on a known-good file before it is trusted, and must scope to what it actually forbids (the wing own chain, stopping at the vehicle root).
- Enforcement (2026-11-06, user): recording lessons is not prevention. `preflight.md` + `blender/scripts/preflight.py` are run BEFORE actions; see SKILL.md section 41B.

## Motion Director pass on Act 1 (2026-11-06)
- The 840-frame master timeline is 7 shots (A1_01_open ... A1_07_final); plan lives in `pushpaka_viman/production/motion-plan.md`. The bake script is the chain `assemble_stage5.py` -> `patch_stage6.py` -> `patch_stage7.py`; edit `stage5_block.txt` (SHOTS) and re-run the chain, never hand-edit the built file.
- Mistake repeated: `patch_stage7.py` saved the .blend with unpacked images (19.7 MB instead of 62.7 MB). The preflight BLOCKed it before any render, which is the system working. Fix at the source: pack all images before `save_as_mainfile` in the stage-7 tail.
- Preflight false positive: exposure is now keyed from black in shot 1, so the check reads `sc.frame_set(frame_end)` to judge the held value.
- Motion tokens in code: `ease(x)` = sine in-out (`camera`), `drift` = linear; smootherstep (quintic) was too slow at the ends for a push (first ~20 frames hardly moved).
- Pod scripts predefine only bpy, bmesh, mathutils, math: `import os` (and numpy) yourself; a missing `os` failed a job (preflight row "Write a Blender script").
- Contact sheets: build them on the pod from bucket keys passed as `files` (no signed URLs to copy), then sign and download one JPEG.
- Framing rules found by review (not by guessing): a track must be sized from the vehicle length (hull about 8.5 m) so both ends keep the subject; the vehicle is about 8.5 m tall with the flag, so a 21 m shot needs 40 mm or wider to avoid cropping; a vehicle state (yaw) set in one shot must persist into the next shot or it pops at the cut.

## Camera Studio round (2026-11-06): user-chosen cameras, transitions, 360 degree sky, clouds
- When the user picks cameras freely, EVERY direction can appear on screen. A photo plate that covers only +-32 deg of azimuth shows a streaked void (Mirror extension) when the camera looks away. Review stills of every chosen shot with the real sky before the full render. Fix: fade the photo to the lighting HDRI between 22 and 42 deg off the plate centre (world shader), preflight row added.
- The studio page used a plain gradient sky, so it hid that problem. The studio is for choosing framing only; Blender stills are the judge.
- Clouds all around: extra volume floor boxes cost about 3x per box (a 12-frame 640x360 test ran over 5 minutes, cancelled by the 3x-budget rule). Do the far field in the world shader instead: a perspective-correct noise plane 60 m under the camera for rays below the horizon, plus stretched-noise banks above it. Cost stays 1.5 to 3 s per 640x360 24 spp frame. Keep one volume box for the forward view.
- Orbit moves must interpolate as an arc about the aim point (angle and radius), not as a straight line through the vehicle; use the shortest angle (the half orbit of A1_06 passes the +l side).
- Lens changes need lens keyframes (co.data.keyframe_insert('lens')). Yaw is keyed per frame from the shot's own start and end values.
- Transitions (Motion Director transitions.md): the relation here is one calm sequence, so one soft cross dissolve of 16 frames (0.67 s) at every cut, not film burns or flashes (those are retro). Render 8 handle frames either side of each cut (PAD=8) so both shots keep moving through the dissolve; nominal shot lengths stay, total render 936 frames for 840 nominal.
- Parallelism: two render jobs of the same engine run at once; the rest queue. Four 234-frame parts at 1080p took about half the wall time of one job.

## Capability audit (2026-11-10, XU reference-video research)
- RE-TESTED: `blender/render format=mp4 frames=all persistentData=true` on a 48-frame Cycles 720p/32spp scene returned a REAL 48-frame, 2.000 s, 24 fps h264 (NVENC) MP4 (`video/probe` nb_frames=48), 9.5 s wall. The older "ONE-frame MP4" note above is stale for the current pod (Blender 5.2.3 LTS); still probe every MP4.
- Verified in one scratch scene (no project files touched): Boolean DIFFERENCE (MANIFOLD) cutaway through a layered slab stack works; emission pulses travelling along beveled curve traces work with a keyed Mapping node (Object coords -> Separate XYZ X+Y -> FRACT -> ColorRamp -> Emission Color), keys set LINEAR via `preferences.edit.keyframe_new_interpolation_type`; camera DoF + keyed push-in work. `blender/script` params do NOT accept `waitMs` inside params: it is a top-level run_operation argument.
- media-fetch (EngineX) can pull YouTube info/subtitles/clip/download; `info` returns a huge `heatmap` array (about 100 entries): delegate or extract fields. No local yt-dlp/ffmpeg on the laptop right now.

## MATSYA-6000 MG builder (2026-11-10)
- `motion-graphic` with `project` + `composition` + `at` fails instantly ("Motion Graphic exited 2", 0.2 s, no stderr). One zip per page with the page as index.html works; snapshot of a 3-still page takes ~2 s on the card.
- GSAP `scale` + `svgOrigin`/`transformOrigin` on SVG `<circle>` elements shifted them off their centres (nodes landed 15-70 px away). Animate `attr:{r}` for dots/nodes instead; for groups set the `transform` attribute yourself in onUpdate.
- Canvas pages: drawing from `M.tl.eventCallback('onUpdate', draw)` reading `tl.time()` renders correctly (no hf-seek listener needed) as long as `window.__timelines` is set literally.
- Clip length comes from the root's `data-duration`; I also pad each timeline with `tl.set({}, {}, dur - 0.01)` so the last state holds (untested whether it is needed).
- Token-cheap loop: inline shared CSS/JS into each page with a local build script, zip per shot, `create_upload_url` + curl; view stills by signing all keys in one call and making ONE local contact sheet (PIL), not one Read per still.
- `transcribe-regional/words` on the 293 s Hindi voice returns 760 words in ~1 min, but the response (~76 KB) overflows the tool result: parse the saved file with Python.
- The motion-graphic queue is shared: 11 renders sat behind ~14 other jobs; queue all renders at once, then poll.
- No local ffmpeg/ffprobe on this desktop: check MP4 length with a tiny box parser (mvhd/stts) or `video/probe`.

## Motion-graphic batch (MATSYA-6000 shots 3.1-6.5, 2026-11-10)
- `motion-graphic/snapshot` with `project` + `composition: "x.html"` FAILED (exit 2, invalid_request): one zip per page with the page as `index.html` is the only reliable form (confirmed again).
- A presigned PUT from `create_upload_url` can be re-used for its whole hour: re-PUT the rebuilt zip to the SAME url and the same key carries the new page. Save the urls in a file (`projects/matsya6000/mg/urls.txt` + `up.sh`) and never ask for a new url per fix.
- Signed output URLs share one X-Amz-Date per sign call: pass only job id + signature to a local script that rebuilds the URL (`mg/sheet.py` makes 2-still contact sheets with PIL). Output keys are predictable: `output/<job>/still-0N.png`, `output/<job>/motion.mp4`.
- mg.js `M.in` / `M.fade` use fromTo with `immediateRender:false`: an element entering at t>0 is VISIBLE before its start. Hide first (`gsap.set(sel,{autoAlpha:0})`); `mg/x.js` wraps both. Same for any own `fromTo(...immediateRender:false)` (the KaTeX terms showed at 3 s).
- Scaling an SVG `<g>` with gsap: use `svgOrigin:'0 0'`, not `transformOrigin:'0 0'` (that is relative to the bbox and put the map pin off the coast). A `scale` tween with `svgOrigin` on circles drawn with cx/cy also drifted them off a line: tween `attr:{r}` instead.
- KaTeX: load katex.min.css + katex.min.js from jsdelivr in the page and pass `libraries:["katex"]`; `\textcolor{#hex}{}` works; render each term into its own span to build the equation up.
- CPU render of a 10 s 1080p SVG page: about 29 s; render result gives frames/fps/size, still probe the file (`mg/probe.py`, pure-python mp4 box walk, no ffmpeg needed).

## MATSYA-6000 Blender builder B1 (2026-11-10)
- P-a underwater look (world Absorption+Scatter volume, one 1200-1500 W spot, 3,500-flake GN snow): 0.24 s/frame at 960x540 48 spp (30 frames in 7 s). Full hero rig (seabed + vehicle + world volume + snow) at 1920x1080 64 spp + denoise, persistentData off: 2.2 s/frame (24 frames in 52 s). A homogeneous world volume is cheap; heterogeneous noise volumes (Pushpaka clouds) are what cost.
- P-b Boolean DIFFERENCE solver 'MANIFOLD' on a 192x96 UV-sphere thick shell (R 1.13 minus R 1.05, then a cube) is clean: 0 non-manifold edges, cut face = 2 n-gons. Bake it with `bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph))`; give the cut face its material by `normal.x > 0.99`.
- Blender 5.2: writing a Geometry Nodes modifier input (`md['Socket_2'] = v`) raises "id properties not supported for this type". Fix: each object gets its own copy of the group, set `group.interface.items_tree[...].default_value`, then re-assign `md.node_group` (None, then the group). Those inputs are not keyable this way: drift comes from Scene Time inside the group.
- World background and SUN lights are fully absorbed through an infinite world volume: "surface light" must be a finite emissive plane plus a wide spot ~25 m above, on a rig empty.
- Volume Scatter anisotropy 0.55 hides lamp cones when the camera is behind the lamps (light scatters away from the lens): use ~0.1 for behind/above views.
- An area light near the camera inside a world volume floods the frame with haze: keep rims on the far side and parent them to the moving subject.
- Dark Ti (#4A5560, metallic 1) in a black void reads flat black: give it something broad to reflect (5 m softbox overhead); in deep water a dim cool area key plus a rim keeps the silhouette. It stayed cool, never beige.
- `bpy.ops.wm.open_mainfile(bpy.data.filepath)` inside a script job, then re-exec the library (rebinds `S`), builds several shot rigs from one base .blend in ONE job (6 rigs + 18 contact frames in 10 s).
- Contact sheets on the pod: `bpy.ops.render.render(write_still=True)` per frame, tile with numpy via `image.pixels.foreach_get/foreach_set` (byte PNGs copy raw), sign one PNG.
- Bash heredoc appending Python broke again ("unexpected EOF"): append code with Edit/Write only.
- The `script` job's closing Workbench picture shows the LAST keyed camera state, not frame 1: judge framing from rendered contact frames.
- MISTAKE (coordinator caught it): an open tube cage with bevelled slab blocks reads as an ROV / primitive boxes, not a crewed submersible. Crewed HOVs (Alvin, Shinkai, Jiaolong, Fendouzhe) have an enclosed streamlined fairing: loft superellipse rings along the length (rounder top, flatter keel), cap the ends, Subsurf 2, two-tone livery by an object-z ColorRamp (constant), panel seams as a bump on fract(y/1.3). Check the silhouette type against real references before lighting.
- Fill/key/rim area lights in a water volume: Cycles `obj.visible_volume_scatter = False` plus EEVEE `light.volume_factor = 0` light the subject while the water stays black (otherwise the whole frame goes teal).
- Measure exposure on the subject only: render a Workbench FLAT white mask of the vehicle collections (same camera), then the share of masked pixels below 5 % luminance. A bounding box over-counts water.
- EEVEE on the Blender 5.2 pod: engine id 'BLENDER_EEVEE' (not _NEXT); `scene.eevee.use_raytracing`, `volumetric_samples`, `volumetric_tile_size`, `use_volumetric_shadows`, `volumetric_end`, `taa_render_samples` exist. The first EEVEE still pays ~12 s of shader compile, then 0.3-1.2 s at 960x540 and 0.68 s/frame at 1080p 64 spp (Cycles 2.2). It matched Cycles closely (cones, snow, paint, Ti) and came out slightly brighter: dark share 28-37 % vs Cycles 45-59 %. Weak point: lamp cones seen from behind are faint.
- Large area lights mirror as hot blobs in metal at 2 m: key them down for macro/patch moments and back up for the wide reveal.
- USER REJECTED the first ocean (2026-11-10): a noise-textured emissive plane read as clouds/camouflage, deep shots were pure black with no particles, the seabed a grey plane. What fixed it (EEVEE): Ocean modifier sheet (choppiness 0, small wave_scale; centre it, tiles grow from the origin; add a big flat far plane or the sheet edge shows at grazing angles) with a Snell's-window shader (dot(Incoming, Normal) > 0.66 -> bright sky + sun hot spot, else dark TIR teal); a sun keyed by depth plus an invisible Voronoi distance-to-edge gobo (DITHERED, transparent shadows) for caustics and shafts; world background blue ambient driven by the sun (SCRIPTED driver 'var*0.12' works headless); snow that follows the camera position (COPY_LOCATION, not parented) so flecks are always in shot and drift upward; abyssal plain = 120 m displaced grid + wave/voronoi/noise bump + GN nodules. Object volume puffs did not show in EEVEE: silt clouds as particle clouds (snow GN, alpha-blended silt material) with keyed scale/hide_render. A material used by nothing in the base .blend is dropped on save: `use_fake_user = True`.
- Looking straight up from just below the surface puts Snell's 97 deg window over the whole frame (blown white): go ~9 m deeper and pitch ~40 deg so the window, its rippled edge and the blue water all read.
- The new environment roughly triples EEVEE render time (4.9 192 f and 4.7 288 f each ~640 s on one pod).
- `get_job` needs the FULL job uuid (an 8-char prefix returns "no job"); recover short ids handed over by another agent by grepping the session transcripts. Final EEVEE 1080p renders: 140-380 s per shot (192-624 frames, ~0.6 s/frame incl. encode), several Blender pods in parallel. Probe locally with imageio_ffmpeg (`-f null` frame count, `select=eq(n\,N)` stills).
- KaTeX in a motion-graphic RENDER: the CDN katex.min.css is NOT applied in the render workers (snapshots looked fine), so HTML + MathML layers both showed, garbled. Fix that works: `katex.render(tex, el, {output:'mathml'})` (Chrome draws MathML natively, subscripts correct, no CSS). Always check a frame of the RENDERED mp4, not only a snapshot: ffmpeg ships with imageio_ffmpeg (`.../site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`).
- `motion-graphic/render` DOES accept `project` + `composition: "<page>.html"` (snapshot does not): one bundle zip with every page renders them all from ONE upload.
- Wrapping a shot timeline in a master (head offset + exit): `master.add(M.tl.paused(false), head)` - a PAUSED child added to a timeline never renders (whole clip blank except stray immediateRender tweens). Fade the page with `opacity` on the svg, not autoAlpha (children set visible by autoAlpha escape a hidden parent), no `overwrite:'auto'` (it killed the entrance on seek). End the exit on the last slot FRAME (head+slot-1/24), else that frame is still ~20 % visible.
- A queued EngineX job reads its input key when it is CLAIMED: re-PUT a fixed zip and every job not yet claimed picks up the fix; check `bytesIn` (zip size) on each result to see which version it rendered.
- ffmpeg `-ss` past the last frame time gives "Output file is empty" with exit 0: seek to (frames-1)/24 minus a hair.
