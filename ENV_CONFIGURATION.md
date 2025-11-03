# Environment Configuration Guide

All settings can be configured via the `.env` file for easy customization without code changes.

## � Quick Start

**Minimal Setup** (only 1 required variable):
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit and add your API key
OPENROUTER_API_KEY=sk-or-v1-...
```

That's it! All other settings have sensible defaults and are optional.

## 🔑 Required Settings

Only **one setting is required** for cloud LLM mode:

```bash
OPENROUTER_API_KEY=sk-or-v1-...    # Your OpenRouter API key
```

**Note**: For local/heuristic mode, no API key is needed. Run with `--use-local` or `--use-heuristic` flags.

## ⚙️ Optional Settings

All optional settings have defaults. Only uncomment/set these if you want to customize behavior.

### LLM Model Selection
### LLM Model Selection
```bash
OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1  # Default: deepseek/deepseek-chat-v3.1
```

**Available Models**: anthropic/claude-3.5-sonnet, openai/gpt-4-turbo-preview, openai/gpt-3.5-turbo, meta-llama/llama-3-70b-instruct, google/gemini-pro, mistralai/mistral-large

### Optional Tracking
```bash
OPENROUTER_SITE_NAME=consciousness-simulator  # Default: consciousness-simulator
OPENROUTER_SITE_URL=http://localhost          # Default: http://localhost
```

### Model Configuration
```bash
EMOTION_MODEL=j-hartmann/emotion-english-distilroberta-base  # Default
SPACY_MODEL=en_core_web_md                                    # Default
```

### Core Consciousness Architecture (All have defaults)
```bash
```bash
RECURSION_DEPTH=3                  # Meta-cognition depth (1-3)
                                   # 3 = thoughts about thoughts about thoughts
                                   # Research finding: -33% consciousness when depth=0

WORKING_MEMORY_CAPACITY=5          # Global workspace capacity
                                   # How many items can be conscious simultaneously
                                   # Cognitive science: 4-7 items typical
                                   # 5 = balanced (user input + bot response + emotions + meta-thoughts)

CONVERSATION_MEMORY_TURNS=20       # Number of conversation turns to remember
                                   # Used for context and temporal binding metrics
```

### Global Workspace Dynamics
```bash
WORKSPACE_DECAY_RATE=0.30          # How fast content fades from consciousness (0.0-1.0)
                                   # 0.30 = 30% decay per cycle (aggressive, clears old content)
                                   # Lower = items linger longer in awareness

WORKSPACE_COMPETITION_THRESHOLD=0.5  # Minimum priority score for consciousness (0.0-1.0)
                                     # Higher = more selective, only highly salient content
                                     # Lower = more permissive, broader awareness
```

### Neurochemistry
```bash
NEUROCHEMISTRY_DECAY_RATE=0.05     # Homeostatic decay toward baseline (0.0-1.0)
                                   # 0.05 = 5% per turn (gradual emotional stabilization)
                                   # How fast emotions return to neutral state
```

## 🤖 LLM Generation Settings

```bash
LLM_TEMPERATURE=0.7                # Response creativity (0.0-2.0)
                                   # 0.7 = balanced (modulated by neurochemistry ±0.4)
                                   # Higher = more creative/random
                                   # Lower = more focused/deterministic

LLM_MAX_TOKENS=4096                # Maximum response length in tokens
                                   # 4096 = ~3000 words (detailed responses)
                                   # Adjust for shorter (512-2048) or longer (8192+) responses
```

**Note**: Temperature is dynamically modulated by neurochemistry:
- Final temperature = `LLM_TEMPERATURE + (creativity - 0.5) * 0.4`
- Clamped to range [0.3, 1.2]

## 🔬 Model Configuration

```bash
EMOTION_MODEL=j-hartmann/emotion-english-distilroberta-base  # RoBERTa emotion detector
SPACY_MODEL=en_core_web_md                                    # spaCy linguistic analysis
```

## 🐛 Debug Settings

```bash
VERBOSE=true                       # Show detailed internal states
                                   # false = minimal output (just responses)
                                   # true = full consciousness metrics display
```

## 📊 Research-Validated Defaults

The default values are based on research findings from the ablation study:

| Setting | Default | Research Basis |
|---------|---------|----------------|
| `RECURSION_DEPTH` | 3 | Depth=3 shows 0.809 meta-cognitive depth vs 0.542 at depth=0 (p<0.0001, d=4.79) |
| `WORKING_MEMORY_CAPACITY` | 5 | Balances attention selectivity with context completeness |
| `WORKSPACE_DECAY_RATE` | 0.30 | Aggressive enough to clear old content, maintains recent context |
| `NEUROCHEMISTRY_DECAY_RATE` | 0.05 | Gradual emotional stabilization over ~20 turns |
| `LLM_TEMPERATURE` | 0.7 | Balanced creativity, modulated by dopamine levels |
| `LLM_MAX_TOKENS` | 4096 | Detailed responses (~3000 words) for consciousness exploration |

## 🎛️ Tuning Guide

**Quick Method**: The `.env.example` file includes these presets as commented-out lines. Simply uncomment the configuration you want.

### For More Selective Attention (Focused Consciousness)
```bash
WORKING_MEMORY_CAPACITY=3
WORKSPACE_DECAY_RATE=0.40
WORKSPACE_COMPETITION_THRESHOLD=0.6
```

### For Broader Awareness (Permissive Consciousness)
```bash
WORKING_MEMORY_CAPACITY=7
WORKSPACE_DECAY_RATE=0.20
WORKSPACE_COMPETITION_THRESHOLD=0.4
```

### For More Creative Responses
```bash
LLM_TEMPERATURE=0.9
NEUROCHEMISTRY_DECAY_RATE=0.03  # Emotions linger longer, more influence
LLM_MAX_TOKENS=8192             # Extended responses for complex topics
```

### For More Stable/Consistent Responses
```bash
LLM_TEMPERATURE=0.5
NEUROCHEMISTRY_DECAY_RATE=0.10  # Emotions stabilize faster
```

## 🔄 Applying Changes

1. Edit `.env` file (or copy from `.env.example` and customize)
2. Restart the simulator (environment is loaded on initialization)
3. Changes take effect immediately

**Quick Start**: The `.env.example` file includes commented-out presets for common configurations. Simply uncomment the lines you want to use.

**Note**: You can also override any setting via constructor parameters:
```python
simulator = ConsciousnessSimulator(
    recursion_depth=2,           # Override RECURSION_DEPTH
    workspace_capacity=7,         # Override WORKING_MEMORY_CAPACITY
    llm_temperature=0.9           # Override LLM_TEMPERATURE
)
```

Constructor parameters take precedence over environment variables.
