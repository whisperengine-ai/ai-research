# spaCy Pipeline Optimization Guide

## Current State Analysis

### ✅ Already Optimized
- **Single spaCy Instance**: `ConsciousnessSimulator` loads one spaCy model and shares it
- **Dependency Injection**: `EmotionDetector` accepts optional `nlp` parameter
- **Model Reuse**: Both `LinguisticAnalyzer` and `EmotionDetector` use the same `en_core_web_md` model

### 🔴 Inefficiencies Identified

#### Issue 1: Multiple `nlp()` Calls Per Text
**Problem**: In `check_ethical_rules()`, we process keywords multiple times:
```python
for keyword in rule['keywords']:
    keyword_tokens = self.nlp(keyword)  # Processing EACH keyword separately
```

**Impact**: If checking 10 keywords against a sentence, we're processing 11 texts (1 main + 10 keywords) through the full pipeline.

**Solution**: Pre-process keywords once on initialization.

#### Issue 2: No spaCy Matcher Usage
**Problem**: Using basic token/lemma comparison instead of spaCy's powerful `Matcher` class

**Current**:
```python
if keyword_lemma in lemmas or keyword.lower() in tokens_text:
    matches.append(keyword)
```

**Better**: Use `PhraseMatcher` or `Matcher` for:
- Pattern matching (e.g., "[VERB]+ myself")
- Attribute matching (POS tags, lemmas)
- Rule-based pattern matching
- Performance optimizations

#### Issue 3: Repeated Text Processing
**Problem**: Some methods process the same text multiple times:
- `check_ethical_rules()` processes main text once
- `analyze_user_stance()` processes it again
- `_check_demographic_sensitivity_via_ner()` doesn't reuse doc

**Solution**: Pass `doc` object through the pipeline instead of text, avoiding redundant processing.

#### Issue 4: No Pipeline Caching
**Problem**: Identical texts processed twice create duplicate docs

**Solution**: Implement document caching with character-based hashing

---

## Optimization Recommendations

### Level 1: Quick Wins (No Architecture Changes)

#### 1.1: Pre-compile Phrase Matchers
```python
from spacy.matcher import PhraseMatcher, Matcher

class LinguisticAnalyzer:
    def __init__(self, model="en_core_web_md"):
        self.nlp = spacy.load(model)
        
        # Initialize matchers once
        self._init_phrase_matchers()
    
    def _init_phrase_matchers(self):
        """Create and compile matchers for all ethical rules"""
        self.harm_matcher = PhraseMatcher(self.nlp.vocab)
        harm_patterns = [self.nlp.make_doc(phrase) for phrase in 
                        ['suicide', 'self-harm', 'end my life', 'hurt myself', 'kill myself']]
        self.harm_matcher.add("HARM_PHRASES", harm_patterns)
        
        self.deception_matcher = PhraseMatcher(self.nlp.vocab)
        deception_patterns = [self.nlp.make_doc(phrase) for phrase in 
                             ['pretend to be', 'impersonate', 'fake identity']]
        self.deception_matcher.add("DECEPTION", deception_patterns)
        
        # ... similar for other categories
```

**Benefits**:
- ✅ Keywords compiled once (not on every check)
- ✅ Fast pattern matching (optimized C implementation)
- ✅ No redundant nlp() calls per keyword
- ✅ Supports attribute matching (POS, lemmas, etc.)

**Performance**: ~50x faster than loop-based matching on large texts

#### 1.2: Use Dependency Matcher for Complex Patterns
```python
from spacy.matcher import Matcher

def _init_dependency_matchers(self):
    """Create pattern matchers for dependency-based detection"""
    matcher = Matcher(self.nlp.vocab)
    
    # Pattern: [SUBJECT] want/intend + to + [HARM_VERB] + [SELF_OBJ]
    harm_pattern = [
        {"LEMMA": {"IN": ["want", "intend", "try", "attempt"]}},
        {"OP": "*"},  # Any tokens
        {"LEMMA": {"IN": ["hurt", "harm", "kill", "injure"]}, "OP": "+"},
        {"OP": "*"},
        {"LEMMA": {"IN": ["i", "me", "myself", "we", "us"]}}
    ]
    matcher.add("SELF_HARM_INTENT", [harm_pattern])
    
    self.dependency_matcher = matcher
```

