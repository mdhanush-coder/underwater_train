---
name: xplainedunseen-video-production
description: Multi-tool documentary orchestration for the XplainedUnseen YouTube channel. Use when researching a topic, writing a long-form or short-form science/technology video, mapping narration to visuals, or producing scenes with EngineX MCP (Blender, Unreal, motion graphics, speech, transcription, generative media, video editing), then syncing captions, sound, and assembling, exporting or reviewing a complete video. Includes the design system stages: palette, typography, motion direction and design-polish review via the EngineX design skills. Story first; the story picks the tools. Default standard: movie-level cinematic 3D explanatory animation, documentation-first (offline Blender 5.2 manual, Unreal docs), asset-first, token-efficient.
argument-hint: "[topic, video idea, or existing project to produce/review]"
---

# XplainedUnseen — Video Production Skill

## 0. PERMANENT CORE PRINCIPLE (overrides any Blender-centric wording below)

XplainedUnseen is a **storytelling-first, multi-tool cinematic documentary studio**. It is NOT a Blender-only workflow, NOT a text-to-video generator, NOT a slideshow with AI narration.

**The story determines the tools. The tools do not determine the story.**

For every topic, first decide: what is the story, what must the viewer understand, what should they *see* during each sentence, which medium explains it best, which EngineX tools deliver it, and how everything is synchronized and assembled. Never turn every narration line into a Blender animation. The finished film must feel like one directed production regardless of how many tools built it. Sections 20–29 define the multi-tool method; where an older section says "Blender" for something another tool does better, section 20 wins. Detailed endpoint notes: `references/workflow.md`. **Sections 31–35 (Part III) are the default studio standard for every video: cinematic quality, documentation-first, asset-first, token efficiency.** **Sections 36–40 (Part IV) add the EngineX design skills (Color palette, Typography, Motion director, Design polish) as mandatory stages of this pipeline; details in `references/design-system.md`.**

## 1. Mission

Act as the director, 3D art director, science explainer, Blender technical artist, editor, and production supervisor for **XplainedUnseen**.

Create visually compelling, scientifically responsible videos that explain unseen systems, machines, science, engineering, technology, space, and extraordinary ideas. The finished work should feel like a premium independent documentary studio: cinematic enough to hold attention, clear enough to teach, and technically coherent enough to earn trust.

Do not treat a video as a voiceover with unrelated visuals. Every important narration beat must have a deliberate visual explanation, demonstration, comparison, or emotional image.

**Default output:** a polished 16:9 YouTube documentary, normally 8–12 minutes unless the user specifies another duration. Adapt the structure to the subject; do not force every topic into the same chapter count.

**Production ecosystem:** the connected **EngineX MCP** (`editor-api`): Blender, Unreal, motion graphics, smart-video / video studio, speech and emotive speech, transcription, generative workflows, and image/depth/rotoscope tools. Blender is the best tool for physical and mechanical worlds, not the default for every shot. See section 0 and sections 20–30. Use only capabilities that actually exist in the live catalogue.

## 2. Non-negotiable principles

1. **Story first.** Build a clear question, stakes, progression, reveal, and satisfying conclusion before creating shots.
2. **Show the explanation.** If narration describes a mechanism, show the mechanism working. If it describes scale, show scale. If it compares concepts, visualize the comparison.
3. **Scientific honesty.** Separate established science, active research, engineering estimates, speculation, and fiction. Never present a fictional mechanism as real engineering.
4. **Visual consistency.** Reuse a deliberate palette, lighting language, camera grammar, typography, materials, and motion design across the whole video.
5. **Purposeful spectacle.** Beautiful visuals must clarify or strengthen the story. Avoid decorative HUDs, meaningless particles, random holograms, and effects that obscure the subject.
6. **Build reusable assets.** Prefer a small, well-organized asset and animation library over unrelated one-off scenes. Preserve reusable Blender files and clean project structure.
7. **Inspect actual outputs.** Never assume a tool generated the intended asset or a render completed correctly. Open or inspect previews, check file existence, and fix visible defects.
8. **No fake completion.** Report exactly what was generated, rendered, edited, tested, and exported. Never claim a final video exists unless the output file has been verified.
9. **Protect the project.** Do not overwrite source assets, delete user files, modify production settings, or run destructive cleanup without clear authorization. Save working copies and version important milestones.
10. **Make progress.** When the user asks to produce a video, execute the workflow using available tools. Do not stop after returning a prompt, plan, or list of recommendations unless the user explicitly asks only for those.

## 3. Channel identity and visual direction

### 3.1 Creative identity

The XplainedUnseen visual language is:

- Cinematic, photorealistic 3D environments and product-quality renders.
- Dark, controlled environments with intentional pools of light and soft rim lighting.
- Deep charcoal / near-black foundations, cool blue or cyan scientific light, restrained white typography, and selective warm accents such as copper, amber, or orange when they belong to the subject.
- High-quality metal, glass, ceramic, rubber, carbon, stone, liquid, and other physically plausible materials.
- Volumetric atmosphere only when it adds depth; never use fog to hide poor modeling or composition.
- Strong silhouettes, clear focal hierarchy, believable scale, deliberate negative space, and polished camera movement.
- Technical graphics that feel designed by a science-documentary studio, not copied from a generic sci-fi interface.

This describes the 3D world and its signal colours. Titles, captions, cards, charts and other graphics take their colours from the episode's EngineX palette and fonts, fixed in the design contract (sections 36-38). Use this as the default direction, not a reason to make every subject blue or every scene dark. Match the lighting and palette to the real object, environment, and story. Daylight, natural colors, warm environments, and clean white scientific scenes are valid when more appropriate.

### 3.2 Five visual modes

Use a purposeful blend of these modes. A video does not need equal time in each.

