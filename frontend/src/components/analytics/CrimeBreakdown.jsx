import { crimeTypes } from './analyticsData'
import { useLanguage } from '../../context/LanguageContext'

export default function CrimeBreakdown() {
  const { t } = useLanguage()

  return (
    <div className="analytics-breakdown-card">
      <div className="analytics-breakdown-header">
        <h3>{t('Crime Type Breakdown')}</h3>
      </div>

      <div className="analytics-breakdown-list">
        {crimeTypes.map((type, i) => (
          <div key={i} className="breakdown-item">
            <div className="breakdown-item-header">
              <span className="breakdown-name">{t(type.name)}</span>
              <span className="breakdown-stats">
                {type.percentage}% • {type.count.toLocaleString()} {t('cases')}
              </span>
            </div>
            <div className="breakdown-bar">
              <div
                className="breakdown-bar-fill"
                style={{ width: `${type.percentage}%`, background: type.color }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

