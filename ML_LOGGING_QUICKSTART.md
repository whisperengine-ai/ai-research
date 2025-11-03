# ML Logging Integration - Quick Start

## ✅ Integration Complete!

ML logging is now fully integrated into the consciousness simulator. The system logs all conversation data needed for training quality prediction models.

---

## 🚀 Usage

### Enable ML Logging

```bash
# Run with ML logging enabled
python consciousness_chatbot.py --log-ml

# Use custom log directory
python consciousness_chatbot.py --log-ml --ml-log-dir my_training_data

# Combine with other flags
python consciousness_chatbot.py --log-ml --depth 3 --local --model gpt2
```

### Programmatic Usage

```python
from consciousness_chatbot import ConsciousnessSimulator

# Initialize with ML logging
sim = ConsciousnessSimulator(
    use_openrouter=True,
    recursion_depth=3,
    verbose=True,
    enable_ml_logging=True,  # ← Enable logging
    ml_log_dir='ml_logs'     # ← Custom directory (optional)
)

# Run conversations (data is logged automatically)
result = sim.process_input("I'm feeling worried about this project.")

# When done, logs are automatically saved on quit
# Or manually save:
if sim.ml_logger:
    filepath = sim.ml_logger.save_session()
    print(f"Saved to: {filepath}")
```

---

## 📊 What Gets Logged

Each conversation turn logs:

### Input/Output
- User input text & length
- Bot response text & length

### Context
- User emotion (RoBERTa detection)
- User emotion confidence
- Bot neurochemical state (5 chemicals)

### Meta-Cognition (15 features)
- `num_reflections` - Number of recursive reflections
- `max_depth` - Maximum recursion level achieved
- `avg_reflection_length` - Average characters per reflection
- `self_ref_count` - Count of "I", "my", "myself", etc.
- `self_ref_density` - Self-references per character
- `confidence_markers` - "certain", "confident", "sure", etc.
- `uncertainty_markers` - "unsure", "maybe", "perhaps", etc.
- `confidence_ratio` - Confidence vs uncertainty balance
- `emotion_words` - "feel", "emotion", "notice", etc.
- `emotional_awareness_density` - Emotion words per character
- `positive_eval` - "good", "appropriate", "helpful", etc.
- `negative_eval` - "inappropriate", "wrong", "poor", etc.
- `eval_polarity` - Positive vs negative balance
- `user_mentions` - References to user/they/them
- `perspective_taking_score` - User focus metric

### Outcomes (Training Targets)
- `consciousness_metrics` - 6 consciousness scores (Φ, meta-depth, etc.)
- `engagement_score` - User engagement level
- `resonance_score` - Emotional alignment
- `appropriateness_score` - Response appropriateness
- `human_quality_rating` - Placeholder for human ratings (1-10)
- `user_satisfaction` - Placeholder for satisfaction (1-5)
- `conversation_continued` - Whether user kept talking

---

## 📁 Output Format

### File Structure

```
ml_logs/
├── ml_log_<session_id>_<timestamp>.json
├── ml_log_<session_id>_<timestamp>.json
└── ...
```

### JSON Schema

```json
{
  "metadata": {
    "session_id": "919dea85",
    "timestamp": "2025-11-03T13:10:11.123456",
    "num_turns": 3,
    "format_version": "1.0"
  },
  "turns": [
    {
      "turn_id": "uuid-here",
      "timestamp": "2025-11-03T13:10:15.123456",
      "user_input": "I'm feeling worried...",
      "response": "I understand...",
      "user_emotion": "fear",
      "meta_cognition_raw": { ... },
      "meta_cognition_features": { ... },
      "neurochemistry": { ... },
      "outcomes": { ... }
    }
  ]
}
```

---

## 🎯 Next Steps: Building the ML Pipeline

### Phase 1: Collect Training Data (Now!)

```bash
# Collect 500-1000 conversations with ML logging enabled
python consciousness_chatbot.py --log-ml --depth 3

# Or use automated collection
python collect_dataset.py --count 500 --enable-ml-logging
```

### Phase 2: Train the Model

```bash
# Train quality predictor from logs
python train_metacognition_model.py --log-dir ml_logs
```

### Phase 3: Deploy with ML Guidance

```bash
# Use trained model to guide responses
python consciousness_chatbot.py --use-ml-guidance --model-path models/quality_predictor.pkl
```

---

## 🔍 Inspecting Logs

### View Summary

```python
from ml_logger import MLLogger

logger = MLLogger(log_dir='ml_logs')
# Load existing log
import json
with open('ml_logs/ml_log_XXX.json') as f:
    data = json.load(f)

print(f"Turns: {data['metadata']['num_turns']}")
for turn in data['turns']:
    print(f"  {turn['user_emotion']:10} - {turn['user_input'][:50]}")
```

### Extract Features for Analysis

```python
import json
import pandas as pd

# Load all logs
logs = []
for log_file in glob.glob('ml_logs/*.json'):
    with open(log_file) as f:
        data = json.load(f)
        logs.extend(data['turns'])

# Convert to DataFrame
df = pd.DataFrame([
    {**turn['meta_cognition_features'], 
     'engagement': turn['outcomes']['engagement_score']}
    for turn in logs
])

print(df.describe())
```

---

## 🧪 Testing

```bash
# Run integration test
python test_ml_logging.py

# Should output:
# ✅ ML LOGGING TEST PASSED!
```

---

## 📝 Adding Human Ratings (Optional)

After conversations, you can add human quality ratings:

```python
from ml_logger import MLLogger

logger = MLLogger(log_dir='ml_logs')
# Load session...

# Add ratings for specific turns
logger.add_human_ratings(
    turn_id='uuid-here',
    quality_rating=8,  # 1-10 scale
    satisfaction=4     # 1-5 scale
)

# Save updated log
logger.save_session()
```

---

## 🎓 Reference

- **Full pipeline documentation**: `ML_METACOGNITION_PIPELINE.md`
- **Recursion analysis**: `RECURSION_ANALYSIS.md`
- **ML logger source**: `ml_logger.py`
- **Integration test**: `test_ml_logging.py`

---

## ✅ Status

- [x] ML logger implemented
- [x] Integrated into ConsciousnessSimulator
- [x] Command-line flags added
- [x] .gitignore updated
- [x] Test suite passing
- [ ] Collect training data (500-1000 conversations)
- [ ] Train quality predictor model
- [ ] Implement runtime ML guidance
- [ ] Evaluate improvements

**Current state**: Ready to collect training data! 🎉
