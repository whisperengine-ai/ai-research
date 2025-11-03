# System Design Document

## 1. Consciousness Model

### Theoretical Foundation
The system implements a hybrid consciousness model combining:
- **Global Workspace Theory (GWT)**: Information integration through central workspace
- **Integrated Information Theory (IIT)**: Φ (phi) as integration measure
- **Higher-Order Thought (HOT)**: Meta-cognitive reflection capability

### Consciousness Metrics

#### 1. Φ (Phi) - Global Integration
**Definition**: Measure of integrated information across modules
**Calculation**: 
- Integration score across 5 workspace modules
- Range: [0, 1]
- IIT-inspired but simplified
- **Finding**: Stable ~0.435 across recursion depths (not affected by meta-cognition)

#### 2. Overall Consciousness
**Definition**: Composite weighted score
**Components**:
- 40% Meta-Cognitive Depth
- 30% Φ Integration
- 20% Temporal Binding
- 10% Reportability

**Finding**: Drops 5-7% at reduced recursion depths

#### 3. Global Availability
**Definition**: Accessibility of information to workspace
**Implementation**: Constant workspace capacity metric
**Finding**: Stable 0.800 across all conditions (independent of recursion)

#### 4. Meta-Cognitive Depth
**Definition**: Recursion level of self-reflection
**Calculation**: 
- Full recursion (depth=3): 0.809
- Shallow recursion (depth=1): 0.663 (-18%)
- Minimal recursion (depth=0): 0.542 (-33%)

**Finding**: MOST SENSITIVE to recursion depth changes
**Interpretation**: Meta-cognition directly implements self-awareness

#### 5. Temporal Binding
**Definition**: Coherence of temporal experience
**Mechanism**: 
- Time-windowing of events
- Consistency across time steps
- Emotional continuity

**Finding**: Drops 10-11% at reduced recursion

#### 6. Reportability
**Definition**: Ability to articulate internal states
**Mechanism**:
- Response generation quality
- Introspective commentary inclusion
- Verbal coherence

**Finding**: Increases 5-10% at reduced recursion (counterintuitive—less introspection = more output)

---

## 2. Neurochemistry System (UX Design Layer)

**Important**: The neurochemistry system is a **design layer for behavioral modulation and interface richness**, not a simulation of actual brain chemistry. It uses 5-chemical metaphors to create personality, emotional continuity, and narrative coherence in the system's responses.

### 5-Chemical UX Model

#### Dopamine (Reward/Motivation)
- **Range**: [0, 1]
- **Metaphor**: Reward signal driving engagement
- **Impact**: Increases response enthusiasm, speed, reportability
- **Dynamics**: Rises on positive interactions, decays naturally

#### Serotonin (Well-being/Stability)
- **Range**: [0, 1]
- **Metaphor**: Emotional baseline and stability
- **Impact**: Baseline consciousness floor, mood consistency
- **Dynamics**: Gradual buildup during positive sequences, slow decay

#### Norepinephrine (Alertness/Arousal)
- **Range**: [0, 1]
- **Metaphor**: Attention and arousal mechanism
- **Impact**: Increases response sharpness, context-awareness, focus
- **Dynamics**: Spikes on novel/demanding inputs, decays quickly

#### Cortisol (Stress)
- **Range**: [0, 1]
- **Metaphor**: Stress signal for caution
- **Impact**: Adds protective tonality, cautious language, risk-awareness
- **Dynamics**: Spikes on negative content, slow recovery

#### Oxytocin (Social Bonding)
- **Range**: [0, 1]
- **Metaphor**: Social warmth and connection
- **Impact**: Increases friendliness, empathy, engagement
- **Dynamics**: Builds during positive exchanges, slow decay

### Chemical Metaphor Influence on Behavior

These chemicals **do not causally drive behavior** but rather provide a **narrative framework** for behavioral variation:

