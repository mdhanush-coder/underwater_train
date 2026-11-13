> **LATEST STATE: read `projects/bullet_tunnel/SESSION_HANDOFF.md` first (2026-11-13 evening).**

# Handoff: Mumbai bullet-train undersea tunnel (Hinglish, ~5:10) - state 2026-11-13

Project: `projects/bullet_tunnel/`. Script `03_script.md` (83 lines, approved), timings `shots.json`, research
`01_research.md`. Voice (approved): `audio/vo_hinglish_arnav_v3.wav` (310 s), EngineX key
`input/2026-11-13/0fcbbd29-7968-4e37-b726-a398b8958c6b.wav`.

## Pipeline
- Blender set scripts: `blender/<set>.py` + shared model `blender/bt_model.py`. Bundle:
  `cat .claude/skills/blender-animation/scripts/skilllib.py projects/bullet_tunnel/blender/bt_model.py projects/bullet_tunnel/blender/<set>.py > projects/bullet_tunnel/blender/_job_<set>.py`
  -> upload -> `run_operation blender script` with `code: exec(open(inputs['job.py']).read(), globals())`,
  `files: {job.py: key}`, `args: {mode: preview|anim, pct: 50|100}`. Brief for chapter work: `diag/AGENT_BRIEF.md`.
- Overlays: `overlays/spec_<ch>.py` -> `overlays/build_mg.py` -> `overlays/<ch>.zip` -> `motion-graphic render`
  (project zip, media [plate key], audio voice key, audioStart = chapter start, format mp4, quality standard, poster false).

## Done (do not rebuild) - EngineX output keys
| Part | Global time | Output |
|---|---|---|
| Hook (v4, with text + voice) | 0-37.17 | `output/8c94f977-0cc2-4dd9-82f4-172728aee576/motion.mp4` |
| Ch2 route (MG) | 37.17-83.44 | `output/b50e87fc-0535-4d98-b2a1-0f0a091df01e/motion.mp4` |
| Ch3 TBM plate 1080p | 83.44-130.29 | `output/52c36daa-6857-4874-9742-bd5f4daf436d/ch3_tbm.mp4` |
| Ch3 composite (text + voice) | | job `85183f8c-a119-40af-8cc9-f46f5679d205` -> `motion.mp4` (check frames) |
| Hook cutaway re-render (cyan arrows) | | `output/ececdd67-6c79-460d-ab70-cb8d7f03c947/set_cutaway.mp4` |

## Next
1. Hook: T2 dissolve with the new cutaway (`video transition` inputs [`output/89eebefe-.../transition.mp4`, cutaway],
   fade 1.5 s, offset 25.6, key `bt-hook-T2-v4-cyan`), then re-render hook page `input/2026-11-13/64330a02-...zip`
   with it, yuv420p.
2. Ch4 slurry (54.52 s, `blender/e_slurry.py`), ch5 rings (49.09 s, `f_rings.py`), ch6 NATM rock (42.0 s,
   `g_natm.py`; MG map at line 65), ch7 finale (34.6 s, `h_finale.py`; lines 75-76 reuse Unreal sunset creek; MG map
   at lines 78-79; plate starts at chapter time 7.1 s). Preview -> review sheet -> anim -> `spec_ch4..7.py` overlays.
3. Assemble hook + ch2-ch7 with ~1 s dissolves, generated music bed ducked under the voice, sprite-check, deliver.
4. Later: English version.
