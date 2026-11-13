# XplainedUnseen — Design system and EngineX design skills (integration reference)

How palette, typography, motion direction and design review plug into the existing production pipeline. This file adds
stages and rules; it does not replace section 20-35 of SKILL.md, the Blender-first approach, or the companion skills.
Everything named here was checked against the live catalogue on 2026-11-06 (`list_palettes`, `list_fonts`,
`check_design`, `get_skill`, `motion-graphic/motion-check|polish|polish-media|check|snapshot|render`). If a name stops
resolving, trust the tool, not this file.

## 0. How to use the four EngineX skills

Call `get_skill` once per episode for each skill you will use, then read ONLY the reference file the current stage
needs. Cache anything learned in `references/ep001-lessons.md` (rule in section 32).

| Skill (`get_skill name`) | Owns | Read these references when the stage needs them |
|---|---|---|
| `enginex-color-palette` | the three-colour palette, its lead, contrast pairs, chart colours | `rules.md` (pairs, photos, charts), `tokens.md` (CSS roles) |
| `enginex-typography` | font choice per job (display, text, label), sizes, Hindi | `pairing.md`, `rules.md`, `scale.md` |
| `enginex-motion-director` | the one idea, motion plan, timeline table, review of motion | `principles.md`, `timing-and-easing.md`, `choreography.md`, `kinetic-type.md`, `camera.md`, `transitions.md`, `pacing.md`, `composition.md`, `engines.md`, `review.md` |
| `enginex-design-polish` | measuring and fixing frames, then hand-over with before/after | `by-hand.md`, `report.md`, `categories.md` |

Fixed order inside any one frame or scene: **palette -> fonts -> polish -> motion -> motion-check -> polish again**.
Design the settled frame still, check it, then move it. Motion lands exactly on the checked layout.

## 1. Stage map (extends the 13-step procedure in section 30)

| # | Stage | Existing steps it wraps | EngineX skill used | Output file | Gate |
|---|---|---|---|---|---|
| 1 | Research and story | `xu-research-first`, sections 4.2, 5 | none | `research/source-notes.md`, `production/script.md` | A |
| 2 | **Visual direction** | section 3, new | palette, typography, motion director (idea + style) | `production/design-contract.md` | **DC** |
| 3 | Asset and model creation | sections 8, 33 | palette (world and accent tones only) | asset manifest, `.blend` versions | B |
| 4 | **Motion planning** | section 21 map, shot list | motion director (Analyse, Direct, Specify) | `production/motion-plan.md` | **MP** |
| 5 | Scene production | sections 10, 23, `xu-cinematic-3d`, `xu-motion-graphics` | motion director (engines.md) | scene files, previews | C |
| 6 | Typography and graphics | sections 11.2, 24, 26 | typography, palette | MG pages, label plates, captions | C |
| 7 | **Design review** | section 14 Gate C, `snapshot` | design polish, motion-check | `production/design-review/` | **DR** |
| 8 | Final quality control | sections 12, 28, Gate D, E | design polish (media), motion director review.md | `production/render-log.md` | D, E |

Skipping stage 2 is not allowed: no scene, label, title or caption is built before the design contract is approved.

## 2. Stage 2 — the design contract (`production/design-contract.md`)

Write it once per episode, keep it short, and change it only with a note.

```
## Design contract (episode, date)
Idea (one sentence): the visual action this video is built on (motion director "the idea first").
Palette: <palette id>/<lead>   preview shown: <previewPage url>   approved: yes/no
  dark #..  accent #..  light #..   roles: background / text / highlight (from list_palettes)
Semantic signal colours (domain meaning only): name = hex = meaning, contrast on the ground >= 4.5 if ever on words
Type system: display <font + weight>, text <font + weight>, label <font + weight>, Hindi partner if needed
Sizes (16:9, 1920x1080): see section 5
Motion: style <name from styles.md>, entrance <token>, exit <token>, caption <token>, card <token>, camera grammar
Safe area: 16:9 words inside the middle 90% (>= 96 px margin); Shorts derived from it use platform "shorts"
Assumptions: anything chosen because it was not given
```

How to choose (do not guess names, call the tools):

