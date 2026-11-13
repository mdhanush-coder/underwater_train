"""python build_mg.py <spec_name>  ->  overlays/<spec_name>/index.html + <spec_name>.zip

One page builder for every chapter of the bullet-tunnel film, in the user's reference style (2026-11-13 board):
gold-dash header + topic, OUTLINED kicker tags, compact Unbounded headlines (52 px) with ONE gold word or a gold
highlight box, gold underline bar, small line icons (pin, calendar, waves), italic Inter statements, boxed number
labels, rounded gold-outlined cards with leader lines. Plates play inside the page (<video>), voice comes as `audio`.
Specs live in specs.py: SPECS[name] = dict(dur, chapter, plates=[(asset, start, dur, media_start)], beats=[...]).
"""
import sys, json, html, pathlib, zipfile
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from specs import SPECS

ICON = {}          # user 2026-11-13: no icons

CSS = """
body{margin:0;background:#000}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#111;color:#FFF8E6;font-family:'Rajdhani','Hind',sans-serif}
.clip{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover}
.mgpage{position:absolute;left:0;top:0;width:1920px;height:1080px}
#topscrim{position:absolute;left:0;top:0;width:1920px;height:150px;background:linear-gradient(180deg,rgba(8,8,10,.55),rgba(8,8,10,0))}
#botscrim{position:absolute;left:0;bottom:0;width:1100px;height:420px;background:radial-gradient(120% 100% at 0% 100%,rgba(8,8,10,.55) 0%,rgba(8,8,10,0) 70%)}
#fx{position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none}
.hdr,.topic{position:absolute;top:44px;font:600 24px 'JetBrains Mono','Hind',monospace;letter-spacing:.1em;text-transform:uppercase;text-shadow:0 2px 12px rgba(0,0,0,.8)}
.hdr{left:72px;display:flex;align-items:center;gap:16px}
.hdr i{display:block;width:52px;height:5px;border-radius:3px;background:#F5B700}
.topic{right:72px;opacity:.85}
.b{position:absolute;visibility:hidden}
.tagbox{display:inline-block;font:600 22px 'JetBrains Mono','Hind',monospace;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border:1.5px solid rgba(245,183,0,.85);border-radius:4px;background:rgba(10,10,12,.35);margin-bottom:12px;text-shadow:0 2px 10px rgba(0,0,0,.6)}
.hl{font:800 52px/1.08 'Unbounded','Hind',sans-serif;letter-spacing:.005em;text-transform:uppercase;text-shadow:0 3px 22px rgba(0,0,0,.7);white-space:nowrap}
.hl .g{color:#F5B700}
.u{text-transform:none !important}
.hl .box{background:#F5B700;color:#121212;padding:0 12px;text-shadow:none;display:inline-block;margin:2px 0}
.it{font:800 italic 46px/1.12 'Inter',sans-serif;letter-spacing:.005em;text-transform:uppercase;text-shadow:0 3px 22px rgba(0,0,0,.7);white-space:nowrap}
.bar{width:110px;height:5px;border-radius:3px;background:#F5B700;margin-top:16px}
.sub{display:flex;align-items:center;gap:10px;margin-top:12px;font:600 28px 'Rajdhani','Hind',sans-serif;letter-spacing:.08em;text-transform:uppercase;text-shadow:0 2px 14px rgba(0,0,0,.75)}
.date{display:flex;align-items:center;gap:16px}
.numb .lab{display:inline-block;font:600 24px 'JetBrains Mono','Hind',monospace;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border:1.5px solid rgba(255,248,230,.55);border-radius:4px;background:rgba(10,10,12,.4)}
.numb .n{font:900 104px/1 'Unbounded','Hind',sans-serif;color:#F5B700;font-variant-numeric:tabular-nums;text-shadow:0 4px 26px rgba(0,0,0,.6);margin:10px 0}
.numb .n small{font-size:58px;color:#FFF8E6;margin-left:8px}
.card{position:absolute;padding:12px 18px;box-sizing:border-box;white-space:nowrap;border:2px solid #F5B700;border-radius:14px;background:rgba(10,10,12,.72);box-shadow:0 8px 28px rgba(0,0,0,.45)}
.card .t{font:700 26px/1.15 'Inter',sans-serif;text-transform:uppercase}
.card .t b{color:#F5B700}
.card .d{font:500 16px/1.35 'JetBrains Mono',monospace;color:#E6E1D6;margin-top:6px;letter-spacing:.06em;text-transform:uppercase}
svg#ld{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
svg#ld polyline{fill:none;stroke:rgba(255,255,255,.9);stroke-width:2}
svg#ld circle.dot{fill:#F5B700}
svg#ld circle.ring{fill:none;stroke:#F5B700;stroke-width:2}
.pill{display:flex;align-items:center;gap:12px;font:600 22px 'JetBrains Mono','Hind',monospace;letter-spacing:.1em;text-transform:uppercase;padding:8px 16px;border:1.5px solid rgba(127,227,255,.8);border-radius:10px;background:rgba(6,30,40,.55)}
"""


