import { useState, useCallback, useEffect } from 'react'
import ChatArea from './copilot/ChatArea'
import ChatHistory from './copilot/ChatHistory'
import ContextPanel from './copilot/ContextPanel'
import { chat, listSessions, getSession, createSession, deleteSession } from '../services/copilot'

export default function CopilotPage() {
  const [activeChatId, setActiveChatId] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [contextOpen, setContextOpen] = useState(false)
  const [sessions, setSessions] = useState([])

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

    try {
      const result = await chat(content, sessionId, 'default', true)
      const data = result.data
      if (data) {
        setSessionId(data.session_id)
        setActiveChatId(data.session_id)
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response,
          time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
        }])
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      }])
    }
    setIsTyping(false)
  }, [sessionId])

  const handleNewChat = () => {
    setMessages([])
    setActiveChatId(null)
    setSessionId(null)
    loadSessions()
  }

  return (
    <div className="flex flex-col h-full">
      <ChatArea
        messages={messages}
        onSend={handleSend}
        isTyping={isTyping}
        onToggleHistory={() => { setHistoryOpen(!historyOpen); loadSessions() }}
        onToggleContext={() => setContextOpen(!contextOpen)}
        historyOpen={historyOpen}
        contextOpen={contextOpen}
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
            <ContextPanel onClose={() => setContextOpen(false)} />
          </div>
        </>
      )}
    </div>
  )
}
