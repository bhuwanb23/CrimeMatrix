import { MapPin } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const COLORS = ['#f59e0b', '#3b82f6', '#10b981', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16']

export default function DistrictComparisonChart({ districts }) {
  const { t } = useLanguage()

  if (!districts || Object.keys(districts).length === 0) {
    return (
      <div className="trend-chart-widget">
        <div className="intel-widget-header">
          <h3><MapPin size={14} /> {t('District Comparison')}</h3>
        </div>
        <div className="similar-empty"><p>{t('No district data')}</p></div>
      </div>
    )
  }

  const entries = Object.entries(districts)
  const allTotals = entries.map(([, v]) => v.total || 0)
  const maxTotal = Math.max(...allTotals, 1)

  return (
    <div className="trend-chart-widget">
      <div className="intel-widget-header">
        <h3><MapPin size={14} /> {t('District Comparison')}</h3>
      </div>

      <div className="district-compare-list">
        {entries.map(([name, data], i) => {
          const color = COLORS[i % COLORS.length]
          const total = data.total || 0
          return (
            <div key={name} className="district-compare-item">
              <div className="district-compare-header">
                <div className="district-compare-dot" style={{ background: color }} />
                <span className="district-compare-name">{name}</span>
                <span className="district-compare-total">{total}</span>
              </div>
              <div className="district-compare-bar">
                <div
                  className="district-compare-fill"
                  style={{ width: `${(total / maxTotal) * 100}%`, background: color }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
