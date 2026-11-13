from tracks import tr
# chapter 4: the slurry (global 130.294-184.818 s, 54.52 s). Plate = blender/e_slurry.py (ch4_slurry.mp4, job f7e0a381). Anchors from the ch4 agent.
SPEC = dict(
    dur=54.52, chapter='04 &mdash; The slurry',
    plates=[('ch4_plate.mp4', 0.0, 54.52, 0.0)], retimed=True,
    beats=[
        dict(kind='hl', t=0.3, z=3.4, pos=(72, 140), tag='The real trick', lines=['Not cutting,', 'but <span class="g">holding back</span>'], scrim=True),
        dict(kind='hl', t=3.7, z=6.6, pos=(72, 140), tag='Machine type', lines=['<span class="g">Mixshield</span> TBM'], scrim=True),
        dict(kind='card', t=6.9, z=10.2, side='left', card=(300, 120), anchor=tr('e_slurry', 'chamber'), title='<b>Closed chamber</b>', desc='Right behind<br>the cutterhead'),
        dict(kind='hl', t=10.6, z=13.2, pos=(72, 140), lines=['Filled with', '<span class="g">bentonite slurry</span>'], scrim=True),
        dict(kind='hl', t=13.6, z=16.4, pos=(72, 140), tag='Bentonite', lines=['A special <span class="g">clay</span>']),
        dict(kind='hl', t=16.6, z=19.9, pos=(1848, 140), align='right', lines=['Mixed with water,', 'it turns <span class="box">thick</span>']),
        dict(kind='hl', t=20.3, z=25.3, pos=(1848, 140), align='right', tag='Pressure', lines=['Slurry presses', 'on the <span class="g">face</span>']),
        dict(kind='hl', t=25.8, z=27.5, pos=(1848, 110), align='right', tag='Outside', lines=['The sea pushes in'], scrim=True),
        dict(kind='hl', t=27.7, z=30.6, pos=(1848, 140), align='right', tag='Inside', lines=['The slurry', 'pushes <span class="g">out</span>']),
        dict(kind='hl', t=31.0, z=34.9, pos=(72, 140), tag='Balance', lines=['Equal pressure,', 'the face <span class="box">holds</span>']),
        dict(kind='card', t=35.4, z=38.0, card=(1450, 80), anchor=tr('e_slurry', 'air_cushion'), title='<b>Air cushion</b>', desc='Adjusts the pressure<br>every moment'),
        dict(kind='hl', t=39.2, z=43.0, pos=(72, 140), lines=['Cut soil leaves', 'through <span class="g">pipes</span>']),
        dict(kind='card', t=43.4, z=46.2, side='left', card=(300, 140), anchor=tr('e_slurry', 'cyclones'), title='<b>Separation plant</b>', desc='Takes the soil<br>out of the slurry'),
        dict(kind='hl', t=46.6, z=49.7, pos=(1848, 140), align='right', lines=['Clean slurry', 'goes <span class="g">back in</span>']),
        dict(kind='hl', t=50.0, z=54.52, pos=(72, 140), tag='In short', lines=['A wall of', '<span class="box">liquid</span> ahead']),
    ],
)
