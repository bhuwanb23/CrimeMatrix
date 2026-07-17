import { alertTypes } from './alertsData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateAlertType } from '../../utils/translate'

export default function AlertTypeChart({ alerts }) {
  const { lang } = useLanguage()
  const typeCounts = {}
  alerts.forEach((a) => {
    typeCounts[a.type] = (typeCounts[a.type] || 0) + 1
  })

  const total = alerts.length || 1
  const sortedTypes = Object.entries(typeCounts).sort((a, b) => b[1] - a[1])

  return (
    <div className="alert-type-chart-card">
      <div className="alert-type-chart-header">
        <h3>{t('alerts_by_type', lang)}</h3>
      </div>

      <div className="alert-type-chart-list">
        {sortedTypes.map(([type, count]) => {
          const info = alertTypes[type]
          const percentage = Math.round((count / total) * 100)

          return (
            <div key={type} className="alert-type-item">
              <div className="alert-type-item-header">
                <div className="alert-type-item-left">
                  <span className="alert-type-dot" style={{ background: info.color }} />
                  <span className="alert-type-name">{translateAlertType(type, lang)}</span>
                </div>
                <span className="alert-type-count">{count}</span>
              </div>
              <div className="alert-type-bar">
                <div
                  className="alert-type-bar-fill"
                  style={{ width: `${percentage}%`, background: info.color }}
                />
              </div>
              <span className="alert-type-percentage">{percentage}%</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
