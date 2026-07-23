import { BarChart3 } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function CrimeTypePredictions({ predictions }) {
  const { t } = useLanguage()
  if (!predictions || predictions.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <BarChart3 size={14} />
          <h3>{t('Crime Type Predictions')}</h3>
        </div>
        <div className="similar-empty"><p>{t('No predictions yet')}</p></div>
      </div>
    )
  }

  // Group by crime type
  const grouped = {}
  predictions.forEach(p => {
    const key = p.crime_type_id || 'unknown'
    if (!grouped[key]) grouped[key] = { type_id: key, predictions: [], total: 0 }
    grouped[key].predictions.push(p)
    grouped[key].total += p.predicted_value || 0
  })

  const types = Object.values(grouped).sort((a, b) => b.total - a.total)
  const maxTotal = Math.max(...types.map(t => t.total), 1)

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <BarChart3 size={14} />
        <h3>{t('Crime Type Predictions')}</h3>
      </div>
      <div className="analytics-type-list">
        {types.map((t, i) => (
          <div key={i} className="analytics-type-item">
            <div className="analytics-type-header">
              <span className="analytics-type-name">{t('Type')} #{t.type_id}</span>
              <span className="analytics-type-count">{Math.round(t.total)}</span>
            </div>
            <div className="analytics-type-bar">
              <div className="analytics-type-fill" style={{ width: `${(t.total / maxTotal) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
