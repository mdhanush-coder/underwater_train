---
name: xu-research-first
description: Mandatory first step for XplainedUnseen before ANY animation, motion graphic, visual effect, camera move, on-screen text overlay or cinematic sequence. Researches the subject and the best creators' techniques, picks the production method, writes a research note, then hands off to xu-motion-graphics or xu-cinematic-3d. Use whenever the user asks to make, change, restyle or fix a visual.
argument-hint: "[the visual/animation about to be made]"
---

# XU research first

**Rule (user, 2026-10-31):** never start production from assumptions or generic technique. Research, analyse the best, choose the method, then build, then verify against the research.

## Procedure (do all six, in order)
1. **Subject:** research the science / mechanism / history the visual explains. Record verified facts and what is simplified or illustrative. Accuracy beats spectacle (e.g. optical signal = light in glass; repeater amplifies light, electricity only powers it).
2. **Best examples:** find the most influential videos/creators/studios in that niche (science communicators, documentary makers, VFX artists, educational animation studios) with WebSearch. Run 3-4 queries in parallel; use `mode: "extended"` for niche or hard-to-find facts, `standard` for simple lookups.
3. **Analyse technique:** for each example, note storytelling and composition, camera/framing/transitions, lighting/materials/rendering, modelling/procedural/MG method, timing/pacing/hierarchy/sound, how complex ideas are explained.
4. **Reverse-engineer:** prefer tutorials, breakdowns, production notes, tool docs (offline Blender 5.2 manual, EngineX `describe_operation`) over screenshots. Understand why it works; do not copy the look or a distinctive scene. Check licences before using any data or media (e.g. TeleGeography route data is paid; use schematic routes and label them).
5. **Choose the method per scene** from the real catalogue (`find_operation`, `list_operations`, `describe_operation`): Blender, Unreal, motion-graphic, existing assets, procedural. Never force one tool on every scene.
6. **Plan, build, verify:** write the plan, apply it, then check the output against the research and the intended explanation.

## Output: a research note (required before building)
Put it in the asset's own `NOTES.md` (or `production/research/<asset>.md`):
```
## Research (date)
Subject facts: ...            (sources)
Best practitioners + technique: ... (named, with URLs)
What I could NOT find: ...    (say so; never invent a studio's internals)
Method chosen and why: ...
How it maps to this shot: ...
Verification plan: ...
```
Honesty: if searches return thin results, state the gap and ask or search deeper; do not claim to have analysed something you did not read.

## Then
- On-screen text, charts, maps, counters, lower thirds -> `xu-motion-graphics`.
- Blender/Unreal camera journeys, cutaways, 3D labels -> `xu-cinematic-3d`.
- Overall episode orchestration stays in `xplainedunseen-video-production`.
