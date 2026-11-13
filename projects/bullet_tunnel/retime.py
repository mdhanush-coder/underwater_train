# Retime a plate (old shot clock) to the v4 voice: output frame at new time t shows the source frame at f(t)
# (audio/plate_warp.json, smooth, 0.75-1.35x). Nearest frame, H.264 yuv420p, 30 fps. Usage: retime.py in.mp4 out.mp4 ch
import json, sys, av, numpy as np
src, dst, ch = sys.argv[1], sys.argv[2], sys.argv[3]
W = np.array(json.load(open('audio/plate_warp.json'))[ch]); FPS = 30
D = W[-1, 0]; n_out = int(round(D * FPS)) + 1
targets = np.interp(np.arange(n_out) / FPS, W[:, 0], W[:, 1])
ic = av.open(src); ist = ic.streams.video[0]
oc = av.open(dst, 'w'); ost = oc.add_stream('libx264', rate=FPS); ost.width, ost.height = 1920, 1080
ost.pix_fmt = 'yuv420p'; ost.options = {'crf': '16', 'preset': 'medium'}
frames = ic.decode(ist); cur = next(frames); cur_i = 0; nxt = None
for k, tt in enumerate(targets):
    want = int(round(tt * FPS))                   # source frame index (0-based) to show
    while cur_i < want:
        try: cur = next(frames); cur_i += 1
        except StopIteration: break               # past the end: hold the last frame
    img = cur.to_ndarray(format='rgb24')
    if img.shape[1] != 1920: img = np.asarray(cur.to_image().resize((1920, 1080)))
    for p in ost.encode(av.VideoFrame.from_ndarray(img, format='rgb24')): oc.mux(p)
for p in ost.encode(): oc.mux(p)
oc.close(); print('retimed', src, '->', dst, n_out, 'frames')
