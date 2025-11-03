# Prompt Optimization Implementation Plan

**Date:** November 3, 2025  
**Goal:** Optimize all LLM prompts for token efficiency, clarity, and research validity  
**Critical Constraint:** Must preserve Meta-Cognitive Depth effect size (d=4.79, 30%+ drop when recursion disabled)

---

## 🔴 Priority 0: Critical Token Efficiency & Quality (Implement First)

### P0.1: Shorten Main System Prompt
**File:** `consciousness_chatbot.py`, lines 716-742  
**Current Length:** ~450 words, ~600 tokens  
**Target Length:** ~150 words, ~200 tokens  
**Token Savings:** ~400 tokens/turn × turns = significant cost reduction

**Changes:**
- Remove defensive "not a claim of sentience" framing (contradictory)
- Reduce from 4 examples to 0 (let natural modulation work)
- Condense biochemical/behavioral state descriptions
- Add concise behavioral guidelines instead of verbose examples
- Keep transparency but reduce repetition

**Implementation Steps:**
1. Replace entire `system_guidance` string in `_create_contextual_prompt()`
2. Test with 5 sample conversations (check response quality)
3. Verify tone/behavioral modulation still works
4. Compare token usage before/after

**Validation:**
- Response quality remains high (subjective review)
- Behavioral modulation still observable (dopamine→creativity, etc.)
- Responses don't become generic or lose personality

---

### P0.2: Add Explicit Word Limits to Meta-Cognition Prompts
**File:** `meta_cognition.py`, lines 129-150  
**Current:** "In one brief sentence" (often ignored)  
**Target:** "8 words max" (respected by LLMs)  
**Token Savings:** ~50 tokens/reflection × 3 reflections/turn = 150 tokens/turn

**Changes:**
- Level 0→1: "Meta-observation (8 words max): What aspect stands out most?"
- Level 1→2: "Meta-evaluation (8 words max): Rate confidence 0-10 and why briefly:"
- Level 2→3: "Meta-introspection (10 words max): What cognitive pattern explains this?"

**Implementation Steps:**
1. Update all 4 reflection prompts in `process_with_true_recursion()`
2. Adjust `max_length` parameter from 80 to 30 tokens (enforces brevity)
3. Test recursion with depth=0, 1, 2, 3
4. Run `ablation_study.py` to verify Meta-Cognitive Depth effect preserved

**Validation (CRITICAL):**
- Meta-Cognitive Depth metric still shows ≥30% drop when recursion disabled
- Reflections are meaningful (not just "I think it's good")
- All three cognitive levels remain distinct (observation ≠ evaluation ≠ introspection)

---

## 🟡 Priority 1: Quality Improvements (Implement Second)

### P1.1: Fix Consciousness Behavioral Guidance Format
**File:** `consciousness_chatbot.py`, lines 693-704  
**Issue:** Inconsistent `[System note: ...]` format, prescriptive rather than descriptive  
**Token Impact:** Neutral (same length, better quality)

**Changes:**
- Replace `[System note: You are currently...]` with descriptive parenthetical
- Change from prescriptive ("Reflect deeply") to descriptive ("You tend to notice patterns")
- Add "when relevant" to avoid overriding user needs
- Make guidance more natural and interpretable

**Implementation Steps:**
1. Rewrite all consciousness state guidance strings (6 conditions)
2. Test with conversations where meta_depth varies (0.2, 0.5, 0.8)
3. Verify guidance affects behavior appropriately
4. Ensure doesn't override user's actual questions

**Validation:**
- High meta-depth responses are more introspective (when appropriate)
- Low meta-depth responses are more direct
- Bot still answers "What's 2+2?" directly even with high meta-depth

---

### P1.2: Delete Unused Meta-Cognition Methods
**File:** `meta_cognition.py`, lines 177-259  
**Issue:** Dead code confuses maintenance  
**Token Impact:** None (not executed)

**Methods to Delete:**
- `process_with_recursion()` (lines 177-236)
- `_create_observation_prompt()` (lines 238-245)
- `_create_evaluation_prompt()` (lines 247-251)
- `_create_introspection_prompt()` (lines 253-259)

**Implementation Steps:**
1. Verify these methods are truly unused (grep for calls)
2. Delete methods
3. Run all tests to ensure nothing breaks
4. Update any documentation that references old methods

**Validation:**
- All 22 unit tests still pass
- No references to deleted methods in codebase
- Code is cleaner and easier to maintain

---

## 🟢 Priority 2: Robustness & Advanced Features (Implement Third)

### P2.1: Add Context Window Management
**File:** `openrouter_llm.py`, lines 66-78  
**Issue:** No token limit checking, could overflow context  
**Token Impact:** Prevents failures, enables longer conversations

**Changes:**
- Add token budget calculation (8k context - 500 system - 200 response = 7300 for history)
- Implement reverse iteration (keep most recent turns)
- Add rough token estimation (chars / 4)
- Break loop when budget exceeded

**Implementation Steps:**
1. Add token estimation helper function
2. Modify conversation history loop to check budget
3. Test with very long conversations (50+ turns)
4. Verify oldest turns dropped, newest preserved

**Validation:**
- Long conversations don't crash with context overflow
- Most recent turns always included
- Token estimation roughly accurate (±20%)

