import { useState } from 'react'
import { FaPaperPlane } from 'react-icons/fa'
import VoiceInput from './VoiceInput'

const InputArea = ({ onSendMessage, isLoading, onVoiceMessage }) => {
  const [message, setMessage] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [isVoiceMode, setIsVoiceMode] = useState(false)

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

  const handleVoiceMessage = (transcript) => {
    if (transcript.trim() && !isLoading) {
      onSendMessage(transcript.trim())
    }
  }

  const handleVoiceModeToggle = () => {
    setIsVoiceMode(!isVoiceMode)
  }

  const handleVoiceMessageFromVapi = (voiceMessage) => {
    // Pass voice messages from Vapi to parent component
    if (onVoiceMessage) {
      onVoiceMessage(voiceMessage)
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
            placeholder={isVoiceMode ? "Voice mode active - use microphone to speak" : "Message ContextLLM..."}
            disabled={isLoading || isListening}
            rows={1}
            className={`message-input ${isVoiceMode ? 'voice-mode' : ''}`}
          />
          <div className="input-buttons">
            <VoiceInput 
              onMessageReceived={handleVoiceMessage}
              isListening={isListening}
              setIsListening={setIsListening}
              isVoiceMode={isVoiceMode}
              onVoiceModeToggle={handleVoiceModeToggle}
              onVoiceMessage={handleVoiceMessageFromVapi}
            />
            <button
              type="submit"
              disabled={!message.trim() || isLoading || isListening}
              className="send-button"
              title="Send message"
            >
              <FaPaperPlane size={16} />
            </button>
          </div>
        </div>
        <div className="input-footer">
          <p>ContextLLM can make mistakes. Consider checking important information.</p>
          {isVoiceMode && (
            <p className="voice-mode-note">
              Voice mode is active. Click the microphone to start speaking.
            </p>
          )}
        </div>
      </form>
    </div>
  )
}

export default InputArea 