def beat_html(i, b):
    k = b['kind']; x, y = b.get('pos', (72, 690))
    style = f"left:{x}px;top:{y}px" if b.get('align', 'left') == 'left' else f"right:{1920 - x}px;top:{y}px;text-align:right"
    inner = ''
    if k == 'hl':
        if b.get('tag'): inner += f'<div class="r"><span class="tagbox">{b["tag"]}</span></div>'
        if b.get('date'): inner += f'<div class="r hl">{b["date"]}</div>'
        for ln in b.get('lines', []): inner += f'<div class="r hl">{ln}</div>'
        for ln in b.get('ital', []): inner += f'<div class="r it">{ln}</div>'
        if b.get('sub'): inner += f'<div class="r sub">{ICON.get(b.get("icon", ""), "")}<span>{b["sub"]}</span></div>'
        if b.get('bar', True): inner += '<div class="r bar"></div>'
    elif k == 'num':
        inner = (f'<div class="r numb"><span class="lab">{b["label"]}</span></div><div class="r numb"><div class="n"><span class="cnt" data-to="{b["to"]}">0</span>'
                 f'<small>{b["unit"]}</small></div></div><div class="r numb"><span class="lab">{b["below"]}</span></div>')
    elif k == 'pill':
        inner = f'<div class="r pill">{ICON.get(b.get("icon", "wave"), "")}<span>{b["text"]}</span></div>'
    elif k == 'card':
        cx, cy = b['card']
        return f'<div class="b co" id="b{i}"><div class="card" style="left:{cx}px;top:{cy}px"><div class="t">{b["title"]}</div><div class="d">{b["desc"]}</div></div></div>'
    return f'<div class="b" id="b{i}" style="{style}">{inner}</div>'


def build(name):
    S = SPECS[name]
    vstyle = ' style="filter:blur(14px) brightness(.45) saturate(.8);transform:scale(1.06)"' if S.get('blur') else ''
    plates = ''.join(f'<video class="clip"{vstyle} src="assets/{a}" data-start="{st:.3f}" data-duration="{d:.3f}" data-media-start="{ms:.3f}" muted playsinline></video>'
                     for a, st, d, ms in S['plates'])
    pages = ''.join(f'<div class="mgpage" id="pg{j}" style="visibility:hidden">{p["html"]}</div>' for j, p in enumerate(S.get('pages', [])))
    beats = ''.join(beat_html(i, b) for i, b in enumerate(S['beats']))
    cards = [(i, b) for i, b in enumerate(S['beats']) if b['kind'] == 'card']
    leaders = ''.join(f'<g id="ld{i}" style="opacity:0"><polyline points=""/><circle class="dot" r="5"/><circle class="ring" r="11"/></g>' for i, _ in cards)
    js_beats = json.dumps([{'i': i, 'k': b['kind'], 't': b['t'], 'z': b['z'], 'sub_t': b.get('sub_t'), 'anchor': b.get('anchor'), 'side': b.get('side', 'right')} for i, b in enumerate(S['beats'])])
    js_pages = json.dumps([{'j': j, 't': p['t'], 'z': p['z']} for j, p in enumerate(S.get('pages', []))])
    page_js = '\n'.join(p.get('js', '') for p in S.get('pages', []))
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@800;900&family=Rajdhani:wght@600;700&family=JetBrains+Mono:wght@500;600&family=Inter:ital,wght@0,500;0,700;0,800;1,800&display=block" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="{name}" data-start="0" data-duration="{S['dur']}" data-width="1920" data-height="1080">
{plates}{pages}<div id="topscrim"></div><div id="botscrim"></div><canvas id="fx" width="1920" height="1080"></canvas>
<svg id="ld" viewBox="0 0 1920 1080">{leaders}</svg>
<div class="hdr" id="hdr"><i></i><span>{S['chapter']}</span></div><div class="topic" id="topic">Mumbai &rarr; Ahmedabad high-speed rail</div>
{beats}
</div>
<script>
window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
window.__hf.buildReady.fonts = Promise.all([document.fonts.load('800 52px "Unbounded"'), document.fonts.load('900 104px "Unbounded"'), document.fonts.load('600 28px "Rajdhani"'),
  document.fonts.load('600 24px "JetBrains Mono"'), document.fonts.load('700 26px "Inter"'), document.fonts.load('italic 800 46px "Inter"')]);
