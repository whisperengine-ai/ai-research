#!/usr/bin/env python3
"""
Quick validation test for emotion detection improvements
Tests that the neutral bias has been fixed
"""

from emotion_detector import EmotionDetector

def test_emotion_detection():
    """Test improved emotion detection without neutral bias"""
    detector = EmotionDetector()
    
    test_cases = [
        # Test cases that were wrongly classified as neutral
        ("I don't know what to do anymore.", ["sadness", "fear"], "Should detect sadness/fear, not neutral"),
        ("Things have been difficult lately.", ["sadness", "fear"], "Should detect sadness, not neutral"),
        ("Why does this keep happening?", ["anger", "surprise"], "Should detect anger, not neutral"),
        
        # Test cases that should remain neutral
        ("How are you today?", ["neutral", "surprise"], "Should be neutral"),
        ("Tell me more about that.", ["neutral"], "Should be neutral"),
        ("What do you think?", ["neutral", "surprise"], "Should be neutral"),
        
        # Clear emotion cases (controls)
        ("I'm so happy!", ["joy"], "Should be joy"),
        ("This is terrible!", ["disgust", "anger", "fear"], "Should be negative emotion"),
        ("I'm scared.", ["fear"], "Should be fear"),
        ("This makes me angry.", ["anger"], "Should be anger"),
    ]
    
    print("=" * 70)
    print("EMOTION DETECTION VALIDATION TEST")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for text, expected_emotions, description in test_cases:
        emotion, confidence, scores = detector.detect_emotion(text)
        
        is_pass = emotion in expected_emotions
        status = "✓ PASS" if is_pass else "✗ FAIL"
        
        if is_pass:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status}: {text[:50]}")
        print(f"  Expected: {', '.join(expected_emotions)}")
        print(f"  Got: {emotion} (confidence: {confidence:.3f})")
        print(f"  Note: {description}")
        
        # Show top 3 for debugging
        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  Top 3: {', '.join([f'{e}={s:.3f}' for e, s in top_3])}")
    
    print(f"\n{'=' * 70}")
    print(f"RESULTS: {passed} passed, {failed} failed ({passed/(passed+failed)*100:.1f}% pass rate)")
    print(f"{'=' * 70}\n")
    
    if failed > 0:
        print(f"⚠️  {failed} test(s) failed. Review the output above.")
        return False
    else:
        print("✓ All tests passed! Neutral bias has been fixed.")
        return True

if __name__ == "__main__":
    import sys
    success = test_emotion_detection()
    sys.exit(0 if success else 1)
