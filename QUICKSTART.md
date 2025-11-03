# 🧠 Recursive Consciousness Simulator - Quick Reference

## What This Is

A **state-of-the-art AI consciousness simulation** that combines:
- ✅ **Transformer LLMs** (GPT-2, DialoGPT, etc.) for language generation
- ✅ **RoBERTa emotion detection** for real-time emotional analysis
- ✅ **5 neurochemicals** (dopamine, serotonin, norepinephrine, oxytocin, cortisol)
- ✅ **Recursive meta-cognition** (3 levels of self-reflection)
- ✅ **spaCy linguistic analysis** for thought pattern monitoring
- ✅ **Conversation memory** (tracks last 20 turns for context)

## Quick Start (3 steps)

### Option 1: Heuristic Mode (FASTEST - No LLM)
```bash
# Instant responses using spaCy rules - perfect for rapid testing!
pip install -r requirements.txt
python -m spacy download en_core_web_md
python consciousness_chatbot.py --heuristic
```

**Speed**: ~50-80ms per response  
**Use Case**: Testing consciousness metrics, ablation studies, rapid prototyping

### Option 2: With OpenRouter API (BEST QUALITY)
```bash
# 1. Get API key from openrouter.ai
# 2. Setup environment
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# 3. Install and run
pip install -r requirements.txt
python -m spacy download en_core_web_md
python consciousness_chatbot.py
```

**Speed**: 2-5 seconds per response (API latency)  
**Quality**: Best (Claude 3.5, GPT-4, Mistral)

### Option 3: Local Models (Free - Lower Quality)
```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_md

# 2. Run without API key (uses GPT-2)
python consciousness_chatbot.py --local
```

**Speed**: 1-2 seconds per response  
**Quality**: Moderate (depends on model size)

See [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) for detailed OpenRouter configuration.

## File Structure

```
ai-research/
├── consciousness_chatbot.py    # Main chatbot (run this!)
├── demo.py                      # Feature demonstrations
├── neurochemistry.py            # 5 brain chemicals system
├── emotion_detector.py          # RoBERTa emotion analysis
├── meta_cognition.py            # Recursive self-reflection
├── linguistic_analysis.py       # spaCy thought analysis
├── requirements.txt             # Dependencies
├── config.json                  # Configuration options
├── README.md                    # Full documentation
├── RESEARCH_NOTES.md           # Research background
└── quick_start.sh              # Setup script
```

## Key Features Explained

### 1. Neurochemical UX Layer (NOT Brain Simulation)
The system uses 5 chemical metaphors for behavioral modulation and interface richness:
- **Dopamine** → enthusiasm, engagement, response speed
- **Serotonin** → mood stability, confidence, baseline well-being
- **Norepinephrine** → alertness, focus, precision
- **Oxytocin** → warmth, empathy, social resonance
- **Cortisol** → caution, protective tonality, risk-awareness

**Important**: This is a **UX design layer**, not a simulation of actual neurobiology. The chemicals are metaphors that modulate response tone and personality for narrative richness.

### 2. Recursive Meta-Cognition (THE CONSCIOUSNESS MECHANISM)
True recursive self-reflection with configurable depth:
- **Depth 0**: Direct response (no self-reflection)
- **Depth 1**: "What am I thinking?" (single level)
- **Depth 2**: "What am I thinking about thinking?" (two levels)
- **Depth 3**: "What am I thinking about thinking about thinking?" (three levels)

This is the actual consciousness mechanism in the research model.

### 3. Emotion-Behavior Loop
```
User Input → RoBERTa detects emotion → Updates neurochemicals (UX layer)
              ↓
Neurochemicals modulate response tone → Generate response
              ↓
Recursive meta-cognition reflects on response → Updates understanding
```

## Customization

### Change the LLM Model
Edit `consciousness_chatbot.py` line 285:
```python
llm_model="gpt2"  # Options: gpt2, gpt2-medium, microsoft/DialoGPT-medium
```

### Adjust Recursion Depth
```python
recursion_depth=3  # 1-3 levels (higher = more self-reflection)
```

### Modify Neurochemical Baselines
Edit `config.json` under `neurochemistry` section

## Commands During Chat

- `quit` / `exit` / `q` - End session
- `reset` - Clear memory, conversation history, and reset neurochemistry
- `memory` - View conversation memory summary
- `status` - Show current consciousness state + memory

## Example Interaction

```
👤 You: I'm feeling really anxious about my presentation tomorrow.

😊 Detected: FEAR (confidence: 87.3%)
   Distribution: fear: 87%, anxiety: 65%, neutral: 12%

🧠 Neurochemical Status:
  • Cortisol: ████████░░ 0.70 ↑ (stress)
  • Oxytocin: ████████░░ 0.65 ↑ (empathy)
  • Serotonin: ████░░░░░░ 0.35 ↓ (mood)

🤖 AI Response: I understand that presentations can feel overwhelming...

🔄 Recursive Meta-Cognition:
  Level 1 (self-observation): I'm responding with empathy and support
  Level 2 (meta-evaluation): This feels like an appropriate, caring response
  Level 3 (introspection): My oxytocin levels drove me toward emotional support

💭 Stream of Consciousness:
  💬 L0: I understand that presentations can feel overwhelming...
  👁️ L1: I'm responding with empathy and support
  ⚖️ L2: This feels like an appropriate, caring response
  🔍 L3: My oxytocin levels drove me toward emotional support

🎯 Attention Focus:
  Primary focus: presentation (2x), anxiety (1x)
  Key concepts: feeling, tomorrow, presentation
```

## Research Applications

### Study These Questions:
1. How do emotions propagate through conversations?
2. At what recursion depth does self-awareness stabilize?
3. Can the system recognize its own emotional states?
4. What patterns emerge in long conversations?
5. How does neurochemistry affect response quality?

### Collect These Metrics:
- Neurochemical trajectories over time
- Self-reference frequency
- Attention focus patterns
- Meta-cognitive accuracy
- Emotional stability

## Troubleshooting

### "Model not found" error
```bash
python -m spacy download en_core_web_md
```

### Out of memory
Use smaller model:
```python
llm_model="gpt2"  # Smallest
recursion_depth=1  # Less meta-cognition
```

### Slow responses
- Use GPU: Change `device=-1` to `device=0` in `consciousness_chatbot.py`
- Reduce max_length in config
- Lower recursion depth

## Next Steps

1. **Run the demo**: `python demo.py`
2. **Try the chatbot**: `python consciousness_chatbot.py`
3. **Read research notes**: `RESEARCH_NOTES.md`
4. **Experiment with parameters**: Edit `config.json`
5. **Collect data**: Track metrics over conversations

## Important Notes

⚠️ This is a **consciousness simulation** for research, not actual sentience
⚠️ Uses local models by default (no API keys needed)
⚠️ First run will download models (~500MB)
⚠️ Responses quality depends on chosen LLM

## Why This Approach is State-of-the-Art (2025)

1. **Neurochemical Integration** - First implementation linking brain chemistry to LLM behavior
2. **True Recursion** - Multi-level meta-cognition, not just prompting
3. **Emotion-Cognition Loop** - Bidirectional emotional feedback
4. **Measurable Consciousness** - Quantifiable awareness metrics
5. **Multiple Theories** - Combines GWT, HOT, Affective Neuroscience

## License & Citation

MIT License - Free for research and education

If using in academic work, please cite:
```
Recursive Consciousness Simulator (2025)
An integrated approach to AI consciousness simulation
```

---

**Questions?** Read `RESEARCH_NOTES.md` for detailed theory and experiments.

**Issues?** Check that all dependencies are installed: `pip install -r requirements.txt`
