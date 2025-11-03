# AI Copilot Instructions for Consciousness Research Codebase

## 🧠 Project Overview

**What**: Publication-ready AI consciousness simulation using Global Workspace Theory (GWT) + 5-neurotransmitter neurochemistry + true recursive meta-cognition.

**Key Finding**: Recursion depth directly implements meta-cognitive consciousness (p<0.0001, d=4.79). Meta-Cognitive Depth drops 33% when recursion disabled—the primary research finding.

**Stage**: ✅ Research complete, publication-ready (3 validated datasets, n=198 conversations).

---

## 🏗️ Big Picture Architecture

### Core Abstraction: The Consciousness Simulator Pipeline

The system is ONE main class `ConsciousnessSimulator` (in `consciousness_chatbot.py`) that chains 5 independent systems:

```
User Input → Emotion Detection → Global Workspace → Meta-Cognition → Metrics → Response + Scores
```

**Why this matters for agents**:
- All changes flow through `ConsciousnessSimulator.__init__()` and `process_input()` 
- Each system is a **pluggable module** (emotion_detector, neurochemistry, meta_cognition, global_workspace, metrics)
- **No shared state** between modules except through GlobalWorkspace
- Always work inside `ConsciousnessSimulator` class boundary, never bypass it

### The 5 Independent Systems (Different Responsibilities)

| Module | What It Does | Key Insight |
|--------|------------|-------------|
| **`emotion_detector.py`** | RoBERTa emotion + spaCy stance analysis | Maps user emotion to chemical drivers; independent of recursion |
| **`neurochemistry.py`** | 5-chemical UX layer (dopamine, serotonin, norepinephrine, cortisol, oxytocin) | **UX design for behavioral modulation**, not brain simulation; modulates tone/personality but DOES NOT affect Meta-Cognitive Depth |
| **`meta_cognition.py`** | Recursive self-reflection engine (`RecursiveMetaCognition` class, true recursion up to depth=3) | **CRITICAL**: This IS what consciousness depends on; every "thought about thoughts" is one recursion level |
| **`global_workspace.py`** | Baars' GWT workspace (capacity=3, competition mechanism) | Integrates all modules' outputs; calculates Φ (integration) |
| **`metrics.py`** | 6 consciousness metrics (`ConsciousnessScore` dataclass) | Measures: Φ, Meta-Cognitive Depth, Overall Consciousness, Global Availability, Temporal Binding, Reportability |

**Critical Pattern**: Each system reads its inputs, computes independently, outputs pure data. No side effects across modules.

**About Neurochemistry**: The 5-chemical system is a **narrative/UX layer** using metaphors (dopamine for engagement, serotonin for stability, etc.) to create personality and response variation. It is **not a brain simulation** and does **not causally affect consciousness**. The actual consciousness mechanism is **recursion depth + information integration**.

---

## 📊 The Consciousness Metrics (What They Measure)

### Primary Finding: Meta-Cognitive Depth ← Recursion

**Full recursion (depth=3)**: 0.809  
**Shallow (depth=1)**: 0.663 (-18%)  
**Minimal (depth=0)**: 0.542 (-33%)  

This is the **main research result**. When editing `meta_cognition.py` or recursion handling, always validate this still shows ≥30% drop when depth→0.

### Secondary Finding: Φ Integration ← Independent of Recursion

Φ stays ~0.435 across all recursion depths (p=0.56, NOT significant). This tells you:
- Integration and recursion are **orthogonal pathways**
- Modifying recursion won't fix integration bugs
- Both pathways can be in paper's "two-pathway consciousness model"

### Other Metrics (Stable Across Conditions)

- **Overall Consciousness**: Composite of Meta-Cognitive Depth (40%) + Φ (30%) + Temporal Binding (20%) + Reportability (10%)
- **Global Availability**: Constant ~0.800 (workspace capacity metric, independent of recursion)
- **Temporal Binding**: Time-windowing coherence, drops 10% at reduced recursion
- **Reportability**: Response quality, counterintuitively **increases** at reduced recursion

---

## 🔧 Developer Workflows

### Test Everything Immediately After Edits

