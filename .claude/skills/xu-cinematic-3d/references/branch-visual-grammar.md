# Branch Education visual grammar (frame study, 2026-11-10)

Source: frame-by-frame study of Branch Education, "Do you think Hard Disk Drives are Slow?" (ZZTC_dXcC2o, 5:17): 115 frames at 2 s from 0:00 to 3:50, 26 key frames, captions. Full log with timestamps: `research/ref_ZZTC_dXcC2o_frame_analysis.md` in the BrahMos repo. Not seen: audio, music, exact easing and lens values, the render engine (no tool is credited, so Blender is not confirmed); 3:50 to 5:17 not frame-sampled. Tags: [V] seen, [R] recommendation.

Use these as principles; do not copy the look, assets or scenes.

## Rules (evidence timestamp in brackets)
1. Open on the object in its real world at real scale, then open it: dolly in, lid off within 6 s. [0:00-0:06]
2. Put a prop in for an abstract claim (price tag for "cheap", SSD strips for "compared to SSD"). [0:16-0:20]
3. One accent set of part colours against grey metal, so parts are told apart without labels. [0:10, 2:00]
4. Highlight the part in 3D first (glow ring, diameter line), then place its number beside it. [0:08-0:12]
5. Each spoken number gets its own on-screen number within about 1 s of the word, never before it is spoken. [0:32, 1:10, 2:12, 3:36]
6. Maths: one derivation plate in the empty third of the frame, only the result coloured, held 8 to 10 s. [0:24-0:34]
7. Same colour pair for every comparison (fast green, slow pink), arc length proportional to speed. [0:26-0:34, 2:16-2:24]
8. A claim sentence gets a 1 s bold streak or sting, not a box. [0:36]
9. Announce "N parts" once with a roadmap card (thumbnails from the film's own shots plus big numerals), re-show it with one part lit at each chapter change and as the final recap. [0:36-0:40, 1:18, 1:52, 2:58]
10. A nanometre gap: camera at gap height, very shallow DoF (sharp slider edge, soft glowing track bars), the gap is the biggest dark slit in the frame, a growing I-beam marks it. [0:44-0:50]
11. Air shown as staggered pale arrows in 2 lanes under the slider, fanned out behind it. [0:48-0:50]
12. Small-part structure in a second angle: ghost shell plus thin translucent streamlines, rim-lit. [0:52-0:56]
13. Molecules as a bead-and-link vertical chain between the surfaces; reuse the same chain for the later analogy. [1:02-1:06, 3:14]
14. Something you cannot draw to scale gets a magnifier lens (chrome ring) over a larger neighbour, a straight leader, and the words "not to scale". [1:08-1:12]
15. Reuse the same ruler object twice (hair for 3 nm, then for 30 nm) so two numbers compare by eye. [1:08, 1:39]
16. Count numbers up on screen so they are felt, not only read (x10,000 to x20,000; 86,400 to 400,000; 3,145,112 to 6,000,000). [1:10-1:12, 2:10-2:12, 3:36-3:40]
17. Make an abstract state a physical toy: a magnetic domain is a glossy N/S cube, red up, blue down, with floating 0/1 digits. [1:22-1:30]
18. New idea, new set: dark void with a floor grid for the domain row; camera low and level, then a dolly forward and up. [1:22-1:36]
19. Speed text is 3D type lying on the moving surface ("75 mph" on the platter edge). [1:44-1:46]
20. Current as green bubbles with a bolt icon along the winding; field as light curved arrows. [2:00]
21. "So many" is shown by rendering density: coarse lines at 86,400, hair-thin lines at 400,000. [2:10-2:12]
22. Turn a count into a length: peel the rings off, stretch into a tube, unspool into one line to the horizon, label lands at the end of the move. [2:32-2:44]
23. A small dark "workings" plate in a corner, typed line by line; where it differs from the narration (<10 vs "fewer than 15"), say so on screen. [2:50-2:52]
24. Radial-blur zoom as the transition into the analogy world. [2:54, 3:02]
25. Analogy reuses the same elements in the order of the roadmap card; an inset map or gauge sits on the live shot. [3:04-3:10, 3:44-3:48]
26. A tiny quantity: isolate on pure black with a few bokeh specks and one I-beam label (grain of sand). [3:30-3:32]
27. A punch number stays on screen for the whole sentence plus the repeat; only the counter moves. [3:36-3:40]
28. Light beams colour-coded consistently (amber read, red write 1, blue write 0); the colours match the domain cubes. [3:16-3:26]
29. Fix a mistake with a tiny top-right grey footnote ("Correction:", "Note:") and keep the label layer separate from the render, so a fix needs no re-render. [0:30, 1:02, 1:06]
30. Never box the same text twice: pills only for part names, bare glow type for numbers, glass plates only for maths. [throughout]

## Timing
Labels land within about 1 s of the key word; hard cuts fall on sentence boundaries; about 4 to 8 s per fact. Build one cue sheet from the voice word timestamps and let both the Blender script and the motion-graphic page read it [R].

## Conflict with project rules (decide per project)
- BrahMos memory: no text boxes, charcoal-gold, one gold word, English labels only. Map Branch's pills to bare text with a thin leader and a gold underline; keep a plate only for the maths derivation, or drop it. Rules 4, 23 and 30 apply in that form.
- This skill's Labels line (dark plate) is for EP002 readability on pale backgrounds; it does not override a project's no-box rule.

## Build with EngineX
- [V in project] Blender 5.2 Cycles OptiX, MP4 render, boolean cutaways (rule 1, 12), emission pulses along traces (rules 7, 20), DoF with keyed focus (rule 10), per-frame label anchor projection fed to a motion-graphic page (rules 4, 5, 14).
- [R, not verified] ghost shells with streamlines, particle molecule chains, procedural hair or grain displacement, radial-blur post, count-up numerals in GSAP (GSAP itself is verified), chrome magnifier insert.
- Check find_asset before modelling; the library has no chip or PCB models.
