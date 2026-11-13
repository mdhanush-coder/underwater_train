---
name: chips-varied-visuals-no-horizon-band
description: "Chips film feedback 2026-11-12 - don't repeat the same Blender plates, mix in drawn MG scenes; no table-horizon band at the top of dark-set plates; keep MG label boxes clear of text"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6efaeb8f-61b4-4e53-8433-f8dfba579c79
  modified: 2026-11-12T10:50:19.212Z
---

User said the Blender plates repeated across the film and "everything is repeated"; wants different visuals so the audience is not bored. Also asked why a black band sat at the top of the missile shots, and flagged an MG ladder whose highlight box overlapped its own labels.

**Why:** the film reused cineA/cineB/wafer/missile plates back to back; the dark table's lit pool / reflected sky showed up as a horizon line.

**How to apply:**
- Alternate Blender plates with drawn MG scenes (overlays/mg_scenes.py: signal, kargil, simple, export, donut, ladder, timeline3, wafers, two_chips, cards, ring4), never the same plate twice in a row inside a section.
- Dark-set plates: light-link the key/fill/rim lights to the model only, and match world camera colour + reflected HDRI to the black table (missile shots use hdri 0.008, bg_col ~0.0008) so no horizon band shows.
- In MG scenes keep highlight boxes clear of row labels and sub-labels inside the box; fill shapes so rails do not run through them.
- Related: [[chips-overlay-rules-v4]], [[chips-smooth-transitions]]
