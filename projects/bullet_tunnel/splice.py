# Splice retakes into the v1 voice: line 10 whole; line 54 only "यानी ADIT" (orig "काम ... गई" kept, retake misread "काम").
import wave, array
def load(p):
    w = wave.open(p); assert w.getsampwidth() == 2; a = array.array('h', w.readframes(w.getnframes())); return w.getparams(), a
P, orig = load('audio/vo_hinglish_arnav_v1.wav'); P2, re_ = load('audio/retake_l10_l54.wav')
assert (P.nchannels, P.framerate) == (P2.nchannels, P2.framerate), (P, P2)
ch, sr = P.nchannels, P.framerate
def cut(a, t0, t1): return a[int(t0*sr)*ch:int(t1*sr)*ch]
def fade(a, ms=10):
    n = int(sr*ms/1000)*ch; a = array.array('h', a)
    for i in range(min(n, len(a))): a[i] = int(a[i]*i/n); a[-1-i] = int(a[-1-i]*i/n)
    return a
parts = [cut(orig, 0, 48.836), fade(cut(re_, 0, 5.51)), fade(cut(orig, 53.726, 268.722)),
         fade(cut(re_, 9.70, 11.45)), cut(orig, 269.577, 1e9)]
out = array.array('h'); [out.extend(p) for p in parts]
w = wave.open('audio/vo_hinglish_arnav_v1_spliced.wav', 'wb'); w.setparams(P); w.writeframes(out.tobytes()); w.close()
print('v2 seconds', round(len(out)/ch/sr, 2))
