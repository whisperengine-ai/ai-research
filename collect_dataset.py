#!/usr/bin/env python3
"""
Collect Large Dataset: 100+ Multi-Turn Conversations
Efficiently collects conversations with diverse user personas and topics
"""

import json
from pathlib import Path
from datetime import datetime
import numpy as np
from run_conversation_test import ConversationTestRunner, SCENARIOS
from research_dashboard import ResearchDashboard
from reliability_validity import MetricValidator

# Diverse test scenarios (using existing ones)
DATASET_SCENARIOS = {
    'User Recovery from Frustration': SCENARIOS.get('User Recovery from Frustration', {
        'name': 'User Recovery from Frustration',
        'description': 'User starts frustrated, gradually recovers',
        'user_inputs': [
            "I'm frustrated with this project.",
            "Nothing seems to be working.",
            "How do I fix this?"
        ],
        'expect_improvement': True
    }),
    'Anxiety to Confidence': SCENARIOS.get('Anxiety to Confidence', {
        'name': 'Anxiety to Confidence',
        'description': 'User moves from anxiety to confidence',
        'user_inputs': [
            "I'm worried about this decision.",
            "What would you do?",
            "That actually makes sense."
        ],
        'expect_improvement': True
    }),
    'Positive Momentum': SCENARIOS.get('Positive Momentum', {
        'name': 'Positive Momentum',
        'description': 'User maintains positive state',
        'user_inputs': [
            "I feel great about this!",
            "What's next?",
            "Keep going!"
        ],
        'expect_improvement': True
    }),
}


class DatasetCollector:
    """Collect large dataset of conversations"""
    
    def __init__(self, target_conversations=100, verbose=True):
        self.target_conversations = target_conversations
        self.verbose = verbose
        self.runner = ConversationTestRunner(verbose=False)
        self.all_conversations = []
        self.start_time = datetime.now()
    
    def log(self, message, level="INFO"):
        if self.verbose:
            print(f"[{level}] {message}")
    
    def collect_batch(self, scenario_name, num_repetitions=1):
        """Collect multiple conversations from same scenario"""
        if scenario_name not in DATASET_SCENARIOS:
            self.log(f"Scenario not found: {scenario_name}", level="WARNING")
            return 0
        
        scenario = DATASET_SCENARIOS[scenario_name]
        self.log(f"\nCollecting {num_repetitions} conversations from: {scenario_name}")
        
        collected = 0
        for rep in range(num_repetitions):
            try:
                # Run scenario
                test_scenarios = {scenario_name: scenario}
                self.runner.run_batch(test_scenarios)
                
                # Extract conversations from runner
                if hasattr(self.runner, 'conversations') and self.runner.conversations:
                    for conv in self.runner.conversations:
                        self.all_conversations.append({
                            'scenario': scenario_name,
                            'repetition': rep + 1,
                            'conversation': conv,
                            'timestamp': datetime.now().isoformat()
                        })
                        collected += 1
                
                if (rep + 1) % 5 == 0:
                    self.log(f"  Progress: {rep + 1}/{num_repetitions} ✓")
            
            except Exception as e:
                self.log(f"  Error in repetition {rep + 1}: {e}", level="ERROR")
                continue
        
        self.log(f"  Collected {collected} conversations")
        return collected
    
    def run_collection(self):
        """Run full dataset collection"""
        self.log("\n" + "="*70)
        self.log("DATASET COLLECTION - 100+ Conversations")
        self.log("="*70)
        
        # Distribute across scenarios
        reps_per_scenario = max(1, self.target_conversations // len(DATASET_SCENARIOS))
        self.log(f"\nTarget: {self.target_conversations} conversations")
        self.log(f"Repetitions per scenario: {reps_per_scenario}")
        self.log(f"Scenarios: {len(DATASET_SCENARIOS)}")
        
        total_collected = 0
        for scenario_name in DATASET_SCENARIOS.keys():
            collected = self.collect_batch(scenario_name, reps_per_scenario)
            total_collected += collected
            
            if total_collected >= self.target_conversations:
                self.log(f"\n✅ Target reached: {total_collected} conversations")
                break
        
        return total_collected
    
    def export_results(self):
        """Export collected data"""
        self.log(f"\n📊 Exporting results...")
        
        # Organize by scenario
        by_scenario = {}
        for conv_data in self.all_conversations:
            scenario = conv_data['scenario']
            if scenario not in by_scenario:
                by_scenario[scenario] = []
            by_scenario[scenario].append(conv_data['conversation'])
        
        # Export JSON
        output = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_conversations': len(self.all_conversations),
                'scenarios': len(by_scenario),
                'collection_duration_seconds': (datetime.now() - self.start_time).total_seconds()
            },
            'by_scenario': {
                scenario: {
                    'count': len(convs),
                    'conversations': convs[:5]  # Store full first 5, summaries of rest
                } for scenario, convs in by_scenario.items()
            },
            'all_conversations': self.all_conversations
        }
        
        output_file = Path('dataset_100_conversations.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        self.log(f"✅ Exported to {output_file}")
        
        # Export CSV summary
        import pandas as pd
        
        summaries = []
        for conv_data in self.all_conversations:
            conv = conv_data['conversation']
            summaries.append({
                'scenario': conv_data['scenario'],
                'turns': len(conv.get('turns', [])),
                'improvement': conv.get('improvement', 0),
                'resonance': conv.get('resonance', 0),
                'engagement': conv.get('engagement', 0),
                'quality': conv.get('quality', 0),
                'emotional_trajectory': conv.get('emotional_trajectory', 'unknown')
            })
        
        df = pd.DataFrame(summaries)
        csv_file = Path('dataset_100_conversations.csv')
        df.to_csv(csv_file, index=False)
        
        self.log(f"✅ Exported to {csv_file}")
        
        # Print summary statistics
        print(f"\n{'='*70}")
        print(f"DATASET COLLECTION SUMMARY")
        print(f"{'='*70}")
        print(f"\nTotal conversations collected: {len(self.all_conversations)}")
        print(f"Scenarios represented: {len(by_scenario)}")
        
        for scenario, count in [(s, len(by_scenario.get(s, []))) for s in by_scenario.keys()]:
            print(f"  • {scenario}: {count} conversations")
        
        print(f"\nMetrics (Mean ± Std):")
        print(f"  Improvement: {df['improvement'].mean():.2f} ± {df['improvement'].std():.2f}")
        print(f"  Resonance: {df['resonance'].mean():.2f} ± {df['resonance'].std():.2f}")
        print(f"  Engagement: {df['engagement'].mean():.2f} ± {df['engagement'].std():.2f}")
        print(f"  Quality: {df['quality'].mean():.2f} ± {df['quality'].std():.2f}")
        
        print(f"\n✅ Collection complete!")
        print(f"Duration: {(datetime.now() - self.start_time).total_seconds():.1f} seconds")
        
        return output_file, csv_file


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect large dataset of conversations')
    parser.add_argument('--target', type=int, default=100, help='Target number of conversations (default: 100)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    collector = DatasetCollector(target_conversations=args.target, verbose=args.verbose or True)
    collector.run_collection()
    collector.export_results()
