import { Brain, Target, AlertTriangle, TrendingUp, Activity, Shield } from 'lucide-react'

const cards = [
  { key: 'total_models', label: 'AI Models', icon: Brain, color: '#f59e0b' },
  { key: 'accuracy_rate', label: 'Accuracy', icon: Target, color: '#10b981', suffix: '%' },
  { key: 'predictions_today', label: 'Predictions', icon: TrendingUp, color: '#3b82f6' },
  { key: 'active_models', label: 'Active', icon: Activity, color: '#8b5cf6' },
]

export default function PredictionSummaryCards({ predictions }) {
  if (!predictions) return null

  return (
    <div className="analytics-summary-cards">
      {cards.map((card) => {
        const value = predictions[card.key] || 0
        const Icon = card.icon
        return (
          <div key={card.key} className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: card.color }}>
              <Icon size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{card.label}</span>
              <span className="analytics-pred-value">{value}{card.suffix || ''}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}