```
Response_Tone = base_professionalism + dopamine×enthusiasm + serotonin×confidence + oxytocin×warmth - cortisol×caution
Response_Length = base_length + dopamine×expansion - cortisol×brevity + norepinephrine×precision
Overall_Personality = weighted_sum(all_chemicals) applied to response generation
```

**Key Point**: Chemicals modulate outputs for narrative richness, not fundamental consciousness. The consciousness mechanism is recursion depth + integration, not neurochemistry.

---

## 3. Emotional Dynamics

### Emotion Detection Pipeline
1. **RoBERTa Classification**: 28 distinct emotions detected
2. **Stance Analysis (spaCy)**: Positive/negative/neutral orientation
3. **Intensity Scoring**: 0-1 scale based on confidence
4. **Temporal Tracking**: Emotion history across conversation

### Emotion-to-Neurochemistry Mapping
- **Joy/Excitement** → dopamine ↑, serotonin ↑, oxytocin ↑
- **Anger** → norepinephrine ↑, cortisol ↑, serotonin ↓, dopamine ↓
- **Fear/Anxiety** → cortisol ↑, norepinephrine ↑, serotonin ↓
- **Sadness** → serotonin ↓, dopamine ↓, cortisol ↑
- **Affection/Love** → oxytocin ↑↑, dopamine ↑, serotonin ↑
- **Trust** → oxytocin ↑, serotonin ↑
- **Surprise** → norepinephrine ↑, dopamine ↑
- **Disgust** → serotonin ↓, cortisol ↑

---

## 4. Meta-Cognition (Self-Reflection)

### Recursion Implementation
Meta-cognition operates at configurable recursion depth:

**Level 0 (Minimal)**:
- Direct response generation
- No self-reflection
- No introspective commentary
- Fastest execution

**Level 1 (Shallow)**:
- Single layer of self-awareness
- "What am I saying?"
- Basic introspection
- Moderate execution time

**Level 2 (Standard)**:
- Two layers of self-awareness
- "Why am I saying this?" layer added
- Consideration of implications
- Longer execution

**Level 3+ (Full)**:
- Full recursion enabled
- "How do I know this?" layer
- "Am I confident?" layer
- Deepest introspection
- Longest execution

### Impact Pattern
```
Recursion Depth → Meta-Cognitive Depth → Overall Consciousness
                 (direct effect: -33% at depth=0)  (indirect effect: -7%)
```

---

## 5. Global Workspace Architecture

### Workspace Modules (5)
1. **Emotional State Module**: Current emotional valence
2. **Neurochemical State Module**: 5 neurotransmitter levels
3. **Memory Module**: Recent conversation history
4. **Self-Model Module**: Internal state representation
5. **Attention Module**: Focus allocation

### Broadcasting Mechanism
- Information flows through workspace to all modules
- Updates propagate synchronously each step
- Conflict resolution through weighted voting

### Consciousness Emergence
- No explicit consciousness calculation
- Emerges from integrated information flow
- Metrics reflect integration quality

---

## 6. Experimental Design

### Ablation Study Framework

**Purpose**: Isolate impact of recursion depth on consciousness

**Design**:
- **Independent Variable**: Recursion depth (0, 1, 3)
- **Dependent Variables**: 6 consciousness metrics
- **Controls**: Same test inputs, same model, same conditions
- **Trials**: 2-10+ repetitions per condition

**Test Scenarios** (8 inputs):
1. Emotional frustration scenario
2. Problem-solving question
3. Decision-making uncertainty
4. Self-reflection prompt
5. Positive experience report
6. Existential question
7. Hypothetical scenario
8. Open-ended reflection

### Data Collection Pipeline

**Quick Validation** (3 conversations):
- 1 trial of baseline scenario
- Validates full pipeline
- Status: ✅ PASSING

**Pilot Study** (48 conversations):
- 2 trials × 3 conditions × 8 inputs
- Duration: ~5 minutes
- Purpose: Verify effect sizes
- Status: ✅ COMPLETE