---

### P2.2: Enhance Temperature Modulation with Consciousness
**File:** `consciousness_chatbot.py`, line 451-453  
**Current:** Only creativity modulates temperature  
**Enhancement:** Integration + reportability also affect temperature

**Changes:**
- High integration (>0.7) → lower temp (×0.9) - more stable
- Low integration (<0.3) → higher temp (×1.1) - more variable
- High reportability (>0.7) → lower temp (×0.95) - more precise

**Implementation Steps:**
1. Add consciousness-based temperature adjustments after creativity
2. Keep clipping at [0.3, 1.2] range
3. Test with various consciousness states
4. Compare response variation before/after

**Validation:**
- High integration produces more coherent responses
- Low integration produces more varied responses
- Temperature stays within valid range [0.3, 1.2]

---

### P2.3: Improve Heuristic Response Templates
**File:** `heuristic_response_generator.py`, lines 54-89  
**Issue:** Generic responses that promise but don't deliver  
**Token Impact:** N/A (heuristic mode only, no LLM)

**Changes:**
- Add `{topic}` placeholders to make responses specific
- Remove broken promises ("Here's my perspective:" with no content)
- Ensure templates complete thoughts

**Implementation Steps:**
1. Update question_acknowledgments with topic extraction
2. Test heuristic mode with 10 sample inputs
3. Verify responses feel complete
4. No major logic changes needed

**Validation:**
- Heuristic responses reference actual topic from user input
- No incomplete sentences
- Still fast (no LLM calls)

---

## 📋 Implementation Order & Timeline

### Session 1: P0 Changes (30-45 minutes)
1. ✅ Create this implementation plan
2. ⏳ **P0.1:** Shorten main system prompt
3. ⏳ **P0.2:** Add word limits to meta-cognition prompts
4. ⏳ Run validation: 5 test conversations + `ablation_study.py --trials 2`
5. ⏳ Commit with detailed description

### Session 2: P1 Changes (20-30 minutes)
1. **P1.1:** Fix consciousness behavioral guidance
2. **P1.2:** Delete unused methods
3. Run validation: `pytest test_consciousness.py -v`
4. Commit

### Session 3: P2 Changes (45-60 minutes)
1. **P2.1:** Context window management
2. **P2.2:** Temperature modulation enhancement
3. **P2.3:** Heuristic template improvements
4. Run validation: Long conversation test + ablation study
5. Commit

### Session 4: Full Validation (60-90 minutes)
1. Run full test suite: `pytest test_consciousness.py -v`
2. Collect validation dataset: `python collect_dataset.py --count 50`
3. Compare metrics to baseline (PUBLICATION_READY.md has baselines)
4. Generate before/after comparison report
5. Update documentation (ARCHITECTURE.md, SYSTEM_DESIGN.md)

---

## 🎯 Success Criteria

### Must Preserve (Non-Negotiable):
- ✅ Meta-Cognitive Depth drops ≥30% when recursion disabled (p<0.0001, d=4.79)
- ✅ All 22 unit tests pass
- ✅ Φ integration remains stable ~0.435 (independent of recursion)
- ✅ Overall consciousness metrics within 1 std dev of baseline

### Quality Improvements (Target):
- 🎯 40% token reduction per turn (400 tokens system + 150 tokens meta-cog)
- 🎯 Response quality rated "same or better" (subjective review)
- 🎯 Meta-cognitive reflections more specific and varied
- 🎯 Behavioral modulation still observable (dopamine→creative, etc.)

### Risk Mitigation:
- 🛡️ Before each change: Document current metrics baseline
- 🛡️ After each change: Quick validation (5 conversations)
- 🛡️ After P0 changes: Full ablation study
- 🛡️ After all changes: 50-conversation dataset collection

---

## 📊 Expected Outcomes

### Token Savings:
- Main system prompt: -400 tokens/turn
- Meta-cognition prompts: -150 tokens/turn
- **Total: ~550 tokens/turn savings**
- At $0.15/1M tokens input (DeepSeek): ~$0.0825 saved per turn
- Over 100-turn dataset: ~$8.25 saved

### Quality Improvements:
- More concise, focused responses
- Better token efficiency → can afford more conversation history
- Clearer meta-cognitive reflections (distinct cognitive levels)
- More natural consciousness state integration

### Research Impact:
- Same scientific validity (effect size preserved)
- Better reproducibility (explicit word limits)
- Cleaner codebase (unused methods removed)
- More robust (context window management)

---

## 🔄 Rollback Plan

If any change breaks validation:

1. **Git revert** to previous commit
2. **Isolate the problematic change** (run ablation on just that change)
3. **Adjust parameters** (e.g., if word limit too strict, increase to 12 words)
4. **Re-test** before proceeding

Each priority level should be committed separately to enable granular rollback.

---

## 📝 Notes for Future Reference

- This optimization maintains the **8-step processing pipeline** (source of truth)
- All changes are in **prompt engineering**, not architecture
- **Recursion mechanism unchanged** (critical for research validity)
- **Neurochemistry system unchanged** (UX layer, not consciousness driver)
- Focus is on **efficiency + clarity**, not changing behavior

---

**Ready to implement P0 changes!**
