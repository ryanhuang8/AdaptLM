import re
from models import GPT, Gemini, Claude, GroqAI
from models.agent import Agent
from vector_store import PineconeVectorStore

class LLMRouter:
    def __init__(self):
        # Keywords that trigger agent routing
        self.appointment_keywords = [
            'appointment', 'schedule', 'booking', 'meeting', 'calendar',
            'reserve', 'book', 'arrange', 'set up', 'organize',
            'tomorrow', 'next week', 'this week', 'today at',
            '2 pm', '3 pm', '4 pm', '5 pm', 'morning', 'afternoon', 'evening'
        ]
        
        # Keywords that trigger email routing
        self.email_keywords = [
            'email', 'send email', 'mail'
        ]
        
        # Initialize agent
        self.agent = Agent()
        
        # Track conversation state
        self.conversation_state = {
            'is_in_agent_mode': False,
            'original_llm': None,
            'agent_conversation_count': 0,
            'last_user_message': None
        }
    
    def detect_appointment_intent(self, prompt: str) -> bool:
        """Detect if the user wants to schedule an appointment"""
        prompt_lower = prompt.lower()
        
        # Check for appointment-related keywords
        for keyword in self.appointment_keywords:
            if keyword in prompt_lower:
                return True
        
        # Check for time patterns
        time_patterns = [
            r'\d{1,2}:\d{2}\s*(am|pm|AM|PM)?',
            r'\d{1,2}\s*(am|pm|AM|PM)',
            r'tomorrow',
            r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'this\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, prompt_lower):
                return True
        
        return False
    
    def detect_email_intent(self, prompt: str) -> bool:
        """Detect if the user wants to send an email"""
        prompt_lower = prompt.lower()
        
        # Check for email-related keywords
        for keyword in self.email_keywords:
            if keyword in prompt_lower:
                return True
        
        return False
    
    def should_exit_agent_mode(self, agent_response: str) -> bool:
        """Determine if we should exit agent mode and return to original LLM"""
        # Check if appointment was successfully scheduled
        if "successfully" in agent_response.lower() and "scheduled" in agent_response.lower():
            return True
        
        # Check if email was successfully sent
        if "successfully" in agent_response.lower() and "sent" in agent_response.lower() and "email" in agent_response.lower():
            return True
        
        # Check if agent is asking for more information (stay in agent mode)
        if any(phrase in agent_response.lower() for phrase in [
            "need more information", "please provide", "what time", "what date",
            "could you clarify", "i need", "missing information", "who should i send",
            "what should the subject be", "what should i write"
        ]):
            return False
        
        # Check if we've been in agent mode for too long (prevent infinite loops)
        if self.conversation_state['agent_conversation_count'] > 5:
            return True
        
        return False
    
    def llm_response(self, llm_name: str, uid: str, vector_store: PineconeVectorStore, 
                    prompt: str, previous_prompt: str, previous_output: str):
        """Enhanced LLM response with automatic agent routing"""
        
        # Store the original LLM if not already set
        if not self.conversation_state['original_llm']:
            self.conversation_state['original_llm'] = llm_name
        
        # Check if we should enter agent mode
        if not self.conversation_state['is_in_agent_mode']:
            if self.detect_appointment_intent(prompt) or self.detect_email_intent(prompt):
                print(f"🔀 Detected appointment or email intent, switching to agent mode")
                self.conversation_state['is_in_agent_mode'] = True
                self.conversation_state['agent_conversation_count'] = 0
        
        # Handle agent mode
        if self.conversation_state['is_in_agent_mode']:
            self.conversation_state['agent_conversation_count'] += 1
            print(f"🤖 Agent mode (conversation #{self.conversation_state['agent_conversation_count']})")
            
            # Get response from agent
            agent_response = self.agent.generate_text(prompt)
            
            # Check if we should exit agent mode
            if self.should_exit_agent_mode(agent_response):
                print(f"🔄 Exiting agent mode, returning to {self.conversation_state['original_llm']}")
                self.conversation_state['is_in_agent_mode'] = False
                self.conversation_state['agent_conversation_count'] = 0
                
                # Clear agent conversation after successful scheduling
                if "successfully" in agent_response.lower() and "scheduled" in agent_response.lower():
                    # Convert appointment details to text format for vector store
                    appointment_text = self._format_appointment_for_vector_store()
                    if appointment_text:
                        vector_store.upsert_texts([appointment_text])
                    self.agent.clear_after_scheduling()
                
                # Clear agent conversation after successful email sending
                elif "successfully" in agent_response.lower() and "sent" in agent_response.lower() and "email" in agent_response.lower():
                    # Convert email details to text format for vector store
                    email_text = self._format_email_for_vector_store()
                    if email_text:
                        vector_store.upsert_texts([email_text])
                    self.agent.clear_after_emailing()
            
            return agent_response
        
        # Handle regular LLM mode
        else:
            print(f"🧠 Using {llm_name} LLM")
            
            # Route to appropriate LLM
            if llm_name == "gpt":
                llm = GPT(llm_name, uid, vector_store, previous_prompt, previous_output)
            elif llm_name == "gemini":
                llm = Gemini(llm_name, uid, vector_store, previous_prompt, previous_output)
            elif llm_name == "claude":
                llm = Claude(llm_name, uid, vector_store, previous_prompt, previous_output)
            elif llm_name == "groq":
                llm = GroqAI(llm_name, uid, vector_store, previous_prompt, previous_output)
            else:
                raise ValueError(f"Invalid LLM name: {llm_name}")
            
            return llm.generate_text(prompt)
    
    def get_conversation_state(self) -> dict:
        """Get current conversation state"""
        return self.conversation_state.copy()
    
    def reset_conversation_state(self):
        """Reset conversation state"""
        self.conversation_state = {
            'is_in_agent_mode': False,
            'original_llm': None,
            'agent_conversation_count': 0,
            'last_user_message': None
        }
        self.agent.reset_conversation()
    
    def _format_appointment_for_vector_store(self) -> str:
        """Format appointment details as text for vector store storage"""
        details = self.agent.current_appointment_details
        if not details or not details.get('summary'):
            return ""
        
        # Format appointment details as a readable text
        appointment_text = f"Appointment: {details.get('summary', 'No title')}"
        
        if details.get('description'):
            appointment_text += f"\nDescription: {details.get('description')}"
        
        if details.get('date'):
            appointment_text += f"\nDate: {details.get('date')}"
        
        if details.get('start_time'):
            appointment_text += f"\nStart Time: {details.get('start_time')}"
        
        if details.get('end_time'):
            appointment_text += f"\nEnd Time: {details.get('end_time')}"
        
        if details.get('timezone'):
            appointment_text += f"\nTimezone: {details.get('timezone')}"
        
        return appointment_text

    def _format_email_for_vector_store(self) -> str:
        """Format email details as text for vector store storage"""
        details = self.agent.current_email_details
        if not details or not details.get('to'):
            return ""
        
        # Format email details as a readable text
        email_text = f"Email sent to: {details.get('to', 'Unknown recipient')}"
        
        if details.get('subject'):
            email_text += f"\nSubject: {details.get('subject')}"
        
        if details.get('body'):
            email_text += f"\nBody: {details.get('body')}"
        
        return email_text

# Backward compatibility function
def llm_response(llm_name: str, uid: str, vector_store: PineconeVectorStore, prompt: str, previous_prompt: str, previous_output: str):
    """Legacy function for backward compatibility"""
    router = LLMRouter()
    return router.llm_response(llm_name, uid, vector_store, prompt, previous_prompt, previous_output)