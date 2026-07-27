import { useRef, useEffect } from 'react'
import { Bot, User, Loader2, MessageSquareText, Info, Volume2, VolumeX } from 'lucide-react'
import Markdown from 'react-markdown'
import ChatInput from './ChatInput'
import { useLanguage } from '../../context/LanguageContext'

function TypingIndicator({ t }) {
  return (
    <div className="flex items-start gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-[var(--bg-active)] flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-[var(--color-accent-dark)]" />
      </div>
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-2">
        <Loader2 size={16} className="text-[var(--text-muted)] animate-spin" />
        <span className="text-sm text-[var(--text-muted)]">{t('Analyzing...')}</span>
      </div>
    </div>
  )
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user'

  return (
    <div className={`flex items-start gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-[var(--btn-primary-bg)]' : 'bg-[var(--bg-active)]'}`}>
        {isUser
          ? <User size={14} className="text-[var(--btn-primary-fg)]" />
          : <Bot size={14} className="text-[var(--color-accent-dark)]" />
        }
      </div>
      <div className={`max-w-[80%] ${isUser ? 'text-right' : ''}`}>
        <div className={`px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? 'bg-[var(--btn-primary-bg)] text-[var(--btn-primary-fg)] rounded-2xl rounded-br-sm'
            : 'bg-[var(--bg-card)] border border-[var(--border)] text-[var(--text-primary)] rounded-2xl rounded-bl-sm'
        }`}>
          {isUser ? (
            <p className="m-0">{msg.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-headings:mt-3 prose-headings:mb-1 prose-p:my-1 prose-li:my-0.5 prose-pre:bg-[var(--bg-input)] prose-pre:p-2 prose-code:text-xs prose-code:bg-[var(--bg-input)] prose-code:px-1 prose-code:rounded">
              <Markdown>{msg.content}</Markdown>
            </div>
          )}
        </div>
        <span className="text-[10px] text-[var(--text-muted)] mt-1 block px-1">{msg.time}</span>
      </div>
    </div>
  )
}

export default function ChatArea({ messages, onSend, isTyping, onToggleHistory, onToggleContext, historyOpen, contextOpen, voiceEnabled, onVoiceToggle, isSpeaking }) {
  const { t } = useLanguage()
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const hasMessages = messages.length > 0

  return (
    <div className="flex flex-col h-full bg-[var(--bg-muted)]">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-[var(--border)] bg-[var(--bg-card)] flex-shrink-0">
        <button
          onClick={onToggleHistory}
          title={t('Chat History')}
          className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${historyOpen ? 'bg-blue-50 text-blue-600' : 'text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-secondary)]'}`}
        >
          <MessageSquareText size={16} />
        </button>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-[var(--text-primary)]">{t('AI Copilot')}</span>
          {isSpeaking && <Volume2 size={14} className="text-blue-500 animate-pulse" />}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={onVoiceToggle}
            title={voiceEnabled ? t('Disable voice') : t('Enable voice')}
            className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${voiceEnabled ? 'bg-blue-50 text-blue-600' : 'text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-secondary)]'}`}
          >
            {voiceEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
          </button>
          <button
            onClick={onToggleContext}
            title={t('Context')}
            className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${contextOpen ? 'bg-blue-50 text-blue-600' : 'text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-secondary)]'}`}
          >
            <Info size={16} />
          </button>
        </div>
      </div>

      {/* Messages / Empty State */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {!hasMessages ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
              <Bot size={32} className="text-blue-500" />
            </div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">{t('Hi, there 👋')}</h1>
            <p className="text-[var(--text-muted)] text-sm max-w-md">
              {t('Ask me anything about cases, suspects, or investigations.')}
            </p>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((msg, i) => (
              <MessageBubble key={i} msg={msg} />
            ))}
            {isTyping && <TypingIndicator t={t} />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={onSend} voiceEnabled={voiceEnabled} />
    </div>
  )
}

