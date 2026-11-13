# XplainedUnseen — Production workflow reference

Story determines tools. Verify every operation name with `find_operation` / `describe_operation` before use; this list comes from the supplied catalogue and may drift.

## Pipeline
1. Research → `research/source-notes.md`
2. Story spine + narration → `production/script.md`
3. Chapters/scenes → `production/shot-list.*`
4. Narration-to-visual map → `production/narration-visual-map.md`
4a. Design contract (palette via `list_palettes`, fonts via `list_fonts`, motion idea) → `production/design-contract.md` — see `design-system.md`
5. Per-scene medium + tool choice (table below); motion plan → `production/motion-plan.md`
6. Preview each scene type once; inspect; approve look; MG pages and Blender shots go through `check_design` / `motion-check` (Gate DR)
7. Generate narration (`emotive-speech`/`speech`) → `transcribe/words` for timings
8. Build scenes, labels, captions from real word timestamps
9. Sound design + music, duck under voice
10. Assemble (`video/*`, `smart-video/render-timeline`), probe, QC, export, package

## Medium → tool
- Mechanics/materials/physics/camera: `blender/*` (script, inspect, preview, render, uv, bake, simulate, composite, turntable, product-shot)
- Big environments: Unreal, only if tested better than Blender
- Diagrams/data/timelines/labels: `motion-graphic` (+`snapshot`, `check`); GSAP preferred
- Edit/finish: `video/probe|frames|concat|transition|compose|duck|volume|fade`, `smart-video/retime|enhance|render-timeline`
- Voice: `emotive-speech`, `speech`
- Sync: `transcribe/words|subtitle|align|separate`, `voice-activity/segments`
- Generative: `list_workflows` → `run_workflow` (inspect inputs first)
- Utility: `scenes`, `rotoscope`, `image-cutout`, `depth-motion`

## Job hygiene
- `fleet_status` once before heavy runs; two Blender GPU pods max.
- Status vocabulary: planned / running / completed / failed / verified.
- Don't poll; check `get_job` when needed. Preview before final.
- Log state in `production/claude_handoff.md` (state, milestones, active jobs, errors, next actions).

## Per-scene checklist
Mapped narration · medium justified · schema inspected · preview inspected · captions placed in negative space · audio layers planned · continuity with neighbours.