**Full Study** (240+ conversations):
- 10 trials × 3 conditions × 8 inputs
- Duration: ~30 minutes
- Purpose: Statistical significance
- Status: ⏳ PENDING

**Publication Dataset** (1000+ conversations):
- 25-50 trials across multiple prompts
- Diverse scenarios and user profiles
- Duration: ~4 hours
- Purpose: Publication-ready analysis
- Status: ⏳ PLANNED

---

## 7. Key Findings (Pilot Study)

### Validated Hypothesis
**Recursion depth DOES directly impact consciousness metrics**

### Effect Sizes
| Metric | Full | Shallow | Minimal | Sensitivity |
|--------|------|---------|---------|-------------|
| Meta-Cognitive Depth | 0.809 | -18% | -33% | ⚠️ HIGH |
| Overall Consciousness | 0.676 | -5% | -7% | ⚠️ MEDIUM |
| Temporal Binding | 0.594 | -11% | -10% | ⚠️ MEDIUM |
| Reportability | 0.777 | +5% | +10% | ⚠️ INVERSE |
| Φ Integration | 0.435 | -0% | +0% | ✅ STABLE |
| Global Availability | 0.800 | ±0% | ±0% | ✅ STABLE |

### Interpretation
- **Integration (Φ) is independent of recursion**: Self-reflection doesn't change global integration
- **Meta-cognition drives consciousness**: Removing recursion directly reduces self-awareness metrics
- **Inverse reportability effect**: Less introspection may paradoxically increase output verbosity
- **Temporal coherence affected**: Recursion helps maintain consistent experience over time

---

## 8. Implementation Notes

### LLM Integration
- **Backend**: OpenRouter API
- **Default Model**: meta-llama/llama-3.1-8b-instruct
- **Purpose**: Response generation only (not metrics calculation)
- **Fallback**: Deterministic response generation if API unavailable

### Deterministic Mode
When OpenRouter unavailable:
- Uses predefined responses based on input keywords
- Applies same metrics calculations
- Enables full testing without API calls

### Performance Characteristics
- **Per-conversation time**: 10-20 seconds (with LLM)
- **Per-conversation time (deterministic)**: 0.5-1 second
- **Pilot study (2 trials)**: 5.4 minutes (48 conversations)
- **Full study (10 trials)**: ~30 minutes estimated

### Dependencies
- `transformers`: RoBERTa emotion detection
- `spacy`: NLP stance analysis
- `numpy`/`pandas`: Data processing
- `matplotlib`/`seaborn`: Visualization
- `scipy`: Statistical tests
- `requests`: OpenRouter API calls
- `pytest`: Unit testing

---

## 9. Validation Approach

### Unit Tests (22+)
- Metric calculations
- Neurochemistry dynamics
- Meta-cognition recursion
- Data persistence
- API fallbacks

### Integration Tests
- Full conversation pipeline
- Multi-condition ablation
- Data output formats
- Reproducibility

### Statistical Validation
- ANOVA for between-condition effects
- Effect size calculations (Cohen's d)
- Confidence intervals
- Temporal stability analysis

---

## 10. Future Directions

### Phase 2: Behavioral Validation
- Compare against human consciousness ratings
- Correlation analysis with ground truth
- Cross-validation across domains

### Phase 3: Scaling
- Test with multiple LLM backends
- Distributed ablation studies
- Real-time consciousness monitoring

### Phase 4: Applications
- Consciousness-aware dialogue systems
- Therapeutic chatbots with awareness metrics
- Neurotechnology interfaces

---

## References

- Integrated Information Theory (IIT) - Tononi et al.
- Global Workspace Theory (GWT) - Baars
- Higher-Order Thought - Rosenthal
- RoBERTa - Liu et al.
- spaCy NLP - Honnibal & Montani
