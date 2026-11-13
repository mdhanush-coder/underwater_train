# v3 = v2 take + retakes spliced at line boundaries (inside the 250 ms line gaps), 10 ms fades on each inserted piece.
# Each entry: (base start s, base end s) of v2 lines to replace -> (retake file, start s, end s).
import wave, array
def load(p):
    w = wave.open(p); assert w.getsampwidth() == 2; return w.getparams(), array.array('h', w.readframes(w.getnframes()))
P, base = load('audio/vo_v2_raw.wav'); ch, sr = P.nchannels, P.framerate
FIX = [((43.337, 49.797), ('audio/retake_l10_l54.wav', 0.0, 5.51)),       # v2 lines 14+15 -> v1 retake "twenty-one ... ज़मीन के अंदर है"
       ((135.668, 137.758), ('audio/retake_v2_4lines.wav', 3.344, 5.344)),  # mix shield
       ((158.924, 162.864), ('audio/retake_v2_4lines.wav', 5.994, 8.924)),  # अंदर से, slurry
       ((270.303, 274.333), ('audio/retake_v2_sept.wav', 0.0, 3.75))]       # September two thousand twenty-five में
def cut(a, t0, t1): return array.array('h', a[int(t0*sr)*ch:int(t1*sr)*ch])
def fade(a, n=int(0.01*44100)):
    n *= ch
    for i in range(min(n, len(a)//2)): a[i] = a[i]*i//n; a[-1-i] = a[-1-i]*i//n
    return a
out, t = array.array('h'), 0.0
for (b0, b1), (f, r0, r1) in FIX:
    Pr, r = load(f); assert (Pr.nchannels, Pr.framerate) == (ch, sr)
    out += cut(base, t, b0); out += fade(cut(r, r0, r1)); t = b1
out += cut(base, t, 1e9)
w = wave.open('audio/vo_hinglish_arnav_v3.wav', 'wb'); w.setparams(P); w.writeframes(out.tobytes()); w.close()
print('v3 seconds', round(len(out)/ch/sr, 2))