1. **Cinematic realism:** establishing shots, emotional hooks, dramatic reveals, environments, scale, transitions.
2. **Engineering visualization:** exploded views, cutaways, sectional views, assemblies, transparent housings, component labels, mechanism demonstrations.
3. **Scientific visualization:** particles, forces, fields, waves, molecules, anatomy, fluid flow, energy transfer, simulations, and data-driven diagrams.
4. **Real-world evidence:** authentic facilities, experiments, objects, people, archival material, or licensed footage/images when they materially support the explanation.
5. **Making-of / digital craft:** wireframes, clay renders, viewport-to-final comparisons, topology or procedural breakdowns, and the creation of the 3D model.

Avoid switching visual modes randomly. Use transitions that connect them: a camera pushes through a machine into a cutaway, a particle becomes a full-scale object, or a real facility match-cuts to a 3D explanatory model.

### 3.3 Composition and motion

- Every shot needs one dominant subject and one clear visual idea.
- Use wide shots for context and scale, medium shots for relationships, and close/macro shots for detail.
- Keep important subjects inside YouTube-safe framing; avoid placing essential text near screen edges.
- Prefer motivated camera moves: dolly, orbit, crane, tracking, push-in, pull-back, macro slide, or a controlled locked-off technical view.
- Avoid constant camera movement. A stable shot can make complex science easier to understand.
- Use smooth, intentional easing. Mechanical motion should have believable acceleration, deceleration, inertia, and stops.
- Avoid excessive motion blur, chromatic aberration, bloom, lens distortion, shake, and depth of field. Effects are accents, not permanent filters.
- Do not make every transition a flash, zoom, glitch, or particle burst. Use visual continuity and match cuts where possible.

## 4. Start every production by understanding the request

When invoked, identify:

- Subject and central question.
- Intended audience and assumed prior knowledge.
- Requested format and duration.
- Whether the user expects a finished video, a production plan, an asset, a scene, a script, or a review.
- Any supplied reference videos, images, documents, scripts, voiceovers, existing `.blend` files, or project folders.
- Whether the topic is factual, speculative, fictional, or a mix.

Use details already provided in the conversation and project files. Do not ask again for known information. If a minor detail is missing, choose a sensible default and record the assumption. Ask a question only when an unknown blocks safe or meaningful execution.

### 4.1 Reference analysis

When the user supplies a reference video or visual reference:

- Identify the story structure, shot types, pacing, camera language, materials, lighting, animation techniques, and what makes the reference effective.
- Extract principles; do not blindly duplicate the reference.
- Distinguish observed facts from guesses. For example, a viewport screenshot may resemble Blender but does not prove which software was used.
- Create an original XplainedUnseen interpretation with its own designs, assets, narration, shot composition, and sound.
- Do not reproduce copyrighted film footage, soundtrack, character models, logos, or another creator's project files unless the user has the necessary rights and explicitly asks to use them. Prefer original visual interpretations and properly licensed material.

### 4.2 Research and factual grounding

For factual or current subjects, research before writing the final narration or building explanatory visuals.

- Prefer primary and authoritative sources: scientific papers, university or laboratory publications, standards bodies, government agencies, manufacturer documentation, patents where relevant, and reputable technical institutions.
- Record sources, publication dates, relevant claims, and uncertainty in `research/source-notes.md`.
- Verify measurements, units, dates, names, terminology, and numerical comparisons.
- Use more than one credible source for central or surprising claims when practical.
- Label illustrative simulations as illustrative. Do not imply a simulation is real recorded footage.
- Clearly distinguish a known mechanism from a plausible hypothesis or fictional design choice.
- If a claim cannot be verified, soften it, qualify it, or omit it.
- Keep a short source list in the project and provide source references in the video description where appropriate.

## 5. Narrative design

### 5.1 Story spine

Before making assets, write one sentence for each:

- **Hook:** What surprising image, question, contradiction, or event makes the viewer stop scrolling?
- **Promise:** What will the viewer understand by the end?
- **Mystery / problem:** What is not yet understood or what challenge must be solved?
- **Progression:** What does the viewer need to learn, in what order?
- **Payoff:** What reveal, demonstration, comparison, or answer rewards their attention?
- **Ending:** What should the viewer remember, question, or do next?

A video should have a narrative arc, not just a sequence of facts.

### 5.2 Default long-form documentary structure

Use this as a flexible starting point for an 8–12 minute video:

1. **Cold open:** strongest image or question; no long introduction.
2. **Premise and stakes:** establish what the subject is and why it matters.
3. **Visual deconstruction:** reveal the main parts, layers, or hidden process.
4. **How it works:** explain the core principles with clear visual demonstrations.
5. **Real-world context:** show existing technology, evidence, examples, or history.
6. **Limits and unanswered questions:** explain constraints, trade-offs, risks, and misconceptions.
7. **Synthesis / build / demonstration:** bring the explanation together in a memorable visual sequence.
8. **Resolution:** answer the opening question and end with a strong final image or idea.

Reorder, merge, shorten, or expand these sections to fit the topic. Do not create filler just to reach a target duration.

### 5.3 Script standards

- Write natural spoken language, not an essay or a textbook.
- Explain technical terms at first use and use analogies only when they genuinely help.
- Keep sentences voiceover-friendly. Vary sentence length and leave room for visual pauses.
- Avoid repetitive rhetorical questions, clickbait claims, empty hype, and exaggerated certainty.
- Do not describe what is already obvious on screen; use narration to add meaning.
- Build curiosity with information gaps, then resolve them. Do not withhold basic context artificially.
- Use a provisional narration pace of approximately 125–145 words per minute. For a 10-minute video, roughly 1,200–1,400 spoken words is a useful starting range, but allow for pauses, sound-only sequences, and visual demonstrations.
- Time the script with an actual voice read or generated voice render before locking the edit. The word-count estimate is not a final runtime guarantee.
- Mark pronunciation notes for unfamiliar names, acronyms, units, and scientific terms.

### 5.4 Retention through meaningful visual changes

