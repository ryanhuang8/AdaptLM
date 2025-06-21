import { Plus, MessageSquare, Settings, User, Trash2 } from 'lucide-react'

const Sidebar = ({ chatSessions, currentChatId, onNewChat, onSwitchChat }) => {
  const handleDeleteChat = (e, chatId) => {
    e.stopPropagation()
    // You can add delete functionality here
    console.log('Delete chat:', chatId)
  }

  return (
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
        <button className="sidebar-btn">
          <User size={16} />
          <span>Account</span>
        </button>
        <button className="sidebar-btn">
          <Settings size={16} />
          <span>Settings</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar 