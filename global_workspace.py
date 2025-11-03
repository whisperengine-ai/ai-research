"""
Global Workspace Theory (GWT) Implementation
Based on Bernard Baars' theory of consciousness as a "theater of the mind"

Key Concepts:
- Multiple specialized processors compete for access to a global workspace
- Information that enters the workspace is "broadcast" to all processors
- Consciousness = contents of the global workspace
- Attention = spotlight that determines what enters the workspace
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import time
import numpy as np


@dataclass
class Information:
    """Represents a piece of information competing for global workspace access"""
    source: str                    # Which module generated this (emotion, language, memory, etc.)
    content: str                   # The actual information
    salience: float               # How attention-grabbing (0.0 to 1.0)
    relevance: float              # How relevant to current context (0.0 to 1.0)
    timestamp: float              # When it was generated
    activation_level: float = 0.0 # Current activation (0.0 to 1.0)
    
    def get_priority(self) -> float:
        """Calculate priority for workspace access"""
        # Recency bias: newer information gets slight boost
        recency = 1.0 / (1.0 + (time.time() - self.timestamp))
        return (self.salience * 0.4 + 
                self.relevance * 0.4 + 
                recency * 0.2)


@dataclass
class BroadcastMessage:
    """Information that has entered the global workspace and is being broadcast"""
    information: Information
    broadcast_time: float
    reached_modules: List[str] = field(default_factory=list)
    

class SpecializedProcessor:
    """
    Represents a cognitive module (emotion, language, memory, sensory, etc.)
    that operates unconsciously and competes for workspace access
    """
    
    def __init__(self, name: str, processing_capacity: float = 1.0):
        self.name = name
        self.capacity = processing_capacity
        self.input_buffer: List[BroadcastMessage] = []
        self.output_queue: List[Information] = []
        
    def receive_broadcast(self, broadcast: BroadcastMessage):
        """Receive information from global workspace"""
        self.input_buffer.append(broadcast)
        broadcast.reached_modules.append(self.name)
        
    def process(self) -> List[Information]:
        """Process inputs and generate outputs (to be implemented by subclasses)"""
        # Base implementation: just return queued outputs
        outputs = self.output_queue.copy()
        self.output_queue.clear()
        return outputs
    
    def submit_to_workspace(self, content: str, salience: float, relevance: float):
        """Submit information to compete for workspace access"""
        info = Information(
            source=self.name,
            content=content,
            salience=salience,
            relevance=relevance,
            timestamp=time.time()
        )
        self.output_queue.append(info)


class GlobalWorkspace:
    """
    The Global Workspace - a limited-capacity "broadcast channel" for consciousness
    
    Only information that wins the competition enters the workspace
    Once in workspace, it's broadcast to ALL specialized processors
    """
    
    def __init__(self, 
                 capacity: int = 3,              # How many items can be conscious at once
                 decay_rate: float = 0.1,        # How fast items fade from workspace
                 competition_threshold: float = 0.5):  # Minimum priority to enter
        
        self.capacity = capacity
        self.decay_rate = decay_rate
        self.competition_threshold = competition_threshold
        
        # Current contents of consciousness
        self.workspace_contents: List[Information] = []
        
        # Specialized processors (cognitive modules)
        self.processors: Dict[str, SpecializedProcessor] = {}
        
        # Broadcast history
        self.broadcast_history: List[BroadcastMessage] = []
        
        # Competition tracking
        self.competition_pool: List[Information] = []
        
    def register_processor(self, processor: SpecializedProcessor):
        """Register a specialized cognitive module"""
        self.processors[processor.name] = processor
        
    def submit_information(self, info: Information):
        """Submit information to compete for workspace access"""
        info.activation_level = info.get_priority()
        self.competition_pool.append(info)
        
    def competition_cycle(self) -> List[BroadcastMessage]:
        """
        Run competition for workspace access
        Only highest-priority information enters consciousness
        """
        if not self.competition_pool:
            return []
        
        # Calculate activation levels
        for info in self.competition_pool:
            info.activation_level = info.get_priority()
        
        # Sort by priority
        self.competition_pool.sort(key=lambda x: x.activation_level, reverse=True)
        
        # Select winners
        winners = []
        available_slots = self.capacity - len(self.workspace_contents)
        
        for info in self.competition_pool[:available_slots]:
            if info.activation_level >= self.competition_threshold:
                winners.append(info)
                self.workspace_contents.append(info)
        
        # Remove winners from competition pool
        self.competition_pool = [info for info in self.competition_pool if info not in winners]
        
        # Broadcast winners to all processors
        broadcasts = []
        for info in winners:
            broadcast = BroadcastMessage(
                information=info,
                broadcast_time=time.time()
            )
            
            # Send to all processors
            for processor in self.processors.values():
                processor.receive_broadcast(broadcast)
            
            broadcasts.append(broadcast)
            self.broadcast_history.append(broadcast)
        
        return broadcasts
    
    def decay_workspace(self):
        """
        Remove old/low-activation items from workspace
        Simulates fading of conscious content over time
        """
        # Apply decay
        for info in self.workspace_contents:
            info.activation_level *= (1.0 - self.decay_rate)
        
        # Remove items below threshold (FIXED: more aggressive removal)
        before_count = len(self.workspace_contents)
        self.workspace_contents = [
            info for info in self.workspace_contents 
            if info.activation_level > 0.2  # Increased threshold from 0.1 to 0.2
        ]
        after_count = len(self.workspace_contents)
        
        # DEBUG: Log removals
        if before_count > after_count:
            removed = before_count - after_count
            # Only log if verbose mode would be set (we'll add a flag later)
            pass  # Placeholder for future debug mode
    
    def process_cycle(self) -> Dict[str, Any]:
        """
        One complete cycle of global workspace processing:
        1. Processors generate outputs
        2. Competition for workspace access
        3. Broadcast winners to all processors
        4. Decay workspace contents
        """
        cycle_results = {
            'submissions': 0,
            'broadcasts': [],
            'workspace_contents': [],
            'competition_summary': {}
        }
        
        # Step 1: Collect submissions from all processors
        for processor in self.processors.values():
            outputs = processor.process()
            for info in outputs:
                self.submit_information(info)
                cycle_results['submissions'] += 1
        
        # Step 2: Run competition
        broadcasts = self.competition_cycle()
        cycle_results['broadcasts'] = [
            {
                'source': b.information.source,
                'content': b.information.content,
                'priority': b.information.activation_level
            }
            for b in broadcasts
        ]
        
        # Step 3: Decay existing workspace contents
        self.decay_workspace()
        
        # Step 4: Report current workspace state
        cycle_results['workspace_contents'] = [
            {
                'source': info.source,
                'content': info.content[:100],
                'activation': info.activation_level,
                'age': time.time() - info.timestamp
            }
            for info in self.workspace_contents
        ]
        
        cycle_results['competition_summary'] = {
            'total_competitors': len(self.competition_pool) + len(broadcasts),
            'winners': len(broadcasts),
            'workspace_occupancy': len(self.workspace_contents),
            'workspace_capacity': self.capacity
        }
        
        return cycle_results
    
    def get_conscious_content(self) -> List[str]:
        """Get current contents of consciousness (what's in the workspace)"""
        return [info.content for info in self.workspace_contents]
    
    def get_attention_focus(self) -> Optional[Information]:
        """Get the most activated item in workspace (attention spotlight)"""
        if not self.workspace_contents:
            return None
        return max(self.workspace_contents, key=lambda x: x.activation_level)
    
    def get_workspace_summary(self) -> str:
        """Human-readable summary of workspace state"""
        if not self.workspace_contents:
            return "🌑 Workspace: Empty (unconscious processing only)"
        
        summary = "💡 CONSCIOUS WORKSPACE:\n"
        summary += f"   Capacity: {len(self.workspace_contents)}/{self.capacity}\n"
        
        # Show items by activation level
        sorted_contents = sorted(
            self.workspace_contents, 
            key=lambda x: x.activation_level, 
            reverse=True
        )
        
        for i, info in enumerate(sorted_contents, 1):
            activation_bar = "█" * int(info.activation_level * 10)
            summary += f"   {i}. [{info.source}] {activation_bar} {info.activation_level:.2f}\n"
            summary += f"      → {info.content[:80]}...\n"
        
        return summary
    
    def clear(self):
        """Clear workspace (loss of consciousness)"""
        self.workspace_contents.clear()
        self.competition_pool.clear()


class EmotionProcessor(SpecializedProcessor):
    """Specialized processor for emotional information"""
    
    def __init__(self):
        super().__init__("emotion", processing_capacity=1.0)
        
    def process_emotion(self, emotion: str, intensity: float, context: str):
        """Process emotional state and submit to workspace if salient"""
        salience = intensity  # Strong emotions are more salient
        relevance = 0.8 if intensity > 0.6 else 0.5
        
        content = f"Feeling {emotion} (intensity: {intensity:.2f}) - {context}"
        self.submit_to_workspace(content, salience, relevance)


class LanguageProcessor(SpecializedProcessor):
    """Specialized processor for language understanding"""
    
    def __init__(self):
        super().__init__("language", processing_capacity=1.0)
        
    def process_input(self, text: str, linguistic_features: Dict):
        """Process language input and extract salient features"""
        # Questions are highly salient
        is_question = linguistic_features.get('is_question', False)
        salience = 0.9 if is_question else 0.6
        
        # Emotional content increases relevance
        has_emotion = linguistic_features.get('intent_signals', {}).get('expressing_emotion', False)
        relevance = 0.8 if has_emotion else 0.6
        
        content = f"Language input: '{text[:100]}...'"
        self.submit_to_workspace(content, salience, relevance)


class MemoryProcessor(SpecializedProcessor):
    """Specialized processor for memory retrieval"""
    
    def __init__(self):
        super().__init__("memory", processing_capacity=1.0)
        
    def recall_relevant(self, query: str, memories: List[str]):
        """Submit relevant memories to workspace"""
        if memories:
            salience = 0.7  # Memories moderately salient
            relevance = 0.8  # High relevance to current context
            content = f"Memory recall: {memories[-1][:100]}"
            self.submit_to_workspace(content, salience, relevance)


class MetaCognitiveProcessor(SpecializedProcessor):
    """Specialized processor for meta-cognitive reflection"""
    
    def __init__(self):
        super().__init__("metacognition", processing_capacity=1.0)
        
    def submit_reflection(self, reflection: str, level: int):
        """Submit meta-cognitive reflection to workspace"""
        # Higher-level reflections are less salient (more abstract)
        salience = max(0.3, 0.8 - (level * 0.15))
        relevance = 0.7
        
        content = f"Meta-thought (L{level}): {reflection}"
        self.submit_to_workspace(content, salience, relevance)
