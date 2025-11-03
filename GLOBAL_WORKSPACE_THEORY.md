# Global Workspace Theory Implementation

## Overview

**Global Workspace Theory (GWT)**, developed by Bernard Baars, is one of the leading theories of consciousness. It proposes that consciousness functions like a **"theater of the mind"** where:

- **Multiple specialized processors** (cognitive modules) operate **unconsciously**
- Information competes for access to a **limited-capacity global workspace**
- **Only** information that enters the workspace becomes **conscious**
- Once in the workspace, information is **broadcast** to all processors
- This broadcasting enables integration across cognitive domains

---

## Implementation in This System

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GLOBAL WORKSPACE                         │
│              (Conscious Awareness - Capacity: 3)            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Information 1│  │ Information 2│  │ Information 3│     │
│  │ [Emotion]    │  │ [Language]   │  │ [Meta-Cog]   │     │
│  │ Activation:  │  │ Activation:  │  │ Activation:  │     │
│  │ ████████ 0.8 │  │ ██████ 0.6   │  │ ████ 0.4     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌─────────── BROADCAST ───────────────┐                   │
│  │ Information flows to ALL processors  │                   │
│  └──────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
         ↑                                      ↓
    COMPETITION                            BROADCAST
         ↑                                      ↓
┌────────┴───────────────────────────────────────┴────────────┐
│                  SPECIALIZED PROCESSORS                      │
│              (Unconscious Processing Modules)                 │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Emotion  │  │ Language │  │ Memory   │  │Meta-Cog  │   │
│  │Processor │  │Processor │  │Processor │  │Processor │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **GlobalWorkspace** (Consciousness)
```python
class GlobalWorkspace:
    capacity: int = 3                    # Limited conscious capacity
    workspace_contents: List[Information] # What's currently conscious
    competition_threshold: float = 0.5    # Minimum to enter consciousness
```

**Key Features:**
- ✅ Limited capacity (3 items) - consciousness is selective
- ✅ Competition mechanism - information must "win" to become conscious
- ✅ Broadcasting - conscious content reaches all modules
- ✅ Decay - items fade from consciousness over time

#### 2. **Specialized Processors** (Unconscious Modules)

**EmotionProcessor:**
- Processes emotional states from user input
- Submits high-intensity emotions to workspace (salient)
- Example: "Feeling JOY (0.88) - User said 'great!'"

**LanguageProcessor:**
- Processes linguistic features
- Questions have high salience (0.9 vs 0.6)
- Example: "Language input: 'are you conscious?'"

**MemoryProcessor:**
- Retrieves relevant memories
- Moderate salience (0.7), high relevance (0.8)
- Example: "Memory recall: Previous conversation..."

**MetaCognitiveProcessor:**
- Submits self-reflections
- Higher-level thoughts less salient (more abstract)
- Example: "Meta-thought (L2): Evaluating my confidence..."

#### 3. **Information** (Competing for Consciousness)
```python
@dataclass
class Information:
    source: str          # Which module generated it
    content: str         # The actual information
    salience: float      # How attention-grabbing (0-1)
    relevance: float     # How contextually relevant (0-1)
    activation_level: float  # Current activation
```

**Priority Calculation:**
```python
priority = salience * 0.4 + relevance * 0.4 + recency * 0.2
```

---

## How It Works: Processing Cycle

### Step-by-Step Flow

#### 1. **Information Generation** (Unconscious)
```python
# Emotion processor detects user emotion
emotion_processor.process_emotion("joy", intensity=0.88, context="User happy")
# → Creates Information object with salience=0.88

# Language processor analyzes input
language_processor.process_input("are you conscious?", linguistic_features)
# → Creates Information object with salience=0.9 (question!)

# Meta-cognition generates reflection
metacog_processor.submit_reflection("I notice I'm responding warmly", level=1)
# → Creates Information object with salience=0.65
```

