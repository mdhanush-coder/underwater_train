# Smooth plate time-warp per chapter: new (voice v4) chapter time -> old plate time. Speed changes slowly (Gaussian-
# smoothed offsets, slope clamped) so the 3D never visibly lurches; every line's plate moment lands near its new start.
import json, itertools, numpy as np
L = json.load(open('audio/v4_line_times.json'))
S = {1: 0.0, 2: 37.17, 3: 83.44, 4: 130.294, 5: 184.818, 6: 233.903, 7: 275.905}
DUR = {1: 37.4, 2: 46.27, 3: 46.85, 4: 54.52, 5: 49.08, 6: 42.0, 7: 34.6}
SIG, LO, HI, DT = 1.6, 0.75, 1.35, 1 / 30
out = {}
for ch, g in itertools.groupby(L, key=lambda l: l['ch']):
    g = list(g); c0 = S[ch]; D = DUR[ch] + 0.8
    n = np.array([l['start'] - c0 for l in g]); o = np.array([l['old'] - c0 for l in g]); s = o - n
    t = np.arange(0, D + DT / 2, DT)
    w = np.exp(-0.5 * ((t[:, None] - n[None, :]) / SIG) ** 2)
    w0 = 0.0                                                        # no pin: a shifted start just holds the first frame
    sm = (w * s).sum(1) / (w.sum(1) + w0 + 1e-9)
    slope = np.clip(1 + np.gradient(sm, DT), LO, HI)
    f = sm[0] + np.concatenate([[0.0], np.cumsum((slope[1:] + slope[:-1]) / 2 * DT)])
    f = np.clip(f, 0.0, D)                                          # before 0 / past the end = held first / last frame
    res = np.interp(n, t, f) - o
    out[ch] = [[round(float(a), 4), round(float(b), 4)] for a, b in zip(t[::3], f[::3])]
    print(f'ch{ch}: speed {slope.min():.2f}-{slope.max():.2f}x, line error max {np.abs(res).max():.2f}s mean {np.abs(res).mean():.2f}s, f(end)={f[-1]:.2f} vs {D:.2f}')
json.dump(out, open('audio/plate_warp.json', 'w'))
