"""Create a separate Bambu project, preserving the original foot mesh.

Four parameter modifiers (not additional printed parts) strengthen screw seats.
Coordinates in the existing 3MF have z=-38..38; the instance adds z=38.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from math import cos, sin, tau
import json
import uuid
import re
import xml.etree.ElementTree as E

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'Standfuss_77mm_D250_Druck.3mf'
OUT = HERE / 'Standfuss_P1S_PETG_HF_230C_8mm_Innenbrim.3mf'
FILAMENT_NAME = 'Bambu PETG HF Schwarz - Standfuss 230C @P1S'
CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
PROD = 'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
BAMBU = 'http://schemas.bambulab.com/package/2021'
E.register_namespace('', CORE)
E.register_namespace('p', PROD)
E.register_namespace('BambuStudio', BAMBU)
def tag(name): return '{'+CORE+'}'+name
def encode(node): return E.tostring(node,encoding='utf-8',xml_declaration=True)

with ZipFile(SOURCE) as z:
    entries = {name:z.read(name) for name in z.namelist()}
settings = json.loads(entries['Metadata/project_settings.config'])
changes = {
    'print_settings_id':'Standfuss PETG HF 0.12mm 5W 15G Innenbrim8',
    'layer_height':'0.12', 'initial_layer_print_height':'0.2',
    'wall_loops':'5', 'sparse_infill_density':'15%', 'sparse_infill_pattern':'gyroid',
    'top_shell_thickness':'1.2', 'bottom_shell_thickness':'1.2',
    'top_shell_layers':'10', 'bottom_shell_layers':'10',
    'outer_wall_speed':['40'], 'outer_wall_acceleration':['1000'],
    'inner_wall_speed':['100'], 'sparse_infill_speed':['150'],
    'internal_solid_infill_speed':['100'], 'top_surface_speed':['30'],
    'top_surface_acceleration':['1000'], 'initial_layer_speed':['20'],
    'initial_layer_infill_speed':['30'],
    'wall_sequence':'inner wall/outer wall', 'seam_position':'aligned',
    'top_surface_pattern':'monotonicline', 'ironing_type':'no ironing',
    'fuzzy_skin':'none', 'brim_type':'inner_only', 'brim_width':'8', 'skirt_loops':'0',
    'enable_support':'1', 'support_type':'normal(auto)', 'support_style':'default',
    'support_threshold_angle':'30', 'support_on_build_plate_only':'0',
    'support_top_z_distance':'0.2', 'support_bottom_z_distance':'0.2',
    'support_interface_top_layers':'2', 'support_interface_bottom_layers':'2',
    'filament_colour':['#161616'],
    'filament_settings_id':[FILAMENT_NAME],
    'nozzle_temperature':['230'],'nozzle_temperature_initial_layer':['230'],
    'textured_plate_temp':['70'],'textured_plate_temp_initial_layer':['70'],
    'close_fan_the_first_x_layers':['3'],'additional_cooling_fan_speed':['0'],
}
assert settings['printer_model'] == 'Bambu Lab P1S'
assert settings['filament_settings_id'] == ['Bambu PETG HF @BBL X1C']
settings.update(changes)
settings['machine_start_gcode'] = re.sub(r'(M106\s+P2\s+S)\d+',r'\g<1>0',settings['machine_start_gcode'])
entries['Metadata/project_settings.config'] = json.dumps(settings,indent=2).encode()

root = E.fromstring(entries['3D/3dmodel.model'])
root.set('xmlns:BambuStudio', BAMBU)
# Stock P1S profile declares a +2 mm Y nozzle offset. Compensate placement
# so the physical first-layer paths stay centered and clear of Y=1.5 purge.
root.find(tag('build')).find(tag('item')).set('transform','1 0 0 0 1 0 0 0 1 128 130 38')
components = root.find(tag('resources')).find(tag('object')).find(tag('components'))
meshes = E.fromstring(entries['3D/Objects/object_1.model'])
meshes.set('xmlns:BambuStudio', BAMBU)
resources = meshes.find(tag('resources'))
original_mesh = E.tostring(resources.find(tag('object')))
config = E.fromstring(entries['Metadata/model_settings.config'])
obj = config.find('object')

for ident,(cx,cy) in enumerate(((56.5,0),(0,56.5),(-56.5,0),(0,-56.5)),3):
    uid = str(uuid.uuid4())
    geom = E.SubElement(resources,tag('object'),{'id':str(ident),'type':'model','{'+PROD+'}UUID':uid})
    mesh = E.SubElement(geom,tag('mesh'))
    verts = E.SubElement(mesh,tag('vertices'))
    n=64
    for z in (28,38):
        for i in range(n):
            a=tau*i/n
            E.SubElement(verts,tag('vertex'),{'x':str(cx+10*cos(a)),'y':str(cy+10*sin(a)),'z':str(z)})
    for z in (28,38): E.SubElement(verts,tag('vertex'),{'x':str(cx),'y':str(cy),'z':str(z)})
    tris=E.SubElement(mesh,tag('triangles'))
    def tri(a,b,c): E.SubElement(tris,tag('triangle'),{'v1':str(a),'v2':str(b),'v3':str(c)})
    for i in range(n):
        j=(i+1)%n
        tri(i,j,n+j);tri(i,n+j,n+i)
        tri(2*n,j,i);tri(2*n+1,n+i,n+j)
    E.SubElement(components,tag('component'),{'{'+PROD+'}path':'/3D/Objects/object_1.model',
        'objectid':str(ident),'{'+PROD+'}UUID':uid,'transform':'1 0 0 0 1 0 0 0 1 0 0 0'})
    part=E.SubElement(obj,'part',{'id':str(ident),'subtype':'modifier_part'})
    for key,value in {'name':f'Schraubensitz {ident-2} - D20 H10 - 100 Prozent',
        'matrix':'1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1',
        'sparse_infill_density':'100%','sparse_infill_pattern':'rectilinear','wall_loops':'6'}.items():
        E.SubElement(part,'metadata',{'key':key,'value':value})
    E.SubElement(part,'mesh_stat',{'face_count':str(4*n),'edges_fixed':'0','degenerate_facets':'0',
        'facets_removed':'0','facets_reversed':'0','backwards_edges':'0'})

assert E.tostring(resources.find(tag('object'))) == original_mesh
entries['3D/3dmodel.model']=encode(root)
entries['3D/Objects/object_1.model']=encode(meshes)
entries['Metadata/model_settings.config']=encode(config)
with ZipFile(OUT,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for name,data in entries.items(): z.writestr(name,data)
profile={**settings,'type':'process','name':changes['print_settings_id'],'from':'User','instantiation':'true'}
(HERE/'P1S_PETG_HF_Standfuss_Innenbrim8.json').write_text(json.dumps(profile,indent=2),encoding='utf-8')
filament={
    'type':'filament','name':FILAMENT_NAME,'from':'User','instantiation':'true',
    'inherits':'Bambu PETG HF @BBL X1C','filament_settings_id':[FILAMENT_NAME],
    'compatible_printers':['Bambu Lab P1S 0.4 nozzle'],
    'nozzle_temperature':['230'],'nozzle_temperature_initial_layer':['230'],
    'textured_plate_temp':['70'],'textured_plate_temp_initial_layer':['70'],
    'close_fan_the_first_x_layers':['3'],'additional_cooling_fan_speed':['0'],
    'filament_colour':['#161616']
}
(HERE/'Bambu_PETG_HF_Schwarz_Standfuss_230C.json').write_text(json.dumps(filament,indent=2),encoding='utf-8')
(HERE/'mcp_slice_request.json').write_text(json.dumps({
    'stl_path':str(OUT),'bambu_model':'p1s','nozzle_diameter':'0.4',
    'slicer_profile':str(HERE/'P1S_PETG_HF_Standfuss_Innenbrim8.json'),
    'load_filaments':str(HERE/'Bambu_PETG_HF_Schwarz_Standfuss_230C.json'),
    'filament_colours':'#161616','arrange':False,'orient':False,'ensure_on_bed':True,
    'slice_plate':1,'min_save':False,'use_printer_filaments':False
},indent=2),encoding='utf-8')
print('Created',OUT)
print('Foot mesh unchanged; four modifier volumes, 100% fill; instance XY 128,130')
