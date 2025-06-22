import { createContext, useContext, useState, useEffect } from 'react'

const VoiceContext = createContext()

export const useVoice = () => {
  const context = useContext(VoiceContext)
  if (!context) {
    throw new Error('useVoice must be used within a VoiceProvider')
  }
  return context
}

export const VoiceProvider = ({ children }) => {
  const [selectedVoice, setSelectedVoice] = useState('pNInz6obpgDQGcFmaJgB') // Default to Adam voice

  const voiceOptions = [
    { id: 'pNInz6obpgDQGcFmaJgB', name: 'Adam (Male)', provider: '11labs' },
    { id: '21m00Tcm4TlvDq8ikWAM', name: 'Rachel (Female)', provider: '11labs' },
    { id: 'AZnzlk1XvdvUeBnXmlld', name: 'Domi (Female)', provider: '11labs' },
    { id: 'EXAVITQu4vr4xnSDxMaL', name: 'Bella (Female)', provider: '11labs' },
  ]

  const updateVoice = (voiceId) => {
    setSelectedVoice(voiceId)
    // Save to localStorage for persistence
    localStorage.setItem('selectedVoice', voiceId)
  }

  // Load saved voice on mount
  useEffect(() => {
    const savedVoice = localStorage.getItem('selectedVoice')
    if (savedVoice) {
      setSelectedVoice(savedVoice)
    }
  }, [])

  const value = {
    selectedVoice,
    voiceOptions,
    updateVoice
  }

  return (
    <VoiceContext.Provider value={value}>
      {children}
    </VoiceContext.Provider>
  )
} 