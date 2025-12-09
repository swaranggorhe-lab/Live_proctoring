import cv2
import json
import os
import sys
from pathlib import Path

# Make sure backend package imports work
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.detector import ProctorDetector

OUT_IMG = Path(__file__).resolve().parent / 'last_capture.jpg'

def capture_frame(index=0, width=1280, height=720, timeout_sec=5):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {index}")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Warm up
    import time
    t0 = time.time()
    frame = None
    while time.time() - t0 < timeout_sec:
        ret, frm = cap.read()
        if not ret:
            continue
        frame = frm
        break
    cap.release()
    if frame is None:
        raise RuntimeError("Failed to capture frame from camera")
    return frame


def main():
    try:
        frame = capture_frame()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    # Save for inspection
    cv2.imwrite(str(OUT_IMG), frame)

    # Encode to JPEG bytes
    ret, buf = cv2.imencode('.jpg', frame)
    if not ret:
        print(json.dumps({"error": "Failed to encode frame to JPEG"}))
        return

    frame_bytes = buf.tobytes()

    # Initialize detector (use default model)
    try:
        detector = ProctorDetector()
    except Exception as e:
        print(json.dumps({"error": f"Failed to init detector: {e}"}))
        return

    try:
        violations = detector.detect(frame_bytes)
        print(json.dumps({"result": violations}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"Detection failed: {e}"}))


if __name__ == '__main__':
    main()
