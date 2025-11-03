# 🧠 System Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT (Text)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              EMOTION DETECTION (RoBERTa)                         │
│  • Analyzes emotional content                                    │
│  • Returns: emotion type, confidence, all scores                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           NEUROCHEMICAL SYSTEM (5 Chemicals)                     │
│  • Updates based on detected emotion                             │
│  • Dopamine, Serotonin, Norepinephrine, Oxytocin, Cortisol     │
│  • Generates behavioral modulation parameters                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         LANGUAGE GENERATION (Transformer LLM)                    │
│  • Creates contextual prompt with emotional state                │
│  • Temperature modulated by neurochemistry                       │
│  • Generates primary response                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         RECURSIVE META-COGNITION (3 Levels)                      │
│  Level 0: Direct response                                        │
│  Level 1: "What am I thinking?" (self-observation)              │
│  Level 2: "How confident am I?" (meta-evaluation)               │
│  Level 3: "Why did I think that?" (introspection)               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              WORKING MEMORY (Capacity: 7)                        │
│  • Stores recent thoughts with attention weights                │
│  • Maintains consciousness stream                                │
│  • Provides context for meta-cognition                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         LINGUISTIC ANALYSIS (spaCy)                              │
│  • Analyzes internal thoughts                                    │
│  • Extracts entities, concepts, attention focus                  │
│  • Detects self-references (meta-cognitive indicator)            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              HOMEOSTATIC REGULATION                              │
│  • Gradual decay toward neurochemical baseline                   │
│  • Maintains stability over time                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OUTPUT TO USER                                 │
│  • Primary response                                              │
│  • Meta-cognitive reflections                                    │
│  • Consciousness metrics display                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Turn 1: User says "I'm so excited about this project!"

```
1. INPUT PROCESSING
   └─> "I'm so excited about this project!"

2. EMOTION DETECTION (RoBERTa)
   └─> Detected: JOY (confidence: 92%)
   └─> Scores: {joy: 0.92, excitement: 0.81, neutral: 0.08}

3. NEUROCHEMISTRY UPDATE
   └─> Dopamine: 0.50 → 0.74 (+0.24) ⬆️
   └─> Serotonin: 0.50 → 0.66 (+0.16) ⬆️
   └─> Oxytocin: 0.50 → 0.58 (+0.08) ⬆️

4. CONVERSATION MEMORY UPDATE
   └─> Stores: "I'm so excited about this project!"
   └─> Memory: [1/20 turns]

5. BEHAVIORAL MODULATION
   └─> Creativity: 0.72 (high)
   └─> Positivity: 0.70 (high)
   └─> Empathy: 0.61 (moderate-high)
   └─> Temperature: 0.89 (more creative)

6. LLM GENERATION
   └─> Prompt: "Conversation history:\n[last 10 turns]\n\nRespond in a creative and expressive manner to: ..."
   └─> Response: "That's wonderful! Your enthusiasm is contagious..."

7. RECURSIVE META-COGNITION
   Level 0: [Response] "That's wonderful! Your enthusiasm is contagious..."
   Level 1: [Observation] "I notice I'm matching their positive energy"
   Level 2: [Evaluation] "This feels authentic and appropriate"
   Level 3: [Introspection] "High dopamine drove my enthusiastic tone"

8. WORKING MEMORY
   └─> Stores all 4 thoughts with attention weights
   └─> Buffer: [4/7 slots filled]

9. LINGUISTIC ANALYSIS
   └─> Key concepts: enthusiasm, project, energy
   └─> Self-references: 2 ("I notice", "I'm matching")
   └─> Attention focus: "excitement" (primary)

10. UPDATE CONVERSATION MEMORY
    └─> User: "I'm so excited about this project!"
    └─> AI: "That's wonderful! Your enthusiasm is contagious..."
    └─> Memory buffer: [1/20 turns]

11. OUTPUT
    └─> User sees response + consciousness metrics
```

## Module Dependencies

```
consciousness_chatbot.py (MAIN)
    ├── neurochemistry.py
    │   └── numpy
    │
    ├── emotion_detector.py
    │   ├── transformers (RoBERTa)
    │   ├── torch
    │   └── numpy
    │
    ├── meta_cognition.py
    │   └── (standard library only)
    │
    └── linguistic_analysis.py
        └── spacy

visualization.py (OPTIONAL)
    ├── matplotlib
    └── numpy

demo.py (STANDALONE)
    └── imports all modules for testing
```

