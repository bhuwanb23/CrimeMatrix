import { Bot, AlertTriangle, Lightbulb, Shield } from 'lucide-react'

export default function IntelligenceAIPanel({ insights }) {
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
        <h3><Bot size={14} /> AI Intelligence</h3>
      </div>

      {insights.summary && (
        <p className="intel-ai-summary">{insights.summary}</p>
      )}

      {alerts.length > 0 && (
        <div className="intel-ai-alerts">
          <h4><AlertTriangle size={12} /> Alerts</h4>
          {alerts.map((alert, i) => (
            <div key={i} className="intel-ai-alert-item">
              <div
                className="intel-ai-alert-dot"
                style={{ background: severityColors[alert.severity] || '#f59e0b' }}
              />
              <span className="intel-ai-alert-msg">{alert.message}</span>
            </div>
          ))}
        </div>
      )}

      {insightList.length > 0 && (
        <div className="intel-ai-insights">
          <h4><Lightbulb size={12} /> Insights</h4>
          {insightList.map((insight, i) => (
            <div key={i} className="intel-ai-insight-item">
              <Shield size={10} />
              <span>{insight}</span>
            </div>
          ))}
        </div>
      )}

      {alerts.length === 0 && insightList.length === 0 && (
        <div className="similar-empty">
          <p>No alerts or insights at this time</p>
        </div>
      )}
    </div>
  )
}
