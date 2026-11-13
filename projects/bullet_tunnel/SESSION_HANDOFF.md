# Session handoff — bullet-train undersea tunnel (Hinglish), 2026-11-13 evening

Read the repo-root `CLAUDE.md` and `HANDOFF.md` first. This file is the latest state and replaces older parts of HANDOFF.md.

## User decisions made in this session (binding)
- **Voice = chips recipe**: `aarav`, expressiveness low, same brief on every line, English words pronounced in English. Arnav was rejected.
  Final voice: `audio/vo_hinglish_aarav_v4.wav` (EngineX `input/2026-11-13/75de18e9-bdc0-459e-b993-bd8fced1f6d7.wav`).
  It was built by `splice_v4.py`: aarav take + 4 retaken lines (21, 39, 40, 52; transcript verified), 4% faster, each line placed
  within 1.5 s of the old line. Line times are in `audio/v4_line_times.json` (start/end new, `old` = old start).
- **The lead does the animation work. No more agents** (the user said "do not give to agents").
- **Callouts must sit on the asset the whole time they are shown** (user saw leaders pointing at nothing).
- **No flicker** (user saw it in ch5). **Smooth transitions**, no hard cuts.
- Do not rebuild finished chapters; fix only what is wrong.

## Fixes found this session (now in the tools)
1. **Flicker** = EEVEE dropping virtual shadow-map tiles. Fix: `stable_eevee(sc)` in `blender/bt_model.py` (pool 2048-4096, 64 samples,
   no shadow jitter, shadows only on 2-4 key lights). Check every plate with `python diag/flick.py file.mp4` (target 0 %).
   Results: ch3 0 %, ch2 0 %; old ch4 15 %, ch5 28 %, ch7 25 % (re-rendered, see below). Hook flags are the shaft-dive motion, not flicker.
2. **Leaders off target**: they used one sampled point while the camera moves. Now every card uses a dense track (every 0.2 s) from the
   scene: `mode: "track"` in d_tbm / e_slurry / f_rings / g_natm / c_shaft, helper `track_screen()` in bt_model.py, results in
   `diag/track/<scene>.json`, read by `overlays/tracks.py` → `anchor=tr('e_slurry','chamber')`.
   Local run (no EngineX run used): `blender -b --factory-startup --python diag/track/run_local.py -- blender/_job_<scene>.py <abs>/diag/track/<scene>.json`
   (bundle first: `cat skilllib.py bt_model.py <scene>.py > _job_<scene>.py`). c_shaft needs library assets → EngineX only.
   Check: `python overlays/check_cards.py hook ch3 ch4 ch5 ch6` → every card must say TRACK OK.
3. **Voice change moved lines up to 2.5 s vs the 3D plates.** Fix: plates are retimed with a smooth warp (speed 0.75-1.35x, line error
   ≤ 0.6 s): `timewarp.py` → `audio/plate_warp.json`; `python retime.py in.mp4 out.mp4 <chapter number>` → `renders/plates_v4/`.
   Specs with `retimed=True` make leaders read the track at the plate's own clock (`pwarp` in build_mg.py). Text beats are still
   warped exactly to the new lines (`WP`). ch2 (pure MG) is not retimed.
4. **Uploaded files are served by their upload id**: a plate uploaded as input must be named in the spec as
   `<uuid>.mp4` (e.g. ch3 plate = `cc4b41e5-9f38-4609-9a80-19235270d3d8.mp4`), else MG exits 2.
5. Pages have a 0.8 s held tail (PAD in build_mg.py) so `assemble.py` can dissolve chapters at their true start (0.6 s xfade).
6. Optional dark backing behind a headline: `scrim=True` on a beat.

## Status per chapter (global start s)
| Part | State | Next step |
|---|---|---|
| Hook (0) | retimed plate uploaded `input/2026-11-13/287d8d20-13a1-49ab-857a-cbeb932dfe46.mp4` | wait c_shaft track job `1ecf6de4-de78-434e-b81e-93d05e988828` → pick the p0..p5 track that matches the 3 cards (old anchors (0.435,0.50) cutterhead, (0.50,0.37) discs, (0.575,0.66) 350 t at hook 12-14.8 s); set `SPECS['hook']` plates to the uuid name + `retimed=True`; render with audio v4, audioStart 0 |
| ch2 (37.17) | FINAL `output/bb80c156-dc8c-4eb2-a9f6-2946f3c8874a/motion.mp4` (0 % flicker) | none |
| ch3 (83.44) | FINAL render running `d36dd827-6a87-4ee1-acde-5d23975eee13` (retimed plate + tracks, frames checked) | sprite check, download |
| ch4 (130.294) | flicker-fixed anim queued `6f669c00-e3f4-4a3d-b9e3-4a2327fd6962` (out `ch4_slurry.mp4`); spec has tracks | flick.py (gauge at 33 s!) → retime ch 4 → upload → spec plate uuid → render, audioStart 130.294 |
| ch5 (184.818) | flicker-fixed plate DONE `output/40142fb5-0f03-46be-a2cf-e96bc1f5c65a/ch5_rings.mp4` | flick.py, retime 5, run f_rings track locally (was interrupted), spec anchors → `tr('f_rings','erector_arm'/'segment'/'grout_new')`, render |
| ch6 (233.903) | anim running `a235b021-e1f1-4f92-9d1c-291639400701` (`ch6_natm.mp4`, anti-flicker on) | flick.py, retime 6, g_natm track locally, spec bolts card → `tr('g_natm','bolts')`, render |
| ch7 (275.905) | anim queued `0ff0ac1c-0130-4ed3-88b0-9a1a37c8c868` (`ch7_finale.mp4`) | flick.py; build one old-time plate = hook plate media 16.5-24.6 s dissolving at 7.1 s into the finale, retime 7, render (no cards) |
| Music | DONE `audio/music_bed.wav` (9 generated text-to-music pieces), mix `audio/final_mix.wav` (-14.5 LUFS, music ~14 dB under voice, ducked) | none |
| Assembly | `assemble.py` (local ffmpeg from imageio_ffmpeg) | put the 7 final composites in `renders/final_parts/{hook,ch2..ch7}.mp4`, run, then sprite + flick + listen check |

Composite render params: `motion-graphic render` {project zip, media [plate key], audio `input/2026-11-13/75de18e9-...wav`,
audioStart = chapter global start, format mp4, quality standard, poster false, idempotencyKey}. Build a page: `python overlays/build_mg.py <ch>`.
Test before render: `motion-graphic snapshot` with `at` list, tier cpu; look at the stills.

## Open quality notes
- ch5 erector reads olive/simple geometry; ch7 passenger palms up (minor).
- Hook cards: hook dissolves to the creek at ~14.6 s old time; with the retimed plate check cards end before the creek appears.
- Every EngineX output still exists; local files under renders/ and audio/*.wav (large) are NOT in git except the voice and mix.
