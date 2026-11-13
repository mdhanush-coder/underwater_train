# Chapter specs for build_mg.py. Times in seconds of the chapter (hook = global time). English only, one gold item per beat, no icons.
SPECS = {}

SPECS['hook'] = dict(
    dur=37.4, chapter='01 &mdash; The sea tunnel',
    plates=[('transition.mp4', 0.0, 37.4, 0.0)],
    beats=[
        dict(kind='hl', t=0.5, z=5.4, pos=(72, 730), tag='The day it started', date='05 July <span class="g">2026</span>', sub='Vikhroli, Mumbai', sub_t=3.0),
        dict(kind='num', t=6.3, z=11.0, pos=(1848, 140), align='right', label='Shaft depth', to=56, unit='m', below='Below ground'),
        dict(kind='card', t=12.0, z=14.8, card=(1400, 190), anchor=(0.435, 0.50), title='Cutterhead <b>&Oslash; 13.6 <span class="u">m</span></b>', desc='Largest ever used for<br>a rail tunnel in India'),
        dict(kind='card', t=12.9, z=14.8, card=(1400, 340), anchor=(0.50, 0.37), title='<b>84</b> disc cutters', desc='Rolling steel discs<br>that crush rock'),
        dict(kind='card', t=13.7, z=14.8, card=(1400, 490), anchor=(0.575, 0.66), title='<b>350 t</b>', desc='The cutterhead alone'),
        dict(kind='hl', t=15.2, z=19.2, pos=(72, 760), tag='Mumbai', lines=['Thane <span class="g">creek</span>']),
        dict(kind='hl', t=19.7, z=22.6, pos=(72, 770), ital=['From above,', 'it looks <span style="color:#F5B700">ordinary.</span>']),
        dict(kind='hl', t=22.8, z=26.0, pos=(72, 760), lines=['But under the water', '<span class="box">a railway</span> is being built']),
        dict(kind='hl', t=26.9, z=30.6, pos=(72, 140), tag='Schematic cutaway &middot; illustrative', lines=["India's first", '<span class="g">undersea</span> rail tunnel']),
        dict(kind='hl', t=32.0, z=37.4, pos=(72, 700), tag='The question', lines=["Why doesn't", '<span class="box">the water</span>', 'flood the tunnel?']),
        dict(kind='pill', t=32.6, z=37.4, pos=(1848, 100), align='right', text='Sea pressure on the tunnel'),
    ],
)

from spec_ch2 import SPEC as _c2
SPECS["ch2"] = _c2

from spec_ch3 import SPEC as _c3
SPECS["ch3"] = _c3
