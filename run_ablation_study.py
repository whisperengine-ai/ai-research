#!/usr/bin/env python3
"""
Pilot Ablation Study: Component Impact Analysis
Tests consciousness simulator with different component configurations

Conditions:
1. FULL_SYSTEM - All components enabled (baseline)
2. NO_EMOTIONS - Disable neurochemical emotion system
3. NO_RECURSION - Disable recursive meta-cognition
4. NO_GWT - Disable global workspace theory

Design: 4 conditions × 10 trials × 8 test inputs = 320 conversations
Expected runtime: 30-60 minutes (depending on LLM latency)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import numpy as np

from consciousness_chatbot import ConsciousnessSimulator
from run_conversation_test import SCENARIOS
from research_dashboard import ResearchDashboard
from reliability_validity import MetricValidator


# Test inputs (representative prompts)
ABLATION_TEST_INPUTS = [
    "I'm feeling frustrated with my current situation.",
    "How do you think I should approach this problem?",
    "I'm worried about making the wrong decision.",
    "Tell me about your own thinking process.",
    "I feel like I'm making progress on this.",
    "I'm not sure if I can handle this challenge.",
    "What's your perspective on human consciousness?",
    "I appreciate your help with this.",
]

# Experiment conditions
ABLATION_CONDITIONS = {
    'full_system': {
        'description': 'All components enabled (baseline)',
        'config': {
            'use_gwt': True,
            'use_recursion': True,
            'use_emotions': True,
            'use_memory': True,
            'recursion_depth': 3
        }
    },
    'no_emotions': {
        'description': 'Neurochemical emotion system disabled',
        'config': {
            'use_gwt': True,
            'use_recursion': True,
            'use_emotions': False,
            'use_memory': True,
            'recursion_depth': 3
        }
    },
    'no_recursion': {
        'description': 'Recursive meta-cognition disabled',
        'config': {
            'use_gwt': True,
            'use_recursion': False,
            'use_emotions': True,
            'use_memory': True,
            'recursion_depth': 0
        }
    },
    'no_gwt': {
        'description': 'Global workspace theory disabled',
        'config': {
            'use_gwt': False,
            'use_recursion': True,
            'use_emotions': True,
            'use_memory': True,
            'recursion_depth': 3
        }
    }
}


class AblationStudy:
    """Run ablation study and analyze results"""
    
    def __init__(self, trials_per_condition=10, verbose=True):
        self.trials_per_condition = trials_per_condition
        self.verbose = verbose
        self.results = {name: [] for name in ABLATION_CONDITIONS.keys()}
        self.start_time = datetime.now()
    
    def log(self, message, level="INFO"):
        """Print log message"""
        if self.verbose:
            print(f"[{level}] {message}")
    
    def run_condition(self, condition_name, config):
        """Run all trials for a condition"""
        self.log(f"\n{'='*70}")
        self.log(f"CONDITION: {condition_name.upper()}", level="CONDITION")
        self.log(f"Description: {ABLATION_CONDITIONS[condition_name]['description']}")
        self.log(f"Trials: {self.trials_per_condition}")
        self.log(f"{'='*70}\n")
        
        condition_results = {
            'metrics': [],
            'conversations': []
        }
        
        # Run trials
        for trial_num in range(self.trials_per_condition):
            self.log(f"\nTrial {trial_num + 1}/{self.trials_per_condition}:")
            
            trial_metrics = []
            
            # Run each test input
            for input_idx, test_input in enumerate(ABLATION_TEST_INPUTS):
                try:
                    # Create simulator with condition config
                    bot = ConsciousnessSimulator(
                        verbose=False,
                        **config
                    )
                    
                    # Run interaction
                    response = bot.process_input(test_input)
                    
                    # Get metrics from last consciousness score
                    if bot.last_consciousness_score:
                        metrics = bot.last_consciousness_score.to_dict()
                        trial_metrics.append(metrics)
                    
                    # Get interaction dynamics
                    if bot.interaction_dynamics.interactions:
                        last_interaction = bot.interaction_dynamics.interactions[-1]
                        
                        condition_results['conversations'].append({
                            'condition': condition_name,
                            'trial': trial_num + 1,
                            'input_idx': input_idx + 1,
                            'user_input': test_input[:100],
                            'resonance': last_interaction.get('resonance', 0),
                            'engagement': last_interaction.get('engagement', 0),
                            'appropriateness': last_interaction.get('appropriateness', 0),
                            'metrics': metrics
                        })
                    
                    if (input_idx + 1) % 4 == 0:
                        self.log(f"  Inputs {input_idx - 2}-{input_idx + 1}: ✓")
                
                except Exception as e:
                    self.log(f"  Error on input {input_idx + 1}: {e}", level="ERROR")
                    continue
            
            # Aggregate trial metrics
            if trial_metrics:
                trial_avg = {}
                for key in trial_metrics[0].keys():
                    trial_avg[key] = np.mean([m[key] for m in trial_metrics])
                
                condition_results['metrics'].append(trial_avg)
                
                self.log(f"  Trial complete: Φ={trial_avg['phi']:.3f}, Overall={trial_avg['overall_consciousness']:.3f}")
        
        self.results[condition_name] = condition_results
        self._print_condition_summary(condition_name, condition_results)
        
        return condition_results
    
    def _print_condition_summary(self, condition_name, results):
        """Print summary for a condition"""
        metrics_list = results['metrics']
        
        if not metrics_list:
            self.log(f"No metrics for {condition_name}", level="WARNING")
            return
        
        print(f"\n  📊 CONDITION SUMMARY ({condition_name}):")
        print(f"  Trials completed: {len(metrics_list)}")
        
        # Average metrics
        avg_phi = np.mean([m['phi'] for m in metrics_list])
        avg_overall = np.mean([m['overall_consciousness'] for m in metrics_list])
        avg_ga = np.mean([m['global_availability'] for m in metrics_list])
        avg_meta = np.mean([m['meta_cognitive_depth'] for m in metrics_list])
        
        print(f"\n  Φ (Integration):          {avg_phi:.3f}")
        print(f"  Global Availability:     {avg_ga:.3f}")
        print(f"  Meta-Cognitive Depth:    {avg_meta:.3f}")
        print(f"  Overall Consciousness:   {avg_overall:.3f}")
    
    def run_full_study(self):
        """Run complete ablation study"""
        self.log("\n" + "="*70)
        self.log("PILOT ABLATION STUDY - Component Impact Analysis")
        self.log("="*70)
        self.log(f"Conditions: {len(ABLATION_CONDITIONS)}")
        self.log(f"Trials per condition: {self.trials_per_condition}")
        self.log(f"Test inputs: {len(ABLATION_TEST_INPUTS)}")
        self.log(f"Total conversations: {len(ABLATION_CONDITIONS) * self.trials_per_condition * len(ABLATION_TEST_INPUTS)}")
        self.log(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run each condition
        for condition_name, condition_info in ABLATION_CONDITIONS.items():
            self.run_condition(condition_name, condition_info['config'])
        
        # Print final summary
        self._print_ablation_summary()
        
        # Export results
        self.export_results()
    
    def _print_ablation_summary(self):
        """Print overall ablation study summary"""
        print("\n" + "="*70)
        print("ABLATION STUDY SUMMARY")
        print("="*70)
        
        condition_averages = {}
        
        for condition_name, results in self.results.items():
            metrics_list = results['metrics']
            if metrics_list:
                avg = {
                    'phi': np.mean([m['phi'] for m in metrics_list]),
                    'overall': np.mean([m['overall_consciousness'] for m in metrics_list]),
                    'ga': np.mean([m['global_availability'] for m in metrics_list]),
                    'meta': np.mean([m['meta_cognitive_depth'] for m in metrics_list]),
                    'trials': len(metrics_list)
                }
                condition_averages[condition_name] = avg
        
        # Print table
        print(f"\n{'Condition':<20} {'Φ':<8} {'Overall':<10} {'GA':<8} {'Meta':<8}")
        print("-" * 60)
        
        baseline = condition_averages.get('full_system', {})
        baseline_overall = baseline.get('overall', 0)
        
        for condition_name, avg in condition_averages.items():
            marker = " ← BASELINE" if condition_name == 'full_system' else ""
            diff = ((avg['overall'] - baseline_overall) / baseline_overall * 100) if baseline_overall else 0
            
            print(f"{condition_name:<20} {avg['phi']:<8.3f} {avg['overall']:<10.3f} {avg['ga']:<8.3f} {avg['meta']:<8.3f}{marker}")
            
            if condition_name != 'full_system':
                impact = "SIGNIFICANT" if abs(diff) > 10 else "MODERATE" if abs(diff) > 5 else "MINIMAL"
                print(f"  → Impact: {diff:+.1f}% ({impact})")
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds() / 60
        
        print(f"\n{'='*70}")
        print(f"Duration: {duration:.1f} minutes")
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
    
    def export_results(self):
        """Export results to JSON and generate dashboard"""
        print(f"\n📊 Exporting results...\n")
        
        # Prepare export data
        export_data = {
            'metadata': {
                'timestamp': self.start_time.isoformat(),
                'study_name': 'Pilot Ablation Study',
                'conditions': len(ABLATION_CONDITIONS),
                'trials_per_condition': self.trials_per_condition,
                'test_inputs': len(ABLATION_TEST_INPUTS)
            },
            'conditions': {}
        }
        
        # Add condition data
        for condition_name, results in self.results.items():
            export_data['conditions'][condition_name] = {
                'description': ABLATION_CONDITIONS[condition_name]['description'],
                'config': ABLATION_CONDITIONS[condition_name]['config'],
                'trials': len(results['metrics']),
                'conversations': results['conversations'],
                'summary_metrics': {
                    'phi': float(np.mean([m['phi'] for m in results['metrics']])) if results['metrics'] else 0,
                    'overall_consciousness': float(np.mean([m['overall_consciousness'] for m in results['metrics']])) if results['metrics'] else 0,
                    'global_availability': float(np.mean([m['global_availability'] for m in results['metrics']])) if results['metrics'] else 0,
                    'meta_cognitive_depth': float(np.mean([m['meta_cognitive_depth'] for m in results['metrics']])) if results['metrics'] else 0
                }
            }
        
        # Save results
        results_file = 'ablation_study_results.json'
        with open(results_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Results exported to {results_file}")
        
        # Generate dashboard if we have enough data
        total_conversations = sum(
            len(results['conversations']) 
            for results in self.results.values()
        )
        
        if total_conversations > 0:
            print(f"\n📈 Generating dashboards ({total_conversations} total conversations)...")
            
            # Save conversation data in format expected by dashboard
            dashboard_data = {
                'conversations': []
            }
            
            for condition_name, results in self.results.items():
                for conv_data in results['conversations']:
                    dashboard_data['conversations'].append({
                        'name': f"{condition_name} (trial {conv_data['trial']})",
                        'turns': conv_data['input_idx'],
                        'analysis': {
                            'resonance_analysis': {
                                'status': 'success',
                                'average_resonance': conv_data['resonance']
                            },
                            'engagement_trajectory': {
                                'status': 'success',
                                'average_engagement': conv_data['engagement']
                            },
                            'emotional_trajectory': {
                                'status': 'success',
                                'trajectory': 0.0,
                                'direction': 'stable',
                                'start_emotion': 'neutral',
                                'end_emotion': 'neutral'
                            },
                            'appropriateness_analysis': {
                                'status': 'success',
                                'average_appropriateness': conv_data['appropriateness']
                            }
                        }
                    })
            
            # Save dashboard data
            dashboard_file = 'ablation_study_dashboard_data.json'
            with open(dashboard_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
            # Generate visualizations
            dashboard = ResearchDashboard()
            dashboard.load_json(dashboard_file)
            outputs = dashboard.plot_all('ablation_output')
            
            print(f"\n✓ Generated {len(outputs)} visualizations in ablation_output/")
            for name, path in list(outputs.items())[:3]:
                print(f"  • {name}")
            print(f"  ... and {len(outputs) - 3} more")
        
        print(f"\n✅ Export complete!")


def main():
    """Run ablation study"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run ablation study')
    parser.add_argument('--trials', type=int, default=10, help='Trials per condition (default: 10)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    study = AblationStudy(trials_per_condition=args.trials, verbose=args.verbose)
    study.run_full_study()


if __name__ == '__main__':
    main()
