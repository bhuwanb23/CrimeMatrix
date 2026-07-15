import { X, AlertTriangle, Clock, FileText, CheckCircle2 } from 'lucide-react'

const activities = [
  {
    icon: AlertTriangle,
    color: 'var(--warning)',
    title: 'New FIR registered — FIR #4521/2026',
    subtitle: 'Theft at Malleshwaram, Bengaluru',
    time: '12 min ago',
  },
  {
    icon: FileText,
    color: 'var(--accent)',
    title: 'Suspect flagged in cross-district search',
    subtitle: 'Ravi Kumar linked to 3 open cases',
    time: '28 min ago',
  },
  {
    icon: CheckCircle2,
    color: 'var(--success)',
    title: 'Case #1089 — Investigation closed',
    subtitle: 'Charge sheet filed, awaiting court date',
    time: '1 hr ago',
  },
  {
    icon: Clock,
    color: 'var(--text-muted)',
    title: 'Whisper Alert: Vehicle KA-01-AB-1234',
    subtitle: 'Matches suspect in unsolved case #987',
    time: '2 hrs ago',
  },
]

const notifications = [
  {
    title: 'AI Analysis ready for Case #1102',
    time: '5 min ago',
    unread: true,
  },
  {
    title: 'Shift handover report pending',
    time: '1 hr ago',
    unread: true,
  },
  {
    title: 'Cross-district intelligence update',
    time: '3 hrs ago',
    unread: false,
  },
]

export default function RightPanel({ isOpen, onClose }) {
  return (
    <>
      {/* Backdrop for mobile */}
      <div
        className={`right-panel-backdrop ${isOpen ? 'visible' : ''}`}
        onClick={onClose}
      />

      <aside className={`right-panel ${isOpen ? 'open' : ''}`}>
        <div className="right-panel-header">
          <h2 className="right-panel-title">Activity & Updates</h2>
          <button
            className="right-panel-close"
            onClick={onClose}
            aria-label="Close panel"
          >
            <X size={18} strokeWidth={1.8} />
          </button>
        </div>

        <div className="right-panel-content">
          {/* Recent Activity */}
          <section className="right-panel-section">
            <h3 className="right-panel-section-title">Recent Activity</h3>
            <div className="right-panel-items">
              {activities.map((item, i) => (
                <div key={i} className="activity-card">
                  <div className="activity-icon" style={{ color: item.color }}>
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
                <div
                  key={i}
                  className={`notification-card ${item.unread ? 'unread' : ''}`}
                >
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
