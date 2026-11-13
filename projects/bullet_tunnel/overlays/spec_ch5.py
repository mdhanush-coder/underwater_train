# chapter 5: the lining (global 184.818-233.903 s, 49.08 s). Plate = blender/f_rings.py (ch5_rings.mp4). Anchors from the ch5 agent preview.
SPEC = dict(
    dur=49.08, chapter='05 &mdash; The lining',
    plates=[('ch5_rings.mp4', 0.0, 49.08, 0.0)],
    beats=[
        dict(kind='hl', t=0.3, z=3.6, pos=(72, 140), tag='The lining', lines=['Where do the', 'tunnel <span class="g">walls</span> come from?']),
        dict(kind='card', t=4.1, z=7.8, card=(1300, 200), anchor=[[1.8, 0.363, 0.327], [5.5, 0.289, 0.652]], title='<b>Erector</b>', desc='Robotic arm that<br>places the lining'),
        dict(kind='hl', t=8.1, z=10.6, pos=(1848, 140), align='right', lines=['It lifts curved', '<span class="g">concrete</span> pieces']),
        dict(kind='card', t=10.9, z=14.4, card=(1300, 200), anchor=[[9.0, 0.481, 0.583], [12.5, 0.468, 0.586], [15.8, 0.508, 0.481]], title='<b>Segment</b>', desc='Precast concrete<br>lining piece'),
        dict(kind='hl', t=14.8, z=17.4, pos=(1848, 140), align='right', tag='Each segment', lines=['<span class="g">2 <span class="u">m</span></span> wide', '0.5 <span class="u">m</span> thick']),
        dict(kind='hl', t=17.8, z=21.8, pos=(72, 140), tag='One ring', lines=['<span class="g">9 + 1</span>', 'segments']),
        dict(kind='hl', t=22.1, z=27.0, pos=(72, 140), lines=['The key segment', 'goes in <span class="box">last</span>']),
        dict(kind='hl', t=27.3, z=29.8, pos=(72, 140), tag='Thrust', lines=['Jacks push on', 'the <span class="g">new ring</span>']),
        dict(kind='hl', t=30.2, z=34.2, pos=(72, 820), lines=['The machine moves', '<span class="g">one ring</span> ahead']),
        dict(kind='card', t=34.6, z=36.5, side='left', card=(300, 250), anchor=(0.617, 0.518), title='<b>Grout</b>', desc='Fills the gap<br>behind the ring'),
        dict(kind='hl', t=36.8, z=39.6, pos=(72, 140), lines=['Water stops', 'at the <span class="g">grout</span>']),
        dict(kind='hl', t=40.0, z=42.3, pos=(72, 140), lines=['Repeated', '<span class="g">thousands</span> of times']),
        dict(kind='num', t=42.9, z=49.08, pos=(72, 140), label='Segments for this tunnel', to=77000, unit='', below='About', cd=1.6),
    ],
)
