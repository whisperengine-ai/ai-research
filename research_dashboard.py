"""
Research Dashboard - Real-time visualization of consciousness metrics
"""

import sys
# Remove local statistics.py from path to avoid name conflict
sys.path = [p for p in sys.path if not p.endswith('.')]

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Tuple


class ResearchDashboard:
    """Visualize consciousness simulator research data"""
    
    def __init__(self, style='darkgrid'):
        """Initialize dashboard with style"""
        sns.set_style(style)
        self.conversations = []
        self.fig = None
        
    def load_json(self, filepath: str):
        """Load conversation data from JSON"""
        with open(filepath) as f:
            data = json.load(f)
        self.conversations = data.get('conversations', [])
        return len(self.conversations)
    
    def plot_emotional_trajectories(self, output_file: str = None, max_conversations: int = 10) -> plt.Figure:
        """Plot emotional trajectories across conversations"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        emotion_valence = {
            'joy': 1.0, 'surprise': 0.5,
            'neutral': 0.0,
            'fear': -0.7, 'sadness': -0.8, 'anger': -0.9, 'disgust': -0.8
        }
        
        colors = plt.cm.tab20(np.linspace(0, 1, min(len(self.conversations), max_conversations)))
        
        for i, conv in enumerate(self.conversations[:max_conversations]):
            traj = conv['analysis']['emotional_trajectory']
            if traj.get('status') != 'success':
                continue
            
            # Get per-turn valences from interactions
            turns = len(conv['exchanges'])
            valences = []
            
            if 'raw_interactions' in traj:
                # Use raw data if available
                for interaction in traj['raw_interactions']:
                    emotion = interaction.get('user_emotion', 'neutral').lower()
                    valence = emotion_valence.get(emotion, 0.0)
                    valences.append(valence)
            else:
                # Interpolate between start and end
                start = traj.get('start_valence', 0)
                end = traj.get('end_valence', 0)
                valences = np.linspace(start, end, turns)
            
            ax.plot(range(1, len(valences) + 1), valences, 
                   marker='o', linewidth=2, label=conv['name'][:20], 
                   color=colors[i], alpha=0.7)
        
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.set_xlabel('Turn', fontsize=12, fontweight='bold')
        ax.set_ylabel('Valence (Emotional Positivity)', fontsize=12, fontweight='bold')
        ax.set_title('Emotional Trajectories Across Conversations', fontsize=14, fontweight='bold')
        ax.set_ylim(-1.2, 1.2)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        return fig
    
    def plot_resonance_heatmap(self, output_file: str = None) -> plt.Figure:
        """Heatmap of emotional resonance across turns and conversations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        resonance_data = []
        conv_names = []
        
        for conv in self.conversations:
            resonance = conv['analysis']['resonance_analysis']
            if resonance.get('status') == 'success' and 'resonance_per_turn' in resonance:
                resonance_data.append(resonance['resonance_per_turn'])
                conv_names.append(conv['name'][:15])
        
        if resonance_data:
            # Pad to same length
            max_len = max(len(r) for r in resonance_data)
            padded = []
            for r in resonance_data:
                if len(r) < max_len:
                    r = list(r) + [np.nan] * (max_len - len(r))
                padded.append(r)
            
            im = ax.imshow(padded, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
            ax.set_xlabel('Turn', fontsize=12, fontweight='bold')
            ax.set_ylabel('Conversation', fontsize=12, fontweight='bold')
            ax.set_title('Emotional Resonance Heatmap', fontsize=14, fontweight='bold')
            ax.set_yticklabels(conv_names, fontsize=9)
            
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Resonance (0-1)', fontsize=10)
        
        plt.tight_layout()
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        return fig
    
    def plot_metrics_comparison(self, output_file: str = None) -> plt.Figure:
        """Compare key metrics across conversations"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        improvements = []
        resonances = []
        engagements = []
        qualities = []
        conv_names = []
        
        for conv in self.conversations:
            analysis = conv['analysis']
            
            # Emotional improvement
            emotional = analysis['emotional_trajectory']
            if emotional.get('status') == 'success':
                improvements.append(emotional.get('trajectory', 0))
            
            # Resonance
            resonance = analysis['resonance_analysis']
            if resonance.get('status') == 'success':
                resonances.append(resonance.get('average_resonance', 0))
            
            # Engagement
            engagement = analysis['engagement_trajectory']
            if engagement.get('status') == 'success':
                engagements.append(engagement.get('average_engagement', 0))
            
            # Quality
            appropriateness = analysis['appropriateness_analysis']
            if appropriateness.get('status') == 'success':
                qualities.append(appropriateness.get('average_appropriateness', 0))
            
            conv_names.append(conv['name'][:20])
        
        x = np.arange(len(improvements))
        width = 0.2
        
        # Plot 1: Emotional Improvement
        colors = ['green' if i > 0.1 else 'orange' if i > -0.1 else 'red' for i in improvements]
        axes[0, 0].bar(x, improvements, color=colors, alpha=0.7)
        axes[0, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[0, 0].set_title('Emotional Improvement', fontweight='bold')
        axes[0, 0].set_ylabel('Improvement Score')
        axes[0, 0].set_ylim(-1.2, 1.2)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Resonance
        axes[0, 1].bar(x, resonances, color='steelblue', alpha=0.7)
        axes[0, 1].axhline(y=0.7, color='green', linestyle='--', alpha=0.5, label='Good (>70%)')
        axes[0, 1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='OK (>50%)')
        axes[0, 1].set_title('Emotional Resonance', fontweight='bold')
        axes[0, 1].set_ylabel('Resonance (0-1)')
        axes[0, 1].set_ylim(0, 1)
        axes[0, 1].legend(fontsize=8)
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Engagement
        axes[1, 0].bar(x, engagements, color='coral', alpha=0.7)
        axes[1, 0].set_title('Engagement Level', fontweight='bold')
        axes[1, 0].set_ylabel('Engagement (0-1)')
        axes[1, 0].set_ylim(0, 1)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Quality
        axes[1, 1].bar(x, qualities, color='mediumseagreen', alpha=0.7)
        axes[1, 1].axhline(y=0.75, color='green', linestyle='--', alpha=0.5, label='Good (>75%)')
        axes[1, 1].axhline(y=0.60, color='orange', linestyle='--', alpha=0.5, label='OK (>60%)')
        axes[1, 1].set_title('Response Quality', fontweight='bold')
        axes[1, 1].set_ylabel('Quality (0-1)')
        axes[1, 1].set_ylim(0, 1)
        axes[1, 1].legend(fontsize=8)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        for ax in axes.flat:
            ax.set_xticks(x)
            ax.set_xticklabels([f"C{i+1}" for i in range(len(improvements))], fontsize=8)
        
        plt.suptitle('Conversation Metrics Comparison', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        return fig
    
    def plot_correlation_matrix(self, output_file: str = None) -> plt.Figure:
        """Correlation matrix of all metrics"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        metrics_dict = {}
        
        for conv in self.conversations:
            analysis = conv['analysis']
            
            # Collect metrics
            if analysis['emotional_trajectory'].get('status') == 'success':
                metrics_dict.setdefault('Improvement', []).append(
                    analysis['emotional_trajectory'].get('trajectory', 0))
            
            if analysis['resonance_analysis'].get('status') == 'success':
                metrics_dict.setdefault('Resonance', []).append(
                    analysis['resonance_analysis'].get('average_resonance', 0))
            
            if analysis['engagement_trajectory'].get('status') == 'success':
                metrics_dict.setdefault('Engagement', []).append(
                    analysis['engagement_trajectory'].get('average_engagement', 0))
            
            if analysis['appropriateness_analysis'].get('status') == 'success':
                metrics_dict.setdefault('Quality', []).append(
                    analysis['appropriateness_analysis'].get('average_appropriateness', 0))
        
        # Pad to same length
        max_len = max(len(v) for v in metrics_dict.values()) if metrics_dict else 0
        for key in metrics_dict:
            while len(metrics_dict[key]) < max_len:
                metrics_dict[key].append(np.nan)
        
        if not metrics_dict:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        else:
            # Compute correlation matrix
            data = np.array([metrics_dict[k] for k in sorted(metrics_dict.keys())])
            corr = np.corrcoef(data)
            
            im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
            
            labels = sorted(metrics_dict.keys())
            ax.set_xticks(range(len(labels)))
            ax.set_yticks(range(len(labels)))
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
            
            # Add correlation values
            for i in range(len(labels)):
                for j in range(len(labels)):
                    text = ax.text(j, i, f'{corr[i, j]:.2f}',
                                  ha="center", va="center", color="black", fontsize=10)
            
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Correlation', fontsize=10)
            
            ax.set_title('Metric Correlations', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        return fig
    
    def plot_distribution(self, metric: str = 'improvement', output_file: str = None) -> plt.Figure:
        """Plot distribution of a metric"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        values = []
        for conv in self.conversations:
            analysis = conv['analysis']
            
            if metric.lower() == 'improvement':
                if analysis['emotional_trajectory'].get('status') == 'success':
                    values.append(analysis['emotional_trajectory'].get('trajectory', 0))
            elif metric.lower() == 'resonance':
                if analysis['resonance_analysis'].get('status') == 'success':
                    values.append(analysis['resonance_analysis'].get('average_resonance', 0))
            elif metric.lower() == 'engagement':
                if analysis['engagement_trajectory'].get('status') == 'success':
                    values.append(analysis['engagement_trajectory'].get('average_engagement', 0))
            elif metric.lower() == 'quality':
                if analysis['appropriateness_analysis'].get('status') == 'success':
                    values.append(analysis['appropriateness_analysis'].get('average_appropriateness', 0))
        
        if values:
            ax.hist(values, bins=10, color='steelblue', alpha=0.7, edgecolor='black')
            ax.axvline(np.mean(values), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(values):.2f}')
            ax.axvline(np.median(values), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(values):.2f}')
            ax.set_xlabel(metric.capitalize(), fontsize=12, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_title(f'{metric.capitalize()} Distribution', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
        else:
            ax.text(0.5, 0.5, f'No {metric} data available', ha='center', va='center')
        
        plt.tight_layout()
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        return fig
    
    def plot_all(self, output_dir: str = '.') -> Dict[str, str]:
        """Generate all plots and save to directory"""
        Path(output_dir).mkdir(exist_ok=True)
        
        outputs = {}
        
        # Trajectories
        fig = self.plot_emotional_trajectories(f'{output_dir}/trajectories.png')
        outputs['trajectories'] = f'{output_dir}/trajectories.png'
        plt.close(fig)
        
        # Resonance heatmap
        fig = self.plot_resonance_heatmap(f'{output_dir}/resonance_heatmap.png')
        outputs['resonance_heatmap'] = f'{output_dir}/resonance_heatmap.png'
        plt.close(fig)
        
        # Metrics comparison
        fig = self.plot_metrics_comparison(f'{output_dir}/metrics_comparison.png')
        outputs['metrics_comparison'] = f'{output_dir}/metrics_comparison.png'
        plt.close(fig)
        
        # Correlation matrix
        fig = self.plot_correlation_matrix(f'{output_dir}/correlations.png')
        outputs['correlations'] = f'{output_dir}/correlations.png'
        plt.close(fig)
        
        # Distributions
        for metric in ['improvement', 'resonance', 'engagement', 'quality']:
            fig = self.plot_distribution(metric, f'{output_dir}/dist_{metric}.png')
            outputs[f'dist_{metric}'] = f'{output_dir}/dist_{metric}.png'
            plt.close(fig)
        
        return outputs


def main():
    """Generate dashboard from conversation results"""
    dashboard = ResearchDashboard()
    
    # Load data
    num = dashboard.load_json('conversation_results_quick.json')
    print(f"Loaded {num} conversations")
    
    if num > 0:
        outputs = dashboard.plot_all('dashboard_output')
        print(f"\n✅ Generated {len(outputs)} visualizations:")
        for name, path in outputs.items():
            print(f"   {name}: {path}")
    else:
        print("No conversation data found")


if __name__ == '__main__':
    main()
