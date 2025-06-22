import { useState } from 'react'
import { Plus, MessageSquare, Settings, User, Trash2, LogOut, Mic } from 'lucide-react'
import { useVoice } from '../contexts/VoiceContext'
import VoiceSettings from './VoiceSettings'

const Sidebar = ({ chatSessions, currentChatId, onNewChat, onSwitchChat, onLogout, user }) => {
  const [showVoiceSettings, setShowVoiceSettings] = useState(false)
  const { selectedVoice, voiceOptions } = useVoice()

  const currentVoice = voiceOptions.find(voice => voice.id === selectedVoice)

  const handleDeleteChat = (e, chatId) => {
    e.stopPropagation()
    // You can add delete functionality here
    console.log('Delete chat:', chatId)
  }

  return (
    <>
      <div className="sidebar">
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={onNewChat}>
            <Plus size={16} />
            New chat
          </button>
        </div>
        
        <div className="conversations">
          {chatSessions.map((chat) => (
            <div 
              key={chat.id} 
              className={`conversation-item ${chat.id === currentChatId ? 'active' : ''}`}
              onClick={() => onSwitchChat(chat.id)}
            >
              <MessageSquare size={16} />
              <span className="conversation-title" title={chat.title}>
                {chat.title}
              </span>
              {chat.messages.length > 0 && (
                <button 
                  className="delete-chat-btn"
                  onClick={(e) => handleDeleteChat(e, chat.id)}
                  title="Delete chat"
                >
                  <Trash2 size={14} />
                </button>
              )}
            </div>
          ))}
        </div>
        
        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.photoURL ? (
                <img src={user.photoURL} alt="User avatar" />
              ) : (
                <User size={16} />
              )}
            </div>
            <div className="user-details">
              <span className="user-name">{user?.displayName || user?.email}</span>
              <span className="user-email">{user?.email}</span>
            </div>
          </div>
          <button className="sidebar-btn" onClick={() => setShowVoiceSettings(true)}>
            <Mic size={16} />
            <span>Voice: {currentVoice?.name || 'Adam'}</span>
          </button>
          <button className="sidebar-btn" onClick={onLogout}>
            <LogOut size={16} />
            <span>Logout</span>
          </button>
          <button className="sidebar-btn">
            <Settings size={16} />
            <span>Settings</span>
          </button>
        </div>
      </div>

      <VoiceSettings 
        isOpen={showVoiceSettings}
        onClose={() => setShowVoiceSettings(false)}
      />
    </>
  )
}

export default Sidebar 