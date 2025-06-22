import { useState } from 'react'
import './App.css'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { VoiceProvider } from './contexts/VoiceContext'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputArea from './components/InputArea'
import Login from './components/Login'

function AppContent() {
  const [chatSessions, setChatSessions] = useState([
    {
      id: '1',
      title: 'New chat',
      messages: []
    }
  ])
  const [currentChatId, setCurrentChatId] = useState('1')
  const [isLoading, setIsLoading] = useState(false)
  const { currentUser, logout } = useAuth()

  const currentChat = chatSessions.find(chat => chat.id === currentChatId)

  const createNewChat = () => {
    const newChatId = Date.now().toString()
    const newChat = {
      id: newChatId,
      title: 'New chat',
      messages: []
    }
    
    setChatSessions(prev => [newChat, ...prev])
    setCurrentChatId(newChatId)
  }

  const switchChat = (chatId) => {
    setCurrentChatId(chatId)
  }

  const updateChatTitle = (chatId, title) => {
    setChatSessions(prev => 
      prev.map(chat => 
        chat.id === chatId ? { ...chat, title } : chat
      )
    )
  }

  const handleSendMessage = async (message) => {
    // Add user message to current chat
    const userMessage = {
      id: Date.now(),
      content: message,
      role: 'user',
      timestamp: new Date()
    }
    
    setChatSessions(prev => 
      prev.map(chat => 
        chat.id === currentChatId 
          ? { 
              ...chat, 
              messages: [...chat.messages, userMessage],
              title: chat.messages.length === 0 ? message.slice(0, 30) + '...' : chat.title
            }
          : chat
      )
    )
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8080/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_prompt: message,
          uid: currentUser?.uid || 'anonymous'
        })
      })

      if (response.ok) {
        const data = await response.json()
        // Handle the response data here
        console.log('Response:', data)
        
        // Add AI response to chat (you can modify this based on your API response structure)
        const aiMessage = {
          id: Date.now() + 1,
          content: data.answer || 'Response received from server',
          role: 'assistant',
          timestamp: new Date()
        }
        
        setChatSessions(prev => 
          prev.map(chat => 
            chat.id === currentChatId 
              ? { ...chat, messages: [...chat.messages, aiMessage] }
              : chat
          )
        )
      } else {
        console.error('Failed to send message:', response.status)
        // Add error message to chat
        const errorMessage = {
          id: Date.now() + 1,
          content: 'Sorry, there was an error processing your request.',
          role: 'assistant',
          timestamp: new Date()
        }
        
        setChatSessions(prev => 
          prev.map(chat => 
            chat.id === currentChatId 
              ? { ...chat, messages: [...chat.messages, errorMessage] }
              : chat
          )
        )
      }
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        content: 'Sorry, there was an error processing your request.',
        role: 'assistant',
        timestamp: new Date()
      }
      
      setChatSessions(prev => 
        prev.map(chat => 
          chat.id === currentChatId 
            ? { ...chat, messages: [...chat.messages, errorMessage] }
            : chat
        )
      )
    }
    
    setIsLoading(false)
  }

  const handleVoiceMessage = (voiceMessage) => {
    // Check if this message already exists to prevent duplicates
    const currentMessages = chatSessions.find(chat => chat.id === currentChatId)?.messages || []
    const isDuplicate = currentMessages.some(msg => 
      msg.content === voiceMessage.content && 
      msg.role === voiceMessage.role &&
      Math.abs(msg.timestamp.getTime() - voiceMessage.timestamp.getTime()) < 1000 // Within 1 second
    )
    
    if (isDuplicate) {
      console.log('Duplicate message detected, skipping:', voiceMessage.content)
      return
    }
    
    // Add voice message to current chat
    setChatSessions(prev => 
      prev.map(chat => 
        chat.id === currentChatId 
          ? { 
              ...chat, 
              messages: [...chat.messages, voiceMessage],
              title: chat.messages.length === 0 ? voiceMessage.content.slice(0, 30) + '...' : chat.title
            }
          : chat
      )
    )
  }

  if (!currentUser) {
    return <Login />
  }

  return (
    <div className="app">
      <Sidebar 
        chatSessions={chatSessions}
        currentChatId={currentChatId}
        onNewChat={createNewChat}
        onSwitchChat={switchChat}
        onLogout={logout}
        user={currentUser}
      />
      <div className="main-content">
        <ChatArea messages={currentChat?.messages || []} isLoading={isLoading} />
        <InputArea 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading} 
          onVoiceMessage={handleVoiceMessage}
        />
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <VoiceProvider>
        <AppContent />
      </VoiceProvider>
    </AuthProvider>
  )
}

export default App
