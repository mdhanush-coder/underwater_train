"""PRE-FLIGHT for a Pushpaka/XplainedUnseen .blend. Run through blender/script with the .blend as `input` BEFORE any render job.
Every check here exists because of a mistake made earlier (see references/ep001-lessons.md). Exit rule: do not render while any check is FAIL.
Run:  code = exec(compile(open(inputs['preflight.py']).read(), 'preflight', 'exec'), globals())   with args {"expect": {...}} optional.
"""
import bpy, collections

r = result
exp = args.get('expect', {}) if isinstance(args, dict) else {}
checks = []

def chk(name, ok, detail='', level='FAIL'):
    checks.append({'check': name, 'status': 'PASS' if ok else level, 'detail': str(detail)[:300]})

sc = bpy.context.scene

# 1. images must be packed, or a separate render job loses textures/HDRIs (mistake: unpacked temp-folder paths)
unpacked = [i.name for i in bpy.data.images if i.source == 'FILE' and not i.packed_file]
chk('images packed', not unpacked, unpacked[:8])

# 2. no volume emission on cloud materials (mistake: emission accumulated through thickness and blew the floor out)
bad = []
for m in bpy.data.materials:
    if m.node_tree:
        for n in m.node_tree.nodes:
            if n.bl_idname == 'ShaderNodeVolumePrincipled' and 'Emission Strength' in n.inputs and n.inputs['Emission Strength'].default_value > 0.01:
                bad.append((m.name, round(n.inputs['Emission Strength'].default_value, 4)))
chk('no strong volume emission', not bad, bad)

# 3. photo sky must be world-projected, not a plane with edges (mistake: visible plane edge)
planes = [o.name for o in bpy.data.objects if 'PLATE' in o.name.upper()]
chk('no sky-plate plane in scene', not planes, planes)
w = sc.world; ok_world = False; detail = 'no world'
if w and w.node_tree:
    types = [n.bl_idname for n in w.node_tree.nodes]
    mirror = [n for n in w.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage' and n.extension == 'MIRROR']
    ok_world = 'ShaderNodeLightPath' in types and bool(mirror)
    detail = {'light_path': 'ShaderNodeLightPath' in types, 'mirror_image': bool(mirror)}
chk('world: camera-only photo sky (Light Path + Mirror image)', ok_world, detail)
fade = bool(w and w.node_tree and any(n.bl_idname=='ShaderNodeMath' and n.operation=='ABSOLUTE' for n in w.node_tree.nodes))
chk('world: photo fades to the HDRI outside its azimuth (no streaked void when the camera looks away)', fade, fade)

# 4. the ornamental wings are never animated (user rule: no flapping)
wing_anim = []
for o in bpy.data.objects:
    if o.type == 'MESH' and any(s.material and s.material.name == 'wings' for s in o.material_slots):
        p = o
        while p and p.name not in ('PUSHPAK_SCALE', 'PUSHPAK_RIG_ROOT'):   # whole-vehicle hover/turn is intended; only the wing's OWN chain matters
            if p.animation_data and (p.animation_data.action or p.animation_data.drivers):
                wing_anim.append(p.name)
            p = p.parent
chk('wings have no animation or drivers up their parent chain', not wing_anim, sorted(set(wing_anim))[:6])

# 5. hero geometry preserved: mesh count and vertex total of the original asset (446157 verts, 316 meshes)
hero = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.endswith(('_gold_0', '_wings_0', '_flag_0', '_lambert11_0', '_steps_0', '_throne_seat_01_0')) or (o.type == 'MESH' and o.name.startswith('pasted__'))]
hero_all = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.users and o.parent is not None and 'CLOUD' not in o.name and 'PLATE' not in o.name]
verts = sum(len(o.data.vertices) for o in hero_all)
chk('hero vertex total unchanged (446157)', verts == exp.get('hero_verts', 446157), {'meshes': len(hero_all), 'verts': verts})

# 6. scene timing and cameras
chk('fps 24', sc.render.fps == 24, sc.render.fps)
chk('frame_step 1', sc.frame_step == 1, sc.frame_step)
mk = list(sc.timeline_markers)
chk('timeline markers bind cameras', bool(mk) and all(m.camera for m in mk), [(m.name, bool(m.camera)) for m in mk][:8])
chk('frame range matches master timeline', (sc.frame_start, sc.frame_end) == tuple(exp.get('range', (1, 744))), (sc.frame_start, sc.frame_end), level='WARN')

# 7. no render overrides left on
chk('no material override left on', bpy.context.view_layer.material_override is None, bpy.context.view_layer.material_override)

# 8. colour management and engine
chk('AgX view transform', sc.view_settings.view_transform == 'AgX', sc.view_settings.view_transform)
sc.frame_set(sc.frame_end)   # exposure is keyed from black in the opening shot; judge the held value
chk('exposure set for bright HDRI (<= -1)', sc.view_settings.exposure <= -1.0, sc.view_settings.exposure, level='WARN')

# 9. materials: every hero material has image textures where promised (mistake class: flat colours instead of scans)
tex = {m.name: sum(1 for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage') for m in bpy.data.materials if m.node_tree and m.name in ('gold', 'lambert11', 'throne_seat_01', 'flag', 'steps')}
chk('hero materials carry scanned textures', all(v >= 2 for v in tex.values()) and bool(tex), tex)

# 10. scale and root rig exist (non-destructive scale)
chk('PUSHPAK_SCALE and RIG_ROOT exist', 'PUSHPAK_SCALE' in bpy.data.objects and 'PUSHPAK_RIG_ROOT' in bpy.data.objects)

# 11. volumes expensive: warn on many volume objects (towers cost 6x per frame)
vols = [o.name for o in bpy.data.objects if o.type == 'MESH' and o.material_slots and o.material_slots[0].material and o.material_slots[0].material.node_tree and any(n.bl_idname == 'ShaderNodeVolumePrincipled' for n in o.material_slots[0].material.node_tree.nodes)]
chk('few volume objects (cost)', len(vols) <= 4, vols, level='WARN')

fails = [c for c in checks if c['status'] == 'FAIL']
warns = [c for c in checks if c['status'] == 'WARN']
r['verdict'] = 'BLOCK: fix FAIL items before rendering' if fails else ('OK with warnings' if warns else 'OK')
r['fail'] = [c['check'] for c in fails]
r['warn'] = [c['check'] for c in warns]
r['checks'] = checks
