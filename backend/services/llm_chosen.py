import re
from models import GPT, Gemini, Claude, Hume, GroqAI
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
    
    def should_exit_agent_mode(self, agent_response: str) -> bool:
        """Determine if we should exit agent mode and return to original LLM"""
        # Check if appointment was successfully scheduled
        if "successfully" in agent_response.lower() and "scheduled" in agent_response.lower():
            return True
        
        # Check if agent is asking for more information (stay in agent mode)
        if any(phrase in agent_response.lower() for phrase in [
            "need more information", "please provide", "what time", "what date",
            "could you clarify", "i need", "missing information"
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
            if self.detect_appointment_intent(prompt):
                print(f"🔀 Detected appointment intent, switching to agent mode")
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
                    self.agent.clear_after_scheduling()
            
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

# Backward compatibility function
def llm_response(llm_name: str, uid: str, vector_store: PineconeVectorStore, prompt: str, previous_prompt: str, previous_output: str):
    """Legacy function for backward compatibility"""
    router = LLMRouter()
    return router.llm_response(llm_name, uid, vector_store, prompt, previous_prompt, previous_output)