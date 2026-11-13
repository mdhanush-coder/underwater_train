---
name: enginex-render-timeline-assembly
description: Whole-film assembly on EngineX in ~3 calls with smart-video/render-timeline (OTIO) + one vfx screen blend; basename-matching gotcha
metadata:
  node_type: memory
  type: reference
  originSessionId: c3564718-d8bf-4e03-9c5a-db328ce36e46
  modified: 2026-11-10T16:03:17.970Z
---

smart-video/render-timeline takes an OTIO json timeline (cuts, gaps, SMPTE_Dissolve transitions with in/out offsets using clip handles) and renders the whole film in one job, frame-exact (verified on MATSYA-6000 v3, 8427 frames).
- It matches media by BASENAME: EngineX outputs are all `motion.mp4` / `render.mp4`, so they collapse to one file. Fix: give each distinct file an alias target_url that matches nothing (`zg00q.mp4`...) and pass `media` in first-use order; unmatched names pair with leftovers in order.
- It does not draw blend modes. For plates + text-on-black overlays: render a plates-only pass (gaps elsewhere) and a graphics pass (MG shots + overlays), then video/vfx `blend: screen` of plates over graphics (one CPU job, ~4.5 min for 6 min of 1080p). A plate<->graphic dissolve then reads as a cross-dissolve.
- The trailing gap of a track is dropped from the output length (use the full-length pass as the vfx input).
- Verify by comparing slot midpoints with local sources (qc_plates.py / qc_graphics.py in projects/matsya6000).
Related: [[enginex-blender-capabilities]]
