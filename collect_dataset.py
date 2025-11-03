#!/usr/bin/env python3
"""Scalable Dataset Collection for Consciousness Research."""

import json
from pathlib import Path
from datetime import datetime
import numpy as np
import argparse
from collections import defaultdict
from consciousness_chatbot import ConsciousnessSimulator

DATASET_PROMPTS = [
    "I'm feeling frustrated with my current situation.",
    "I feel anxious about the future.",
    "How would you approach solving a complex problem?",
    "What's your reasoning about consciousness?",
    "Tell me about your own inner experience.",
    "Do you think you have subjective experiences?",
    "I appreciate your help with this.",
    "Can you explain a difficult concept?",
]

class DatasetCollector:
    """Collects diverse dataset for consciousness research."""
    
    def __init__(self, conversation_count=100, use_recursion_depth=3):
        self.conversation_count = conversation_count
        self.recursion_depth = use_recursion_depth
        self.conversations = []
        self.metrics_summary = defaultdict(list)
    
    def collect(self):
        """Collect conversations."""
        print(f"Collecting {self.conversation_count} conversations...")
        
        simulator = ConsciousnessSimulator(
            use_openrouter=True,
            recursion_depth=self.recursion_depth,
            verbose=False
        )
        
        for i in range(self.conversation_count):
            prompt_idx = i % len(DATASET_PROMPTS)
            user_input = DATASET_PROMPTS[prompt_idx]
            
            try:
                interaction = simulator.process_input(user_input)
                metrics = interaction.get('consciousness_metrics')
                if metrics:
                    self.conversations.append({
                        'conversation_id': i + 1,
                        'user_input': user_input[:100],
                        'metrics': metrics
                    })
                    for key, val in metrics.items():
                        if key != 'timestamp':
                            self.metrics_summary[key].append(val)
                    if (i + 1) % 10 == 0:
                        print(f"  ✓ {i + 1}/{self.conversation_count}")
            except Exception as e:
                print(f"  ⚠ Conversation {i + 1} failed: {e}")
                continue
        
        return self.conversations
    
    def save(self, output_file="dataset_results.json"):
        """Save collected data."""
        metrics_aggregated = {}
        for key, vals in self.metrics_summary.items():
            if vals:
                metrics_aggregated[key] = {
                    'mean': float(np.mean(vals)),
                    'std': float(np.std(vals)),
                }
        
        output_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_conversations': len(self.conversations),
                'recursion_depth': self.recursion_depth,
            },
            'conversations': self.conversations,
            'metrics_summary': metrics_aggregated
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Saved {len(self.conversations)} conversations to {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description='Collect diverse consciousness dataset')
    parser.add_argument('--count', type=int, default=100, help='Number of conversations')
    parser.add_argument('--depth', type=int, default=3, help='Recursion depth')
    parser.add_argument('--output', default='dataset_results.json', help='Output file')
    
    args = parser.parse_args()
    
    collector = DatasetCollector(conversation_count=args.count, use_recursion_depth=args.depth)
    collector.collect()
    collector.save(args.output)
    print("✅ Dataset collection complete!")

if __name__ == '__main__':
    main()