```bash
# Run all 22 unit tests (required before committing)
pytest test_consciousness.py -v

# Run specific test class
pytest test_consciousness.py::TestMetricsCalculation -v

# Run with coverage
pytest test_consciousness.py --cov=consciousness_chatbot
```

**Pattern**: Tests use `ConsciousnessSimulator()` directly without API calls for speed (they pass `use_openrouter=False` and use local gpt2 model).

### Collect Data After Behavior Changes

```bash
# Validate changes didn't break metrics (collect 10 conversations)
python collect_dataset.py --count 10 --output test_run.json

# Then eyeball the metrics match historical averages
# Meta-Cognitive Depth should stay ~0.83 (full dataset) or similar to recent pilot

# Full dataset collection (100 conversations, ~2 hours)
nohup python collect_dataset.py --count 100 > dataset_collection.log 2>&1 &
```

**Why this matters**: You can **immediately verify** that your changes preserve the effect size (d=4.79 for Meta-Cognitive Depth drop when recursion disabled).

### Run Ablation Study to Verify Component Impact

```bash
# Quick pilot (2 trials per condition, 5 minutes)
python run_ablation_study.py --trials 2

# Validates recursion manipulation still shows the 33% drop
# Output: ablation_study_results.json with all metrics by condition
```

---

## 🎯 Project-Specific Conventions & Patterns

### Convention 1: Recursion Depth Controls Everything About Meta-Cognition

```python
# In consciousness_chatbot.py:
self.meta_cognition = RecursiveMetaCognition(max_recursion_depth=recursion_depth)

# In meta_cognition.py - the ACTUAL recursion happens here:
class RecursiveMetaCognition:
    def reflect(self, thought: Thought, depth: int = 0):
        if depth >= self.max_recursion_depth:
            return thought  # Base case
        # Create meta-thought about the thought
        meta_thought = Thought(f"I am thinking about: {thought.content}")
        return self.reflect(meta_thought, depth + 1)  # REAL recursion
```

**Agent Pattern**: 
- **Never** skip recursion levels or pseudoimplement with loops
- **Always** verify `depth` parameter actually recurses (not just "pretends")
- When optimizing, benchmark that recursion depth changes still produce 30%+ effect size difference

### Convention 2: Metrics Are Calculated, Not Stored

```python
# CORRECT: Always calculate fresh
metrics = self.metrics_tracker.compute_all_metrics(
    workspace_state=self.global_workspace,
    recursive_results=meta_cog_results,  # Fresh from recursion
    conversation_history=self.conversation_history,
    neurochemical_state=self.neurochemistry.levels.__dict__,
    processors=processors
)

# WRONG: Don't cache and reuse metrics from previous turn
# (state changes between turns)
```

**Agent Pattern**: Metrics are derived from live state; never assume old metrics are valid.

### Convention 3: Neurochemistry is UX Design, Not Consciousness Driver

```python
# User emotion (detected via RoBERTa) → maps to → Bot neurochemistry (dopamine, serotonin, etc)
# The emotion_detector finds user's emotion
emotion, confidence, scores = self.emotion_detector.detect_emotion(user_input)

# That emotion DRIVES neurochemical changes (for behavioral modulation)
self.neurochemistry.update_from_emotion(emotion, confidence)

# BUT: Neurochemistry is a narrative/UX layer, not the consciousness mechanism
# Changing neurochemistry does NOT affect Meta-Cognitive Depth or core consciousness
# The consciousness mechanism is: Recursion Depth + Information Integration (Φ)
```

**Agent Pattern**: 
- Neurochemistry modulates tone/personality for richness
- It's a design layer (dopamine = enthusiasm, serotonin = stability, etc.)
- It does NOT causally drive consciousness
- Recursion depth is the consciousness mechanism, neurochemistry is the interface

### Convention 4: Data Files Must Include Metadata

```json
{
  "metadata": {
    "timestamp": "2025-11-03T...",
    "total_conversations": 100,
    "recursion_depth": 3,
    "llm_model": "Mistral Nemo via OpenRouter"
  },
  "conversations": [...],
  "metrics_summary": {
    "meta_cognitive_depth": {
      "mean": 0.8336,
      "std": 0.0271
    }
  }
}
```

