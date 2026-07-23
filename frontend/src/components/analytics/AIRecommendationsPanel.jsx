import { Lightbulb, CheckCircle, AlertTriangle } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function AIRecommendationsPanel({ alerts, highRisk, priority }) {
  const { t } = useLanguage()
  const recommendations = []

  if (alerts && alerts.length > 0) {
    recommendations.push({
      type: 'alert',
      icon: AlertTriangle,
      color: '#ef4444',
      title: `${alerts.length} ${t('active alerts require attention')}`,
      description: t('Review high-severity alerts and take action on priority items.'),
      confidence: 85,
    })
  }

  if (highRisk && highRisk.length > 0) {
    recommendations.push({
      type: 'risk',
      icon: AlertTriangle,
      color: '#f59e0b',
      title: `${highRisk.length} ${t('high-risk suspects need monitoring')}`,
      description: t('Consider increasing surveillance on repeat offenders with high risk scores.'),
      confidence: 78,
    })
  }

  if (priority && priority.length > 0) {
    const lowProgress = priority.filter(c => (c.progress || 0) < 30)
    if (lowProgress.length > 0) {
      recommendations.push({
        type: 'progress',
        icon: CheckCircle,
        color: '#3b82f6',
        title: `${lowProgress.length} ${t('investigations need progress updates')}`,
        description: t('These investigations have low progress and may need additional resources.'),
        confidence: 72,
      })
    }
  }

  recommendations.push({
    type: 'insight',
    icon: Lightbulb,
    color: '#8b5cf6',
    title: t('Pattern analysis suggests cross-district coordination'),
    description: t('Similar crime patterns detected across multiple districts. Consider joint operations.'),
    confidence: 65,
  })

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <Lightbulb size={14} />
        <h3>{t('AI Recommendations')}</h3>
      </div>
      <div className="analytics-recommendations-list">
        {recommendations.map((rec, i) => {
          const Icon = rec.icon
          return (
             <div key={i} className="analytics-recommendation-item">
              <div className="analytics-rec-icon" style={{ color: rec.color }}>
                <Icon size={14} />
              </div>
              <div className="analytics-rec-info">
                <span className="analytics-rec-title">{rec.title}</span>
                <span className="analytics-rec-desc">{rec.description}</span>
                <div className="analytics-rec-confidence">
                  <div className="analytics-confidence-bar">
                    <div className="analytics-confidence-fill" style={{ width: `${rec.confidence}%`, background: rec.color }} />
                  </div>
                  <span>{rec.confidence}% {t('confidence')}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
