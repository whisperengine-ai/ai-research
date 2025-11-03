"""
Visualization and Analysis Tools
Helper functions for understanding consciousness metrics
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from typing import List, Dict
import numpy as np


def plot_neurochemical_timeline(conversation_history: List[Dict], save_path: str = "neurochemicals.png"):
    """
    Plot how neurochemical levels change over conversation
    
    Args:
        conversation_history: List of interaction dictionaries
        save_path: Where to save the plot
    """
    if not conversation_history:
        print("No conversation history to plot")
        return
    
    turns = [item['turn'] for item in conversation_history]
    
    chemicals = {
        'dopamine': [],
        'serotonin': [],
        'norepinephrine': [],
        'oxytocin': [],
        'cortisol': []
    }
    
    for item in conversation_history:
        neuro = item['neurochemicals']
        for chem in chemicals.keys():
            chemicals[chem].append(neuro[chem])
    
    plt.figure(figsize=(12, 6))
    
    for chem, values in chemicals.items():
        plt.plot(turns, values, marker='o', label=chem.capitalize(), linewidth=2)
    
    plt.xlabel('Conversation Turn', fontsize=12)
    plt.ylabel('Chemical Level', fontsize=12)
    plt.title('Neurochemical Dynamics Over Conversation', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✓ Saved neurochemical timeline to {save_path}")


def plot_emotional_journey(conversation_history: List[Dict], save_path: str = "emotions.png"):
    """
    Visualize the emotional journey through conversation
    """
    if not conversation_history:
        return
    
    turns = [item['turn'] for item in conversation_history]
    emotions = [item['user_emotion'] for item in conversation_history]
    
    # Map emotions to numeric values for plotting
    emotion_map = {
        'joy': 1.0, 'happiness': 0.9,
        'neutral': 0.5,
        'surprise': 0.6,
        'fear': -0.5, 'anxiety': -0.6,
        'sadness': -0.7,
        'anger': -0.8,
        'disgust': -0.9
    }
    
    emotion_values = [emotion_map.get(e.lower(), 0) for e in emotions]
    
    plt.figure(figsize=(12, 5))
    
    colors = ['green' if v > 0.3 else 'red' if v < -0.3 else 'gray' for v in emotion_values]
    plt.bar(turns, emotion_values, color=colors, alpha=0.7)
    
    plt.xlabel('Conversation Turn', fontsize=12)
    plt.ylabel('Emotional Valence', fontsize=12)
    plt.title('Emotional Journey (User Emotions Detected)', fontsize=14, fontweight='bold')
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.ylim(-1, 1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✓ Saved emotional journey to {save_path}")


def plot_consciousness_metrics(conversation_history: List[Dict], save_path: str = "consciousness.png"):
    """
    Plot key consciousness indicators
    """
    if not conversation_history:
        return
    
    turns = [item['turn'] for item in conversation_history]
    self_refs = [item['self_references'] for item in conversation_history]
    attention_breadth = [item['attention_focus']['attention_breadth'] for item in conversation_history]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Self-reference frequency (meta-cognition indicator)
    ax1.plot(turns, self_refs, marker='o', color='purple', linewidth=2)
    ax1.set_ylabel('Self-References', fontsize=11)
    ax1.set_title('Meta-Cognitive Awareness (Self-Reference Count)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Attention breadth (complexity of thought)
    ax2.plot(turns, attention_breadth, marker='s', color='orange', linewidth=2)
    ax2.set_xlabel('Conversation Turn', fontsize=12)
    ax2.set_ylabel('Unique Concepts', fontsize=11)
    ax2.set_title('Cognitive Complexity (Attention Breadth)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✓ Saved consciousness metrics to {save_path}")


def generate_report(conversation_history: List[Dict]) -> str:
    """
    Generate comprehensive analysis report
    """
    if not conversation_history:
        return "No conversation data to analyze"
    
    report = "\n" + "="*70 + "\n"
    report += "CONSCIOUSNESS SIMULATION ANALYSIS REPORT\n"
    report += "="*70 + "\n\n"
    
    # Basic stats
    report += f"Total Interactions: {len(conversation_history)}\n\n"
    
    # Neurochemical summary
    report += "NEUROCHEMICAL PATTERNS:\n"
    report += "-" * 40 + "\n"
    
    all_neuro = [item['neurochemicals'] for item in conversation_history]
    for chem in ['dopamine', 'serotonin', 'norepinephrine', 'oxytocin', 'cortisol']:
        values = [n[chem] for n in all_neuro]
        avg = np.mean(values)
        std = np.std(values)
        min_val = np.min(values)
        max_val = np.max(values)
        
        report += f"  {chem.capitalize()}:\n"
        report += f"    Average: {avg:.3f} ± {std:.3f}\n"
        report += f"    Range: {min_val:.3f} to {max_val:.3f}\n"
    
    # Emotional patterns
    report += "\nEMOTIONAL PATTERNS:\n"
    report += "-" * 40 + "\n"
    
    emotions = [item['user_emotion'] for item in conversation_history]
    emotion_counts = {}
    for e in emotions:
        emotion_counts[e] = emotion_counts.get(e, 0) + 1
    
    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(emotions)) * 100
        report += f"  {emotion.capitalize()}: {count} ({pct:.1f}%)\n"
    
    # Meta-cognition analysis
    report += "\nMETA-COGNITION INDICATORS:\n"
    report += "-" * 40 + "\n"
    
    self_refs = [item['self_references'] for item in conversation_history]
    total_refs = sum(self_refs)
    avg_refs = np.mean(self_refs)
    
    report += f"  Total self-references: {total_refs}\n"
    report += f"  Average per turn: {avg_refs:.2f}\n"
    report += f"  Self-awareness level: {'High' if avg_refs > 2 else 'Moderate' if avg_refs > 1 else 'Low'}\n"
    
    # Attention analysis
    report += "\nATTENTION & COGNITIVE COMPLEXITY:\n"
    report += "-" * 40 + "\n"
    
    attention = [item['attention_focus']['attention_breadth'] for item in conversation_history]
    avg_attention = np.mean(attention)
    
    report += f"  Average attention breadth: {avg_attention:.1f} concepts\n"
    report += f"  Cognitive complexity: {'High' if avg_attention > 15 else 'Moderate' if avg_attention > 10 else 'Low'}\n"
    
    # Emergent patterns
    report += "\nEMERGENT PATTERNS:\n"
    report += "-" * 40 + "\n"
    
    # Check for emotional stability
    neuro_variance = np.mean([np.std([n[chem] for n in all_neuro]) for chem in ['dopamine', 'serotonin']])
    
    if neuro_variance < 0.1:
        report += "  ✓ Emotional stability: System shows homeostatic balance\n"
    elif neuro_variance < 0.2:
        report += "  ~ Emotional stability: Moderate fluctuations\n"
    else:
        report += "  ⚠ Emotional stability: High volatility detected\n"
    
    # Check for self-awareness trend
    if len(self_refs) > 3:
        early_refs = np.mean(self_refs[:len(self_refs)//2])
        late_refs = np.mean(self_refs[len(self_refs)//2:])
        if late_refs > early_refs * 1.2:
            report += "  ✓ Self-awareness: Increasing over time (learning)\n"
        else:
            report += "  ~ Self-awareness: Stable throughout conversation\n"
    
    report += "\n" + "="*70 + "\n"
    
    return report


def create_visualizations(conversation_history: List[Dict], output_dir: str = "."):
    """
    Create all visualization plots
    """
    try:
        import os
        
        plot_neurochemical_timeline(conversation_history, 
                                   os.path.join(output_dir, "neurochemicals.png"))
        plot_emotional_journey(conversation_history, 
                             os.path.join(output_dir, "emotions.png"))
        plot_consciousness_metrics(conversation_history, 
                                  os.path.join(output_dir, "consciousness.png"))
        
        print(f"\n✓ All visualizations saved to {output_dir}/")
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")


if __name__ == "__main__":
    print("Visualization tools loaded")
    print("Use these functions after running consciousness_chatbot.py")
    print("\nExample usage:")
    print("  from visualization import create_visualizations, generate_report")
    print("  report = generate_report(simulator.conversation_history)")
    print("  create_visualizations(simulator.conversation_history)")
