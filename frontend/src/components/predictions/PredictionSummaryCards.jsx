import { Brain, Target, TrendingUp, Activity } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function PredictionSummaryCards({ stats }) {
  const { t } = useLanguage()
  if (!stats) return null

  const cards = [
    { key: 'total_predictions', label: t('Predictions'), icon: Brain, color: 'text-amber-500', bg: 'bg-amber-50' },
    { key: 'forecasts', label: t('Forecasts'), icon: TrendingUp, color: 'text-blue-500', bg: 'bg-blue-50' },
    { key: 'avg_confidence', label: t('Avg Confidence'), icon: Target, color: 'text-emerald-500', bg: 'bg-emerald-50', suffix: '%' },
    { key: 'total_models', label: t('Models'), icon: Activity, color: 'text-purple-500', bg: 'bg-purple-50' },
  ]

  return (
    <div className="grid grid-cols-4 gap-4">
      {cards.map((card) => {
        const value = stats[card.key] || 0
        const Icon = card.icon
        return (
          <div key={card.key} className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4 hover:shadow-sm transition-shadow">
            <div className="flex items-center gap-3 mb-2">
              <div className={`w-9 h-9 rounded-xl ${card.bg} flex items-center justify-center`}>
                <Icon size={16} className={card.color} />
              </div>
              <span className="text-[10px] text-[var(--text-muted)] font-medium uppercase tracking-wide">{card.label}</span>
            </div>
            <div className="text-xl font-bold text-[var(--text-primary)]">{Math.round(value)}{card.suffix || ''}</div>
          </div>
        )
      })}
    </div>
  )
}
