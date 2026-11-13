---
name: xu-hindi-voice-sameer-b
description: "User chose Sameer, style B (relaxed friend) as the Hindi narration voice; one sentence per line, lively, no slow/heavy directions"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c3564718-d8bf-4e03-9c5a-db328ce36e46
  modified: 2026-11-11T10:03:51.528Z
---

For XU Hindi narration use `sameer` (chosen 2026-11-10, after comparing Arnav A/B and Sameer A/B).

Recipe (updated 2026-11-11, Thorium v3): ONE brief, the same at the start of every paragraph, and no other feeling directions: `[a friendly explainer, steady energy, one even tone and pitch throughout]`. User wants the same tone and a straight, unlifted pitch for the whole video. No "?" questions (they lift pitch): rewrite them as statements ("अब देखते हैं, कि..."). **One sentence per line** (no joined/continued lines). `[pause]` lines are fine. Never slowing words ("heavy", "slow", "quietly", "relaxed"). `lineGapMs` 250, `continuity` true, no `temperature`/`emotion`. English words in Latin script: [[hinglish-english-words-latin]].

Edit method that worked (Thorium v4): never regenerate approved audio. Voice only the NEW or FIXED lines as extra paragraphs with the same recipe, then splice into the approved WAV at line boundaries with python `wave` (cut at the next line's start, add 250 ms, or 650 ms between paragraphs), and re-transcribe the result to check every join. TTS can silently drop a short word ("आम" before "uranium"): transcribe every take, do not trust the engine's own check (it flags English words falsely).

**Why:** Arnav with no brief sounded robotic. On Thorium v1, an `[honest, a little heavy]` direction made Sameer slow and low-energy (user flagged 3:34), and the user wants sentence-by-sentence lines so it sounds clear and keeps the same voice.
**How to apply:** every Hindi XU narration script unless the user changes it. Related: [[gaganyaan-voice-approved]].
