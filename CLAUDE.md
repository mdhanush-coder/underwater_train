# Rules for Claude Code on this repo (bullet-train undersea tunnel video)

Read `HANDOFF.md` first (state, EngineX output keys, next steps). Then copy `handoff/memory/*.md` into your Claude
memory folder (`~/.claude/projects/<this-folder>/memory/`) so the user's rules persist.

- For any Blender/3D/animation task, load and follow `.claude/skills/blender-animation/SKILL.md`.
- For the whole explainer pipeline, follow `.claude/skills/tech-explainer-video/SKILL.md`.
- Also use the skills `xu-research-first`, `xu-cinematic-3d`, `xu-motion-graphics` and `xplainedunseen-video-production`
  (in `.claude/skills/`) and the EngineX skills (`get_skill`: enginex-blender, motion-director, typography, design-polish).
- All rendering runs on EngineX (editor-api MCP). The laptop needs the same EngineX MCP server connected.

## User rules (all binding)
- Do NOT rebuild chapters that are already done (see HANDOFF.md). Fix only what the user asks.
- No failed EngineX runs: bundle, `ast.parse`, re-read for Blender 5.2 API mistakes BEFORE submitting. Failures and
  cancels in a row pause the engine. `idempotencyKey` on every job; long jobs `waitMs: 0`, then a background `sleep`
  and `get_job` (waitMs >= 60000 times the client out). Don't waste tokens or runs.
- Verify real rendered frames (montage / sprite -> sign_output -> download -> look) before claiming anything is fixed.
- Max 3D, realistic geometry and colours (steel, concrete, wet soil, blue water). Use library assets; Unreal for
  environments; rigged characters. Machines (JCB, train) must be clearly visible; train must never vanish into black.
- No hard cuts: smooth ~1 s dissolves, continuous cameras. Visuals follow the narration line by line (new view per idea).
- On-screen text: English only, compact motion-graphics in the chips/BrahMos style (outlined kicker tag, gold highlight
  box, gold underline, italic statements, boxed numbers, gold-outlined cards with leaders). Charcoal-gold for overlays
  only, ONE gold item per frame. No icons. Text never covers the 3D model.
- Credits only in the YouTube description. Original/generated sound only (no library music).
- 3D from an image: 3d-shapeForge only. Blender runs capped ~125/day.
- Take references from the internet. Short reports, no long essays.

## Added 2026-11-13 (evening)
- Read `projects/bullet_tunnel/SESSION_HANDOFF.md`. Do the animation yourself; do NOT delegate to agents (user rule).
- Voice: aarav chips recipe (v4). Callout leaders must follow dense tracks (check_cards.py all TRACK OK).
- Every 3D plate must pass `diag/flick.py` (0 % flicker) — use `stable_eevee(sc)`.
- Plates follow the voice via `retime.py`; uploaded inputs are referenced by their uuid file name in specs.