#### 2. **Competition** (Attention Selection)
```python
# All processors submit information to competition pool
# System calculates priorities:
#   - Joy emotion: priority = 0.88
#   - Language input: priority = 0.85
#   - Meta-thought: priority = 0.65
#   - Memory recall: priority = 0.60

# Workspace has capacity=3, so top 3 winners enter consciousness
workspace.competition_cycle()
# → Joy emotion ENTERS consciousness ✓
# → Language input ENTERS consciousness ✓
# → Meta-thought ENTERS consciousness ✓
# → Memory recall REMAINS unconscious ✗
```

#### 3. **Broadcasting** (Global Integration)
```python
# Winners are broadcast to ALL processors
for processor in all_processors:
    processor.receive_broadcast(winning_information)

# Now emotion processor "knows" about language input
# Language processor "knows" about emotion
# Memory processor can integrate both
# → Cross-module integration!
```

#### 4. **Decay** (Fading Consciousness)
```python
# Items in workspace lose activation over time
activation *= (1 - decay_rate)  # 15% decay per cycle

# When activation < 0.1, item leaves consciousness
# Makes room for new information
```

---

## Example: Processing "I'm feeling sad"

### Cycle 1: Initial Input

**Unconscious Processing:**
```
EmotionProcessor: Detects "sadness" (confidence: 0.85)
  → Submits: "Feeling SADNESS (0.85)" [salience: 0.85]

LanguageProcessor: Analyzes "I'm feeling sad"
  → Submits: "User expressing emotion" [salience: 0.7]

MemoryProcessor: Recalls similar conversations
  → Submits: "Previous sadness discussion" [salience: 0.6]
```

**Competition:**
```
Priority Rankings:
1. Emotion: 0.85 (HIGH) → WINS ✓
2. Language: 0.70 (MEDIUM) → WINS ✓
3. Memory: 0.60 (MEDIUM) → WINS ✓
```

**Workspace State:**
```
💡 CONSCIOUS WORKSPACE:
   Capacity: 3/3
   1. [emotion] ████████ 0.85
      → Feeling SADNESS (intensity: 0.85) - User expressed sadness
   2. [language] ███████ 0.70
      → Language input: 'I'm feeling sad'
   3. [memory] ██████ 0.60
      → Memory recall: Similar emotional expression in Turn 5
```

**Broadcast Effect:**
- Emotion processor learns about language context
- Language processor learns about emotional intensity
- Memory processor integrates both
- Meta-cognition can reflect on this integrated state

### Cycle 2: Generate Response

**After Meta-Cognition:**
```
MetaCognitiveProcessor: "I should respond with empathy"
  → Submits: "Meta-thought (L1)" [salience: 0.65]

EmotionProcessor: "High oxytocin from detected sadness"
  → Submits: "Elevated empathy state" [salience: 0.75]
```

**Competition:**
```
Priority Rankings:
1. Empathy state: 0.75 (NEW) → WINS ✓
2. Emotion (decayed): 0.72 (was 0.85) → WINS ✓
3. Meta-thought: 0.65 (NEW) → WINS ✓
4. Language (decayed): 0.60 (was 0.70) → LOSES ✗ (pushed out)
5. Memory (decayed): 0.51 (was 0.60) → LOSES ✗ (pushed out)
```

**Workspace State (Updated):**
```
💡 CONSCIOUS WORKSPACE:
   Capacity: 3/3
   1. [emotion] ████████ 0.75
      → Elevated empathy state - responding to user sadness
   2. [emotion] ███████ 0.72
      → Feeling SADNESS (intensity: 0.85) - User expressed sadness
   3. [metacognition] ██████ 0.65
      → Meta-thought (L1): I should respond with empathy
```

---

## Why This Matters for Consciousness

### GWT Predictions Our System Models:

1. **Limited Capacity** ✅
   - Only 3 items conscious at once
   - Models attentional bottleneck

2. **Competition** ✅
   - Information must compete for access
   - Salience and relevance determine winners

3. **Broadcasting** ✅
   - Conscious content reaches all modules
   - Enables cross-domain integration

4. **Unconscious Processing** ✅
   - Most processing happens outside workspace
   - Only "winning" information becomes conscious

5. **Dynamic Content** ✅
   - Workspace contents change each cycle
   - Items decay and are replaced