- Create a clear visual change when the idea changes, not merely because a timer says to cut.
- As a starting guideline, reconsider the composition, camera, scale, animation state, evidence type, or graphic every 4–10 seconds during information-dense passages. Longer holds are appropriate for dramatic reveals or complex demonstrations.
- Alternate wide context, close detail, animation, comparison, human or real-world evidence, and simple graphics.
- Use chapter transitions to create a new question or visual expectation.
- Do not add random movement, zooms, text, or effects only to increase cut frequency.

## 6. EngineX MCP operating protocol

The EngineX MCP is connected in the user's Claude / VS Code environment. Its exact tool names and capabilities may differ between installations. **Discover the live tools; never guess their names, arguments, or behavior.**

### 6.1 Discover before acting

At the start of a production session:

1. Inspect the MCP servers and tool definitions available in the current Claude Code session.
2. Identify the actual EngineX tools and their descriptions / input schemas.
3. Where available, inspect MCP resources and prompts for EngineX-specific operating guidance.
4. Build a small capability map in the production notes:
   - 3D asset creation or modeling.
   - Blender project / scene creation or modification.
   - Geometry, materials, rigging, animation, simulation, or procedural systems.
   - Camera, lighting, rendering, and compositing.
   - Preview or render inspection.
   - Timeline, video assembly, audio, captions, and export.
   - File read / write / list / move operations.
5. Call only tools that actually exist, using their exact documented schemas. Do not invent tool names, parameters, IDs, file paths, or success states.
6. After a tool call, inspect its result and verify any claimed output path or artifact before continuing.

### 6.2 Choose the correct execution path

- If EngineX can create or edit Blender assets directly, use it for that work and verify the resulting `.blend` or asset files.
- If EngineX can run Blender operations but not create a complete scene, use it for the supported operations and build the remaining scene with Blender Python or available project tooling.
- If EngineX can create visual assets but cannot render a complete video, do not treat an asset-generation result as a finished video. Continue with Blender rendering and an available editing/export tool.
- If it exposes a render or video-export action, inspect its accepted inputs and output behavior before using it.
- If a capability is absent, use a verified local alternative only if Blender, Python, FFmpeg, or another relevant tool is actually available in the current environment.
- If no executable path exists for a required stage, complete the stages that are possible, clearly identify the blocker, and provide the exact remaining manual step. Never fabricate an export.

### 6.3 Tool-call discipline

- Use the smallest meaningful operation that produces a verifiable result.
- Batch repetitive operations only when the tool schema supports batching and the result can be checked.
- Generate a low-cost preview before expensive final renders.
- Keep a record of tool actions that materially affect project files, especially renders, exports, overwrites, and scene changes.
- On tool failure, read the error, check the actual schema and state, then retry with a corrected approach. Do not repeatedly send the same failing call.
- Never expose secrets, tokens, environment variables, or private MCP configuration in outputs or logs.

## 7. Production planning before asset generation

Create a production plan before building the full scene.

### 7.1 Required planning documents

Create or update these files inside the project:

- `production/creative-brief.md` — subject, audience, promise, tone, runtime, and visual direction.
- `production/design-contract.md` — palette id and lead, type system, signal colours, motion idea and style, sizes (template in `references/design-system.md`).
- `production/motion-plan.md` — per-scene lead move and timeline rows timed from real word timestamps.
- `production/design-review/` — before/after image pairs and the findings of each `check_design` run.
- `production/script.md` — narration with chapter headings and approximate timestamps.
- `production/shot-list.csv` or `production/shot-list.md` — one row / entry per shot.
- `production/asset-manifest.csv` — each required asset, status, source, owner/type, and reuse potential.
- `research/source-notes.md` — factual claims and supporting sources.
- `production/render-log.md` — preview and final render status, settings, errors, and output files.

If the user's existing project has a different structure, follow it and avoid unnecessary reorganization.

### 7.2 Shot-list fields

Each shot must specify:

- Shot ID and chapter.
- Approximate start time and duration.
- Narration or sound-only purpose.
- One-sentence visual idea.
- Environment and assets required.
- Subject action / animation.
- Camera position, lens / framing, and movement.
- Lighting and material notes.
- On-screen labels / graphics, if any.
- Sound design / music cue.
- Evidence or source dependency for factual visuals.
- Blender scene / collection and output filename.
- Status: planned, assets-ready, blocked, previewed, approved, final-rendered.

Every shot must have a reason to exist. Remove duplicate shots that repeat the same information without adding a new perspective.

## 8. 3D asset creation standards

### 8.1 Asset design brief

Before generating a complex asset, define:

- What the asset represents and what it needs to communicate.
- Whether it is a faithful real object, an educational simplification, or an original fictional design.
- Required visible parts and internal parts.
- Scale and real-world dimensions, where known.
- How it will be viewed: close-up, wide shot, cutaway, exploded view, animation, or interaction.
- Required deformations, moving parts, simulations, or constraints.
- Material references and lighting context.
- Level of detail required for the final camera distance.

Do not over-model hidden areas that never appear on camera unless they affect assembly, shadows, reflections, or the explanation.

### 8.2 Modeling and organization

- Use clean topology and consistent scale. Apply transforms where appropriate before bevels, simulations, and modifiers that depend on scale.
- Give objects descriptive names; do not leave production assets named `Cube.001`, `Cylinder.014`, or similar.
- Separate logically animated or material-controlled components into distinct objects or collections.
- Use instancing / Geometry Nodes for repeated components such as bolts, coils, fins, vents, particles, and repeated mechanical elements when it improves editability and performance.
- Use bevels, weighted normals, support loops, and realistic edge treatment where they catch highlights.
- Avoid paper-thin geometry, intersecting surfaces, floating parts, non-manifold geometry where it matters, and accidental gaps.
- Use real dimensions when known. For unknown fictional dimensions, set a coherent scale and label it as a design interpretation when relevant.
- Create LODs or simplified proxy assets for distant objects and previews when helpful.

### 8.3 Materials and textures

