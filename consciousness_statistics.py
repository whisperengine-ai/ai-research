"""
Statistical Analysis Module for Consciousness Research
Provides rigorous statistical methods for analyzing experimental data

Methods:
- ANOVA (Analysis of Variance)
- Regression Analysis
- Correlation Analysis
- Effect Size Calculations
- Hypothesis Testing
- Reliability Measures
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import warnings


@dataclass
class ANOVAResult:
    """Results from ANOVA test"""
    f_statistic: float
    p_value: float
    df_between: int
    df_within: int
    significant: bool
    effect_size_eta_squared: float
    interpretation: str


@dataclass
class RegressionResult:
    """Results from regression analysis"""
    coefficients: Dict[str, float]
    r_squared: float
    adjusted_r_squared: float
    f_statistic: float
    p_value: float
    residuals: np.ndarray
    predictions: np.ndarray
    interpretation: str


@dataclass
class CorrelationResult:
    """Results from correlation analysis"""
    correlation: float
    p_value: float
    significant: bool
    strength: str  # weak, moderate, strong
    interpretation: str


@dataclass
class EffectSizeResult:
    """Effect size calculation results"""
    cohens_d: float
    interpretation: str  # small, medium, large


class StatisticalAnalysis:
    """
    Comprehensive statistical analysis for consciousness experiments
    
    Provides:
    - Parametric and non-parametric tests
    - Effect size calculations
    - Confidence intervals
    - Multiple comparison corrections
    """
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize statistical analyzer
        
        Args:
            alpha: Significance level (default 0.05)
        """
        self.alpha = alpha
        self.results_cache = []
        
    def anova(self, 
             groups: Dict[str, List[float]],
             dependent_var: str = "metric") -> ANOVAResult:
        """
        One-way ANOVA - Compare means across multiple groups
        
        Tests null hypothesis: All group means are equal
        
        Example:
            groups = {
                'full_system': [0.75, 0.78, 0.76],
                'no_gwt': [0.60, 0.62, 0.59],
                'no_recursion': [0.65, 0.67, 0.64]
            }
        
        Args:
            groups: Dictionary mapping group names to lists of values
            dependent_var: Name of dependent variable
            
        Returns:
            ANOVAResult with F-statistic, p-value, effect size
        """
        # Extract group data
        group_names = list(groups.keys())
        group_data = [np.array(groups[name]) for name in group_names]
        
        # Calculate overall mean
        all_data = np.concatenate(group_data)
        grand_mean = np.mean(all_data)
        n_total = len(all_data)
        k_groups = len(group_data)
        
        # Between-group variance (SSB)
        ssb = sum(len(group) * (np.mean(group) - grand_mean)**2 
                 for group in group_data)
        df_between = k_groups - 1
        msb = ssb / df_between
        
        # Within-group variance (SSW)
        ssw = sum(np.sum((group - np.mean(group))**2) 
                 for group in group_data)
        df_within = n_total - k_groups
        msw = ssw / df_within
        
        # F-statistic
        f_stat = msb / msw if msw > 0 else 0
        
        # P-value (using F-distribution approximation)
        from scipy import stats
        p_value = 1 - stats.f.cdf(f_stat, df_between, df_within)
        
        # Effect size (eta-squared)
        eta_squared = ssb / (ssb + ssw) if (ssb + ssw) > 0 else 0
        
        # Determine significance
        significant = p_value < self.alpha
        
        # Interpretation
        if significant:
            if eta_squared > 0.14:
                effect = "large"
            elif eta_squared > 0.06:
                effect = "medium"
            else:
                effect = "small"
            interpretation = (f"Significant difference between groups (p={p_value:.4f}). "
                            f"Effect size: {effect} (η²={eta_squared:.3f})")
        else:
            interpretation = f"No significant difference between groups (p={p_value:.4f})"
        
        result = ANOVAResult(
            f_statistic=f_stat,
            p_value=p_value,
            df_between=df_between,
            df_within=df_within,
            significant=significant,
            effect_size_eta_squared=eta_squared,
            interpretation=interpretation
        )
        
        self.results_cache.append(('anova', result))
        
        return result
    
    def regression(self,
                  X: np.ndarray,
                  y: np.ndarray,
                  predictor_names: Optional[List[str]] = None) -> RegressionResult:
        """
        Multiple Linear Regression
        
        Model: y = β₀ + β₁X₁ + β₂X₂ + ... + ε
        
        Example:
            Predict overall_consciousness from phi, global_availability, meta_depth
        
        Args:
            X: Predictor variables (n_samples, n_features) or (n_samples,) for simple
            y: Outcome variable (n_samples,)
            predictor_names: Names of predictors
            
        Returns:
            RegressionResult with coefficients, R², p-values
        """
        # Ensure X is 2D
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        
        n_samples, n_features = X.shape
        
        # Add intercept column
        X_with_intercept = np.column_stack([np.ones(n_samples), X])
        
        # Calculate coefficients using normal equation: β = (X'X)⁻¹X'y
        try:
            XtX = X_with_intercept.T @ X_with_intercept
            Xty = X_with_intercept.T @ y
            coefficients = np.linalg.solve(XtX, Xty)
        except np.linalg.LinAlgError:
            # Singular matrix, use pseudoinverse
            coefficients = np.linalg.lstsq(X_with_intercept, y, rcond=None)[0]
        
        # Predictions
        predictions = X_with_intercept @ coefficients
        residuals = y - predictions
        
        # R-squared
        ss_total = np.sum((y - np.mean(y))**2)
        ss_residual = np.sum(residuals**2)
        r_squared = 1 - (ss_residual / ss_total) if ss_total > 0 else 0
        
        # Adjusted R-squared
        adj_r_squared = 1 - (1 - r_squared) * (n_samples - 1) / (n_samples - n_features - 1)
        
        # F-statistic for overall model
        ms_regression = (ss_total - ss_residual) / n_features
        ms_residual = ss_residual / (n_samples - n_features - 1)
        f_stat = ms_regression / ms_residual if ms_residual > 0 else 0
        
        # P-value for F-statistic
        from scipy import stats
        p_value = 1 - stats.f.cdf(f_stat, n_features, n_samples - n_features - 1)
        
        # Create coefficient dictionary
        if predictor_names is None:
            predictor_names = [f"X{i+1}" for i in range(n_features)]
        
        coef_dict = {'intercept': coefficients[0]}
        for i, name in enumerate(predictor_names):
            coef_dict[name] = coefficients[i + 1]
        
        # Interpretation
        interpretation = (f"Model explains {r_squared*100:.1f}% of variance (R²={r_squared:.3f}). "
                        f"{'Significant' if p_value < self.alpha else 'Not significant'} "
                        f"(F={f_stat:.2f}, p={p_value:.4f})")
        
        result = RegressionResult(
            coefficients=coef_dict,
            r_squared=r_squared,
            adjusted_r_squared=adj_r_squared,
            f_statistic=f_stat,
            p_value=p_value,
            residuals=residuals,
            predictions=predictions,
            interpretation=interpretation
        )
        
        self.results_cache.append(('regression', result))
        
        return result
    
    def correlation_matrix(self,
                          data: Dict[str, List[float]],
                          method: str = 'pearson') -> Dict[Tuple[str, str], CorrelationResult]:
        """
        Compute pairwise correlations between variables
        
        Args:
            data: Dictionary mapping variable names to lists of values
            method: 'pearson' or 'spearman'
            
        Returns:
            Dictionary mapping (var1, var2) pairs to CorrelationResults
        """
        from scipy import stats as sp_stats
        
        variables = list(data.keys())
        correlations = {}
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                values1 = np.array(data[var1])
                values2 = np.array(data[var2])
                
                # Remove NaN values
                mask = ~(np.isnan(values1) | np.isnan(values2))
                values1 = values1[mask]
                values2 = values2[mask]
                
                if len(values1) < 3:
                    continue
                
                # Calculate correlation
                if method == 'pearson':
                    corr, p_val = sp_stats.pearsonr(values1, values2)
                elif method == 'spearman':
                    corr, p_val = sp_stats.spearmanr(values1, values2)
                else:
                    raise ValueError(f"Unknown method: {method}")
                
                # Determine strength
                abs_corr = abs(corr)
                if abs_corr > 0.7:
                    strength = "strong"
                elif abs_corr > 0.4:
                    strength = "moderate"
                elif abs_corr > 0.2:
                    strength = "weak"
                else:
                    strength = "very weak"
                
                # Significance
                significant = p_val < self.alpha
                
                # Interpretation
                direction = "positive" if corr > 0 else "negative"
                interpretation = (f"{strength.capitalize()} {direction} correlation "
                                f"(r={corr:.3f}, p={p_val:.4f}). "
                                f"{'Significant' if significant else 'Not significant'}.")
                
                result = CorrelationResult(
                    correlation=corr,
                    p_value=p_val,
                    significant=significant,
                    strength=strength,
                    interpretation=interpretation
                )
                
                correlations[(var1, var2)] = result
        
        return correlations
    
    def effect_size(self,
                   group1: List[float],
                   group2: List[float]) -> EffectSizeResult:
        """
        Calculate Cohen's d effect size between two groups
        
        Cohen's d = (M₁ - M₂) / SD_pooled
        
        Interpretation:
        - Small: d = 0.2
        - Medium: d = 0.5
        - Large: d = 0.8
        
        Args:
            group1: First group values
            group2: Second group values
            
        Returns:
            EffectSizeResult with Cohen's d and interpretation
        """
        arr1 = np.array(group1)
        arr2 = np.array(group2)
        
        # Calculate means
        mean1 = np.mean(arr1)
        mean2 = np.mean(arr2)
        
        # Calculate pooled standard deviation
        n1 = len(arr1)
        n2 = len(arr2)
        var1 = np.var(arr1, ddof=1)
        var2 = np.var(arr2, ddof=1)
        
        pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        # Cohen's d
        d = (mean1 - mean2) / pooled_sd if pooled_sd > 0 else 0
        
        # Interpretation
        abs_d = abs(d)
        if abs_d > 0.8:
            size = "large"
        elif abs_d > 0.5:
            size = "medium"
        elif abs_d > 0.2:
            size = "small"
        else:
            size = "negligible"
        
        direction = "higher" if d > 0 else "lower"
        interpretation = (f"Cohen's d = {d:.3f} ({size} effect). "
                        f"Group 1 is {abs_d:.2f} standard deviations {direction} than Group 2.")
        
        result = EffectSizeResult(
            cohens_d=d,
            interpretation=interpretation
        )
        
        return result
    
    def t_test(self,
              group1: List[float],
              group2: List[float],
              paired: bool = False) -> Dict[str, Any]:
        """
        Independent or paired t-test
        
        Args:
            group1: First group values
            group2: Second group values
            paired: If True, use paired t-test
            
        Returns:
            Dictionary with t-statistic, p-value, significance
        """
        from scipy import stats
        
        arr1 = np.array(group1)
        arr2 = np.array(group2)
        
        if paired:
            t_stat, p_val = stats.ttest_rel(arr1, arr2)
            test_type = "Paired t-test"
        else:
            t_stat, p_val = stats.ttest_ind(arr1, arr2)
            test_type = "Independent t-test"
        
        significant = p_val < self.alpha
        
        # Calculate effect size
        effect = self.effect_size(group1, group2)
        
        return {
            'test_type': test_type,
            't_statistic': t_stat,
            'p_value': p_val,
            'significant': significant,
            'effect_size': effect.cohens_d,
            'interpretation': (f"{test_type}: t={t_stat:.3f}, p={p_val:.4f}. "
                             f"{'Significant' if significant else 'Not significant'} difference. "
                             f"{effect.interpretation}")
        }
    
    def confidence_interval(self,
                          data: List[float],
                          confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Calculate confidence interval for mean
        
        Args:
            data: Sample data
            confidence: Confidence level (default 0.95 for 95% CI)
            
        Returns:
            Tuple of (mean, lower_bound, upper_bound)
        """
        from scipy import stats
        
        arr = np.array(data)
        n = len(arr)
        mean = np.mean(arr)
        se = stats.sem(arr)
        
        # t-distribution critical value
        df = n - 1
        t_crit = stats.t.ppf((1 + confidence) / 2, df)
        
        margin = t_crit * se
        lower = mean - margin
        upper = mean + margin
        
        return mean, lower, upper
    
    def test_retest_reliability(self,
                               test_scores: List[float],
                               retest_scores: List[float]) -> Dict[str, Any]:
        """
        Test-retest reliability using correlation
        
        Measures consistency of measurements over time.
        
        Args:
            test_scores: Scores from first test
            retest_scores: Scores from retest
            
        Returns:
            Dictionary with correlation, p-value, interpretation
        """
        from scipy import stats
        
        arr1 = np.array(test_scores)
        arr2 = np.array(retest_scores)
        
        # Pearson correlation
        corr, p_val = stats.pearsonr(arr1, arr2)
        
        # Interpretation based on reliability standards
        if corr > 0.90:
            reliability = "excellent"
        elif corr > 0.80:
            reliability = "good"
        elif corr > 0.70:
            reliability = "acceptable"
        else:
            reliability = "poor"
        
        return {
            'correlation': corr,
            'p_value': p_val,
            'reliability': reliability,
            'interpretation': (f"Test-retest reliability: r={corr:.3f} ({reliability}). "
                             f"{'Significant' if p_val < self.alpha else 'Not significant'} "
                             f"(p={p_val:.4f})")
        }
    
    def inter_rater_reliability(self,
                               ratings: List[List[float]]) -> Dict[str, Any]:
        """
        Inter-rater reliability using Cronbach's alpha
        
        Measures consistency across multiple raters/items.
        
        Args:
            ratings: List of rating lists (each list = one rater's ratings)
            
        Returns:
            Dictionary with Cronbach's alpha and interpretation
        """
        # Convert to array (items × raters)
        arr = np.array(ratings).T
        n_items, n_raters = arr.shape
        
        # Calculate Cronbach's alpha
        # α = (k/(k-1)) * (1 - Σσ²ᵢ/σ²ₜ)
        
        item_vars = np.var(arr, axis=1, ddof=1)
        total_var = np.var(arr.sum(axis=1), ddof=1)
        
        sum_item_vars = np.sum(item_vars)
        
        if total_var > 0:
            alpha = (n_raters / (n_raters - 1)) * (1 - sum_item_vars / total_var)
        else:
            alpha = 0.0
        
        # Interpretation
        if alpha > 0.90:
            reliability = "excellent"
        elif alpha > 0.80:
            reliability = "good"
        elif alpha > 0.70:
            reliability = "acceptable"
        else:
            reliability = "poor"
        
        return {
            'cronbachs_alpha': alpha,
            'n_raters': n_raters,
            'n_items': n_items,
            'reliability': reliability,
            'interpretation': (f"Cronbach's α = {alpha:.3f} ({reliability} reliability) "
                             f"across {n_raters} raters and {n_items} items.")
        }
    
    def internal_consistency(self,
                           measures: Dict[str, List[float]]) -> Dict[Tuple[str, str], float]:
        """
        Internal consistency - correlations between related measures
        
        Related measures should correlate positively.
        
        Args:
            measures: Dictionary mapping measure names to lists of values
            
        Returns:
            Dictionary of pairwise correlations
        """
        correlations = {}
        variables = list(measures.keys())
        
        from scipy import stats
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                values1 = np.array(measures[var1])
                values2 = np.array(measures[var2])
                
                corr, _ = stats.pearsonr(values1, values2)
                correlations[(var1, var2)] = corr
        
        return correlations
    
    def bonferroni_correction(self,
                            p_values: List[float],
                            alpha: Optional[float] = None) -> List[bool]:
        """
        Bonferroni correction for multiple comparisons
        
        Adjusted alpha = α / n_tests
        
        Args:
            p_values: List of p-values from multiple tests
            alpha: Significance level (uses self.alpha if None)
            
        Returns:
            List of booleans indicating significance after correction
        """
        if alpha is None:
            alpha = self.alpha
        
        n_tests = len(p_values)
        adjusted_alpha = alpha / n_tests
        
        return [p < adjusted_alpha for p in p_values]
    
    def generate_report(self, filepath: str = 'statistical_report.txt'):
        """
        Generate comprehensive statistical report
        
        Args:
            filepath: Output file path
        """
        if not self.results_cache:
            print("No statistical analyses cached to report.")
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATISTICAL ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            
            for i, (test_type, result) in enumerate(self.results_cache):
                f.write(f"Analysis {i+1}: {test_type.upper()}\n")
                f.write("-"*70 + "\n")
                
                if test_type == 'anova':
                    f.write(f"F-statistic: {result.f_statistic:.4f}\n")
                    f.write(f"p-value: {result.p_value:.4f}\n")
                    f.write(f"Effect size (η²): {result.effect_size_eta_squared:.4f}\n")
                    f.write(f"Significant: {result.significant}\n")
                    f.write(f"\nInterpretation: {result.interpretation}\n")
                
                elif test_type == 'regression':
                    f.write(f"R²: {result.r_squared:.4f}\n")
                    f.write(f"Adjusted R²: {result.adjusted_r_squared:.4f}\n")
                    f.write(f"F-statistic: {result.f_statistic:.4f}\n")
                    f.write(f"p-value: {result.p_value:.4f}\n")
                    f.write(f"\nCoefficients:\n")
                    for name, coef in result.coefficients.items():
                        f.write(f"  {name}: {coef:.4f}\n")
                    f.write(f"\nInterpretation: {result.interpretation}\n")
                
                f.write("\n" + "="*70 + "\n\n")
        
        print(f"✓ Statistical report saved to {filepath}")


# Convenience functions

def compare_conditions(results_by_condition: Dict[str, List[Any]],
                      metric_name: str = 'overall_consciousness',
                      alpha: float = 0.05) -> ANOVAResult:
    """
    Compare multiple experimental conditions using ANOVA
    
    Args:
        results_by_condition: Dictionary mapping condition names to trial results
        metric_name: Name of metric to compare
        alpha: Significance level
        
    Returns:
        ANOVAResult
    """
    analyzer = StatisticalAnalysis(alpha=alpha)
    
    # Extract metric values for each condition
    groups = {}
    for condition, trials in results_by_condition.items():
        values = [t.metrics[metric_name] if hasattr(t, 'metrics') 
                 else t[metric_name] for t in trials]
        groups[condition] = values
    
    return analyzer.anova(groups, dependent_var=metric_name)


def analyze_parameter_effect(results_by_value: Dict[Any, List[Any]],
                            metric_name: str = 'overall_consciousness') -> RegressionResult:
    """
    Analyze effect of parameter on metric using regression
    
    Args:
        results_by_value: Dictionary mapping parameter values to trial results
        metric_name: Name of metric to analyze
        
    Returns:
        RegressionResult
    """
    analyzer = StatisticalAnalysis()
    
    # Extract data
    X = []
    y = []
    
    for param_value, trials in results_by_value.items():
        for trial in trials:
            X.append(param_value)
            metric_val = trial.metrics[metric_name] if hasattr(trial, 'metrics') else trial[metric_name]
            y.append(metric_val)
    
    X = np.array(X)
    y = np.array(y)
    
    return analyzer.regression(X, y, predictor_names=['parameter'])


def create_statistical_analyzer(alpha: float = 0.05) -> StatisticalAnalysis:
    """Create StatisticalAnalysis instance"""
    return StatisticalAnalysis(alpha=alpha)
