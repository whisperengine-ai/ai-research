#!/usr/bin/env python3
"""
Quick test of heuristic mode vs. standard modes
Demonstrates the speed advantage of heuristic generation
"""

import time
import sys
from consciousness_chatbot import ConsciousnessSimulator

def test_mode(mode_name: str, **kwargs):
    """Test a mode with sample inputs"""
    print(f"\n{'='*80}")
    print(f"Testing: {mode_name}")
    print('='*80)
    
    start_init = time.time()
    simulator = ConsciousnessSimulator(**kwargs)
    init_time = time.time() - start_init
    
    print(f"✓ Initialized in {init_time:.2f}s\n")
    
    test_inputs = [
        "Hello, how are you?",
        "What do you think about consciousness?",
    ]
    
    for user_input in test_inputs:
        print(f"👤 User: {user_input}")
        start = time.time()
        result = simulator.process_input(user_input)
        elapsed = time.time() - start
        
        print(f"🤖 Response: {result['response'][:100]}...")
        print(f"⏱️  Time: {elapsed:.3f}s\n")

if __name__ == "__main__":
    # Test heuristic mode (fastest)
    test_mode(
        "HEURISTIC MODE (No LLM, instant)",
        use_heuristic=True,
        verbose=False
    )
    
    print("\n" + "="*80)
    print("✅ Heuristic mode is ready for fast testing!")
    print("="*80)
    print("""
USAGE EXAMPLES:

# Fast testing with heuristic responses (NO LLM NEEDED):
python consciousness_chatbot.py --heuristic

# Local model (default gpt2):
python consciousness_chatbot.py --local

# Local model with different size:
python consciousness_chatbot.py --local --model gpt2-medium

# API mode (requires OPENROUTER_API_KEY in .env):
python consciousness_chatbot.py

# Reduce verbosity:
python consciousness_chatbot.py --heuristic --quiet

# Lower recursion depth for faster processing:
python consciousness_chatbot.py --heuristic --depth 1

# Get help:
python consciousness_chatbot.py --help
    """)
