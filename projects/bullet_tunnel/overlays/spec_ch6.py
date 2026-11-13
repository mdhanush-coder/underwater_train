# chapter 6: the rock section (global 233.903-275.905 s, 42.0 s). Plate = blender/g_natm.py (ch6_natm.mp4). Line 65 = MG map.
# Facts: research ledger rows 4, 16, 17 (4.88 km Ghansoli-Shilphata, final blast 20 Sept 2025, ADIT).
_MAP = """<div style="position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 45%,rgba(16,18,22,.8),rgba(8,8,10,.94))"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
 <path d="M880 120 C 900 330, 860 520, 905 700 S 900 980, 930 1080 L 1240 1080 C 1215 900, 1255 700, 1222 520 S 1250 260, 1235 120 Z" fill="rgba(60,140,170,.18)" stroke="rgba(127,227,255,.35)" stroke-width="2"/>
 <path d="M420 600 C 560 590, 650 560, 730 560 S 1000 520, 1240 515" fill="none" stroke="rgba(255,248,230,.3)" stroke-width="5" stroke-linecap="round"/>
 <path id="n_seg" d="M1240 515 C 1330 512, 1420 505, 1500 470" fill="none" stroke="#F5B700" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <g font-family="JetBrains Mono" font-weight="600" font-size="22" letter-spacing=".1em" fill="#FFF8E6">
  <g><circle cx="420" cy="600" r="8" fill="#FFF8E6"/><text x="420" y="650" text-anchor="middle">BKC</text></g>
  <g><circle cx="1240" cy="515" r="9" fill="#FFF8E6"/><text x="1240" y="570" text-anchor="middle">GHANSOLI</text></g>
  <g><circle cx="1500" cy="470" r="9" fill="#FFF8E6"/><text x="1500" y="430" text-anchor="middle">SHILPHATA</text></g>
  <text id="n_lab" x="1370" y="560" font-size="20" text-anchor="middle" opacity="0">HARD ROCK</text>
 </g>
 <text x="1848" y="1030" fill="rgba(255,248,230,.6)" font-family="JetBrains Mono" font-size="18" letter-spacing=".12em" text-anchor="end">SCHEMATIC MAP &#183; NOT TO SCALE</text>
</svg>"""
_MAP_JS = """
tl.to('#n_seg', {strokeDashoffset: 0, duration: 1.6, ease: 'power2.inOut'}, 4.0);
tl.to('#n_lab', {opacity: 1, duration: .5}, 5.0);
"""
SPEC = dict(
    dur=42.0, chapter='06 &mdash; The rock section',
    plates=[('ch6_natm.mp4', 0.0, 42.0, 0.0)],
    pages=[dict(t=3.1, z=8.3, html=_MAP, js=_MAP_JS)],
    beats=[
        dict(kind='hl', t=0.3, z=3.2, pos=(72, 140), ital=['Is all of it', 'dug by a <span style="color:#F5B700">machine?</span>']),
        dict(kind='hl', t=3.5, z=7.9, pos=(72, 820), tag='Ghansoli &rarr; Shilphata', lines=['Solid <span class="g">rock</span>']),
        dict(kind='num', t=8.4, z=11.7, pos=(72, 140), label='Blasted rock tunnel', to=5, unit='<span class="u">km</span>', below='About', cd=1.0),
        dict(kind='pill', t=8.6, z=11.7, pos=(1848, 100), align='right', text='NATM &middot; drill and blast'),
        dict(kind='hl', t=12.0, z=14.8, pos=(72, 140), lines=['Deep holes', 'are <span class="g">drilled</span>'], scrim=True),
        dict(kind='hl', t=15.1, z=19.4, pos=(72, 140), lines=['Explosives,', 'a <span class="box">controlled blast</span>'], scrim=True),
        dict(kind='hl', t=19.7, z=23.5, pos=(72, 140), lines=['Then concrete', 'is <span class="g">sprayed</span>'], scrim=True),
        dict(kind='card', t=23.8, z=27.2, card=(1300, 150), anchor=(0.481, 0.334), title='<b>Rock bolts</b>', desc='Steel bolts pin<br>the rock in place'),
        dict(kind='hl', t=27.5, z=32.4, pos=(72, 140), tag='Adit', lines=['A <span class="g">side tunnel</span>', 'built midway'], scrim=True),
        dict(kind='hl', t=32.7, z=35.4, pos=(72, 140), lines=['Several faces', 'dug <span class="g">at once</span>']),
        dict(kind='hl', t=35.6, z=40.0, pos=(72, 140), tag='Final blast', lines=['<span class="g">20 Sept 2025</span>'], scrim=True),
        dict(kind='hl', t=40.2, z=42.0, pos=(72, 140), tag='Breakthrough', lines=['<span class="box">4.88 km</span> joined'], scrim=True),
    ],
)
