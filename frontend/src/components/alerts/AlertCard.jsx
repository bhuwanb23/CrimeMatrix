import { alertTypes } from './alertsData'

export default function AlertCard({ alert, onAccept, onReject, onView }) {
  const typeInfo = alertTypes[alert.type]

  return (
    <div className={`alert-card ${alert.status}`}>
      <div className="alert-card-header">
        <div className="alert-card-type">
          <span className="alert-type-dot" style={{ background: typeInfo.color }} />
          <span className="alert-type-label">{typeInfo.label}</span>
        </div>
        <span className={`alert-priority-badge ${alert.priority}`}>{alert.priority}</span>
      </div>

      <div className="alert-card-body">
        <h4 className="alert-card-title">{alert.title}</h4>
        <p className="alert-card-desc">{alert.description}</p>
      </div>

      <div className="alert-card-meta">
        <span className="alert-card-time">{alert.timestamp}</span>
        <span className="alert-card-case">{alert.caseId}</span>
        <span className="alert-card-district">{alert.district}</span>
      </div>

      <div className="alert-card-actions">
        <button className="alert-action-btn accept" onClick={() => onAccept(alert.id)}>
          ✓ Accept
        </button>
        <button className="alert-action-btn reject" onClick={() => onReject(alert.id)}>
          ✕ Reject
        </button>
        <button className="alert-action-btn view" onClick={() => onView(alert)}>
          → View
        </button>
      </div>
    </div>
  )
}
