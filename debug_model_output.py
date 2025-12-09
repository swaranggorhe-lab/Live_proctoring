#!/usr/bin/env python3
"""Debug what the model outputs at different confidence levels."""
import sys
sys.path.insert(0, '/Users/swarang.gorhe/Documents/live_proctoring/backend')

import cv2
from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

model_path = "/Users/swarang.gorhe/Documents/live_proctoring/runs/detect/train2/weights/best.pt"
img_path = "/Users/swarang.gorhe/Documents/live_proctoring/backend/training/dataset/images/train/train_0029.jpg"

logger.info("=" * 70)
logger.info("🔍 RAW MODEL DEBUG")
logger.info("=" * 70)

try:
    logger.info(f"\n1️⃣  Loading model: {model_path}")
    model = YOLO(model_path)
    logger.info("   ✅ Model loaded")
    
    logger.info(f"\n2️⃣  Loading image: {img_path}")
    frame = cv2.imread(img_path)
    logger.info(f"   ✅ Image: {frame.shape}")
    
    # Test with different confidence thresholds
    for conf_thresh in [0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6]:
        logger.info(f"\n3️⃣  Testing with confidence threshold: {conf_thresh}")
        results = model(frame, conf=conf_thresh, verbose=False)
        
        if results and results[0].boxes:
            result = results[0]
            logger.info(f"   ✅ Found {len(result.boxes)} detections:")
            for box in result.boxes:
                try:
                    cls = int(box.cls[0]) if hasattr(box.cls, '__len__') else int(box.cls)
                    conf = float(box.conf[0]) if hasattr(box.conf, '__len__') else float(box.conf)
                    class_names = {0: "face", 1: "cellphone"}
                    logger.info(f"      • {class_names.get(cls, f'class_{cls}')}: conf={conf:.3f}")
                except Exception as e:
                    logger.warning(f"      ! Error extracting box: {e}")
        else:
            logger.info(f"   ⚠️  No detections at conf={conf_thresh}")
    
    logger.info("\n" + "=" * 70)
    
except Exception as e:
    logger.error(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
