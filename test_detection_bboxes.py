#!/usr/bin/env python3
"""
Comprehensive test of phone and face detection with bounding boxes.
"""
import sys
sys.path.insert(0, '/Users/swarang.gorhe/Documents/live_proctoring/backend')

import cv2
import numpy as np
from app.detector import ProctorDetector
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_test_image_with_face_and_phone():
    """Create a test image with simulated face and phone."""
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 240
    
    # Simulate a face (circle in the center-left)
    center = (200, 240)
    cv2.circle(frame, center, 60, (200, 150, 100), -1)  # Face
    cv2.circle(frame, (180, 220), 8, (0, 0, 0), -1)      # Eye
    cv2.circle(frame, (220, 220), 8, (0, 0, 0), -1)      # Eye
    
    # Simulate a phone (rectangle in the center-right)
    phone_tl = (400, 150)
    phone_br = (480, 350)
    cv2.rectangle(frame, phone_tl, phone_br, (100, 100, 100), -1)  # Phone
    cv2.rectangle(frame, phone_tl, phone_br, (50, 50, 50), 2)      # Border
    
    cv2.putText(frame, 'Face + Phone Test', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    return frame

def test_detection():
    """Test phone and face detection."""
    logger.info("=" * 70)
    logger.info("🔍 COMPREHENSIVE DETECTION TEST WITH BOUNDING BOXES")
    logger.info("=" * 70)
    
    try:
        # Initialize detector
        logger.info("\n1️⃣  Initializing trained detector...")
        detector = ProctorDetector()
        logger.info("   ✅ Detector loaded")
        
        # Create test image with face and phone
        logger.info("\n2️⃣  Creating test image (face + phone)...")
        frame = create_test_image_with_face_and_phone()
        
        # Convert to JPEG bytes
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        logger.info(f"   ✅ Test image created: {len(frame_bytes)} bytes")
        
        # Run detection
        logger.info("\n3️⃣  Running detection...")
        violations = detector.detect(frame_bytes)
        logger.info(f"   ✅ Detection completed")
        
        # Display results
        logger.info("\n📊 DETECTION RESULTS:")
        logger.info(f"   Total violations found: {len(violations)}")
        
        if not violations:
            logger.info("   ⚠️  No violations detected")
        else:
            for i, v in enumerate(violations, 1):
                logger.info(f"\n   Violation #{i}:")
                logger.info(f"   • Type: {v.get('type')}")
                logger.info(f"   • Severity: {v.get('severity')}")
                logger.info(f"   • Confidence: {v.get('confidence', 'N/A'):.3f}")
                
                if 'count' in v:
                    logger.info(f"   • Count: {v['count']}")
                
                if 'items' in v:
                    logger.info(f"   • Items detected:")
                    for item in v['items']:
                        logger.info(f"     - {item.get('type')}: confidence={item.get('confidence', 0):.3f}")
                
                if 'boxes' in v:
                    logger.info(f"   • Bounding boxes: {len(v['boxes'])} detected")
                    for j, box in enumerate(v['boxes'], 1):
                        logger.info(f"     - Box {j}: {box.get('class_name')}, conf={box.get('confidence'):.3f}")
                        if box.get('bbox'):
                            x1, y1, x2, y2 = box['bbox']
                            logger.info(f"       Coords: ({x1:.0f}, {y1:.0f}) → ({x2:.0f}, {y2:.0f})")
        
        # JSON output for debugging
        logger.info("\n📋 RAW JSON OUTPUT:")
        logger.info(json.dumps(violations, indent=2, default=str)[:500] + "...")
        
        logger.info("\n" + "=" * 70)
        logger.info("✨ TEST COMPLETE - System ready for live detection!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    test_detection()
