import { useState, useRef, useEffect } from 'react'
import {
  AlertTriangle, Clock, FileText, CheckCircle2, Activity, TrendingUp,
  Send, Bot,
} from 'lucide-react'
import ChatMessage from './ChatMessage'

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

export default function RightPanel({ isOpen }) {
  const [activeTab, setActiveTab] = useState('activity')
  const [messages, setMessages] = useState(initialMessages)
  const [inputValue, setInputValue] = useState('')
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = () => {
    if (!inputValue.trim()) return
    const userMsg = { role: 'user', content: inputValue.trim(), time: 'Now' }
    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
    setTimeout(() => {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Let me analyze that for you. Based on the current database, I found relevant information. Would you like me to generate a detailed report?',
        time: 'Now',
      }])
    }, 1200)
  }

  return (
    <aside className={`right-panel ${isOpen ? 'open' : 'closed'}`}>
      <div className="right-panel-tabs">
        <button
          className={`right-panel-tab ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          <Activity size={14} strokeWidth={1.8} />
          Activity
        </button>
        <button
          className={`right-panel-tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <Bot size={14} strokeWidth={1.8} />
          AI Copilot
        </button>
      </div>

      {activeTab === 'activity' && (
        <div className="right-panel-content">
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Today's Overview</h3>
            <div className="quick-stats-grid">
              {quickStats.map((stat, i) => (
                <div key={i} className="quick-stat-card">
                  <div className="quick-stat-icon" style={{ background: stat.bg, color: stat.color }}>
                    <stat.icon size={14} strokeWidth={1.8} />
                  </div>
                  <div className="quick-stat-value">{stat.value}</div>
                  <div className="quick-stat-label">{stat.label}</div>
                </div>
              ))}
            </div>
          </section>

          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Recent Activity</h3>
            <div className="right-panel-items">
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
            <div ref={chatEndRef} />
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask about cases..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button className="chat-send-btn" onClick={handleSend} disabled={!inputValue.trim()}>
              <Send size={16} strokeWidth={1.8} />
            </button>
          </div>
        </div>
      )}
    </aside>
  )
}
