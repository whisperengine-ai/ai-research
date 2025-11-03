"""
Interaction Dynamics Analyzer
Tracks emotional resonance, stance alignment, engagement patterns, and trajectories
between user and bot without inferring user neurochemicals.

This module provides research-grade analysis of user-bot emotional interactions.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from collections import defaultdict


class InteractionDynamics:
    """
    Analyzes patterns in user-bot emotional interactions.
    
    Key metrics:
    - Emotional Resonance: How aligned are user and bot emotions?
    - Stance Alignment: Do they share perspectives (self vs other-focused)?
    - Engagement Trajectory: Is user engagement increasing or decreasing?
    - Emotional Trajectory: How is user emotion changing over conversation?
    - Response Quality: Is bot's response appropriate to user's state?
    """
    
    def __init__(self):
        """Initialize interaction tracker."""
        self.interactions: List[Dict] = []
        self.emotion_map = {
            'anger': 1, 'fear': 1, 'sadness': 2,
            'disgust': 1, 'surprise': 2, 'joy': 3,
            'neutral': 2
        }
    
    def add_interaction(self, 
                       turn: int,
                       user_emotion: str,
                       user_confidence: float,
                       user_stance: Dict,
                       bot_emotion: str,
                       bot_confidence: float,
                       user_linguistic: Dict,
                       bot_response: str) -> Dict:
        """
        Record a single turn interaction.
        
        Args:
            turn: Turn number
            user_emotion: User's detected emotion
            user_confidence: Confidence in user emotion detection
            user_stance: User's emotional stance analysis
            bot_emotion: Bot's autonomous emotion
            bot_confidence: Confidence in bot emotion detection
            user_linguistic: User's linguistic features
            bot_response: Bot's response text
            
        Returns:
            Dictionary with computed interaction metrics
        """
        
        # Compute resonance metrics
        resonance = self._compute_emotional_resonance(user_emotion, bot_emotion)
        alignment = self._compute_stance_alignment(user_stance)
        
        # Engagement metrics
        engagement = self._compute_engagement(user_linguistic, user_confidence)
        
        # Response appropriateness
        appropriateness = self._compute_response_appropriateness(
            user_emotion, bot_emotion, user_stance, bot_response
        )
        
        interaction = {
            'turn': turn,
            'user_emotion': user_emotion,
            'user_confidence': user_confidence,
            'user_stance': user_stance,
            'bot_emotion': bot_emotion,
            'bot_confidence': bot_confidence,
            'resonance': resonance,
            'stance_alignment': alignment,
            'engagement': engagement,
            'appropriateness': appropriateness,
            'user_linguistic_complexity': user_linguistic.get('complexity', 0),
            'response_length': len(bot_response.split()),
        }
        
        self.interactions.append(interaction)
        return interaction
    
    def _compute_emotional_resonance(self, user_emotion: str, bot_emotion: str) -> float:
        """
        Measure emotional resonance (0-1).
        
        1.0 = Perfect match (both angry, both joyful, etc.)
        0.5 = Neutral emotions or complement
        0.0 = Opposite emotions (one angry, one joyful)
        
        Args:
            user_emotion: User's detected emotion
            bot_emotion: Bot's emotion
            
        Returns:
            Resonance score 0-1
        """
        
        # Define emotional compatibility
        compatible_pairs = {
            ('anger', 'calm'): 0.7,      # Bot responds calmly to anger - good
            ('anger', 'neutral'): 0.8,   # Bot stays neutral to anger - appropriate
            ('anger', 'anger'): 0.3,     # Both angry - escalation, not helpful
            ('sadness', 'neutral'): 0.8, # Bot neutral to sadness - supportive
            ('sadness', 'fear'): 0.4,    # Bot's fear to user's sadness - unclear
            ('joy', 'joy'): 0.9,         # Both joyful - excellent resonance
            ('neutral', 'neutral'): 0.5, # Both neutral - stable, unremarkable
            ('fear', 'calm'): 0.85,      # Bot calm to user's fear - appropriate
            ('fear', 'fear'): 0.2,       # Both afraid - not helpful
        }
        
        # Normalize emotions for comparison
        user_norm = user_emotion.lower()
        bot_norm = bot_emotion.lower()
        
        # Handle similarity (same emotion)
        if user_norm == bot_norm:
            if user_norm in ['joy', 'neutral']:
                return 0.7  # Shared positive/neutral is good
            else:
                return 0.3  # Shared negative is not ideal
        
        # Check compatibility pairs
        pair = (user_norm, bot_norm)
        if pair in compatible_pairs:
            return compatible_pairs[pair]
        
        # Default: neutral emotions are mildly resonant
        if user_norm == 'neutral' or bot_norm == 'neutral':
            return 0.5
        
        # Different emotions that aren't paired
        return 0.4
    
    def _compute_stance_alignment(self, user_stance: Dict) -> float:
        """
        Measure stance alignment (0-1).
        
        1.0 = User is self-focused (DIRECT)
        0.5 = User is mixed (about self and others)
        0.0 = User is other-focused (ATTRIBUTED)
        
        Returns:
            Alignment score 0-1
        """
        
        self_focus = user_stance.get('self_focus', 0.5)
        emotion_type = user_stance.get('emotion_type', 'mixed')
        
        # User directly expressing their own emotions
        if emotion_type == 'direct':
            return 0.9
        # User mixed (self and others)
        elif emotion_type == 'mixed':
            return self_focus
        # User focused on others
        else:  # attributed
            return max(0.1, 1 - self_focus)
    
    def _compute_engagement(self, user_linguistic: Dict, confidence: float) -> float:
        """
        Measure user engagement (0-1).
        
        Based on:
        - Question asking (higher engagement)
        - Personal pronouns (self-reference = engagement)
        - Linguistic complexity
        - Confidence in emotion detection (clear emotions = more engaged)
        
        Args:
            user_linguistic: Linguistic analysis of user input
            confidence: Emotion detection confidence
            
        Returns:
            Engagement score 0-1
        """
        
        # Base: emotion confidence
        base_engagement = min(confidence, 1.0)
        
        # Boost for questions (seeking information)
        if user_linguistic.get('is_question', False):
            base_engagement = min(base_engagement + 0.15, 1.0)
        
        # Boost for self-references (active participation)
        self_refs = user_linguistic.get('personal_pronouns_count', 0)
        if self_refs > 0:
            base_engagement = min(base_engagement + 0.1 * min(self_refs, 3), 1.0)
        
        # Boost for complexity (thoughtful engagement)
        complexity = user_linguistic.get('complexity', 0)
        if complexity > 0.6:
            base_engagement = min(base_engagement + 0.1, 1.0)
        
        # Penalty for very low confidence
        if confidence < 0.4:
            base_engagement *= 0.7
        
        return base_engagement
    
    def _compute_response_appropriateness(self,
                                        user_emotion: str,
                                        bot_emotion: str,
                                        user_stance: Dict,
                                        bot_response: str) -> float:
        """
        Measure if bot's response is appropriate to user's state.
        
        Heuristics:
        - If user is self-focused, bot should acknowledge their feelings
        - If user asks question, response should be informative
        - Response length should match user input length
        - Bot should not mirror negative emotions (escalation)
        
        Args:
            user_emotion: User's emotion
            bot_emotion: Bot's emotion
            user_stance: User's stance
            bot_response: Bot's response text
            
        Returns:
            Appropriateness score 0-1
        """
        
        score = 0.5  # Start neutral
        
        # Check for inappropriate mirroring (escalation risk)
        if user_emotion == bot_emotion and user_emotion in ['anger', 'fear', 'sadness']:
            score -= 0.2  # Not good - escalating negative emotions
        
        # If user is asking for help (self-focused), bot should engage
        if user_stance.get('emotion_type') == 'direct':
            if len(bot_response) > 50:  # Substantive response
                score += 0.2
            if 'understand' in bot_response.lower() or 'help' in bot_response.lower():
                score += 0.15
        
        # Check response length appropriateness
        response_length = len(bot_response.split())
        if response_length < 5:
            score -= 0.1  # Too short
        elif response_length > 100:
            score -= 0.05  # Slightly too long
        else:
            score += 0.1  # Appropriate length
        
        # Ensure within bounds
        return min(max(score, 0.0), 1.0)
    
    def get_emotional_trajectory(self) -> Dict:
        """
        Analyze how user's emotional state changes over conversation.
        
        Returns:
            Dictionary with trajectory analysis
        """
        
        if len(self.interactions) < 2:
            return {'status': 'insufficient_data', 'turns': len(self.interactions)}
        
        # Map emotions to valence (positive, neutral, negative)
        emotion_valence = {
            'joy': 1.0, 'surprise': 0.5,
            'neutral': 0.0,
            'fear': -0.7, 'sadness': -0.8, 'anger': -0.9, 'disgust': -0.8
        }
        
        valences = [
            emotion_valence.get(interaction['user_emotion'].lower(), 0.0)
            for interaction in self.interactions
        ]
        
        # Calculate trajectory
        start_valence = valences[0]
        end_valence = valences[-1]
        trajectory = end_valence - start_valence
        
        # Calculate trend
        if len(valences) > 1:
            trend = np.polyfit(range(len(valences)), valences, 1)[0]
        else:
            trend = 0.0
        
        return {
            'status': 'success',
            'start_emotion': self.interactions[0]['user_emotion'],
            'start_valence': start_valence,
            'end_emotion': self.interactions[-1]['user_emotion'],
            'end_valence': end_valence,
            'trajectory': trajectory,
            'trend': trend,
            'direction': 'improving' if trajectory > 0.1 else 'declining' if trajectory < -0.1 else 'stable',
            'trend_direction': 'improving' if trend > 0.05 else 'declining' if trend < -0.05 else 'stable',
        }
    
    def get_engagement_trajectory(self) -> Dict:
        """
        Analyze how user engagement changes over conversation.
        
        Returns:
            Dictionary with engagement trajectory
        """
        
        if len(self.interactions) < 2:
            return {'status': 'insufficient_data', 'turns': len(self.interactions)}
        
        engagements = [interaction['engagement'] for interaction in self.interactions]
        
        start_engagement = engagements[0]
        end_engagement = engagements[-1]
        trajectory = end_engagement - start_engagement
        
        if len(engagements) > 1:
            trend = np.polyfit(range(len(engagements)), engagements, 1)[0]
            avg_engagement = np.mean(engagements)
        else:
            trend = 0.0
            avg_engagement = engagements[0]
        
        return {
            'status': 'success',
            'start_engagement': start_engagement,
            'end_engagement': end_engagement,
            'trajectory': trajectory,
            'trend': trend,
            'average_engagement': avg_engagement,
            'direction': 'increasing' if trajectory > 0.1 else 'decreasing' if trajectory < -0.1 else 'stable',
        }
    
    def get_resonance_analysis(self) -> Dict:
        """
        Analyze emotional resonance between user and bot.
        
        Returns:
            Dictionary with resonance metrics
        """
        
        if not self.interactions:
            return {'status': 'no_data'}
        
        resonances = [interaction['resonance'] for interaction in self.interactions]
        
        return {
            'status': 'success',
            'turns': len(self.interactions),
            'average_resonance': np.mean(resonances),
            'max_resonance': np.max(resonances),
            'min_resonance': np.min(resonances),
            'resonance_std': np.std(resonances),
            'high_resonance_turns': sum(1 for r in resonances if r >= 0.7),
            'low_resonance_turns': sum(1 for r in resonances if r <= 0.3),
            'resonance_trend': 'improving' if resonances[-1] > np.mean(resonances[:len(resonances)//2]) else 'declining',
        }
    
    def get_appropriateness_analysis(self) -> Dict:
        """
        Analyze response appropriateness over conversation.
        
        Returns:
            Dictionary with appropriateness metrics
        """
        
        if not self.interactions:
            return {'status': 'no_data'}
        
        appropriateness = [interaction['appropriateness'] for interaction in self.interactions]
        
        return {
            'status': 'success',
            'turns': len(self.interactions),
            'average_appropriateness': np.mean(appropriateness),
            'max_appropriateness': np.max(appropriateness),
            'min_appropriateness': np.min(appropriateness),
            'appropriate_turns': sum(1 for a in appropriateness if a >= 0.6),
            'inappropriate_turns': sum(1 for a in appropriateness if a <= 0.3),
        }
    
    def get_comprehensive_report(self) -> Dict:
        """
        Generate comprehensive interaction dynamics report.
        
        Returns:
            Dictionary with all analysis
        """
        
        return {
            'total_turns': len(self.interactions),
            'emotional_trajectory': self.get_emotional_trajectory(),
            'engagement_trajectory': self.get_engagement_trajectory(),
            'resonance_analysis': self.get_resonance_analysis(),
            'appropriateness_analysis': self.get_appropriateness_analysis(),
            'raw_interactions': self.interactions,
        }
    
    def get_summary(self) -> str:
        """
        Generate human-readable summary of interaction dynamics.
        
        Returns:
            Formatted string summary
        """
        
        report = self.get_comprehensive_report()
        
        summary = "=" * 80 + "\n"
        summary += "INTERACTION DYNAMICS ANALYSIS\n"
        summary += "=" * 80 + "\n\n"
        
        # Emotional trajectory
        et = report['emotional_trajectory']
        if et['status'] == 'success':
            summary += f"EMOTIONAL TRAJECTORY:\n"
            summary += f"  Start: {et['start_emotion'].upper()} ({et['start_valence']:.2f})\n"
            summary += f"  End:   {et['end_emotion'].upper()} ({et['end_valence']:.2f})\n"
            summary += f"  Direction: {et['direction'].upper()}\n"
            summary += f"  Overall change: {et['trajectory']:.2f}\n\n"
        
        # Engagement trajectory
        egt = report['engagement_trajectory']
        if egt['status'] == 'success':
            summary += f"ENGAGEMENT TRAJECTORY:\n"
            summary += f"  Average: {egt['average_engagement']:.1%}\n"
            summary += f"  Start: {egt['start_engagement']:.1%} → End: {egt['end_engagement']:.1%}\n"
            summary += f"  Direction: {egt['direction'].upper()}\n\n"
        
        # Resonance
        res = report['resonance_analysis']
        if res['status'] == 'success':
            summary += f"EMOTIONAL RESONANCE:\n"
            summary += f"  Average: {res['average_resonance']:.1%}\n"
            summary += f"  Range: {res['min_resonance']:.1%} - {res['max_resonance']:.1%}\n"
            summary += f"  High resonance turns: {res['high_resonance_turns']}\n"
            summary += f"  Low resonance turns: {res['low_resonance_turns']}\n\n"
        
        # Appropriateness
        app = report['appropriateness_analysis']
        if app['status'] == 'success':
            summary += f"RESPONSE APPROPRIATENESS:\n"
            summary += f"  Average: {app['average_appropriateness']:.1%}\n"
            summary += f"  Appropriate turns: {app['appropriate_turns']}/{report['total_turns']}\n"
            summary += f"  Inappropriate turns: {app['inappropriate_turns']}/{report['total_turns']}\n\n"
        
        summary += "=" * 80 + "\n"
        
        return summary