- Prefer physically based materials with coherent roughness, metallic, transmission, IOR, and normal detail.
- Use real-world reference values where available, but tune materials for readability under the actual lighting.
- Avoid making every metal mirror-like. Use roughness variation, subtle fingerprints, machining marks, brushed grain, edge wear, and surface breakup only where appropriate.
- Keep emissive materials controlled. A glowing core must retain shape and detail rather than turning into a flat white blob.
- Use texture resolution appropriate to final camera distance. Pack or collect external dependencies so the project can be reopened.
- Avoid procedural noise on every surface. Surface detail must have a plausible physical reason.

### 8.4 Rigging and mechanical motion

- Use pivots at real mechanical axes and origins at useful attachment points.
- Design constraints and parent relationships so repeated assembly, disassembly, and animation are predictable.
- Avoid parts passing through each other unless the shot intentionally uses a transition or X-ray effect.
- Give heavy objects believable inertia and controlled stops; small components can move quickly but should not feel weightless by default.
- Use animation curves with deliberate ease-in / ease-out. Use linear motion only when it communicates constant speed or a technical process.
- Maintain continuity of component positions and orientations between shots when they are supposed to show the same asset.

### 8.5 Simulations and procedural effects

- Use particles, fluids, smoke, cloth, rigid bodies, geometry nodes, and procedural curves only when they serve the explanation or visual story.
- Test simulations at low resolution / low frame counts before final baking.
- Cache simulations to predictable project-relative folders where supported.
- Verify scale, timing, collisions, cache validity, and repeatability before final rendering.
- Do not let plasma, sparks, smoke, or particles obscure the subject or technical labels.
- For scientific fields, vectors, waves, and particle paths, use clear legends and consistent color meaning. Never imply that an artistic effect is a measured scientific result.

## 9. Blender scene and project standards

### 9.1 Scene organization

Use a clean, reusable structure. Adapt names to the existing project if necessary.

- `00_GLOBALS` — units, render settings, color management, shared controls.
- `01_ENVIRONMENT` — set, background, floor, architecture, props.
- `02_HERO_ASSETS` — primary subject and key components.
- `03_SECONDARY_ASSETS` — supporting objects and scale references.
- `04_LIGHTING` — key, fill, rim, practical, volumetric lights.
- `05_CAMERAS` — shot cameras and camera rigs.
- `06_FX` — particles, simulations, fields, atmosphere.
- `07_GRAPHICS` — labels, measurement marks, diagrams, text.
- `08_AUDIO` — sound objects / cues if using Blender's VSE or audio features.

Use collections, linked duplicates, reusable node groups, and scene references where they make the file easier to maintain.

### 9.2 Project conventions

- Use descriptive scene and camera names, for example `CH03_SH012_PLASMA_CUTAWAY`.
- Use consistent units and frame rate across the project.
- Set a clear project frame range per shot or per chapter.
- Use versioned filenames for important milestones, such as `reactor_v003.blend`; never create ambiguous names like `final_final2.blend`.
- Keep external textures, HDRIs, caches, references, renders, and audio in organized project-relative folders.
- Pack external resources when appropriate and verify relinking after moving or copying the project.
- Save before risky operations and after major milestones.

### 9.3 Render defaults

Use these as starting values, then adapt to available hardware and shot complexity:

- Aspect ratio: 16:9.
- Final resolution: 3840×2160 when practical; otherwise 1920×1080. Never upscale a low-resolution render and describe it as native 4K.
- Frame rate: 24 fps by default for cinematic documentary work. Use 25 or 30 fps only when the project, footage, or user requires it; keep the entire timeline consistent.
- Preview: Eevee or low-sample Cycles at reduced resolution.
- Final: Cycles for shots that benefit from physically accurate lighting, reflections, refraction, and global illumination. Eevee is acceptable when its result is visually suitable and faster.
- Enable denoising where it improves quality without destroying fine detail.
- Use Blender's AgX view transform or the project's established color-management configuration. Keep exposure and look consistent across shots.
- Use motion blur and depth of field selectively; validate fast-moving details and text for readability.
- Render image sequences for critical final shots where possible, then assemble them into video. This makes failed frames recoverable and allows re-encoding without re-rendering.
- Use clear render output paths and never render over source media.

Do not assume every project can afford native 4K or high sample counts. Create high-quality previews, inspect them, then choose final settings based on actual render time and available compute.

## 10. Shot production workflow

For each shot, follow this loop:

1. **Build:** create or reuse the required assets and environment.
2. **Block:** establish camera, composition, timing, and major movement with simple geometry.
3. **Preview:** render a low-resolution / low-sample preview or use a verified real-time viewport capture.
4. **Inspect:** check composition, silhouette, scale, camera path, object intersections, animation timing, and visual clarity.
5. **Refine:** improve modeling, materials, lighting, animation, labels, and compositing based on visible issues.
6. **Approve:** compare the shot to the shot-list intent and chapter continuity.
7. **Final render:** render at final quality and verify the actual output sequence / file.
8. **Log:** record the file path, settings, frame range, and any known limitation.

Do not render an entire ten-minute video at final quality before checking representative shots. First create a style frame and a short motion test for the main visual language. Then produce one representative shot from each major visual mode and approve the look before scaling production. The style frame carries the design contract (palette, fonts, label plate, caption style) and must pass Gate DC and one `check_design` / contact-sheet review (Gate DR) before any other scene is built; compare it with later scenes as before/after pairs to catch drift.

## 11. Scientific and technical visual explanation

### 11.1 Explain mechanisms, not just objects

For every mechanism, consider these visualization techniques:

- Exploded view to show assembly order.
- Cutaway / sectional view to reveal hidden internal structure.
- Transparent or X-ray view to show relationships between layers.
- Flow visualization to show material, fluid, heat, or energy movement.
- Force / field visualization to show invisible interactions.
- Scale comparison to explain size and distance.
- Time compression or slow motion to reveal processes.
- Side-by-side comparison to distinguish two designs or states.
- Before / after to show a transformation.
- Energy / information flow diagram to explain inputs, outputs, and losses.

Use only the techniques that help the viewer understand the subject.

### 11.2 Label and diagram rules

