import { activityLog, alertTypes } from './alertsData'
import { useLanguage } from '../../context/LanguageContext'

export default function RecentActivity() {
  const { t } = useLanguage()

  return (
    <div className="recent-activity-card">
      <div className="recent-activity-header">
        <h3>{t('Recent Activity')}</h3>
      </div>

      <div className="recent-activity-list">
        {activityLog.map((item) => {
          const typeInfo = alertTypes[item.type]
          return (
            <div key={item.id} className="recent-activity-item">
              <div className="recent-activity-dot" style={{ background: typeInfo.color }} />
              <div className="recent-activity-content">
                <p className="recent-activity-action">{item.action}</p>
                <div className="recent-activity-meta">
                  <span>{item.user}</span>
                  <span>•</span>
                  <span>{item.time}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

