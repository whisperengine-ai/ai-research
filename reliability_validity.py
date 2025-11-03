"""
Reliability & Validity Measurements for Consciousness Metrics
Extends consciousness_statistics module with research-grade validation
"""

import numpy as np
from scipy import stats as scipy_stats
from typing import Dict, List, Tuple, Optional


class ReliabilityValidator:
    """Test-retest reliability, consistency, and reproducibility"""
    
    @staticmethod
    def cronbach_alpha(data: np.ndarray) -> float:
        """Compute Cronbach's alpha for internal consistency"""
        n_items = data.shape[1]
        item_vars = np.var(data, axis=0, ddof=1)
        total_var = np.var(np.sum(data, axis=1), ddof=1)
        alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_vars) / total_var)
        return float(np.clip(alpha, -1, 1))
    
    @staticmethod
    def test_retest_reliability(test1: np.ndarray, test2: np.ndarray) -> Dict:
        """Compute test-retest reliability (ICC)"""
        # Intraclass correlation coefficient (2,1)
        n = len(test1)
        mean_1 = np.mean(test1)
        mean_2 = np.mean(test2)
        ss_between = n * ((mean_1 - np.mean([mean_1, mean_2]))**2 + 
                         (mean_2 - np.mean([mean_1, mean_2]))**2)
        ss_within = np.sum((test1 - test2)**2)
        ss_total = ss_between + ss_within
        ms_between = ss_between / 1
        ms_within = ss_within / (2*n - 2)
        icc = (ms_between - ms_within) / (ms_between + ms_within)
        
        return {
            'icc_2_1': float(np.clip(icc, -1, 1)),
            'correlation': float(np.corrcoef(test1, test2)[0, 1]),
            'mean_difference': float(np.mean(test1 - test2)),
            'std_difference': float(np.std(test1 - test2, ddof=1))
        }
    
    @staticmethod
    def split_half_reliability(data: np.ndarray) -> Dict:
        """Split-half reliability (Spearman-Brown corrected)"""
        n = len(data)
        split1 = data[:n//2]
        split2 = data[n//2:]
        r = np.corrcoef(split1, split2)[0, 1]
        # Spearman-Brown correction
        sb_r = 2*r / (1 + r)
        
        return {
            'split_half_correlation': float(r),
            'spearman_brown_corrected': float(sb_r),
            'n_items': len(split1) + len(split2)
        }
    
    @staticmethod
    def homogeneity(items: List[np.ndarray]) -> Dict:
        """Item homogeneity analysis"""
        if len(items) < 2:
            return {'status': 'insufficient_data'}
        
        data = np.array(items)
        correlations = []
        
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                corr = np.corrcoef(data[i], data[j])[0, 1]
                if not np.isnan(corr):
                    correlations.append(corr)
        
        if not correlations:
            return {'status': 'no_correlations'}
        
        return {
            'mean_inter_item_correlation': float(np.mean(correlations)),
            'min_correlation': float(np.min(correlations)),
            'max_correlation': float(np.max(correlations)),
            'std_correlation': float(np.std(correlations, ddof=1)),
            'num_correlations': len(correlations)
        }


class ValidityValidator:
    """Construct validity, convergent/discriminant validity, criterion validity"""
    
    @staticmethod
    def construct_validity(theoretical_construct: np.ndarray, 
                          measured_construct: np.ndarray) -> Dict:
        """Correlation with theoretical construct"""
        corr, p_value = scipy_stats.pearsonr(theoretical_construct, measured_construct)
        
        return {
            'correlation': float(corr),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'r_squared': float(corr**2),  # Variance explained
        }
    
    @staticmethod
    def convergent_validity(measure1: np.ndarray, measure2: np.ndarray, 
                           expected_r: float = 0.7) -> Dict:
        """Related measures should correlate (>0.7)"""
        corr, p_value = scipy_stats.pearsonr(measure1, measure2)
        
        return {
            'correlation': float(corr),
            'p_value': float(p_value),
            'meets_threshold': corr >= expected_r,
            'expected_r': expected_r,
            'status': 'valid' if corr >= expected_r else 'questionable'
        }
    
    @staticmethod
    def discriminant_validity(measure1: np.ndarray, measure2: np.ndarray,
                             expected_r: float = 0.3) -> Dict:
        """Unrelated measures should weakly correlate (<0.3)"""
        corr, p_value = scipy_stats.pearsonr(measure1, measure2)
        
        return {
            'correlation': float(corr),
            'p_value': float(p_value),
            'discriminant': abs(corr) <= expected_r,
            'max_r': expected_r,
            'status': 'valid' if abs(corr) <= expected_r else 'overlap'
        }
    
    @staticmethod
    def criterion_validity(predictor: np.ndarray, criterion: np.ndarray) -> Dict:
        """Predictive validity - can measure predict outcome?"""
        # Linear regression
        slope, intercept, r_value, p_value, std_err = scipy_stats.linregress(predictor, criterion)
        
        return {
            'correlation': float(r_value),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'slope': float(slope),
            'intercept': float(intercept),
            'std_error': float(std_err),
            'r_squared': float(r_value**2),
            'predictive_power': 'strong' if r_value**2 > 0.5 else 'moderate' if r_value**2 > 0.25 else 'weak'
        }
    
    @staticmethod
    def factor_validity(data: np.ndarray, n_factors: int = 2) -> Dict:
        """Principal component analysis for construct validity"""
        try:
            u, s, vt = np.linalg.svd(np.cov(data.T))
            variance_explained = s[:n_factors] / np.sum(s)
            cumsum_var = np.cumsum(variance_explained)
            
            return {
                'n_factors': n_factors,
                'variance_explained': [float(v) for v in variance_explained],
                'cumulative_variance': [float(cv) for cv in cumsum_var],
                'total_variance_explained': float(cumsum_var[-1]) if len(cumsum_var) > 0 else 0,
                'sufficient': cumsum_var[-1] > 0.6 if len(cumsum_var) > 0 else False
            }
        except:
            return {'status': 'error', 'message': 'Could not compute SVD'}


class MetricValidator:
    """Comprehensive validation of all consciousness metrics"""
    
    def __init__(self):
        self.reliability = ReliabilityValidator()
        self.validity = ValidityValidator()
    
    def validate_consciousness_metric(self, metric_data: List[float],
                                     metric_name: str) -> Dict:
        """Full validation report for a single metric"""
        data = np.array(metric_data)
        
        if len(data) < 3:
            return {'status': 'insufficient_data', 'n': len(data)}
        
        # Basic statistics
        report = {
            'metric': metric_name,
            'n': len(data),
            'mean': float(np.mean(data)),
            'std': float(np.std(data, ddof=1)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'range': float(np.max(data) - np.min(data)),
            'skewness': float(scipy_stats.skew(data)),
            'kurtosis': float(scipy_stats.kurtosis(data)),
        }
        
        # Normality test (Shapiro-Wilk)
        if len(data) <= 5000:
            stat, p_norm = scipy_stats.shapiro(data)
            report['normality_test'] = {
                'statistic': float(stat),
                'p_value': float(p_norm),
                'normal': p_norm > 0.05
            }
        
        return report
    
    def compare_metrics(self, metrics: Dict[str, List[float]]) -> Dict:
        """Compare multiple metrics for validity patterns"""
        if len(metrics) < 2:
            return {'status': 'insufficient_metrics'}
        
        metric_names = list(metrics.keys())
        metric_arrays = {k: np.array(v) for k, v in metrics.items()}
        
        # Pairwise comparisons
        comparisons = {}
        for i, m1 in enumerate(metric_names):
            for j in range(i+1, len(metric_names)):
                m2 = metric_names[j]
                key = f'{m1}_vs_{m2}'
                
                # Determine if should converge or diverge based on names
                should_converge = any(keyword in m1.lower() and keyword in m2.lower() 
                                     for keyword in ['emotion', 'engagement', 'resonance'])
                
                if should_converge:
                    comparisons[key] = self.validity.convergent_validity(
                        metric_arrays[m1], metric_arrays[m2]
                    )
                else:
                    comparisons[key] = self.validity.discriminant_validity(
                        metric_arrays[m1], metric_arrays[m2]
                    )
        
        return comparisons
    
    def generate_validity_report(self, data: Dict[str, List[float]]) -> Dict:
        """Generate comprehensive validity report"""
        report = {
            'individual_metrics': {},
            'pairwise_comparisons': self.compare_metrics(data),
            'summary': {}
        }
        
        for metric_name, values in data.items():
            report['individual_metrics'][metric_name] = \
                self.validate_consciousness_metric(values, metric_name)
        
        # Summary statistics
        valid_count = 0
        questionable_count = 0
        
        for comp_name, comp_data in report['pairwise_comparisons'].items():
            if comp_data.get('meets_threshold'):
                valid_count += 1
            elif not comp_data.get('discriminant'):
                questionable_count += 1
        
        total = len(report['pairwise_comparisons'])
        report['summary'] = {
            'total_comparisons': total,
            'valid_comparisons': valid_count,
            'questionable_comparisons': questionable_count,
            'validity_score': float(valid_count / total) if total > 0 else 0,
            'overall_assessment': 'good' if valid_count / total > 0.7 else 'fair' if valid_count / total > 0.5 else 'poor'
        }
        
        return report


# Example usage
if __name__ == '__main__':
    # Generate sample data
    np.random.seed(42)
    n = 50
    
    # Simulated consciousness metrics
    metrics = {
        'phi': np.clip(np.random.normal(0.5, 0.15, n), 0, 1),
        'global_availability': np.clip(np.random.normal(0.7, 0.1, n), 0, 1),
        'meta_cognitive_depth': np.clip(np.random.normal(0.65, 0.12, n), 0, 1),
        'temporal_binding': np.clip(np.random.normal(0.45, 0.15, n), 0, 1),
        'reportability': np.clip(np.random.normal(0.75, 0.1, n), 0, 1),
    }
    
    # Validate
    validator = MetricValidator()
    report = validator.generate_validity_report(metrics)
    
    # Print results
    print("\n" + "="*70)
    print("CONSCIOUSNESS METRICS VALIDITY REPORT")
    print("="*70)
    
    print("\n📊 INDIVIDUAL METRICS:")
    for metric_name, metric_data in report['individual_metrics'].items():
        if metric_data.get('status') != 'insufficient_data':
            print(f"\n{metric_name}:")
            print(f"  Mean: {metric_data['mean']:.3f} ± {metric_data['std']:.3f}")
            print(f"  Range: {metric_data['min']:.3f} - {metric_data['max']:.3f}")
            print(f"  Skewness: {metric_data['skewness']:.3f}")
            if 'normality_test' in metric_data:
                normal = "✓" if metric_data['normality_test']['normal'] else "✗"
                print(f"  Normal distribution: {normal} (p={metric_data['normality_test']['p_value']:.3f})")
    
    print("\n\n🔗 PAIRWISE COMPARISONS:")
    for comp_name, comp_data in report['pairwise_comparisons'].items():
        status = "✓ VALID" if comp_data.get('meets_threshold') or comp_data.get('discriminant') else "✗ INVALID"
        print(f"{comp_name}: r={comp_data['correlation']:.3f} {status}")
    
    print("\n\n📈 VALIDITY SUMMARY:")
    summary = report['summary']
    print(f"Valid comparisons: {summary['valid_comparisons']}/{summary['total_comparisons']}")
    print(f"Validity score: {summary['validity_score']:.1%}")
    print(f"Assessment: {summary['overall_assessment'].upper()}")
    print("="*70)
