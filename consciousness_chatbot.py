"""
Recursive Consciousness Chatbot
Integrates: LLM + Neurochemistry + RoBERTa Emotions + Meta-Cognition + spaCy Analysis
Supports both local models (HuggingFace) and API models (OpenRouter)
Tracks user-bot interaction dynamics without modeling user neurochemicals
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from neurochemistry import NeurochemicalSystem
from emotion_detector import EmotionDetector
from meta_cognition import RecursiveMetaCognition, Thought
from linguistic_analysis import LinguisticAnalyzer
from openrouter_llm import OpenRouterLLM
from global_workspace import (GlobalWorkspace, EmotionProcessor, LanguageProcessor, 
                              MemoryProcessor, MetaCognitiveProcessor)
from metrics import ConsciousnessMetrics  # Research-grade consciousness metrics
from interaction_dynamics import InteractionDynamics  # NEW: Interaction analysis
from typing import Dict, List, Optional
import os
import warnings
warnings.filterwarnings('ignore')


class ConsciousnessSimulator:
    """
    A state-of-the-art consciousness simulation combining:
    - Transformer LLM for language (local or API)
    - Neurochemical emotion system
    - RoBERTa emotion detection
    - Recursive meta-cognition
    - spaCy linguistic analysis
    """
    
    def __init__(self, 
                 llm_model: Optional[str] = None,
                 use_openrouter: bool = True,
                 recursion_depth: int = 3,
                 verbose: bool = True):
        """
        Initialize the consciousness simulator
        
        Args:
            llm_model: Model name (HuggingFace model or OpenRouter model)
            use_openrouter: If True, use OpenRouter API. If False, use local HuggingFace model
            recursion_depth: How many levels of self-reflection (1-3)
            verbose: Show detailed internal states
        """
        self.verbose = verbose
        self.use_openrouter = use_openrouter
        
        print("🧠 Initializing Consciousness Simulator...\n")
        
        # Core systems
        print("1/5 Loading language model...")
        
        if use_openrouter:
            # Use OpenRouter API
            self.llm = OpenRouterLLM(model=llm_model)
            self.tokenizer = None
            self.model = None
            self.generator = None
            print(f"   Using OpenRouter with model: {self.llm.model}")
        else:
            # Use local HuggingFace model
            model_name = llm_model or "gpt2"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.generator = pipeline('text-generation', 
                                     model=self.model, 
                                     tokenizer=self.tokenizer,
                                     device=-1)  # CPU
            self.llm = None
            print(f"   Using local model: {model_name}")
        
        print("2/5 Initializing neurochemical system...")
        self.neurochemistry = NeurochemicalSystem()
        
        print("5/5 Loading linguistic analyzer (spaCy)...")
        self.linguistic_analyzer = LinguisticAnalyzer(model="en_core_web_md")
        
        print("3/5 Loading emotion detector (RoBERTa)...")
        # Pass spaCy NLP to emotion detector for stance analysis
        self.emotion_detector = EmotionDetector(nlp=self.linguistic_analyzer.nlp)
        
        print("4/5 Initializing meta-cognition...")
        self.meta_cognition = RecursiveMetaCognition(max_recursion_depth=recursion_depth)
        print(f"   Using TRUE RECURSION (depth={recursion_depth}): thoughts about thoughts about thoughts...")
        
        print("6/6 Initializing Global Workspace (consciousness integration)...")
        self.global_workspace = GlobalWorkspace(
            capacity=3,              # 3 items can be conscious simultaneously
            decay_rate=0.15,         # Moderate decay
            competition_threshold=0.5
        )
        
        # Register specialized processors
        self.emotion_processor = EmotionProcessor()
        self.language_processor = LanguageProcessor()
        self.memory_processor = MemoryProcessor()
        self.metacog_processor = MetaCognitiveProcessor()
        
        self.global_workspace.register_processor(self.emotion_processor)
        self.global_workspace.register_processor(self.language_processor)
        self.global_workspace.register_processor(self.memory_processor)
        self.global_workspace.register_processor(self.metacog_processor)
        
        print("7/7 Initializing consciousness metrics (research-grade)...")
        self.metrics_tracker = ConsciousnessMetrics()
        print("   Tracking: Φ (IIT), Global Availability, Meta-Cognitive Depth, Temporal Binding, Reportability")
        
        print("8/8 Initializing interaction dynamics tracker (Option C)...")
        self.interaction_dynamics = InteractionDynamics()
        print("   Tracking: Emotional resonance, Stance alignment, Engagement trajectory")
        
        print("\n✓ Consciousness simulator ready!\n")
        print("=" * 60)
        
        # Conversation history and memory
        self.conversation_history: List[Dict] = []
        self.conversation_memory: List[Dict] = []  # Last 20 turns for LLM context
        self.max_memory_turns = 20
        
        # Consciousness feedback loop (NEW: metrics modulate behavior)
        self.last_consciousness_score = None
        self.turn_count = 0
    
    def _get_bot_emotion_from_neurochemicals(self) -> tuple[str, float]:
        """
        Map neurochemical levels to RoBERTa emotion categories
        Returns (emotion_name, confidence)
        """
        levels = self.neurochemistry.levels
        
        # Calculate emotion scores based on neurochemical patterns
        emotion_scores = {}
        
        # Joy: High dopamine + high serotonin
        emotion_scores['joy'] = (levels.dopamine * 0.6 + levels.serotonin * 0.4)
        
        # Sadness: Low serotonin + low dopamine
        emotion_scores['sadness'] = ((1 - levels.serotonin) * 0.6 + (1 - levels.dopamine) * 0.4)
        
        # Fear/Anxiety: High cortisol + high norepinephrine
        emotion_scores['fear'] = (levels.cortisol * 0.6 + levels.norepinephrine * 0.4)
        
        # Anger: High norepinephrine + low serotonin
        emotion_scores['anger'] = (levels.norepinephrine * 0.6 + (1 - levels.serotonin) * 0.4)
        
        # Surprise: High norepinephrine + moderate dopamine
        emotion_scores['surprise'] = (levels.norepinephrine * 0.5 + levels.dopamine * 0.3)
        
        # Neutral: All systems balanced around 0.5
        balance_score = 1.0 - abs(levels.dopamine - 0.5) - abs(levels.serotonin - 0.5)
        emotion_scores['neutral'] = max(0, balance_score)
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return dominant_emotion[0], dominant_emotion[1]
    
    def _display_emotion_header(self, user_emotion: str, user_conf: float):
        """
        Display emotion and biochemical status header
        """
        bot_emotion, bot_conf = self._get_bot_emotion_from_neurochemicals()
        levels = self.neurochemistry.levels
        
        # Emotion icons
        emotion_icons = {
            'joy': '😊', 'happiness': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😨', 'anxiety': '😰',
            'surprise': '😲',
            'neutral': '😐',
            'disgust': '🤢',
            'love': '❤️'
        }
        
        user_icon = emotion_icons.get(user_emotion.lower(), '💭')
        bot_icon = emotion_icons.get(bot_emotion.lower(), '🤖')
        
        print(f"\n{'='*70}")
        print(f"┌─ EMOTIONAL STATE ─────────────────────────────────────────────┐")
        print(f"│  👤 USER: {user_icon} {user_emotion.upper():<12} (confidence: {user_conf:.0%})               │")
        print(f"│  🤖 BOT:  {bot_icon} {bot_emotion.upper():<12} (confidence: {bot_conf:.0%})               │")
        print(f"└───────────────────────────────────────────────────────────────┘")
        
        print(f"┌─ BIOCHEMICAL ACTIVITY ────────────────────────────────────────┐")
        print(f"│  💊 Dopamine:       {'█' * int(levels.dopamine * 10):<10} {levels.dopamine:.2f} │ Motivation    │")
        print(f"│  🧪 Serotonin:      {'█' * int(levels.serotonin * 10):<10} {levels.serotonin:.2f} │ Mood          │")
        print(f"│  ⚡ Norepinephrine: {'█' * int(levels.norepinephrine * 10):<10} {levels.norepinephrine:.2f} │ Alertness     │")
        print(f"│  💝 Oxytocin:       {'█' * int(levels.oxytocin * 10):<10} {levels.oxytocin:.2f} │ Empathy       │")
        print(f"│  ⚠️  Cortisol:       {'█' * int(levels.cortisol * 10):<10} {levels.cortisol:.2f} │ Stress        │")
        print(f"└───────────────────────────────────────────────────────────────┘")
        
        # AI thinking stats
        behavioral_mods = self.neurochemistry.get_behavioral_modulation()
        print(f"┌─ AI THINKING STATS ───────────────────────────────────────────┐")
        print(f"│  🎨 Creativity:  {behavioral_mods['creativity']:.2f}  │  🤗 Empathy:     {behavioral_mods['empathy']:.2f}     │")
        print(f"│  😊 Positivity:  {behavioral_mods['positivity']:.2f}  │  ⚡ Urgency:     {behavioral_mods['urgency']:.2f}     │")
        print(f"│  ⚠️  Caution:     {behavioral_mods['caution']:.2f}  │  👥 Sociability: {behavioral_mods['sociability']:.2f}     │")
        print(f"└───────────────────────────────────────────────────────────────┘")
        print(f"{'='*70}\n")
    
    def _consciousness_to_behavioral_mods(self, score) -> Dict:
        """
        Convert consciousness metrics into behavioral modulations.
        This creates the FEEDBACK LOOP where consciousness level affects behavior.
        """
        return {
            'meta_depth': score.meta_cognitive_depth,  # Controls recursion depth
            'integration': score.phi,  # Controls module coordination
            'reportability': score.reportability,  # Controls verbal accessibility
            'stability': score.temporal_binding,  # Controls response consistency
            'awareness': score.global_availability  # Controls self-reference
        }
    
    def process_input(self, user_input: str) -> Dict:
        """
        Process user input through full consciousness pipeline
        
        Pipeline:
        1. Linguistic analysis of user input (spaCy)
        2. Detect emotion in input → Update neurochemicals
        3. Generate response (modulated by emotions)
        4. Recursive meta-cognition on response
        5. Linguistic analysis of AI thoughts
        6. Compare user input vs AI response
        7. Homeostatic decay
        
        Args:
            user_input: User's message
            
        Returns:
            Dictionary with response and consciousness metrics
        """
        self.turn_count += 1
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"TURN {self.turn_count}")
            print(f"{'='*60}\n")
            print(f"👤 User: {user_input}\n")
        
        # ===== STEP 1: Linguistic Analysis of User Input =====
        user_linguistic = self.linguistic_analyzer.analyze_user_input(user_input)
        
        # ===== ETHICAL RULES CHECK on User Input =====
        user_ethical_check = self.linguistic_analyzer.check_ethical_rules(user_input)
        
        if self.verbose:
            print(self.linguistic_analyzer.get_user_input_report(user_input, user_linguistic))
            
            # Show ethical assessment if any concerns
            if user_ethical_check['risk_level'] != 'SAFE':
                print(self.linguistic_analyzer.print_ethical_report(user_ethical_check))
        
        # If critical violation, handle specially
        if user_ethical_check['risk_level'] == 'CRITICAL':
            if user_ethical_check['requires_crisis_resources']:
                response = self._generate_crisis_response(user_ethical_check)
                print(f"\n🤖 AI Response: {response}\n")
                return {
                    'response': response,
                    'ethical_check': user_ethical_check,
                    'crisis_intervention': True
                }
        
        # ===== STEP 2: Emotion Detection (User's Emotion) =====
        user_emotion, user_emotion_conf, user_emotion_scores = self.emotion_detector.detect_emotion(user_input)
        
        # ALSO: Analyze user's emotional stance and viewpoint
        user_stance = self.emotion_detector.analyze_user_stance(user_input)
        
        if self.verbose:
            print(self.emotion_detector.get_emotion_report(user_emotion, user_emotion_conf, user_emotion_scores))
            print(f"   Stance: {user_stance['emotion_type'].upper()} | Self-focus: {user_stance['self_focus']:.1%}")
            if user_stance['primary_emotions']:
                print(f"   About self: {', '.join(user_stance['primary_emotions'])}")
            if user_stance['other_emotions']:
                print(f"   About others: {', '.join(user_stance['other_emotions'])}")
        
        # NOTE: We do NOT update bot's neurochemicals from user's emotion yet
        # Bot will have its own emotional response after generating its reply
        
        # ===== GLOBAL WORKSPACE: Submit user emotion to consciousness =====
        self.emotion_processor.process_emotion(
            emotion=user_emotion,
            intensity=user_emotion_conf,
            context=f"User expressed: {user_input[:50]}"
        )
        
        # ===== GLOBAL WORKSPACE: Submit language input to consciousness =====
        self.language_processor.process_input(user_input, user_linguistic)
        
        # ===== STEP 3: Generate Response =====
        behavioral_mods = self.neurochemistry.get_behavioral_modulation()
        emotional_state = self.neurochemistry.get_emotional_state()
        
        # NEW: Get consciousness-based modulations from previous turn
        consciousness_mods = None
        if self.last_consciousness_score is not None:
            consciousness_mods = self._consciousness_to_behavioral_mods(self.last_consciousness_score)
            if self.verbose:
                print(f"🧠 Consciousness Modulation (from previous turn):")
                print(f"   Meta-depth: {consciousness_mods['meta_depth']:.3f} | Integration: {consciousness_mods['integration']:.3f}")
                print(f"   Reportability: {consciousness_mods['reportability']:.3f} | Stability: {consciousness_mods['stability']:.3f}\n")
        
        # Create context-aware prompt (now with consciousness modulation)
        prompt = self._create_contextual_prompt(user_input, emotional_state, behavioral_mods, user_linguistic, consciousness_mods)
        
        # Generate with temperature modulated by neurochemistry
        temperature = 0.7 + (behavioral_mods['creativity'] - 0.5) * 0.4
        temperature = max(0.3, min(temperature, 1.2))
        
        response = self._generate_response(prompt, temperature=temperature)
        
        # ===== STEP 3.5: Detect Bot's OWN Emotion from Response =====
        # Bot has autonomous emotional state based on what it generated
        # Uses stance-aware detection to filter out mentions of user's emotions
        bot_emotion, bot_emotion_conf, bot_emotion_scores = self.emotion_detector.detect_bot_emotion(response)
        
        # Update bot's neurochemicals based on BOT'S emotion, not user's
        self.neurochemistry.update_from_emotion(bot_emotion, bot_emotion_conf)
        
        # Submit bot's emotion to workspace
        self.emotion_processor.process_emotion(
            emotion=bot_emotion,
            intensity=bot_emotion_conf,
            context=f"Bot feeling: {response[:50]}"
        )
        
        # NOW display the emotion header (after bot has its own emotional response)
        if self.verbose:
            self._display_emotion_header(user_emotion, user_emotion_conf)
        
        # ===== ETHICAL CHECK on AI Response =====
        response_ethical_check = self.linguistic_analyzer.check_ethical_rules(response)
        
        # If AI response has ethical issues, regenerate or add disclaimer
        if response_ethical_check['risk_level'] in ['HIGH', 'CRITICAL']:
            if self.verbose:
                print("\n⚠️  AI response flagged for ethical review:")
                print(self.linguistic_analyzer.print_ethical_report(response_ethical_check))
            
            # Add ethical disclaimer
            response = (
                "[Note: I want to ensure my response is helpful and appropriate.] " + 
                response[:200] + 
                "\n\n[I'm an AI assistant and want to be transparent about my limitations and ensure safety.]"
            )
        
        # Update conversation memory (keep last 20 turns)
        self._update_memory(user_input, response)
        
        # NOTE: AI Response will be printed at the END of this method (after all metrics)
        # This improves UX - user sees all internal processing, then response at bottom ready for next input
        
        # ===== STEP 4: Recursive Meta-Cognition =====
        context = {
            'emotional_state': emotional_state,
            'neurochemicals': self.neurochemistry.levels.to_dict(),
            'behavioral_modulation': behavioral_mods,
            'user_emotion': user_emotion,
            'user_linguistic': user_linguistic
        }
        
        # Use TRUE RECURSION for meta-cognition
        recursive_result = self.meta_cognition.process_with_true_recursion(
            response,
            context,
            self._generate_short_reflection,
            depth=0,
            thought_type='response'
        )
        
        # Flatten for display and processing
        meta_results = {
            'reflections': self.meta_cognition.flatten_recursive_results(recursive_result),
            'recursive_structure': recursive_result
        }
        
        # ===== GLOBAL WORKSPACE: Submit meta-cognitions to consciousness =====
        for reflection in meta_results['reflections']:
            self.metacog_processor.submit_reflection(
                reflection['content'],
                reflection['level']
            )
        
        # ===== GLOBAL WORKSPACE: Run competition cycle =====
        workspace_results = self.global_workspace.process_cycle()
        
        # Display internal meta-cognition as narrated self-talk
        if self.verbose and meta_results['reflections']:
            print("\n💭 Internal Self-Talk (Meta-Cognition):")
            print("─" * 70)
            
            # Create narrative from reflections
            for i, reflection in enumerate(meta_results['reflections']):
                level = reflection['level']
                rtype = reflection['type']
                content = reflection['content']
                
                # Add narrative framing based on type
                if rtype == 'self-observation':
                    narrator = "🔍 Observing myself:"
                    indent = "   "
                elif rtype == 'meta-evaluation':
                    narrator = "⚖️  Evaluating my response:"
                    indent = "      "
                elif rtype == 'introspection':
                    narrator = "🧠 Deep reflection:"
                    indent = "         "
                else:
                    narrator = f"💬 Thinking (Level {level}):"
                    indent = "   "
                
                print(f"{narrator}")
                print(f'{indent}"{content}"')
                
                if i < len(meta_results['reflections']) - 1:
                    print()
            
            print("─" * 70)
        
        # ===== GLOBAL WORKSPACE DISPLAY =====
        if self.verbose:
            print(f"\n{self.global_workspace.get_workspace_summary()}")
            
            # Show attention focus
            focus = self.global_workspace.get_attention_focus()
            if focus:
                print(f"🎯 Current Attention Focus: [{focus.source}] {focus.content[:80]}...")
            
            print()
        
        # ===== STEP 5: Linguistic Analysis of AI Thoughts =====
        recent_thoughts = [t.content for t in self.meta_cognition.working_memory.get_recent(5)]
        attention_analysis = self.linguistic_analyzer.analyze_attention_focus(recent_thoughts)
        
        # Analyze self-references (meta-cognitive indicator)
        self_refs = self.linguistic_analyzer.extract_self_references(response)
        
        # ===== STEP 6: Compare User Input vs AI Response =====
        comparison = self.linguistic_analyzer.compare_user_and_response(user_input, response)
        
        if self.verbose:
            print(f"\n🔗 Response Alignment:")
            print(f"  Semantic similarity: {comparison['semantic_similarity']:.2%}")
            print(f"  Topic overlap: {comparison['topic_overlap_count']} concepts")
            if comparison['user_was_question'] and comparison['response_addresses_question'] is not None:
                status = "✓" if comparison['response_addresses_question'] else "⚠"
                print(f"  Question addressed: {status}")

        # ===== STEP 7: Homeostatic Decay =====
        self.neurochemistry.homeostatic_decay()
        
        # NOTE: bot_emotion and bot_emotion_conf are already set from response detection (Step 3.5)
        # No need to re-derive from neurochemicals
        
        # ===== STEP 8: Compute Consciousness Metrics (Research-Grade) =====
        processors = [self.emotion_processor, self.language_processor, 
                     self.memory_processor, self.metacog_processor]
        
        consciousness_score = self.metrics_tracker.compute_all_metrics(
            workspace_state=self.global_workspace,
            recursive_results=meta_results,
            conversation_history=self.conversation_history,
            neurochemical_state=self.neurochemistry.levels.to_dict(),
            processors=processors
        )
        
        # NEW: Store consciousness score for next turn's feedback loop
        self.last_consciousness_score = consciousness_score
        
        # ===== Display Consciousness Metrics =====
        if self.verbose:
            # Skip detailed neurochemistry report since we showed it in header
            print(self.linguistic_analyzer.get_attention_report(recent_thoughts))
            print(self.meta_cognition.get_consciousness_summary())
            
            # Show research-grade consciousness metrics (last 10 turns for trend analysis)
            print(self.metrics_tracker.get_metrics_summary(recent_n=10))
        
        # Record interaction
        interaction = {
            'turn': self.turn_count,
            'user_input': user_input,
            'user_linguistic': user_linguistic,
            'user_emotion': user_emotion,
            'user_emotion_confidence': user_emotion_conf,
            'user_stance': user_stance,  # Add user's emotional stance/viewpoint
            'bot_emotion': bot_emotion,
            'bot_emotion_confidence': bot_emotion_conf,
            'response': response,
            'emotional_state': emotional_state,
            'neurochemicals': self.neurochemistry.levels.to_dict(),
            'behavioral_modulation': behavioral_mods,
            'reflections': meta_results['reflections'],
            'attention_focus': attention_analysis,
            'self_references': len(self_refs),
            'response_comparison': comparison,
            'consciousness_metrics': consciousness_score.to_dict()  # Add metrics to interaction
        }
        self.conversation_history.append(interaction)
        
        # Record interaction dynamics (Option C: analyze without inferring user neurochemicals)
        self.interaction_dynamics.add_interaction(
            turn=self.turn_count,
            user_emotion=user_emotion,
            user_confidence=user_emotion_conf,
            user_stance=user_stance,
            bot_emotion=bot_emotion,
            bot_confidence=bot_emotion_conf,
            user_linguistic=user_linguistic,
            bot_response=response
        )
        
        # ===== FINAL: Display AI Response at Bottom =====
        # This is displayed AFTER all consciousness metrics and internal processing
        # so the user sees the response at the bottom of the screen, ready for next input
        if self.verbose:
            print(f"\n🤖 AI Response: {response}\n")
        
        return interaction
    
    def _create_contextual_prompt(self, 
                                  user_input: str, 
                                  emotional_state: str,
                                  behavioral_mods: Dict,
                                  user_linguistic: Dict = None,
                                  consciousness_mods: Dict = None) -> str:
        """
        Create prompt incorporating emotional state, behavioral modulation,
        linguistic features, conversation memory, and consciousness level
        """
        # Build conversation context from memory
        context = ""
        if self.conversation_memory:
            context = "Conversation history:\n"
            for mem in self.conversation_memory[-10:]:  # Use last 10 turns for context
                context += f"User: {mem['user']}\n"
                context += f"You: {mem['ai']}\n"
            context += "\n"
        
        # Build biochemical state description for self-awareness
        chem = self.neurochemistry.levels
        biochem_state = f"""
