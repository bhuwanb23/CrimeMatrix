import { Plus, ChevronDown, ChevronRight, X } from 'lucide-react'
import { useState } from 'react'

const ICON_COLORS = ['#3b82f6', '#f59e0b', '#8b5cf6', '#10b981', '#e57373', '#06b6d4', '#ec4899']

function CollapsibleSection({ title, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="chat-history-section">
      <button className="chat-history-section-header" onClick={() => setOpen(!open)}>
        {open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        {title}
      </button>
      {open && <div className="chat-history-section-body">{children}</div>}
    </div>
  )
}

function ChatItem({ item, active, onClick, onDelete }) {
  const colorIndex = Math.abs(item.session_id?.charCodeAt(0) || 0) % ICON_COLORS.length
  const color = ICON_COLORS[colorIndex]
  const initial = (item.title || 'N')[0].toUpperCase()

  return (
    <button className={`chat-history-item ${active ? 'active' : ''}`} onClick={onClick}>
      <div className="chat-history-item-icon" style={{ background: color + '18', color }}>
        {initial}
      </div>
      <span className="chat-history-item-title">{item.title || 'New Conversation'}</span>
    </button>
  )
}

export default function ChatHistory({ sessions = [], activeChatId, onSelectChat, onNewChat, onDeleteChat, onClose }) {
  const today = new Date().toDateString()
  const todaySessions = (sessions || []).filter(s => {
    const d = s.created_at ? new Date(s.created_at).toDateString() : null
    return d === today
  })
  const olderSessions = (sessions || []).filter(s => {
    const d = s.created_at ? new Date(s.created_at).toDateString() : null
    return d !== today
  })

  return (
    <div className="slide-panel-inner">
      <div className="slide-panel-header">
        <h2 className="slide-panel-title">Chat History</h2>
        <button className="slide-panel-close" onClick={onClose} aria-label="Close">
          <X size={18} strokeWidth={1.8} />
        </button>
      </div>

      <button className="chat-history-new" onClick={onNewChat}>
        <Plus size={16} strokeWidth={2} />
        New Chat
      </button>

      <div className="slide-panel-body">
        {todaySessions.length > 0 && (
          <CollapsibleSection title="Today" defaultOpen={true}>
            {todaySessions.map((chat) => (
              <ChatItem
                key={chat.session_id}
                item={chat}
                active={activeChatId === chat.session_id}
                onClick={() => onSelectChat(chat.session_id)}
              />
            ))}
          </CollapsibleSection>
        )}

        {olderSessions.length > 0 && (
          <CollapsibleSection title="Previous" defaultOpen={true}>
            {olderSessions.map((chat) => (
              <ChatItem
                key={chat.session_id}
                item={chat}
                active={activeChatId === chat.session_id}
                onClick={() => onSelectChat(chat.session_id)}
              />
            ))}
          </CollapsibleSection>
        )}

        {sessions.length === 0 && (
          <div style={{ padding: '20px', textAlign: 'center', opacity: 0.5, fontSize: '13px' }}>
            No conversations yet. Start a new chat!
          </div>
        )}
      </div>
    </div>
  )
}