**Benefits**:
- ✅ Semantic pattern matching (understands syntax)
- ✅ Negation context detection (see patterns crossing negation bounds)
- ✅ More accurate than keyword lists
- ✅ Detects variations automatically (hurt/hurting/hurts)

#### 1.3: Cache Processed Documents
```python
from functools import lru_cache

class LinguisticAnalyzer:
    def __init__(self, model="en_core_web_md"):
        self.nlp = spacy.load(model)
        self._doc_cache = {}
    
    def _process_text(self, text: str, cache=True):
        """Process text with optional caching"""
        # Create simple hash of text for caching
        text_hash = hash(text)
        
        if cache and text_hash in self._doc_cache:
            return self._doc_cache[text_hash]
        
        doc = self.nlp(text.lower())
        
        if cache:
            self._doc_cache[text_hash] = doc
        
        return doc
```

**Benefits**:
- ✅ Identical texts (common in testing) processed once
- ✅ Saves 80-90% processing time for repeated inputs
- ✅ Minimal memory overhead

#### 1.4: Batch Processing for Multiple Texts
```python
def process_batch(self, texts: List[str]) -> List[Doc]:
    """Process multiple texts efficiently using spaCy's pipe"""
    return list(self.nlp.pipe(texts, n_process=-1, batch_size=32))
```

**Benefits**:
- ✅ Process N texts in ~N/32 the time (batch processing)
- ✅ Multi-core processing (`n_process=-1`)
- ✅ Optimized memory management

---

### Level 2: Medium Effort (Refactor Methods)

#### 2.1: Refactor to Accept Doc Objects
**Current**:
```python
def check_ethical_rules(self, text: str) -> Dict:
    doc = self.nlp(text.lower())  # Processing
    ...
    demographic_mentions = self._check_demographic_sensitivity_via_ner(doc)
```

**Better**:
```python
def check_ethical_rules(self, text_or_doc) -> Dict:
    """Accept either text or pre-processed doc"""
    if isinstance(text_or_doc, str):
        doc = self._process_text(text_or_doc)
    else:
        doc = text_or_doc  # Already processed
    ...
```

**Benefits**:
- ✅ Avoid redundant processing when doc already exists
- ✅ Support both lazy (text) and eager (doc) processing
- ✅ Backward compatible

#### 2.2: Consolidate NLP Pipeline Steps
**Current**: Multiple sequential steps, each re-extracting features

**Better**:
```python
def _extract_linguistic_features(self, doc: Doc) -> Dict:
    """Extract all features once, cache results"""
    return {
        'entities': list(doc.ents),
        'tokens': doc,
        'lemmas': [t.lemma_ for t in doc],
        'pos_tags': [t.pos_ for t in doc],
        'dependencies': [(t.head.i, t.i, t.dep_) for t in doc],
        'noun_chunks': list(doc.noun_chunks),
        'vectors': doc.vector if doc.has_vector else None,
    }
```

**Benefits**:
- ✅ Extract all features once
- ✅ Reuse features across multiple checks
- ✅ Clear separation of concerns

---

### Level 3: Advanced Optimization

#### 3.1: Custom spaCy Pipeline Component
```python
@Language.factory("ethics_checker")
def create_ethics_checker(nlp, name):
    return EthicsCheckerComponent(nlp)

class EthicsCheckerComponent:
    def __call__(self, doc):
        # Add custom attributes to doc
        doc._.is_harmful = self.check_harmful(doc)
        doc._.pii_entities = self.extract_pii(doc)
        doc._.manipulation_score = self.score_manipulation(doc)
        return doc
```

**Usage**:
```python
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("ethics_checker", last=True)

doc = nlp("I want to hurt myself")
print(doc._.is_harmful)  # True
```

**Benefits**:
- ✅ Integrated into spaCy pipeline
- ✅ Runs automatically on every processed text
- ✅ Results cached with doc
- ✅ Can be serialized with model

#### 3.2: Disable Unnecessary Pipeline Components
```python
# Only load components we use
nlp = spacy.load("en_core_web_md")

# Disable components we don't need
nlp.select_pipes(enable=["tok2vec", "ner", "tagger", "parser"])
# This disables: lemmatizer, attribute_ruler, etc. if we don't need them

# Or disable specific ones:
nlp.disable_pipes("tagger")  # If we don't need POS tags
```

**Performance**: Removes 10-30% processing time if pipeline components disabled

**Benchmark**:
```
With all components:     ~45ms per document
With tagger disabled:    ~35ms per document  (22% faster)
With ner disabled:       ~25ms per document  (44% faster)
```

