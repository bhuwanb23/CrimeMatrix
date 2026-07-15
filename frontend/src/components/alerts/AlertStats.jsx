import { AlertTriangle, Clock, CheckCircle2 } from 'lucide-react'

export default function AlertStats({ alerts }) {
  const newCount = alerts.filter((a) => a.status === 'new').length
  const pendingCount = alerts.filter((a) => a.status === 'pending').length
  const resolvedCount = alerts.filter((a) => a.status === 'resolved').length

  return (
    <div className="alert-stats">
      <div className="alert-stat-card new">
        <div className="alert-stat-icon">
          <AlertTriangle size={20} />
        </div>
        <div className="alert-stat-info">
          <span className="alert-stat-value">{newCount}</span>
          <span className="alert-stat-label">New Alerts</span>
        </div>
      </div>

      <div className="alert-stat-card pending">
        <div className="alert-stat-icon">
          <Clock size={20} />
        </div>
        <div className="alert-stat-info">
          <span className="alert-stat-value">{pendingCount}</span>
          <span className="alert-stat-label">Pending</span>
        </div>
      </div>

      <div className="alert-stat-card resolved">
        <div className="alert-stat-icon">
          <CheckCircle2 size={20} />
        </div>
        <div className="alert-stat-info">
          <span className="alert-stat-value">{resolvedCount}</span>
          <span className="alert-stat-label">Resolved</span>
        </div>
      </div>
    </div>
  )
}
