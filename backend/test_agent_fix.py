#!/usr/bin/env python3
"""
Test script to verify that the agent properly stores appointment details after scheduling
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.agent import Agent

def test_appointment_details_storage():
    """Test that appointment details are properly stored after scheduling"""
    print("🧪 Testing appointment details storage...")
    
    # Create agent
    agent = Agent()
    
    # Test with a complete appointment request
    user_message = "Schedule a meeting with John tomorrow at 2 PM for 1 hour. The topic is project review."
    
    print(f"User: {user_message}")
    response = agent.generate_text(user_message)
    print(f"Agent: {response}")
    
    # Check the appointment details
    details = agent.get_scheduled_appointment_details()
    print(f"\n📋 Stored appointment details:")
    for key, value in details.items():
        print(f"  {key}: {value}")
    
    # Check conversation summary
    summary = agent.get_conversation_summary()
    print(f"\n📊 Conversation summary:")
    print(f"  Message count: {summary['message_count']}")
    print(f"  Last messages: {len(summary['last_messages'])}")
    
    # Verify that details are not blank
    has_details = any(value is not None for value in details.values() if key != 'timezone')
    if has_details:
        print("\n✅ SUCCESS: Appointment details are properly stored!")
    else:
        print("\n❌ FAILURE: Appointment details are still blank!")
    
    return has_details

if __name__ == "__main__":
    test_appointment_details_storage() 