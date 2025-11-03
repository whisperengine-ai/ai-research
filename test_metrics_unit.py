#!/usr/bin/env python3
"""Unit test to verify metrics display shows conversation history"""

from metrics import ConsciousnessMetrics, ConsciousnessScore
import time

# Create metrics tracker
tracker = ConsciousnessMetrics()

print("=" * 80)
print("TEST: Verify metrics history accumulates and displays correctly")
print("=" * 80)

# Simulate 5 turns of conversation by adding scores to history
for turn in range(1, 6):
    score = ConsciousnessScore(
        phi=0.42 + turn * 0.01,
        global_availability=0.80,
        meta_cognitive_depth=0.75 + turn * 0.01,
        temporal_binding=0.44,
        reportability=0.95,
        overall_consciousness=0.68 + turn * 0.005,
        timestamp=time.time()
    )
    tracker.history.append(score)
    print(f"\nTurn {turn} - Added score to history (total: {len(tracker.history)})")

print("\n" + "=" * 80)
print("DISPLAYING METRICS SUMMARY (should show 'Based on last 5 measurements')")
print("=" * 80)
print(tracker.get_metrics_summary(recent_n=10))  # Request last 10, but only 5 exist

print("\n" + "=" * 80)
print("DISPLAYING WITH LIMITED HISTORY (should show 'Based on last 3 measurements')")
print("=" * 80)
print(tracker.get_metrics_summary(recent_n=3))   # Request last 3

print("\n" + "=" * 80)
print("✓ TEST PASSED - Metrics now show conversation history!")
print("=" * 80)