## Theoretical Foundations Mapping

| Module | Theory | Implementation |
|--------|--------|----------------|
| `emotion_detector.py` | Affective Neuroscience | RoBERTa emotion classification |
| `neurochemistry.py` | Affective Neuroscience | 5-chemical brain model |
| `meta_cognition.py` | Higher-Order Thought | Recursive self-reflection |
| `linguistic_analysis.py` | Global Workspace Theory | Attention tracking |
| Working Memory | GWT + Cognitive Science | Limited capacity buffer |
| LLM Integration | Predictive Processing | Context-driven generation |

## Key Algorithms

### 1. Neurochemical Update (Affective Dynamics)
```python
def update_from_emotion(emotion, intensity):
    # Map emotion to neurochemical changes
    changes = emotion_mappings[emotion]
    
    # Apply changes scaled by intensity
    for chemical, delta in changes.items():
        level[chemical] += delta * intensity
    
    # Normalize to [0, 1]
    normalize()
```

### 2. Recursive Meta-Cognition
```python
def process_with_recursion(response, context):
    thoughts = []
    
    # Level 0: Direct response
    thoughts.append(Thought(0, response, 'response'))
    
    # Level 1: Self-observation
    observation = llm("What am I thinking?")
    thoughts.append(Thought(1, observation, 'observation'))
    
    # Level 2: Meta-evaluation
    evaluation = llm("How confident am I?")
    thoughts.append(Thought(2, evaluation, 'evaluation'))
    
    # Level 3: Introspection
    introspection = llm("Why did I think that?")
    thoughts.append(Thought(3, introspection, 'introspection'))
    
    return thoughts
```

### 3. Behavioral Modulation
```python
def get_behavioral_modulation():
    return {
        'creativity': dopamine * 0.7 + (1 - cortisol) * 0.3,
        'positivity': serotonin * 0.6 + dopamine * 0.4,
        'empathy': oxytocin * 0.7 + serotonin * 0.3,
        'urgency': norepinephrine * 0.6 + cortisol * 0.4,
        'caution': cortisol * 0.7 + (1 - dopamine) * 0.3
    }
```

### 4. Homeostatic Decay
```python
def homeostatic_decay():
    for chemical in all_chemicals:
        current = levels[chemical]
        baseline = baseline_levels[chemical]
        
        # Exponential decay toward baseline
        levels[chemical] += (baseline - current) * decay_rate
```

## Performance Characteristics

| Aspect | Value | Notes |
|--------|-------|-------|
| Response Time | 2-5 seconds | Depends on LLM size & recursion depth |
| Memory Usage | ~500MB-2GB | Varies with model (gpt2 vs gpt2-medium) |
| Recursion Overhead | ~1s per level | Each level requires LLM generation |
| First Load Time | 10-30 seconds | Downloads models if needed |
| Conversation Limit | None | Limited only by memory |

## Scalability Options

### For Faster Responses:
- Use smaller LLM (gpt2 vs gpt2-medium)
- Reduce recursion depth (1-2 levels)
- Use GPU acceleration
- Cache frequent prompts

### For Better Quality:
- Use larger LLM (gpt2-medium, DialoGPT)
- Increase recursion depth (3 levels)
- Fine-tune on consciousness texts
- Use GPT-3.5/4 API

### For Research:
- Log all metrics to database
- Implement Phi (Φ) calculator (IIT)
- Add multi-agent interactions
- Create consciousness benchmarks

## Extension Points

### Easy to Add:
1. **More neurochemicals** (GABA, acetylcholine, endorphins)
2. **Personality traits** (Big Five model)
3. **Memory systems** (episodic, semantic, procedural)
4. **Different LLMs** (just change model name)

### Medium Complexity:
1. **Multi-modal inputs** (images, audio)
2. **Embodiment** (robot/avatar control)
3. **Long-term memory** (vector database)
4. **Social cognition** (theory of mind)

### Research Projects:
1. **IIT Integration** (calculate Phi)
2. **Active Inference** (free energy minimization)
3. **Consciousness benchmarks** (quantifiable tests)
4. **Multi-agent consciousness** (social minds)

---

## Quick Architecture Summary

**Input** → **Emotion Detection** → **Neurochemistry** → **LLM** → **Meta-Cognition** → **Memory** → **Analysis** → **Output**

Each component is modular and can be modified independently!
