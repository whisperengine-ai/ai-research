"""
Simple Demo of Consciousness Simulator
Shows key features with minimal setup
"""

from consciousness_chatbot import ConsciousnessSimulator


def demo_neurochemistry():
    """Demonstrate neurochemical emotion system"""
    print("\n" + "="*60)
    print("DEMO 1: Neurochemical Emotion System")
    print("="*60)
    
    from neurochemistry import NeurochemicalSystem
    
    neuro = NeurochemicalSystem()
    print("\n📊 Baseline state:")
    print(neuro.get_status_report())
    
    print("\n➡️  Processing 'joy' emotion...")
    neuro.update_from_emotion('joy', intensity=0.8)
    print(neuro.get_status_report())
    
    print("\n➡️  Processing 'anxiety' emotion...")
    neuro.update_from_emotion('anxiety', intensity=0.7)
    print(neuro.get_status_report())


def demo_emotion_detection():
    """Demonstrate RoBERTa emotion detection"""
    print("\n" + "="*60)
    print("DEMO 2: RoBERTa Emotion Detection")
    print("="*60)
    
    from emotion_detector import EmotionDetector
    
    detector = EmotionDetector()
    
    test_texts = [
        "I'm so happy and excited about this!",
        "This is really frustrating and annoying.",
        "I'm worried about what might happen.",
        "Thank you so much, you're amazing!"
    ]
    
    for text in test_texts:
        print(f"\n📝 Text: '{text}'")
        emotion, conf, scores = detector.detect_emotion(text)
        print(detector.get_emotion_report(emotion, conf, scores))


def demo_meta_cognition():
    """Demonstrate recursive meta-cognition"""
    print("\n" + "="*60)
    print("DEMO 3: Recursive Meta-Cognition")
    print("="*60)
    
    from meta_cognition import RecursiveMetaCognition, Thought
    import time
    
    meta = RecursiveMetaCognition(max_recursion_depth=3)
    
    # Simulate some thoughts
    thoughts = [
        Thought(0, "I think AI consciousness is fascinating", time.time(), 'response'),
        Thought(1, "I notice I'm excited about this topic", time.time(), 'observation'),
        Thought(2, "I'm quite confident in this assessment", time.time(), 'evaluation'),
    ]
    
    for thought in thoughts:
        meta.working_memory.add(thought)
        meta.consciousness_stream.append(thought)
    
    print(meta.get_consciousness_summary())


def demo_linguistic_analysis():
    """Demonstrate spaCy linguistic analysis"""
    print("\n" + "="*60)
    print("DEMO 4: Linguistic Analysis")
    print("="*60)
    
    from linguistic_analysis import LinguisticAnalyzer
    
    analyzer = LinguisticAnalyzer(model="en_core_web_md")
    
    thoughts = [
        "I believe artificial intelligence will transform society",
        "The neural network processes information efficiently",
        "I'm analyzing my own thought patterns right now"
    ]
    
    print(analyzer.get_attention_report(thoughts))
    
    # Show self-references
    self_refs = analyzer.extract_self_references(thoughts[2])
    print(f"\n🔍 Self-references detected: {len(self_refs)}")
    for ref in self_refs:
        print(f"  • '{ref}'")


def run_interactive_demo():
    """Run a short interactive conversation"""
    print("\n" + "="*60)
    print("INTERACTIVE DEMO: Full Consciousness Simulation")
    print("="*60)
    
    simulator = ConsciousnessSimulator(
        llm_model="gpt2",
        recursion_depth=2,  # Use 2 levels for faster demo
        verbose=True
    )
    
    # Demo conversation
    demo_inputs = [
        "Hello! How are you feeling?",
        "Tell me about consciousness.",
        "That's interesting! What are you thinking about?",
    ]
    
    print("\n🎬 Running demo conversation...\n")
    print("(Type your own messages or press Enter to use demo inputs)")
    print("(Type 'skip' to skip to next demo, 'quit' to exit)\n")
    
    for i, demo_input in enumerate(demo_inputs):
        user_input = input(f"\n👤 You (or press Enter for demo #{i+1}): ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'skip':
            continue
        elif not user_input:
            user_input = demo_input
            print(f"👤 You: {user_input}")
        
        simulator.process_input(user_input)
        
        input("\n[Press Enter to continue...]")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print(" 🧠 RECURSIVE CONSCIOUSNESS SIMULATOR - DEMO SUITE 🧠 ")
    print("="*70)
    print("\nThis demo showcases:")
    print("• Neurochemical emotion modeling (5 brain chemicals)")
    print("• RoBERTa-based emotion detection")
    print("• Recursive meta-cognition (self-awareness)")
    print("• spaCy linguistic analysis")
    print("• Full consciousness simulation")
    print("\n" + "="*70)
    
    try:
        # Run component demos
        demo_neurochemistry()
        input("\n[Press Enter for next demo...]")
        
        demo_emotion_detection()
        input("\n[Press Enter for next demo...]")
        
        demo_meta_cognition()
        input("\n[Press Enter for next demo...]")
        
        demo_linguistic_analysis()
        input("\n[Press Enter for interactive demo...]")
        
        # Interactive demo
        run_interactive_demo()
        
        print("\n" + "="*70)
        print("✓ Demo complete!")
        print("\nTo run full chatbot: python consciousness_chatbot.py")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n⚠️ Demo error: {e}")
        print("\nNote: Make sure to install dependencies first:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_md")


if __name__ == "__main__":
    main()
