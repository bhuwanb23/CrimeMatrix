import { Bot, AlertTriangle, Lightbulb, Shield } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function IntelligenceAIPanel({ insights }) {
  const { t } = useLanguage()

  if (!insights) return null

  const alerts = insights.alerts || []
  const insightList = insights.insights || []

  const severityColors = {
    high: '#ef4444',
    medium: '#f59e0b',
    low: '#10b981',
  }

  return (
    <div className="intel-ai-panel">
      <div className="intel-widget-header">
        <h3><Bot size={14} /> {t('AI Intelligence')}</h3>
      </div>

      {insights.summary && (
        <p className="intel-ai-summary">{t(insights.summary)}</p>
      )}

      {alerts.length > 0 && (
        <div className="intel-ai-alerts">
          <h4><AlertTriangle size={12} /> {t('Alerts')}</h4>
          {alerts.map((alert, i) => (
            <div key={i} className="intel-ai-alert-item">
              <div
                className="intel-ai-alert-dot"
                style={{ background: severityColors[alert.severity] || '#f59e0b' }}
              />
              <span className="intel-ai-alert-msg">{t(alert.message)}</span>
            </div>
          ))}
        </div>
      )}

      {insightList.length > 0 && (
        <div className="intel-ai-insights">
          <h4><Lightbulb size={12} /> {t('Insights')}</h4>
          {insightList.map((insight, i) => (
            <div key={i} className="intel-ai-insight-item">
              <Shield size={10} />
              <span>{t(insight)}</span>
            </div>
          ))}
        </div>
      )}

      {alerts.length === 0 && insightList.length === 0 && (
        <div className="similar-empty">
          <p>{t('No alerts or insights at this time')}</p>
        </div>
      )}
    </div>
  )
}

