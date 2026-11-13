# chapter 3: the machine (global 83.44-130.29 s, 46.85 s). Plate = blender/d_tbm.py (ch3_tbm.mp4). Anchors from job f2bcefc2.
SPEC = dict(
    dur=46.85, chapter='03 &mdash; The machine',
    plates=[('ch3_tbm.mp4', 0.0, 46.85, 0.0)],
    beats=[
        dict(kind='hl', t=0.3, z=6.2, pos=(72, 140), tag='The machine', lines=['Tunnel boring <span class="g">machine</span>'],
             sub='Largest ever on an Indian rail project', sub_t=2.1),
        dict(kind='card', t=6.6, z=10.2, card=(1240, 280), anchor=(0.335, 0.51), title='<b>Cutterhead</b>', desc='The rotating front<br>of the machine'),
        dict(kind='num', t=10.7, z=14.1, pos=(1848, 300), align='right', label='Cutterhead diameter', to=13.6, unit='<span class="u">m</span>', below='Across the face'),
        dict(kind='num', t=14.4, z=17.7, pos=(1848, 300), align='right', label='Cutterhead weight', to=350, unit='<span class="u">t</span>', below='The cutterhead alone'),
        dict(kind='num', t=17.9, z=22.1, pos=(1848, 300), align='right', label='Whole machine', to=96, unit='<span class="u">m</span>', below='Long'),
        dict(kind='num', t=22.3, z=24.6, pos=(72, 300), label='Total weight', to=3200, unit='<span class="u">t</span>', below='About'),
        dict(kind='card', t=24.9, z=28.9, side='left', card=(300, 250), anchor=(0.778, 0.452), title='<b>84</b> disc cutters', desc='Steel discs roll and<br>crush soil and rock'),
        dict(kind='hl', t=29.2, z=34.8, pos=(1848, 140), align='right', tag='Thrust', lines=['Hydraulic <span class="g">jacks</span>', 'push it forward']),
        dict(kind='hl', t=35.1, z=36.9, pos=(1848, 760), align='right', ital=['But here,', 'there is a <span style="color:#F5B700">problem.</span>']),
        dict(kind='hl', t=37.2, z=41.6, pos=(1848, 140), align='right', lines=['Seabed soil is', '<span class="box">wet and soft</span>']),
        dict(kind='hl', t=41.9, z=44.4, pos=(1848, 140), align='right', lines=['And above it,', 'the weight of <span class="g">the sea</span>']),
        dict(kind='hl', t=44.7, z=46.85, pos=(1848, 760), align='right', lines=['The face', '<span class="box">starts to collapse</span>']),
        dict(kind='pill', t=44.8, z=46.85, pos=(1848, 100), align='right', text='Illustrative'),
    ],
)
