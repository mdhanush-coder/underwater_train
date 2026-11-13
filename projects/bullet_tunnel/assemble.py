# Final film: chapter composites (each has a 0.8 s held tail) laid at their true global starts, 0.6 s dissolves,
# picture only; the sound is audio/final_mix.wav (aarav voice v4 + generated music, ducked, -14 LUFS).
import subprocess, imageio_ffmpeg, pathlib
FF = imageio_ffmpeg.get_ffmpeg_exe(); D = pathlib.Path(__file__).parent
PARTS = [('hook', 0.0), ('ch2', 37.17), ('ch3', 83.44), ('ch4', 130.294), ('ch5', 184.818), ('ch6', 233.903), ('ch7', 275.905)]
END, XF = 310.9, 0.6
cmd = [FF, '-hide_banner', '-y']
for n, _ in PARTS: cmd += ['-i', str(D / 'renders/final_parts' / f'{n}.mp4')]
cmd += ['-i', str(D / 'audio/final_mix.wav')]
fc = ''.join(f'[{i}:v]fps=30,scale=1920:1080,format=yuv420p,setpts=PTS-STARTPTS[v{i}];' for i in range(len(PARTS)))
prev = 'v0'
for i in range(1, len(PARTS)):
    fc += f'[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={PARTS[i][1]:.3f}[x{i}];'; prev = f'x{i}'
fc += f'[{prev}]trim=0:{END},setpts=PTS-STARTPTS,fade=t=out:st={END - 1.2}:d=1.2[vout]'
cmd += ['-filter_complex', fc, '-map', '[vout]', '-map', f'{len(PARTS)}:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-t', str(END), '-movflags', '+faststart',
        str(D / 'renders/bullet_tunnel_FINAL_hinglish.mp4')]
print(' '.join(cmd[:4]), '...'); subprocess.run(cmd, check=True)
