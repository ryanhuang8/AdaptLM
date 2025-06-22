import { useEffect, useRef } from 'react'
import { User, Bot } from 'lucide-react'

const ChatArea = ({ messages, isLoading, currentLLM }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  // Function to get the appropriate icon and color for a specific LLM
  const getLLMInfo = (llm) => {
    switch (llm) {
      case 'gpt':
        return { icon: '📘', color: '#10a37f' }
      case 'gemini':
        return { icon: '🧠', color: '#4285f4' }
      case 'claude':
        return { icon: '🤖', color: '#d97706' }
      case 'groq':
        return { icon: '⚡', color: '#7c3aed' }
      default:
        return { icon: <Bot size={20} />, color: '#10a37f' }
    }
  }

  return (
    <div className="chat-area">
      {messages.length === 0 && !isLoading && (
        <div className="welcome-message">
          <h1>AdaptLM</h1>
          <p>How can I help you today?</p>
        </div>
      )}
      
      <div className="messages">
        {messages.map((message) => {
          const llmInfo = message.role === 'assistant' ? getLLMInfo(message.llm) : null
          
          return (
            <div key={message.id} className={`message ${message.role}`}>
              <div 
                className="message-avatar"
                style={message.role === 'assistant' ? { backgroundColor: llmInfo.color } : {}}
              >
                {message.role === 'user' ? (
                  <User size={20} />
                ) : (
                  <span className="llm-icon">{llmInfo.icon}</span>
                )}
              </div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          )
        })}
        
        {isLoading && (
          <div className="message assistant">
            <div 
              className="message-avatar"
              style={{ backgroundColor: getLLMInfo(currentLLM).color }}
            >
              <span className="llm-icon">{getLLMInfo(currentLLM).icon}</span>
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          </div>
        )}
        
        {/* Invisible element to scroll to */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}

export default ChatArea 