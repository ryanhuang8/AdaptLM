import { Plus, MessageSquare, Settings, User } from 'lucide-react'

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <button className="new-chat-btn">
          <Plus size={16} />
          New chat
        </button>
      </div>
      
      <div className="conversations">
        <div className="conversation-item">
          <MessageSquare size={16} />
          <span>Previous conversation</span>
        </div>
        <div className="conversation-item">
          <MessageSquare size={16} />
          <span>Another chat</span>
        </div>
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