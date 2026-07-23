import { AlertTriangle, Shield, MapPin, TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


const alertIcons = {
  repeat_offender: Shield,
  hotspot: MapPin,
  pattern: TrendingUp,
}

const severityColors = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#3b82f6',
}

export default function ActiveAlertsPanel({ alerts }) {
  const { t } = useLanguage()
  if (!alerts || alerts.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <AlertTriangle size={14} />
          <h3>{t(t('Active Alerts'))}</h3>
        </div>
        <div className="similar-empty"><p>{t(t('No active alerts'))}</p></div>
      </div>
    )
  }

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <AlertTriangle size={14} />
        <h3>{t(t('Active Alerts'))}</h3>
        <span className="similar-count">{alerts.length}</span>
      </div>
      <div className="analytics-alerts-list">
        {alerts.map((alert, i) => {
          const Icon = alertIcons[alert.type] || AlertTriangle
          const color = severityColors[alert.severity] || '#64748b'
          return (
            <div key={i} className="analytics-alert-item">
              <div className="analytics-alert-icon" style={{ color }}>
                <Icon size={14} />
              </div>
              <div className="analytics-alert-info">
                <span className="analytics-alert-title">{alert.title}</span>
                <span className="analytics-alert-desc">{alert.description}</span>
                <div className="analytics-alert-confidence">
                  <div className="analytics-confidence-bar">
                    <div className="analytics-confidence-fill" style={{ width: `${alert.confidence}%`, background: color }} />
                  </div>
                  <span>{alert.confidence}%</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
