import { useLanguage } from '../../context/LanguageContext'
import { useNavigate } from 'react-router-dom'

export default function SuspectCard({ suspect }) {
  const { t } = useLanguage()
  const navigate = useNavigate()

  return (
    <button
      className="suspect-card"
      onClick={() => navigate(`/suspects/${suspect.id}`)}
    >
      <div className="suspect-card-avatar" style={{ background: suspect.gradient }}>
        {suspect.initials}
      </div>
      <div className="suspect-card-info">
        <span className="suspect-card-name">{suspect.name}</span>
        <span className="suspect-card-meta">{suspect.age} yrs • {suspect.district}</span>
      </div>
      <div className="suspect-card-stats">
        <div className="suspect-card-risk">
          <span className="risk-label">{t('Risk')}</span>
          <div className="risk-bar">
            <div
              className="risk-fill"
              style={{
                width: `${suspect.riskScore}%`,
                background: suspect.riskScore > 70 ? '#ef4444' : suspect.riskScore > 40 ? '#f59e0b' : '#10b981',
              }}
            />
          </div>
          <span className="risk-value">{suspect.riskScore}</span>
        </div>
        <div className="suspect-card-badges">
          <span className={`suspect-status-badge ${suspect.status.toLowerCase().replace(' ', '-')}`}>
            {suspect.status}
          </span>
          <span className="suspect-cases-count">{suspect.cases} cases</span>
        </div>
      </div>
    </button>
  )
}
