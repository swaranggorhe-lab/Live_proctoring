import cv2
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.detector import ProctorDetector

OUT_IMG = Path(__file__).resolve().parent / 'last_capture.jpg'
OUT_ANNOT = Path(__file__).resolve().parent / 'last_capture_annotated_debug.jpg'


def capture_frame(index=0, width=1280, height=720, timeout_sec=5):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {index}")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

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


def annotate_and_report(frame, detector: ProctorDetector):
    report = {"haar_faces": [], "dnn_faces": [], "yolo_boxes": [], "violations": None}
    h, w = frame.shape[:2]

    # Haar
    haar_faces = []
    if detector.face_cascade is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30,30), maxSize=(400,400))
        for (x,y,fw,fh) in faces:
            haar_faces.append({"xywh": [int(x),int(y),int(fw),int(fh)], "confidence": None})
            cv2.rectangle(frame, (x,y), (x+fw, y+fh), (0,255,0), 2)
            cv2.putText(frame, 'haar_face', (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    report['haar_faces'] = haar_faces

    # DNN
    dnn_faces = []
    if detector.dnn_net is not None:
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), [104,117,123], False, False)
        detector.dnn_net.setInput(blob)
        detections = detector.dnn_net.forward()
        for i in range(detections.shape[2]):
            conf = float(detections[0,0,i,2])
            if conf > 0.3:
                box = detections[0,0,i,3:7] * [w, h, w, h]
                (x1,y1,x2,y2) = box.astype('int')
                dnn_faces.append({"xyxy": [int(x1),int(y1),int(x2),int(y2)], "confidence": conf})
                cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,0), 2)
                cv2.putText(frame, f'dnn {conf:.2f}', (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
    report['dnn_faces'] = dnn_faces

    # YOLO (run at very low conf to show candidates)
    yolo_results = detector.yolo_model(frame, conf=0.0, verbose=False)
    if yolo_results and yolo_results[0].boxes:
        res = yolo_results[0]
        names = None
        try:
            names = res.names
        except Exception:
            names = None
        for box in res.boxes:
            try:
                cls = None
                conf = None
                if hasattr(box, 'cls'):
                    try:
                        cls = int(box.cls[0])
                    except Exception:
                        cls = int(box.cls)
                if hasattr(box, 'conf'):
                    try:
                        conf = float(box.conf[0])
                    except Exception:
                        conf = float(box.conf)
                bbox = None
                if hasattr(box, 'xyxy'):
                    try:
                        coords = box.xyxy[0]
                        bbox = [int(float(c)) for c in coords]
                    except Exception:
                        pass
                cls_name = None
                if names and cls is not None:
                    try:
                        cls_name = names.get(cls, None)
                    except Exception:
                        try:
                            cls_name = names[int(cls)]
                        except Exception:
                            cls_name = None
                report['yolo_boxes'].append({"class": cls, "class_name": cls_name, "confidence": conf if conf is not None else 0.0, "bbox": bbox})
                # Draw box
                if bbox:
                    x1,y1,x2,y2 = bbox
                    color = (0,0,255)
                    cv2.rectangle(frame, (x1,y1),(x2,y2), color, 2)
                    label = f"{cls_name or cls}:{conf:.2f}" if cls_name else f"{cls}:{conf:.2f}"
                    cv2.putText(frame, label, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            except Exception as e:
                continue

    # Run the usual detector to generate violations
    try:
        ret = detector.detect(cv2.imencode('.jpg', frame)[1].tobytes())
        report['violations'] = ret
    except Exception as e:
        report['violations'] = {"error": str(e)}

    return frame, report


def main():
    try:
        frame = capture_frame()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    cv2.imwrite(str(OUT_IMG), frame)

    try:
        det = ProctorDetector()
    except Exception as e:
        print(json.dumps({"error": f"Failed to init detector: {e}"}))
        return

    annotated, report = annotate_and_report(frame, det)
    cv2.imwrite(str(OUT_ANNOT), annotated)

    print(json.dumps({"result": report}, indent=2))

if __name__ == '__main__':
    main()
