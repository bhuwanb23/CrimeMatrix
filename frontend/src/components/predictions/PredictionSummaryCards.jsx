import { Brain, Target, TrendingUp, Activity } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function PredictionSummaryCards({ stats }) {
  const { t } = useLanguage()
  if (!stats) return null

  const cards = [
    { key: 'total_predictions', label: t('Predictions'), icon: Brain, color: '#f59e0b' },
    { key: 'forecasts', label: t('Forecasts'), icon: TrendingUp, color: '#3b82f6' },
    { key: 'avg_confidence', label: t('Avg Confidence'), icon: Target, color: '#10b981', suffix: '%' },
    { key: 'total_models', label: t('Models'), icon: Activity, color: '#8b5cf6' },
  ]

  return (
    <div className="analytics-summary-cards">
      {cards.map((card) => {
        const value = stats[card.key] || 0
        const Icon = card.icon
        return (
          <div key={card.key} className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: card.color }}>
              <Icon size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{t(card.label)}</span>
              <span className="analytics-pred-value">{Math.round(value)}{card.suffix || ''}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}
