# 🌐 OpenRouter Setup Guide

## What is OpenRouter?

OpenRouter provides unified API access to multiple LLM providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3.5, Claude 3)
- Meta (Llama 3)
- Google (Gemini)
- Mistral AI
- And many more!

## Setup Steps

### 1. Get Your API Key

1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Go to [Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy your key (starts with `sk-or-...`)

### 2. Configure Your Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
   ```

3. Save the file

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- `python-dotenv` for environment variables
- `openai` library (OpenRouter uses OpenAI-compatible API)
- `requests` for HTTP calls

### 4. Run the Chatbot

```bash
python consciousness_chatbot.py
```

The system will automatically detect your API key and use OpenRouter!

## Available Models

### Recommended Models:

**Best Quality (Higher Cost):**
- `anthropic/claude-3.5-sonnet` - Excellent reasoning, consciousness simulation
- `openai/gpt-4-turbo-preview` - Strong general intelligence
- `anthropic/claude-3-opus` - Best for complex tasks

**Balanced (Medium Cost):**
- `anthropic/claude-3-sonnet` - Good quality, faster
- `openai/gpt-3.5-turbo` - Fast and capable
- `meta-llama/llama-3-70b-instruct` - Open source, strong

**Fast & Economical:**
- `anthropic/claude-3-haiku` - Very fast, cheap
- `meta-llama/llama-3-8b-instruct` - Lightweight
- `mistralai/mistral-small` - Efficient

### Change Models

Edit `.env`:
```bash
OPENROUTER_MODEL=openai/gpt-4-turbo-preview
```

Or in code:
```python
simulator = ConsciousnessSimulator(
    llm_model="anthropic/claude-3.5-sonnet",
    use_openrouter=True
)
```

## Pricing

OpenRouter charges per token. Check current prices:
[https://openrouter.ai/models](https://openrouter.ai/models)

**Typical costs for consciousness simulation:**
- Claude 3.5 Sonnet: ~$0.10-0.30 per conversation
- GPT-3.5 Turbo: ~$0.05-0.15 per conversation
- Llama 3 70B: ~$0.03-0.10 per conversation

**Tips to reduce costs:**
- Use smaller models for testing
- Reduce recursion depth to 1-2 levels
- Use Claude Haiku for frequent testing

## Benefits of Using OpenRouter

### vs Local Models (GPT-2):
✅ **Much better quality** - GPT-2 is outdated (2019)
✅ **Better consciousness simulation** - Modern models understand context better
✅ **Faster responses** - No local model loading
✅ **No GPU needed** - Runs on any computer

### vs Direct API:
✅ **One API for all models** - Easy to switch providers
✅ **Best pricing** - Often cheaper than direct APIs
✅ **Fallback options** - Switch if one provider is down
✅ **Credits system** - Add credits once, use multiple models

## Testing Your Setup

Run the test script:
```bash
python openrouter_llm.py
```

Should see:
```
Testing OpenRouter integration...

Model: anthropic/claude-3.5-sonnet
Site: consciousness-simulator

Test response: Hello! I'm happy to assist you...

✓ OpenRouter integration working!
```

## Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify `OPENROUTER_API_KEY=` has your actual key
- No spaces around the `=`

### "Invalid API key"
- Copy the full key including `sk-or-v1-`
- Check for typos
- Generate a new key from OpenRouter dashboard

### "Model not found"
- Check model name is exact (case-sensitive)
- See available models: [https://openrouter.ai/models](https://openrouter.ai/models)
- Try default: `anthropic/claude-3.5-sonnet`

### "Rate limit exceeded"
- Wait a few seconds between requests
- Upgrade your OpenRouter plan
- Use a cheaper/faster model

## Using Local Models Instead

If you don't want to use API:

1. Don't set `OPENROUTER_API_KEY` in `.env`
2. System will auto-fallback to local GPT-2
3. Or specify in code:

```python
simulator = ConsciousnessSimulator(
    llm_model="gpt2-medium",
    use_openrouter=False  # Use local model
)
```

## Best Practices

1. **Start with Claude 3 Haiku** - Fast and cheap for testing
2. **Upgrade to Claude 3.5 Sonnet** - When you want quality
3. **Set credit alerts** - In OpenRouter dashboard
4. **Monitor usage** - Check OpenRouter dashboard regularly
5. **Keep .env secure** - Never commit to git (already in .gitignore)

## Support

- OpenRouter Docs: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- Discord: [https://discord.gg/openrouter](https://discord.gg/openrouter)
- Model prices: [https://openrouter.ai/models](https://openrouter.ai/models)

---

**Ready to go!** 🚀

Your consciousness simulator will be much more intelligent with Claude or GPT-4!
