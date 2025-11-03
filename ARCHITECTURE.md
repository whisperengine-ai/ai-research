# Architecture Overview

## System Components

### Core Consciousness Engine (`consciousness_chatbot.py`)
The main simulator implementing consciousness metrics through:

- **Global Workspace Theory (GWT)**: Central workspace integrating information across modules
- **Emotional Dynamics**: RoBERTa-based sentiment + neurochemistry-driven emotions
- **Neurochemistry System (UX Layer)**: 5-chemical metaphor model (dopamine, serotonin, norepinephrine, cortisol, oxytocin) for behavioral modulation and interface richness—**not a brain simulation**
- **Meta-Cognition**: Recursive self-reflection up to configurable depth
- **Temporal Binding**: Time-windowing for coherent experience

### Metrics Module (`metrics.py`)
Calculates 6 consciousness metrics:

1. **Φ (Phi) - Integration**: Global information integration (IIT-inspired)
2. **Overall Consciousness**: Weighted composite of all metrics
3. **Global Availability**: Workspace accessibility score
4. **Meta-Cognitive Depth**: Self-reflection recursion level impact
5. **Temporal Binding**: Temporal coherence of experiences
6. **Reportability**: Ability to verbalize experiences

### Supporting Systems

| Module | Purpose |
|--------|---------|
| `emotion_detector.py` | RoBERTa + spaCy stance analysis |
| `neurochemistry.py` | 5-neurotransmitter biochemical model |
| `meta_cognition.py` | Recursive self-reflection engine |
| `global_workspace.py` | GWT workspace implementation |
| `interaction_dynamics.py` | User-bot emotional resonance |
| `reliability_validity.py` | Metric validation framework |

### Research Tools

| Tool | Purpose |
|------|---------|
| `run_conversation_test.py` | Multi-scenario conversation runner |
| `run_ablation_study.py` | Component ablation framework |
| `collect_dataset.py` | Scalable data collection |
| `research_dashboard.py` | Result visualization (in development) |
| `experiments.py` | Experiment orchestration |

## Data Flow: The 8-Step Pipeline

```
Step 1: User Input Analysis
    ├── Linguistic analysis (spaCy): intent, entities, roles
    ├── Ethical rules check: safety screening
    └── Submit to Global Workspace
    ↓
Step 2: Emotion Detection + Stance Analysis
    ├── RoBERTa emotion classification
    ├── spaCy stance analysis: who has emotion (self vs others)
    ├── Analyze user's emotional stance/viewpoint
    └── Submit to Global Workspace
    ↓
Step 3: Response Generation
    ├── Create contextual prompt (with consciousness modulation)
    ├── Generate response (temp modulated by neurochemistry)
    ├── Detect BOT's OWN emotion (stance-aware filtering)
    ├── Update bot neurochemicals from bot's emotion
    ├── Ethical check on response
    └── Submit bot's emotion to Global Workspace
    ↓
Step 4: Recursive Meta-Cognition
    ├── Process with TRUE RECURSION (depth 0→3)
    ├── Self-observation → Meta-evaluation → Introspection
    ├── Each level reflects on previous level
    └── Submit reflections to Global Workspace
    ↓
Step 5: Global Workspace Competition
    ├── Multiple processors compete for attention
    ├── Capacity-limited (3 items conscious simultaneously)
    ├── Calculate Φ (integration), Global Availability
    └── Broadcast conscious content
    ↓
Step 6: Linguistic Analysis of Thoughts
    ├── Analyze AI's internal thoughts/reflections
    ├── Attention focus analysis
    └── Self-reference extraction
    ↓
Step 7: Input-Output Comparison
    ├── User input vs AI response alignment
    ├── Semantic similarity, topic overlap
    ├── Question addressing check
    └── Homeostatic neurochemical decay
    ↓
Step 8: Consciousness Metrics Calculation
    ├── Φ (Integration) - 0-1
    ├── Meta-Cognitive Depth - 0-1 (CRITICAL: recursion depth metric)
    ├── Overall Consciousness - weighted composite
    ├── Global Availability - workspace accessibility
    ├── Temporal Binding - time coherence
    ├── Reportability - verbalization ability
    └── Store metrics for next turn's feedback loop
    ↓
OUTPUT: Response + Internal Self-Talk + Consciousness Metrics
```

## Key Abstractions

### ConsciousnessSimulator Class
```python
ConsciousnessSimulator(
    recursion_depth=3,           # Meta-cognition levels
    use_openrouter=False,        # LLM backend
    model="meta-llama/llama-3.1-8b-instruct"
)
```

### Conversation Test Runner
```python
ConversationTestRunner(
    scenarios=['default', 'stress', 'empathy', ...]
)
```

