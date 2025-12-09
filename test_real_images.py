#!/usr/bin/env python3
"""Test detection on actual training images."""
import sys
sys.path.insert(0, '/Users/swarang.gorhe/Documents/live_proctoring/backend')

import cv2
from app.detector import ProctorDetector
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_with_training_image():
    """Test with actual training image that has faces and phones."""
    logger.info("=" * 70)
    logger.info("🔍 TESTING WITH ACTUAL TRAINING IMAGES")
    logger.info("=" * 70)
    
    try:
        logger.info("\n1️⃣  Loading detector...")
        detector = ProctorDetector()
        logger.info("   ✅ Detector ready")
        
        # Test with first training image
        img_path = "/Users/swarang.gorhe/Documents/live_proctoring/backend/training/dataset/images/train/train_0029.jpg"
        logger.info(f"\n2️⃣  Loading training image: train_0029.jpg")
        frame = cv2.imread(img_path)
        
        if frame is None:
            logger.error("   ❌ Failed to load image")
            return
        
        logger.info(f"   ✅ Image loaded: {frame.shape}")
        
        # Convert to bytes
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        logger.info(f"\n3️⃣  Running detection...")
        violations = detector.detect(frame_bytes)
        logger.info(f"   ✅ Detection complete")
        
        logger.info(f"\n📊 RESULTS: {len(violations)} violations")
        for v in violations:
            logger.info(f"   • {v['type']}: severity={v['severity']}, conf={v.get('confidence', 0):.2f}")
            if 'boxes' in v:
                logger.info(f"     Boxes: {len(v['boxes'])}")
                for box in v['boxes']:
                    logger.info(f"       - {box['class_name']}: {box['confidence']:.2f}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Detection test complete!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_with_training_image()
