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
  const [isLoadingHistory, setIsLoadingHistory] = useState(false)

  // Load conversation history
  const loadSessions = useCallback(async () => {
    try {
      const result = await listSessions()
      setSessions(result.data || [])
    } catch (e) {
      console.error('Failed to load sessions:', e)
    }
  }, [])

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  // Load a specific conversation
  const loadConversation = useCallback(async (sid) => {
    setIsLoadingHistory(true)
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
    setIsLoadingHistory(false)
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
          reasoning_trace: data.reasoning_trace,
          steps: data.steps,
        }])
      }
    } catch (e) {
      console.error('Chat error:', e)
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

  const handleDeleteChat = async (sid) => {
    try {
      await deleteSession(sid)
      if (activeChatId === sid) {
        handleNewChat()
      }
      loadSessions()
    } catch (e) {
      console.error('Delete failed:', e)
    }
  }

  return (
    <div className="copilot-page">
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
          <div className="copilot-overlay" onClick={() => setHistoryOpen(false)} />
          <div className="copilot-slide-panel left">
            <ChatHistory
              sessions={sessions}
              activeChatId={activeChatId}
              onSelectChat={(id) => { loadConversation(id); setHistoryOpen(false) }}
              onNewChat={() => { handleNewChat(); setHistoryOpen(false) }}
              onDeleteChat={handleDeleteChat}
              onClose={() => setHistoryOpen(false)}
            />
          </div>
        </>
      )}

      {/* Context Overlay */}
      {contextOpen && (
        <>
          <div className="copilot-overlay" onClick={() => setContextOpen(false)} />
          <div className="copilot-slide-panel right">
            <ContextPanel onClose={() => setContextOpen(false)} />
          </div>
        </>
      )}
    </div>
  )
}
