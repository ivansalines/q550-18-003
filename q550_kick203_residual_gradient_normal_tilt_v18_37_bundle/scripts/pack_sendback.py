#!/usr/bin/env python3
"""Fail closed unless new authentic v18.37 Q550 gradients, comparisons and plots exist."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1]
proof=R/'results/original_v18_37_proof.json'
if not proof.is_file():raise RuntimeError('Missing ORIGINAL v18.37 Q550 run; preflight is NOT a physical certificate')
p=json.loads(proof.read_text())
if (p.get('status')!='ORIGINAL_Q550_RESIDUAL_GRADIENT_NORMAL_TILT_MOVING_LEVEL_COMPLETED' or p.get('original_integrations')!=13 or p.get('original_cases')!=12 or
    p.get('rhs_only_gradient_crosschecks')!=48 or not p.get('original_ode_sha256_verified') or not p.get('all_seeds_jointly_admissible') or not p.get('no_physical_material_constraint_certified')):
    raise RuntimeError('Missing or incompatible original v18.37 Q550 proof')
for name in ('original_v18_37_residual_gradient_profiles.csv','original_v18_37_case_summary.csv','original_v18_37_rhs_gradient_crosscheck.csv',
             'original_v18_37_stable_normal_tilt.png','original_v18_37_moving_level.png','original_v18_37_transverse_source.png'):
    if not (R/'results'/name).is_file():raise RuntimeError('Missing original v18.37 product: '+name)
files=json.loads((R/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,sha in files.items():
    if not (R/name).is_file() or hashlib.sha256((R/name).read_bytes()).hexdigest()!=sha:raise RuntimeError('Manifest failure '+name)
output=R.parent/(R.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for name in sorted(files):z.write(R/name,R.name+'/'+name,compress_type=zipfile.ZIP_STORED if name.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'SHA256SUMS_OUTPUT.json',R.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(output) as z:
    if z.testzip() or {x.split('/')[0] for x in z.namelist()}!={R.name}:raise RuntimeError('Bad v18.37 sendback ZIP')
print('SEND_BACK',output)