const BEATS = {js_beats}, PAGES = {js_pages};
const tl = gsap.timeline({{paused: true, onUpdate: () => {{ drawFx(tl.time()); drawLeaders(); if (window.pageDraw) window.pageDraw(tl.time()); }}}});
const prog = {{}};
function drawLeaders() {{
  BEATS.filter(b => b.k === 'card').forEach(b => {{
    const el = document.getElementById('b' + b.i), g = document.getElementById('ld' + b.i), card = el.querySelector('.card');
    const vis = getComputedStyle(el).visibility !== 'hidden' && parseFloat(getComputedStyle(el).opacity) > 0.01;
    const cw = card.offsetWidth || 300, ch = card.offsetHeight || 80, cx = parseFloat(card.style.left), cy = parseFloat(card.style.top);
    const left = b.side === 'right';                       // card on the right: leader leaves its left edge
    const sx = left ? cx : cx + cw, sy = cy + ch / 2, ex = left ? sx - 50 : sx + 50;
    const X = b.anchor[0] * 1920, Y = b.anchor[1] * 1080, p = prog[b.i] || 0;
    g.querySelector('polyline').setAttribute('points', [[sx, sy], [ex, sy], [ex + (X - ex) * p, sy + (Y - sy) * p]].map(q => q.join(',')).join(' '));
    g.querySelectorAll('circle').forEach(c => {{ c.setAttribute('cx', X); c.setAttribute('cy', Y); c.style.opacity = p > 0.97 ? 1 : 0; }});
    g.style.opacity = vis ? getComputedStyle(el).opacity : 0;
  }});
}}
const fx = document.getElementById('fx').getContext('2d');
const BK = Array.from({{length: 18}}, () => ({{x: Math.random() * 1920, y: Math.random() * 1080 * 0.7, r: 6 + Math.random() * 20, a: 0.02 + Math.random() * 0.045,
  vx: (Math.random() - 0.5) * 6, vy: -2 - Math.random() * 5, ph: Math.random() * 6.28}}));
function drawFx(t) {{ fx.clearRect(0, 0, 1920, 1080); BK.forEach(b => {{ const x = (b.x + b.vx * t + 1920) % 1920, y = (b.y + b.vy * t + 1080) % 1080, a = b.a * (0.75 + 0.25 * Math.sin(b.ph + t * 0.6));
  const g = fx.createRadialGradient(x, y, 0, x, y, b.r); g.addColorStop(0, `rgba(255,170,60,${{a}})`); g.addColorStop(1, 'rgba(255,170,60,0)'); fx.fillStyle = g; fx.beginPath(); fx.arc(x, y, b.r, 0, 6.2832); fx.fill(); }}); }}
gsap.set(['#hdr', '#topic'], {{autoAlpha: 0}});
tl.fromTo(['#hdr', '#topic'], {{autoAlpha: 0, y: -12}}, {{autoAlpha: 1, y: 0, duration: 0.6, ease: 'power3.out', stagger: 0.1}}, 0.2);
PAGES.forEach(p => {{ const el = '#pg' + p.j; tl.set(el, {{visibility: 'visible'}}, p.t); tl.fromTo(el, {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.8, ease: 'power1.inOut'}}, p.t);
  tl.to(el, {{autoAlpha: 0, duration: 0.8, ease: 'power1.inOut'}}, p.z - 0.8); }});
BEATS.forEach(b => {{
  const el = '#b' + b.i; tl.set(el, {{visibility: 'visible'}}, b.t);
  if (b.k === 'card') {{
    tl.fromTo(el + ' .card', {{autoAlpha: 0, x: 20}}, {{autoAlpha: 1, x: 0, duration: 0.5, ease: 'power3.out'}}, b.t);
    const o = {{p: 0}}; tl.to(o, {{p: 1, duration: 0.55, ease: 'power2.out', onUpdate: () => {{ prog[b.i] = o.p; }}}}, b.t + 0.25);
  }} else {{
    const rs = gsap.utils.toArray(el + ' .r');
    const late = b.sub_t ? rs.filter(r => r.classList.contains('sub')) : [];
    const early = rs.filter(r => !late.includes(r));
    tl.fromTo(early, {{autoAlpha: 0, y: 20}}, {{autoAlpha: 1, y: 0, duration: 0.5, ease: 'power3.out', stagger: 0.1}}, b.t + 0.05);
    if (late.length) {{ gsap.set(late, {{autoAlpha: 0}}); tl.fromTo(late, {{autoAlpha: 0, y: 20}}, {{autoAlpha: 1, y: 0, duration: 0.5, ease: 'power3.out'}}, b.sub_t); }}
    document.querySelectorAll(el + ' .cnt').forEach(c => {{ const o = {{v: 0}}, to = parseFloat(c.dataset.to);
      tl.to(o, {{v: to, duration: 2.6, ease: 'power2.inOut', onUpdate: () => {{ c.textContent = (to % 1 ? o.v.toFixed(1) : Math.round(o.v).toLocaleString('en-IN')); }}}}, b.t + 0.3); }});
  }}
  tl.to(el, {{autoAlpha: 0, duration: 0.4, ease: 'power2.in'}}, b.z - 0.4);
}});
{page_js}
drawFx(0); drawLeaders();
window.__timelines = {{['{name}']: tl}};
</script></body></html>"""
    d = HERE / name; d.mkdir(exist_ok=True)
    (d / 'index.html').write_text(doc, encoding='utf-8')
    with zipfile.ZipFile(HERE / f'{name}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(d / 'index.html', 'index.html')
    print('built', name, len(doc), 'bytes')


if __name__ == '__main__':
    build(sys.argv[1])
