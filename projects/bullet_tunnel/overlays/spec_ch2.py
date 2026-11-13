# chapter 2: the route (global 37.17-83.44 s, 46.27 s). Pure motion graphics over the blurred sunset creek plate.
_bg = [('script.mp4', 12.5 * k, 12.5, 0.0) for k in range(4)]

_MAP = """<div style="position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 45%,rgba(16,18,22,.72),rgba(8,8,10,.92))"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0">
 <defs><pattern id="dg" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="rgba(255,248,230,.07)"/></pattern></defs>
 <rect width="1920" height="1080" fill="url(#dg)"/>
 <path id="m_creek" d="M880 120 C 900 330, 860 520, 905 700 S 900 980, 930 1080 L 1240 1080 C 1215 900, 1255 700, 1222 520 S 1250 260, 1235 120 Z" fill="rgba(60,140,170,.22)" stroke="rgba(127,227,255,.45)" stroke-width="2" opacity="0"/>
 <text id="m_creekl" x="1060" y="300" fill="#7FE3FF" font-family="Inter" font-style="italic" font-weight="800" font-size="26" letter-spacing=".12em" text-anchor="middle" opacity="0">THANE CREEK</text>
 <path id="m_route" d="M420 600 C 560 590, 650 560, 730 560 S 1000 520, 1240 515 S 1420 500, 1500 470" fill="none" stroke="#F5B700" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <path id="m_creekseg" d="M880 548 C 980 530, 1100 520, 1240 515" fill="none" stroke="#FFF8E6" stroke-width="11" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <g font-family="JetBrains Mono" font-weight="600" font-size="22" letter-spacing=".1em" fill="#FFF8E6">
  <g id="d_bkc" opacity="0"><circle cx="420" cy="600" r="10" fill="#F5B700"/><circle cx="420" cy="600" r="20" fill="none" stroke="#F5B700" stroke-width="2"/><text x="420" y="650" text-anchor="middle">BKC</text></g>
  <g id="d_vik" opacity="0"><circle cx="730" cy="560" r="8" fill="#FFF8E6"/><text x="730" y="520" text-anchor="middle">VIKHROLI</text></g>
  <g id="d_gha" opacity="0"><circle cx="1240" cy="515" r="8" fill="#FFF8E6"/><text x="1240" y="575" text-anchor="middle">GHANSOLI</text></g>
  <g id="d_shi" opacity="0"><circle cx="1500" cy="470" r="10" fill="#F5B700"/><circle cx="1500" cy="470" r="20" fill="none" stroke="#F5B700" stroke-width="2"/><text x="1500" y="425" text-anchor="middle">SHILPHATA</text></g>
 </g>
 <text id="m_note" x="1848" y="1030" fill="rgba(255,248,230,.6)" font-family="JetBrains Mono" font-size="18" letter-spacing=".12em" text-anchor="end" opacity="0">SCHEMATIC MAP &#183; NOT TO SCALE</text>
</svg>"""
_MAP_JS = """
tl.to('#d_bkc', {opacity: 1, duration: .5}, 0.6);
tl.to('#m_route', {strokeDashoffset: 0, duration: 4.2, ease: 'power2.inOut'}, 1.2);
tl.to('#d_vik', {opacity: 1, duration: .4}, 2.6); tl.to('#d_gha', {opacity: 1, duration: .4}, 4.4); tl.to('#d_shi', {opacity: 1, duration: .5}, 5.2);
tl.to('#m_note', {opacity: 1, duration: .5}, 1.0);
tl.to(['#m_creek', '#m_creekl'], {opacity: 1, duration: .8}, 14.4);
tl.to('#m_creekseg', {strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut'}, 14.8);
"""

_PROF = """<div style="position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 45%,rgba(16,18,22,.78),rgba(8,8,10,.94))"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0" font-family="JetBrains Mono" font-weight="600" letter-spacing=".1em">
 <path d="M300 380 L 677 380 C 690 410, 1100 410, 1117 380 L 1240 380 C 1300 300, 1360 250, 1400 250 C 1440 250, 1500 300, 1560 380 L 1620 380 L 1620 760 L 300 760 Z" fill="rgba(120,92,62,.35)" stroke="rgba(255,248,230,.55)" stroke-width="2"/>
 <path d="M677 380 C 690 410, 1100 410, 1117 380 Z" fill="rgba(60,140,170,.45)"/>
 <rect id="p_band" x="300" y="435" width="1320" height="88" fill="rgba(245,183,0,.12)" stroke="rgba(245,183,0,.5)" stroke-dasharray="8 8" opacity="0"/>
 <path id="p_tun" d="M300 470 C 420 470, 560 445, 700 450 S 1000 470, 1150 470 S 1340 500, 1400 501 S 1560 470, 1620 455" fill="none" stroke="#F5B700" stroke-width="8" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
 <text x="300" y="800" fill="#FFF8E6" font-size="20">BKC</text><text x="1620" y="800" fill="#FFF8E6" font-size="20" text-anchor="end">SHILPHATA</text>
 <text x="1400" y="232" fill="#FFF8E6" font-size="20" text-anchor="middle">PARSIK HILL</text>
 <g id="p_114" opacity="0"><path d="M1400 250 V 501" stroke="#FFF8E6" stroke-width="2" stroke-dasharray="6 6"/><circle cx="1400" cy="501" r="8" fill="#F5B700"/></g>
 <g id="p_qutub" opacity="0"><path d="M1500 501 L 1512 341 L 1520 341 L 1532 501 Z" fill="rgba(255,248,230,.85)"/><text x="1516" y="325" fill="#FFF8E6" font-size="18" text-anchor="middle">QUTUB MINAR 72.5 m</text></g>
 <text x="1848" y="1030" fill="rgba(255,248,230,.6)" font-size="18" text-anchor="end">DEPTH PROFILE &#183; ILLUSTRATIVE</text>
</svg>"""
_PROF_JS = """
tl.to('#p_tun', {strokeDashoffset: 0, duration: 3.0, ease: 'power2.inOut'}, 17.2);
tl.to('#p_band', {opacity: 1, duration: .6}, 18.0);
tl.to('#p_114', {opacity: 1, duration: .6}, 22.2);
tl.fromTo('#p_qutub', {opacity: 0, y: -30}, {opacity: 1, y: 0, duration: .7, ease: 'power3.out'}, 26.9);
"""

