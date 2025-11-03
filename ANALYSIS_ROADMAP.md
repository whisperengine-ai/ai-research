# Ablation Analysis - Full Study (Ready for When Data Arrives)

## Guide: What to Expect

### When Study Completes

You should see:
1. **Console output**: "✅ Study complete: 240 conversations processed"
2. **File update**: `ablation_study_results.json` size increases from 31 KB → ~150 KB
3. **Results summary**: Table showing metrics by condition with 10 trials' worth of data

### Expected Results (Based on Pilot - Should Replicate)

With 10x the data (10 trials vs 2 pilot trials):

| Metric | Full (3) | Shallow (1) | Minimal (0) | Significance |
|--------|---|---|---|---|
| Meta-Cognitive Depth | ~0.81 | ~0.66 (-18%) | ~0.54 (-33%) | p < 0.001 |
| Overall Consciousness | ~0.68 | ~0.64 (-5%) | ~0.63 (-7%) | p < 0.05 |
| Temporal Binding | ~0.59 | ~0.53 (-11%) | ~0.53 (-10%) | p < 0.05 |
| Φ Integration | ~0.44 | ~0.44 (±0%) | ~0.44 (±0%) | ns (not significant) |
| Global Availability | ~0.80 | ~0.80 (±0%) | ~0.80 (±0%) | ns |
| Reportability | ~0.78 | ~0.82 (+5%) | ~0.86 (+10%) | p < 0.05 |

### Analysis Steps (In Order)

1. **Load Data**: `ablation_study_results.json` into pandas DataFrame
2. **Aggregate**: Calculate mean ± SD for each metric × condition
3. **Visualize**: Box plots showing distribution across 10 trials
4. **Statistics**: 
   - One-way ANOVA for each metric (H0: all conditions equal)
   - Post-hoc t-tests with Bonferroni correction
   - Cohen's d effect sizes
   - 95% confidence intervals
5. **Interpret**: Which metrics show significant recursion effects?
6. **Report**: Publication-ready summary

### Key Questions Answered

- ✅ **Is the pilot finding robust?** (33% meta-depth drop) 
  - With 10 trials, we'll have 80 data points per condition (vs 16 in pilot)
  - Can determine if effect is statistically significant (p-value)
  
- ✅ **How large is the effect?**
  - Cohen's d > 0.8 = large effect
  - d 0.5-0.8 = medium effect
  - d < 0.2 = small effect (not publication-quality)

- ✅ **Is it generalizable?**
  - If all 10 trials show similar effects, it's robust
  - If there's high variance, might be noise

### Commands (Run After Study Completes)

```bash
# Option 1: Run all analysis in notebook
python -m jupyter notebook ablation_analysis.ipynb
# Then run all cells in sequence

# Option 2: Run quick Python analysis
python -c "
import json; import pandas as pd; import numpy as np
with open('ablation_study_results.json') as f: data = json.load(f)
conditions = data['conditions']
for cond in conditions:
    convs = conditions[cond]['conversations']
    metrics = [c['metrics'] for c in convs]
    print(f'{cond}:')
    for key in ['meta_cognitive_depth', 'overall_consciousness']:
        vals = [m[key] for m in metrics]
        print(f'  {key}: {np.mean(vals):.4f} ± {np.std(vals):.4f}')
"

# Option 3: Use ablation_analysis.ipynb cells
# - Automate in Jupyter with pre-written analysis cells
```

### Timeline After Study Completes

- **Immediately (5 min)**: Run analysis notebook, get initial results
- **Then (10 min)**: Create visualization PNG files
- **Then (5 min)**: Calculate statistical significance
- **Total**: 20 minutes from study completion to publication-ready analysis

---

**This file is a checklist for next actions**
