import { useState, useRef, useEffect } from 'react'
import {
  AlertTriangle, Clock, FileText, CheckCircle2, Activity, TrendingUp,
  Send, Bot,
} from 'lucide-react'
import ChatMessage from './ChatMessage'
import { useLanguage } from '../context/LanguageContext'
import { chat } from '../services/copilot'

const quickStats = [
  { icon: FileText, color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)', value: '12', label: 'Cases Today' },
  { icon: AlertTriangle, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', value: '5', label: 'Alerts' },
  { icon: Clock, color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)', value: '8', label: 'Pending' },
  { icon: TrendingUp, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)', value: '73%', label: 'Resolution' },
]

const activities = [
  {
    icon: AlertTriangle, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)',
    title: 'New FIR registered — FIR #4521/2026',
    subtitle: 'Theft at Malleshwaram, Bengaluru',
    time: '12 min ago',
  },
  {
    icon: FileText, color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)',
    title: 'Suspect flagged — Ravi Kumar',
    subtitle: 'Linked to 3 open cases across districts',
    time: '28 min ago',
  },
  {
    icon: CheckCircle2, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)',
    title: 'Case #1089 — Investigation closed',
    subtitle: 'Charge sheet filed, awaiting court date',
    time: '1 hr ago',
  },
  {
    icon: Activity, color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)',
    title: 'Whisper Alert: Vehicle KA-01-AB-1234',
    subtitle: 'Matches suspect in unsolved case #987',
    time: '2 hrs ago',
  },
]

const initialMessages = [
  {
    role: 'assistant',
    content: 'Hello SI Karthik. I\'m your AI Investigation Copilot. How can I help you today?',
    time: '9:00 AM',
  },
]

function nowLabel() {
  return new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
}

export default function RightPanel({ isOpen }) {
  const { t, language } = useLanguage()
  const [activeTab, setActiveTab] = useState('activity')
  const [messages, setMessages] = useState(initialMessages)
  const [inputValue, setInputValue] = useState('')
  const [sending, setSending] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const chatEndRef = useRef(null)

  const copilotLang = language === 'Kannada' || language === 'kn' ? 'kn' : 'en'

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!inputValue.trim() || sending) return
    const text = inputValue.trim()
    const userMsg = { role: 'user', content: text, time: nowLabel() }
    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
    setSending(true)

    try {
      const res = await chat(text, sessionId, 'default', true, copilotLang)
      const data = res?.data || res || {}
      if (data.session_id) setSessionId(data.session_id)
      const reply =
        data.response ||
        data.message ||
        data.content ||
        data.reply ||
        (typeof data === 'string' ? data : null) ||
        'No response from copilot.'
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: reply,
        time: nowLabel(),
      }])
    } catch (err) {
      console.error(err)
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Sorry — the copilot is unavailable right now. Please try again.',
        time: nowLabel(),
      }])
    } finally {
      setSending(false)
    }
  }

  return (
    <aside className={`right-panel ${isOpen ? 'open' : 'closed'}`}>
      <div className="right-panel-tabs">
        <button
          className={`right-panel-tab ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          <Activity size={14} strokeWidth={1.8} />
          {t('Activity')}
        </button>
        <button
          className={`right-panel-tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <Bot size={14} strokeWidth={1.8} />
          {t('AI Copilot')}
        </button>
      </div>

      {activeTab === 'activity' && (
        <div className="right-panel-content">
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">{t("Today's Overview")}</h3>
            <div className="quick-stats-grid">
              {quickStats.map((stat, i) => (
                <div key={i} className="quick-stat-card">
                  <div className="quick-stat-icon" style={{ background: stat.bg, color: stat.color }}>
                    <stat.icon size={14} strokeWidth={1.8} />
                  </div>
                  <div className="quick-stat-value">{stat.value}</div>
                  <div className="quick-stat-label">{t(stat.label)}</div>
                </div>
              ))}
            </div>
          </section>

          <section className="right-panel-section">
            <h3 className="right-panel-section-title">{t("Recent Activity")}</h3>
            <div className="right-panel-items">
              {activities.map((item, i) => (
                <div key={i} className="activity-card">
                  <div className="activity-icon" style={{ background: item.bg, color: item.color }}>
                    <item.icon size={14} strokeWidth={1.8} />
                  </div>
                  <div className="activity-content">
                    <p className="activity-title">{t(item.title)}</p>
                    <p className="activity-subtitle">{t(item.subtitle)}</p>
                    <span className="activity-time">{t(item.time)}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}

      {activeTab === 'chat' && (
        <div className="chat-panel">
          <div className="chat-messages">
            {messages.map((msg, i) => (
              <ChatMessage key={i} {...msg} />
            ))}
            {sending && (
              <ChatMessage role="assistant" content="Thinking..." time={nowLabel()} />
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              className="chat-input"
              placeholder={t("Ask about cases...")}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              disabled={sending}
            />
            <button className="chat-send-btn" onClick={handleSend} disabled={!inputValue.trim() || sending}>
              <Send size={16} strokeWidth={1.8} />
            </button>
          </div>
        </div>
      )}
    </aside>
  )
}
