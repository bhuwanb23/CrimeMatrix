import { useState, useRef, useEffect } from 'react'
import {
  AlertTriangle, Clock, FileText, Activity, TrendingUp,
  Send, Bot,
} from 'lucide-react'
import ChatMessage from './ChatMessage'
import { useLanguage } from '../context/LanguageContext'
import { chat } from '../services/copilot'
import { getStatistics } from '../services/analyticsLive'
import { listAlerts } from '../services/earlyWarning'
import { getUnifiedTimeline } from '../services/intelligenceTimeline'

const initialMessages = [
  {
    role: 'assistant',
    content: 'Hello. I\'m your AI Investigation Copilot. How can I help you today?',
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
  const [quickStats, setQuickStats] = useState([])
  const [activities, setActivities] = useState([])
  const [activityLoading, setActivityLoading] = useState(true)
  const chatEndRef = useRef(null)

  const copilotLang = language === 'Kannada' || language === 'kn' ? 'kn' : 'en'

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    let cancelled = false
    async function loadActivity() {
      setActivityLoading(true)
      try {
        const [statsRes, alertsRes, timelineRes] = await Promise.all([
          getStatistics().catch(() => null),
          listAlerts({ status: 'active' }).catch(() => null),
          getUnifiedTimeline({ limit: 8 }).catch(() => null),
        ])
        if (cancelled) return
        const stats = statsRes?.data || {}
        const totals = stats.totals || {}
        const byStatus = stats.cases_by_status || {}
        setQuickStats([
          { icon: FileText, color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)', value: String(totals.cases ?? '—'), label: 'Cases' },
          { icon: AlertTriangle, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', value: String(totals.alerts ?? '—'), label: 'Alerts' },
          { icon: Clock, color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)', value: String(byStatus.pending ?? byStatus.active ?? '—'), label: 'Pending' },
          { icon: TrendingUp, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)', value: `${stats.resolution_rate ?? 0}%`, label: 'Resolution' },
        ])

        const alerts = alertsRes?.data?.items || []
        const timeline = timelineRes?.data?.items || timelineRes?.data || []
        const fromAlerts = alerts.slice(0, 4).map((a) => ({
          icon: AlertTriangle,
          color: '#f59e0b',
          bg: 'rgba(245, 158, 11, 0.1)',
          title: a.title || 'Alert',
          subtitle: a.description || a.alert_type || '',
          time: a.created_at ? new Date(a.created_at).toLocaleString() : a.status || '',
        }))
        const fromTimeline = (Array.isArray(timeline) ? timeline : []).slice(0, 4).map((e) => ({
          icon: Activity,
          color: '#8b5cf6',
          bg: 'rgba(139, 92, 246, 0.1)',
          title: e.title || e.event_type || 'Timeline event',
          subtitle: e.description || e.entity_type || '',
          time: e.created_at || e.timestamp || '',
        }))
        setActivities([...fromAlerts, ...fromTimeline].slice(0, 6))
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setActivityLoading(false)
      }
    }
    loadActivity()
    return () => { cancelled = true }
  }, [])

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
          type="button"
          className={`right-panel-tab ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          <Activity size={14} strokeWidth={1.8} />
          {t('Activity')}
        </button>
        <button
          type="button"
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
              {(activityLoading ? [] : quickStats).map((stat, i) => (
                <div key={i} className="quick-stat-card">
                  <div className="quick-stat-icon" style={{ background: stat.bg, color: stat.color }}>
                    <stat.icon size={14} strokeWidth={1.8} />
                  </div>
                  <div className="quick-stat-value">{stat.value}</div>
                  <div className="quick-stat-label">{t(stat.label)}</div>
                </div>
              ))}
              {activityLoading && <p className="text-xs text-slate-400 m-0">{t('Loading...')}</p>}
            </div>
          </section>

          <section className="right-panel-section">
            <h3 className="right-panel-section-title">{t('Recent Activity')}</h3>
            <div className="right-panel-items">
              {!activityLoading && activities.length === 0 && (
                <p className="text-xs text-slate-400 m-0">{t('No recent activity')}</p>
              )}
              {activities.map((item, i) => (
                <div key={i} className="activity-card">
                  <div className="activity-icon" style={{ background: item.bg, color: item.color }}>
                    <item.icon size={14} strokeWidth={1.8} />
                  </div>
                  <div className="activity-content">
                    <p className="activity-title">{item.title}</p>
                    <p className="activity-subtitle">{item.subtitle}</p>
                    <span className="activity-time">{item.time}</span>
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
              placeholder={t('Ask about cases...')}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              disabled={sending}
            />
            <button type="button" className="chat-send-btn" onClick={handleSend} disabled={!inputValue.trim() || sending}>
              <Send size={16} strokeWidth={1.8} />
            </button>
          </div>
        </div>
      )}
    </aside>
  )
}
