import { useState, useEffect, useRef } from 'react'
import { FaMicrophone, FaMicrophoneSlash, FaVolumeUp } from 'react-icons/fa'
import { useVoice } from '../contexts/VoiceContext'
import vapi from '../vapi'

const VoiceInput = ({ onMessageReceived, isListening, setIsListening, isVoiceMode, onVoiceModeToggle, onVoiceMessage }) => {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState('')
  const [volumeLevel, setVolumeLevel] = useState(0)
  const [conversationHistory, setConversationHistory] = useState([])
  const { selectedVoice } = useVoice()

  // Assistant options for Vapi - now uses the selected voice from context
  const getAssistantOptions = () => ({
    name: 'ContextLLM Assistant',
    transcriber: {
      provider: 'deepgram',
      model: 'nova-2',
      language: 'en-US',
    },
    voice: {
      provider: '11labs',
      voiceId: selectedVoice,
    },
    model: {
      provider: 'openai',
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful AI assistant for ContextLLM. Provide clear, concise, and helpful responses to user queries.',
        },
      ],
    },
  })

  useEffect(() => {
    // Set up event listeners for Vapi
    const handleCallStart = () => {
      console.log('Call started')
      setIsListening(true)
      setError('')
      setTranscript('')
    }

    const handleCallEnd = () => {
      console.log('Call ended')
      setIsListening(false)
      setIsSpeaking(false)
      setVolumeLevel(0)
    }

    const handleSpeechStart = () => {
      console.log('Speech started')
      setIsSpeaking(true)
    }

    const handleSpeechEnd = () => {
      console.log('Speech ended')
      setIsSpeaking(false)
    }

    const handleVolumeLevel = (level) => {
      setVolumeLevel(level)
    }

    const handleMessage = (message) => {
      console.log('Message received:', message)
      
      // Handle different message types
      if (message.type === 'transcript') {
        // Handle transcript messages
        if (message.transcriptType === 'final') {
          // Final transcript - add to chat
          const chatMessage = {
            id: Date.now() + Math.random(), // Ensure unique ID
            content: message.transcript,
            role: message.role,
            timestamp: new Date()
          }
          
          // Add to conversation history
          setConversationHistory(prev => [...prev, chatMessage])
          
          // Send to parent component to add to chat
          if (onVoiceMessage) {
            onVoiceMessage(chatMessage)
          }
          
          // Update transcript display for user messages
          if (message.role === 'user') {
            setTranscript(message.transcript)
            // Don't call onMessageReceived here - it's handled by onVoiceMessage
          }
        } else if (message.transcriptType === 'partial') {
          // Partial transcript - just update display for user messages
          if (message.role === 'user') {
            setTranscript(message.transcript)
          }
        }
      } else if (message.type === 'message') {
        // Handle regular message events
        if (message.role === 'user') {
          setTranscript(message.content)
          onMessageReceived(message.content)
        }
      }
    }

    const handleError = (error) => {
      console.error('Vapi error:', error)
      setError('Voice input error. Please try again.')
      setIsListening(false)
    }

    vapi.on('call-start', handleCallStart)
    vapi.on('call-end', handleCallEnd)
    vapi.on('speech-start', handleSpeechStart)
    vapi.on('speech-end', handleSpeechEnd)
    vapi.on('volume-level', handleVolumeLevel)
    vapi.on('message', handleMessage)
    vapi.on('error', handleError)

    return () => {
      // Cleanup event listeners
      vapi.off('call-start', handleCallStart)
      vapi.off('call-end', handleCallEnd)
      vapi.off('speech-start', handleSpeechStart)
      vapi.off('speech-end', handleSpeechEnd)
      vapi.off('volume-level', handleVolumeLevel)
      vapi.off('message', handleMessage)
      vapi.off('error', handleError)
    }
  }, [onMessageReceived, setIsListening, isVoiceMode, onVoiceMessage, selectedVoice])

  const startCall = async () => {
    try {
      setError('')
      setConversationHistory([])
      vapi.start(getAssistantOptions())
    } catch (error) {
      console.error('Failed to start call:', error)
      setError('Failed to start voice input. Please check your microphone permissions.')
    }
  }

  const stopCall = async () => {
    try {
      console.log(conversationHistory)
      vapi.stop()
    } catch (error) {
      console.error('Failed to stop call:', error)
    }
  }

  const toggleVoiceInput = () => {
    if (isListening) {
      stopCall()
    } else {
      startCall()
    }
  }

  const toggleVoiceMode = () => {
    if (isListening) {
      stopCall()
    }
    onVoiceModeToggle()
  }

  return (
    <div className="voice-input-container">
      {error && (
        <div className="voice-error">
          {error}
        </div>
      )}
      
      <div className="voice-controls">
        <button
          onClick={toggleVoiceInput}
          className={`voice-button ${isListening ? 'listening' : ''} ${isSpeaking ? 'speaking' : ''}`}
          title={isListening ? 'Stop listening' : 'Start voice input'}
        >
          {isListening ? (
            <FaMicrophoneSlash size={16} />
          ) : (
            <FaMicrophone size={16} />
          )}
        </button>

        <button
          onClick={toggleVoiceMode}
          className={`voice-mode-button ${isVoiceMode ? 'active' : ''}`}
          title={isVoiceMode ? 'Disable voice mode' : 'Enable voice mode'}
        >
          <FaVolumeUp size={50} />
        </button>
      </div>

      {transcript && (
        <div className="transcript">
          <span className="transcript-label">You said:</span>
          <span className="transcript-text">{transcript}</span>
        </div>
      )}

      {isListening && (
        <div className="listening-indicator">
          <div className="pulse-dot"></div>
          <span>Listening...</span>
        </div>
      )}

      {isSpeaking && (
        <div className="speaking-indicator">
          <FaVolumeUp size={14} />
          <span>Assistant speaking...</span>
        </div>
      )}

      {volumeLevel > 0 && (
        <div className="volume-indicator">
          <div 
            className="volume-bar" 
            style={{ width: `${volumeLevel * 100}%` }}
          ></div>
        </div>
      )}

      {isVoiceMode && (
        <div className="voice-mode-indicator">
          <span>Voice Mode Active</span>
        </div>
      )}
    </div>
  )
}

export default VoiceInput 