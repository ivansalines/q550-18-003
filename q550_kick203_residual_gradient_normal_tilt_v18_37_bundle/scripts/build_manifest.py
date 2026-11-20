#!/usr/bin/env python3
"""SHA256 manifest, excludes logs and runtime; no self-reference."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
files={}
for p in sorted(R.rglob('*')):
    if not p.is_file():continue
    n=p.relative_to(R).as_posix()
    if n=='SHA256SUMS_OUTPUT.json' or n.startswith('.runtime/') or '__pycache__' in n or n.endswith(('.pyc','.log','.tmp')):continue
    files[n]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=files),indent=2)+'\n')
print('V18_37_SHA256_ENTRIES',len(files))
