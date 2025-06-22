import { useState } from 'react'
import { FaCog, FaMicrophone, FaVolumeUp, FaCheck } from 'react-icons/fa'
import vapi from '../vapi'

const VoiceSettings = ({ isOpen, onClose }) => {
  const [selectedVoice, setSelectedVoice] = useState('pNInz6obpgDQGcFmaJgB')
  const [isTesting, setIsTesting] = useState(false)

  const voiceOptions = [
    { id: 'pNInz6obpgDQGcFmaJgB', name: 'Adam (Male)', provider: '11labs' },
    { id: '21m00Tcm4TlvDq8ikWAM', name: 'Rachel (Female)', provider: '11labs' },
    { id: 'AZnzlk1XvdvUeBnXmlld', name: 'Domi (Female)', provider: '11labs' },
    { id: 'EXAVITQu4vr4xnSDxMaL', name: 'Bella (Female)', provider: '11labs' },
  ]

  const handleVoiceChange = (voiceId) => {
    setSelectedVoice(voiceId)
    // Here you would update the Vapi configuration
    console.log('Voice changed to:', voiceId)
  }

  const testVoice = async () => {
    setIsTesting(true)
    
    try {
      // Create test assistant options with the selected voice
      const testAssistantOptions = {
        name: 'Voice Test Assistant',
        firstMessage: 'This is a test of the voice settings. How does this voice sound to you?',
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
              content: 'You are a voice test assistant. Respond with a brief test message.',
            },
          ],
        },
      }

      // Start a test call
      vapi.start(testAssistantOptions)
      
      // Stop the test call after 5 seconds
      setTimeout(() => {
        vapi.stop()
        setIsTesting(false)
      }, 5000)
      
    } catch (error) {
      console.error('Voice test failed:', error)
      setIsTesting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="voice-settings-overlay">
      <div className="voice-settings-modal">
        <div className="voice-settings-header">
          <h3>Voice Settings</h3>
          <button onClick={onClose} className="close-button">
            ×
          </button>
        </div>

        <div className="voice-settings-content">
          <div className="setting-group">
            <label className="setting-label">
              <FaMicrophone />
              Voice Assistant
            </label>
            <div className="voice-options">
              {voiceOptions.map((voice) => (
                <div
                  key={voice.id}
                  className={`voice-option ${selectedVoice === voice.id ? 'selected' : ''}`}
                  onClick={() => handleVoiceChange(voice.id)}
                >
                  <div className="voice-info">
                    <span className="voice-name">{voice.name}</span>
                    <span className="voice-provider">{voice.provider}</span>
                  </div>
                  {selectedVoice === voice.id && (
                    <FaCheck className="check-icon" />
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="setting-group">
            <label className="setting-label">
              <FaVolumeUp />
              Test Voice
            </label>
            <button
              onClick={testVoice}
              disabled={isTesting}
              className="test-voice-button"
            >
              {isTesting ? 'Testing Voice...' : 'Test Voice'}
            </button>
            {isTesting && (
              <p className="test-note">
                Testing voice for 5 seconds. You should hear the assistant speak.
              </p>
            )}
          </div>

          <div className="voice-settings-footer">
            <p className="settings-note">
              Voice settings are saved automatically. Make sure your microphone is enabled for voice input.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VoiceSettings 