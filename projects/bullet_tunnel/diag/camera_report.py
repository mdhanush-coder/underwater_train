# Camera trajectory report (Blender coords, metres). Pitch < 0 = looking down; horizon leaves a 28 mm frame below pitch ~ -21 deg.
import math, sys
OLD = [(0.0, (-96, -150, 2.8), (-10, -40, 1.2)), (4.5, (-40, -92, 3.6), (10, -20, 1.5)), (5.0, (-36, -96, 6.5), (6, -10, 2.0)),
       (7.6, (-10, -210, 92), (0, 60, 0)), (8.4, (0, -140, 82), (0, -60, 0)), (9.6, (0, -78, 10), (0, -40, -4)), (10.3, (0, -70, -14), (0, 0, -30))]
NEW = [(0.0, (-130, -270, 4.0), (0, 800, 35)), (4.5, (-75, -190, 5.0), (10, 800, 38)), (8.0, (-45, -175, 30.0), (0, 800, 20)),
       (11.5, (-10, -105, 1.6), (0, 800, 25)), (12.5, (-6, -95, 1.2), (0, 800, 25))]
def rep(name, P, lens=28.0):
    vfov = 2 * math.degrees(math.atan(12 / lens))
    print(f'\n{name}  (lens {lens} mm, vertical FOV {vfov:.1f} deg)')
    print(' t s |   camera x,y,z     | pitch | yaw  | speed to next m/s | horizon in frame')
    for i, (t, c, l) in enumerate(P):
        d = [l[k] - c[k] for k in range(3)]; hd = math.hypot(d[0], d[1])
        pitch = math.degrees(math.atan2(d[2], hd)); yaw = math.degrees(math.atan2(d[0], d[1]))
        sp = ''
        if i + 1 < len(P):
            t2, c2, _ = P[i + 1]; sp = f'{math.dist(c, c2) / (t2 - t):6.1f}'
        hz = 'yes' if abs(pitch) < vfov / 2 else 'NO'
        under = '  BELOW WATER' if c[2] < 0 else ''
        print(f'{t:4.1f} | {c[0]:6.0f},{c[1]:6.0f},{c[2]:5.1f} | {pitch:5.1f} | {yaw:5.1f} | {sp:>17} | {hz}{under}')
rep('CURRENT PATH (v1)', OLD); rep('REDESIGNED PATH (v2)', NEW, 28.0)
