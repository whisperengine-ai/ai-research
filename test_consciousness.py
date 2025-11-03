"""
Pytest test suite for consciousness simulator
"""

import pytest
import numpy as np
from pathlib import Path
import sys
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))


class TestMetricsCalculation:
    """Unit tests for consciousness metrics"""
    
    def test_metrics_initialization(self):
        """Test metrics module initializes"""
        from metrics import ConsciousnessMetrics, ConsciousnessScore
        
        metrics = ConsciousnessMetrics()
        assert hasattr(metrics, 'history')
        assert isinstance(metrics.history, list)
    
    def test_consciousness_score(self):
        """Test ConsciousnessScore dataclass"""
        from metrics import ConsciousnessScore
        
        score = ConsciousnessScore(
            phi=0.5,
            global_availability=0.6,
            meta_cognitive_depth=0.7,
            temporal_binding=0.4,
            reportability=0.8,
            overall_consciousness=0.6,
            timestamp=0.0
        )
        
        assert score.phi == 0.5
        assert score.reportability == 0.8
        
        # Test to_dict
        d = score.to_dict()
        assert len(d) == 7
        assert d['phi'] == 0.5


class TestEmotionDetection:
    """Test emotion detection and stance analysis"""
    
    def test_emotion_detection_basic(self):
        """Test basic emotion detection"""
        from emotion_detector import EmotionDetector
        detector = EmotionDetector()
        emotion, confidence, scores = detector.detect_emotion("I'm happy today")
        
        assert emotion in ['joy', 'anger', 'fear', 'sadness', 'disgust', 'surprise', 'neutral']
        assert 0 <= confidence <= 1
        assert isinstance(scores, dict)
        assert sum(scores.values()) == pytest.approx(1.0, rel=0.01)
    
    def test_stance_analysis(self):
        """Test user emotional stance analysis"""
        from emotion_detector import EmotionDetector
        detector = EmotionDetector()
        
        # Direct emotion
        stance_direct = detector.analyze_user_stance("I'm frustrated")
        assert stance_direct['emotion_type'] in ['direct', 'attributed', 'mixed']
        assert 0 <= stance_direct['self_focus'] <= 1
        
        # Attributed emotion
        stance_attr = detector.analyze_user_stance("They seem angry")
        assert 0 <= stance_attr['self_focus'] <= 1


class TestInteractionDynamics:
    """Test interaction dynamics tracking"""
    
    def test_add_interaction(self):
        """Test adding interaction record"""
        from interaction_dynamics import InteractionDynamics
        tracker = InteractionDynamics()
        
        result = tracker.add_interaction(
            turn=1,
            user_emotion='joy',
            user_confidence=0.95,
            user_stance={'emotion_type': 'direct', 'self_focus': 0.8},
            bot_emotion='neutral',
            bot_confidence=0.85,
            user_linguistic={'complexity': 0.7},
            bot_response="That's great!"
        )
        
        assert result['turn'] == 1
        assert 'resonance' in result
        assert 'engagement' in result
        assert 'appropriateness' in result
    
    def test_emotional_trajectory(self):
        """Test emotional trajectory analysis"""
        from interaction_dynamics import InteractionDynamics
        tracker = InteractionDynamics()
        
        # Add multiple turns
        for i, emotion in enumerate(['anger', 'neutral', 'joy']):
            tracker.add_interaction(
                turn=i+1,
                user_emotion=emotion,
                user_confidence=0.9,
                user_stance={'emotion_type': 'direct', 'self_focus': 0.8},
                bot_emotion='neutral',
                bot_confidence=0.8,
                user_linguistic={},
                bot_response="Test"
            )
        
        trajectory = tracker.get_emotional_trajectory()
        assert trajectory['status'] == 'success'
        assert 'trajectory' in trajectory
        assert trajectory['direction'] in ['improving', 'stable', 'declining']
    
    def test_resonance_analysis(self):
        """Test emotional resonance calculation"""
        from interaction_dynamics import InteractionDynamics
        tracker = InteractionDynamics()
        
        for _ in range(3):
            tracker.add_interaction(
                turn=1,
                user_emotion='joy',
                user_confidence=0.9,
                user_stance={'emotion_type': 'direct', 'self_focus': 0.8},
                bot_emotion='joy',
                bot_confidence=0.85,
                user_linguistic={},
                bot_response="Great!"
            )
        
        resonance = tracker.get_resonance_analysis()
        assert resonance['status'] == 'success'
        assert 0 <= resonance['average_resonance'] <= 1


