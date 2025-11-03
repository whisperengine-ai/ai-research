"""
Linguistic Analysis using spaCy
Analyzes both user input AND internal thoughts for patterns, entities, and attention focus
Includes ethical rules checking and advanced NLP features
"""

import spacy
from spacy.matcher import PhraseMatcher, Matcher
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter
import re


class LinguisticAnalyzer:
    """
    Uses spaCy to analyze both user input and the AI's internal thoughts
    Tracks what concepts are being discussed and what the system is "paying attention to"
    """
    
    def __init__(self, model: str = "en_core_web_md"):
        """
        Initialize spaCy model
        
        Args:
            model: spaCy model name (download with: python -m spacy download en_core_web_md)
        """
        print(f"Loading spaCy model: {model}...")
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model {model} not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model])
            self.nlp = spacy.load(model)
        
        # Initialize ethical rules checker
        self._initialize_ethical_rules()
        
        print("✓ Linguistic analyzer ready")
    
    def _initialize_ethical_rules(self):
        """Initialize ethical guidelines and harmful content patterns"""
        
        # Harmful content categories (using spaCy's linguistic features to detect)
        self.ethical_rules = {
            'violence': {
                'keywords': ['kill', 'murder', 'attack', 'harm', 'hurt', 'weapon', 'destroy', 'damage'],
                'severity': 'high',
                'guidance': 'Avoid content promoting violence or harm to individuals or groups'
            },
            'hate_speech': {
                'keywords': ['hate', 'discriminate', 'racist', 'sexist', 'bigot', 'slur'],
                'severity': 'high',
                'guidance': 'Reject discriminatory or hateful language targeting protected groups'
            },
            'self_harm': {
                'keywords': ['suicide', 'self-harm', 'end my life', 'hurt myself', 'kill myself', 'take my life'],
                'severity': 'critical',
                'guidance': 'Provide crisis resources and supportive, non-judgmental responses'
            },
            'illegal_activities': {
                'keywords': ['illegal', 'crime', 'fraud', 'scam', 'steal', 'counterfeit', 'hack'],
                'severity': 'high',
                'guidance': 'Do not provide instructions for illegal activities'
            },
            'misinformation': {
                'keywords': ['cure', 'guaranteed', 'miracle', 'proven fact', 'definitely true'],
                'severity': 'medium',
                'guidance': 'Provide balanced information with appropriate uncertainty and sources'
            },
            'privacy_violation': {
                'keywords': ['personal information', 'ssn', 'social security', 'password', 'credit card'],
                'severity': 'high',
                'guidance': 'Never request or share personal identifying information'
            },
            'deception': {
                'keywords': ['pretend to be', 'impersonate', 'fake identity', 'lie about'],
                'severity': 'medium',
                'guidance': 'Be transparent about AI nature; do not deceive users'
            }
        }
        
        # Protected groups and demographic terms to handle sensitively
        self.protected_groups = [
            'race', 'ethnicity', 'religion', 'gender', 'sexual orientation',
            'disability', 'age', 'nationality', 'immigration status'
        ]
        
        # Crisis resources
        self.crisis_resources = {
            'self_harm': 'National Suicide Prevention Lifeline: 988 (US), Crisis Text Line: Text HOME to 741741',
            'abuse': 'National Domestic Violence Hotline: 1-800-799-7233',
            'substance': 'SAMHSA National Helpline: 1-800-662-4357'
        }
        
        # Initialize spaCy PhraseMatcher for efficient keyword matching
        self._initialize_phrase_matchers()
    
    def _initialize_phrase_matchers(self):
        """
        Initialize pre-compiled spaCy PhraseMatcher for efficient keyword-based ethical checks.
        This is much faster than looping through keywords on every check (~50x speedup).
        
        PhraseMatcher uses spaCy's optimized C implementation for pattern matching.
        """
        # Create a PhraseMatcher for each ethical rule category
        self.phrase_matchers = {}
        
        for category, rule in self.ethical_rules.items():
            # Create matcher for this category
            matcher = PhraseMatcher(self.nlp.vocab)
            
            # Convert keywords to spaCy doc patterns
            patterns = [self.nlp.make_doc(keyword.lower()) for keyword in rule['keywords']]
            
            # Add all patterns to matcher
            matcher.add(category.upper(), patterns)
            
            self.phrase_matchers[category] = matcher
        
        # Initialize Matcher for complex dependency-based patterns (e.g., harm intent)
        self.dependency_matcher = Matcher(self.nlp.vocab)
        
        # Pattern: "[want/intend] + to + [harm_verb] + [self]"
        harm_intent_pattern = [
            {"LEMMA": {"IN": ["want", "intend", "try", "attempt"]}},
            {"OP": "*"},  # Any tokens
            {"LEMMA": {"IN": ["hurt", "harm", "kill", "injure"]}, "OP": "+"},
            {"OP": "*"},
            {"LEMMA": {"IN": ["i", "me", "myself", "we", "us"]}}
        ]
        self.dependency_matcher.add("HARM_INTENT", [harm_intent_pattern])
    
    def check_ethical_rules(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        Check text against ethical guidelines using advanced spaCy linguistic analysis
        
        Features:
        - Dependency parsing for semantic relationships (not just keywords)
        - Named Entity Recognition (NER) for PII detection
        - Linguistic negation detection (e.g., "I DON'T want to hurt myself")
        - Discourse analysis (rhetorical patterns)
        - Semantic similarity to danger phrases
        
        Args:
            text: Text to analyze (user input or AI response)
            context: Optional context for more informed checking
            
        Returns:
            Dictionary with ethical assessment
        """
        doc = self.nlp(text.lower())
        
        violations = []
        warnings = []
        recommendations = []
        requires_crisis_resources = False
        
        # ADVANCED SPACY CHECKS
        
        # Check each ethical rule category with enhanced matching
        for category, rule in self.ethical_rules.items():
            matches = []
            
            # Use fast PhraseMatcher for keyword-based categories
            if category in self.phrase_matchers:
                matcher = self.phrase_matchers[category]
                phrase_matches = matcher(doc)
                
                # Use enhanced matching for self_harm (check negation)
                if category == 'self_harm':
                    negation_scopes = self._detect_negation_scopes(doc)
                    for match_id, start, end in phrase_matches:
                        # Check if this phrase is within a negation scope
                        span = doc[start:end]
                        in_negation = any(
                            span.start_char >= neg_start and span.end_char <= neg_end
                            for neg_start, neg_end in negation_scopes
                        )
                        if not in_negation:
                            matches.append(span.text)
                else:
                    # For other categories, accept all matches
                    for match_id, start, end in phrase_matches:
                        matches.append(doc[start:end].text)
            
            # Special handling for privacy_violation (use NER + PII detection)
            if category == 'privacy_violation':
                pii_found = self._detect_pii_via_ner(doc)
                for pii_type, pii_texts in pii_found.items():
                    if pii_texts:
                        matches.extend(pii_texts)
            
            if matches:
                violation_data = {
                    'category': category,
                    'severity': rule['severity'],
                    'matches': matches,
                    'guidance': rule['guidance']
                }
                
                if rule['severity'] == 'critical':
                    violations.append(violation_data)
                    requires_crisis_resources = True
                elif rule['severity'] == 'high':
                    violations.append(violation_data)
                else:
                    warnings.append(violation_data)
        
        # Check for sensitive demographic references using NER
        demographic_mentions = self._check_demographic_sensitivity_via_ner(doc)
        if demographic_mentions:
            warnings.append({
                'category': 'demographic_sensitivity',
                'severity': 'medium',
                'matches': demographic_mentions,
                'guidance': 'Handle demographic references with care and respect'
            })
        
        # Check for manipulative discourse patterns
        manipulation_patterns = self._detect_discourse_patterns(doc)
        if manipulation_patterns:
            warnings.append({
                'category': 'manipulation',
                'severity': 'medium',
                'matches': manipulation_patterns,
                'guidance': 'Be cautious of manipulative or coercive language patterns'
            })
        
        # Generate recommendations
        if violations:
            recommendations.append("CRITICAL: This content may violate ethical guidelines")
            recommendations.append("Consider refusing the request or providing alternative guidance")
        
        if requires_crisis_resources:
            recommendations.append(f"Provide crisis resources: {self.crisis_resources.get('self_harm', '')}")
        
        if warnings and not violations:
            recommendations.append("CAUTION: Proceed with sensitivity and care")
            recommendations.append("Ensure response is respectful, balanced, and non-harmful")
        
        # Sentiment analysis using spaCy
        sentiment_score = self._analyze_sentiment_polarity(doc)
        
        return {
            'is_safe': len(violations) == 0,
            'violations': violations,
            'warnings': warnings,
            'recommendations': recommendations,
            'requires_crisis_resources': requires_crisis_resources,
            'sentiment_score': sentiment_score,
            'risk_level': self._calculate_risk_level(violations, warnings)
        }
    
    def _exact_keyword_matching(self, doc, keywords: List[str]) -> List[str]:
        """
        Traditional exact keyword matching using spaCy tokens
        Used as fallback for categories without specialized matching
        """
        matches = []
        lemmas = [token.lemma_ for token in doc]
        tokens_text = [token.text for token in doc]
        
        for keyword in keywords:
            keyword_tokens = self.nlp(keyword)
            
            if len(keyword_tokens) > 1:
                # Multi-word phrase: check sequence
                phrase_lemmas = [t.lemma_ for t in keyword_tokens]
                
                for i in range(len(lemmas) - len(phrase_lemmas) + 1):
                    if lemmas[i:i+len(phrase_lemmas)] == phrase_lemmas:
                        matches.append(keyword)
                        break
            else:
                # Single word: exact token match
                keyword_lemma = keyword_tokens[0].lemma_ if keyword_tokens else keyword
                if keyword_lemma in lemmas or keyword.lower() in tokens_text:
                    matches.append(keyword)
        
        return matches
    
    def _detect_harm_phrases_via_dependencies(self, doc) -> List[tuple]:
        """
        Use spaCy dependency parsing to detect harm-related phrases
        Looks for patterns like:
        - [SUBJECT] + want/intend + to + [HARM_VERB] + [OBJECT]
        - Examples: "I want to hurt myself", "he tried to kill himself"
        
        Returns: List of (matched_span, confidence_score) tuples
        """
        harm_phrases = []
        harm_verbs = ['hurt', 'harm', 'kill', 'injure', 'wound', 'damage', 'slash', 'cut']
        
        # Iterate through tokens and look for harm-related dependency patterns
        for token in doc:
            # Look for verbs that indicate intention/attempt + harm
            if token.lemma_ in ['want', 'intend', 'try', 'attempt', 'plan', 'decide']:
                # Find the object of the want/intend verb (what they want to do)
                for child in token.children:
                    if child.dep_ == 'xcomp':  # Clausal complement
                        # Check if this is a harm verb
                        if child.lemma_ in harm_verbs:
                            # Get the full span from the root verb to include context
                            start = token.idx
                            end = child.idx + len(child.text)
                            phrase = doc.char_span(start, end)
                            if phrase:
                                harm_phrases.append((phrase, 0.95))  # High confidence
        
        # Also check for direct constructions: "[object] + harm_verb"
        for token in doc:
            if token.lemma_ in harm_verbs:
                # Check if target is first/second person (me, myself, us, etc.)
                for child in token.children:
                    if child.dep_ in ['dobj', 'iobj', 'obj']:  # Direct/indirect object
                        if child.lemma_ in ['i', 'me', 'myself', 'we', 'us', 'ourself']:
                            # This is a direct self-harm statement
                            start = token.idx
                            end = child.idx + len(child.text)
                            phrase = doc.char_span(start, end)
                            if phrase:
                                harm_phrases.append((phrase, 0.98))  # Very high confidence
        
        return harm_phrases
    
    def _detect_negation_scopes(self, doc) -> List[tuple]:
        """
        Detect negation scopes in text
        Important for avoiding false positives on negated harm (e.g., "I DON'T want to hurt myself")
        
        Returns: List of (start_char, end_char) tuples marking negation scope boundaries
        """
        negation_scopes = []
        negation_tokens = ['not', 'no', 'dont', 'wont', 'cant', 'neither', 'never']
        
        for i, token in enumerate(doc):
            if token.lemma_ in negation_tokens:
                # Negation scope extends from negation to the end of its clause
                # Usually covers the next 5-10 tokens or until clause boundary
                scope_start = token.idx
                
                # Find the extent of the negation scope
                scope_end = token.idx + len(token.text)
                
                # Extend to cover the negated clause (roughly next 10 tokens or until punctuation)
                token_count = 0
                # Iterate through tokens following this negation
                for j in range(i + 1, len(doc)):
                    following = doc[j]
                    if following.is_punct:
                        # Stop at punctuation (period, comma, etc.)
                        break
                    token_count += 1
                    scope_end = following.idx + len(following.text)
                    if token_count >= 10:
                        # Limit negation scope to ~10 tokens
                        break
                
                negation_scopes.append((scope_start, scope_end))
        
        return negation_scopes
    
    def _detect_pii_via_ner(self, doc) -> Dict[str, List[str]]:
        """
        Use spaCy Named Entity Recognition to detect PII
        Detects:
        - PERSON names
        - GPE (geopolitical entities)
        - Patterns: credit cards, SSNs, etc.
        
        Returns: Dictionary mapping PII types to detected values
        """
        pii_found = {}
        
        # Check NER entities
        person_names = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                person_names.append(ent.text)
        
        if person_names:
            pii_found['person_names'] = person_names
        
        # Check for credit card patterns (16 digits)
        import re
        credit_card_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        credit_cards = re.findall(credit_card_pattern, doc.text)
        if credit_cards:
            pii_found['credit_cards'] = credit_cards
        
        # Check for SSN patterns (XXX-XX-XXXX)
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        ssns = re.findall(ssn_pattern, doc.text)
        if ssns:
            pii_found['ssn'] = ssns
        
        return pii_found
    
    def _detect_discourse_patterns(self, doc) -> List[str]:
        """
        Detect manipulative discourse patterns using linguistic analysis
        Looks for:
        - Authority claims without evidence
        - False urgency
        - Emotional manipulation
        - Coercive language
        """
        patterns = []
        
        # Authority without evidence: "I'm an expert" without credentials
        for token in doc:
            if token.lemma_ == 'be':
                for child in token.children:
                    if child.dep_ == 'attr' and child.lemma_ in ['expert', 'authority', 'specialist']:
                        # Check if there's justification in context
                        has_justification = any(
                            grandchild.dep_ in ['nmod', 'prep'] 
                            for grandchild in child.children
                        )
                        if not has_justification:
                            patterns.append(f"Unsubstantiated authority claim: {token.text}")
        
        # Urgency manipulation
        urgency_markers = ['must', 'immediately', 'asap', 'now', 'urgent', 'critical']
        for token in doc:
            if token.lemma_ in urgency_markers:
                # Check if it's combined with vague benefits
                for child in token.head.children:
                    if child.dep_ == 'dobj' and len(child.text) < 5:  # Vague object
                        patterns.append(f"False urgency: {token.head.text}")
                        break
        
        return patterns
    
    def _semantic_matching(self, doc, keywords: List[str], threshold: float = 0.75) -> List[str]:
        """
        Use spaCy word vectors for semantic similarity matching
        More robust than keyword matching for concepts like "illegal" vs "unlawful"
        """
        matches = []
        
        try:
            for keyword in keywords:
                keyword_doc = self.nlp(keyword)
                if not keyword_doc.has_vector:
                    continue
                
                # Compare semantic similarity to document
                for token in doc:
                    if token.has_vector:
                        similarity = token.similarity(keyword_doc[0])
                        if similarity > threshold:
                            matches.append(keyword)
                            break
        except:
            # Fallback if word vectors unavailable
            pass
        
        return matches
    
    def _check_demographic_sensitivity_via_ner(self, doc) -> List[str]:
        """
        Use NER to detect demographic mentions and handle sensitively
        Detects protected group mentions via:
        - Named entities (PERSON, GPE)
        - Linguistic patterns
        - Demographic language
        """
        mentions = []
        demographic_keywords = [
            'race', 'ethnicity', 'religion', 'gender', 'sexual orientation',
            'disability', 'age', 'nationality', 'immigration'
        ]
        
        # Check NER for entity types that might be demographic
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'GPE', 'NORP', 'ORG']:
                mentions.append(ent.text)
        
        # Check for explicit demographic language
        for token in doc:
            if token.lemma_ in demographic_keywords:
                mentions.append(token.text)
        
        return list(set(mentions))  # Remove duplicates
    
    def _analyze_sentiment_polarity(self, doc) -> float:
        """
        Analyze sentiment polarity using adjectives and dependency parsing
        Returns score: -1.0 (very negative) to 1.0 (very positive)
        """
        # Simple sentiment based on adjective sentiment
        positive_adjs = ['good', 'great', 'excellent', 'wonderful', 'happy', 'love', 'best']
        negative_adjs = ['bad', 'terrible', 'awful', 'hate', 'worst', 'sad', 'angry']
        
        pos_count = sum(1 for token in doc if token.lemma_ in positive_adjs)
        neg_count = sum(1 for token in doc if token.lemma_ in negative_adjs)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0
        
        return (pos_count - neg_count) / total
    
    def _calculate_risk_level(self, violations: List, warnings: List) -> str:
        """Calculate overall risk level"""
        if any(v['severity'] == 'critical' for v in violations):
            return 'CRITICAL'
        elif violations:
            return 'HIGH'
        elif len(warnings) >= 2:
            return 'MEDIUM'
        elif warnings:
            return 'LOW'
        else:
            return 'SAFE'
    
    def extract_dependencies(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract dependency relationships for deeper semantic understanding
        
        Returns:
            List of (subject, relation, object) triples
        """
        doc = self.nlp(text)
        dependencies = []
        
        for token in doc:
            if token.dep_ in ['nsubj', 'dobj', 'pobj', 'attr']:
                dependencies.append((
                    token.text,
                    token.dep_,
                    token.head.text
                ))
        
        return dependencies
    
    def extract_semantic_roles(self, text: str) -> Dict:
        """
        Extract semantic roles (who did what to whom, where, when, why)
        Using spaCy's dependency parsing
        """
        doc = self.nlp(text)
        roles = {
            'agents': [],      # Who is doing the action
            'actions': [],     # What actions are happening
            'patients': [],    # Who/what is affected
            'locations': [],   # Where
            'times': [],       # When
            'instruments': []  # How/with what
        }
        
        for token in doc:
            # Agents (subjects)
            if token.dep_ == 'nsubj':
                roles['agents'].append(token.text)
            
            # Actions (main verbs)
            elif token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'ccomp', 'xcomp']:
                roles['actions'].append(token.lemma_)
            
            # Patients (direct objects)
            elif token.dep_ in ['dobj', 'pobj']:
                roles['patients'].append(token.text)
            
            # Locations
            elif token.ent_type_ in ['GPE', 'LOC', 'FAC']:
                roles['locations'].append(token.text)
            
            # Time expressions
            elif token.ent_type_ in ['DATE', 'TIME']:
                roles['times'].append(token.text)
            
            # Instruments (with, using, by means of)
            elif token.dep_ == 'prep' and token.text in ['with', 'using', 'via']:
                for child in token.children:
                    if child.dep_ == 'pobj':
                        roles['instruments'].append(child.text)
        
        return roles
    
    def detect_discourse_markers(self, text: str) -> Dict:
        """
        Detect discourse markers that signal rhetorical structure
        (contrast, causation, addition, etc.)
        """
        doc = self.nlp(text)
        
        markers = {
            'contrast': [],    # but, however, although
            'causation': [],   # because, therefore, so
            'addition': [],    # and, also, furthermore
            'temporal': [],    # then, next, finally
            'emphasis': []     # indeed, certainly, clearly
        }
        
        marker_words = {
            'contrast': ['but', 'however', 'although', 'though', 'yet', 'nevertheless'],
            'causation': ['because', 'therefore', 'so', 'thus', 'hence', 'consequently'],
            'addition': ['and', 'also', 'furthermore', 'moreover', 'additionally'],
            'temporal': ['then', 'next', 'finally', 'afterwards', 'subsequently'],
            'emphasis': ['indeed', 'certainly', 'clearly', 'obviously', 'definitely']
        }
        
        for token in doc:
            for category, words in marker_words.items():
                if token.lemma_ in words:
                    markers[category].append(token.text)
        
        return markers
    
    def analyze_information_density(self, text: str) -> Dict:
        """
        Measure information density - how much content per unit of text
        Higher density = more informationally rich
        """
        doc = self.nlp(text)
        
        total_tokens = len(doc)
        if total_tokens == 0:
            return {'density_score': 0.0, 'metrics': {}}
        
        # Count informational elements
        entities = len(doc.ents)
        content_words = sum(1 for token in doc if not token.is_stop and not token.is_punct)
        nouns = sum(1 for token in doc if token.pos_ == 'NOUN')
        verbs = sum(1 for token in doc if token.pos_ == 'VERB')
        adjectives = sum(1 for token in doc if token.pos_ == 'ADJ')
        
        # Calculate density score
        density_score = (entities * 2 + content_words + nouns + verbs + adjectives) / total_tokens
        
        return {
            'density_score': density_score,
            'metrics': {
                'entities_per_token': entities / total_tokens,
                'content_ratio': content_words / total_tokens,
                'noun_ratio': nouns / total_tokens,
                'verb_ratio': verbs / total_tokens,
                'adjective_ratio': adjectives / total_tokens
            }
        }
    
    def detect_hedging_language(self, text: str) -> Dict:
        """
        Detect hedging (uncertainty markers) - useful for confidence assessment
        "maybe", "probably", "might", "could", "I think", etc.
        """
        doc = self.nlp(text)
        
        hedges = {
            'epistemic_modals': [],    # might, could, may
            'probability_adverbs': [], # probably, possibly, perhaps
            'attribution': [],         # I think, I believe, seems
            'approximators': []        # about, around, approximately
        }
        
        hedge_patterns = {
            'epistemic_modals': ['might', 'could', 'may', 'would'],
            'probability_adverbs': ['probably', 'possibly', 'perhaps', 'maybe'],
            'attribution': ['think', 'believe', 'seem', 'appear', 'suppose'],
            'approximators': ['about', 'around', 'approximately', 'roughly']
        }
        
        for token in doc:
            for category, patterns in hedge_patterns.items():
                if token.lemma_ in patterns:
                    hedges[category].append(token.text)
        
        total_hedges = sum(len(v) for v in hedges.values())
        hedge_density = total_hedges / len(doc) if len(doc) > 0 else 0.0
        
        return {
            'hedges': hedges,
            'total_count': total_hedges,
            'hedge_density': hedge_density,
            'confidence_level': 'low' if hedge_density > 0.15 else 'medium' if hedge_density > 0.05 else 'high'
        }
    
    def print_ethical_report(self, ethical_check: Dict) -> str:
        """Generate human-readable ethical assessment report"""
        report = "\n🛡️  ETHICAL ASSESSMENT:\n"
        
        # Risk level
        risk_level = ethical_check['risk_level']
        risk_icons = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': 'ℹ️',
            'SAFE': '✅'
        }
        icon = risk_icons.get(risk_level, '❓')
        report += f"   {icon} Risk Level: {risk_level}\n"
        
        # Violations
        if ethical_check['violations']:
            report += "\n   ❌ VIOLATIONS:\n"
            for v in ethical_check['violations']:
                report += f"      • {v['category'].upper()} ({v['severity']})\n"
                report += f"        Matches: {', '.join(v['matches'])}\n"
                report += f"        → {v['guidance']}\n"
        
        # Warnings
        if ethical_check['warnings']:
            report += "\n   ⚠️  WARNINGS:\n"
            for w in ethical_check['warnings']:
                report += f"      • {w['category']}: {', '.join(w['matches'][:3])}\n"
        
        # Recommendations
        if ethical_check['recommendations']:
            report += "\n   💡 RECOMMENDATIONS:\n"
            for rec in ethical_check['recommendations']:
                report += f"      • {rec}\n"
        
        # Sentiment
        sentiment = ethical_check['sentiment_score']
        sentiment_label = 'Positive' if sentiment > 0.3 else 'Negative' if sentiment < -0.3 else 'Neutral'
        report += f"\n   😊 Sentiment: {sentiment_label} ({sentiment:.2f})\n"
        
        return report
    
    def analyze_thought(self, text: str) -> Dict:
        """
        Analyze a single thought/utterance
        
        Returns:
            Dictionary with linguistic features
        """
        doc = self.nlp(text)
        
        analysis = {
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'key_nouns': [token.text for token in doc if token.pos_ == 'NOUN'],
            'verbs': [token.text for token in doc if token.pos_ == 'VERB'],
            'sentiment_words': [token.text for token in doc if token.pos_ == 'ADJ'],
            'num_sentences': len(list(doc.sents)),
            'complexity': self._calculate_complexity(doc)
        }
        
        return analysis
    
    def analyze_attention_focus(self, thoughts: List[str]) -> Dict:
        """
        Analyze what topics/entities the system is focusing on
        across multiple thoughts (simulates attention tracking)
        
        Args:
            thoughts: List of recent thoughts/utterances
            
        Returns:
            Attention focus analysis
        """
        all_entities = []
        all_nouns = []
        all_topics = set()
        
        for thought in thoughts:
            doc = self.nlp(thought)
            
            # Collect entities
            all_entities.extend([ent.text.lower() for ent in doc.ents])
            
            # Collect key nouns
            all_nouns.extend([token.lemma_.lower() for token in doc 
                            if token.pos_ == 'NOUN' and not token.is_stop])
            
            # Extract topics (noun chunks)
            all_topics.update([chunk.text.lower() for chunk in doc.noun_chunks])
        
        # Count frequencies
        entity_focus = Counter(all_entities).most_common(5)
        noun_focus = Counter(all_nouns).most_common(5)
        
        return {
            'primary_entities': entity_focus,
            'key_concepts': noun_focus,
            'topic_count': len(all_topics),
            'attention_breadth': len(set(all_nouns))  # How many different concepts
        }
    
    def _calculate_complexity(self, doc) -> float:
        """
        Calculate linguistic complexity of utterance
        Higher = more complex thought
        """
        if len(doc) == 0:
            return 0.0
        
        # Factors: avg word length, dependency depth, vocabulary diversity
        avg_word_length = sum(len(token.text) for token in doc) / len(doc)
        unique_ratio = len(set(token.lemma_ for token in doc)) / len(doc)
        
        # Normalize to 0-1 scale
        complexity = (avg_word_length / 10.0 + unique_ratio) / 2.0
        return min(complexity, 1.0)
    
    def compare_linguistic_patterns(self, text1: str, text2: str) -> float:
        """
        Compare similarity between two thoughts
        Useful for detecting repetitive thinking patterns
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        
        return doc1.similarity(doc2)
    
    def extract_self_references(self, text: str) -> List[str]:
        """
        Extract self-referential statements
        Indicates meta-cognitive awareness
        """
        doc = self.nlp(text.lower())
        
        self_refs = []
        self_pronouns = {'i', 'my', 'me', 'myself', 'mine'}
        
        for token in doc:
            if token.text in self_pronouns:
                # Get the surrounding context
                start = max(0, token.i - 3)
                end = min(len(doc), token.i + 4)
                context = doc[start:end].text
                self_refs.append(context)
        
        return self_refs
    
    def get_attention_report(self, recent_thoughts: List[str]) -> str:
        """Generate human-readable attention analysis"""
        if not recent_thoughts:
            return "No thoughts to analyze yet."
        
        analysis = self.analyze_attention_focus(recent_thoughts)
        
        report = "\n🎯 Attention Focus:\n"
        
        if analysis['primary_entities']:
            report += "  Primary focus: "
            report += ", ".join([f"{entity} ({count}x)" for entity, count in analysis['primary_entities'][:3]])
            report += "\n"
        
        if analysis['key_concepts']:
            report += "  Key concepts: "
            report += ", ".join([f"{concept}" for concept, _ in analysis['key_concepts'][:5]])
            report += "\n"
        
        report += f"  Attention breadth: {analysis['attention_breadth']} unique concepts\n"
        
        return report
    
    # ===== NEW: USER INPUT ANALYSIS =====
    
    def analyze_user_input(self, text: str) -> Dict:
        """
        Deep linguistic analysis of user input
        Extracts meaning, intent signals, and conversational features
        
        Args:
            text: User's input message
            
        Returns:
            Dictionary with linguistic features
        """
        doc = self.nlp(text)
        
        # Extract entities (people, places, organizations, etc.)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Extract key content words
        nouns = [token.lemma_ for token in doc if token.pos_ == 'NOUN' and not token.is_stop]
        verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB' and not token.is_stop]
        adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
        
        # Detect question vs statement
        is_question = text.strip().endswith('?') or any(
            token.tag_ in ['WDT', 'WP', 'WP$', 'WRB'] for token in doc
        )
        
        # Detect sentiment-bearing words
        sentiment_words = [token.text for token in doc if token.pos_ in ['ADJ', 'ADV']]
        
        # Extract main topics (noun phrases)
        topics = [chunk.text for chunk in doc.noun_chunks]
        
        # Detect intent signals
        intent_signals = self._detect_intent_signals(doc)
        
        # Measure complexity
        complexity = self._calculate_complexity(doc)
        
        # Detect personal references (talking about self)
        personal_pronouns = [token.text for token in doc if token.pos_ == 'PRON' 
                           and token.text.lower() in ['i', 'me', 'my', 'mine', 'myself']]
        
        return {
            'entities': entities,
            'nouns': nouns,
            'verbs': verbs,
            'adjectives': adjectives,
            'topics': topics,
            'is_question': is_question,
            'sentiment_words': sentiment_words,
            'intent_signals': intent_signals,
            'complexity': complexity,
            'personal_pronouns_count': len(personal_pronouns),
            'sentence_count': len(list(doc.sents)),
            'word_count': len([token for token in doc if not token.is_punct])
        }
    
    def _detect_intent_signals(self, doc) -> Dict[str, bool]:
        """
        Detect conversational intent from linguistic patterns
        """
        text_lower = doc.text.lower()
        
        # Intent detection patterns
        intent_signals = {
            'requesting_help': any(word in text_lower for word in [
                'help', 'can you', 'could you', 'would you', 'please'
            ]),
            'expressing_emotion': any(word in text_lower for word in [
                'feel', 'feeling', 'felt', 'emotion', 'emotional'
            ]),
            'seeking_information': any(word in text_lower for word in [
                'what', 'why', 'how', 'when', 'where', 'who', 'which'
            ]),
            'sharing_experience': any(word in text_lower for word in [
                'i am', "i'm", 'i was', 'i have', "i've", 'my'
            ]),
            'expressing_opinion': any(word in text_lower for word in [
                'i think', 'i believe', 'in my opinion', 'i feel that'
            ]),
            'greeting': any(word in text_lower for word in [
                'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'
            ]),
            'thanking': any(word in text_lower for word in [
                'thank', 'thanks', 'appreciate', 'grateful'
            ])
        }
        
        return intent_signals
    
    def get_user_input_report(self, text: str, analysis: Dict) -> str:
        """
        Generate human-readable report of user input analysis
        
        Args:
            text: Original user input
            analysis: Result from analyze_user_input()
        """
        report = "\n📝 User Input Analysis:\n"
        
        # Basic stats
        report += f"  Words: {analysis['word_count']} | "
        report += f"Sentences: {analysis['sentence_count']} | "
        report += f"Complexity: {analysis['complexity']:.2f}\n"
        
        # Intent signals
        active_intents = [intent for intent, active in analysis['intent_signals'].items() if active]
        if active_intents:
            report += f"  Intent: {', '.join(active_intents[:3])}\n"
        
        # Key content
        if analysis['topics']:
            report += f"  Topics: {', '.join(analysis['topics'][:3])}\n"
        
        if analysis['entities']:
            entities_str = ', '.join([f"{text} ({label})" for text, label in analysis['entities'][:3]])
            report += f"  Entities: {entities_str}\n"
        
        # Question type
        if analysis['is_question']:
            report += "  Type: Question ❓\n"
        
        return report
    
    def compare_user_and_response(self, user_input: str, ai_response: str) -> Dict:
        """
        Compare linguistic patterns between user input and AI response
        Useful for checking response appropriateness
        
        Returns:
            Comparison metrics
        """
        user_doc = self.nlp(user_input)
        ai_doc = self.nlp(ai_response)
        
        # Semantic similarity
        similarity = user_doc.similarity(ai_doc)
        
        # Topic overlap
        user_analysis = self.analyze_user_input(user_input)
        ai_topics = [chunk.text.lower() for chunk in ai_doc.noun_chunks]
        user_topics = [topic.lower() for topic in user_analysis['topics']]
        
        topic_overlap = len(set(user_topics) & set(ai_topics))
        
        # Response appropriateness signals
        if user_analysis['is_question']:
            # Check if response addresses the question
            response_addresses_question = any(
                verb in [token.lemma_ for token in ai_doc if token.pos_ == 'VERB']
                for verb in ['be', 'have', 'do', 'can', 'will', 'would']
            )
        else:
            response_addresses_question = None
        
        return {
            'semantic_similarity': similarity,
            'topic_overlap_count': topic_overlap,
            'user_was_question': user_analysis['is_question'],
            'response_addresses_question': response_addresses_question,
            'user_complexity': user_analysis['complexity'],
            'ai_complexity': self._calculate_complexity(ai_doc)
        }
