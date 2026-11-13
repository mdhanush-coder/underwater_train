import inspect, unreal
r = {}
for n in ('shape', 'plain_material', 'environment', 'light', 'sky_light', 'post_process', 'camera', 'import_model', 'look_at', 'setp', 'colour', 'new_sequence', 'animate_camera', 'still', 'group', 'fit_stage', 'clear_view'):
    try: r[n] = str(inspect.signature(getattr(ex, n)))
    except Exception as e: r[n] = 'ERR ' + str(e)[:60]
try: r['film'] = str(inspect.signature(film))
except Exception as e: r['film'] = 'ERR'
try: r['environments'] = list(ex.ENVIRONMENTS) if not isinstance(ex.ENVIRONMENTS, dict) else list(ex.ENVIRONMENTS.keys())
except Exception as e: r['environments'] = 'ERR'
try: r['quality'] = list(ex.QUALITY) if not isinstance(ex.QUALITY, dict) else {k: v for k, v in list(ex.QUALITY.items())[:6]}
except Exception as e: r['quality'] = 'ERR'
try: r['resolutions'] = ex.RESOLUTIONS if isinstance(ex.RESOLUTIONS, (list, dict, tuple)) else str(ex.RESOLUTIONS)
except Exception: r['resolutions'] = 'ERR'
try: r['plain'] = str(ex.PLAIN)
except Exception: pass
result.update(r)
