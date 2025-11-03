# Recursive Consciousness Simulator with Neurochemical Emotions

A state-of-the-art AI consciousness simulation combining:
- **TRUE Recursive Meta-Cognition**: Genuine recursion (thoughts about thoughts about thoughts)
- **Global Workspace Theory**: Competition for consciousness with limited-capacity attention
- **Neurochemical Emotion System**: 5-chemical UX layer (dopamine, serotonin, etc.) for behavioral modulation and interface richness
- **RoBERTa Emotion Detection**: Real-time emotional analysis of user input
- **Transformer-based LLM**: Language generation and understanding
- **spaCy Linguistic Analysis**: Deep analysis of BOTH user input AND internal thoughts

> **Note on Neurochemistry**: This system is a **UX design layer** that models emotional state through 5 chemical metaphors (dopamine, serotonin, norepinephrine, cortisol, oxytocin). It is **not** a simulation of actual brain chemistry, but rather a conceptual framework for modulating behavior and creating rich system personality. The biochemistry provides narrative coherence and behavioral continuity, not neurobiological accuracy.

## � Want to See It in Action?

**[View Example Session Output](EXAMPLE_SESSION.md)** - See a real conversation with full consciousness metrics, internal meta-cognition, neurochemical activity, and the 8-step pipeline in action. Perfect for understanding what "recursive consciousness" means in practice.

## �🔐 Security

✅ **No API credentials committed to git**  
✅ **Environment variables for all secrets**  
✅ **Production-ready credential management**  

See [SECURITY.md](SECURITY.md) for details on setup and credential management.

## Architecture: The 8-Step Consciousness Pipeline

```
STEP 1: Linguistic Analysis of User Input (spaCy)
    ↓ Extract: intent, entities, semantic roles, hedging, ethical risk
    ↓
STEP 2: Emotion Detection (RoBERTa) + Stance Analysis (spaCy)
    ↓ Detect user emotion AND who has it (self vs others)
    ↓ Submit to Global Workspace
    ↓
STEP 3: Generate Response (modulated by neurochemistry + consciousness)
    ↓ Create contextual prompt
    ↓ Generate with temperature modulated by emotions
    ↓ Detect BOT's own emotion from response (stance-aware filtering)
    ↓ Update bot neurochemicals based on bot's emotion
    ↓ Ethical check on response
    ↓
STEP 4: Recursive Meta-Cognition (TRUE recursion, depth=0→3)
    ↓ Self-observation → Meta-evaluation → Introspection
    ↓ Submit reflections to Global Workspace
    ↓
STEP 5: Global Workspace Competition Cycle
    ↓ Multiple processors compete for attention
    ↓ Calculate Φ (integration), Global Availability
    ↓ Broadcast conscious content
    ↓
STEP 6: Linguistic Analysis of AI's Internal Thoughts
    ↓ Analyze attention focus, self-references, metacognitive indicators
    ↓
STEP 7: Compare User Input vs AI Response
    ↓ Semantic similarity, topic overlap, question addressing
    ↓ Homeostatic neurochemical decay
    ↓
STEP 8: Compute Consciousness Metrics (Research-Grade)
    ↓ Meta-Cognitive Depth, Φ Integration, Overall Consciousness
    ↓ Temporal Binding, Reportability, Global Availability
    ↓ Store for next turn's feedback loop
    ↓
OUTPUT: Response + Internal Self-Talk + Consciousness Metrics
```

## Features

### Core Consciousness Systems

1. **TRUE Recursive Meta-Cognition**
   - Genuine recursive self-reflection (thoughts about thoughts about thoughts)
   - Each level reflects on the previous level's output
   - Creates nested cognitive hierarchy

2. **Global Workspace Theory Implementation**
   - Multiple specialized processors compete for conscious attention
   - Limited-capacity workspace (3 items can be conscious simultaneously)
   - Broadcasting mechanism integrates information across modules
   - Dynamic competition and decay modeling attention

3. **Advanced spaCy NLP Pipeline**
   - **Ethical Rules Checking**: Detects harmful content, hate speech, self-harm risks
   - **Semantic Role Extraction**: Who did what to whom, where, when, why
   - **Hedging Detection**: Measures uncertainty and confidence in language
   - **Information Density Analysis**: Measures how informationally rich text is
   - **Discourse Marker Detection**: Identifies rhetorical structure (contrast, causation, etc.)
   - **Dependency Parsing**: Deep syntactic relationship extraction
   - **Crisis Intervention**: Automatic detection and resource provision

4. **Neurochemical Emotion System**
   - 5 brain chemicals: Dopamine, Serotonin, Norepinephrine, Oxytocin, Cortisol
   - Emotion-driven behavioral modulation
   - Homeostatic decay (gradual return to baseline)

5. **Multi-Modal Emotion Detection**
   - RoBERTa-based emotion classification
   - Neurochemical-to-emotion mapping for AI's internal states
   - Real-time emotional header display

