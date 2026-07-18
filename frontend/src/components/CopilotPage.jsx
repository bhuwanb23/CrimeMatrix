import { useState, useCallback, useEffect } from 'react'
import { Volume2, VolumeX } from 'lucide-react'
import ChatArea from './copilot/ChatArea'
import ChatHistory from './copilot/ChatHistory'
import ContextPanel from './copilot/ContextPanel'
import { chat, chatStream, listSessions, getSession, deleteSession, deleteAllSessions, togglePin, searchSessions, exportSession } from '../services/copilot'
import { speak, stopSpeaking, isTTSSupported } from '../services/voice'

export default function CopilotPage() {
  const [activeChatId, setActiveChatId] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [contextOpen, setContextOpen] = useState(false)
  const [sessions, setSessions] = useState([])
  const [voiceEnabled, setVoiceEnabled] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [language, setLanguage] = useState('en')

  const loadSessions = useCallback(async () => {
    try {
      const result = await listSessions()
      setSessions(result.data || [])
    } catch (e) {
      console.error('Failed to load sessions:', e)
    }
  }, [])

  useEffect(() => { loadSessions() }, [loadSessions])

  const loadConversation = useCallback(async (sid) => {
    try {
      const result = await getSession(sid)
      if (result.data) {
        setSessionId(sid)
        setActiveChatId(sid)
        setMessages(result.data.messages || [])
      }
    } catch (e) {
      console.error('Failed to load conversation:', e)
    }
  }, [])

  const handleSend = useCallback(async (content, source) => {
    const userMsg = {
      role: 'user',
      content,
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
    }
    setMessages(prev => [...prev, userMsg])
    setIsTyping(true)

    // Add empty assistant message for streaming
    const streamMsg = {
      role: 'assistant',
      content: '',
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      streaming: true,
    }
    setMessages(prev => [...prev, streamMsg])
    const msgIdx = messages.length + 1

    try {
      chatStream(content, sessionId, 'default', language,
        (chunk) => {
          setMessages(prev => {
            const updated = [...prev]
            if (updated[msgIdx]) {
              updated[msgIdx] = { ...updated[msgIdx], content: updated[msgIdx].content + chunk }
            }
            return updated
          })
        },
        () => {
          setMessages(prev => {
            const updated = [...prev]
            if (updated[msgIdx]) {
              updated[msgIdx] = { ...updated[msgIdx], streaming: false }
            }
            return updated
          })
          setIsTyping(false)
        }
      )
    } catch (e) {
      setMessages(prev => {
        const updated = [...prev]
        if (updated[msgIdx]) {
          updated[msgIdx] = { ...updated[msgIdx], content: 'Sorry, I encountered an error.', streaming: false }
        }
        return updated
      })
      setIsTyping(false)
    }
  }, [sessionId, language])

  const handleNewChat = () => {
    setMessages([])
    setActiveChatId(null)
    setSessionId(null)
    stopSpeaking()
    setIsSpeaking(false)
    loadSessions()
  }

  const handleDeleteAll = async () => {
    if (!confirm('Delete all conversations? This cannot be undone.')) return
    try { await deleteAllSessions() } catch (e) {}
    setMessages([])
    setActiveChatId(null)
    setSessionId(null)
    loadSessions()
  }

  const toggleVoice = () => {
    if (isSpeaking) { stopSpeaking(); setIsSpeaking(false) }
    setVoiceEnabled(!voiceEnabled)
  }

  const handlePin = async (sid) => {
    try { await togglePin(sid); loadSessions() } catch (e) {}
  }

  const handleSearch = async (query) => {
    if (!query) { loadSessions(); return }
    try {
      const result = await searchSessions(query)
      setSessions(result.data || [])
    } catch (e) {}
  }

  return (
    <div className="flex flex-col h-full">
      {/* Voice mode indicator */}
      {voiceEnabled && (
        <div className="flex items-center justify-center gap-2 py-1.5 bg-blue-50 border-b border-blue-100 text-xs text-blue-600">
          <Volume2 size={12} />
          Voice mode active — Speak to interact
        </div>
      )}

      <ChatArea
        messages={messages}
        onSend={handleSend}
        isTyping={isTyping}
        onToggleHistory={() => { setHistoryOpen(!historyOpen); loadSessions() }}
        onToggleContext={() => setContextOpen(!contextOpen)}
        historyOpen={historyOpen}
        contextOpen={contextOpen}
        voiceEnabled={voiceEnabled}
        onVoiceToggle={toggleVoice}
        isSpeaking={isSpeaking}
        language={language}
        onLanguageChange={setLanguage}
      />

      {/* History Overlay */}
      {historyOpen && (
        <>
          <div className="fixed inset-0 z-50" onClick={() => setHistoryOpen(false)} />
          <div className="fixed top-[var(--header-height)] bottom-0 left-[68px] w-80 z-50 bg-white border-r border-gray-200 shadow-xl animate-slide-in-left">
            <ChatHistory
              sessions={sessions}
              activeChatId={activeChatId}
              onSelectChat={(id) => { loadConversation(id); setHistoryOpen(false) }}
              onNewChat={() => { handleNewChat(); setHistoryOpen(false) }}
              onDeleteAll={handleDeleteAll}
              onSearch={handleSearch}
              onClose={() => setHistoryOpen(false)}
            />
          </div>
        </>
      )}

      {/* Context Overlay */}
      {contextOpen && (
        <>
          <div className="fixed inset-0 z-50" onClick={() => setContextOpen(false)} />
          <div className="fixed top-[var(--header-height)] bottom-0 right-0 w-80 z-50 bg-white border-l border-gray-200 shadow-xl animate-slide-in-right">
            <ContextPanel onClose={() => setContextOpen(false)} messages={messages} sessionId={sessionId} />
          </div>
        </>
      )}
    </div>
  )
}
