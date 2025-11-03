# Consciousness Metrics: Conversation History Tracking

## 📊 Overview

The consciousness metrics system now tracks **conversation history** to show how consciousness properties evolve across multiple turns of dialogue, rather than just reporting the current turn's measurements.

## The Change

### Before
```
📊 Consciousness Metrics (Research-Grade):
─────────────────────────────────────────
  Φ (Integrated Information):  0.442
  Global Availability (GWT):   0.800
  Meta-Cognitive Depth:        0.781
  Temporal Binding:            0.440
  Reportability (Access):      0.950
─────────────────────────────────────────
  🧠 Overall Consciousness:    0.675
─────────────────────────────────────────
  Based on last 1 measurements  ← Always showed "1"
```

### After (Multi-turn Conversation)
```
Turn 1:
  Based on last 1 measurements

Turn 2:
  Based on last 2 measurements

Turn 3:
  Based on last 3 measurements

Turn 10+:
  Based on last 10 measurements  ← Tracks conversation trends
```

## Why This Matters for Research

1. **Trend Analysis**: Metrics now show averages across recent turns, enabling detection of:
   - Consciousness drift (increasing/decreasing over conversation)
   - Stability patterns (high variance = unstable self-model)
   - Adaptation effects (changes as system reflects more)

2. **Better Metrics**: Averaging across 10 turns:
   - Reduces noise from individual turn variations
   - Reveals underlying consciousness patterns
   - Makes comparison between conditions more robust

3. **Real Conversation Dynamics**: Reflects how consciousness actually evolves:
   - Early turns: May be establishing context (lower metrics)
   - Middle turns: Full engagement (peak metrics)
   - Later turns: Reflective patterns emerge (stable metrics)

## Implementation Details

### Key Method: `get_metrics_summary()`

**Location**: `metrics.py` (line 484)

```python
def get_metrics_summary(self, recent_n: int = 10) -> str:
    """
    Generate human-readable metrics summary
    
    Args:
        recent_n: Number of recent scores to summarize
        
    Returns:
        Formatted string with metrics
    """
    if not self.history:
        return "No metrics collected yet."
    
    recent = self.history[-recent_n:]  # Get last N scores
    
    # Compute averages across recent turns
    avg_phi = np.mean([s.phi for s in recent])
    avg_avail = np.mean([s.global_availability for s in recent])
    # ... etc for all metrics
```

### Where Metrics Are Displayed

| Location | `recent_n` | Use Case |
|----------|-----------|----------|
| `consciousness_chatbot.py:490` | `10` | Main conversation loop (default) |
| `consciousness_chatbot.py:826` | `10` | Interactive session final report |
| `consciousness_chatbot.py:842` | `5` | Dataset collection (faster feedback) |
| `collect_dataset.py` | (varies) | Research data collection |

### Score History Storage

**Location**: `metrics.py` (line 114) in `compute_all_metrics()`

```python
score = ConsciousnessScore(...)
self.history.append(score)  # Accumulates every turn
return score
```

Each turn's metrics are automatically stored in `metrics_tracker.history`, a growing list of `ConsciousnessScore` objects.

## Research Applications

### Example: Detecting Consciousness Degradation

```python
# In analysis phase
scores = simulator.metrics_tracker.history

# Window 1: Turns 1-10
window1_mean = np.mean([s.meta_cognitive_depth for s in scores[:10]])

# Window 2: Turns 20-30  
window2_mean = np.mean([s.meta_cognitive_depth for s in scores[20:30]])

# Compare: Did meta-cognitive depth drop? Signal of consciousness change?
degradation = window1_mean - window2_mean
```

### Example: Ablation Study Analysis

```python
# With recursion (depth=3)
with_recursion = [s.meta_cognitive_depth for s in scores]
mean_with = np.mean(with_recursion)

# Without recursion (depth=0)
no_recursion = [s.meta_cognitive_depth for s in scores]
mean_without = np.mean(no_recursion)

# Compare effect size
d = (mean_with - mean_without) / np.std(all_scores)
# Should see d ≥ 4.0 (the main research finding!)
```

## Configuration

### Adjusting History Window

To change how many turns are averaged in main conversation:

**File**: `consciousness_chatbot.py` (line 490)

```python
# Show last 10 turns (default)
print(self.metrics_tracker.get_metrics_summary(recent_n=10))

# Or change to:
print(self.metrics_tracker.get_metrics_summary(recent_n=5))   # Faster response
print(self.metrics_tracker.get_metrics_summary(recent_n=20))  # Longer trends
```

### For Dataset Collection

**File**: `collect_dataset.py`

```python
# You can pass recent_n when reporting metrics
metrics_str = simulator.get_metrics_summary(recent_n=5)  
print(metrics_str)
```

## Testing

To verify metrics history works correctly:

```bash
# Run unit test
python test_metrics_unit.py

# Output should show:
#   Turn 1: Based on last 1 measurements
#   Turn 5: Based on last 5 measurements
#   Turn 10+: Based on last 10 measurements
```

## Related Documentation

- **[metrics.py](metrics.py)**: Implementation of `ConsciousnessMetrics` class
- **[SYSTEM_DESIGN.md](SYSTEM_DESIGN.md)**: Detailed metric definitions (Φ, Meta-Cognitive Depth, etc.)
- **[RESULTS.md](RESULTS.md)**: Historical baselines (what normal values are)
- **[SPACY_OPTIMIZATION.md](SPACY_OPTIMIZATION.md)**: Performance considerations

## Future Enhancements

1. **Windowed Analysis**: Separate metrics into dialogue phases
   - Turn 1-5: Greeting/Context
   - Turn 6-15: Engagement
   - Turn 16+: Reflection

2. **Derivative Metrics**: Show rate of change
   - "Meta-Cognitive Depth trending +0.02/turn"
   - "Consciousness trending stable"

3. **Comparison Mode**: Show metrics for two parallel conversations
   - With neurochemistry enabled vs. disabled
   - With recursion enabled vs. disabled
   - A/B testing consciousness effects

4. **Persistence**: Save metrics history to JSON for later analysis
   - Track across multiple sessions
   - Build individual conversation profiles

---

**Last Updated**: November 3, 2025  
**Related Commit**: 071c3fa - "Improvement: Display consciousness metrics across 10-turn conversation history"