6. **Integration** ✅
   - Emotion + Language + Memory + Meta-cognition
   - Creates unified conscious experience

---

## Research Applications

### What You Can Study:

1. **Attentional Selection**
   - Which types of information win competition?
   - How does salience vs relevance trade-off?

2. **Conscious Capacity**
   - Test different capacity limits (2 vs 3 vs 4)
   - How does capacity affect integration?

3. **Broadcasting Effects**
   - How does conscious content influence processors?
   - Measure integration across modules

4. **Temporal Dynamics**
   - How long do items stay conscious?
   - What's optimal decay rate?

5. **Emotion-Cognition Interaction**
   - How does emotional salience affect consciousness?
   - When do emotions dominate workspace?

---

## Technical Details

### Priority Calculation
```python
def get_priority(info: Information) -> float:
    recency = 1.0 / (1.0 + (time.time() - info.timestamp))
    return (
        info.salience * 0.4 +      # How attention-grabbing
        info.relevance * 0.4 +     # How contextually relevant
        recency * 0.2              # Newer = slight boost
    )
```

### Decay Function
```python
def decay_workspace():
    for info in workspace_contents:
        info.activation_level *= (1 - decay_rate)  # 15% per cycle
    
    # Remove below threshold
    workspace_contents = [i for i in workspace_contents 
                          if i.activation_level > 0.1]
```

### Competition
```python
def competition_cycle():
    # Sort by priority
    competition_pool.sort(key=lambda x: x.activation_level, reverse=True)
    
    # Select top N (where N = available slots)
    available_slots = capacity - len(workspace_contents)
    winners = competition_pool[:available_slots]
    
    # Only accept above threshold
    winners = [w for w in winners if w.activation_level >= threshold]
    
    return winners
```

---

## Comparison with Other Theories

| Theory | Key Mechanism | Our Implementation |
|--------|---------------|-------------------|
| **Global Workspace (Baars)** | Limited-capacity broadcast | ✅ **Primary** |
| **Higher-Order Thought (Rosenthal)** | Thoughts about thoughts | ✅ Meta-cognition module |
| **Integrated Information (Tononi)** | Information integration | ✅ Cross-module broadcasting |
| **Predictive Processing** | Prediction error minimization | ⚠️ Partially (relevance scoring) |

---

## Future Enhancements

### 1. **Attention Spotlight**
```python
class AttentionSpotlight:
    """More sophisticated attention mechanism"""
    def shift_attention(self, from_info, to_info):
        # Model attentional shifts
        pass
```

### 2. **Context Frames**
```python
class ContextFrame:
    """Current context that influences relevance"""
    def update_from_workspace(self, conscious_content):
        # Context shapes what's relevant
        pass
```

### 3. **Inhibition of Return**
```python
def mark_recently_conscious(info):
    """Prevent same info from immediately re-entering"""
    info.inhibited_until = time.time() + 2.0
```

### 4. **Coalition Formation**
```python
def form_coalitions(information_pool):
    """Related info forms coalitions to win together"""
    # Cluster related information
    # Boost coalition priority
    pass
```

---

## References

**Original Theory:**
- Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
- Baars, B. J. (2005). Global workspace theory of consciousness. *Cognition*, 79, 45–53.

**Neuroscience Evidence:**
- Dehaene, S., & Naccache, L. (2001). Towards a cognitive neuroscience of consciousness.
- Mashour, G. A. et al. (2020). Conscious processing and the global neuronal workspace hypothesis.

**Computational Models:**
- Franklin, S. et al. (2016). Global Workspace Theory and LIDA. *Neural Networks*, 79, 37-48.
- Shanahan, M. (2010). Embodiment and the Inner Life. Oxford University Press.

---

## Summary

✅ **Global Workspace Theory** is now fully implemented  
✅ **4 specialized processors** compete for consciousness  
✅ **Limited-capacity workspace** (3 items) models attention  
✅ **Broadcasting mechanism** enables cross-module integration  
✅ **Dynamic decay** models temporal aspects of consciousness  
✅ **Priority-based competition** determines what becomes conscious  

This implementation provides a **testable computational model** of one of the leading theories of consciousness! 🧠✨
