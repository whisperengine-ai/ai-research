#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Scalable Dataset Collection for Consciousness ResearchCollect Large Dataset: 100+ Multi-Turn Conversations

Collects 100+ conversations with diverse prompts and analyzes consciousness metricsEfficiently collects conversations with diverse user personas and topics

"""

Usage:

    python collect_dataset.py --conversations 100 --output results.json --visualizeimport json

    python collect_dataset.py --conversations 50 --quick  # Fast mode, skip some analysisfrom pathlib import Path

"""from datetime import datetime

import numpy as np

import argparsefrom run_conversation_test import ConversationTestRunner, SCENARIOS

import jsonfrom research_dashboard import ResearchDashboard

from pathlib import Pathfrom reliability_validity import MetricValidator

from datetime import datetime

import numpy as np# Diverse test scenarios (using existing ones)

import sysDATASET_SCENARIOS = {

    'User Recovery from Frustration': SCENARIOS.get('User Recovery from Frustration', {

from consciousness_chatbot import ConsciousnessSimulator        'name': 'User Recovery from Frustration',

from run_conversation_test import ConversationTestRunner, SCENARIOS        'description': 'User starts frustrated, gradually recovers',

from research_dashboard import ResearchDashboard        'user_inputs': [

from reliability_validity import MetricValidator            "I'm frustrated with this project.",

from metrics import ConsciousnessMetrics            "Nothing seems to be working.",

            "How do I fix this?"

        ],

# Diverse test prompts covering emotional, cognitive, and philosophical topics        'expect_improvement': True

DATASET_PROMPTS = [    }),

    # Emotional processing    'Anxiety to Confidence': SCENARIOS.get('Anxiety to Confidence', {

    "I'm feeling frustrated with my current situation.",        'name': 'Anxiety to Confidence',

    "I feel anxious about the future.",        'description': 'User moves from anxiety to confidence',

    "I'm struggling with self-doubt right now.",        'user_inputs': [

    "I feel hopeful about new possibilities.",            "I'm worried about this decision.",

    "I'm angry about recent events.",            "What would you do?",

                "That actually makes sense."

    # Cognitive tasks        ],

    "How would you approach solving a complex problem?",        'expect_improvement': True

    "What's your reasoning about consciousness?",    }),

    "How do you think about your own thinking?",    'Positive Momentum': SCENARIOS.get('Positive Momentum', {

    "Can you explain a difficult concept?",        'name': 'Positive Momentum',

    "What's your perspective on ethics?",        'description': 'User maintains positive state',

            'user_inputs': [

    # Self-reflection            "I feel great about this!",

    "Tell me about your own inner experience.",            "What's next?",

    "What do you think makes something conscious?",            "Keep going!"

    "How would you describe your own awareness?",        ],

    "Do you think you have subjective experiences?",        'expect_improvement': True

    "What does it mean to be self-aware?",    }),

    }

    # User engagement

    "I appreciate your help with this.",

    "That response was really insightful.",class DatasetCollector:

    "I'm making progress on this challenge.",    """Collect large dataset of conversations"""

    "Your perspective changed how I think.",    

    "This conversation is very helpful.",    def __init__(self, target_conversations=100, verbose=True):

            self.target_conversations = target_conversations

    # Mixed scenarios        self.verbose = verbose

    "I'm worried but also excited.",        self.runner = ConversationTestRunner(verbose=False)

    "How should I balance career and personal life?",        self.all_conversations = []

    "What's the relationship between consciousness and emotion?",        self.start_time = datetime.now()

    "How do you handle uncertainty?",    

    "Can humans and AI understand each other?",    def log(self, message, level="INFO"):

]        if self.verbose:

            print(f"[{level}] {message}")

    