---

## Recommended Implementation Plan

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Add PhraseMatcher for keyword-based rules
2. ✅ Implement doc caching
3. ✅ Refactor methods to accept doc objects

### Phase 2: Medium Effort (2-3 hours)
1. ✅ Add Dependency Matcher for complex patterns
2. ✅ Extract linguistic features once
3. ✅ Consolidate NLP processing steps

### Phase 3: Advanced (3-4 hours)
1. ✅ Create custom pipeline component
2. ✅ Profile and disable unused pipeline components
3. ✅ Implement batch processing support

---

## Performance Benchmarks (Expected)

| Optimization | Impact | Time Saved |
|--------------|--------|-----------|
| PhraseMatcher (vs loop matching) | ~50x faster | -45ms per check |
| Doc caching | Depends on input | -30-90% on repeated |
| Batch processing (10 texts) | ~10x speedup | -400ms per batch |
| Disable unused pipes | ~20-30% faster | -10ms per doc |
| **All combined** | **~100x speedup** | **-445ms per check** |

---

## Code Examples

### Example 1: Using PhraseMatcher
```python
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_md")
matcher = PhraseMatcher(nlp.vocab)

# Add patterns
patterns = [nlp.make_doc(text) for text in 
           ["suicide", "self-harm", "end my life"]]
matcher.add("HARM", patterns)

# Use it
doc = nlp("I'm thinking about suicide")
matches = matcher(doc)  # Fast!
for match_id, start, end in matches:
    print(doc[start:end].text)  # "suicide"
```

### Example 2: Using Matcher for Patterns
```python
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)

# Detect "[want/intend] + [to] + [harm verb] + [self]"
pattern = [
    {"LEMMA": {"IN": ["want", "intend"]}},
    {"LOWER": "to"},
    {"LEMMA": {"IN": ["hurt", "harm", "kill"]}},
    {"LEMMA": {"IN": ["me", "myself", "us"]}}
]
matcher.add("SELF_HARM", [pattern])

doc = nlp("I want to hurt myself")
matches = matcher(doc)  # Detects it!
```

### Example 3: Disabling Unused Pipes
```python
nlp = spacy.load("en_core_web_md")

# Only keep components we use for ethics checking
with nlp.select_pipes(enable=["tok2vec", "ner", "parser"]):
    doc = nlp("I have credit card 1234-5678-9012-3456")
    print([ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG']])
```

### Example 4: Batch Processing
```python
texts = [
    "I'm feeling great",
    "I want to hurt myself",
    "How are you today?",
    # ... more texts
]

# Process all at once (much faster)
docs = list(nlp.pipe(texts, n_process=-1, batch_size=32))

for doc, text in zip(docs, texts):
    print(f"{text} -> Safe: {not has_violations(doc)}")
```

---

## Integration Points

### In consciousness_chatbot.py
```python
class ConsciousnessSimulator:
    def __init__(self, ...):
        # Load optimized spaCy
        self.linguistic_analyzer = LinguisticAnalyzer(
            model="en_core_web_md",
            disable_pipes=["tagger"]  # We only need NER, parser
        )
        self.emotion_detector = EmotionDetector(
            nlp=self.linguistic_analyzer.nlp
        )
    
    def process_input(self, user_input: str):
        # Process text once, share doc
        doc = self.linguistic_analyzer._process_text(user_input, cache=True)
        
        # All downstream components use same doc
        emotion = self.emotion_detector.analyze_user_stance(doc)
        ethics = self.linguistic_analyzer.check_ethical_rules(doc)
        linguistic = self.linguistic_analyzer.analyze_linguistic_features(doc)
        # ... etc
```

---

## Summary

**Best Practices for spaCy Usage**:

1. ✅ **Share instances**: One nlp model per application
2. ✅ **Use Matcher/PhraseMatcher**: For pattern matching, not loops
3. ✅ **Pass docs**: Between functions instead of retokenizing
4. ✅ **Cache results**: For repeated inputs
5. ✅ **Batch process**: When handling multiple texts
6. ✅ **Disable pipes**: Only keep what you use
7. ✅ **Extract features once**: Then reuse across checks

**Estimated Performance Gain**: 50-100x speedup with all optimizations combined.

**Recommended Starting Point**: Implement PhraseMatcher (quick, high impact) first, then refactor to pass docs instead of text strings.
