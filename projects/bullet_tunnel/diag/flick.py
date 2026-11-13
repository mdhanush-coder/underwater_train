# Flicker check: per 8x6 grid cell, count frames where the cell's brightness flips up/down vs both neighbours by > T.
import av, numpy as np, sys
for fn in sys.argv[1:]:
    c=av.open(fn); s=c.streams.video[0]; M=[]
    for f in c.decode(s):
        g=f.to_ndarray(format='gray').astype(np.float32); H,W=g.shape
        M.append(g[:H//6*6,:W//8*8].reshape(6,H//6,8,W//8).mean(axis=(1,3)))
    M=np.array(M); a=M[1:-1]-M[:-2]; b=M[1:-1]-M[2:]
    spike=((a>3)&(b>3))|((a<-3)&(b<-3))           # a cell jumps and comes back next frame
    per_t=spike.reshape(len(spike),-1).sum(axis=1)
    bad=np.where(per_t>=2)[0]
    secs=sorted(set(int((i+1)/30) for i in bad))
    print(f"{fn}: {len(M)} frames, flicker frames {len(bad)} ({100*len(bad)/len(M):.1f}%), seconds: {secs[:40]}")
