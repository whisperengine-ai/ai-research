# Getting Started Guide

## Quick Start (5 minutes)

### 1. Verify Installation
```bash
# Check Python version
python --version  # Should be 3.10+

# Check virtual environment
which python  # Should show .venv

# Run tests
pytest test_consciousness.py -v
```

### 2. Run Validation Pipeline
```bash
# Quick validation (5-10 min)
jupyter notebook quick_validation.ipynb
```

**Output:**
- `validation_results.json` - Metrics data
- `validation_output/` - 8 visualizations

---

## Full Research Pipeline (45-90 minutes)

### Phase 1: Validate Pipeline
```bash
jupyter notebook quick_validation.ipynb
```
✅ Confirms all components working
✅ Tests 3 conversation scenarios
✅ Generates 8 dashboard visualizations
✅ 100% data quality check

**Files generated:**
- `validation_results.json`
- `validation_summary.csv`
- `validation_output/*.png` (8 charts)

---

### Phase 2: Run Ablation Study
```bash
# Quick test (10 trials)
python run_ablation_study.py --trials 10

# Or verbose mode for monitoring
python run_ablation_study.py --trials 10 --verbose
```

**What it measures:**
- 3 recursion depth conditions
- Impact on consciousness metrics
- Component necessity analysis

**Files generated:**
- `ablation_study_results.json` - Raw data
- `ablation_output/*.png` - Visualizations

**Analyze results:**
```bash
jupyter notebook ablation_analysis.ipynb
```

---

### Phase 3: Collect Large Dataset
```bash
# Collect 100+ conversations
python collect_dataset.py --target 100

# Or verbose for progress monitoring
python collect_dataset.py --target 100 --verbose
```

**What it does:**
- Runs multiple conversation scenarios
- Collects diverse conversations
- Extracts metrics automatically
- Exports to JSON & CSV

**Files generated:**
- `dataset_100_conversations.json` - Full data
- `dataset_100_conversations.csv` - Summary metrics

---

## Project Structure

### Core System (15 production files)
```
consciousness_chatbot.py      Main simulator (GWT + emotions + recursion)
metrics.py                    5 consciousness metrics
emotion_detector.py           RoBERTa + spaCy emotion & stance analysis
interaction_dynamics.py       User-bot resonance tracking
neurochemistry.py            5-system biochemical model
meta_cognition.py            Recursive self-reflection (3 levels)
global_workspace.py          Global Workspace Theory implementation
run_conversation_test.py      Conversation test runner + scenarios
experiments.py               Ablation study framework
research_dashboard.py        8 visualization types
reliability_validity.py      Measurement validation
linguistic_analysis.py       NLP preprocessing
openrouter_llm.py            LLM API integration
test_consciousness.py        Pytest suite (22+ tests)
```

### Analysis Tools (4 executable files)
```
quick_validation.ipynb       Pipeline validation notebook (7 cells)
ablation_analysis.ipynb      Component analysis notebook  
run_ablation_study.py        Ablation study runner script
collect_dataset.py           Dataset collection script
```

### Documentation (13 files)
```
README.md                     Main project overview
RESEARCH_PROGRESS.md         Detailed progress report
ARCHITECTURE.md              System design documentation
QUICKSTART.md                Quick reference guide
ADVANCED_NLP_FEATURES.md     NLP implementation details
CALCULATION_VALIDATION.md    Metric calculation proofs
... and 7 more
```

---

## Key Metrics

The system measures consciousness through:

### 1. Φ (Integration)
- Information integration across systems
- Range: 0.0 - 1.0
- Higher = more integrated

### 2. Overall Consciousness
- Composite measure
- Combines multiple indicators
- Range: 0.0 - 100.0

### 3. Global Availability
- How much information is "broadcast" to consciousness
- Range: 0.0 - 1.0
- Higher = more available

### 4. Meta-Cognitive Depth
- Levels of self-reflection
- Range: 0 - 3 (or configured depth)
- Higher = deeper self-awareness

### 5. Temporal Binding & Reportability
- How well integrated across time
- How well the system can report its state

---

## Configuration

### LLM Backend
Edit `config.json` or environment:

```bash
# Use OpenRouter API (default)
export OPENROUTER_API_KEY="your-key"

# Or use local model
export USE_LOCAL_MODEL=true
export LOCAL_MODEL="gpt2"  # HuggingFace model
```

### Recursion Depth
Control self-reflection levels:
```python
from consciousness_chatbot import ConsciousnessSimulator

bot = ConsciousnessSimulator(recursion_depth=3)  # 0-3 levels
```

