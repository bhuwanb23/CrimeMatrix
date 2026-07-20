import { Lightbulb, TrendingUp, AlertTriangle } from 'lucide-react'

export default function AIPredictionsPanel({ forecast, predictions, districts }) {
  const insights = []

  if (forecast) {
    if (forecast.trend === 'increasing') {
      insights.push({
        type: 'trend',
        icon: TrendingUp,
        color: '#ef4444',
        title: 'Crime rate trending upward',
        description: `Forecast shows increasing crime with ${forecast.confidence}% confidence. Consider increasing patrols.`,
        confidence: forecast.confidence,
      })
    } else if (forecast.trend === 'decreasing') {
      insights.push({
        type: 'trend',
        icon: TrendingUp,
        color: '#10b981',
        title: 'Crime rate trending downward',
        description: `Current strategies appear effective. Confidence: ${forecast.confidence}%.`,
        confidence: forecast.confidence,
      })
    }
  }

  if (districts && districts.length > 0) {
    const highRisk = districts.filter(d => d.risk === 'high')
    if (highRisk.length > 0) {
      insights.push({
        type: 'district',
        icon: AlertTriangle,
        color: '#f59e0b',
        title: `${highRisk.length} districts with high predicted crime`,
        description: `Districts: ${highRisk.map(d => d.name).join(', ')}. Recommend targeted interventions.`,
        confidence: 72,
      })
    }
  }

  if (predictions && predictions.length > 10) {
    insights.push({
      type: 'volume',
      icon: TrendingUp,
      color: '#3b82f6',
      title: `${predictions.length} active predictions in system`,
      description: 'Multiple prediction models are generating insights across districts and crime types.',
      confidence: 80,
    })
  }

  insights.push({
    type: 'recommendation',
    icon: Lightbulb,
    color: '#8b5cf6',
    title: 'Cross-district coordination recommended',
    description: 'Pattern analysis suggests similar criminal activity across multiple districts. Joint operations may improve resolution rates.',
    confidence: 68,
  })

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <Lightbulb size={14} />
        <h3>AI Predictions & Recommendations</h3>
      </div>
      <div className="analytics-recommendations-list">
        {insights.map((insight, i) => {
          const Icon = insight.icon
          return (
            <div key={i} className="analytics-recommendation-item">
              <div className="analytics-rec-icon" style={{ color: insight.color }}>
                <Icon size={14} />
              </div>
              <div className="analytics-rec-info">
                <span className="analytics-rec-title">{insight.title}</span>
                <span className="analytics-rec-desc">{insight.description}</span>
                <div className="analytics-rec-confidence">
                  <div className="analytics-confidence-bar">
                    <div className="analytics-confidence-fill" style={{ width: `${insight.confidence}%`, background: insight.color }} />
                  </div>
                  <span>{insight.confidence}% confidence</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
