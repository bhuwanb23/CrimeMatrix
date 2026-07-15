import { AlertTriangle, Clock, CheckCircle2, Activity } from 'lucide-react'

export default function AlertStats({ alerts }) {
  const newCount = alerts.filter((a) => a.status === 'new').length
  const pendingCount = alerts.filter((a) => a.status === 'pending').length
  const resolvedCount = alerts.filter((a) => a.status === 'resolved').length

  return (
    <div className="alert-stats">
      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #fef3c7, #fde68a)' }}>
          <AlertTriangle size={20} style={{ color: '#d97706' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{newCount}</span>
          <span className="alert-stat-label">New Alerts</span>
        </div>
      </div>

      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #ede9fe, #ddd6fe)' }}>
          <Clock size={20} style={{ color: '#7c3aed' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{pendingCount}</span>
          <span className="alert-stat-label">Pending</span>
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
      </div>

      <div className="alert-stat-card">
        <div className="alert-stat-icon-wrap" style={{ background: 'linear-gradient(135deg, #dbeafe, #bfdbfe)' }}>
          <Activity size={20} style={{ color: '#2563eb' }} />
        </div>
        <div className="alert-stat-content">
          <span className="alert-stat-value">{alerts.length}</span>
          <span className="alert-stat-label">Total Alerts</span>
        </div>
      </div>
    </div>
  )
}
