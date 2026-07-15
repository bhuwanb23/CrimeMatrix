import { useRef, useEffect } from 'react'
import { Bot, User, Loader2, MessageSquareText, Info } from 'lucide-react'
import ChatInput from './ChatInput'

function TypingIndicator() {
  return (
    <div className="chat-message assistant">
      <div className="chat-message-avatar">
        <div className="chat-avatar-bot"><Bot size={14} strokeWidth={2} /></div>
      </div>
      <div className="chat-message-body">
        <div className="chat-message-bubble typing-bubble">
          <Loader2 size={16} className="typing-spinner" />
          <span>Analyzing...</span>
        </div>
      </div>
    </div>
  )
}

export default function ChatArea({ messages, onSend, isTyping, onToggleHistory, onToggleContext, historyOpen, contextOpen }) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const hasMessages = messages.length > 0

  return (
    <div className="chat-area">
      {/* Toolbar */}
      <div className="chat-toolbar">
        <button
          className={`chat-toolbar-btn ${historyOpen ? 'active' : ''}`}
          onClick={onToggleHistory}
          aria-label="Toggle chat history"
        >
          <MessageSquareText size={18} strokeWidth={1.8} />
        </button>

        <div className="chat-toolbar-center">
          <Bot size={18} strokeWidth={1.8} className="chat-toolbar-icon" />
          <span className="chat-toolbar-title">AI Copilot</span>
        </div>

        <button
          className={`chat-toolbar-btn ${contextOpen ? 'active' : ''}`}
          onClick={onToggleContext}
          aria-label="Toggle context panel"
        >
          <Info size={18} strokeWidth={1.8} />
        </button>
      </div>

      {/* Messages / Empty State */}
      <div className="chat-area-scroll">
        {!hasMessages ? (
          <div className="chat-empty">
            <div className="chat-empty-avatar">
              <Bot size={32} strokeWidth={1.5} />
            </div>
            <h1 className="chat-empty-title">Hi, there 👋</h1>
            <p className="chat-empty-subtitle">
              Ask me anything about cases, suspects, or investigations.
            </p>
          </div>
        ) : (
          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`chat-message ${msg.role}`}>
                <div className="chat-message-avatar">
                  {msg.role === 'user' ? (
                    <div className="chat-avatar-user"><User size={14} strokeWidth={2} /></div>
                  ) : (
                    <div className="chat-avatar-bot"><Bot size={14} strokeWidth={2} /></div>
                  )}
                </div>
                <div className="chat-message-body">
                  <div className="chat-message-bubble">
                    <p>{msg.content}</p>
                  </div>
                  <span className="chat-message-time">{msg.time}</span>
                </div>
              </div>
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={onSend} />
    </div>
  )
}
