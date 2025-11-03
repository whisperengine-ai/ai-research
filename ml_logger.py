"""
ML Logger for Meta-Cognition Pipeline
Logs conversation data for training quality prediction models
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from uuid import uuid4


class MLLogger:
    """
    Logs consciousness simulator interactions for ML training
    
    Purpose: Collect data to train models that predict response quality
             from meta-cognitive features
    """
    
    def __init__(self, log_dir='ml_logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.session_id = str(uuid4())[:8]
        self.current_log = []
    
    def log_turn(self,
                 user_input: str,
                 response: str,
                 meta_cognition: Dict,
                 metrics: Any,
                 dynamics: Any,
                 neurochemistry: Dict,
                 user_emotion: str | None = None,
                 user_emotion_confidence: float | None = None) -> None:
        """
        Log a single conversation turn with all relevant data
        
        Args:
            user_input: User's input text
            response: Bot's response
            meta_cognition: Recursive meta-cognition results
            metrics: Consciousness metrics
            dynamics: Interaction dynamics
            neurochemistry: Neurochemical state
            user_emotion: Detected user emotion
            user_emotion_confidence: Confidence of emotion detection
        """
        
        # Extract features from meta-cognition
        meta_features = self._extract_meta_features(meta_cognition)
        
        # Build log entry
        entry = {
            'turn_id': str(uuid4()),
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            
            # Input/Output
            'user_input': user_input,
            'user_input_length': len(user_input),
            'response': response,
            'response_length': len(response),
            
            # User context
            'user_emotion': user_emotion,
            'user_emotion_confidence': user_emotion_confidence,
            
            # Meta-cognition (raw)
            'meta_cognition_raw': {
                'reflections': meta_cognition.get('reflections', []),
                'num_reflections': len(meta_cognition.get('reflections', []))
            },
            
            # Meta-cognition (features)
            'meta_cognition_features': meta_features,
            
            # Bot state
            'neurochemistry': neurochemistry,
            
            # Outcomes (the training targets)
            'outcomes': {
                'consciousness_metrics': metrics.to_dict() if hasattr(metrics, 'to_dict') else {},
                'engagement_score': getattr(dynamics, 'engagement', None),
                'resonance_score': getattr(dynamics, 'resonance', None),
                'appropriateness_score': getattr(dynamics, 'appropriateness', None),
                
                # Placeholders for human evaluation (to be filled later)
                'human_quality_rating': None,  # 1-10 scale
                'user_satisfaction': None,      # 1-5 scale
                'conversation_continued': None  # True/False
            }
        }
        
        self.current_log.append(entry)
    
    def _extract_meta_features(self, meta_cognition: Dict) -> Dict[str, float]:
        """
        Extract ML features from meta-cognition reflections
        
        These features will be used to train the quality predictor
        """
        reflections = meta_cognition.get('reflections', [])
        
        if not reflections:
            return self._empty_features()
        
        features = {}
        
        # Structural features
        features['num_reflections'] = len(reflections)
        features['max_depth'] = max([r.get('level', 0) for r in reflections], default=0)
        features['avg_reflection_length'] = sum(len(r.get('content', '')) for r in reflections) / len(reflections)
        
        # Combine all reflection text
        all_text = ' '.join([r.get('content', '') for r in reflections]).lower()
        text_len = max(1, len(all_text))
        
        # Linguistic features
        features['self_ref_count'] = self._count_patterns(all_text, ['i ', 'my ', 'myself', "i'm", 'me '])
        features['self_ref_density'] = features['self_ref_count'] / text_len
        
        # Confidence indicators
        confidence_markers = self._count_patterns(all_text, 
            ['certain', 'confident', 'sure', 'definitely', 'clearly', 'appropriate', 'good'])
        uncertainty_markers = self._count_patterns(all_text,
            ['unsure', 'maybe', 'perhaps', 'might', 'possibly', 'uncertain'])
        
        features['confidence_markers'] = confidence_markers
        features['uncertainty_markers'] = uncertainty_markers
        features['confidence_ratio'] = confidence_markers / max(1, confidence_markers + uncertainty_markers)
        
        # Emotional awareness
        features['emotion_words'] = self._count_patterns(all_text,
            ['feel', 'feeling', 'emotion', 'sense', 'notice', 'aware', 'noticing'])
        features['emotional_awareness_density'] = features['emotion_words'] / text_len
        
        # Evaluation polarity
        positive = self._count_patterns(all_text,
            ['good', 'appropriate', 'helpful', 'supportive', 'effective', 'positive'])
        negative = self._count_patterns(all_text,
            ['inappropriate', 'unhelpful', 'wrong', 'poor', 'ineffective', 'negative'])
        
        features['positive_eval'] = positive
        features['negative_eval'] = negative
        features['eval_polarity'] = (positive - negative) / max(1, positive + negative)
        
        # Perspective-taking
        features['user_mentions'] = self._count_patterns(all_text,
            ['user', 'they', 'their', 'them', 'person', 'you '])
        features['perspective_taking_score'] = features['user_mentions'] / text_len
        
        return features
    
    def _count_patterns(self, text: str, patterns: List[str]) -> int:
        """Count occurrences of patterns in text"""
        return sum(text.count(pattern) for pattern in patterns)
    
    def _empty_features(self) -> Dict[str, float]:
        """Return empty feature dict when no reflections"""
        return {
            'num_reflections': 0,
            'max_depth': 0,
            'avg_reflection_length': 0,
            'self_ref_count': 0,
            'self_ref_density': 0,
            'confidence_markers': 0,
            'uncertainty_markers': 0,
            'confidence_ratio': 0.5,
            'emotion_words': 0,
            'emotional_awareness_density': 0,
            'positive_eval': 0,
            'negative_eval': 0,
            'eval_polarity': 0,
            'user_mentions': 0,
            'perspective_taking_score': 0
        }
    
    def save_session(self, filename: str | None = None) -> str:
        """
        Save logged data to JSON file
        
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"ml_log_{self.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.log_dir, filename)
        
        data = {
            'metadata': {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'num_turns': len(self.current_log),
                'format_version': '1.0'
            },
            'turns': self.current_log
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ ML training data saved to {filepath}")
        return filepath
    
    def add_human_ratings(self, turn_id: str, quality_rating: int, satisfaction: int):
        """
        Add human quality ratings to a logged turn
        
        Args:
            turn_id: ID of the turn to rate
            quality_rating: 1-10 scale
            satisfaction: 1-5 scale
        """
        for entry in self.current_log:
            if entry['turn_id'] == turn_id:
                entry['outcomes']['human_quality_rating'] = quality_rating
                entry['outcomes']['user_satisfaction'] = satisfaction
                break
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of logged data"""
        if not self.current_log:
            return {'num_turns': 0}
        
        return {
            'num_turns': len(self.current_log),
            'avg_input_length': sum(e['user_input_length'] for e in self.current_log) / len(self.current_log),
            'avg_response_length': sum(e['response_length'] for e in self.current_log) / len(self.current_log),
            'avg_num_reflections': sum(e['meta_cognition_raw']['num_reflections'] for e in self.current_log) / len(self.current_log),
            'emotions_detected': set(e['user_emotion'] for e in self.current_log if e['user_emotion'])
        }


# Example usage
if __name__ == "__main__":
    print("ML Logger Test\n")
    
    # Initialize logger
    logger = MLLogger(log_dir='ml_logs')
    
    # Simulate a conversation turn
    from dataclasses import dataclass
    
    @dataclass
    class MockMetrics:
        meta_cognitive_depth: float = 0.8
        phi: float = 0.43
        overall_consciousness: float = 0.68
        
        def to_dict(self):
            return {
                'meta_cognitive_depth': self.meta_cognitive_depth,
                'phi': self.phi,
                'overall_consciousness': self.overall_consciousness
            }
    
    @dataclass
    class MockDynamics:
        engagement: float = 0.85
        resonance: float = 0.72
        appropriateness: float = 0.80
    
    # Log a turn
    logger.log_turn(
        user_input="I'm worried about this project.",
        response="I understand your concern. Let me help you break this down into manageable steps.",
        meta_cognition={
            'reflections': [
                {'level': 0, 'content': 'Response about helping with project', 'type': 'response'},
                {'level': 1, 'content': "I'm noticing empathy in my response to their worry", 'type': 'observation'},
                {'level': 2, 'content': 'This feels appropriate for their emotional state', 'type': 'evaluation'}
            ]
        },
        metrics=MockMetrics(),
        dynamics=MockDynamics(),
        neurochemistry={'dopamine': 0.6, 'serotonin': 0.7, 'cortisol': 0.3},
        user_emotion='fear',
        user_emotion_confidence=0.78
    )
    
    # Show summary
    print("Summary:", logger.get_summary_stats())
    
    # Save
    filepath = logger.save_session()
    print(f"\nTest log saved to: {filepath}")
