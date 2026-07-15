import { useRef, useEffect } from 'react'
import { Bot, User, Loader2, MessageSquareText, Info, X } from 'lucide-react'
import { AssistantCard, TasksCard, PromptCard } from './SuggestionCard'
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

            <div className="chat-suggestions">
              <AssistantCard />
              <TasksCard onSend={(task) => onSend(task, 'All Sources')} />
              <PromptCard onSend={(prompt) => onSend(prompt, 'All Sources')} />
            </div>

            <div className="chat-quick-actions">
              <button className="chat-quick-action" onClick={() => onSend('Show me FIR database', 'FIR Database')}>
                <span className="chat-quick-action-icon" style={{ background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' }}>📋</span>
                FIR Database
              </button>
              <button className="chat-quick-action" onClick={() => onSend('Analyze this case', 'All Sources')}>
                <span className="chat-quick-action-icon" style={{ background: 'rgba(139, 92, 246, 0.1)', color: '#8b5cf6' }}>🔍</span>
                Case Analysis
              </button>
              <button className="chat-quick-action" onClick={() => onSend('Browse evidence', 'Evidence')}>
                <span className="chat-quick-action-icon" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981' }}>📁</span>
                Evidence Browse
              </button>
              <button className="chat-quick-action" onClick={() => onSend('Show shared investigations', 'All Sources')}>
                <span className="chat-quick-action-icon" style={{ background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>🔗</span>
                Shared Cases
              </button>
            </div>
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
