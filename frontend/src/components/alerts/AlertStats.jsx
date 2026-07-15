import { AlertTriangle, Clock, CheckCircle2, Bell } from 'lucide-react'

export default function AlertStats({ alerts }) {
  const newCount = alerts.filter((a) => a.status === 'new').length
  const pendingCount = alerts.filter((a) => a.status === 'pending').length
  const resolvedCount = alerts.filter((a) => a.status === 'resolved').length

  return (
    <div className="alert-stats">
      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #fef3c7, #fde68a)' }}>
          <Bell size={20} style={{ color: '#d97706' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{newCount}</span>
          <span className="alert-stat-label">New Alerts</span>
        </div>
        <div className="alert-stat-trend up">
          <span>●</span> Live
        </div>
      </div>

      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #ede9fe, #ddd6fe)' }}>
          <Clock size={20} style={{ color: '#7c3aed' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{pendingCount}</span>
          <span className="alert-stat-label">Pending Review</span>
        </div>
        <div className="alert-stat-trend">
          <span>●</span> Awaiting action
        </div>
      </div>

      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #d1fae5, #a7f3d0)' }}>
          <CheckCircle2 size={20} style={{ color: '#059669' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{resolvedCount}</span>
          <span className="alert-stat-label">Resolved</span>
        </div>
        <div className="alert-stat-trend">
          <span>●</span> Completed
        </div>
      </div>
    </div>
  )
}
