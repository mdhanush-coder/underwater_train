# Leader tracks sampled from the 3D scenes every 0.2 s (old plate time): diag/track/<scene>.json
import json, pathlib
_D = pathlib.Path(__file__).parent.parent / 'diag' / 'track'
def tr(scene, name):
    return [r[:3] for r in json.load(open(_D / f'{scene}.json'))['track'][name]]