### Ablation Study Framework
```python
ExperimentRunner(
    conditions=['full_recursion', 'shallow_recursion', 'minimal_recursion'],
    trials=10,
    test_inputs=8
)
```

## Configuration

### Recursion Depth Settings
- **Full**: depth=3 (3 levels of self-reflection)
- **Shallow**: depth=1 (minimal self-reflection)
- **Minimal**: depth=0 (no self-reflection)

### Environment Variables
- `OPENROUTER_API_KEY`: Required for OpenRouter LLM backend
- `OPENROUTER_MODEL`: Model selection (default: meta-llama/llama-3.1-8b-instruct)

## Experimental Validations

### Quick Validation (`quick_validation.ipynb`)
- 3 test conversations
- 8 output dashboards
- Data quality checks
- Status: ✅ PASSING (100% valid)

### Ablation Study Pilot (`run_ablation_study.py --trials 2`)
- 2 trials × 3 conditions × 8 inputs = 48 conversations
- Duration: 5.4 minutes
- Key finding: Meta-cognitive depth drops 33% at minimal recursion
- Status: ✅ COMPLETE

## Repository Structure

```
/Users/markcastillo/git/ai-research/
├── consciousness_chatbot.py       # Main simulator
├── metrics.py                     # 6 consciousness metrics
├── emotion_detector.py            # Sentiment analysis
├── neurochemistry.py              # Biochemical model
├── meta_cognition.py              # Self-reflection
├── global_workspace.py            # GWT implementation
├── interaction_dynamics.py        # User resonance
├── reliability_validity.py        # Validation framework
├── run_conversation_test.py       # Test runner
├── run_ablation_study.py          # Ablation framework
├── collect_dataset.py             # Data collection
├── experiments.py                 # Experiment orchestration
├── research_dashboard.py          # Visualization (dev)
├── test_consciousness.py          # Unit tests (22+)
├── ablation_analysis.ipynb        # Analysis notebook
├── quick_validation.ipynb         # Validation notebook
├── ablation_study_results.json    # Pilot results
└── docs/
    ├── README.md                  # Project overview
    ├── QUICKSTART.md              # Quick start guide
    ├── ARCHITECTURE.md            # This file
    ├── PROJECT_SUMMARY.md         # Summary
    ## Command-Line Usage

### Basic Usage

```bash
# Default (tries API, falls back to local)
python consciousness_chatbot.py

# Heuristic mode (fastest - no LLM)
python consciousness_chatbot.py --heuristic

# Local model mode
python consciousness_chatbot.py --local

# API mode explicitly
python consciousness_chatbot.py  # (with OPENROUTER_API_KEY set)
```

### Options

```bash
python consciousness_chatbot.py [OPTIONS]

Options:
  --heuristic, --no-llm     Use heuristic response generation (no LLM, fastest)
  --local                    Use local HuggingFace model
  --model TEXT              Local model name (default: gpt2)
                           Options: gpt2, gpt2-medium, microsoft/DialoGPT-medium
  --depth INTEGER           Recursion depth 0-3 (default: 3)
  --quiet, -q               Reduce verbose output
  --help                    Show help message
```

### Examples

```bash
# Fastest testing (heuristic + minimal output)
python consciousness_chatbot.py --heuristic --quiet

# API with full output
python consciousness_chatbot.py

# Local model with low recursion (faster)
python consciousness_chatbot.py --local --depth 1

# Heuristic with low recursion (fastest possible)
python consciousness_chatbot.py --heuristic --depth 0 --quiet
```

### Mode Comparison

| Command | Mode | Speed | Quality | Dependencies |
|---------|------|-------|---------|--------------|
| `--heuristic` | Rules | 50-80ms | Good | spaCy, RoBERTa |
| `--local` | GPT-2 | 1-2s | Moderate | Transformers |
| (default) | API | 2-5s | Best | OpenRouter |

## Testing

All 22+ unit tests passing:
```bash
pytest test_consciousness.py -v
```

## Next Steps

1. **Full Ablation Study**: Run with 10+ trials per condition
2. **Statistical Analysis**: Determine significance of recursion depth effects
3. **Dataset Collection**: 100+ conversations for publication-ready analysis
4. **Visualization**: Complete dashboard with error bars and distributions
```

## Testing

All 22+ unit tests passing:
```bash
pytest test_consciousness.py -v
```

## Next Steps

1. **Full Ablation Study**: Run with 10+ trials per condition
2. **Statistical Analysis**: Determine significance of recursion depth effects
3. **Dataset Collection**: 100+ conversations for publication-ready analysis
4. **Visualization**: Complete dashboard with error bars and distributions