class TestReliabilityValidity:
    """Test reliability and validity measurements"""
    
    def test_cronbach_alpha(self):
        """Test Cronbach's alpha calculation"""
        from reliability_validity import ReliabilityValidator
        
        # Create sample data with high internal consistency
        data = np.random.RandomState(42).normal(0.5, 0.1, (30, 5))
        data = np.clip(data, 0, 1)
        
        alpha = ReliabilityValidator.cronbach_alpha(data)
        assert isinstance(alpha, float)
        assert -1 <= alpha <= 1
    
    def test_test_retest_reliability(self):
        """Test test-retest ICC calculation"""
        from reliability_validity import ReliabilityValidator
        
        test1 = np.random.RandomState(42).normal(0.5, 0.1, 20)
        test2 = test1 + np.random.RandomState(43).normal(0, 0.05, 20)
        
        result = ReliabilityValidator.test_retest_reliability(test1, test2)
        assert 'icc_2_1' in result
        assert 'correlation' in result
        assert -1 <= result['icc_2_1'] <= 1
    
    def test_convergent_validity(self):
        """Test convergent validity (related measures)"""
        from reliability_validity import ValidityValidator
        
        # Create highly correlated measures
        x = np.random.RandomState(42).normal(0, 1, 30)
        y = x + np.random.RandomState(43).normal(0, 0.2, 30)
        
        result = ValidityValidator.convergent_validity(x, y, expected_r=0.8)
        assert 'correlation' in result
        assert 'meets_threshold' in result
        assert 'status' in result
    
    def test_discriminant_validity(self):
        """Test discriminant validity (unrelated measures)"""
        from reliability_validity import ValidityValidator
        
        # Create uncorrelated measures
        x = np.random.RandomState(42).normal(0, 1, 30)
        y = np.random.RandomState(43).normal(0, 1, 30)
        
        result = ValidityValidator.discriminant_validity(x, y, expected_r=0.3)
        assert 'correlation' in result
        assert 'discriminant' in result
        assert 'status' in result


class TestConversationRunner:
    """Test conversation runner"""
    
    def test_runner_import(self):
        """Test ConversationTestRunner imports"""
        from run_conversation_test import ConversationTestRunner, SCENARIOS
        
        assert len(SCENARIOS) > 0
        runner = ConversationTestRunner(verbose=False)
        assert hasattr(runner, 'run_batch')
        assert hasattr(runner, 'export_json')
        assert hasattr(runner, 'export_csv')
    
    def test_scenario_format(self):
        """Test scenario data format"""
        from run_conversation_test import SCENARIOS
        
        for name, turns in SCENARIOS.items():
            assert isinstance(name, str)
            assert isinstance(turns, list)
            assert len(turns) > 0
            assert all(isinstance(t, str) for t in turns)


class TestResearchDashboard:
    """Test research dashboard visualization"""
    
    def test_dashboard_import(self):
        """Test ResearchDashboard imports"""
        from research_dashboard import ResearchDashboard
        
        dashboard = ResearchDashboard()
        assert hasattr(dashboard, 'plot_emotional_trajectories')
        assert hasattr(dashboard, 'plot_metrics_comparison')
        assert hasattr(dashboard, 'plot_correlation_matrix')
    
    def test_empty_data_handling(self):
        """Test dashboard handles empty data gracefully"""
        from research_dashboard import ResearchDashboard
        
        dashboard = ResearchDashboard()
        # Should not crash with no data
        assert len(dashboard.conversations) == 0


class TestNeurochemistry:
    """Test neurochemical system"""
    
    def test_neurochemistry_levels(self):
        """Test neurochemical levels are in valid range"""
        from neurochemistry import NeurochemicalSystem
        
        neuro = NeurochemicalSystem()
        levels = neuro.levels.to_dict()
        
        for chemical, level in levels.items():
            assert 0 <= level <= 1, f"{chemical} out of range: {level}"
    
    def test_neurochemistry_update(self):
        """Test neurochemical updating"""
        from neurochemistry import NeurochemicalSystem
        
        neuro = NeurochemicalSystem()
        old_dopamine = neuro.levels.dopamine
        
        neuro.update_from_emotion('joy', intensity=0.8)
        new_dopamine = neuro.levels.dopamine
        
        # Joy should increase dopamine
        assert new_dopamine > old_dopamine
    
    def test_emotional_mappings(self):
        """Test various emotion mappings"""
        from neurochemistry import NeurochemicalSystem
        
        neuro = NeurochemicalSystem()
        
        emotions = ['joy', 'sadness', 'anger', 'fear', 'neutral']
        for emotion in emotions:
            neuro.update_from_emotion(emotion, intensity=0.7)
            # Should not crash and levels should stay in bounds
            levels = neuro.levels.to_dict()
            for level in levels.values():
                assert 0 <= level <= 1


class TestIntegration:
    """Integration tests"""
    
    def test_metrics_bounds(self):
        """Test that metrics stay in valid bounds"""
        from metrics import ConsciousnessScore
        
        # Test with extreme values
        score = ConsciousnessScore(
            phi=1.0,
            global_availability=0.0,
            meta_cognitive_depth=0.5,
            temporal_binding=0.75,
            reportability=0.25,
            overall_consciousness=0.5,
            timestamp=1.0
        )
        
        d = score.to_dict()
        for key, value in d.items():
            if key != 'timestamp':
                assert 0 <= value <= 1, f"{key} out of bounds: {value}"
    
    def test_file_loading(self):
        """Test that data files can be loaded"""
        # Test that conversation_results.json exists
        results_path = Path(__file__).parent / 'conversation_results.json'
        if results_path.exists():
            with open(results_path, 'r') as f:
                data = json.load(f)
                assert isinstance(data, dict)
                assert 'conversations' in data or isinstance(data, list)


# Performance tests - Optional
class TestPerformance:
    """Performance checks (not full benchmarks without pytest-benchmark)"""
    
    def test_emotion_detection_exists(self):
        """Test emotion detection module exists"""
        try:
            from emotion_detector import EmotionDetector
            assert EmotionDetector is not None
        except ImportError:
            pytest.skip("EmotionDetector not available")
    
    def test_metrics_module_exists(self):
        """Test metrics module can be imported"""
        from metrics import ConsciousnessMetrics, ConsciousnessScore
        assert ConsciousnessMetrics is not None
        assert ConsciousnessScore is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
