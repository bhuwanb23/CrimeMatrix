import { X, AlertTriangle, Clock, FileText, CheckCircle2, Activity, TrendingUp, Bell } from 'lucide-react'

const quickStats = [
  { icon: FileText, color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)', value: '12', label: 'Cases Today' },
  { icon: AlertTriangle, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)', value: '5', label: 'Alerts' },
  { icon: Clock, color: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.1)', value: '8', label: 'Pending' },
  { icon: TrendingUp, color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)', value: '73%', label: 'Resolution' },
]

const activities = [
  {
    icon: AlertTriangle,
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.1)',
    title: 'New FIR registered — FIR #4521/2026',
    subtitle: 'Theft at Malleshwaram, Bengaluru',
    time: '12 min ago',
  },
  {
    icon: FileText,
    color: '#3b82f6',
    bg: 'rgba(59, 130, 246, 0.1)',
    title: 'Suspect flagged — Ravi Kumar',
    subtitle: 'Linked to 3 open cases across districts',
    time: '28 min ago',
  },
  {
    icon: CheckCircle2,
    color: '#10b981',
    bg: 'rgba(16, 185, 129, 0.1)',
    title: 'Case #1089 — Investigation closed',
    subtitle: 'Charge sheet filed, awaiting court date',
    time: '1 hr ago',
  },
  {
    icon: Activity,
    color: '#8b5cf6',
    bg: 'rgba(139, 92, 246, 0.1)',
    title: 'Whisper Alert: Vehicle KA-01-AB-1234',
    subtitle: 'Matches suspect in unsolved case #987',
    time: '2 hrs ago',
  },
]

const notifications = [
  { title: 'AI Analysis ready for Case #1102', time: '5 min ago', unread: true },
  { title: 'Shift handover report pending', time: '1 hr ago', unread: true },
  { title: 'Cross-district intelligence update', time: '3 hrs ago', unread: false },
  { title: 'NewMO pattern detected in Zone 4', time: '5 hrs ago', unread: false },
]

export default function RightPanel({ isOpen, onClose }) {
  return (
    <>
      <div
        className={`right-panel-backdrop ${isOpen ? 'visible' : ''}`}
        onClick={onClose}
      />

      <aside className={`right-panel ${isOpen ? 'open' : ''}`}>
        <div className="right-panel-header">
          <h2 className="right-panel-title">Activity & Updates</h2>
          <button className="right-panel-close" onClick={onClose} aria-label="Close panel">
            <X size={16} strokeWidth={1.8} />
          </button>
        </div>

        <div className="right-panel-content">
          {/* Quick Stats */}
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Today's Overview</h3>
            <div className="quick-stats-grid">
              {quickStats.map((stat, i) => (
                <div key={i} className="quick-stat-card">
                  <div className="quick-stat-icon" style={{ background: stat.bg, color: stat.color }}>
                    <stat.icon size={16} strokeWidth={1.8} />
                  </div>
                  <div className="quick-stat-value">{stat.value}</div>
                  <div className="quick-stat-label">{stat.label}</div>
                </div>
              ))}
            </div>
          </section>

          {/* Recent Activity */}
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Recent Activity</h3>
            <div className="right-panel-items">
              {activities.map((item, i) => (
                <div key={i} className="activity-card">
                  <div className="activity-icon" style={{ background: item.bg, color: item.color }}>
                    <item.icon size={16} strokeWidth={1.8} />
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

          {/* Notifications */}
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Notifications</h3>
            <div className="right-panel-items">
              {notifications.map((item, i) => (
                <div key={i} className={`notification-card ${item.unread ? 'unread' : ''}`}>
                  <div className="notification-dot" />
                  <div className="notification-content">
                    <p className="notification-title">{item.title}</p>
                    <span className="notification-time">{item.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </aside>
    </>
  )
}