_XS = """<div style="position:absolute;inset:0;background:radial-gradient(90% 80% at 55% 50%,rgba(16,18,22,.8),rgba(8,8,10,.95))"></div>
<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;left:0;top:0" font-family="JetBrains Mono" font-weight="600" letter-spacing=".1em">
 <circle id="x_ring" cx="1260" cy="540" r="243" fill="rgba(90,90,96,.25)" stroke="rgba(255,248,230,.35)" stroke-width="20" opacity="0"/>
 <circle id="x_c" cx="1260" cy="540" r="223" fill="none" stroke="#F5B700" stroke-width="5" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" transform="rotate(-90 1260 540)"/>
 <g id="x_dim" opacity="0"><path d="M1037 540 H 1483" stroke="#FFF8E6" stroke-width="2"/><path d="M1037 525 V 555 M1483 525 V 555" stroke="#FFF8E6" stroke-width="2"/>
  <text x="1260" y="525" fill="#F5B700" font-size="30" text-anchor="middle">13.1 m</text></g>
 <rect id="x_floor" x="1060" y="662" width="400" height="18" fill="rgba(255,248,230,.5)" opacity="0"/>
 <g id="x_tr1" opacity="0"><rect x="1124" y="536" width="112" height="126" rx="22" fill="rgba(127,227,255,.25)" stroke="#7FE3FF" stroke-width="3"/></g>
 <g id="x_tr2" opacity="0"><rect x="1284" y="536" width="112" height="126" rx="22" fill="rgba(127,227,255,.25)" stroke="#7FE3FF" stroke-width="3"/></g>
 <text x="1848" y="1030" fill="rgba(255,248,230,.6)" font-size="18" text-anchor="end">CROSS-SECTION &#183; ILLUSTRATIVE</text>
</svg>"""
_XS_JS = """
tl.to('#x_c', {strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut'}, 31.4);
tl.to('#x_ring', {opacity: 1, duration: .8}, 32.2);
tl.to('#x_dim', {opacity: 1, duration: .5}, 33.7);
tl.to('#x_floor', {opacity: 1, duration: .4}, 36.2);
tl.fromTo('#x_tr1', {opacity: 0, x: 60}, {opacity: 1, x: 0, duration: .8, ease: 'power3.out'}, 36.5);
tl.fromTo('#x_tr2', {opacity: 0, x: -60}, {opacity: 1, x: 0, duration: .8, ease: 'power3.out'}, 37.0);
tl.fromTo('#pg2 svg', {scale: 1}, {scale: 1.8, transformOrigin: '1260px 540px', duration: 4.4, ease: 'power2.in'}, 41.2);
"""

SPEC = dict(
    dur=46.27, chapter='02 &mdash; The route', blur=True, plates=_bg,
    pages=[dict(t=0.0, z=17.2, html=_MAP, js=_MAP_JS), dict(t=16.8, z=31.4, html=_PROF, js=_PROF_JS), dict(t=31.0, z=46.27, html=_XS, js=_XS_JS)],
    beats=[
        dict(kind='hl', t=0.4, z=6.8, pos=(72, 820), tag='The route', lines=['BKC <span class="g">to</span> Shilphata']),
        dict(kind='num', t=7.6, z=14.4, pos=(1848, 140), align='right', label='Tunnel length', to=21, cd=1.3, unit='km', below='Entirely underground'),
        dict(kind='num', t=14.8, z=17.0, pos=(1848, 140), align='right', label='Under Thane Creek', to=7, cd=1.0, unit='km', below='Of the 21 km'),
        dict(kind='hl', t=17.3, z=21.6, pos=(72, 140), tag='Depth', lines=['<span class="g">25&ndash;65 <span class="u">m</span></span> below ground']),
        dict(kind='num', t=21.9, z=26.5, pos=(72, 140), label='Under Parsik hill', to=114, cd=1.3, unit='m', below='Deepest point'),
        dict(kind='hl', t=26.8, z=31.0, pos=(72, 140), lines=['About <span class="box">1.5&times;</span>', 'the Qutub Minar']),
        dict(kind='hl', t=31.4, z=36.0, pos=(72, 400), tag='One tube', lines=['Single tunnel', '&Oslash; <span class="g">13.1 <span class="u">m</span></span>']),
        dict(kind='hl', t=36.3, z=40.7, pos=(72, 400), lines=['Trains in', '<span class="g">both</span> directions']),
        dict(kind='hl', t=41.1, z=46.27, pos=(72, 400), tag='So', lines=['How do you dig this', '<span class="box">under the sea?</span>']),
    ],
)