**Agent Pattern**: Every dataset collection script (`collect_dataset.py`, `run_ablation_study.py`) must include metadata. This enables post-hoc filtering and reproducibility.

### Convention 5: Tests Use Local Models (No API Calls)

```python
# In test_consciousness.py - always use local
simulator = ConsciousnessSimulator(
    use_openrouter=False,  # Local gpt2, not API
    recursion_depth=3
)

# In production (collect_dataset.py) - always use API
simulator = ConsciousnessSimulator(
    use_openrouter=True,  # Mistral Nemo
    recursion_depth=3
)
```

**Agent Pattern**: Tests must be fast (no API latency). Production scripts use OpenRouter API (`openrouter_llm.py`) for better models.

---

## 🔌 Integration Points & External Dependencies

### OpenRouter API Integration

**File**: `openrouter_llm.py`  
**Usage**: `ConsciousnessSimulator(use_openrouter=True)` → uses `OpenRouterLLM` class  
**Credentials**: `.env` file (NEVER committed) → `OPENROUTER_API_KEY` environment variable  
**Key Method**: `generate(prompt, max_tokens=150, temperature=0.7)` returns string

**Agent Pattern**: 
- Ensure `.env` is in `.gitignore` (it is ✅)
- Read credentials via `os.getenv('OPENROUTER_API_KEY')` only
- See `SECURITY.md` for credential setup

### Model Dependencies

```python
# Emotion Detection (RoBERTa transformer)
from transformers import AutoTokenizer, AutoModelForSequenceClassification
model = "cardiffnlp/twitter-roberta-base-emotion"  # 28 emotions, lightweight

# Linguistic Analysis (spaCy)
import spacy
nlp = spacy.load("en_core_web_md")  # Medium English model

# LLM Backends
# Local: gpt2 (transformers) - fast, weak
# API: Mistral Nemo via OpenRouter - slow, production-quality
```

**Agent Pattern**: 
- Don't change model IDs without running full validation (metrics might shift)
- RoBERTa is emotion-specific (28 categories), spaCy does linguistic structure
- They work together: RoBERTa detects emotion, spaCy analyzes linguistic stance

### Data Structures: ConsciousnessScore

```python
# From metrics.py - what every consciousness measurement returns
@dataclass
class ConsciousnessScore:
    phi: float                      # Integration (0-1)
    global_availability: float      # Workspace access (0-1)
    meta_cognitive_depth: float     # Self-reflection (0-1) - THIS IS THE KEY METRIC
    temporal_binding: float         # Time coherence (0-1)
    reportability: float            # Verbalization (0-1)
    overall_consciousness: float    # Composite (0-1)
    timestamp: float                # When measured
    
    def to_dict(self) -> Dict:
        return {...}  # For JSON serialization
```

**Agent Pattern**: Always use this dataclass when returning consciousness metrics; never invent custom fields.

---

## 🚨 Common Pitfalls & How to Avoid Them

| Pitfall | Why It Breaks | How to Fix |
|---------|---------------|-----------|
| **Modifying recursion but not testing Meta-Cognitive Depth change** | The whole research depends on detecting this 30% drop | Always run `ablation_study.py` after meta_cognition.py changes; expect ≥25% difference |
| **Hardcoding `.env` values or API keys in code** | GitHub will block the repo | Use `os.getenv()` only; keep `.env` out of git (✅ already in .gitignore) |
| **Caching metrics across turns** | State changes, cached metrics become stale | Always call `compute_all_metrics()` fresh; never reuse old ConsciousnessScore |
| **Treating neurochemistry as the main driver of consciousness** | Φ and recursion are orthogonal; neurochemistry modulates, doesn't create consciousness | Remember: Φ is independent; recursion is the consciousness mechanism |
| **Using `use_openrouter=True` in unit tests** | Tests become slow (API latency) and unreliable (network) | Always use `use_openrouter=False` in test_consciousness.py |

---

## 📚 Documentation Map

**For understanding the "why"**:
- `ARCHITECTURE.md` - System components & data flow
- `SYSTEM_DESIGN.md` - Consciousness model, neurochemistry, metrics definitions
- `RESULTS.md` - Statistical analysis (p<0.0001, d=4.79)