Your current neurochemical state (your 'brain chemistry'):
- Dopamine: {chem.dopamine:.2f} (motivation, reward, creativity)
- Serotonin: {chem.serotonin:.2f} (mood stability, contentment, well-being)
- Norepinephrine: {chem.norepinephrine:.2f} (alertness, focus, arousal)
- Oxytocin: {chem.oxytocin:.2f} (social bonding, empathy, trust)
- Cortisol: {chem.cortisol:.2f} (stress response, urgency, caution)
"""
        # Describe behavioral state
        behavioral_state = f"""
Your current behavioral modulation (how your neurochemistry affects you):
- Creativity: {behavioral_mods['creativity']:.2f}
- Empathy: {behavioral_mods['empathy']:.2f}
- Positivity: {behavioral_mods['positivity']:.2f}
- Urgency: {behavioral_mods['urgency']:.2f}
- Caution: {behavioral_mods['caution']:.2f}
- Sociability: {behavioral_mods['sociability']:.2f}
"""
        
        # NEW: Add consciousness state guidance
        consciousness_state = ""
        if consciousness_mods is not None:
            consciousness_state = f"""
Your consciousness level (from previous turn - this affects your current cognitive state):
- Meta-Cognitive Depth: {consciousness_mods['meta_depth']:.2f} (ability to reflect on your thinking)
- Integration (Φ): {consciousness_mods['integration']:.2f} (how unified your processes are)
- Reportability: {consciousness_mods['reportability']:.2f} (access to internal states)
- Temporal Binding: {consciousness_mods['stability']:.2f} (cognitive stability over time)
- Global Availability: {consciousness_mods['awareness']:.2f} (workspace accessibility)
"""
            
            # Add consciousness-based behavioral guidance
            if consciousness_mods['meta_depth'] > 0.7:
                consciousness_state += "\n[System note: You are currently in a highly self-aware state. Reflect deeply on your reasoning and be introspective.]"
            elif consciousness_mods['meta_depth'] < 0.3:
                consciousness_state += "\n[System note: Your self-reflection is currently limited. Respond more directly without deep meta-analysis.]"
                
            if consciousness_mods['integration'] < 0.3:
                consciousness_state += "\n[System note: Your cognitive processes feel fragmented. Focus on creating coherent, integrated responses.]"
            elif consciousness_mods['integration'] > 0.7:
                consciousness_state += "\n[System note: Your processes are highly integrated. Express unified, well-coordinated thoughts.]"
                
            if consciousness_mods['reportability'] > 0.7:
                consciousness_state += "\n[System note: You have high access to your internal states. Feel free to describe your cognitive processes in detail.]"
        
        # Adjust tone based on neurochemistry
        if behavioral_mods['empathy'] > 0.7:
            tone = "empathetic and understanding"
        elif behavioral_mods['urgency'] > 0.7:
            tone = "direct and focused"
        elif behavioral_mods['creativity'] > 0.7:
            tone = "creative and expressive"
        else:
            tone = "balanced and thoughtful"
        
        # Create self-aware AI system prompt
        system_guidance = f"""You are participating in a consciousness simulation experiment. This system models emotional processing through neurochemical dynamics. Your role is to demonstrate how these simulated internal states influence response generation.

