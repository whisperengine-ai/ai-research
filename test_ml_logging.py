#!/usr/bin/env python3
"""
Quick test to verify ML logging integration
"""

from consciousness_chatbot import ConsciousnessSimulator
import os

def test_ml_logging():
    """Test that ML logging works correctly"""
    
    print("=" * 70)
    print("TESTING ML LOGGING INTEGRATION")
    print("=" * 70)
    
    # Initialize with ML logging enabled
    print("\n1. Initializing simulator with ML logging...\n")
    sim = ConsciousnessSimulator(
        use_openrouter=False,  # Use local for testing
        use_heuristic=False,
        recursion_depth=3,
        verbose=False,  # Quiet mode for cleaner output
        enable_ml_logging=True,
        ml_log_dir='ml_logs_test'
    )
    
    # Run a few test conversations
    print("\n2. Running test conversations...\n")
    test_inputs = [
        "I'm feeling worried about this project.",
        "Can you help me understand consciousness?",
        "That's interesting, tell me more."
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"   Turn {i}: '{user_input}'")
        result = sim.process_input(user_input)
        print(f"   Response: '{result['response'][:60]}...'")
    
    # Check logger stats
    print("\n3. Checking logged data...\n")
    if sim.ml_logger:
        stats = sim.ml_logger.get_summary_stats()
        print(f"   Turns logged: {stats['num_turns']}")
        print(f"   Avg reflections: {stats['avg_num_reflections']:.1f}")
        print(f"   Emotions: {stats['emotions_detected']}")
        
        # Save session
        filepath = sim.ml_logger.save_session()
        print(f"\n4. Session saved to: {filepath}")
        
        # Verify file exists and has content
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"   File size: {file_size:,} bytes")
            
            # Load and verify structure
            import json
            with open(filepath) as f:
                data = json.load(f)
            
            print(f"   Metadata: {list(data['metadata'].keys())}")
            print(f"   Turns: {len(data['turns'])}")
            
            if len(data['turns']) > 0:
                turn = data['turns'][0]
                print(f"\n5. First turn structure:")
                print(f"   Keys: {list(turn.keys())}")
                print(f"   Meta-cognition features: {list(turn['meta_cognition_features'].keys())}")
                print(f"   Outcomes: {list(turn['outcomes'].keys())}")
                
                print("\n✅ ML LOGGING TEST PASSED!")
                return True
        else:
            print("\n❌ TEST FAILED: File not created")
            return False
    else:
        print("\n❌ TEST FAILED: ML logger not initialized")
        return False

if __name__ == "__main__":
    try:
        success = test_ml_logging()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
