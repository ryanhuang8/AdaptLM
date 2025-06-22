#!/usr/bin/env python3
"""
Comprehensive test script for the smart routing system
"""

import os
import sys
import time

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.llm_chosen import LLMRouter

def simulate_conversation():
    """Simulate a realistic conversation flow"""
    print("🎭 Simulating Smart Routing Conversation")
    print("="*60)
    
    # Create router
    router = LLMRouter()
    
    # Mock vector store
    vector_store = None
    
    # Conversation flow
    conversation = [
        {
            "user": "Hi! How are you doing today?",
            "expected_mode": "LLM",
            "description": "Regular greeting"
        },
        {
            "user": "I need to schedule a meeting with my team",
            "expected_mode": "Agent",
            "description": "Appointment request"
        },
        {
            "user": "It's for tomorrow at 2 PM",
            "expected_mode": "Agent", 
            "description": "Providing time details"
        },
        {
            "user": "The topic is quarterly planning",
            "expected_mode": "Agent",
            "description": "Providing meeting topic"
        },
        {
            "user": "Thanks! Now can you tell me a joke?",
            "expected_mode": "LLM",
            "description": "Back to regular conversation"
        },
        {
            "user": "What's the weather like?",
            "expected_mode": "LLM",
            "description": "Another regular question"
        }
    ]
    
    for i, turn in enumerate(conversation, 1):
        print(f"\n🔄 Turn {i}: {turn['description']}")
        print(f"User: {turn['user']}")
        
        # Get response
        response = router.llm_response("gpt", "test_user", vector_store, turn['user'], "", "")
        
        # Get state
        state = router.get_conversation_state()
        current_mode = "Agent" if state['is_in_agent_mode'] else "LLM"
        
        print(f"Mode: {current_mode} (Expected: {turn['expected_mode']})")
        print(f"Response: {response[:200]}...")
        print(f"State: {state}")
        
        # Small delay for readability
        time.sleep(1)

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n" + "="*60)
    print("🧪 Testing Edge Cases")
    print("="*60)
    
    router = LLMRouter()
    vector_store = None
    
    # Test 1: Ambiguous time reference
    print("\n1. Ambiguous time reference:")
    response = router.llm_response("gpt", "test_user", vector_store, "I have a meeting later", "", "")
    state = router.get_conversation_state()
    print(f"Response: {response[:100]}...")
    print(f"Mode: {'Agent' if state['is_in_agent_mode'] else 'LLM'}")
    
    # Test 2: False positive keywords
    print("\n2. False positive keywords:")
    response = router.llm_response("gpt", "test_user", vector_store, "I booked a flight yesterday", "", "")
    state = router.get_conversation_state()
    print(f"Response: {response[:100]}...")
    print(f"Mode: {'Agent' if state['is_in_agent_mode'] else 'LLM'}")
    
    # Test 3: Reset functionality
    print("\n3. Testing reset:")
    router.reset_conversation_state()
    state = router.get_conversation_state()
    print(f"State after reset: {state}")

def test_keyword_expansion():
    """Test various appointment-related keywords"""
    print("\n" + "="*60)
    print("🔍 Testing Keyword Detection")
    print("="*60)
    
    router = LLMRouter()
    
    test_cases = [
        "schedule a call",
        "book an appointment", 
        "reserve a slot",
        "arrange a meeting",
        "set up a call",
        "organize a session",
        "tomorrow at 3",
        "next Monday",
        "this Friday",
        "2:30 PM",
        "morning meeting",
        "afternoon session",
        "evening call"
    ]
    
    for test_case in test_cases:
        is_appointment = router.detect_appointment_intent(test_case)
        status = "✅ APPOINTMENT" if is_appointment else "❌ REGULAR"
        print(f"{status}: {test_case}")

if __name__ == "__main__":
    test_keyword_expansion()
    test_edge_cases()
    simulate_conversation()
    
    print("\n" + "="*60)
    print("🎉 Smart Routing Test Complete!")
    print("="*60) 