import { User, Bot } from 'lucide-react'

const ChatArea = ({ messages, isLoading }) => {
  return (
    <div className="chat-area">
      {messages.length === 0 && !isLoading && (
        <div className="welcome-message">
          <h1>ContextLLM</h1>
          <p>How can I help you today?</p>
        </div>
      )}
      
      <div className="messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'user' ? (
                <User size={20} />
              ) : (
                <Bot size={20} />
              )}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
              <div className="message-timestamp">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">
              <Bot size={20} />
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
      </div>
    </div>
  )
}

export default ChatArea 