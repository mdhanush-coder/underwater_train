import json, sys, os
a = sys.argv[sys.argv.index('--') + 1:]; job, outjson = a[0], a[1]
out = os.path.dirname(outjson)
g = {'args': {'mode': 'track', 'pct': 25}, 'out': out, 'result': {}, 'inputs': {}, '__name__': '__main__'}
try:
    exec(open(job, encoding='utf-8').read(), g)
except SystemExit:
    pass
json.dump(g['result'], open(outjson, 'w'))
print('WROTE', outjson, list(g['result'].get('track', {}).keys()))
