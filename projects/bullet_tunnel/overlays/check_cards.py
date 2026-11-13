# For every card beat: real-time window (inverse of the page warp) and its leader track. Fails when the anchor is off frame,
# behind the camera, or the track does not cover the whole window. Usage: python check_cards.py ch3 ch4 ...
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from specs import SPECS
HERE = pathlib.Path(__file__).parent
CH = {'hook': 1, 'ch2': 2, 'ch3': 3, 'ch4': 4, 'ch5': 5, 'ch6': 6, 'ch7': 7}
L = json.load(open(HERE.parent / 'audio' / 'v4_line_times.json'))
def warp_pts(name):
    ls = [l for l in L if l['ch'] == CH[name]]; c0 = 0.0 if CH[name] == 1 else ls[0]['old']; wp = [[0, 0]]
    for l in ls:
        q = [l['start'] - c0, l['old'] - c0]
        if q[0] > wp[-1][0] and q[1] >= wp[-1][1]: wp.append(q)
    return wp
def inv(wp, told):            # page-old-time -> real time
    for a, b in zip(wp, wp[1:]):
        if told <= b[1]: return a[0] + (b[0] - a[0]) * (told - a[1]) / max(1e-9, b[1] - a[1])
    return wp[-1][0] + told - wp[-1][1]
def at(tr, t):
    if isinstance(tr[0], (int, float)): return tr[0], tr[1], 1
    if t < tr[0][0] - 1e-6 or t > tr[-1][0] + 1e-6: return None
    for a, b in zip(tr, tr[1:]):
        if t <= b[0]:
            f = (t - a[0]) / (b[0] - a[0]); return a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f, (a[3] if len(a) > 3 else 1)
    return tr[-1][1], tr[-1][2], (tr[-1][3] if len(tr[-1]) > 3 else 1)
PW = json.load(open(HERE.parent / 'audio' / 'plate_warp.json'))
def pwarp(name, t):
    if not SPECS[name].get('retimed'): return t
    W = PW[str(CH[name])]
    for a, b in zip(W, W[1:]):
        if t <= b[0]: return a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0])
    return W[-1][1]
bad = 0
for name in sys.argv[1:]:
    wp = warp_pts(name)
    for i, b in enumerate(SPECS[name]['beats']):
        if b['kind'] != 'card': continue
        r0, r1 = inv(wp, b['t']), inv(wp, b['z']); probs = []; t = r0
        while t <= r1:
            p = at(b['anchor'], pwarp(name, t))
            if p is None: probs.append(f'no track at {t:.1f}'); break
            x, y, d = p
            if not (0.03 < x < 0.97 and 0.05 < y < 0.95) or d <= 0: probs.append(f'off frame at {t:.1f} ({x:.2f},{y:.2f})'); break
            t += 0.1
        kind = 'TRACK' if not isinstance(b['anchor'][0], (int, float)) else 'STATIC'
        print(f"{name} card{i} {b['title'][:28]:28s} real {r0:5.1f}-{r1:5.1f} {kind:6s} {'OK' if not probs else 'FAIL ' + probs[0]}")
        bad += bool(probs) or kind == 'STATIC'
print('problems (incl. static anchors):', bad)
