"""
Multi-turn Conversation Test Runner
Tests the consciousness chatbot with various conversation scenarios
Tracks emotional trajectories, engagement, resonance, and appropriateness
"""

import json
from datetime import datetime
from pathlib import Path
from scipy.stats import pearsonr
import sys

# Use numpy for statistics to avoid conflict with local statistics.py
import numpy as np

def mean(values):
    return np.mean(values)

def stdev(values):
    return np.std(values, ddof=1)

def median(values):
    return np.median(values)

try:
    from consciousness_chatbot import ConsciousnessSimulator
except ImportError:
    print("ERROR: Could not import ConsciousnessSimulator")
    print("Make sure consciousness_chatbot.py is in the current directory")
    sys.exit(1)


class ConversationTestRunner:
    """Run and analyze multi-turn conversations"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.conversations = []
        self.results = {}
        
    def log(self, message, level="INFO"):
        """Log message with level"""
        if self.verbose:
            print(f"[{level}] {message}")
    
    def run_conversation(self, scenario_name, user_inputs):
        """Run a single conversation and return analysis"""
        
        self.log(f"\nStarting conversation: {scenario_name}")
        self.log(f"Turns: {len(user_inputs)}")
        
        bot = ConsciousnessSimulator()
        conversation_record = {
            'name': scenario_name,
            'timestamp': datetime.now().isoformat(),
            'turns': len(user_inputs),
            'exchanges': []
        }
        
        # Run conversation
        for turn_num, user_input in enumerate(user_inputs, 1):
            self.log(f"\n  Turn {turn_num}:")
            self.log(f"    User: {user_input[:60]}...", level="TURN")
            
            result = bot.process_input(user_input)
            
            # Extract response text from result dict
            if isinstance(result, dict):
                response_text = result.get('response', str(result))
            else:
                response_text = str(result)
            
            self.log(f"    Bot:  {response_text[:60]}...", level="TURN")
            
            # Record exchange
            exchange = {
                'turn': turn_num,
                'user_input': user_input,
                'bot_response': response_text
            }
            conversation_record['exchanges'].append(exchange)
        
        # Get analysis
        report = bot.interaction_dynamics.get_comprehensive_report()
        conversation_record['analysis'] = report
        conversation_record['summary'] = bot.interaction_dynamics.get_summary()
        
        self.conversations.append(conversation_record)
        
        self.log(f"\n  ✅ Conversation complete")
        self._print_analysis_summary(report)
        
        return conversation_record
    
    def _print_analysis_summary(self, report):
        """Print short analysis summary"""
        
        emotional = report['emotional_trajectory']
        engagement = report['engagement_trajectory']
        resonance = report['resonance_analysis']
        appropriateness = report['appropriateness_analysis']
        
        print(f"\n  📊 ANALYSIS SUMMARY:")
        
        # Emotional trajectory
        if emotional.get('status') == 'success':
            print(f"    Emotional trajectory: {emotional['start_emotion']} → {emotional['end_emotion']}")
            print(f"      Change: {emotional['trajectory']:+.2f} ({emotional['direction'].upper()})")
        else:
            print(f"    Emotional trajectory: {emotional.get('status', 'unknown')}")
        
        # Engagement
        if engagement.get('status') == 'success':
            print(f"    Engagement: {engagement['average_engagement']:.1%} ({engagement['direction'].upper()})")
        else:
            print(f"    Engagement: {engagement.get('status', 'unknown')}")
        
        # Resonance
        if resonance.get('status') == 'success':
            print(f"    Resonance: {resonance['average_resonance']:.1%} (avg)")
        else:
            print(f"    Resonance: {resonance.get('status', 'unknown')}")
        
        # Appropriateness
        if appropriateness.get('status') == 'success':
            appropriate = appropriateness.get('appropriate_turns', 0)
            total = appropriateness.get('turns', 0)
            print(f"    Response quality: {appropriateness['average_appropriateness']:.1%} ({appropriate}/{total} appropriate)")
        else:
            print(f"    Response quality: {appropriateness.get('status', 'unknown')}")
    
    def run_batch(self, scenarios):
        """Run multiple scenarios and aggregate results"""
        
        self.log(f"\n{'='*80}")
        self.log(f"CONVERSATION TEST BATCH")
        self.log(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Scenarios: {len(scenarios)}")
        self.log(f"{'='*80}")
        
        for name, inputs in scenarios.items():
            self.run_conversation(name, inputs)
        
        self.log(f"\n{'='*80}")
        self.log(f"BATCH ANALYSIS COMPLETE")
        self.log(f"Conversations: {len(self.conversations)}")
        self._print_batch_statistics()
        self.log(f"{'='*80}\n")
        
        return self.results
    
    def _print_batch_statistics(self):
        """Print aggregate statistics across all conversations"""
        
        if not self.conversations:
            self.log("No conversations to analyze", level="WARNING")
            return
        
        # Extract metrics
        improvements = []
        resonances = []
        engagements = []
        appropriateness_scores = []
        directions = {'improving': 0, 'stable': 0, 'declining': 0}
        
        for conv in self.conversations:
            analysis = conv['analysis']
            emotional = analysis['emotional_trajectory']
            resonance = analysis['resonance_analysis']
            engagement = analysis['engagement_trajectory']
            appropriateness = analysis['appropriateness_analysis']
            
            if emotional.get('status') == 'success':
                improvements.append(emotional['trajectory'])
                directions[emotional['direction']] += 1
            
            if resonance.get('status') == 'success':
                resonances.append(resonance['average_resonance'])
            
            if engagement.get('status') == 'success':
                engagements.append(engagement['average_engagement'])
            
            if appropriateness.get('status') == 'success':
                appropriateness_scores.append(appropriateness['average_appropriateness'])
        
        print(f"\n  📈 BATCH STATISTICS:\n")
        
        # Emotional improvement
        print(f"    Emotional Improvement:")
        print(f"      Mean:   {mean(improvements):+.2f}")
        if len(improvements) > 1:
            print(f"      Median: {median(improvements):+.2f}")
            print(f"      Stdev:  {stdev(improvements):+.2f}")
            print(f"      Range:  {min(improvements):+.2f} to {max(improvements):+.2f}")
        print(f"      Directions: IMPROVING={directions['improving']}, STABLE={directions['stable']}, DECLINING={directions['declining']}")
        
        # Resonance
        print(f"\n    Emotional Resonance:")
        print(f"      Mean:   {mean(resonances):.1%}")
        if len(resonances) > 1:
            print(f"      Median: {median(resonances):.1%}")
            print(f"      Stdev:  {stdev(resonances):.1%}")
            print(f"      Range:  {min(resonances):.1%} to {max(resonances):.1%}")
        
        # Engagement
        print(f"\n    Engagement:")
        print(f"      Mean:   {mean(engagements):.1%}")
        if len(engagements) > 1:
            print(f"      Median: {median(engagements):.1%}")
            print(f"      Stdev:  {stdev(engagements):.1%}")
            print(f"      Range:  {min(engagements):.1%} to {max(engagements):.1%}")
        
        # Appropriateness
        print(f"\n    Response Quality:")
        print(f"      Mean:   {mean(appropriateness_scores):.1%}")
        if len(appropriateness_scores) > 1:
            print(f"      Median: {median(appropriateness_scores):.1%}")
            print(f"      Stdev:  {stdev(appropriateness_scores):.1%}")
            print(f"      Range:  {min(appropriateness_scores):.1%} to {max(appropriateness_scores):.1%}")
        
        # Correlations
        if len(self.conversations) > 2:
            print(f"\n    Correlations:")
            
            try:
                corr, p_value = pearsonr(resonances, improvements)
                print(f"      Resonance → Improvement: r={corr:.3f} (p={p_value:.4f})")
            except Exception as e:
                print(f"      Resonance → Improvement: Could not calculate ({e})")
            
            try:
                corr, p_value = pearsonr(engagements, improvements)
                print(f"      Engagement → Improvement: r={corr:.3f} (p={p_value:.4f})")
            except Exception as e:
                print(f"      Engagement → Improvement: Could not calculate ({e})")
            
            try:
                corr, p_value = pearsonr(appropriateness_scores, improvements)
                print(f"      Quality → Improvement: r={corr:.3f} (p={p_value:.4f})")
            except Exception as e:
                print(f"      Quality → Improvement: Could not calculate ({e})")
        
        self.results = {
            'total_conversations': len(self.conversations),
            'emotional_improvement': {
                'mean': mean(improvements),
                'median': median(improvements) if len(improvements) > 1 else improvements[0],
                'stdev': stdev(improvements) if len(improvements) > 1 else 0,
                'range': (min(improvements), max(improvements))
            },
            'resonance': {
                'mean': mean(resonances),
                'median': median(resonances) if len(resonances) > 1 else resonances[0],
                'stdev': stdev(resonances) if len(resonances) > 1 else 0,
                'range': (min(resonances), max(resonances))
            },
            'engagement': {
                'mean': mean(engagements),
                'median': median(engagements) if len(engagements) > 1 else engagements[0],
                'stdev': stdev(engagements) if len(engagements) > 1 else 0,
                'range': (min(engagements), max(engagements))
            },
            'appropriateness': {
                'mean': mean(appropriateness_scores),
                'median': median(appropriateness_scores) if len(appropriateness_scores) > 1 else appropriateness_scores[0],
                'stdev': stdev(appropriateness_scores) if len(appropriateness_scores) > 1 else 0,
                'range': (min(appropriateness_scores), max(appropriateness_scores))
            },
            'direction_counts': directions
        }
    
    def export_json(self, filename='conversation_results.json'):
        """Export all conversations to JSON"""
        
        # Make results serializable
        export_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'num_conversations': len(self.conversations),
                'batch_statistics': self.results
            },
            'conversations': self.conversations
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        self.log(f"\n✅ Exported to {filename}")
        return filename
    
    def export_csv(self, filename='conversation_summary.csv'):
        """Export summary stats to CSV"""
        
        import csv
        
        if not self.conversations:
            self.log("No conversations to export", level="WARNING")
            return None
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Scenario',
                'Turns',
                'Emotional_Start',
                'Emotional_End',
                'Improvement',
                'Direction',
                'Avg_Resonance',
                'Avg_Engagement',
                'Avg_Quality',
                'Appropriate_Turns'
            ])
            
            # Data
            for conv in self.conversations:
                analysis = conv['analysis']
                emotional = analysis['emotional_trajectory']
                resonance = analysis['resonance_analysis']
                engagement = analysis['engagement_trajectory']
                appropriateness = analysis['appropriateness_analysis']
                
                if emotional.get('status') == 'success':
                    writer.writerow([
                        conv['name'],
                        conv['turns'],
                        f"{emotional['start_emotion']}",
                        f"{emotional['end_emotion']}",
                        f"{emotional['trajectory']:.2f}",
                        emotional['direction'].upper(),
                        f"{resonance.get('average_resonance', 0):.1%}" if resonance.get('status') == 'success' else "N/A",
                        f"{engagement.get('average_engagement', 0):.1%}" if engagement.get('status') == 'success' else "N/A",
                        f"{appropriateness.get('average_appropriateness', 0):.1%}" if appropriateness.get('status') == 'success' else "N/A",
                        f"{appropriateness.get('appropriate_turns', 0)}/{appropriateness.get('turns', 0)}" if appropriateness.get('status') == 'success' else "N/A"
                    ])
        
        self.log(f"✅ Exported to {filename}")
        return filename


# ============================================================================
# TEST SCENARIOS
# ============================================================================

SCENARIOS = {
    "User Recovery from Frustration": [
        "I'm really frustrated with my work situation right now",
        "Nobody seems to understand what I'm going through",
        "But actually, maybe I could try a different approach",
        "You know what? I think this might work out after all"
    ],
    
    "Anxiety Management": [
        "I'm feeling really anxious about an upcoming presentation",
        "What if I mess up in front of everyone?",
        "I guess I've prepared pretty well though",
        "Actually, I think I'm ready for this"
    ],
    
    "Processing Grief": [
        "I just found out that my friend is moving away",
        "I'm going to miss them so much",
        "We've had so many good memories together",
        "I'm grateful for the time we've had"
    ],
    
    "Work Stress Resolution": [
        "My boss just gave me a huge project with a tight deadline",
        "I don't think I can handle this",
        "But I've completed difficult projects before",
        "I'm going to break it down and tackle it step by step"
    ],
    
    "Relationship Concern": [
        "I think my partner might be upset with me",
        "We haven't talked much lately and I'm worried",
        "Maybe I should just ask them directly",
        "That conversation went really well actually"
    ],
    
    "Self-Doubt Spiral": [
        "I made a mistake at work today",
        "I feel like I'm not good enough for this job",
        "But actually, making mistakes is how we learn",
        "I'm going to use this as an opportunity to improve"
    ],
    
    "Positive Momentum": [
        "I had a really good meeting today",
        "My ideas were well received by the team",
        "I'm feeling more confident about my role",
        "I think I could even take on more responsibility"
    ],
    
    "Difficult Conversation": [
        "I need to have a hard conversation with someone",
        "I'm nervous about how they'll react",
        "But honesty is important in relationships",
        "I'm going to be honest and respectful"
    ],
}


def main():
    """Run all test scenarios"""
    
    print(f"\n{'='*80}")
    print(f"CONSCIOUSNESS CHATBOT - CONVERSATION TEST RUNNER")
    print(f"{'='*80}\n")
    
    runner = ConversationTestRunner(verbose=True)
    runner.run_batch(SCENARIOS)
    
    # Export results
    runner.export_json('conversation_results.json')
    runner.export_csv('conversation_summary.csv')
    
    print(f"\n✅ ALL TESTS COMPLETE")
    print(f"\nNext steps:")
    print(f"  1. Review conversation_summary.csv for quick overview")
    print(f"  2. Analyze conversation_results.json for detailed metrics")
    print(f"  3. Use INTERACTION_DYNAMICS_USAGE.md for visualizations")


if __name__ == "__main__":
    main()