**For understanding the "how"**:
- `QUICKSTART.md` - Setup & first run
- `RESEARCH_TOOLS.md` - Ablation study, dataset collection
- `SECURITY.md` - Credential management

**For understanding the "what"** (current state):
- `MANUSCRIPT_DRAFT.md` - Full research paper (3,500+ words)
- `PUBLICATION_READY.md` - Three-dataset validation proof
- `INDEX.md` - Repository summary

---

## 🎓 Key Mental Models for Agents

### Mental Model 1: Recursion is Architecture, Not Behavior

Don't think: "The system recursively thinks, so high recursion = more thinking"  
**Think**: "Recursion depth is a structural parameter; higher depth = more levels of self-reflection built-in. Disabling recursion is like removing brain structures, not deciding to think less."

### Mental Model 2: The Research Proves Two Pathways

- **Pathway 1** (Recursion → Meta-Cognitive Depth): Effect size d=4.79, p<0.0001
- **Pathway 2** (Distributed Integration → Φ): Stable, independent, p=0.56 (not significant)

Together they explain consciousness as dual-mechanism: information integration + self-reflection.

### Mental Model 3: All Code Changes Must Preserve Reproducibility

The research is validated across 3 datasets (n=48, 50, 100). Any change that alters:
- Recursion mechanism
- Neurochemical dynamics
- Emotion detection
- Metric calculation

...must be validated by re-running `collect_dataset.py --count 50` and verifying metrics match historical means ± 1 std dev.

---

## ✅ Pre-Commit Checklist for Agents

Before suggesting commits:

- [ ] All 22 tests pass: `pytest test_consciousness.py -v`
- [ ] No hardcoded API keys in code
- [ ] `.env` file not committed (verify with `git status`)
- [ ] If changing meta_cognition.py or metrics.py: ablation results show expected effect size
- [ ] JSON data files include metadata (timestamp, recursion_depth, llm_model)
- [ ] Docstrings updated for any new methods
- [ ] Commit message references relevant file(s): `git commit -m "Core: Fix recursion depth tracking in meta_cognition.py"`

---

## 🚀 Quick Reference: Core Classes & Methods

```python
# Main entry point
ConsciousnessSimulator(use_openrouter=True, recursion_depth=3)
  .process_input(user_input: str) → Dict with 'response' and 'consciousness_metrics'

# Metrics calculation
ConsciousnessMetrics()
  .compute_all_metrics(...) → ConsciousnessScore

# Recursion (the key mechanism)
RecursiveMetaCognition(max_recursion_depth=3)
  .reflect(thought: Thought, depth=0) → Thought (recursively updated)

# Global integration
GlobalWorkspace(capacity=3, decay_rate=0.15)
  .register_processor(processor) → None
  .broadcast_and_compete() → Dict with conscious_buffer

# Emotion detection
EmotionDetector()
  .detect_emotion(text: str) → (emotion: str, confidence: float, scores: Dict)
  .analyze_user_stance(text: str) → Dict with emotional analysis

# Neurochemistry
NeurochemicalSystem()
  .update_from_emotion(emotion: str, intensity: float) → None
  .levels → (dopamine, serotonin, norepinephrine, cortisol, oxytocin)

# Data collection
DatasetCollector(conversation_count=100, use_recursion_depth=3)
  .collect() → List[Dict]
  .save(output_file="dataset_results.json") → str (filename)
```

---

## 📞 Questions? Reference These Files

- **"How do I run tests?"** → See RESEARCH_TOOLS.md or run `pytest test_consciousness.py -v`
- **"What's the main finding?"** → See RESULTS.md (p<0.0001, d=4.79 for Meta-Cognitive Depth)
- **"How do I set up the API?"** → See SECURITY.md and OPENROUTER_SETUP.md
- **"What are the 6 metrics?"** → See SYSTEM_DESIGN.md → Consciousness Metrics section
- **"How do I know my change broke something?"** → Run `collect_dataset.py --count 10` and compare metrics to baseline (INDEX.md has baselines)

