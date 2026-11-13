---
name: enginex-media-gotchas
description: "EngineX quirks hit while building the chips Short: media names in MG pages, sound: ids unreachable, project-zip trick"
metadata:
  type: reference
---

- Motion Graphic `media` files are at `assets/<uuid>.<ext>` (the storage key's basename), NOT the upload filename; a wrong name makes snapshot/render fail with a bare "exited 2".
- To avoid resending a big page: zip it as index.html, upload with create_upload_url, pass as `project` (media still given via `media`).
- 2026-11-13: `sound:<id>` was "cannot be fetched" in video/sound-design; the signed `listen` URL from find_sound worked for music and cues.
- Reframe outputs are all named reframed.mp4: re-upload each under a fresh key before using several in one page.
- Chips Short built at projects/chips/short/ (build_short.py + short_template2.html, final/ has mp4, srt, thumbnails, publish.md).
**Why:** saves a failed-run loop (see [[enginex-no-failed-runs]]). **How to apply:** any EngineX page/sound-design job.
