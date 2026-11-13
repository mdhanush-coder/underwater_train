---
name: xu-sound-original-only
description: "User 2026-11-09 (Gaganyaan): no possibly-copyrighted music/sfx; EngineX library tracks have no licence info, so use generated music + self-synthesised sfx"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8570bfe4-1787-415c-be0b-986f04b085c7
  modified: 2026-11-09T16:33:34.778Z
---

User asked to check whether the song/sfx were copyrighted and replace them if so. The EngineX sound library shows no licence field, and its "trailer-scores" pack has commercial-sounding titles (Eternal Flame, Aurora Borealis, Mindcrimes), so its tracks could not be cleared.

**Why:** YouTube Content ID / copyright risk on the channel.
**How to apply:** for XU videos, music = EngineX `text-to-music` workflow (run_workflow, values caption/lyrics "[Instrumental]"/max_duration; takes come out ~20-110 s regardless, so generate several per mood and chain with 3 s acrossfades); sfx/ambience = synthesise in numpy (see projects/gaganyaan/build/synth_sfx.py, premix.py → 3 stems fed to video/sound-design). Tell the user generated music has the model's own terms and Content ID false flags are possible. Related: [[onscreen-text-english-only]].

Also from the same night: the user removed the "5 WAYS TO DIE" list component entirely and the parachute 1-10 count; prefer clean footage over list/count gimmicks, and text styled via the EngineX colour-palette + typography skills (Montserrat display + Kalam pen notes, charcoal-gold; projects/gaganyaan/DESIGN_SYSTEM.md).
