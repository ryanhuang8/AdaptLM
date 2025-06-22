#!/usr/bin/env python3
"""
Test script to demonstrate smart routing between LLMs and Agent
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.llm_chosen import LLMRouter
from vector_store.vector_store import PineconeVectorStore

def test_smart_routing():
    """Test the smart routing functionality"""
    print("🧪 Testing Smart Routing System...")
    
    # Create router
    router = LLMRouter()
    
    # Mock vector store (you can replace with real one)
    vector_store = None
    
    # Test 1: Regular conversation (should use LLM)
    print("\n" + "="*50)
    print("Test 1: Regular conversation")
    print("="*50)
    
    user_message = "What's the weather like today?"
    print(f"User: {user_message}")
    
    response = router.llm_response("gpt", "test_user", vector_store, user_message, "", "")
    print(f"Response: {response[:100]}...")
    
    state = router.get_conversation_state()
    print(f"State: {state}")
    
    # Test 2: Appointment request (should switch to agent)
    print("\n" + "="*50)
    print("Test 2: Appointment request")
    print("="*50)
    
    user_message = "I need to schedule an appointment for tomorrow at 3 PM"
    print(f"User: {user_message}")
    
    response = router.llm_response("gpt", "test_user", vector_store, user_message, "", "")
    print(f"Response: {response}")
    
    state = router.get_conversation_state()
    print(f"State: {state}")
    
    # Test 3: Follow-up in agent mode
    print("\n" + "="*50)
    print("Test 3: Follow-up in agent mode")
    print("="*50)
    
    user_message = "The meeting is about project review"
    print(f"User: {user_message}")
    
    response = router.llm_response("gpt", "test_user", vector_store, user_message, "", "")
    print(f"Response: {response}")
    
    state = router.get_conversation_state()
    print(f"State: {state}")
    
    # Test 4: After scheduling (should return to LLM)
    print("\n" + "="*50)
    print("Test 4: After scheduling completion")
    print("="*50)
    
    user_message = "Thanks! Now tell me about the weather"
    print(f"User: {user_message}")
    
    response = router.llm_response("gpt", "test_user", vector_store, user_message, "", "")
    print(f"Response: {response[:100]}...")
    
    state = router.get_conversation_state()
    print(f"State: {state}")

def test_keyword_detection():
    """Test keyword detection functionality"""
    print("\n" + "="*50)
    print("Testing Keyword Detection")
    print("="*50)
    
    router = LLMRouter()
    
    test_phrases = [
        "What's the weather like?",
        "Schedule a meeting",
        "Book an appointment",
        "I need to arrange something",
        "Tell me a joke",
        "Tomorrow at 2 PM",
        "Next Monday",
        "What time is it?",
        "Reserve a slot",
        "How are you doing?"
    ]
    
    for phrase in test_phrases:
        is_appointment = router.detect_appointment_intent(phrase)
        status = "🔀 APPOINTMENT" if is_appointment else "🧠 REGULAR"
        print(f"{status}: {phrase}")

if __name__ == "__main__":
    test_keyword_detection()
    test_smart_routing() 