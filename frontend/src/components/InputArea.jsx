import { useState } from 'react'
import { FaPaperPlane } from 'react-icons/fa'

const InputArea = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="input-area">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message ContextLLM..."
            disabled={isLoading}
            rows={1}
            className="message-input"
          />
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="send-button"
            title="Send message"
          >
            <FaPaperPlane size={16} />
          </button>
        </div>
        <div className="input-footer">
          <p>ContextLLM can make mistakes. Consider checking important information.</p>
        </div>
      </form>
    </div>
  )
}

export default InputArea 