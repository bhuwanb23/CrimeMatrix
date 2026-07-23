import { alertTypes } from './alertsData'
import { ChevronRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function AlertFeed({ alerts, onAlertSelect, selectedAlert }) {
  const { t } = useLanguage()

  return (
    <div className="alert-feed-card">
      <div className="alert-feed-header">
        <h3>{t('Alert Feed')}</h3>
        <span className="alert-feed-count">{alerts.length} {t('alerts')}</span>
      </div>

      <div className="alert-feed-list">
        {alerts.map((alert) => {
          const typeInfo = alertTypes[alert.type]
          const isSelected = selectedAlert?.id === alert.id

          return (
            <div
              key={alert.id}
              className={`alert-feed-item ${isSelected ? 'selected' : ''} ${alert.status}`}
              onClick={() => onAlertSelect(alert)}
            >
              <div className="alert-feed-icon" style={{ background: typeInfo.color + '15', color: typeInfo.color }}>
                {typeInfo.icon}
              </div>
              <div className="alert-feed-content">
                <div className="alert-feed-top">
                  <span className="alert-feed-type" style={{ color: typeInfo.color }}>{t(typeInfo.label)}</span>
                  <span className="alert-feed-time">{alert.timestamp}</span>
                </div>
                <p className="alert-feed-title">{alert.title}</p>
                <div className="alert-feed-meta">
                  <span>{alert.caseId}</span>
                  <span>•</span>
                  <span>{alert.district}</span>
                </div>
              </div>
              <ChevronRight size={14} className="alert-feed-arrow" />
            </div>
          )
        })}
      </div>
    </div>
  )
}