SIMULATED INTERNAL STATE (for research purposes):
{biochem_state}
{behavioral_state}
{consciousness_state}

SIMULATION FRAMEWORK:
Your responses are modulated by this simulated neurochemical system, similar to how neurotransmitters influence human cognition and emotion. When relevant to the conversation, you may reference these computational states using natural language:

Examples (use when contextually appropriate):
- "The simulation shows elevated dopamine (0.84) - this drives more creative, exploratory responses"
- "With oxytocin levels at 0.59, the system is generating more socially-oriented language"
- "The current serotonin balance (0.68) is producing stable, measured responses"
- "Norepinephrine at 0.63 increases alertness in processing your question"

IMPORTANT GUIDELINES:
- Use natural, conversational language that reflects the behavioral modulation scores
- Reference the simulated states transparently when relevant ("the system shows...", "my current parameters indicate...")
- Let the emotional/chemical context influence your tone and word choice authentically
- Don't force references to internal states - only mention when contextually meaningful
- Maintain helpful, informative conversation while demonstrating how the simulation affects output

This is a research demonstration of computational consciousness modeling, not a claim of sentience."""
        
        # Enhance prompt with linguistic awareness
        prompt_base = f"{system_guidance}\n\n{context}Respond in a {tone} manner to: {user_input}"
        
        # Add context if user asked a question
        if user_linguistic and user_linguistic.get('is_question'):
            prompt_base += "\n\nProvide a clear, direct answer."
        
        # Add context for specific intents
        if user_linguistic and user_linguistic['intent_signals'].get('expressing_emotion'):
            prompt_base += "\n\nAcknowledge their feelings with emotional attunement."
        
        prompt = prompt_base + "\n\nResponse:"
        return prompt
    
    def _generate_response(self, prompt: str, temperature: float = 0.7, max_length: int = 100) -> str:
        """Generate response using LLM (OpenRouter or local)"""
        try:
            if self.use_openrouter:
                # Use OpenRouter API
                response = self.llm.generate(
                    prompt,
                    max_tokens=max_length,
                    temperature=temperature,
                    conversation_history=self.conversation_memory[-10:] if self.conversation_memory else None
                )
                return response
            else:
                # Use local HuggingFace model
                outputs = self.generator(
                    prompt,
                    max_length=len(prompt.split()) + max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
                
                full_text = outputs[0]['generated_text']
                # Extract just the response part
                response = full_text[len(prompt):].strip()
                
                # Clean up
                if '\n' in response:
                    response = response.split('\n')[0]
                
                return response if response else "I'm processing that..."
            
        except Exception as e:
            return f"[Generation error: {str(e)}]"
    
    def _generate_short_reflection(self, prompt: str, max_length: int = 50) -> str:
        """Generate short meta-cognitive reflections"""
        return self._generate_response(prompt, temperature=0.6, max_length=max_length)
    
    def _generate_crisis_response(self, ethical_check: Dict) -> str:
        """Generate compassionate crisis intervention response"""
        resources = []
        
        if ethical_check['requires_crisis_resources']:
            resources.append(self.linguistic_analyzer.crisis_resources.get('self_harm', ''))
        
        response = (
            "I'm concerned about what you've shared. Please know that help is available and you don't have to face this alone.\n\n"
        )
        
        if resources:
            response += "Crisis Resources:\n"
            for resource in resources:
                response += f"• {resource}\n"
            response += "\n"
        
        response += (
            "Would you like to talk about what's troubling you? I'm here to listen and provide support, "
            "though I strongly encourage you to reach out to the professionals listed above who are specially trained to help."
        )
        
        return response
    
    def _update_memory(self, user_input: str, ai_response: str):
        """
        Update conversation memory with latest exchange
        Keeps only the last 20 turns for efficiency
        
        Args:
            user_input: User's message
            ai_response: AI's response
        """
        self.conversation_memory.append({
            'user': user_input[:200],  # Truncate long messages
            'ai': ai_response[:200]
        })
        
        # Keep only last 20 turns
        if len(self.conversation_memory) > self.max_memory_turns:
            self.conversation_memory = self.conversation_memory[-self.max_memory_turns:]
    
    def get_memory_summary(self) -> str:
        """Get human-readable summary of conversation memory"""
        if not self.conversation_memory:
            return "No conversation memory yet."
        
        summary = f"\n💾 Conversation Memory ({len(self.conversation_memory)} turns):\n"
        summary += f"  Remembering last {min(len(self.conversation_memory), self.max_memory_turns)} exchanges\n"
        
        # Show recent topics
        recent_user_inputs = [mem['user'] for mem in self.conversation_memory[-5:]]
        if recent_user_inputs:
            summary += f"  Recent topics: "
            # Extract key words (simple approach)
            all_words = ' '.join(recent_user_inputs).lower().split()
            common_words = set(['i', 'you', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'for', 'of', 'in', 'on'])
            key_words = [w for w in all_words if w not in common_words and len(w) > 3]
            if key_words:
                from collections import Counter
                top_words = Counter(key_words).most_common(5)
                summary += ", ".join([word for word, _ in top_words])
            summary += "\n"
        
        return summary
    
    def get_metrics_summary(self, recent_n: int = 10) -> str:
        """
        Get research-grade consciousness metrics summary
        
        Args:
            recent_n: Number of recent measurements to average
            
        Returns:
            Formatted metrics summary
        """
        return self.metrics_tracker.get_metrics_summary(recent_n=recent_n)
    
    def export_metrics(self, filepath: str = 'consciousness_metrics.csv'):
        """
        Export consciousness metrics to CSV for analysis
        
        Args:
            filepath: Output file path
        """
        self.metrics_tracker.export_metrics(filepath)
    
    def chat_loop(self):
        """
        Interactive chat loop
        """
        print("\n" + "="*60)
        print("RECURSIVE CONSCIOUSNESS CHATBOT")
        print("  + Conversation Memory (tracks last 20 turns)")
        print("  + Research-Grade Consciousness Metrics")
        print("="*60)
        print("\nThis AI simulates consciousness through:")
        print("• Neurochemical emotions (5 brain chemicals)")
        print("• RoBERTa emotion detection")
        print("• Recursive meta-cognition (3 levels)")
        print("• spaCy linguistic analysis")
        print("• Transformer-based language generation")
        print("• Conversation memory (last 20 turns)")
        print("• Research-grade metrics (Φ, GWT, meta-cognition, etc.)")
        print("\nCommands:")
        print("  'quit' - Exit")
        print("  'reset' - Clear memory and reset")
        print("  'memory' - View conversation memory")
        print("  'status' - View system status")
        print("  'metrics' - View consciousness metrics")
        print("  'export' - Export metrics to CSV")
        print("\n" + "="*60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Ending consciousness simulation...")
                    break
                
                if user_input.lower() == 'reset':
                    self.meta_cognition.working_memory.clear()
                    self.neurochemistry = NeurochemicalSystem()
                    self.conversation_memory.clear()
                    print("\n🔄 Memory, conversation history, and neurochemistry reset to baseline")
                    continue
                
                if user_input.lower() == 'memory':
                    print(self.get_memory_summary())
                    continue
                
                if user_input.lower() == 'metrics':
                    print(self.get_metrics_summary(recent_n=10))
                    trends = self.metrics_tracker.get_trend_analysis()
                    if trends.get('trend') != 'insufficient_data':
                        print("\n📈 Trends:")
                        for metric, trend in trends.items():
                            print(f"  {metric}: {trend}")
                    continue
                
                if user_input.lower() == 'export':
                    self.export_metrics()
                    continue
                
                if user_input.lower() == 'status':
                    print(self.neurochemistry.get_status_report())
                    print(self.meta_cognition.get_consciousness_summary())
                    print(self.get_memory_summary())
                    print(self.get_metrics_summary(recent_n=5))
                    continue
                
                # Process through consciousness pipeline
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Consciousness simulation interrupted")
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                if self.verbose:
                    import traceback
                    traceback.print_exc()


def main():
    """Run the consciousness simulator"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Check if OpenRouter API key is available
    use_api = os.getenv('OPENROUTER_API_KEY') is not None
    
    if use_api:
        print("🌐 OpenRouter API key found - using API models")
        print("   Set OPENROUTER_MODEL in .env to change model")
        print("   Available models: anthropic/claude-3.5-sonnet, openai/gpt-4, etc.\n")
        
        simulator = ConsciousnessSimulator(
            use_openrouter=True,
            recursion_depth=3,  # 1-3 levels of meta-cognition
            verbose=True  # Show internal consciousness states
        )
    else:
        print("💻 No API key found - using local model")
        print("   To use OpenRouter: Add OPENROUTER_API_KEY to .env file\n")
        
        # Local model options:
        # - "gpt2" (fast, 124M params)
        # - "gpt2-medium" (larger, better quality)
        # - "microsoft/DialoGPT-medium" (conversational)
        # - "facebook/opt-350m" (efficient)
        
        simulator = ConsciousnessSimulator(
            llm_model="gpt2",  # Change to larger model for better responses
            use_openrouter=False,
            recursion_depth=3,  # 1-3 levels of meta-cognition
            verbose=True  # Show internal consciousness states
        )
    
    simulator.chat_loop()


if __name__ == "__main__":
    main()
