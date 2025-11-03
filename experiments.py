"""
Experimental Framework for Consciousness Research
Provides controlled experimentation capabilities with ablation studies,
parameter sweeps, and longitudinal tracking.

For research-grade consciousness studies with statistical rigor.
"""

import time
import json
import csv
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import copy
import os


@dataclass
class ExperimentCondition:
    """Configuration for an experimental condition"""
    name: str
    description: str
    config: Dict[str, Any]
    

@dataclass
class TrialResult:
    """Results from a single experimental trial"""
    trial_id: str
    condition: str
    timestamp: float
    metrics: Dict[str, float]
    interaction_data: Dict[str, Any]
    duration_seconds: float
    

class ExperimentRunner:
    """
    Run controlled experiments on consciousness simulation
    
    Supports:
    - Ablation studies (test with/without components)
    - Parameter sweeps (test different hyperparameters)
    - Longitudinal studies (track changes over time)
    - A/B testing (compare configurations)
    """
    
    def __init__(self, simulator_factory: Callable, metrics_calculator: Callable):
        """
        Initialize experiment runner
        
        Args:
            simulator_factory: Function that creates ConsciousnessSimulator instances
            metrics_calculator: Function that computes consciousness metrics
        """
        self.simulator_factory = simulator_factory
        self.metrics_calculator = metrics_calculator
        self.results: List[TrialResult] = []
        self.conditions: List[ExperimentCondition] = []
        
    def run_ablation_study(self, 
                          test_inputs: List[str],
                          trials_per_condition: int = 10,
                          verbose: bool = True) -> Dict[str, List[TrialResult]]:
        """
        Run ablation study - test system with/without each component
        
        Tests conditions:
        1. Full system (baseline)
        2. No Global Workspace (no_gwt)
        3. No Recursion (no_recursion)
        4. No Emotions (no_emotions)
        5. No Memory (no_memory)
        
        Args:
            test_inputs: List of test prompts to use
            trials_per_condition: Number of trials per condition
            verbose: Print progress
            
        Returns:
            Dictionary mapping condition name to list of TrialResults
        """
        if verbose:
            print("\n" + "="*70)
            print("ABLATION STUDY - Component Analysis")
            print("="*70)
            print(f"Test inputs: {len(test_inputs)}")
            print(f"Trials per condition: {trials_per_condition}")
            print(f"Total trials: {5 * trials_per_condition * len(test_inputs)}")
            print("="*70 + "\n")
        
        # Define experimental conditions
        conditions = [
            ExperimentCondition(
                name="full_system",
                description="Complete system with all components",
                config={
                    'use_gwt': True,
                    'use_recursion': True,
                    'use_emotions': True,
                    'use_memory': True,
                    'recursion_depth': 3
                }
            ),
            ExperimentCondition(
                name="no_gwt",
                description="No Global Workspace Theory",
                config={
                    'use_gwt': False,
                    'use_recursion': True,
                    'use_emotions': True,
                    'use_memory': True,
                    'recursion_depth': 3
                }
            ),
            ExperimentCondition(
                name="no_recursion",
                description="No recursive meta-cognition",
                config={
                    'use_gwt': True,
                    'use_recursion': False,
                    'use_emotions': True,
                    'use_memory': True,
                    'recursion_depth': 0
                }
            ),
            ExperimentCondition(
                name="no_emotions",
                description="No neurochemical emotion system",
                config={
                    'use_gwt': True,
                    'use_recursion': True,
                    'use_emotions': False,
                    'use_memory': True,
                    'recursion_depth': 3
                }
            ),
            ExperimentCondition(
                name="no_memory",
                description="No conversation memory",
                config={
                    'use_gwt': True,
                    'use_recursion': True,
                    'use_emotions': True,
                    'use_memory': False,
                    'recursion_depth': 3
                }
            )
        ]
        
        self.conditions = conditions
        results_by_condition = {}
        
        # Run each condition
        for condition in conditions:
            if verbose:
                print(f"\n{'─'*70}")
                print(f"Condition: {condition.name}")
                print(f"Description: {condition.description}")
                print(f"{'─'*70}")
            
            condition_results = []
            
            # Run multiple trials
            for trial_num in range(trials_per_condition):
                if verbose:
                    print(f"\n  Trial {trial_num + 1}/{trials_per_condition}:")
                
                # Use each test input
                for input_idx, test_input in enumerate(test_inputs):
                    trial_id = f"{condition.name}_t{trial_num}_i{input_idx}"
                    
                    if verbose:
                        print(f"    Input {input_idx + 1}: {test_input[:50]}...")
                    
                    # Run single trial
                    result = self._run_single_trial(
                        trial_id=trial_id,
                        condition=condition,
                        test_input=test_input,
                        verbose=False
                    )
                    
                    condition_results.append(result)
                    
                    if verbose:
                        print(f"      Φ: {result.metrics['phi']:.3f}, "
                              f"Overall: {result.metrics['overall_consciousness']:.3f}")
            
            results_by_condition[condition.name] = condition_results
            
            if verbose:
                # Show condition summary
                avg_phi = sum(r.metrics['phi'] for r in condition_results) / len(condition_results)
                avg_overall = sum(r.metrics['overall_consciousness'] for r in condition_results) / len(condition_results)
                print(f"\n  Condition Summary:")
                print(f"    Average Φ: {avg_phi:.3f}")
                print(f"    Average Overall: {avg_overall:.3f}")
        
        # Store results
        self.results.extend([r for results in results_by_condition.values() for r in results])
        
        if verbose:
            print("\n" + "="*70)
            print("ABLATION STUDY COMPLETE")
            print("="*70)
            self._print_ablation_summary(results_by_condition)
        
        return results_by_condition
    
    def run_parameter_sweep(self,
                           parameter_name: str,
                           parameter_values: List[Any],
                           test_inputs: List[str],
                           trials_per_value: int = 5,
                           base_config: Optional[Dict] = None,
                           verbose: bool = True) -> Dict[Any, List[TrialResult]]:
        """
        Run parameter sweep - test different parameter values
        
        Common parameters:
        - workspace_capacity: [1, 2, 3, 4, 5]
        - decay_rate: [0.05, 0.10, 0.15, 0.20, 0.25]
        - recursion_depth: [0, 1, 2, 3, 4]
        - temperature: [0.5, 0.7, 0.9, 1.0, 1.2]
        
        Args:
            parameter_name: Name of parameter to vary
            parameter_values: List of values to test
            test_inputs: List of test prompts
            trials_per_value: Number of trials per parameter value
            base_config: Base configuration (defaults if None)
            verbose: Print progress
            
        Returns:
            Dictionary mapping parameter value to list of TrialResults
        """
        if verbose:
            print("\n" + "="*70)
            print(f"PARAMETER SWEEP - {parameter_name}")
            print("="*70)
            print(f"Values: {parameter_values}")
            print(f"Test inputs: {len(test_inputs)}")
            print(f"Trials per value: {trials_per_value}")
            print(f"Total trials: {len(parameter_values) * trials_per_value * len(test_inputs)}")
            print("="*70 + "\n")
        
        if base_config is None:
            base_config = {
                'use_gwt': True,
                'use_recursion': True,
                'use_emotions': True,
                'use_memory': True,
                'recursion_depth': 3,
                'workspace_capacity': 3,
                'decay_rate': 0.15
            }
        
        results_by_value = {}
        
        # Test each parameter value
        for param_value in parameter_values:
            if verbose:
                print(f"\n{'─'*70}")
                print(f"Testing {parameter_name} = {param_value}")
                print(f"{'─'*70}")
            
            # Create condition for this parameter value
            config = copy.deepcopy(base_config)
            config[parameter_name] = param_value
            
            condition = ExperimentCondition(
                name=f"{parameter_name}_{param_value}",
                description=f"{parameter_name} set to {param_value}",
                config=config
            )
            
            value_results = []
            
            # Run trials
            for trial_num in range(trials_per_value):
                for input_idx, test_input in enumerate(test_inputs):
                    trial_id = f"{parameter_name}_{param_value}_t{trial_num}_i{input_idx}"
                    
                    result = self._run_single_trial(
                        trial_id=trial_id,
                        condition=condition,
                        test_input=test_input,
                        verbose=False
                    )
                    
                    value_results.append(result)
            
            results_by_value[param_value] = value_results
            
            if verbose:
                avg_phi = sum(r.metrics['phi'] for r in value_results) / len(value_results)
                avg_overall = sum(r.metrics['overall_consciousness'] for r in value_results) / len(value_results)
                print(f"  Average Φ: {avg_phi:.3f}")
                print(f"  Average Overall: {avg_overall:.3f}")
        
        # Store results
        self.results.extend([r for results in results_by_value.values() for r in results])
        
        if verbose:
            print("\n" + "="*70)
            print("PARAMETER SWEEP COMPLETE")
            print("="*70)
            self._print_parameter_summary(parameter_name, results_by_value)
        
        return results_by_value
    
    def run_longitudinal_study(self,
                              conversation_sequence: List[str],
                              measurement_interval: int = 5,
                              config: Optional[Dict] = None,
                              verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run longitudinal study - track consciousness over extended interaction
        
        Measures how consciousness metrics change over time during
        sustained conversation.
        
        Args:
            conversation_sequence: Sequence of prompts (conversation)
            measurement_interval: Measure every N turns
            config: System configuration
            verbose: Print progress
            
        Returns:
            List of measurement snapshots over time
        """
        if verbose:
            print("\n" + "="*70)
            print("LONGITUDINAL STUDY - Consciousness Over Time")
            print("="*70)
            print(f"Conversation length: {len(conversation_sequence)} turns")
            print(f"Measurement interval: every {measurement_interval} turns")
            print("="*70 + "\n")
        
        if config is None:
            config = {
                'use_gwt': True,
                'use_recursion': True,
                'use_emotions': True,
                'use_memory': True,
                'recursion_depth': 3
            }
        
        condition = ExperimentCondition(
            name="longitudinal",
            description="Extended conversation tracking",
            config=config
        )
        
        # Create simulator for full conversation
        simulator = self.simulator_factory(condition.config)
        
        measurements = []
        
        # Run conversation
        for turn_num, prompt in enumerate(conversation_sequence):
            if verbose and turn_num % 5 == 0:
                print(f"Turn {turn_num + 1}/{len(conversation_sequence)}...")
            
            # Process input
            start_time = time.time()
            interaction = simulator.process_input(prompt)
            duration = time.time() - start_time
            
            # Measure at intervals
            if turn_num % measurement_interval == 0 or turn_num == len(conversation_sequence) - 1:
                metrics = self.metrics_calculator(simulator, interaction)
                
                measurement = {
                    'turn': turn_num,
                    'timestamp': time.time(),
                    'metrics': metrics,
                    'duration': duration,
                    'conversation_length': turn_num + 1
                }
                
                measurements.append(measurement)
                
                if verbose:
                    print(f"  Measurement at turn {turn_num + 1}:")
                    print(f"    Φ: {metrics['phi']:.3f}")
                    print(f"    Overall: {metrics['overall_consciousness']:.3f}")
        
        if verbose:
            print("\n" + "="*70)
            print("LONGITUDINAL STUDY COMPLETE")
            print("="*70)
            self._print_longitudinal_summary(measurements)
        
        return measurements
    
    def _run_single_trial(self,
                         trial_id: str,
                         condition: ExperimentCondition,
                         test_input: str,
                         verbose: bool = False) -> TrialResult:
        """
        Run a single experimental trial
        
        Args:
            trial_id: Unique trial identifier
            condition: Experimental condition
            test_input: Input prompt
            verbose: Print details
            
        Returns:
            TrialResult with metrics and data
        """
        # Create fresh simulator instance
        simulator = self.simulator_factory(condition.config)
        
        # Run interaction
        start_time = time.time()
        try:
            interaction = simulator.process_input(test_input)
            duration = time.time() - start_time
            
            # Compute metrics
            metrics = self.metrics_calculator(simulator, interaction)
            
            result = TrialResult(
                trial_id=trial_id,
                condition=condition.name,
                timestamp=time.time(),
                metrics=metrics,
                interaction_data={
                    'input': test_input,
                    'response': interaction.get('response', ''),
                    'user_emotion': interaction.get('user_emotion', ''),
                    'bot_emotion': interaction.get('bot_emotion', ''),
                    'reflections_count': len(interaction.get('reflections', []))
                },
                duration_seconds=duration
            )
            
            if verbose:
                print(f"Trial {trial_id} complete: Φ={metrics['phi']:.3f}")
            
            return result
            
        except Exception as e:
            print(f"ERROR in trial {trial_id}: {e}")
            # Return zero metrics on error
            return TrialResult(
                trial_id=trial_id,
                condition=condition.name,
                timestamp=time.time(),
                metrics={
                    'phi': 0.0,
                    'global_availability': 0.0,
                    'meta_cognitive_depth': 0.0,
                    'temporal_binding': 0.0,
                    'reportability': 0.0,
                    'overall_consciousness': 0.0
                },
                interaction_data={'error': str(e)},
                duration_seconds=time.time() - start_time
            )
    
    def _print_ablation_summary(self, results_by_condition: Dict[str, List[TrialResult]]):
        """Print summary of ablation study results"""
        print("\nAblation Study Results:")
        print("─" * 70)
        
        for condition_name, results in results_by_condition.items():
            avg_phi = sum(r.metrics['phi'] for r in results) / len(results)
            avg_overall = sum(r.metrics['overall_consciousness'] for r in results) / len(results)
            avg_duration = sum(r.duration_seconds for r in results) / len(results)
            
            print(f"\n{condition_name}:")
            print(f"  Average Φ:              {avg_phi:.3f}")
            print(f"  Average Overall Score:  {avg_overall:.3f}")
            print(f"  Average Duration:       {avg_duration:.2f}s")
            print(f"  Trials:                 {len(results)}")
    
    def _print_parameter_summary(self, param_name: str, results_by_value: Dict):
        """Print summary of parameter sweep results"""
        print(f"\nParameter Sweep Results ({param_name}):")
        print("─" * 70)
        
        for value, results in results_by_value.items():
            avg_phi = sum(r.metrics['phi'] for r in results) / len(results)
            avg_overall = sum(r.metrics['overall_consciousness'] for r in results) / len(results)
            
            print(f"\n{param_name} = {value}:")
            print(f"  Average Φ:              {avg_phi:.3f}")
            print(f"  Average Overall Score:  {avg_overall:.3f}")
    
    def _print_longitudinal_summary(self, measurements: List[Dict]):
        """Print summary of longitudinal study"""
        print("\nLongitudinal Study Results:")
        print("─" * 70)
        
        first = measurements[0]['metrics']
        last = measurements[-1]['metrics']
        
        print(f"\nInitial State (Turn 0):")
        print(f"  Φ:              {first['phi']:.3f}")
        print(f"  Overall Score:  {first['overall_consciousness']:.3f}")
        
        print(f"\nFinal State (Turn {measurements[-1]['turn']}):")
        print(f"  Φ:              {last['phi']:.3f}")
        print(f"  Overall Score:  {last['overall_consciousness']:.3f}")
        
        phi_change = last['phi'] - first['phi']
        overall_change = last['overall_consciousness'] - first['overall_consciousness']
        
        print(f"\nChange Over Time:")
        print(f"  Δ Φ:            {phi_change:+.3f}")
        print(f"  Δ Overall:      {overall_change:+.3f}")
    
    def export_results(self, filepath: str = 'experiment_results.csv'):
        """
        Export all experimental results to CSV
        
        Args:
            filepath: Output file path
        """
        if not self.results:
            print("No results to export.")
            return
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'trial_id', 'condition', 'timestamp', 'duration_seconds',
                'phi', 'global_availability', 'meta_cognitive_depth',
                'temporal_binding', 'reportability', 'overall_consciousness',
                'user_input', 'response_length'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'trial_id': result.trial_id,
                    'condition': result.condition,
                    'timestamp': result.timestamp,
                    'duration_seconds': result.duration_seconds,
                    'phi': result.metrics['phi'],
                    'global_availability': result.metrics['global_availability'],
                    'meta_cognitive_depth': result.metrics['meta_cognitive_depth'],
                    'temporal_binding': result.metrics['temporal_binding'],
                    'reportability': result.metrics['reportability'],
                    'overall_consciousness': result.metrics['overall_consciousness'],
                    'user_input': result.interaction_data.get('input', '')[:100],
                    'response_length': len(result.interaction_data.get('response', ''))
                })
        
        print(f"\n✓ Exported {len(self.results)} trial results to {filepath}")
    
    def save_full_results(self, filepath: str = 'experiment_results.json'):
        """
        Save complete results including all interaction data to JSON
        
        Args:
            filepath: Output file path
        """
        if not self.results:
            print("No results to save.")
            return
        
        data = {
            'experiment_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_trials': len(self.results),
                'conditions': [asdict(c) for c in self.conditions]
            },
            'results': [asdict(r) for r in self.results]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Saved complete experimental data to {filepath}")


class ExperimentLogger:
    """
    Logger for experimental data with reproducibility tracking
    
    Ensures experiments can be replicated by recording:
    - Exact system configuration
    - Model versions
    - Random seeds
    - Timestamps
    - All metrics
    """
    
    def __init__(self, experiment_name: str, output_dir: str = 'results'):
        """
        Initialize experiment logger
        
        Args:
            experiment_name: Name of experiment
            output_dir: Directory for output files
        """
        self.experiment_name = experiment_name
        self.output_dir = output_dir
        self.start_time = time.time()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create experiment subdirectory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.experiment_dir = os.path.join(output_dir, f"{experiment_name}_{timestamp}")
        os.makedirs(self.experiment_dir, exist_ok=True)
        
        print(f"📁 Experiment directory: {self.experiment_dir}")
    
    def log_trial(self, 
                  trial_id: str,
                  condition: str,
                  metrics: Dict[str, float],
                  config: Dict[str, Any],
                  interaction_data: Optional[Dict] = None):
        """
        Log a single trial with all data
        
        Args:
            trial_id: Unique trial identifier
            condition: Experimental condition
            metrics: Consciousness metrics
            config: System configuration
            interaction_data: Interaction details
        """
        trial_data = {
            'trial_id': trial_id,
            'condition': condition,
            'timestamp': time.time(),
            'metrics': metrics,
            'config': config,
            'interaction': interaction_data or {}
        }
        
        # Append to trial log
        log_file = os.path.join(self.experiment_dir, 'trials.jsonl')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(trial_data) + '\n')
    
    def export_dataset(self, format: str = 'csv'):
        """
        Export collected dataset in specified format
        
        Args:
            format: Output format ('csv', 'json', 'pandas')
        """
        log_file = os.path.join(self.experiment_dir, 'trials.jsonl')
        
        if not os.path.exists(log_file):
            print("No trial data to export.")
            return
        
        # Read all trials
        trials = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                trials.append(json.loads(line))
        
        if format == 'csv':
            output_file = os.path.join(self.experiment_dir, 'dataset.csv')
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if trials:
                    fieldnames = ['trial_id', 'condition', 'timestamp'] + list(trials[0]['metrics'].keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for trial in trials:
                        row = {
                            'trial_id': trial['trial_id'],
                            'condition': trial['condition'],
                            'timestamp': trial['timestamp']
                        }
                        row.update(trial['metrics'])
                        writer.writerow(row)
            
            print(f"✓ Exported {len(trials)} trials to {output_file}")
        
        elif format == 'json':
            output_file = os.path.join(self.experiment_dir, 'dataset.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(trials, f, indent=2)
            print(f"✓ Exported {len(trials)} trials to {output_file}")
        
        elif format == 'pandas':
            try:
                import pandas as pd
                # Flatten metrics into columns
                data = []
                for trial in trials:
                    row = {
                        'trial_id': trial['trial_id'],
                        'condition': trial['condition'],
                        'timestamp': trial['timestamp']
                    }
                    row.update(trial['metrics'])
                    data.append(row)
                
                df = pd.DataFrame(data)
                output_file = os.path.join(self.experiment_dir, 'dataset.pkl')
                df.to_pickle(output_file)
                print(f"✓ Exported {len(trials)} trials to pandas DataFrame: {output_file}")
                return df
            except ImportError:
                print("pandas not installed. Install with: pip install pandas")


# Convenience functions

def create_experiment_runner(simulator_factory, metrics_calculator) -> ExperimentRunner:
    """Create ExperimentRunner instance"""
    return ExperimentRunner(simulator_factory, metrics_calculator)


def create_experiment_logger(experiment_name: str, output_dir: str = 'results') -> ExperimentLogger:
    """Create ExperimentLogger instance"""
    return ExperimentLogger(experiment_name, output_dir)
