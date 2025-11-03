"""
RoBERTa-based Emotion Detection
Analyzes text for emotional content to update neurochemical system
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Tuple
import numpy as np


class EmotionDetector:
    """
    Uses RoBERTa-based emotion classification model
    Maps detected emotions to neurochemical changes
    """
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """
        Initialize RoBERTa emotion detector
        
        Args:
            model_name: HuggingFace model for emotion classification
                       Default: fine-tuned RoBERTa on emotion detection
        """
        print(f"Loading emotion detection model: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        
        # Standard emotion labels (varies by model)
        self.emotion_labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
        
        print("✓ Emotion detector ready")
    
    def detect_emotion(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Detect emotion in text using RoBERTa
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (primary_emotion, confidence, all_scores)
        """
        if not text.strip():
            return 'neutral', 1.0, {'neutral': 1.0}
        
        # Tokenize and get predictions
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get scores for all emotions
        scores = predictions[0].numpy()
        emotion_scores = {self.emotion_labels[i]: float(scores[i]) for i in range(len(scores))}
        
        # Get primary emotion
        primary_idx = np.argmax(scores)
        primary_emotion = self.emotion_labels[primary_idx]
        confidence = float(scores[primary_idx])
        
        return primary_emotion, confidence, emotion_scores
    
    def analyze_conversation_turn(self, user_input: str, ai_response: str = None) -> Dict:
        """
        Analyze both user input and AI's own response
        Useful for tracking emotional dynamics
        
        Args:
            user_input: User's message
            ai_response: AI's generated response (optional)
            
        Returns:
            Dictionary with emotion analysis for both
        """
        analysis = {}
        
        # Analyze user input
        user_emotion, user_conf, user_scores = self.detect_emotion(user_input)
        analysis['user'] = {
            'emotion': user_emotion,
            'confidence': user_conf,
            'scores': user_scores
        }
        
        # Analyze AI response if provided
        if ai_response:
            ai_emotion, ai_conf, ai_scores = self.detect_emotion(ai_response)
            analysis['ai'] = {
                'emotion': ai_emotion,
                'confidence': ai_conf,
                'scores': ai_scores
            }
        
        return analysis
    
    def get_emotion_report(self, emotion: str, confidence: float, scores: Dict[str, float]) -> str:
        """Generate human-readable emotion report"""
        report = f"😊 Detected: {emotion.upper()} (confidence: {confidence:.2%})\n"
        report += "   Distribution: "
        report += ", ".join([f"{e}: {s:.1%}" for e, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]])
        return report
