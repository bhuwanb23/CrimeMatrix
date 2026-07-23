import { Shield } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

export default function HighRiskSuspectsList({ suspects }) {
  const { t } = useLanguage()
  if (!suspects || suspects.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <Shield size={14} />
          <h3>{t(t('High-Risk Suspects'))}</h3>
        </div>
        <div className="similar-empty"><p>{t(t('No high-risk suspects'))}</p></div>
      </div>
    )
  }

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <Shield size={14} />
        <h3>{t(t('High-Risk Suspects'))}</h3>
        <span className="similar-count">{suspects.length}</span>
      </div>
      <div className="analytics-risk-list">
        {suspects.map((s, i) => {
          const color = riskColors[s.risk_level] || '#64748b'
          return (
            <div key={s.id || i} className="analytics-risk-item">
              <div className="analytics-risk-rank">#{i + 1}</div>
              <div className="analytics-risk-info">
                <span className="analytics-risk-name">{s.name}</span>
                <div className="analytics-risk-bar">
                  <div className="analytics-risk-fill" style={{ width: `${s.risk_score}%`, background: color }} />
                </div>
                <div className="analytics-risk-meta">
                  <span>{s.offenses} offenses</span>
                  <span className="analytics-risk-badge" style={{ color }}>{s.risk_level}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
