import cv2
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.detector import ProctorDetector


def run_image(path):
    img = cv2.imread(str(path))
    if img is None:
        print(json.dumps({"error": f"Failed to read image {path}"}))
        return
    ret, buf = cv2.imencode('.jpg', img)
    if not ret:
        print(json.dumps({"error": "Failed to encode image"}))
        return
    frame_bytes = buf.tobytes()
    try:
        detector = ProctorDetector()
    except Exception as e:
        print(json.dumps({"error": f"Failed to init detector: {e}"}))
        return
    try:
        violations = detector.detect(frame_bytes)
        print(json.dumps({"image": str(path), "result": violations}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"Detection failed: {e}"}))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: run_image_detect.py <image_path>"}))
    else:
        run_image(sys.argv[1])
