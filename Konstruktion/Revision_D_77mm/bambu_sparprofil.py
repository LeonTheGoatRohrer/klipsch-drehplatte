"""Sliced comparisons for <=300 g, approximately 6.5 h; no geometry change."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,sys

H=Path(__file__).resolve().parent
variant=sys.argv[1] if len(sys.argv)>1 else '020_3W_8A'
variants={
 '020_3W_8A':('0.20','3','8%','4'),
 '024_3W_6A':('0.24','3','6%','4'),
 '020_3W_8P':('0.20','3','8%','4'),
 '020_3W_6P':('0.20','3','6%','4'),
}
layer,walls,infill,shell_layers=variants[variant]
stem='Standfuss_P1S_PETG_HF_Spar_'+variant
src=H/'Standfuss_P1S_PETG_HF_230C_8mm_Innenbrim.3mf'
out=H/(stem+'.3mf')
with ZipFile(src) as z:entries={n:z.read(n) for n in z.namelist()}
s=json.loads(entries['Metadata/project_settings.config'])
s.update({
 'print_settings_id':'Standfuss Spar '+variant,'layer_height':layer,'wall_loops':walls,
 'sparse_infill_density':infill,'sparse_infill_pattern':'adaptivecubic',
 'top_shell_thickness':'0.8','bottom_shell_thickness':'0.8',
 'top_shell_layers':shell_layers,'bottom_shell_layers':shell_layers,
 'outer_wall_speed':['100'],'outer_wall_acceleration':['2500'],
 'inner_wall_speed':['230'],'sparse_infill_speed':['230'],
 'internal_solid_infill_speed':['160'],'top_surface_speed':['50'],
 'support_speed':['150'],'support_interface_speed':['60'],
 'independent_support_layer_height':'0',
})
if variant in ('020_3W_8P','020_3W_6P'):
 s.update({'ensure_vertical_shell_thickness':'partial','outer_wall_speed':['120'],
           'support_base_pattern_spacing':'3','independent_support_layer_height':'0'})
if variant=='020_3W_6P':
 s.update({'outer_wall_speed':['140'],'inner_wall_speed':['250'],
           'sparse_infill_speed':['250'],'internal_solid_infill_speed':['180']})
assert s['nozzle_temperature']==['230'] and s['close_fan_the_first_x_layers']==['3']
assert s['brim_type']=='inner_only' and s['brim_width']=='8'
entries['Metadata/project_settings.config']=json.dumps(s,indent=2).encode()
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in entries.items():z.writestr(n,b)
profile={**s,'type':'process','name':s['print_settings_id'],'from':'User','instantiation':'true'}
profile_path=H/(stem+'.json')
profile_path.write_text(json.dumps(profile,indent=2),encoding='utf-8')
request={
 'stl_path':str(out),'bambu_model':'p1s','nozzle_diameter':'0.4',
 'slicer_profile':str(profile_path),'load_filaments':str(H/'Bambu_PETG_HF_Schwarz_Standfuss_230C.json'),
 'filament_colours':'#161616','arrange':False,'orient':False,'ensure_on_bed':True,
 'slice_plate':1,'use_printer_filaments':False,
}
(H/(stem+'_request.json')).write_text(json.dumps(request,indent=2),encoding='utf-8')
print('Prepared',out)
