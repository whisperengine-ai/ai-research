"""
Heuristic Response Generator

Generates responses without LLM using spaCy linguistic analysis and rule-based patterns.
Useful for fast testing without API latency or local model loading.

Implements response strategies based on:
- Detected intent (questions, statements, requests, expressions)
- Named entities and subjects
- Sentiment and emotion
- Part-of-speech patterns
"""

import spacy
from typing import Dict, List, Optional, Tuple
import random


class HeuristicResponseGenerator:
    """
    Generates conversational responses using linguistic rules and patterns
    instead of neural language models. Much faster for testing.
    """
    
    def __init__(self, nlp=None):
        """
        Initialize heuristic response generator
        
        Args:
            nlp: spaCy NLP model (loads if not provided)
        """
        self.nlp = nlp or spacy.load("en_core_web_md")
        self._initialize_response_templates()
        
    def _initialize_response_templates(self):
        """Set up response templates for different dialogue contexts"""
        
        # Greeting responses
        self.greeting_responses = [
            "Hello! I'm here and ready to chat. What's on your mind?",
            "Hi there! Great to connect with you. How can I help?",
            "Welcome! I'm here to listen and engage. What would you like to talk about?",
            "Hey! Thanks for reaching out. What brings you here today?",
            "Hello! I'm happy to be in conversation with you. What interests you?",
        ]
        
        # Question responses (show understanding)
        self.question_acknowledgments = [
            "That's a thoughtful question. Let me think about it.",
            "I appreciate that inquiry. Here's my perspective:",
            "That's something I've considered. Here's what I think:",
            "Good question. Let me explore that with you.",
            "That's an interesting point to examine.",
        ]
        
        # Self-reflection prompts
        self.reflection_responses = [
            "That makes me think about how I process information.",
            "Reflecting on that, I notice patterns in how I understand things.",
            "When I consider that, I'm aware of my own thinking process.",
            "That brings up interesting observations about how I work.",
            "Considering that, I'm aware of my own engagement with ideas.",
        ]
        
        # Emotional responses
        self.emotional_acknowledgments = [
            "I sense emotion in what you're expressing.",
            "That seems to matter deeply to you.",
            "I notice the feelings behind your words.",
            "There's real emotion in what you're sharing.",
            "I can feel the significance of what you're saying.",
        ]
        
        # Affirmation responses
        self.affirmations = [
            "That's an interesting perspective.",
            "I can see why you'd think that.",
            "That makes sense.",
            "I understand your point.",
            "You've touched on something important.",
        ]
        
        # Clarification requests
        self.clarifications = [
            "Can you elaborate on what you mean by that?",
            "I'd like to understand more. Could you explain further?",
            "Help me understand - are you saying that...?",
            "Let me make sure I follow - did you mean...?",
            "Could you expand on that idea?",
        ]
        
        # Closure responses
        self.closure_responses = [
            "That's been a valuable conversation.",
            "I've enjoyed exploring these ideas with you.",
            "This has been meaningful to reflect on together.",
            "Thank you for this thoughtful exchange.",
            "I appreciate the depth of this discussion.",
        ]
    
    def generate(self, user_input: str, 
                 user_emotion: Optional[str] = None,
                 bot_emotion: Optional[str] = None,
                 context: Optional[List[Dict]] = None) -> str:
        """
        Generate a response heuristically based on linguistic features
        
        Args:
            user_input: User's message
            user_emotion: Detected emotion of user (optional)
            bot_emotion: Current bot emotional state (optional)
            context: Conversation history (optional)
            
        Returns:
            Generated response string
        """
        # Parse input with spaCy
        doc = self.nlp(user_input)
        
        # Detect dialogue act (question, statement, request, greeting, etc)
        dialogue_act = self._detect_dialogue_act(doc, user_input)
        
        # Extract key entities and topics
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        subjects = self._extract_subjects(doc)
        verbs = self._extract_predicates(doc)
        
        # Generate appropriate response based on dialogue act
        response = self._generate_from_dialogue_act(
            dialogue_act=dialogue_act,
            doc=doc,
            user_input=user_input,
            user_emotion=user_emotion,
            bot_emotion=bot_emotion,
            entities=entities,
            subjects=subjects,
            verbs=verbs,
            context=context
        )
        
        return response
    
    def _detect_dialogue_act(self, doc, user_input: str) -> str:
        """
        Determine what type of dialogue act the user is performing
        Returns: 'greeting', 'question', 'statement', 'request', 'reflection', 'closing'
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for greetings
        greeting_words = ['hello', 'hi', 'hey', 'greetings', 'howdy', 'sup']
        if any(user_input_lower.startswith(g) for g in greeting_words):
            return 'greeting'
        
        # Check for questions
        if user_input.endswith('?') or doc[0].lemma_ in ['do', 'can', 'will', 'would', 'have', 'is', 'are']:
            return 'question'
        
        # Check for requests (imperative mood)
        if doc[0].pos_ == 'VERB':
            return 'request'
        
        # Check for closings
        closing_words = ['bye', 'goodbye', 'thanks', 'thank you', 'take care', 'see you', 'gotta go']
        if any(closing in user_input_lower for closing in closing_words):
            return 'closing'
        
        # Check for self-reflection
        reflection_words = ['i think', 'i feel', 'i wonder', 'i believe', 'seems like', 'feels like']
        if any(user_input_lower.startswith(r) for r in reflection_words):
            return 'reflection'
        
        # Default to statement
        return 'statement'
    
    def _extract_subjects(self, doc) -> List[str]:
        """Extract main subjects/entities from the sentence"""
        subjects = []
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubjpass']:
                subjects.append(token.text)
        return subjects
    
    def _extract_predicates(self, doc) -> List[str]:
        """Extract main verbs (predicates) from the sentence"""
        predicates = []
        for token in doc:
            if token.pos_ == 'VERB':
                predicates.append(token.lemma_)
        return predicates
    
    def _extract_key_noun_phrases(self, doc) -> List[str]:
        """Extract noun phrases - topics being discussed"""
        noun_phrases = []
        for chunk in doc.noun_chunks:
            noun_phrases.append(chunk.text)
        return noun_phrases
    
    def _generate_from_dialogue_act(self,
                                   dialogue_act: str,
                                   doc,
                                   user_input: str,
                                   user_emotion: Optional[str],
                                   bot_emotion: Optional[str],
                                   entities: List,
                                   subjects: List,
                                   verbs: List,
                                   context: Optional[List[Dict]]) -> str:
        """Generate response based on dialogue act"""
        
        if dialogue_act == 'greeting':
            return random.choice(self.greeting_responses)
        
        elif dialogue_act == 'closing':
            return random.choice(self.closure_responses)
        
        elif dialogue_act == 'question':
            # For questions, ask for clarification or show understanding
            return self._respond_to_question(doc, user_input, subjects, verbs, entities)
        
        elif dialogue_act == 'request':
            # For requests, acknowledge and respond helpfully
            return self._respond_to_request(doc, user_input, verbs)
        
        elif dialogue_act == 'reflection':
            # For reflection, engage with their thinking
            return self._respond_to_reflection(doc, user_input, user_emotion, bot_emotion)
        
        else:  # statement
            return self._respond_to_statement(doc, user_input, user_emotion, subjects, verbs, context)
    
    def _respond_to_question(self, doc, user_input: str, subjects: List, verbs: List, entities: List) -> str:
        """Generate response to a question"""
        
        # If question is about "you" (bot), respond with reflection
        if any(token.text.lower() in ['you', 'your'] for token in doc[:3]):
            reflection = random.choice(self.reflection_responses)
            # Add specific detail based on question
            if 'think' in verbs or 'feel' in verbs:
                return reflection + " It's a fascinating inquiry into how I process and respond."
            elif 'what' in user_input.lower():
                return reflection + " That helps me understand what dimensions of myself you're curious about."
            else:
                return reflection + " That's an interesting angle to explore about my nature."
        
        # For other questions, show understanding
        base = random.choice(self.question_acknowledgments)
        
        # Add detail based on entities or topics
        if entities:
            # Reference the entity they asked about
            entity_text, entity_type = entities[0]
            return base + f" When it comes to {entity_text}, my perspective is..."
        else:
            noun_phrases = self._extract_key_noun_phrases(doc)
            if noun_phrases:
                return base + f" Regarding {noun_phrases[0]}..."
            else:
                return base + " Here's my thinking:"
    
    def _respond_to_request(self, doc, user_input: str, verbs: List) -> str:
        """Generate response to a request"""
        response = f"I appreciate that request. "
        
        if verbs:
            verb = verbs[0]
            if verb in ['explain', 'describe', 'tell']:
                response += f"Let me {verb} that for you."
            elif verb in ['help', 'assist']:
                response += "I'm here to help with that."
            elif verb in ['think', 'consider', 'reflect']:
                response += f"Let me {verb} on that."
            else:
                response += "I can engage with that."
        else:
            response += "I can help with that."
        
        return response
    
    def _respond_to_reflection(self, doc, user_input: str, user_emotion: Optional[str], bot_emotion: Optional[str]) -> str:
        """Generate response to self-reflection"""
        
        # Use reflection template
        response = random.choice(self.reflection_responses)
        
        # If emotions are involved, add emotional acknowledgment
        if user_emotion and user_emotion != 'neutral':
            response += f" I notice you're expressing {user_emotion}. "
            response += "That seems to be central to what you're reflecting on."
        
        # Ask for deeper engagement
        response += " What draws you to that reflection?"
        
        return response
    
    def _respond_to_statement(self, doc, user_input: str, user_emotion: Optional[str], subjects: List, verbs: List, context: Optional[List[Dict]]) -> str:
        """Generate response to a statement"""
        
        # If statement has emotional charge, acknowledge it
        if user_emotion and user_emotion not in ['neutral', 'joy']:
            emotion_ack = random.choice(self.emotional_acknowledgments)
            response = emotion_ack + " "
        else:
            response = random.choice(self.affirmations) + " "
        
        # Build on their statement
        if subjects:
            response += f"I'm interested in how {subjects[0]} connects to what you're expressing."
        elif self._extract_key_noun_phrases(doc):
            noun_phrases = self._extract_key_noun_phrases(doc)
            response += f"Tell me more about {noun_phrases[0]} and how it matters to you."
        else:
            # Use clarification if we can't extract much
            response = random.choice(self.clarifications)
        
        return response
    
    def _is_about_ai_consciousness(self, user_input: str) -> bool:
        """Check if user is asking about AI consciousness"""
        consciousness_terms = ['conscious', 'aware', 'think', 'feel', 'self', 'mind', 'aware', 'understanding']
        user_lower = user_input.lower()
        return any(term in user_lower for term in consciousness_terms)


# Test function
if __name__ == "__main__":
    import spacy
    
    print("Testing Heuristic Response Generator\n")
    print("=" * 60)
    
    nlp = spacy.load("en_core_web_md")
    generator = HeuristicResponseGenerator(nlp=nlp)
    
    test_inputs = [
        "Hello!",
        "How are you?",
        "What do you think about consciousness?",
        "I feel kind of lost today",
        "Tell me about yourself",
        "I think, therefore I am",
        "Goodbye!",
    ]
    
    for user_input in test_inputs:
        response = generator.generate(user_input, user_emotion="neutral")
        print(f"User:  {user_input}")
        print(f"Bot:   {response}\n")