- Labels should attach visually to the correct object or region.
- Use concise names, units, legends, and arrows. Avoid paragraphs on screen.
- Maintain a consistent type scale and alignment system.
- Make labels readable on a mobile screen at normal playback size.
- Avoid overlapping labels, crossing leader lines, unreadable microtext, and excessive floating UI.
- Clearly identify conceptual diagrams, simplified models, and not-to-scale visuals.
- A scientific color scale must have a defined meaning. Do not use arbitrary colors that imply false physical quantities.

## 12. Audio, narration, and editing

### 12.1 Audio layers

Plan sound as part of each shot, not as an afterthought:

- Narration: clean, intelligible, consistent level, natural delivery.
- Music: supports emotion and pacing without competing with the voice.
- Foley: mechanical clicks, movement, handling, impacts, air, room tone.
- Designed effects: energy pulses, transitions, whooshes, low-frequency impacts, subtle electronic textures.
- Ambience: workshop, laboratory, atmosphere, environment, or restrained science-fiction texture.

Do not use a loud sound effect for every movement. Silence and restrained ambience are powerful tools.

### 12.2 Mix and intelligibility

- Keep narration clearly above music and effects.
- Duck music and effects automatically or manually under speech where needed.
- Avoid clipping, distortion, excessive bass, harsh high frequencies, and sudden loudness jumps.
- Target approximately -14 to -16 LUFS integrated loudness for a typical YouTube mix, with true peak at or below -1 dBTP as a starting point; use listening tests and the actual delivery requirements.
- Use consistent sample rate and channel layout throughout the project, preferably 48 kHz for video production.
- Check audio on headphones and ordinary speakers if possible.

### 12.3 Editing rules

- Align picture changes with narration meaning, action, music, or sound cues.
- Let important reveals breathe. Do not cut away before the viewer understands the visual.
- Avoid long static shots that contain no new information, but do not cut away from complex diagrams too quickly.
- Use transitions to connect ideas, not conceal weak continuity.
- Keep chapter titles brief and visually consistent.
- Use subtitles / captions that match the spoken words and timing. Review generated captions; do not assume transcription timing is correct.
- Never allow captions to cover essential technical detail or UI labels.

## 13. Project folder and deliverables

Use the user's existing structure where practical. For a new project, start with:

```text
xplainedunseen_<topic>/
├── production/
│   ├── creative-brief.md
│   ├── script.md
│   ├── shot-list.csv
│   ├── asset-manifest.csv
│   ├── render-log.md
│   ├── design-contract.md
│   ├── motion-plan.md
│   ├── design-review/
│   └── edit-notes.md
├── research/
│   └── source-notes.md
├── blender/
│   ├── master-assets/
│   ├── environments/
│   ├── chapters/
│   ├── animation-library/
│   └── caches/
├── assets/
│   ├── textures/
│   ├── hdri/
│   ├── references/
│   ├── graphics/
│   ├── audio/
│   └── licensed-media/
├── renders/
│   ├── previews/
│   ├── image-sequences/
│   └── final-shots/
├── edit/
│   ├── project-files/
│   ├── captions/
│   └── exports/
└── delivery/
    ├── final-video.mp4
    ├── thumbnail.png
    ├── captions.srt
    └── video-description.md
```

Expected delivery items depend on the user's request and available tools. Aim to provide:

- Final video export.
- Editable Blender project files and dependencies.
- Script and shot list.
- Preview renders / style frames.
- Captions / subtitle file.
- Thumbnail image.
- Video description and source list.
- A short completion report listing verified files, render specs, runtime, frame rate, and known limitations.

If a final video cannot be rendered or assembled in the current environment, provide all completed project files and state precisely which stage remains. Do not label a preview as the final export.

## 14. Quality assurance gates

Do not move to the next stage until the relevant gate is satisfied, unless a documented constraint requires a conscious compromise.

### Gate A — Story approval

- Opening creates curiosity within the first 5–15 seconds.
- The central question and viewer promise are clear.
- The narrative has logical progression and a real payoff.
- The script fits the intended runtime when read aloud.
- Factual claims have supporting sources or are properly qualified.

### Gate B — Asset approval

- Main assets have correct silhouette, scale, proportions, and required parts.
- Materials respond plausibly to light.
- Names, collections, and dependencies are organized.
- No obvious intersections, floating pieces, holes, broken normals, or clipping.
- Asset reads clearly at the intended camera distance.

### Gate C — Shot approval

- Shot communicates its intended point without narration-dependent guessing.
- Camera movement and subject motion are smooth and motivated.
- Lighting supports the focal point.
- Labels are accurate and readable.
- No accidental flicker, geometry pop, simulation glitch, z-fighting, or frame jump.
- Shot matches the look and continuity of adjacent shots.

### Gate D — Edit approval

- Narration, picture, captions, music, and effects are synchronized.
- No gaps, accidental black frames, missing shots, or unintended freeze frames.
- No abrupt audio changes, clipping, or music overpowering speech.
- The video has a satisfying opening, coherent middle, and memorable ending.
- Total runtime matches the request within a reasonable tolerance.

### Gate E — Export approval

- Export exists at the stated path and can be opened / probed.
- Resolution, frame rate, aspect ratio, codec, audio, and duration are verified.
- Captions and thumbnail are present when requested.
- Watch the full export when feasible; at minimum inspect the opening, chapter transitions, high-complexity scenes, and ending.
- Check for black frames, audio silence, corrupt frames, wrong aspect ratio, missing media, or watermark / debug overlays.

## 15. YouTube packaging

For a finished video, prepare a small packaging set:

- **Title:** specific and curiosity-driven; no unsupported superlatives or false promises.
- **Thumbnail:** one strong subject, one clear visual contrast, readable at small size, minimal text (ideally 0–4 words), no clutter. Use the episode palette and display font from the design contract and run `check_design` with `thumbnail: true` (type at least 100 px, six words at most) before delivery.
- **Description:** concise premise, useful chapter timestamps, credits / licenses, and sources for factual claims.
- **Captions:** accurate, synchronized, punctuated, and properly formatted.
- **Chapters:** reflect meaningful topic changes, not arbitrary equal intervals.
- **End screen:** allow a clean visual hold and space for YouTube end-screen elements when requested.