1. **Palette. APPROVED HOUSE PALETTE (user, 2026-11-06): `navy-royal/dark`** — Midnight Navy `#0A1A3F` ground, Light Cream
   `#F8F3F0` words, Royal Blue `#044ABA` highlight blocks, lines and chart accents (never word colour on the navy, contrast
   2.2). Use it for every new episode, thumbnail and Short unless the user names another. Say "making it in navy-royal/dark";
   no new palette preview round is needed. Pass `palette: navy-royal` to `check_design`. The rest of this item is the
   procedure for when a different palette is wanted. `list_palettes` (the full list is large, so grep the saved file for ids or call it with `preview`).
   Show the palette's `previewPage` and the lead's `previewUrl`, say "making it in <id>", and use the default lead unless
   the person picks another. Starting proposals for the XplainedUnseen dark science identity, to be confirmed by the
   person: `navy-royal/dark` (midnight navy ground, cream words, royal-blue highlight blocks; contrast dark+light 15.5)
   or `black-royal/dark` (black ground, cloud-white words, royal blue). In both, **royal blue on the dark is never a word
   colour** (contrast 2.2 and 2.6): it is a block behind words, a line, a fill or a chart series.
2. **Fonts.** `list_fonts` (`category: tech-and-ai`, or `query`). The catalogue has no "Studio Grotesk" (EP002's face): a
   new episode takes catalogue fonts; EP002 keeps its own until the user decides. Proposed science set from real entries:
   display **Unbounded** 700 or **Exo 2** 800 (both listed under Science & Space), text **IBM Plex Sans** 500/600 (rupee
   drawn), label **IBM Plex Mono** or **Space Mono** 500 (Science & Space). Hindi text: **Rajdhani** draws Devanagari;
   every other face gets its `hindiPartner` (Hind). Use each font's `css` string from `list_fonts`. Show the previews and
   let the person choose before building.
3. **Motion style and idea.** Read motion director `styles.md` and write two or three candidate ideas, pick one.
   Test: could this video be swapped onto another channel's topic and still work? Then it has no idea yet.

## 3. Applying the palette in each medium

| Medium | Rule |
|---|---|
| Motion Graphic pages | Roles as CSS variables from motion director/palette `tokens.md` (`--bg --text --hl`). Chart series use the palette's colours and `color-mix` opacities; the highlight marks the one value that matters. Pass `palette: <id>` to `check_design` so fixes take its colours. |
| Blender world and light | Section 3.1 still rules: real objects keep physical materials; only the environment, rim light and graphics tones echo the palette (cool, dark, controlled). Never tint a real subject to match the palette. |
| Blender 3D labels | Dark plate in the palette's dark, light text, leader line in the light or the accent, anchor dot in the accent. This agrees with the `xu-cinematic-3d` dark-plate rule. |
| Blender 3D titles and logos | `blender/text-3d` takes its `font` from Motion Graphic's catalogue (house fonts included): set the contract's display font, a `material` that reads on the navy or black ground (matte or glass for science, never gold or neon unless the palette is gold or neon), `transparent: true` when it goes over footage. Look at the brightest frame for hot spots that hide letters. |
| Captions | Words in the palette's text colour; the spoken word marked by a highlight **block** (or underline when `highlightWords` is `none`), never by an off-palette colour. |
| Thumbnails | Palette ground, one subject, words only on pairs of 4.5 : 1 or more, run `check_design` with `thumbnail: true` (type >= 100 px, six words at most). |

**Semantic colours.** Documentary meaning colours (for example optical signal = cyan, electrical power = amber, from
`xu-motion-graphics`) are the one allowed exception to "no colour outside the palette". They exist only as marks of a
physical quantity (a pulse, a cable, a series), are declared once in the contract, keep one meaning for the whole film,
and never become decoration. All chrome (titles, captions, cards, lower thirds, chart frames) stays in the palette.

## 4. Typography rules for XplainedUnseen

- Three jobs only. **display**: chapter titles, the one big number, a title card. **text**: captions, sublines,
  legends. **label**: kickers, chapter marks, component names, units, chart axes. Never a full sentence in display, never
  a three-word hook in text.
- Two families, three at most (a mono for labels counts). Same job, same font and weight in every scene and every tool.
- Captions: one or two lines, at most about 32 characters a line, never covering a labelled component. Split a long
  sentence across caption boxes. Timing from real word timestamps (section 26), never divided evenly.
- Labels: concise name plus unit, attached to the real component, never a paragraph.
- Scientific terms are set once with a short definition at first use (a text-job subline), then as plain label.
- Capitals-only styles never get lowercase; layered or novelty fonts only at display size.
- Hindi (Shorts or localisation): a font that draws Devanagari, line height 1.18 or more, never letter-spaced, animated
  by word or line. Rupees as the sign with Indian grouping (₹1,00,000).
- No em dashes in any on-screen text or caption.

## 5. Sizes and safe area (16:9, 1920 x 1080; from typography `scale.md` and design polish)

| Job | Use | Size | Minimum |
|---|---|---|---|
| display | title card, chapter title | 120-135 | 96 |
| display | name in a lower third, big number label | 62-72 | 54 |
| text | subline, caption, role | 36-40 | 32 |
| label | chapter mark, component name, axis | 28-30 | 24 |

- Nothing under **24 px** anywhere, fine print included (this supersedes the old 22 px figure).
- Words inside the middle 90% of the frame (margin >= 96 px) and clear of the bottom ~90 px (player UI).
- Every word at 4.5 : 1 against what is really behind it at every second it is on screen. Over 3D footage use a soft
  scrim or a dark plate; a busy picture is judged where it is worst.
- Four words or more stay up at least 17 characters a second, 0.8 s minimum. No more than three flashes in a second.
- Shorts and reels cut from a long video: 9:16, `platform: "shorts"` (keep words out of the top 15%, bottom 35%,
  right 18%); never reuse the 16:9 layout by cropping.

## 6. Stage 4 — motion plan (`production/motion-plan.md`)

Follow motion director's Analyse -> Direct -> Specify. Write the timeline **before** building a scene.

1. Per scene: one objective, one focal point, the **lead move** (everything else supports it, waits for it, or stays
   still), what stays still, how words arrive, how the scene hands over, which narration word or sound each move lands on.
2. A row per animated event: `element | start-end (s) | from -> to | ease token | stagger | cue (voice line or beat)`.
   Times come from the generated narration's word timestamps, not from the script.
3. Pick the engine with motion director `engines.md`: diagram, chart, type, caption or lower third -> **Motion Graphic**
   page (one paused GSAP timeline); mechanism, cutaway, 3D title or logo, product -> **Blender** (`script`, `text-3d`,
   `logo-3d`, `turntable`, `product-shot`); a still that must move -> **Depth Motion**; footage with action ->
   **Speed ramp**. Mixed scenes render each part on its engine and assemble where the timeline lives.
4. Blender camera grammar stays as in `xu-cinematic-3d`: a continuous path, Bezier easing, **hold keys** wherever a label
   is read, plausible speed. A label never travels while it is being read: arrive, settle, read, leave. Exits are quicker
   than entrances. Linear motion only for constant-speed things (a drift, a ticker, a signal pulse). Same role, same
   move for the whole film.
5. Transitions connect two ideas or keep rhythm; a hard cut is the default; prefer match cuts and push-throughs
   (section 3.3). Anything else needs a one-line reason.

Gate **MP**: every move has a reason said in one line; each scene names its lead move; times come from real word
timestamps; the product or hero asset is the same object in every shot (lay stills side by side).

## 7. Stage 7 — design review loop (do not skip, do not render first)

Never show, render or hand over a page before it has been checked.

**A. Motion Graphic pages (labels, charts, captions, titles, lower thirds)**
1. `check_design` with the page (`html` or `project`, `media`, `palette: <id>`, leave `platform` out for 16:9, leave
   `at` out, `fix` on). It measures the page in a browser, fixes what a rule can fix, and returns before/after stills,
   findings and `fixed.html`. For a video use `render: true` in the same call so the video is rendered once, from the
   fixed page.
2. Look at the after still. Fix every `must` and `should` left by hand (`by-hand.md`), run again until none is left.
   Auto-fixed blocks that float or space unevenly are re-set in the page's own CSS.
3. `motion-graphic/motion-check` on the final page (add `beats` when there is music). Fix every `should`.
4. Take stills with `motion-graphic/snapshot` at each move's middle and end, each transition's middle, and the middle
   **and end** of each hold. Look at every one. Use `tier: "cpu"` for snapshots and drafts (the existing render-safety
   rule beats motion director's blanket GPU rule; never queue GPU work while another session is busy).

**B. Blender shots and any rendered video (no page to measure)**
1. Contact sheets as in `xu-cinematic-3d` (640 x 360, low samples, 8 tiles) plus the CPU label-fit check. Look at
   them with Read.
2. `check_design` with `input` (a still or an MP4) runs polish-media on pixels: text size, contrast, safe zones, reading
   time, flashes, captions against speech. It never changes pixels: fix in the Blender or MG source, re-render, check
   again.
3. Compare before and after as image pairs saved under `production/design-review/<scene>_before.png` and `_after.png`;
   show them when reporting.

**C. What to report after a review** (answer the question asked first): counts of findings by severity, what the
check fixed, what you fixed by hand and why, the before/after pair, the new render. Mark every claim
**planned / rendered / checked**; never say a frame was looked at, a move was smooth or a caption was in sync unless a
still, a check or a job result showed it. Minor findings are listed, not re-rendered for. Plan two full renders, three
at most.

Gate **DR**: no `must` left; any `should` left is the user's choice and said; hold-end stills looked at; after still
shows a laid-out page, not nudged blocks.

## 8. Stage 8 — final quality control (adds to Gate D and E)

- `check_design` with the final export (or each chapter export) as `input`: flashes within limit, words up long enough,
  captions on time against the speech, no text under 24 px, nothing in the bottom player zone, contrast.
- Palette audit: sample 5-8 frames across chapters; every colour is the palette or a declared signal colour.
- Type audit: every on-screen text uses the contract's fonts at the contract's sizes.
- Motion audit (`review.md`): idea first (is there a moment someone remembers and that is this channel's, not a
  template), then each problem with severity (critical, major, minor), second, and concrete correction. Fix critical and
  major, render again, check again.
- One look across all scenes: same palette, same type roles, same entrance and exit, same camera grammar.

## 9. Conflicts resolved (this order wins)

1. The user's own words, then the episode design contract, then these rules, then older text in SKILL.md.
2. **Palette vs "charcoal / cyan / amber" in section 3.1.** 3.1 describes the 3D world and signal colours; the EngineX
   palette governs graphics chrome. Signal colours are declared in the contract and used only for their meaning.
3. **Fine print 22 px (xu-motion-graphics) vs design polish 24 px.** 24 px is the floor.
4. **Studio Grotesk vs catalogue fonts.** New episodes use catalogue fonts; the old face stays only inside EP002.
5. **GPU tier.** Motion director says GPU for every job that takes one; the studio render-safety rule (two Blender GPU
   pods, no GPU queueing while another session is busy, CPU for MG snapshots and drafts) wins.
6. **Words that move.** Motion director forbids travelling words; 3D labels attached to components follow the camera
   only during a move and are held still (hold keys) while read. Same rule, two tools.
7. **Caption colour.** The spoken word is marked with a palette highlight block or underline, not an off-palette colour.
8. **Standing narrator** (`oliver`, `calm`) and **sound from the library** (`find_sound` first, generate only when asked
   or nothing fits, and say which) are unchanged by anything here.
9. Particles and glow only where the explanation needs them (agrees with the user's earlier rule; particles on dark
   frames read as noise).

## 10. Limits and honesty

- `check_design` on a picture or video reports; it does not edit pixels. Words printed inside a 3D scene (a sign, a
  model's engraving) are reported too; sort them against the stills.
- Bengali, Gujarati, Punjabi, Kannada, Malayalam and Odia on screen are not read by the media check; say so.
- `list_palettes` returns a very large result; save-and-grep it instead of reading it whole.
- None of these skills builds Blender geometry, materials or lighting: that stays with sections 8, 9, 32-33 and
  `xu-cinematic-3d`. Do not claim a Blender scene was "design polished" unless a frame went through `check_design` or a
  contact sheet was inspected.
