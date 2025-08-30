"""
Current Agent Tests

These tests verify that the refactored agents work correctly with the new interface.
"""

import pytest
from core.agents import EvidenceVerificationAgent, ConfidenceValidatorAgent, ActiveLearningAgent


def test_evidence_verification_agent_initialization():
    """Test that EvidenceVerificationAgent can be initialized"""
    try:
        agent = EvidenceVerificationAgent(rag_base_url="http://localhost:8000")
        assert agent is not None
        assert hasattr(agent, 'verify_evidence')
        print("✅ EvidenceVerificationAgent initialization successful")
        return True
    except Exception as e:
        print(f"❌ EvidenceVerificationAgent initialization failed: {e}")
        return False


def test_confidence_validator_agent_initialization():
    """Test that ConfidenceValidatorAgent can be initialized"""
    try:
        agent = ConfidenceValidatorAgent(rag_base_url="http://localhost:8000")
        assert agent is not None
        assert hasattr(agent, 'validate_compliance')
        print("✅ ConfidenceValidatorAgent initialization successful")
        return True
    except Exception as e:
        print(f"❌ ConfidenceValidatorAgent initialization failed: {e}")
        return False


def test_active_learning_agent_initialization():
    """Test that ActiveLearningAgent can be initialized"""
    try:
        agent = ActiveLearningAgent(rag_base_url="http://localhost:8000")
        assert agent is not None
        assert hasattr(agent, 'record_correction')
        print("✅ ActiveLearningAgent initialization successful")
        return True
    except Exception as e:
        print(f"❌ ActiveLearningAgent initialization failed: {e}")
        return False


def test_agent_methods_exist():
    """Test that all expected methods exist on the agents"""
    try:
        # Evidence Verification Agent
        evidence_agent = EvidenceVerificationAgent(rag_base_url="http://localhost:8000")
        expected_evidence_methods = ['verify_evidence', 'get_verification_stats', 'get_rag_system_status']
        for method in expected_evidence_methods:
            assert hasattr(evidence_agent, method), f"Missing method: {method}"
        
        # Confidence Validator Agent
        validator_agent = ConfidenceValidatorAgent(rag_base_url="http://localhost:8000")
        expected_validator_methods = ['validate_compliance', 'get_validation_stats', 'explain_decision']
        for method in expected_validator_methods:
            assert hasattr(validator_agent, method), f"Missing method: {method}"
        
        # Active Learning Agent
        learning_agent = ActiveLearningAgent(rag_base_url="http://localhost:8000")
        expected_learning_methods = ['record_correction', 'record_feedback', 'analyze_patterns']
        for method in expected_learning_methods:
            assert hasattr(learning_agent, method), f"Missing method: {method}"
        
        print("✅ All expected agent methods exist")
        return True
    except Exception as e:
        print(f"❌ Agent method verification failed: {e}")
        return False


def test_agent_fallback_mechanism():
    """Test that agents can work without RAG service (fallback mode)"""
    try:
        # Test with invalid RAG URL to trigger fallback
        evidence_agent = EvidenceVerificationAgent(rag_base_url="http://invalid-url:9999")
        assert evidence_agent.rag_available is False
        
        validator_agent = ConfidenceValidatorAgent(rag_base_url="http://invalid-url:9999")
        assert validator_agent.rag_available is False
        
        learning_agent = ActiveLearningAgent(rag_base_url="http://invalid-url:9999")
        assert learning_agent.rag_available is False
        
        print("✅ Agent fallback mechanism working correctly")
        return True
    except Exception as e:
        print(f"❌ Agent fallback mechanism test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Running Current Agent Tests")
    print("=" * 50)
    
    test_results = []
    
    test_results.append(("Agent Initialization", test_evidence_verification_agent_initialization()))
    test_results.append(("Confidence Validator Initialization", test_confidence_validator_agent_initialization()))
    test_results.append(("Active Learning Initialization", test_active_learning_agent_initialization()))
    test_results.append(("Method Verification", test_agent_methods_exist()))
    test_results.append(("Fallback Mechanism", test_agent_fallback_mechanism()))
    
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All current agent tests passed!")
        exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above.")
        exit(1)
