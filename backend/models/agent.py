import ast
import json
from datetime import datetime, date
import os
import sys

from services.google_cal import ScheduleAppointmentTool
from services.emailing import SendEmailTool

# Updated Agent class to use both scheduling and emailing tools
class Agent:
    SYSTEM_PROMPT = """
    Today's date is 6/22/2025.
    You are a helpful assistant that can schedule appointments and send emails.
    
    You can help with two main tasks however you can only EXECUTE ONE AT A TIME:
    
    1. SCHEDULING APPOINTMENTS:
    Required information for scheduling:
    - Date (year, month, day)
    - Start time (hour, minute)
    - End time (hour, minute)  
    - Summary/title of the appointment
    - Description (optional)
    
    2. SENDING EMAILS:
    Required information for sending emails:
    - Recipient email address
    - Subject line
    - Email body content
    
    Use the schedule_appointment function when you have all required appointment information.
    Use the send_email function when you have all required email information.
    
    IMPORTANT: Remember the conversation context and use information from previous messages
    to fill out details. If the user provides information in multiple messages,
    combine them to create complete information.
    """
    
    def __init__(self):
        from openai import OpenAI
        import os
        print(os.getenv("OPENAI_API_KEY"))
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schedule_tool = ScheduleAppointmentTool()
        self.email_tool = SendEmailTool()
        
        # Store conversation context
        self.conversation_history = []
        self.current_appointment_details = {
            'summary': None,
            'description': None,
            'date': None,
            'start_time': None,
            'end_time': None,
            'timezone': 'America/New_York'
        }
        self.current_email_details = {
            'to': None,
            'subject': None,
            'body': None
        }
        
    def add_to_conversation(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_conversation_context(self) -> str:
        """Get a summary of the conversation context for the AI"""
        if not self.conversation_history:
            return ""
        
        context = "Previous conversation:\n"
        for i, message in enumerate(self.conversation_history[-5:], 1):  # Last 5 messages
            context += f"{i}. {message['role'].title()}: {message['content']}\n"
        
        # Add current appointment details
        context += "\nCurrent appointment details:\n"
        for key, value in self.current_appointment_details.items():
            if value is not None:
                context += f"- {key}: {value}\n"
        
        # Add current email details
        context += "\nCurrent email details:\n"
        for key, value in self.current_email_details.items():
            if value is not None:
                context += f"- {key}: {value}\n"
        
        return context
        
    def generate_text(self, prompt: str) -> str:
        # Add user message to conversation history
        self.add_to_conversation('user', prompt)
        
        # Get conversation context
        context = self.get_conversation_context()
        
        # Create enhanced prompt with context
        enhanced_prompt = f"{context}\n\nCurrent user message: {prompt}"
        
        tools = [self.schedule_tool.to_openai_tool(), self.email_tool.to_openai_tool()]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            tools=tools,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ]
        )
        
        message = response.choices[0].message
        
        # Handle tool calls
        if message.tool_calls:
            tool_results = []
            for tool_call in message.tool_calls:
                if tool_call.function.name == "schedule_appointment":
                    # Parse the function arguments
                    args = json.loads(tool_call.function.arguments)
                    
                    # Store the appointment details before clearing
                    self.current_appointment_details.update({
                        'summary': args.get('summary'),
                        'description': args.get('description'),
                        'start_time': args.get('start_time'),
                        'end_time': args.get('end_time'),
                        'timezone': args.get('timezone', 'America/New_York')
                    })
                    
                    result = self.schedule_tool.execute(**args)
                    tool_results.append(result)
                    
                elif tool_call.function.name == "send_email":
                    # Parse the function arguments
                    args = json.loads(tool_call.function.arguments)
                    
                    # Store the email details before clearing
                    self.current_email_details.update({
                        'to': args.get('to'),
                        'subject': args.get('subject'),
                        'body': args.get('body')
                    })
                    
                    result = self.email_tool.execute(**args)
                    tool_results.append(result)
            
            if tool_results:
                response_text = "\n".join(tool_results)
                self.add_to_conversation('assistant', response_text)
                return response_text
        
        # Add assistant response to conversation history
        response_text = message.content or "I need more information to help you."
        self.add_to_conversation('assistant', response_text)
        return response_text
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the current conversation state"""
        return {
            'message_count': len(self.conversation_history),
            'current_appointment_details': self.current_appointment_details.copy(),
            'last_messages': self.conversation_history[-3:] if self.conversation_history else []
        }
    
    def reset_conversation(self):
        """Reset the conversation history and appointment details"""
        self.conversation_history = []
        self.current_appointment_details = {
            'summary': None,
            'description': None,
            'date': None,
            'start_time': None,
            'end_time': None,
            'timezone': 'America/New_York'
        }
        self.current_email_details = {
            'to': None,
            'subject': None,
            'body': None
        }
    
    def clear_after_scheduling(self):
        """Clear conversation history and appointment details after successful scheduling"""
        self.conversation_history = []
        self.current_appointment_details = {
            'summary': None,
            'description': None,
            'date': None,
            'start_time': None,
            'end_time': None,
            'timezone': 'America/New_York'
        }
        self.current_email_details = {
            'to': None,
            'subject': None,
            'body': None
        }
    
    def clear_after_emailing(self):
        """Clear conversation history and email details after successful email sending"""
        self.conversation_history = []
        self.current_appointment_details = {
            'summary': None,
            'description': None,
            'date': None,
            'start_time': None,
            'end_time': None,
            'timezone': 'America/New_York'
        }
        self.current_email_details = {
            'to': None,
            'subject': None,
            'body': None
        }
    
    def get_scheduled_appointment_details(self) -> dict:
        """Get the details of the last scheduled appointment"""
        return self.current_appointment_details.copy()
    
    def get_sent_email_details(self) -> dict:
        """Get the details of the last sent email"""
        return self.current_email_details.copy()
