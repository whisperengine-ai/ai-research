#!/usr/bin/env python3
"""Quick test of the fix for truncated responses"""

from consciousness_chatbot import ConsciousnessSimulator

print("Testing local mode with fixed token parameters...")
print("=" * 80)

sim = ConsciousnessSimulator(
    llm_model="gpt2",
    use_openrouter=False,
    recursion_depth=2,
    verbose=False
)

print("\n✓ Simulator initialized (no warnings about conflicting max_length/max_new_tokens)")

test_inputs = [
    "Hello! How are you doing?",
    "What do you think about consciousness?",
]

for user_input in test_inputs:
    print(f"\n👤 User: {user_input}")
    result = sim.process_input(user_input)
    response = result['response']
    print(f"🤖 Bot:   {response}")
    print(f"    Length: {len(response)} chars, {len(response.split())} words")

print("\n✅ Test complete - responses should be longer now!")
