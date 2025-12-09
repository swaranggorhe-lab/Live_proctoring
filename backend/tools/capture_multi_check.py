import cv2
import numpy as np
from pathlib import Path
import json

OUT_DIR = Path(__file__).resolve().parent
results = []
for idx in range(4):
    cap = cv2.VideoCapture(idx)
    if not cap.isOpened():
        results.append({"index": idx, "opened": False})
        continue
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    cap.release()
    if not ret or frame is None:
        results.append({"index": idx, "opened": True, "captured": False})
        continue
    path = OUT_DIR / f'capture_idx_{idx}.jpg'
    cv2.imwrite(str(path), frame)
    arr = np.asarray(frame)
    stats = {
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "min": int(arr.min()),
        "max": int(arr.max()),
        "mean": float(arr.mean()),
        "file": str(path),
        "size_bytes": path.stat().st_size
    }
    results.append({"index": idx, "opened": True, "captured": True, "stats": stats})

print(json.dumps(results, indent=2))
