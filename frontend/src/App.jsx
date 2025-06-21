import { useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputArea from './components/InputArea'

function App() {
  const [chatSessions, setChatSessions] = useState([
    {
      id: '1',
      title: 'New chat',
      messages: []
    }
  ])
  const [currentChatId, setCurrentChatId] = useState('1')
  const [isLoading, setIsLoading] = useState(false)

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

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        content: `This is a simulated response to: "${message}". In a real application, this would be replaced with an actual API call to your backend.`,
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
      setIsLoading(false)
    }, 1000)
  }

  return (
    <div className="app">
      <Sidebar 
        chatSessions={chatSessions}
        currentChatId={currentChatId}
        onNewChat={createNewChat}
        onSwitchChat={switchChat}
      />
      <div className="main-content">
        <ChatArea messages={currentChat?.messages || []} isLoading={isLoading} />
        <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  )
}

export default App
