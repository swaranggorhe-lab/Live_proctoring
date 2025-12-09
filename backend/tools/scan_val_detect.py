from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.detector import ProctorDetector

val_dir = ROOT / 'training' / 'dataset' / 'images' / 'val'
if not val_dir.exists():
    print('no val dir found:', val_dir)
    raise SystemExit(0)

det = ProctorDetector()
# Lower confidence threshold for discovery testing
try:
    det.confidence_threshold = 0.01
except Exception:
    pass
found_any = False
for p in sorted(val_dir.glob('*.jpg')):
    with open(p,'rb') as f:
        b = f.read()
    res = det.detect(b)
    for v in res:
        if v.get('type')=='prohibited_items':
            print(json.dumps({'image':str(p),'violations':v},indent=2))
            found_any = True
print('done; found_any=',found_any)