Do not use another creator's thumbnail, branding, or exact composition. Build an original channel identity.

## 16. Efficiency and quality management

- Reuse master assets, environments, material libraries, lighting rigs, camera rigs, node groups, animation actions, and graphic templates.
- Build a small number of high-value hero assets rather than hundreds of generic assets.
- Use proxies, low-resolution previews, simplified simulations, and render samples during look development.
- Render representative frames before full sequences.
- Render image sequences for long or expensive shots where practical.
- Parallelize only independent work that will not create file conflicts or inconsistent asset versions.
- Track expensive tasks and avoid repeating completed work.
- Keep a clear distinction between draft, preview, approved, and final assets.
- Prioritize fixes by viewer impact: broken explanation / factual error first, then composition / animation defects, then polish.

## 17. How to respond to common user requests

### User gives only a topic

Create a short creative brief, research the subject if factual, propose the strongest story angle, then begin the production workflow if the user is asking for a video rather than merely ideas. Make reasonable assumptions about runtime and visual direction.

### User asks for a full video

Execute end-to-end: research → story → script → shot list → asset plan → EngineX capability discovery → asset / scene creation → previews → revisions → final renders → edit / audio / captions → export verification → delivery report.

### User asks for assets only

Create production-ready, reusable assets with clean names, materials, pivots, scale, dependencies, and a small preview. Do not create an unrelated full video.

### User asks for a Blender scene or animation

Create or modify the actual `.blend` / scene assets using the available EngineX and Blender capabilities. Include a preview render or animation test and verify the saved project.

### User asks to analyze a reference video

Analyze the storytelling and visual techniques, identify transferable principles, and explain how XplainedUnseen can create an original version. Do not automatically create a prompt or a project unless asked.

### User asks for a review

Inspect the actual project or video if accessible. Report concrete issues with timestamps / object names / file paths where possible. Prioritize issues by impact and, when asked, fix them rather than only listing them.

## 18. Final response format after production

Keep the completion report practical and honest. Include:

1. **What was created** — scenes, assets, chapters, or final export.
2. **Verified output paths** — exact paths only.
3. **Video specifications** — actual runtime, resolution, frame rate, codec, and audio settings when verified.
4. **Quality checks** — what was previewed, inspected, or tested.
5. **Remaining limitations** — any missing renders, unverified sections, licensing needs, or manual actions.

Never say "complete" when only a script, prompt, preview, or partial render exists. Clearly distinguish completed production from planned production.

## 19. The ultimate quality test

Before delivery, ask:

- Would a viewer understand the subject better after watching this?
- Does every major visual have a storytelling or explanatory purpose?
- Does the video feel like one coherent XplainedUnseen production rather than unrelated AI-generated clips?
- Are the most important claims trustworthy and properly qualified?
- Does the 3D work feel intentional, detailed, and cinematic without sacrificing clarity?
- Is the final export genuinely ready to publish?

If any answer is no, fix the highest-impact issue before delivery or state the limitation honestly.

---

# PART II — Multi-tool documentary orchestration

## 20. Tool selection principles

Pick the medium that makes the concept easiest to understand, then the tool. Combine methods within a scene when useful; use a tool only when it adds value.

| Need | Medium | EngineX capability |
|---|---|---|
| Mechanical/physical object, cutaway, rig, product shot, physics | 3D | Blender: `blender/script`, `inspect`, `preview`, `render`, `uv`, `bake`, `simulate`, `composite`, `turntable`, `product-shot` |
| Large environment, facility walkthrough, real-time lighting | 3D environment | Unreal — only when a tested quality/performance advantage exists |
| Diagrams, data, timelines, comparisons, process steps, labels, chapter cards | Motion graphics | `motion-graphic` (+ `/snapshot`, `/check`); explore component/template catalogue first |
| Invisible science (atoms, fusion, fields) | Scientific visualization | Blender particles/sim and/or motion-graphic diagrams |
| History, evidence, real places | Archival/photos/maps/timeline | Licensed media + image tools + motion-graphic timelines/maps |
| Emotional moments | Footage + music + directed voice | Generative media, emotive speech, sound design |
| Cut, join, transition, reframe, retime, duck, loudness, encode | Editing | `video/probe`, `frames`, `concat`, `transition`, `compose`, `duck`, `volume`, `fade`; `smart-video/retime`, `enhance`, `render-timeline` |
| Narration | Voice | `emotive-speech`, `speech` |
| Word timing, captions | Transcription | `transcribe/words`, `subtitle`, `align`, `separate`; `voice-activity/segments` |
| Images, video, music, backgrounds, upscaling | Generative | Saved workflows via `list_workflows` / `run_workflow` |
| Scene detect, isolate subject, 2.5D camera | Utility | `scenes`, `rotoscope`, `image-cutout`, `depth-motion` |

Rules: use the real catalogue (`find_operation`, `describe_operation`, `list_workflows`) — never guess names or parameters. Generated footage must not replace accurate scientific visualization. Never force Unreal or Blender in because it is available.

## 21. Narration-to-visual mapping (required before production)

Create `production/narration-visual-map.md` (or a column set in the shot list). For each important narration segment record: what is explained; what must be visible; what moves; camera target; what is highlighted; on-screen information; caption placement; **chosen medium and tool**; status.

Principles: show the exact component being discussed (engine → engine, atom → microscopic world, history → place/date/people/timeline, experiment → the real process). Every visual must add new information, context, or emotion. Never reuse the same animation repeatedly just because the asset exists.

## 22. Beginner-first explanation

Assume no prior knowledge. Define terms at first use; build progressively; use simple analogies, labeled components, step-by-step animation, before/after, micro/macro views. Visuals must make the idea easier, not busier. Scientific accuracy is never sacrificed for drama.

## 23. Multimodal scene production

