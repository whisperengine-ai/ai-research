"""
Recursive Meta-Cognition System
Implements multi-level self-reflection and awareness
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import time


@dataclass
class Thought:
    """Represents a single thought in the consciousness stream"""
    level: int          # Recursion depth (0=direct, 1=meta, 2=meta-meta, etc.)
    content: str        # The actual thought/reflection
    timestamp: float    # When it occurred
    thought_type: str   # 'response', 'observation', 'evaluation', 'introspection'
    
    
class WorkingMemory:
    """
    Maintains a limited buffer of recent thoughts/interactions
    Simulates conscious attention and working memory capacity
    """
    
    def __init__(self, capacity: int = 7):
        """
        Args:
            capacity: Number of items that can be held (Miller's 7±2)
        """
        self.capacity = capacity
        self.buffer: List[Thought] = []
        self.attention_weights: List[float] = []
    
    def add(self, thought: Thought, attention: float = 1.0):
        """Add thought to working memory with attention weight"""
        self.buffer.append(thought)
        self.attention_weights.append(attention)
        
        # Remove oldest if over capacity
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
            self.attention_weights.pop(0)
    
    def get_recent(self, n: int = 3) -> List[Thought]:
        """Get n most recent thoughts"""
        return self.buffer[-n:]
    
    def get_attended(self, n: int = 3) -> List[Thought]:
        """Get n most attended thoughts"""
        if not self.buffer:
            return []
        
        # Sort by attention weight
        sorted_thoughts = sorted(zip(self.buffer, self.attention_weights), 
                                key=lambda x: x[1], reverse=True)
        return [t for t, _ in sorted_thoughts[:n]]
    
    def clear(self):
        """Clear working memory"""
        self.buffer.clear()
        self.attention_weights.clear()
    
    def __len__(self):
        return len(self.buffer)


class RecursiveMetaCognition:
    """
    Implements recursive self-reflection:
    Level 0: Direct response
    Level 1: "What am I thinking?" (self-observation)
    Level 2: "How confident am I?" (meta-evaluation)
    Level 3: "Why did I think that?" (introspection)
    """
    
    def __init__(self, max_recursion_depth: int = 3):
        self.max_depth = max_recursion_depth
        self.working_memory = WorkingMemory(capacity=7)
        self.consciousness_stream: List[Thought] = []
    
    def process_with_true_recursion(self,
                                    thought: str,
                                    context: Dict[str, Any],
                                    llm_generator,
                                    depth: int = 0,
                                    thought_type: str = 'response') -> Dict[str, Any]:
        """
        TRUE RECURSIVE meta-cognition: Each level reflects on the previous level's output
        
        This is genuine recursion where:
        1. Function calls itself with its own output as input
        2. Each level builds on the reflection from the level below
        3. Creates nested structure of thoughts about thoughts about thoughts
        
        Args:
            thought: The thought to reflect upon
            context: Current context (emotions, memory, etc.)
            llm_generator: Function to generate LLM responses
            depth: Current recursion depth (0 = base, 1+ = meta-levels)
            thought_type: Type of thought at this level
            
        Returns:
            Nested dictionary with thought and recursive meta-reflections
        """
        # Base case: Maximum depth reached
        if depth >= self.max_depth:
            return {
                'level': depth,
                'content': thought,
                'type': thought_type,
                'meta_reflection': None  # No deeper reflection
            }
        
        # Store current thought in working memory
        current_thought = Thought(
            level=depth,
            content=thought,
            timestamp=time.time(),
            thought_type=thought_type
        )
        attention_weight = max(0.2, 1.0 - (depth * 0.2))  # Deeper = less attention
        self.working_memory.add(current_thought, attention=attention_weight)
        self.consciousness_stream.append(current_thought)
        
        # Generate meta-reflection on current thought
        if depth == 0:
            # Level 0 → Level 1: Self-observation (What am I noticing?)
            reflection_prompt = f"""Response: "{thought[:150]}..."

Meta-observation (8 words max): What aspect of this response stands out most to you?"""
            next_type = 'observation'
        elif depth == 1:
            # Level 1 → Level 2: Meta-evaluation (How adequate is this?)
            reflection_prompt = f"""You noticed: "{thought[:150]}..."

Meta-evaluation (8 words max): Rate confidence in this observation (0-10) and explain briefly:"""
            next_type = 'evaluation'
        elif depth == 2:
            # Level 2 → Level 3: Deep introspection (Why this pattern?)
            reflection_prompt = f"""You evaluated: "{thought[:150]}..."

Meta-introspection (10 words max): What cognitive pattern or bias might explain this evaluation?"""
            next_type = 'introspection'
        else:
            # Generic meta-reflection for deeper levels
            reflection_prompt = f"""Reflect on: "{thought[:150]}..."

Brief meta-thought (8 words max):"""
            next_type = f'meta-{depth}'
        
        # Generate the meta-reflection (with strict token limit)
        meta_thought = llm_generator(reflection_prompt, max_length=30)
        
        # RECURSIVE CALL: Reflect on the reflection
        deeper_reflection = self.process_with_true_recursion(
            meta_thought,      # ← Previous output becomes current input
            context,
            llm_generator,
            depth + 1,         # ← Increase depth
            next_type
        )
        
        # Return nested structure
        return {
            'level': depth,
            'content': thought,
            'type': thought_type,
            'meta_reflection': deeper_reflection  # ← Contains recursive structure
        }
    
    def flatten_recursive_results(self, recursive_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Convert nested recursive structure to flat list for display
        
        Args:
            recursive_dict: Nested dictionary from process_with_true_recursion
            
        Returns:
            Flat list of reflections
        """
        reflections = []
        
        def traverse(node, accumulated=[]):
            if node is None:
                return
            
            reflections.append({
                'level': node['level'],
                'type': node['type'],
                'content': node['content']
            })
            
            # Recursively traverse deeper reflections
            if node.get('meta_reflection'):
                traverse(node['meta_reflection'])
        
        traverse(recursive_dict)
        return reflections
    
    def process_with_recursion(self, 
                               primary_response: str,
                               context: Dict[str, Any],
                               llm_generator) -> Dict[str, Any]:
        """
        Process a response through recursive meta-cognitive levels
        
        Args:
            primary_response: The base response to reflect upon
            context: Current context (emotions, memory, etc.)
            llm_generator: Function to generate LLM responses
            
        Returns:
            Dictionary with responses at each recursive level
        """
        results = {
            'level_0_response': primary_response,
            'reflections': [],
            'consciousness_stream': []
        }
        
        # Level 0: Direct response
        thought_0 = Thought(
            level=0,
            content=primary_response,
            timestamp=time.time(),
            thought_type='response'
        )
        self.working_memory.add(thought_0, attention=1.0)
        self.consciousness_stream.append(thought_0)
        results['consciousness_stream'].append(thought_0)
        
        # Level 1: Self-observation - "What am I thinking?"
        if self.max_depth >= 1:
            observation_prompt = self._create_observation_prompt(primary_response, context)
            observation = llm_generator(observation_prompt, max_length=100)
            
            thought_1 = Thought(
                level=1,
                content=observation,
                timestamp=time.time(),
                thought_type='observation'
            )
            self.working_memory.add(thought_1, attention=0.8)
            self.consciousness_stream.append(thought_1)
            results['reflections'].append({
                'level': 1,
                'type': 'self-observation',
                'content': observation
            })
            results['consciousness_stream'].append(thought_1)
        
        # Level 2: Meta-evaluation - "How confident/appropriate is this?"
        if self.max_depth >= 2:
            evaluation_prompt = self._create_evaluation_prompt(primary_response, context)
            evaluation = llm_generator(evaluation_prompt, max_length=80)
            
            thought_2 = Thought(
                level=2,
                content=evaluation,
                timestamp=time.time(),
                thought_type='evaluation'
            )
            self.working_memory.add(thought_2, attention=0.6)
            self.consciousness_stream.append(thought_2)
            results['reflections'].append({
                'level': 2,
                'type': 'meta-evaluation',
                'content': evaluation
            })
            results['consciousness_stream'].append(thought_2)
        
        # Level 3: Introspection - "Why did I respond this way?"
        if self.max_depth >= 3:
            introspection_prompt = self._create_introspection_prompt(primary_response, context)
            introspection = llm_generator(introspection_prompt, max_length=100)
            
            thought_3 = Thought(
                level=3,
                content=introspection,
                timestamp=time.time(),
                thought_type='introspection'
            )
            self.working_memory.add(thought_3, attention=0.4)
            self.consciousness_stream.append(thought_3)
            results['reflections'].append({
                'level': 3,
                'type': 'introspection',
                'content': introspection
            })
            results['consciousness_stream'].append(thought_3)
        
        return results
    
    def _create_observation_prompt(self, response: str, context: Dict) -> str:
        """Generate prompt for self-observation (Level 1)"""
        emotional_state = context.get('emotional_state', 'neutral')
        
        prompt = f"""You just responded: "{response[:200]}..."

Your current emotional state: {emotional_state}

In one brief sentence, observe what you're thinking or feeling about this response:"""
        return prompt
    
    def _create_evaluation_prompt(self, response: str, context: Dict) -> str:
        """Generate prompt for meta-evaluation (Level 2)"""
        prompt = f"""Your response was: "{response[:200]}..."

In one brief sentence, evaluate how confident and appropriate this response is:"""
        return prompt
    
    def _create_introspection_prompt(self, response: str, context: Dict) -> str:
        """Generate prompt for introspection (Level 3)"""
        chemicals = context.get('neurochemicals', {})
        
        prompt = f"""You responded: "{response[:200]}..."

Your neurochemical state: {chemicals}

In one brief sentence, reflect on why you responded this way:"""
        return prompt
    
    def get_consciousness_summary(self) -> str:
        """Generate summary of recent conscious experience"""
        if not self.consciousness_stream:
            return "No conscious thoughts yet."
        
        recent = self.consciousness_stream[-5:]
        summary = "\n💭 Stream of Consciousness:\n"
        
        for thought in recent:
            indent = "  " * thought.level
            icon = {
                'response': '💬',
                'observation': '👁️',
                'evaluation': '⚖️',
                'introspection': '🔍'
            }.get(thought.thought_type, '•')
            
            summary += f"{indent}{icon} L{thought.level}: {thought.content[:100]}\n"
        
        return summary
