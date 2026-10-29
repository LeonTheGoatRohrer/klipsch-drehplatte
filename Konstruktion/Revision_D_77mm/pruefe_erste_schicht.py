"""Review the actual sliced first layer and enforce requested auxiliary fan OFF.

No printer connection or print command. The change only switches P2 fan to zero.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from collections import defaultdict
from math import atan2, hypot, pi, cos, sin, ceil
import hashlib, json, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Circle

H=Path(__file__).resolve().parent
P=H/(sys.argv[1] if len(sys.argv)>1 else 'Standfuss_P1S_PETG_HF_230C_8mm_Innenbrim_sliced.3mf')
suffix='_'+sys.argv[2] if len(sys.argv)>2 else ''
with ZipFile(P) as z: entries={n:z.read(n) for n in z.namelist()}
g=entries['Metadata/plate_1.gcode'].decode()
# MCP deliberately restores the stock P1S machine preset. Its start routine
# briefly starts P2, so switch these two startup commands off as requested.
g,changes=re.subn(r'(?m)^(M106\s+P2\s+S)(?!0(?:\s|$))\d+',r'\g<1>0',g)
entries['Metadata/plate_1.gcode']=g.encode()
entries['Metadata/plate_1.gcode.md5']=hashlib.md5(g.encode()).hexdigest().encode()
s=json.loads(entries['Metadata/project_settings.config'])
s['machine_start_gcode']=re.sub(r'(M106\s+P2\s+S)\d+',r'\g<1>0',s['machine_start_gcode'])
entries['Metadata/project_settings.config']=json.dumps(s,indent=2).encode()
tmp=P.with_suffix('.checked.3mf')
with ZipFile(tmp,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in entries.items():z.writestr(n,b)
tmp.replace(P)
assert s['nozzle_temperature']==['230'] and s['nozzle_temperature_initial_layer']==['230']
assert s['textured_plate_temp']==['70'] and s['textured_plate_temp_initial_layer']==['70']
assert s['close_fan_the_first_x_layers']==['3']
assert s['filament_max_volumetric_speed']==['21']
assert s['filament_flow_ratio']==['0.95'] # still uncalibrated stock value
assert s['brim_type']=='inner_only' and s['brim_width']=='8'
assert not re.search(r'(?m)^M106\s+P2\s+S(?:[1-9]\d*)',g)
layers=g.split('; CHANGE_LAYER\n')[1:]
for i,chunk in enumerate(layers[:3],1):
    for line in chunk.splitlines():
        if line.startswith('M106'):
            p=re.search(r'\bP(\d+)',line);v=re.search(r'\bS(\d+)',line)
            if (not p or p.group(1)=='1') and v:assert int(v.group(1))==0,(i,line)
body='; CHANGE_LAYER\n'+g.split('; CHANGE_LAYER\n',1)[1]
assert not re.search(r'(?m)^M10[49]\s+S(?!230(?:\s|$)|0(?:\s|$))\d+',body)

paths=defaultdict(list);speeds=defaultdict(set)
x=y=0.;feed=0.;feature='Unbekannt'
first=layers[0]
for line in first.splitlines():
    if line.startswith('; FEATURE:'):feature=line.split(':',1)[1].strip()
    code=line.split(';',1)[0].strip()
    match=re.match(r'^G([0123])\b',code)
    if not match:continue
    values={k:float(v) for k,v in re.findall(r'([XYZEFI J])\s*(-?\d*\.?\d+)',code)}
    feed=values.get('F',feed)
    nx,ny=values.get('X',x),values.get('Y',y)
    if values.get('E',0)>0 and ('X' in values or 'Y' in values):
        if match.group(1) in ('2','3') and ('I' in values or 'J' in values):
            cx,cy=x+values.get('I',0),y+values.get('J',0)
            r=hypot(x-cx,y-cy);a=atan2(y-cy,x-cx);b=atan2(ny-cy,nx-cx)
            sweep=(b-a)%(2*pi) if match.group(1)=='3' else -((a-b)%(2*pi))
            if abs(sweep)<1e-8:sweep=2*pi if match.group(1)=='3' else -2*pi
            n=max(2,ceil(abs(sweep)/(pi/90)))
            pts=[(cx+r*cos(a+sweep*j/n),cy+r*sin(a+sweep*j/n)) for j in range(n+1)]
            paths[feature].extend(zip(pts[:-1],pts[1:]))
        elif hypot(nx-x,ny-y)>1e-8:paths[feature].append(((x,y),(nx,ny)))
        speeds[feature].add(round(feed/60,3))
    x,y=nx,ny
allpts=[p for group in paths.values() for segment in group for p in segment]
bounds=[min(p[0] for p in allpts),min(p[1] for p in allpts),max(p[0] for p in allpts),max(p[1] for p in allpts)]
assert min(bounds[:2])>=0 and max(bounds[2:])<=256
assert bounds[1]>=2.25,'First layer too close to P1S Y=1.5 startup purge line'
assert speeds['Outer wall'] and max(speeds['Outer wall'])<=25
for feature in ('Bottom surface','Internal solid infill','Sparse infill'):
    if speeds[feature]:assert max(speeds[feature])<=40,(feature,speeds[feature])
assert any('Skirt' in k or 'Brim' in k for k in paths),'Brim paths absent'
fig,ax=plt.subplots(figsize=(10,10),dpi=160)
ax.add_patch(Rectangle((0,0),256,256,facecolor='#f3f5f7',edgecolor='#444',linewidth=1))
ax.add_patch(Rectangle((0,0),18,28,facecolor='#f3bbbb',edgecolor='#a33',label='Sperrbereich'))
ax.add_patch(Circle((128,128),125,fill=False,edgecolor='#777',linestyle='--',linewidth=.7,label='Bauteil Ø250'))
palette={'Outer wall':'#084c91','Inner wall':'#348ac4','Bottom surface':'#4caa88',
    'Internal solid infill':'#4caa88','Support':'#cc6b39','Support interface':'#aa4c20','Skirt':'#af2595','Brim':'#af2595'}
labels={'Outer wall':'Außenkontur','Inner wall':'Innenkonturen','Bottom surface':'Bodenfüllung',
    'Internal solid infill':'Massive Füllung','Support':'Stützen','Support interface':'Stützschnittstelle','Skirt':'Innenbrim','Brim':'Innenbrim'}
for feature,segments in paths.items():
    if segments:ax.add_collection(LineCollection(segments,colors=palette.get(feature,'#888'),linewidths=.45,label=labels.get(feature,feature)))
ax.set(xlim=(-4,260),ylim=(-4,260),aspect='equal',xlabel='X [mm]',ylabel='Y [mm]')
ax.set_title('Vollständige erste Schicht – tatsächliche Druckbahnen\nP1S · PETG HF Schwarz · 230 °C / 70 °C · 8 mm Innenbrim')
ax.legend(loc='upper right',fontsize=8)
fig.tight_layout();fig.savefig(H/('Erste_Schicht_230C_Innenbrim8'+suffix+'.png'));plt.close(fig)
report={'bounds_xy_mm':bounds,'first_layer_speeds_mm_s':{k:sorted(v) for k,v in speeds.items() if v},
    'paths_per_feature':{k:len(v) for k,v in paths.items() if v},'part_fan_first_three_layers_off':True,
    'auxiliary_fan_all_commands_off':True,'auxiliary_startup_commands_changed':changes,
    'layer_nozzle_temperature_C':230,'bed_C':70,'max_volumetric_speed_unchanged_mm3_s':21,
    'flow_ratio_uncalibrated_stock':.95,'calibration_required_before_large_print':True,
    'bed_leveling_required_at_dispatch':True,'automatic_flow_calibration_supported_by_P1S':False,
    'sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
(H/('Erste_Schicht_Pruefung'+suffix+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