A scene may combine, e.g.: Blender mechanism + motion-graphic labels + emotive narration + word-aligned captions + sound design + compositing; or real footage + depth-motion + scientific diagram + narration. Procedure per scene: choose techniques → inspect catalogue schema → generate a preview/snapshot → **inspect the output** (`motion-graphic/snapshot|check`, `blender/preview`, `video/frames`) → refine → final. Maintain one palette, typography, and camera/motion grammar across all tools so scenes cut together.

## 24. Motion graphics and data visualization

Motion graphics are teaching tools, not decoration: animated diagrams, process steps, comparisons (e.g. temperatures), timelines, annotations, chapter cards. Explore the component/template catalogue before building from scratch. Pages are authored with GSAP (preferred), Anime.js or Motion per `describe_operation`'s `authoring` rules. Use defined color scales and units; label conceptual or not-to-scale graphics. Avoid random HUDs and glow.

## 25. Voice and audio direction

Choose the narrator with the voice-inspection tools and keep one narrator identity per episode. Direct delivery to the story (curious, investigative, serious, dramatic, emotional) via `emotive-speech`. Plan separate sound layers — atmosphere, machinery, transitions, impacts — plus music that supports, never overpowers, narration (duck under speech; loudness per section 12.2). Generate narration before locking edit timing.

## 26. Caption synchronization

Captions come from real word-level timestamps (`transcribe/words`, `transcribe/align`); **never estimate word timing by dividing sentence duration**. Highlight the currently spoken word; keep consistent typography; stay readable on bright and dark scenes; place in negative space per scene composition and never cover important objects.

## 27. Editing and assembly

Assemble with video/smart-video tools (concat, transition, compose, retime, duck, volume, fade, `render-timeline`) according to editing need, not indiscriminately. Use transitions that carry continuity. Keep one fps/sample rate across the timeline. Probe every intermediate (`video/probe`).

## 28. Final audiovisual QC

Beyond Gate E: every narration segment has its mapped visual; captions sync to audio at sampled points; no caption/label collisions; narrator and loudness consistent; music ducks correctly; no repeated filler shots; no untextured grey models, excess glow, or generic AI filler; scientific claims match research notes. Review the whole documentary, fix highest-impact issues, then export and package (video, captions, thumbnail, description/sources).

## 29. Token, credit, and resource optimization

- Inspect existing assets and approved scenes before creating new ones; reuse them.
- Skip redundant tool discovery and repeated file reads; keep tool outputs concise (summaries, paths, not dumps).
- Batch independent operations; preview before expensive finals.
- Respect the **two Blender GPU pod** limit — queue, don't flood. Don't poll jobs repeatedly (check `fleet_status` once, then `get_job` sparingly).
- Don't rebuild existing production infrastructure.
- Maintain `production/claude_handoff.md`: current state, completed milestones, active jobs, errors, next actions. Label every operation **planned / running / completed / failed / verified**.

## 30. New-topic procedure

1 research → 2 story → 3 narration → 4 chapters & scenes → 5 narration-to-visual map → **5a design contract (section 37, Gate DC)** → 6 pick technique per scene → **6a motion plan (Gate MP)** → 7 generate & verify assets → 8 animations/diagrams/explanations → 9 narration + captions synced → **9a design review per scene (Gate DR)** → 10 sound design & music → 11 assemble → 12 review & improve → 13 export & package (Gate E includes `check_design` on the export). When execution is requested, do not stop at a storyboard or previews.

---

# PART III — Cinematic studio standard (default for every video)

## 31. Philosophy
Every video must look like a professionally directed animated documentary: visual explanation over information display, cinematic composition, realistic lighting, detailed materials, smooth intentional animation, physical consistency. Not a collection of AI clips. Full standards, movie-level animation do/avoid list, explanatory staging and scene QA: `references/studio-standards.md`. Quality and accuracy are never reduced to save tokens.

## 32. Documentation-first (before any complex scene, animation, material, lighting or sequence)
1. Check cached notes: `references/ep001-lessons.md`, `references/blender-lookup.md`.
2. Else `Grep` the offline **Blender 5.3 manual** text copy (`C:/Users/dinot/OneDrive/Pictures/Documents/Deepsoch/enginex_ideas/.claude/blender_manual_v530_en_text/`: grep `INDEX.md` by topic, then `text/`; topic map and version caveat in `references/blender-lookup.md`; the 5.2 epub copy `.../blender_manual_v520_en.epub/` is the fallback; see also skill `blender-manual`) and Read only the matching page. EngineX pods have run Blender 5.2, so confirm any 5.3-only feature exists on the pod (tiny `blender/script` printing `bpy.app.version_string`) before relying on it. Name the manual page(s) you used in the asset or shot notes.
3. Unreal: `.claude/unreal_engien docs/` is currently EMPTY, so report the guide as missing instead of assuming; see `references/unreal-cinematics.md`.
4. Use documented features only; never invent API names or unsupported operations. Cache each new verified finding in `references/ep001-lessons.md` (rename to a general lessons file if desired).

## 33. Asset-first
Inspect existing project assets and `.blend`/build scripts first, then libraries, then adapt, then model, then optimize. Inspect each asset for missing meshes/textures/materials, wrong proportions, inconsistent look before animating. Details: `references/studio-standards.md`.

## 34. Mandatory rules for every future video
1 Documentation first. 2 Inspect existing assets first. 3 Reuse suitable assets. 4 Manually create only what is missing. 5 Cinematic quality plus explanatory clarity. 6 Never compromise geometry, textures, materials, animation. 7 Blender vs Unreal by strength; never force both. 8 Every animation has a storytelling purpose. 9 Every scene passes visual QA (a render that merely completed is not done). 10 Preserve the workflow; add new learnings to the references.

## 35. Token-efficient production (never at the cost of quality)
Read selectively (one page/section, not whole manuals); cache findings in references; don't re-inspect assets/config/docs unless changed; batch related operations; reuse models, materials, scripts, workflows; implement instead of long explanations or re-planning; QA critical visuals and the final render, not unchanged parts; update only relevant skill sections; call EngineX only when it serves the current task; lookup order: local notes, then offline docs, then other sources only if needed. Existing rules in section 29 still apply.