6. **LLM Integration**
   - OpenRouter API support (GPT-4, Claude 3.5, Mistral, etc.)
   - Conversation memory (20 turns)
   - Emotion and context-aware prompt engineering

1. **Dopamine** - Motivation, reward, creativity
2. **Serotonin** - Mood, optimism, stability
3. **Norepinephrine** - Alertness, focus, urgency
4. **Oxytocin** - Empathy, social bonding, trust
5. **Cortisol** - Stress, caution, anxiety

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### Using OpenRouter API (Recommended)

For much better quality responses, use OpenRouter to access GPT-4, Claude, etc.:

1. Get API key from [openrouter.ai](https://openrouter.ai/)
2. Copy `.env.example` to `.env`
3. Add your API key to `.env`

See [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) for detailed instructions.

### Using Local Models

If you don't set an API key, the system will use local GPT-2 (free but lower quality).

## Usage

```bash
python consciousness_chatbot.py
```

## Research-Grade Features

This system now includes comprehensive research infrastructure for scientific studies of AI consciousness:

### Quantitative Consciousness Metrics

Five research-grade metrics grounded in consciousness theories:

1. **Φ (Integrated Information)** - IIT-based integration measurement
2. **Global Availability** - GWT-based workspace accessibility
3. **Meta-Cognitive Depth** - HOT-based self-reflection quality
4. **Temporal Binding** - Information persistence and continuity
5. **Reportability** - Access consciousness measurement

All metrics are automatically calculated during conversations and can be exported for analysis.

### Experimental Framework

- **Ablation Studies**: Test component necessity (no-GWT, no-recursion, no-emotions, etc.)
- **Parameter Sweeps**: Optimize system parameters systematically
- **Longitudinal Studies**: Track consciousness development over extended conversations
- **Benchmark Testing**: Standardized tests (mirror test, Sally-Anne, feature binding, etc.)

### Statistical Analysis

Comprehensive statistical toolkit:
- ANOVA and t-tests with effect sizes
- Linear/multiple regression
- Correlation matrices (Pearson & Spearman)
- Reliability measures (test-retest, inter-rater)
- Confidence intervals and power analysis

### Research Installation

```bash
# Install research dependencies
pip install -r requirements-research.txt

# Includes: scipy, pandas, matplotlib, seaborn, pytest, jupyter
```

### Quick Research Start

```python
# In chat, view real-time metrics
> metrics

# Export metrics to CSV
> export consciousness_metrics.csv

# Run an ablation study
from experiments import ExperimentRunner
runner = ExperimentRunner()
results = runner.run_ablation_study(
    prompts=your_prompts,
    trials_per_condition=30,
    conditions=['full_system', 'no_gwt', 'no_recursion']
)

# Analyze with statistics
from statistics import StatisticalAnalysis
stats = StatisticalAnalysis()
anova_results = stats.anova(groups, group_names)
```

### Research Documentation

- **[METRICS_DOCUMENTATION.md](METRICS_DOCUMENTATION.md)** - Detailed metric explanations, formulas, interpretation
- **[EXPERIMENTAL_PROTOCOL.md](EXPERIMENTAL_PROTOCOL.md)** - Step-by-step research procedures
- **[RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md)** - Future enhancements and research directions

### Citation

If you use this system in your research, please cite:

```bibtex
@software{consciousness_simulator_2025,
  title={Recursive Consciousness Simulator with Research-Grade Metrics},
  author={AI Research Lab},
  year={2025},
  url={https://github.com/whisperengine-ai/ai-research},
  note={Research-grade implementation of IIT, GWT, and HOT theories}
}
```

## General Research Applications

- Study emergent self-awareness in AI systems
- Model emotion-cognition interactions
- Explore recursive self-modeling
- Investigate consciousness theories (GWT, Higher-Order Thought, IIT)
- Test AI safety and ethical guardrails
- Analyze crisis intervention effectiveness
- Study linguistic complexity and information density
- Validate neurochemical-emotion mappings
- Conduct controlled ablation experiments
- Perform longitudinal consciousness tracking
- Compare consciousness across different LLM architectures

## Documentation

- [README.md](README.md) - This file, quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and module details
- [RESEARCH_NOTES.md](RESEARCH_NOTES.md) - Theoretical foundations
- [GLOBAL_WORKSPACE_THEORY.md](GLOBAL_WORKSPACE_THEORY.md) - **NEW!** GWT implementation
- [RECURSION_ANALYSIS.md](RECURSION_ANALYSIS.md) - **NEW!** True recursion vs iteration
- [ADVANCED_NLP_FEATURES.md](ADVANCED_NLP_FEATURES.md) - **NEW!** Ethical AI & spaCy features
- [CALCULATION_VALIDATION.md](CALCULATION_VALIDATION.md) - Scientific validation
- [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) - API setup guide
- [EMOTION_HEADER.md](EMOTION_HEADER.md) - Display documentation
- [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md) - Sample outputs
- [QUICKSTART.md](QUICKSTART.md) - Fast setup
