import { createContext, useContext, useState, useEffect } from 'react'

const VoiceContext = createContext()

export const useVoice = () => {
  const context = useContext(VoiceContext)
  if (!context) {
    throw new Error('useVoice must be used within a VoiceProvider')
  }
  return context
}

export const fetchVoiceLLM = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/get_voice_llm')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.chosen_llm
  } catch (error) {
    console.error('Error fetching voice LLM:', error)
    // Return a default value or re-throw the error depending on your needs
    return "gpt" // or throw error if you want to handle it in the calling component
  }
}

export const fetchContext = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/get_context')
    const data = await response.json()
    return data.context
  } catch (error) {
    console.error('Error fetching context:', error)
    return ["This is a placeholder context. RAG pipeline not yet implemented."]
  }
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