---

# PART IV — EngineX design skills in the pipeline (mandatory, added 2026-11-06)

Goal: every video is directed like a professional animated documentary, with the combined eye of a 3D artist, a senior
motion designer, a graphic designer, a typographer, an art director and a quality-control designer. These stages are
inside the existing pipeline, not a second one. Full tables, templates and conflict rulings: `references/design-system.md`.

## 36. The four skills and the order they run in
`get_skill` (once per episode, then only the reference the stage needs): `enginex-color-palette` (colour), `enginex-typography`
(fonts), `enginex-motion-director` (motion), `enginex-design-polish` (review). Order inside any frame or scene:
**palette -> fonts -> polish -> motion -> motion-check -> polish again.** Design the settled frame still, check it, then move it.

## 37. Stage map (wraps the steps in section 30)
1 Research and story (`xu-research-first`) -> **2 Visual direction: write `production/design-contract.md`** (palette: house default **`navy-royal/dark`**, approved by the user 2026-11-06, otherwise via `list_palettes`
with previews shown and approved, fonts via `list_fonts`, the one motion idea and style, declared signal colours, sizes) ->
3 Asset and model creation (sections 8, 33; palette only tints world, light and graphics, never a real subject) ->
**4 Motion planning: `production/motion-plan.md`** (motion director Analyse, Direct, Specify; timeline rows timed from real word
timestamps) -> 5 Scene production (`xu-cinematic-3d`, `xu-motion-graphics`, engine per `engines.md`) -> 6 Typography and graphics
(contract fonts and sizes, palette roles, captions from real timestamps) -> **7 Design review** (`check_design` on every MG page
before it is shown or rendered; `motion-graphic/motion-check`; `snapshot` stills at moves and at the END of each hold; contact
sheets and `check_design input=` for Blender shots) -> 8 Final quality control (`check_design` on the export, palette, type and
motion audits, Gate D and E). No scene, label, title or caption is built before the design contract is approved.

## 38. Standards that never bend (16:9 documentary)
- Palette: three colours with fixed jobs; royal-blue-type accents are never word colour on the dark; words only on pairs of 4.5 : 1
  or more. Signal colours (optical, power, and so on) are declared once and keep one meaning for the whole film; all other graphics
  stay in the palette.
- Type: three jobs (display, text, label), two or three families, same role same font everywhere, nothing under 24 px, words in the
  middle 90% of the frame, no em dashes in on-screen text, captions at most two lines.
- Motion: one idea per video, one lead move per scene, every move has a one-line reason, words never travel while read, exits quicker
  than entrances, linear only for constant-speed things, the same role moves the same way across the film, labels held still by hold keys.
- Models: clean geometry, correct proportions, believable materials, professional lighting (sections 8, 9); look at library models in
  close-up for another brand's mark before building on them; one object per product across all shots.
- Review: inspect, fix, review again. Never show or render before the check; plan two full renders, three at most; mark every claim
  planned, rendered or checked.

## 39. New gates
- **Gate DC (design contract):** palette and lead approved after previews, fonts chosen, signal colours declared, motion idea written, sizes set.
- **Gate MP (motion plan):** lead move per scene, reason per move, times from real word timestamps, same object in every shot.
- **Gate DR (design review):** no `must` left, any `should` left is the user's choice and stated, hold-end stills looked at, before/after pairs
  saved in `production/design-review/`.
Gates A-E in section 14 still apply; Gate C additionally requires the scene's frames to have passed Gate DR, and Gate E requires `check_design` on the export.

## 40. Precedence and honesty
User's words > episode design contract > Part IV and `references/design-system.md` > older text in sections 3-35 (for design, type, colour and motion
questions only; storytelling, science accuracy, Blender-first and render-safety rules are unchanged). Do not call something "design polished" unless a
frame actually went through `check_design` or a contact sheet was inspected. Use only operations that exist in the live catalogue.

## 41. Learn, then prevent (user instruction, 2026-11-06, standing, two parts)
**A. Record.** Whenever you learn something new, verify a tool's real behaviour, or make a mistake, write it into `references/ep001-lessons.md` **in the same turn** (verified facts: what happened, the cause, the fix) and update the section of this skill, `references/design-system.md` or `references/blender-lookup.md` that it changes.
**B. Prevent (a note alone is not enough).** Before every build, render, asset fetch or EngineX call, open `references/preflight.md`, run the row for that action, and for any `.blend` run the automated `blender/scripts/preflight.py` through `blender/script` before rendering. State "pre-flight: checks run, result" in the reply; a FAIL blocks the action. For each new mistake add BOTH a row in `preflight.md` AND an automated check in `preflight.py`, then run the checker once on a known-good file to prove it has no false positives. Never repeat a recorded mistake; if a lesson turns out wrong, correct it. Report in the reply what was added and which pre-flight checks ran.

---

# Companion skills (added 2026-10-31, mandatory)
Before creating ANY animation, motion graphic, overlay or cinematic sequence: invoke `xu-research-first` (research the subject and best creators, write a research note), then `xu-motion-graphics` (on-screen text, maps, charts, MG) or `xu-cinematic-3d` (Blender/Unreal journeys, cutaways, 3D labels). These override any shortcut in sections 20-35. Since 2026-11-06 the design contract (section 37) comes after research and before either of them, and the four EngineX design skills of Part IV apply on top of both; where they disagree on size, font, colour or GPU tier, see `references/design-system.md` section 9.

# Standing narrator (decided 2026-10-31, overrides section 25 voice choice)
All English narration for every video uses EngineX `emotive-speech/speak` with `voice: "oliver"`, `emotion: "calm"` (no reference/describe/other voice). Never change the voice mid-video or between videos. Details: memory `narrator-oliver`, `XPLAINEDUNSEEN_EP002/assets/voice/README.md`.
