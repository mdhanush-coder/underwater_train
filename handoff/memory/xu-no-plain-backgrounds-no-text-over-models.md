---
name: xu-no-plain-backgrounds-no-text-over-models
description: "Thorium film - no flat/plain dark backgrounds on cards or space plates, and overlay text must never sit on the 3D models; use motion graphics as well as Blender"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 29ecb82e-471d-450e-b0e8-b97186813c0b
  modified: 2026-11-11T13:36:10.133Z
---

User feedback (Thorium film, S7 review, 2026-11-11): "i dont want a plain background" and "texts are contradicting on the blender models".

**Why:** a flat charcoal card and black starfield plates looked empty, and labels placed on top of nuclei/halos were hard to read.

**How to apply:**
- RULE (user, S7 v2): card/chart/timeline/bar screens (motion-graphics only) get a dimmed blurred reactor-footage backdrop with a vignette; the 3D science scenes (nuclei on black space) stay plain black. Do NOT screen-blend a backdrop under the nucleus plates.
- Before rendering any overlay, snapshot frames and check every label against the nuclei/model anchors (use the Blender `anchors` mode); keep labels in empty zones, arrows end on the object edge, never text over a model.
- Mix motion-graphics pieces (intro cards, bars, step tracker, strike-throughs) with the 3D plates; do not rely on Blender alone. See [[onscreen-text-english-only]] and [[brahmos-no-text-boxes]].
- Backdrop video layers (blur) are very slow on the MG CPU tier (13+ min, never finished): render with `tier: "gpu"` (28 s). Upload media gets a generated basename, reference `assets/<that name>`.