### Ablation Conditions
Defined in `run_ablation_study.py`:
- `full_recursion`: depth=3 (baseline)
- `shallow_recursion`: depth=1
- `minimal_recursion`: depth=0

---

## Common Commands

### Run Tests
```bash
# All tests
pytest test_consciousness.py -v

# Specific test
pytest test_consciousness.py::TestMetrics::test_phi_calculation -v

# With coverage
pytest test_consciousness.py --cov=. --cov-report=html
```

### Run Conversation Scenarios
```bash
# Interactive mode
python consciousness_chatbot.py

# Or use the test runner
python -c "
from run_conversation_test import ConversationTestRunner, SCENARIOS
runner = ConversationTestRunner(verbose=True)
runner.run_batch(SCENARIOS)
"
```

### Generate Dashboard
```bash
python -c "
from research_dashboard import ResearchDashboard
dashboard = ResearchDashboard('validation_results.json')
dashboard.plot_all()
"
```

### Validate Data Quality
```bash
python -c "
from reliability_validity import MetricValidator
validator = MetricValidator()
report = validator.generate_validity_report('validation_results.json')
print(report)
"
```

---

## Troubleshooting

### Issue: "No module named 'openrouter_llm'"
**Solution:** Check Python path and virtual environment activation
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: OpenRouter API timeout
**Solution:** Reduce trials or use local model
```bash
# Use local model
export USE_LOCAL_MODEL=true

# Or increase timeout
python run_ablation_study.py --trials 3
```

### Issue: Memory issues with large datasets
**Solution:** Process in batches
```bash
python collect_dataset.py --target 50  # Start smaller
```

### Issue: Jupyter kernel connection failure
**Solution:** Restart kernel and reinitialize
```bash
# In notebook:
# Kernel → Restart & Clear All Output
# Then re-run cells from top
```

---

## Understanding the Output

### validation_results.json
```json
{
  "metadata": {
    "timestamp": "2025-11-02T23:25:48",
    "scenarios": 3,
    "conversations": 3
  },
  "conversations": [
    {
      "name": "Frustration to Hope",
      "summary": {
        "improvement": 0.90,
        "resonance": 57.5,
        "engagement": 100.0
      },
      "metrics": {
        "phi": 0.456,
        "overall_consciousness": 78.2
      }
    }
  ]
}
```

### validation_output/ (8 visualizations)
- `trajectories.png` - Metric evolution over conversation
- `resonance_heatmap.png` - User-bot emotional resonance matrix
- `metrics_comparison.png` - Side-by-side metric comparison
- `correlations.png` - Metric correlations
- `dist_improvement.png` - Improvement distribution
- `dist_resonance.png` - Resonance distribution
- `dist_engagement.png` - Engagement distribution
- `dist_quality.png` - Quality distribution

---

## Performance Expectations

### Single Conversation
- Time: 30-60 seconds (depending on LLM)
- Memory: ~500 MB
- Output: ~50 KB JSON

### Validation (3 conversations)
- Time: 2-3 minutes
- Memory: ~1-2 GB
- Output: 22 MB total

### Ablation Study (3 conditions × 10 trials × 8 inputs = 240 conversations)
- Time: 60-120 minutes (OpenRouter API)
- Memory: ~4-8 GB
- Output: 50-100 MB

### Dataset Collection (100 conversations)
- Time: 30-60 minutes (depends on scenario complexity)
- Memory: ~2-4 GB
- Output: 100+ MB

---

## Next Steps

1. **Try validation notebook** (5 min)
   ```bash
   jupyter notebook quick_validation.ipynb
   ```

2. **Run ablation study** (60 min)
   ```bash
   python run_ablation_study.py --trials 5
   ```

3. **Collect dataset** (30 min)
   ```bash
   python collect_dataset.py --target 100
   ```

4. **Analyze results** (15 min)
   ```bash
   jupyter notebook ablation_analysis.ipynb
   ```

5. **Read research progress**
   ```bash
   cat RESEARCH_PROGRESS.md
   ```

---

## Support

### Documentation Files
- `ARCHITECTURE.md` - Detailed system design
- `ADVANCED_NLP_FEATURES.md` - Emotion detection details
- `CALCULATION_VALIDATION.md` - Metric calculations
- `RESEARCH_PROGRESS.md` - Full project progress report

### Code Examples
- See `test_consciousness.py` for usage examples
- See `quick_validation.ipynb` for analysis patterns
- See `run_conversation_test.py` for runner usage

### Questions?
Check the docstrings in the code:
```bash
python -c "from consciousness_chatbot import ConsciousnessSimulator; help(ConsciousnessSimulator)"
```

---

*Last Updated: November 2, 2025*
*Version: 1.0 - Production Ready*
