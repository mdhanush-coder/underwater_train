# chapter 7: the finale (global 275.905-310.5 s, 34.6 s). Creek reuse from the hook plate (0-8.1), then blender/h_finale.py
# (ch7_finale.mp4) from chapter time 7.1 with a 1 s dissolve. Lines 78-79 are the MG map. Anchors from the ch7 agent (local t + 7.1).
_MAP = """<div style="position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 45%,rgba(16,18,22,.94),rgba(8,8,10,.97))"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
 <path d="M880 120 C 900 330, 860 520, 905 700 S 900 980, 930 1080 L 1240 1080 C 1215 900, 1255 700, 1222 520 S 1250 260, 1235 120 Z" fill="rgba(60,140,170,.22)" stroke="rgba(127,227,255,.45)" stroke-width="2"/>
 <text x="1060" y="300" fill="#7FE3FF" font-family="Inter" font-style="italic" font-weight="800" font-size="26" letter-spacing=".12em" text-anchor="middle">THANE CREEK</text>
 <path d="M420 600 C 560 590, 650 560, 730 560 S 1000 520, 1240 515" fill="none" stroke="rgba(255,248,230,.25)" stroke-width="5" stroke-linecap="round"/>
 <path id="a1" d="M730 560 C 650 560, 560 590, 440 599" fill="none" stroke="#F5B700" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <path id="a2" d="M1200 517 C 1100 520, 980 528, 752 559" fill="none" stroke="#FFF8E6" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <g font-family="JetBrains Mono" font-weight="600" font-size="22" letter-spacing=".1em" fill="#FFF8E6">
  <g><circle cx="420" cy="600" r="9" fill="#FFF8E6"/><text x="420" y="650" text-anchor="middle">BKC</text></g>
  <g><circle cx="730" cy="560" r="9" fill="#FFF8E6"/><text x="730" y="520" text-anchor="middle">VIKHROLI</text></g>
  <g id="m_sav" opacity="0"><circle cx="1200" cy="517" r="9" fill="#FFF8E6"/><text x="1200" y="575" text-anchor="middle">SAVLI</text></g>
  <text id="m_l1" x="575" y="640" fill="#F5B700" font-size="20" text-anchor="middle" opacity="0">TBM 1</text>
  <text id="m_l2" x="1000" y="575" font-size="20" text-anchor="middle" opacity="0">TBM 2</text>
 </g>
 <text x="1848" y="1030" fill="rgba(255,248,230,.6)" font-family="JetBrains Mono" font-size="18" letter-spacing=".12em" text-anchor="end">SCHEMATIC MAP &#183; NOT TO SCALE</text>
</svg>"""
_MAP_JS = """
tl.fromTo('#root video.clip:nth-of-type(2)', {opacity: 0}, {opacity: 1, duration: 1.0, ease: 'power1.inOut'}, 7.1);
tl.to('#a1', {strokeDashoffset: 0, duration: 1.6, ease: 'power2.inOut'}, 10.0);
tl.to('#m_l1', {opacity: 1, duration: .4}, 10.8);
tl.to('#m_sav', {opacity: 1, duration: .4}, 12.1);
tl.to('#a2', {strokeDashoffset: 0, duration: 3.0, ease: 'power2.inOut'}, 12.4);
tl.to('#m_l2', {opacity: 1, duration: .4}, 13.8);
"""
SPEC = dict(
    dur=34.6, chapter='07 &mdash; The finish',
    plates=[('transition.mp4', 0.0, 8.1, 16.5), ('ch7_finale.mp4', 7.1, 27.5, 0.0)],
    pages=[dict(t=9.5, z=17.0, html=_MAP, js=_MAP_JS)],
    beats=[
        dict(kind='hl', t=0.4, z=6.9, pos=(72, 760), tag='Back to the surface', lines=['Thane <span class="g">creek</span>']),
        dict(kind='hl', t=7.4, z=9.6, pos=(72, 140), lines=['Two machines,', '<span class="g">one from each side</span>']),
        dict(kind='hl', t=17.4, z=21.2, pos=(72, 140), tag='When it opens', lines=['The bullet <span class="g">train</span>']),
        dict(kind='num', t=21.5, z=26.6, pos=(72, 140), label='Top speed', to=320, unit='<span class="u">km/h</span>', below='Up to', cd=1.4),
        dict(kind='hl', t=26.9, z=31.4, pos=(72, 140), ital=['You might not', 'even <span style="color:#F5B700">notice</span>'], scrim=True),
        dict(kind='hl', t=31.7, z=34.6, pos=(72, 140), lines=['The whole sea,', '<span class="box">right above you</span>']),
    ],
)
