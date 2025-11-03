# AI Research Project - Quick Context for Next Session

## Current State (Nov 2, 2025)
- ✅ **RESEARCH-READY**: 15 production modules, 22+ tests passing, fully functional
- ✅ **Clean repo**: 17 Python files, 2 notebooks, 6 docs only (no bloat)
- ✅ **Portable**: No hard-coded paths, works anywhere

## 3 Essential Commands

```bash
# 1. Validate pipeline works (5 min)
jupyter notebook quick_validation.ipynb

# 2. Run ablation study - component testing (30-60 min)
python run_ablation_study.py --trials 10

# 3. Collect 100+ conversations (30-60 min)
python collect_dataset.py --conversations 100
```

## Key Files

**Production Code:**
- `consciousness_chatbot.py` - Main simulator (GWT + emotions + recursion + neurochemistry)
- `metrics.py` - 6 consciousness metrics (Φ, overall, global_availability, meta_depth, temporal_binding, reportability)
- `run_conversation_test.py` - ConversationTestRunner with 8 built-in scenarios
- `experiments.py` - ExperimentRunner for ablation studies

**Research Tools:**
- `quick_validation.ipynb` - Fast pipeline check (generates validation_results.json + 8 dashboards)
- `ablation_analysis.ipynb` - Analyze ablation results (load + compare + visualize)
- `run_ablation_study.py` - Ablation framework (3 recursion depths, configurable trials)
- `collect_dataset.py` - Scalable dataset collector (25 diverse prompts, auto metrics)

**Tests:**
- `test_consciousness.py` - 22+ pytest tests (all passing)

## Next Steps

1. **Ablation Study**: Run `python run_ablation_study.py --trials 10` (~45 min) → Get ablation_study_results.json
2. **Dataset Collection**: Run `python collect_dataset.py --conversations 100` (~45 min) → Get dataset_results.json
3. **Analysis**: Open `ablation_analysis.ipynb` and analyze results
4. **Publication**: Use generated visualizations + data for research paper

## Important Notes

- All tools use **dynamic paths** (no hard-coded usernames)
- All tests pass - code is production quality
- OpenRouter API required (check OPENROUTER_SETUP.md if needed)
- Notebooks auto-generate dashboards (validation_output/, ablation_output/, dataset_output/)

## Don't Read

- PROJECT_STATUS.md (reference only if needed)
- PROJECT_SUMMARY.md (reference only if needed)
- RESEARCH_TOOLS.md (detailed reference only)
- QUICKSTART.md (covered above)
- README.md (high-level overview)
- OPENROUTER_SETUP.md (only if API issues)

**Focus on the 3 commands above. That's it.**
