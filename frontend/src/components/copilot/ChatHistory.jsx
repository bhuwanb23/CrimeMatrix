import { Plus, ChevronDown, ChevronRight, X } from 'lucide-react'
import { useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateChatTitle } from '../../utils/translate'

const savedChats = [
  { id: 1, title: 'FIR #4521 Analysis', icon: 'F', color: '#3b82f6' },
  { id: 2, title: 'Suspect Network — Ravi Kumar', icon: 'S', color: '#f59e0b' },
  { id: 3, title: 'MO Pattern Research', icon: 'M', color: '#8b5cf6' },
]

const todayChats = [
  { id: 4, title: 'Cross-district case linking', icon: 'C', color: '#10b981' },
  { id: 5, title: 'Theft pattern Bengaluru North', icon: 'T', color: '#e57373' },
]

const yesterdayChats = [
  { id: 6, title: 'Whisper alert investigation', icon: 'W', color: '#f59e0b' },
  { id: 7, title: 'Evidence report generation', icon: 'E', color: '#3b82f6' },
]

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

function ChatItem({ item, active, onClick }) {
  const { lang } = useLanguage()
  return (
    <button className={`chat-history-item ${active ? 'active' : ''}`} onClick={onClick}>
      <div className="chat-history-item-icon" style={{ background: item.color + '18', color: item.color }}>
        {item.icon}
      </div>
      <span className="chat-history-item-title">{translateChatTitle(item.title, lang)}</span>
    </button>
  )
}

export default function ChatHistory({ activeChatId, onSelectChat, onNewChat, onClose }) {
  const { lang } = useLanguage()

  return (
    <div className="slide-panel-inner">
      <div className="slide-panel-header">
        <h2 className="slide-panel-title">{t('chat_history', lang)}</h2>
        <button className="slide-panel-close" onClick={onClose} aria-label="Close">
          <X size={18} strokeWidth={1.8} />
        </button>
      </div>

      <button className="chat-history-new" onClick={onNewChat}>
        <Plus size={16} strokeWidth={2} />
        {t('new_chat', lang)}
      </button>

      <div className="slide-panel-body">
        <CollapsibleSection title={t('saved', lang)} defaultOpen={true}>
          {savedChats.map((chat) => (
            <ChatItem
              key={chat.id}
              item={chat}
              active={activeChatId === chat.id}
              onClick={() => onSelectChat(chat.id)}
            />
          ))}
        </CollapsibleSection>

        <CollapsibleSection title={t('today', lang)} defaultOpen={true}>
          {todayChats.map((chat) => (
            <ChatItem
              key={chat.id}
              item={chat}
              active={activeChatId === chat.id}
              onClick={() => onSelectChat(chat.id)}
            />
          ))}
        </CollapsibleSection>

        <CollapsibleSection title={t('yesterday', lang)} defaultOpen={false}>
          {yesterdayChats.map((chat) => (
            <ChatItem
              key={chat.id}
              item={chat}
              active={activeChatId === chat.id}
              onClick={() => onSelectChat(chat.id)}
            />
          ))}
        </CollapsibleSection>
      </div>
    </div>
  )
}
