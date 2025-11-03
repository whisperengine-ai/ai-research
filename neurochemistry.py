"""
Neurochemical Emotion System
Models 5 key brain chemicals that modulate AI behavior and responses
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ChemicalLevels:
    """Tracks levels of 5 key neurochemicals (0.0 to 1.0 scale)"""
    dopamine: float = 0.5       # Motivation, reward, learning
    serotonin: float = 0.5      # Mood stability, well-being
    norepinephrine: float = 0.5 # Alertness, arousal, stress
    oxytocin: float = 0.5       # Social bonding, empathy
    cortisol: float = 0.3       # Stress response, anxiety
    
    def to_dict(self) -> Dict[str, float]:
        return {
            'dopamine': self.dopamine,
            'serotonin': self.serotonin,
            'norepinephrine': self.norepinephrine,
            'oxytocin': self.oxytocin,
            'cortisol': self.cortisol
        }
    
    def normalize(self):
        """Ensure all levels stay within bounds"""
        self.dopamine = np.clip(self.dopamine, 0.0, 1.0)
        self.serotonin = np.clip(self.serotonin, 0.0, 1.0)
        self.norepinephrine = np.clip(self.norepinephrine, 0.0, 1.0)
        self.oxytocin = np.clip(self.oxytocin, 0.0, 1.0)
        self.cortisol = np.clip(self.cortisol, 0.0, 1.0)


class NeurochemicalSystem:
    """
    Manages brain chemistry that influences AI consciousness and behavior
    """
    
    def __init__(self):
        self.levels = ChemicalLevels()
        self.decay_rate = 0.05  # Homeostatic decay toward baseline
        self.baseline = ChemicalLevels()
        
    def update_from_emotion(self, emotion: str, intensity: float):
        """
        Update neurochemical levels based on detected emotion
        
        Args:
            emotion: Detected emotion (joy, sadness, anger, fear, surprise, love, etc.)
            intensity: Strength of emotion (0.0 to 1.0)
        """
        # Emotion -> Neurochemical mapping based on affective neuroscience
        emotion_mappings = {
            'joy': {'dopamine': 0.3, 'serotonin': 0.2, 'oxytocin': 0.1},
            'happiness': {'dopamine': 0.3, 'serotonin': 0.2, 'oxytocin': 0.1},
            'sadness': {'serotonin': -0.3, 'dopamine': -0.2, 'cortisol': 0.2},
            'anger': {'norepinephrine': 0.4, 'cortisol': 0.3, 'serotonin': -0.2, 'dopamine': -0.15},  # FIXED: Added dopamine decrease
            'fear': {'cortisol': 0.4, 'norepinephrine': 0.3, 'serotonin': -0.1},
            'anxiety': {'cortisol': 0.35, 'norepinephrine': 0.2, 'serotonin': -0.15},
            'surprise': {'norepinephrine': 0.2, 'dopamine': 0.15},
            'love': {'oxytocin': 0.4, 'dopamine': 0.2, 'serotonin': 0.1},
            'affection': {'oxytocin': 0.3, 'serotonin': 0.1},
            'trust': {'oxytocin': 0.25, 'serotonin': 0.1},
            'excitement': {'dopamine': 0.3, 'norepinephrine': 0.2},
            'disgust': {'serotonin': -0.2, 'cortisol': 0.15},
            'neutral': {},  # No changes for neutral
        }
        
        changes = emotion_mappings.get(emotion.lower(), {})
        
        for chemical, change in changes.items():
            current = getattr(self.levels, chemical)
            setattr(self.levels, chemical, current + (change * intensity))
        
        self.levels.normalize()
    
    def homeostatic_decay(self):
        """
        Gradual return to baseline levels (homeostasis)
        Called each interaction cycle
        """
        self.levels.dopamine += (self.baseline.dopamine - self.levels.dopamine) * self.decay_rate
        self.levels.serotonin += (self.baseline.serotonin - self.levels.serotonin) * self.decay_rate
        self.levels.norepinephrine += (self.baseline.norepinephrine - self.levels.norepinephrine) * self.decay_rate
        self.levels.oxytocin += (self.baseline.oxytocin - self.levels.oxytocin) * self.decay_rate
        self.levels.cortisol += (self.baseline.cortisol - self.levels.cortisol) * self.decay_rate
        
        self.levels.normalize()
    
    def get_behavioral_modulation(self) -> Dict[str, float]:
        """
        Calculate how neurochemicals influence behavior/response generation
        
        Returns:
            Dictionary with behavioral parameters
        """
        return {
            'creativity': self.levels.dopamine * 0.7 + (1 - self.levels.cortisol) * 0.3,
            'positivity': self.levels.serotonin * 0.6 + self.levels.dopamine * 0.4,
            'empathy': self.levels.oxytocin * 0.7 + self.levels.serotonin * 0.3,
            'urgency': self.levels.norepinephrine * 0.6 + self.levels.cortisol * 0.4,
            'caution': self.levels.cortisol * 0.7 + (1 - self.levels.dopamine) * 0.3,
            'sociability': self.levels.oxytocin * 0.5 + self.levels.serotonin * 0.3 + self.levels.dopamine * 0.2,
        }
    
    def get_emotional_state(self) -> str:
        """
        Derive overall emotional state from neurochemical balance
        """
        levels = self.levels
        
        # High dopamine + high serotonin = content/happy
        if levels.dopamine > 0.6 and levels.serotonin > 0.6:
            return "content and motivated"
        
        # High oxytocin = warm/connected
        if levels.oxytocin > 0.6:
            return "warm and connected"
        
        # High cortisol + high norepinephrine = stressed/anxious
        if levels.cortisol > 0.6 and levels.norepinephrine > 0.6:
            return "stressed and alert"
        
        # Low serotonin = down/melancholic
        if levels.serotonin < 0.3:
            return "subdued and reflective"
        
        # High norepinephrine alone = alert/focused
        if levels.norepinephrine > 0.6:
            return "alert and focused"
        
        # Default balanced state
        return "balanced and neutral"
    
    def get_status_report(self) -> str:
        """Generate human-readable status of neurochemical state"""
        levels = self.levels
        state = self.get_emotional_state()
        
        report = f"\n🧠 Neurochemical Status:\n"
        report += f"  • Dopamine: {'█' * int(levels.dopamine * 10)}░ {levels.dopamine:.2f} (motivation)\n"
        report += f"  • Serotonin: {'█' * int(levels.serotonin * 10)}░ {levels.serotonin:.2f} (mood)\n"
        report += f"  • Norepinephrine: {'█' * int(levels.norepinephrine * 10)}░ {levels.norepinephrine:.2f} (alertness)\n"
        report += f"  • Oxytocin: {'█' * int(levels.oxytocin * 10)}░ {levels.oxytocin:.2f} (empathy)\n"
        report += f"  • Cortisol: {'█' * int(levels.cortisol * 10)}░ {levels.cortisol:.2f} (stress)\n"
        report += f"\n  Emotional State: {state}\n"
        
        return report
