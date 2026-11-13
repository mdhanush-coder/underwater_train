# XplainedUnseen — Cinematic studio standards (default for every video)

Target: a professionally directed animated documentary, not a set of AI-generated clips. Never trade visual quality or accuracy for speed or tokens; trade only research/execution overhead.

## Every scene must
- Explain visually (mechanism, scale, comparison), not just display.
- Have composition, lighting, real materials, intentional camera, depth, and a clear purpose.
- Keep physical consistency: scale, proportions, believable environment.
- Match the look of neighbouring scenes.

## Movie-level animation
Do: motivated camera moves with easing; transitions that carry continuity (push-through, match cut); real inertia on heavy parts; Graph Editor-curated ease in/out; particles/volumetrics only where they explain; designed typography; narration-synced beats; localized part separations instead of one big explode.
Avoid: default/linear keys; static object + spinning camera; PowerPoint-style fades; flat/low-detail models; grey untextured geometry; repeated camera move or repeated clip; inconsistent scale; effects that hide the subject.

## Explanatory staging (default arc for a system)
establishing shot -> reveal whole system -> push to key component -> separate/cut away -> animate internal process with labels -> reassemble -> transition. The viewer should be able to follow it with narration muted.

## Asset-first order
1 project assets (`XPLAINEDUNSEEN_*/assets`, `blender/*.blend`, `blender/scripts/library_assets.py`) -> 2 other libraries -> 3 adapt/combine -> 4 model manually -> 5 optimize.
Reuse a good Earth/human/vehicle/building instead of a primitive. Before animating any asset inspect: missing mesh/texture/material, wrong proportions/scale, loose edges, axis needles (lathe at r=0), inconsistent look.
Reuse the master `.blend` + `build_*.py` / `patch_*.py` pattern; version files (`name_v008.blend`).

## Pipeline (choose tools per scene; never force both apps)
Research > Script > Storyboard > Scene plan > Asset inspection > Asset create/modify > Blender modeling > Materials/textures > Rigging > Animation > Unreal cinematics (only if justified) > Lighting > Camera > Render > Composite > Edit > Sound > QA > Export.

## Blender vs Unreal
Blender: mechanisms, product/macro, exploded/cutaway, sims, procedural, anything EngineX can render today. Unreal: large real-time environments, Niagara-scale VFX, Sequencer/Movie Render Queue, only after a tested advantage. See `unreal-cinematics.md`.

## Scene QA (targeted: check critical visuals, not every unchanged part)
Meshes complete? Materials/textures applied (no grey)? Proportions right? Motion natural, camera intentional? Cinematic lighting? Smooth transitions? Explains the concept? No clipping/flicker/z-fight/missing assets/artifacts? Matches neighbouring scenes? A scene that rendered but looks unfinished is NOT done: improve before moving on. Inspect an actual frame or contact sheet, not just job status.

## Text rule (user-flagged twice)
No two texts in the same screen area at once; fade the outgoing text fully before the next; caption zone != label zone; run the clash check.
