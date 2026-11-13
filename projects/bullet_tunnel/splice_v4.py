# v4 = aarav take (chips recipe) laid onto the v3 shot clock: each chapter keeps its start/length (plates are fixed),
# lines go at their old start or right after the previous line; a chapter that would overrun is sped up (WSOLA, pitch kept).
import json, wave, itertools, numpy as np
SR = 44100
def wsola(x, f, win=1024, hop=256, tol=256):
    if abs(f - 1) < 1e-3: return x.copy()
    w = np.hanning(win); n_out = int(len(x) / f); out = np.zeros(n_out + win); norm = np.zeros(n_out + win)
    prev = 0; k = 0
    while k * hop + win < n_out:
        a = int(k * hop * f)
        if k == 0: best = a
        else:
            nat = prev + hop; tmpl = x[nat:nat + win] if nat + win <= len(x) else None
            lo, hi = max(0, a - tol), min(len(x) - win, a + tol)
            if tmpl is None or hi <= lo: break
            seg = x[lo:hi + win]; c = np.correlate(seg, tmpl, 'valid'); best = lo + int(np.argmax(c))
        if best + win > len(x): break
        out[k*hop:k*hop+win] += x[best:best+win] * w; norm[k*hop:k*hop+win] += w; prev = best; k += 1
    norm[norm < 1e-3] = 1; return (out / norm)[:n_out]
w = wave.open('audio/vo_aarav_v4_raw.wav'); assert w.getnchannels() == 1 and w.getframerate() == SR
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64)
S = json.load(open('shots.json', encoding='utf-8')); L = json.load(open('audio/aarav_v4_lines.json'))
END = 310.5; GAP = 0.15
wr = wave.open('audio/aarav_retake_21_39_40_52.wav'); xr = np.frombuffer(wr.readframes(wr.getnframes()), np.int16).astype(np.float64)
RETAKE = {20: (0, 3.37), 38: (4.02, 7.224), 39: (7.474, 10.168), 51: (10.818, 14.951)}   # 0-based line -> retake span (lines 21, 39, 40, 52)
def piece(i, f):
    src, (a, b) = (xr, RETAKE[i]) if i in RETAKE else (x, L[i]); seg = src[max(0, int((a - 0.03) * SR)):int((b + 0.06) * SR)]
    return wsola(seg, f)
out = np.zeros(int(END * SR) + 3 * SR); new = []; F = 1.04; t = None
for ch, g in itertools.groupby(range(83), key=lambda i: S[i]['ch']):
    g = list(g); c0 = S[g[0]]['start']; c1 = S[g[-1] + 1]['start'] if g[-1] < 82 else END
    gap = 0.12 if ch == 1 else GAP
    for k, i in enumerate(g):
        p = piece(i, F)
        if k == 0: s0 = c0 if t is None else max(c0, t + 0.4)
        else: s0 = max(S[i]['start'] - 1.5, t + gap)
        n = int(s0 * SR); out[n:n + len(p)] += p; t = s0 + len(p) / SR
        new.append(dict(n=i + 1, ch=ch, start=round(s0, 3), end=round(t, 3), old=S[i]['start']))
    print('ch', ch, 'ends', round(t, 2), 'slot end', round(c1, 2), 'max |shift|', round(max(abs(d['start'] - d['old']) for d in new if d['ch'] == ch), 2))
out = np.clip(out[:int(max(END, t + 0.5) * SR)], -32768, 32767).astype(np.int16)
o = wave.open('audio/vo_hinglish_aarav_v4.wav', 'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(out.tobytes()); o.close()
json.dump(new, open('audio/v4_line_times.json', 'w'), indent=0)
print('written', len(out) / SR, 's')
