#!/usr/bin/env python3
"""Manifest input, code, documentation and results excluding temporary runtime and active logs."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
files={}
for f in sorted(R.rglob('*')):
    if not f.is_file():continue
    s=f.relative_to(R).as_posix()
    if s=='SHA256SUMS_OUTPUT.json' or s.startswith('.runtime/') or '__pycache__' in s or s.endswith(('.pyc','.log','.tmp')):continue
    files[s]=hashlib.sha256(f.read_bytes()).hexdigest()
(R/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=files),indent=2)+'\n')
print('V18_38_MANIFEST',len(files))
