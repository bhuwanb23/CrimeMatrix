import { alertTypes } from './alertsData'
import { ChevronRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function AlertCard({ alert, onAccept, onReject, onView }) {
  const { t } = useLanguage()
  const typeInfo = alertTypes[alert.type]

  return (
    <div className={`alert-card ${alert.status}`}>
      <div className="alert-card-left">
        <div className="alert-card-indicator" style={{ background: typeInfo.color }} />
      </div>

      <div className="alert-card-main">
        <div className="alert-card-top">
          <div className="alert-card-type-badge" style={{ background: typeInfo.color + '15', color: typeInfo.color }}>
            {t(typeInfo.label)}
          </div>
          <span className={`alert-priority-badge ${alert.priority}`}>{alert.priority}</span>
        </div>

        <h4 className="alert-card-title">{alert.title}</h4>
        <p className="alert-card-desc">{alert.description}</p>

        <div className="alert-card-footer">
          <div className="alert-card-meta">
            <span className="alert-meta-item">{alert.timestamp}</span>
            <span className="alert-meta-sep">·</span>
            <span className="alert-meta-item">{alert.caseId}</span>
            <span className="alert-meta-sep">·</span>
            <span className="alert-meta-item">{alert.district}</span>
          </div>

          <div className="alert-card-actions">
            <button className="alert-btn accept" onClick={() => onAccept(alert.id)}>
              {t('Accept')}
            </button>
            <button className="alert-btn reject" onClick={() => onReject(alert.id)}>
              {t('Dismiss')}
            </button>
            <button className="alert-btn view" onClick={() => onView(alert)}>
              {t('View')} <ChevronRight size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

