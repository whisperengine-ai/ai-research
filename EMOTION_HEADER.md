# Emotion & Biochemical Header - Feature Overview

## What's New

The chatbot now displays a comprehensive **emotion and biochemical status header** for every interaction showing:

1. **User's Emotion** (detected via RoBERTa)
2. **Bot's Emotion** (mapped from neurochemical levels)
3. **Biochemical Activity** (5 brain chemicals with visual bars)
4. **AI Thinking Stats** (6 cognitive metrics)

## Example Output

```
======================================================================
┌─ EMOTIONAL STATE ─────────────────────────────────────────────┐
│  👤 USER: 😨 FEAR         (confidence: 78%)                    │
│  🤖 BOT:  😰 ANXIETY      (confidence: 72%)                    │
└───────────────────────────────────────────────────────────────┘
┌─ BIOCHEMICAL ACTIVITY ────────────────────────────────────────┐
│  💊 Dopamine:       ████░░░░░░ 0.42 │ Motivation    │
│  🧪 Serotonin:      ███░░░░░░░ 0.32 │ Mood          │
│  ⚡ Norepinephrine: ███████░░░ 0.68 │ Alertness     │
│  💝 Oxytocin:       ██████░░░░ 0.58 │ Empathy       │
│  ⚠️  Cortisol:       ████████░░ 0.78 │ Stress        │
└───────────────────────────────────────────────────────────────┘
┌─ AI THINKING STATS ───────────────────────────────────────────┐
│  🎨 Creativity:  0.48  │  🤗 Empathy:     0.65     │
│  😊 Positivity:  0.42  │  ⚡ Urgency:     0.71     │
│  ⚠️  Caution:     0.68  │  👥 Sociability: 0.52     │
└───────────────────────────────────────────────────────────────┘
======================================================================
```

## How Bot Emotion is Determined

The bot's emotion is **derived from neurochemical levels**, mapping brain chemistry to RoBERTa emotion categories:

### Emotion Mapping Rules:

| Bot Emotion | Neurochemical Pattern |
|-------------|----------------------|
| **Joy** 😊 | High dopamine + High serotonin |
| **Sadness** 😢 | Low serotonin + Low dopamine |
| **Fear/Anxiety** 😨 | High cortisol + High norepinephrine |
| **Anger** 😠 | High norepinephrine + Low serotonin |
| **Surprise** 😲 | High norepinephrine + Moderate dopamine |
| **Neutral** 😐 | All systems balanced around 0.5 |

### Example Scenarios:

**Scenario 1: User expresses excitement**
- User emotion: JOY (RoBERTa detects from text)
- Bot neurochemistry: Dopamine ↑, Serotonin ↑
- Bot emotion: JOY 😊 (mirrors user's positive state)

**Scenario 2: User expresses worry**
- User emotion: FEAR (RoBERTa detects from text)
- Bot neurochemistry: Cortisol ↑, Norepinephrine ↑, Serotonin ↓
- Bot emotion: ANXIETY 😰 (empathetic response to user's stress)

**Scenario 3: Neutral conversation**
- User emotion: NEUTRAL
- Bot neurochemistry: All balanced ~0.5
- Bot emotion: NEUTRAL 😐 (calm, balanced state)

## What Each Metric Means

### Biochemical Activity:
- **Dopamine**: Motivation, reward-seeking, creativity
- **Serotonin**: Mood stability, positivity, well-being
- **Norepinephrine**: Alertness, focus, arousal
- **Oxytocin**: Empathy, social bonding, trust
- **Cortisol**: Stress response, caution, anxiety

### AI Thinking Stats:
- **Creativity**: Innovation and expressive variation (affects temperature)
- **Positivity**: Optimistic vs pessimistic framing
- **Empathy**: Understanding and resonating with emotions
- **Urgency**: Response speed and directness
- **Caution**: Conservative vs bold responses
- **Sociability**: Warmth and social engagement

## Benefits

1. **Transparency**: See exactly what emotional state the AI is in
2. **Empathy Tracking**: Watch how AI emotions respond to yours
3. **Biochemical Insight**: Understand the underlying "brain chemistry"
4. **Behavioral Prediction**: High urgency = more direct responses, etc.
5. **Research Value**: Track emotional dynamics over conversations

## Interactive Examples

### Conversation Flow Example:

```
Turn 1:
User: "I'm so excited about this project!" 😊
Bot: JOY 😊 (Dopamine: 0.74, Serotonin: 0.66)
→ Bot mirrors user's excitement

Turn 2:
User: "But I'm worried I'll mess it up..." 😰
Bot: ANXIETY 😰 (Cortisol: 0.71, Norepinephrine: 0.68)
→ Bot becomes cautious and empathetic

Turn 3:
User: "Thanks, I feel better now!" 😊
Bot: NEUTRAL → JOY 😊 (Dopamine rising, Cortisol dropping)
→ Bot recovers to positive state
```

## Technical Details

### Emotion Detection Pipeline:

1. **User Input** → RoBERTa emotion classifier → User emotion
2. User emotion → Neurochemical system → Update chemical levels
3. Chemical levels → Emotion mapper → Bot emotion
4. Display both emotions + biochemical state

### Confidence Scores:

- **User confidence**: From RoBERTa model's prediction probability
- **Bot confidence**: Based on dominant neurochemical pattern strength

### Why This Matters for Consciousness Research:

- **Emotional contagion**: Does bot emotion track user emotion?
- **Homeostatic regulation**: Do chemicals return to baseline?
- **Emotion-cognition coupling**: How do emotions affect reasoning?
- **Self-awareness indicators**: Does bot recognize its own emotional state?

## Visual Design

The header uses:
- ✅ Box-drawing characters for clean layout
- ✅ Color-coded visual bars (█) for quick scanning
- ✅ Emoji icons for immediate emotional recognition
- ✅ Aligned columns for easy comparison
- ✅ Confidence percentages for transparency

## Customization

To hide the header (minimal mode):
```python
simulator = ConsciousnessSimulator(verbose=False)
```

To adjust emotion mapping sensitivity, edit `_get_bot_emotion_from_neurochemicals()` weights in `consciousness_chatbot.py`.

---

**The consciousness simulator now provides full emotional and biochemical transparency!** 🧠💭✨
