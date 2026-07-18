import { useRef, useEffect } from 'react'
import { Bot, User, Loader2, MessageSquareText, Info, Volume2, VolumeX } from 'lucide-react'
import Markdown from 'react-markdown'
import ChatInput from './ChatInput'

function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-blue-600" />
      </div>
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-2">
        <Loader2 size={16} className="text-gray-400 animate-spin" />
        <span className="text-sm text-gray-500">Analyzing...</span>
      </div>
    </div>
  )
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user'

  return (
    <div className={`flex items-start gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-slate-700' : 'bg-blue-100'}`}>
        {isUser
          ? <User size={14} className="text-white" />
          : <Bot size={14} className="text-blue-600" />
        }
      </div>
      <div className={`max-w-[80%] ${isUser ? 'text-right' : ''}`}>
        <div className={`px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? 'bg-slate-800 text-white rounded-2xl rounded-br-sm'
            : 'bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-bl-sm'
        }`}>
          {isUser ? (
            <p className="m-0">{msg.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-headings:mt-3 prose-headings:mb-1 prose-p:my-1 prose-li:my-0.5 prose-pre:bg-gray-100 prose-pre:p-2 prose-code:text-xs prose-code:bg-gray-100 prose-code:px-1 prose-code:rounded">
              <Markdown>{msg.content}</Markdown>
            </div>
          )}
        </div>
        <span className="text-[10px] text-gray-400 mt-1 block px-1">{msg.time}</span>
      </div>
    </div>
  )
}

export default function ChatArea({ messages, onSend, isTyping, onToggleHistory, onToggleContext, historyOpen, contextOpen, voiceEnabled, onVoiceToggle, isSpeaking }) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const hasMessages = messages.length > 0

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-gray-200 bg-white flex-shrink-0">
        <button
          onClick={onToggleHistory}
          title="Chat History"
          className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${historyOpen ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:bg-gray-100 hover:text-gray-600'}`}
        >
          <MessageSquareText size={16} />
        </button>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-gray-800">AI Copilot</span>
          {isSpeaking && <Volume2 size={14} className="text-blue-500 animate-pulse" />}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={onVoiceToggle}
            title={voiceEnabled ? 'Disable voice' : 'Enable voice'}
            className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${voiceEnabled ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:bg-gray-100 hover:text-gray-600'}`}
          >
            {voiceEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
          </button>
          <button
            onClick={onToggleContext}
            title="Context"
            className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${contextOpen ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:bg-gray-100 hover:text-gray-600'}`}
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
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Hi, there 👋</h1>
            <p className="text-gray-500 text-sm max-w-md">
              Ask me anything about cases, suspects, or investigations.
            </p>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((msg, i) => (
              <MessageBubble key={i} msg={msg} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={onSend} voiceEnabled={voiceEnabled} />
    </div>
  )
}
