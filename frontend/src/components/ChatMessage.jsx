import { Bot, User } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function ChatMessage({ role, content, time }) {
  const { lang } = useLanguage()
  const isUser = role === 'user'

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className="chat-message-avatar">
        {isUser ? (
          <div className="chat-avatar-user"><User size={14} strokeWidth={2} /></div>
        ) : (
          <div className="chat-avatar-bot"><Bot size={14} strokeWidth={2} /></div>
        )}
      </div>
      <div className="chat-message-body">
        <div className="chat-message-bubble">
          <p>{content}</p>
        </div>
        <span className="chat-message-time">{time}</span>
      </div>
    </div>
  )
}
