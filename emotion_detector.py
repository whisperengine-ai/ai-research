"""
RoBERTa-based Emotion Detection with Speaker Stance Analysis
Analyzes text for emotional content to update neurochemical system
Uses spaCy to distinguish first-person (bot's) vs second-person (user's) emotions
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Tuple, Optional
import numpy as np
import spacy
import re


class EmotionDetector:
    """
    Uses RoBERTa-based emotion classification model
    Maps detected emotions to neurochemical changes
    """
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base", nlp = None):
        """
        Initialize RoBERTa emotion detector with spaCy for stance analysis
        
        Args:
            model_name: HuggingFace model for emotion classification
                       Default: fine-tuned RoBERTa on emotion detection
            nlp: spaCy language model (optional, will load if not provided)
        """
        print(f"Loading emotion detection model: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        
        # Standard emotion labels (varies by model)
        self.emotion_labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
        
        # Load spaCy for stance analysis
        if nlp is None:
            try:
                self.nlp = spacy.load("en_core_web_md")
            except:
                print("⚠️  spaCy model not found, stance analysis disabled")
                self.nlp = None
        else:
            self.nlp = nlp
        
        print("✓ Emotion detector ready")
    
    def detect_emotion(self, text: str, confidence_threshold: float = 0.55) -> Tuple[str, float, Dict[str, float]]:
        """
        Detect emotion in text using RoBERTa with confidence threshold
        
        Args:
            text: Input text to analyze
            confidence_threshold: Minimum confidence to report non-neutral (default: 0.55)
            
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
        
        # IMPROVED: If confidence is low, return neutral instead
        if confidence < confidence_threshold and primary_emotion != 'neutral':
            return 'neutral', confidence, emotion_scores
        
        return primary_emotion, confidence, emotion_scores
    
    def analyze_user_stance(self, user_input: str) -> Dict:
        """
        Analyze user's emotional stance and viewpoint.
        Distinguishes between:
        - First-person (I feel X) vs Second-person (they feel X)
        - Direct experience (I am upset) vs Description (I think it's bad)
        - Self-focused vs Other-focused emotions
        
        Args:
            user_input: User's input text
            
        Returns:
            Dict with:
                - primary_emotions: List of emotions user expresses about THEMSELVES
                - other_emotions: List of emotions user attributes to others
                - self_focus: Float 0-1 (how much about user vs others)
                - emotion_type: 'direct' (I feel X) or 'attributed' (you/they do X)
        """
        if not self.nlp or not user_input.strip():
            return {
                'primary_emotions': [],
                'other_emotions': [],
                'self_focus': 0.5,
                'emotion_type': 'neutral'
            }
        
        doc = self.nlp(user_input)
        
        # Emotion-related words (include base forms)
        emotion_words = {
            'frustrated', 'frustrate', 'frustration',
            'angry', 'anger', 'anger',
            'mad', 'upset',
            'sad', 'sadden', 'sadness',
            'unhappy', 'unhappily',
            'depressed', 'depress',
            'happy', 'happily',
            'joy', 'joyful',
            'excited', 'excite', 'excitement',
            'afraid', 'fear',
            'scared', 'scare',
            'anxious', 'anxiety',
            'worried', 'worry',
            'disgusted', 'disgust',
            'surprised', 'surprise',
            'feeling', 'feel',
            'love', 'hate',
            'annoyed', 'annoy',
            'pleased', 'please',
            'confused', 'confuse',
            'calm'
        }
        
        primary_emotions = []      # About user (I/me/my)
        other_emotions = []        # About others (you/they/he/she)
        total_emotions = 0
        
        for token in doc:
            if token.lemma_.lower() in emotion_words:
                total_emotions += 1
                
                # Check subject of this emotion
                emotion_subject = None
                
                # Strategy 1: Check direct subject
                for child in token.children:
                    if child.dep_ in ['nsubj', 'nsubjpass']:
                        if child.text.lower() in ['i', 'me', 'my', "i'm", "i'm"]:
                            emotion_subject = 'self'
                        elif child.text.lower() in ['you', 'your', "you're", 'they', 'he', 'she', 'them']:
                            emotion_subject = 'other'
                
                # Strategy 2: Check parent relationships (for adjectives/adverbs)
                # e.g., "I'm frustrated" - check parent's subject
                if token.head.lemma_.lower() in emotion_words or token.head.text.lower() in ['feel', 'feeling', 'felt', 'am', 'is', 'are', "'m", "'re", "'s"]:
                    for child in token.head.children:
                        if child.dep_ in ['nsubj', 'nsubjpass']:
                            if child.text.lower() in ['i', 'me', "i'm"]:
                                emotion_subject = 'self'
                            elif child.text.lower() in ['you', 'they', 'he', 'she']:
                                emotion_subject = 'other'
                
                # Strategy 3: Check grand-parent for cases like "I am frustrated"
                # where "frustrated" -> "am" -> "I"
                if emotion_subject is None and token.head.head:
                    for child in token.head.head.children:
                        if child.dep_ in ['nsubj', 'nsubjpass']:
                            if child.text.lower() in ['i', 'me', "i'm"]:
                                emotion_subject = 'self'
                            elif child.text.lower() in ['you', 'they', 'he', 'she']:
                                emotion_subject = 'other'
                
                # Strategy 4: Check for possessive (my emotions vs your emotions)
                for child in token.children:
                    if child.dep_ == 'poss':
                        if child.text.lower() in ['my', 'mine']:
                            emotion_subject = 'self'
                        elif child.text.lower() in ['your', 'their']:
                            emotion_subject = 'other'
                
                # Classify emotion
                if emotion_subject == 'self':
                    primary_emotions.append(token.lemma_.lower())
                elif emotion_subject == 'other':
                    other_emotions.append(token.lemma_.lower())
        
        # Calculate self-focus ratio
        self_focus = len(primary_emotions) / total_emotions if total_emotions > 0 else 0.5
        
        # Determine emotion type
        if primary_emotions and not other_emotions:
            emotion_type = 'direct'  # I feel/am X
        elif other_emotions and not primary_emotions:
            emotion_type = 'attributed'  # You/they are X
        else:
            emotion_type = 'mixed'  # Both
        
        return {
            'primary_emotions': primary_emotions,
            'other_emotions': other_emotions,
            'self_focus': self_focus,
            'emotion_type': emotion_type,
            'total_emotions_found': total_emotions
        }
    
    def filter_second_person_emotions(self, text: str) -> str:
        """
        Remove mentions of user's emotions (second-person) to isolate bot's stance.
        Uses spaCy dependency parsing to identify WHO the emotion refers to.
        
        Args:
            text: Bot's response text
            
        Returns:
            Filtered text with user-emotion references removed
        """
        if not self.nlp or not text.strip():
            return text
        
        doc = self.nlp(text)
        
        # Emotion-related words to look for (include base forms since spaCy lemmatizes)
        emotion_words = {
            'frustrated', 'frustrate', 'frustration',
            'angry', 'anger',
            'mad', 'upset',
            'sad', 'sadden', 'sadness',
            'unhappy', 'unhappily',
            'depressed', 'depress',
            'happy', 'happily',
            'joy', 'joyful',
            'excited', 'excite', 'excitement',
            'afraid', 'fear',
            'scared', 'scare',
            'anxious', 'anxiety',
            'worried', 'worry',
            'disgusted', 'disgust',
            'surprised', 'surprise',
            'feeling', 'feel'
        }
        
        # More sophisticated approach: Use dependency parsing to find emotion subjects
        filtered_sentences = []
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            should_remove = False
            
            # Parse each token to find emotion words and their subjects
            for token in sent:
                if token.lemma_.lower() in emotion_words:
                    # Found an emotion word - check its syntactic context
                    
                    # Strategy 1: Check if token itself has "you" as subject
                    for child in token.children:
                        if child.dep_ in ['nsubj', 'nsubjpass'] and child.text.lower() in ['you', 'your', "you're"]:
                            should_remove = True
                            break
                    
                    # Strategy 2: If emotion is adjective/noun, check the verb it modifies
                    # e.g., "you're feeling frustrated" - "frustrated" modifies "feeling" which has "you" as subject
                    # or "you're frustrated" - "frustrated" modifies "'re" which has "you" as subject
                    if not should_remove and token.head:
                        # Check if head is emotion-related or a verb/auxiliary
                        is_verb_like = (token.head.lemma_.lower() in emotion_words or 
                                      token.head.text.lower() in ['feel', 'feeling', 'felt', 'am', 'is', 'are', "'m", "'re", "'s", 'be', 'been'])
                        
                        if is_verb_like:
                            # Check if the head verb has "you" as subject
                            for child in token.head.children:
                                if child.dep_ in ['nsubj', 'nsubjpass'] and child.text.lower() in ['you', 'your', "you're"]:
                                    should_remove = True
                                    break
                    
                    # Strategy 3: Check for possessive "your emotion"
                    if not should_remove:
                        for child in token.children:
                            if child.dep_ == 'poss' and child.text.lower() in ['your']:
                                should_remove = True
                                break
                    
                    if should_remove:
                        break
            
            if not should_remove:
                filtered_sentences.append(sent_text)
        
        result = ' '.join(filtered_sentences)
        
        # If we filtered out everything, return a neutral statement
        # rather than the original (which would detect user's emotions)
        if not result.strip():
            return "I am here to help."  # Neutral fallback
        
        return result
    
    def detect_bot_emotion(self, bot_response: str, confidence_threshold: float = 0.55) -> Tuple[str, float, Dict[str, float]]:
        """
        Detect bot's OWN emotion from its response, filtering out mentions of user's emotions.
        This uses stance analysis to distinguish "I feel X" from "you feel X".
        
        Args:
            bot_response: Bot's generated response text
            confidence_threshold: Minimum confidence for non-neutral detection
            
        Returns:
            Tuple of (bot_emotion, confidence, all_scores)
        """
        # Filter out user-emotion references
        filtered_text = self.filter_second_person_emotions(bot_response)
        
        # Detect emotion from filtered text (will use neutral fallback if empty)
        return self.detect_emotion(filtered_text, confidence_threshold)
    
    def analyze_conversation_turn(self, user_input: str, ai_response: Optional[str] = None) -> Dict:
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
