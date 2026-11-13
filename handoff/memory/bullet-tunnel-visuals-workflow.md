---
name: bullet-tunnel-visuals-workflow
description: "Bullet-train tunnel video visuals: voice v3 approved, shot clock, set build order, real TBM facts, Blender job gotchas"
metadata:
  node_type: memory
  type: project
  originSessionId: 47085ce1-ab78-4197-8123-bd5b371d9e7f
  modified: 2026-11-13T12:37:15.828Z
---

Voice `audio/vo_hinglish_arnav_v3.wav` (310 s) and the 83-line script were approved by the user on 2026-11-13; visuals started the same day.
User rule for visuals: do not waste tokens, make it perfect, take references from the internet (web facts; the 3D library has no TBM or tower crane).

**Why:** the user pays per token and wants film quality, not iterations of grey primitives.
**How to apply:** research the real object first, build once with real counts, review a lit sheet before any long render.

- Shot clock: `projects/bullet_tunnel/shots.json` from `build_timing.py` (DP-aligns script lines to transcript_v3 words, +-1 s).
- Set plan: `04_sets.md` (C shaft, A creek, B cutaway, MG maps, D TBM, E x-ray, F rings, G NATM). Build order C, A, B, then D-G.
- Code: `blender/bt_model.py` (shared Acc mesh accumulator, build_tbm with 84 discs / 124 scrapers / 16 bucket lips, lattice cranes), `blender/c_shaft.py` (set C job). Job = skilllib.py + bt_model.py + set file concatenated, uploaded, run with `exec(open(inputs['job.py']).read(), globals())`.
- Real facts (NHSRCL, NBM&CW, Afcons): cutterhead 13.6 m (Afcons says 13.5 m, 354.5 t), five shipments welded on site with 1,600 kg of welding, 84 discs, 124 scrapers, 16 bucket lips; Vikhroli shaft ~56 m deep (55 m per Afcons); TBM over 3,000 t; Mixshield. Swarajya: the formal 5 July ceremony was deferred for rain though excavation began - hedge the "5 July" opening if challenged.
- Blender 5.2 gotchas hit: sky_type 'NISHITA' is gone (use SINGLE_SCATTERING); ShaderNodeMix needs sockets picked by type RGBA; a cylinder wall keeps its caps (end_fill_type='NOTHING') and the top cap hides a pit seen from above; cameras must stay inside the shaft radius; an unchanged byte size between renders means the change never reached the frame.
- EngineX: blender runs are capped at 125 per day; a preview run is ~11 s; `get_job wait` can sit for minutes after the job ended, prefer `run_operation waitMs 90000`; the heredoc in Bash choked on some content, use the Write tool.
- Related: [[xu-story-narration-shot-rhythm]], [[next-video-bullet-train-tunnel]], [[xu-3d-realistic-colours]].

## Status 2026-11-13 (hook 0-37.4 s assembled, projects/bullet_tunnel/renders/hook_v1_with_voice_1080p.mp4)
- Pipeline that worked: Blender builds geometry -> GLB (<=40k verts/mesh, flat colours) -> Unreal (sky, Lumen, mirror water, camera) for the creek;
  shaft and cutaway stay Blender EEVEE (1080p renders take 1-2 min); video/transition fades (T1 offset 14.6 s d1.0, T2 offset 25.6 s d1.5);
  video/audio-replace (shortest) with vo v3; software transcode (tier cpu) forces yuv420p (the nvenc transition output was yuv444p).
- Plate scripts: blender/c_shaft.py (shaft, continuous camera, JCB + rigged crew), blender/env_creek.py + unreal/diag_creek.py (args test C = blur 0.25),
  blender/d_cutaway2.py (rigged 4-car train, soil layers, arrows). Camera report: diag/camera_report.txt.
- Rigging (user asked): library Reallusion Worker (101 bones; arms down = local Z rotation of L/R_Upperarm; remove its 'Background' mesh and
  renormalise from the body mesh) via bt_model.rigged_worker; train = armature + vertex-group skinning.
- Library facts: veh-jcb-excavator is untextured and has no tracks (recolour + add tracks); ai3d excavator reads as a table; no TBM/crane/train in library.
- Blur lesson: 1.25 fps draft previews smeared the shutter; always judge at 30 fps. Unreal 1080p standard ~5-6 min, daily cap 60.
- Still to do: render overlays/hook.html (screen blend), music bed, soften the faceted left-island canopies, motivated creek->cutaway move,
  Test D formal pass, English version, chapters 2-7.

## Progress 2026-11-13 evening (user: "complete the whole video, fast and perfect")
- Text style (user reference board): overlays/build_mg.py + specs.py/spec_ch2.py -> one motion-graphic page per chapter
  (plates as <video> assets, voice as audio + audioStart = chapter start). Compact 52 px Unbounded, OUTLINED kicker tags,
  gold highlight box (.box), gold underline bar, italic Inter statements, boxed number labels, gold-outlined cards with
  leaders. NO ICONS (user). Units lowercase via <span class="u">m</span>. Hook -> renders/hook_v4_golden_1080p.mp4.
- Golden hour: Unreal env='sunset' sun_el 4 sun_az 100 bloom .6 (unreal/diag_creek.py args) = sun in frame over the creek.
- Chapter clock (global s): ch1 0-37.4, ch2 37.17-83.44, ch3 83.44-130.29, ch4 130.29-184.82, ch5 184.82-233.9,
  ch6 233.9-275.9, ch7 275.9-310.1. Ch2 done as pure MG (map, depth profile+Qutub, cross-section) job bf9ba68e (re-render
  after the unit fix). Next: ch3 TBM plate (bt_model.build_tbm + gantries, continuous camera), ch4 x-ray chamber + MG
  pressure diagram, ch5 ring build (erector, segments), ch6 NATM rock tunnel, ch7 reuse creek sunset + cutaway; then
  concat all with dissolves, fix hook arrows (emission 9 blew to white -> 4, cyan).