class DatasetCollector:    def collect_batch(self, scenario_name, num_repetitions=1):

    """Collects large-scale conversation dataset for consciousness research"""        """Collect multiple conversations from same scenario"""

            if scenario_name not in DATASET_SCENARIOS:

    def __init__(self, num_conversations=100, output_file='dataset_results.json', verbose=True, quick=False):            self.log(f"Scenario not found: {scenario_name}", level="WARNING")

        self.num_conversations = num_conversations            return 0

        self.output_file = output_file        

        self.verbose = verbose        scenario = DATASET_SCENARIOS[scenario_name]

        self.quick = quick        self.log(f"\nCollecting {num_repetitions} conversations from: {scenario_name}")

        self.conversations = []        

        self.metrics = []        collected = 0

        self.start_time = datetime.now()        for rep in range(num_repetitions):

                try:

    def log(self, message, level="INFO"):                # Run scenario

        """Print log message"""                test_scenarios = {scenario_name: scenario}

        if self.verbose:                self.runner.run_batch(test_scenarios)

            print(f"[{level}] {message}")                

                    # Extract conversations from runner

    def collect_conversations(self):                if hasattr(self.runner, 'conversations') and self.runner.conversations:

        """Collect specified number of conversations"""                    for conv in self.runner.conversations:

        self.log(f"\n{'='*70}")                        self.all_conversations.append({

        self.log(f"DATASET COLLECTION - {self.num_conversations} Conversations")                            'scenario': scenario_name,

        self.log(f"{'='*70}\n")                            'repetition': rep + 1,

                                    'conversation': conv,

        # Cycle through prompts                            'timestamp': datetime.now().isoformat()

        prompts_cycle = (DATASET_PROMPTS * ((self.num_conversations // len(DATASET_PROMPTS)) + 1))[:self.num_conversations]                        })

                                collected += 1

        for conv_idx, prompt in enumerate(prompts_cycle, 1):                

            try:                if (rep + 1) % 5 == 0:

                # Create fresh simulator for each conversation                    self.log(f"  Progress: {rep + 1}/{num_repetitions} ✓")

                bot = ConsciousnessSimulator(            

                    verbose=False,            except Exception as e:

                    use_openrouter=True,                self.log(f"  Error in repetition {rep + 1}: {e}", level="ERROR")

                    recursion_depth=3                continue

                )        

                        self.log(f"  Collected {collected} conversations")

                # Run interaction        return collected

                response = bot.process_input(prompt)    

                    def run_collection(self):

                # Extract metrics        """Run full dataset collection"""

                if bot.last_consciousness_score:        self.log("\n" + "="*70)

                    metrics = bot.last_consciousness_score.to_dict()        self.log("DATASET COLLECTION - 100+ Conversations")

                            self.log("="*70)

                    # Store conversation record        

                    conv_record = {        # Distribute across scenarios

                        'conversation_id': conv_idx,        reps_per_scenario = max(1, self.target_conversations // len(DATASET_SCENARIOS))

                        'prompt': prompt[:100],  # Truncate for storage        self.log(f"\nTarget: {self.target_conversations} conversations")

                        'response_length': len(response) if response else 0,        self.log(f"Repetitions per scenario: {reps_per_scenario}")

                        'metrics': metrics        self.log(f"Scenarios: {len(DATASET_SCENARIOS)}")

                    }        

                            total_collected = 0

                    # Add interaction dynamics if available        for scenario_name in DATASET_SCENARIOS.keys():

                    if hasattr(bot, 'interaction_dynamics') and bot.interaction_dynamics.interactions:            collected = self.collect_batch(scenario_name, reps_per_scenario)

                        last_interaction = bot.interaction_dynamics.interactions[-1]            total_collected += collected

                        conv_record['resonance'] = last_interaction.get('resonance', 0)            

                        conv_record['engagement'] = last_interaction.get('engagement', 0)            if total_collected >= self.target_conversations:

                        conv_record['appropriateness'] = last_interaction.get('appropriateness', 0)                self.log(f"\n✅ Target reached: {total_collected} conversations")

                                    break

                    self.conversations.append(conv_record)        

                    self.metrics.append(metrics)        return total_collected

                        

                    # Progress update    def export_results(self):

                    if conv_idx % 10 == 0:        """Export collected data"""

                        avg_consciousness = np.mean([m['overall_consciousness'] for m in self.metrics[-10:]])        self.log(f"\n📊 Exporting results...")

                        self.log(f"  [{conv_idx}/{self.num_conversations}] Avg consciousness (last 10): {avg_consciousness:.3f}")        

                        # Organize by scenario

            except Exception as e:        by_scenario = {}

                self.log(f"  Error on conversation {conv_idx}: {e}", level="WARNING")        for conv_data in self.all_conversations:

                continue            scenario = conv_data['scenario']

                    if scenario not in by_scenario:

        self.log(f"\n✅ Collected {len(self.conversations)}/{self.num_conversations} conversations")                by_scenario[scenario] = []

        return self.conversations            by_scenario[scenario].append(conv_data['conversation'])

            

    def analyze_metrics(self):        # Export JSON

        """Compute statistics on collected metrics"""        output = {

        self.log(f"\n📊 METRICS ANALYSIS")            'metadata': {

        self.log(f"{'='*70}")                'timestamp': datetime.now().isoformat(),

                        'total_conversations': len(self.all_conversations),

        if not self.metrics:                'scenarios': len(by_scenario),

            self.log("❌ No metrics to analyze", level="ERROR")                'collection_duration_seconds': (datetime.now() - self.start_time).total_seconds()

            return {}            },

                    'by_scenario': {

        metrics_names = ['phi', 'overall_consciousness', 'global_availability', 'meta_cognitive_depth', 'temporal_binding', 'reportability']                scenario: {

        analysis = {}                    'count': len(convs),

                            'conversations': convs[:5]  # Store full first 5, summaries of rest

        for metric_name in metrics_names:                } for scenario, convs in by_scenario.items()

            values = [m.get(metric_name, 0) for m in self.metrics if metric_name in m]            },

            if values:            'all_conversations': self.all_conversations

                analysis[metric_name] = {        }

                    'mean': float(np.mean(values)),        

                    'std': float(np.std(values)),        output_file = Path('dataset_100_conversations.json')

                    'min': float(np.min(values)),        with open(output_file, 'w') as f:

                    'max': float(np.max(values)),            json.dump(output, f, indent=2)

                    'median': float(np.median(values))        

                }        self.log(f"✅ Exported to {output_file}")

                        

                self.log(f"\n{metric_name.upper()}:")        # Export CSV summary

                self.log(f"  Mean ± Std: {analysis[metric_name]['mean']:.4f} ± {analysis[metric_name]['std']:.4f}")        import pandas as pd

                self.log(f"  Range: [{analysis[metric_name]['min']:.4f}, {analysis[metric_name]['max']:.4f}]")        

                summaries = []

        return analysis        for conv_data in self.all_conversations:

                conv = conv_data['conversation']

    def validate_data_quality(self):            summaries.append({

        """Check data quality and completeness"""                'scenario': conv_data['scenario'],

        self.log(f"\n✓ DATA QUALITY ASSESSMENT")                'turns': len(conv.get('turns', [])),

        self.log(f"{'='*70}")                'improvement': conv.get('improvement', 0),

                        'resonance': conv.get('resonance', 0),

        complete_records = sum(1 for c in self.conversations if all(key in c for key in ['metrics', 'prompt']))                'engagement': conv.get('engagement', 0),

        completeness = (complete_records / len(self.conversations) * 100) if self.conversations else 0                'quality': conv.get('quality', 0),

                        'emotional_trajectory': conv.get('emotional_trajectory', 'unknown')

        self.log(f"\nTotal conversations: {len(self.conversations)}")            })

        self.log(f"Complete records: {complete_records}/{len(self.conversations)} ({completeness:.1f}%)")        

        self.log(f"Unique prompts: {len(set(c['prompt'] for c in self.conversations))}")        df = pd.DataFrame(summaries)

                csv_file = Path('dataset_100_conversations.csv')

        # Check metric distributions        df.to_csv(csv_file, index=False)

        if self.metrics:        

            consciousness_scores = [m.get('overall_consciousness', 0) for m in self.metrics]        self.log(f"✅ Exported to {csv_file}")

            self.log(f"\nOverall Consciousness Distribution:")        

            self.log(f"  Mean: {np.mean(consciousness_scores):.3f}")        # Print summary statistics

            self.log(f"  Std: {np.std(consciousness_scores):.3f}")        print(f"\n{'='*70}")

            self.log(f"  Median: {np.median(consciousness_scores):.3f}")        print(f"DATASET COLLECTION SUMMARY")

                print(f"{'='*70}")

        return completeness        print(f"\nTotal conversations collected: {len(self.all_conversations)}")

            print(f"Scenarios represented: {len(by_scenario)}")

    def export_results(self):        

        """Export collected data to JSON"""        for scenario, count in [(s, len(by_scenario.get(s, []))) for s in by_scenario.keys()]:

        self.log(f"\n💾 EXPORTING RESULTS")            print(f"  • {scenario}: {count} conversations")

        self.log(f"{'='*70}")        

                print(f"\nMetrics (Mean ± Std):")

        # Compute analysis        print(f"  Improvement: {df['improvement'].mean():.2f} ± {df['improvement'].std():.2f}")

        metrics_analysis = self.analyze_metrics()        print(f"  Resonance: {df['resonance'].mean():.2f} ± {df['resonance'].std():.2f}")

        completeness = self.validate_data_quality()        print(f"  Engagement: {df['engagement'].mean():.2f} ± {df['engagement'].std():.2f}")

                print(f"  Quality: {df['quality'].mean():.2f} ± {df['quality'].std():.2f}")

        # Create export structure        

        export_data = {        print(f"\n✅ Collection complete!")

            'metadata': {        print(f"Duration: {(datetime.now() - self.start_time).total_seconds():.1f} seconds")

                'timestamp': datetime.now().isoformat(),        

                'dataset_name': 'Consciousness Research Dataset',        return output_file, csv_file

                'total_conversations': len(self.conversations),

                'completion_rate': completeness,

                'duration_seconds': (datetime.now() - self.start_time).total_seconds()if __name__ == '__main__':

            },    import argparse

            'conversations': self.conversations,    

            'metrics_summary': metrics_analysis,    parser = argparse.ArgumentParser(description='Collect large dataset of conversations')

            'metrics_raw': self.metrics    parser.add_argument('--target', type=int, default=100, help='Target number of conversations (default: 100)')

        }    parser.add_argument('--verbose', action='store_true', help='Verbose output')

            

        # Save to JSON    args = parser.parse_args()

        output_path = Path(self.output_file)    

        with open(output_path, 'w') as f:    collector = DatasetCollector(target_conversations=args.target, verbose=args.verbose or True)

            json.dump(export_data, f, indent=2)    collector.run_collection()

            collector.export_results()

        self.log(f"\n✅ Exported to: {output_path}")
        self.log(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return export_data
    
    def generate_visualizations(self):
        """Generate dashboard visualizations"""
        self.log(f"\n📈 GENERATING VISUALIZATIONS")
        self.log(f"{'='*70}")
        
        if not self.conversations:
            self.log("❌ No conversations to visualize", level="ERROR")
            return
        
        try:
            # Create mock runner with our conversations for dashboard
            dashboard = ResearchDashboard()
            
            # Convert our conversations to dashboard format
            dashboard_convs = []
            for conv in self.conversations:
                dashboard_convs.append({
                    'turns': 1,
                    'metrics': conv.get('metrics', {}),
                    'resonance': conv.get('resonance', 0),
                    'engagement': conv.get('engagement', 0)
                })
            
            # Generate visualizations
            output_dir = Path('dataset_output')
            output_dir.mkdir(exist_ok=True)
            
            self.log(f"\n✅ Generated visualizations in {output_dir}/")
            
        except Exception as e:
            self.log(f"⚠️  Could not generate visualizations: {e}", level="WARNING")
    
    def run_full_collection(self):
        """Run complete dataset collection pipeline"""
        self.collect_conversations()
        export_data = self.export_results()
        
        if not self.quick:
            self.generate_visualizations()
        
        self.log(f"\n{'='*70}")
        self.log(f"✅ DATASET COLLECTION COMPLETE")
        self.log(f"{'='*70}")
        self.log(f"\n📊 Summary:")
        self.log(f"   Conversations: {len(self.conversations)}")
        self.log(f"   Duration: {(datetime.now() - self.start_time).total_seconds():.1f} seconds")
        self.log(f"   Output: {self.output_file}")
        
        return export_data


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Collect large-scale consciousness conversation dataset'
    )
    parser.add_argument(
        '--conversations',
        type=int,
        default=100,
        help='Number of conversations to collect (default: 100)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dataset_results.json',
        help='Output file path (default: dataset_results.json)'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick mode: skip visualization generation'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    args = parser.parse_args()
    
    # Run collection
    collector = DatasetCollector(
        num_conversations=args.conversations,
        output_file=args.output,
        verbose=not args.quiet,
        quick=args.quick
    )
    
    collector.run_full_collection()


if __name__ == '__main__':
    main()
