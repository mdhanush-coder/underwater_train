---
name: xu-motion-graphics
description: XplainedUnseen motion-graphics craft: on-screen text, stat cards, maps, counters, annotations, lower thirds, progressive diagrams, built and rendered with the EngineX motion-graphic engine. Use after xu-research-first whenever building or fixing an MG page or text overlay. Encodes safe areas, hierarchy, colour semantics, easing and the snapshot-check-render workflow.
argument-hint: "[the MG/overlay to build or fix]"
---

# XU motion graphics

Run **xu-research-first** first and keep its note with the asset. Then apply these rules (learned on EP002 cable map v001 -> v003).

## Design rules
- **Safe area:** keep all text inside the 90% title-safe zone (>= 96 px margin on 1920x1080, SMPTE EG 2046-3). Nothing in the bottom ~90 px (player UI); footer baseline <= y 1000.
- **Less text, clear hierarchy:** one card, not stacked boxes. Eyebrow (24 px tracked) -> hero number (about 130 px) -> descriptor (about 34 px) -> fine print (>= 24 px, the Design Polish floor). Delete the least important element before shrinking the important one. Annotations must never cover the data (the map/subject).
- **No heavy boxes:** use a soft radial/linear scrim (about 55% fading to 0) behind text, not opaque chips.
- **Colour has one meaning each across the whole film:** cyan (#5cc8ff / #8fdcff) = optical data and cables; amber (#ffc35c) = electrical power ONLY; white/neutral = labels; steel-blue for neutral highlights (e.g. a country). Never reuse a meaning-colour decoratively.
- **Motion:** entrances ease-out (cubic) about 0.5-0.6 s, staggered in reading order; exits shorter; vary rhythm within a scene; linear only for motion that never lands. Counters ease in-out and end on the true value ("600+" for "more than six hundred").
- **Truthful graphics:** schematic routes/diagrams are tagged on screen ("SCHEMATIC ROUTES · NOT TO SCALE"); sources in fine print; illustrative signals say "ILLUSTRATIVE". Keep true scale (a 40 mm duct stays 40 mm; use a leader-line callout).
- **Camera grammar for maps:** wide -> push to the subject -> pull back; lines draw on with a travelling head, markers at places; no particles (user rule).
- Maps: only `hf-assets/maps/` (Natural Earth, India's official view). Fonts: take them from the episode design contract (EngineX catalogue via `list_fonts`; Studio Grotesk is not in the catalogue and stays EP002-only; load any custom weight in `buildReady`). Colours: palette roles from the contract; the meaning colours below are the declared signal colours. Run `check_design` on the page before rendering (see `xplainedunseen-video-production/references/design-system.md`).

## EngineX workflow (verified)
1. Write `index.html` (canvas drawn from `hf-seek`/GSAP paused timeline; root has `data-composition-id`, size, duration, fps). Never use rAF/timers/Date.now.
2. Zip as `index.html` at the zip top; upload (`create_upload_url`, `curl -T`); `libraries: ["d3"]` for maps.
3. **Snapshot first**: `motion-graphic/snapshot` with `at:[...]`, `tier:"cpu"` (about 8 s), download stills (`sign_output` + `curl`), view a contact sheet (ffmpeg xstack) before any render.
4. `motion-graphic/check` for overflow/contrast if needed, then `render` (`tier:"cpu"`, `quality:"high"`, `poster:false`, about 70 s for 12 s of 1080p). Drawing on the CPU tier avoids the GPU queue.
5. Verify the real MP4 (ffmpeg -i for size/fps/frames; extract 2-4 frames) and compare against the research note.
6. Version outputs (`_v002`, `_v003`); never overwrite another session's file.
7. Windows ffmpeg filter paths: do not put `C:` paths inside filter options; `cd` and use relative output names.

## Checklist before saying done
Text inside safe area · hero subject visible · colours match meanings · fine print readable (>= 24 px) · `check_design` and `motion-check` run with no `must` left · sources and "schematic/illustrative" tags present · render specs match the edit (fps, frames, size) · NOTES.md updated with research + changes.
