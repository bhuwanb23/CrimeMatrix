import { useLanguage } from '../../context/LanguageContext'

const categories = [
  { label: 'Theft', value: 42000, pct: 33, color: '#e57373' },
  { label: 'Fraud', value: 28000, pct: 22, color: '#ef9a9a' },
  { label: 'Assault', value: 22000, pct: 17, color: '#ffcdd2' },
  { label: 'Cybercrime', value: 18000, pct: 14, color: '#fbe9e7' },
  { label: 'Other', value: 18000, pct: 14, color: '#f5f5f5' },
]

export default function CrimeTypeChart() {
  const { t } = useLanguage()

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">{t('Cases by Crime Type')}</h3>
        <button className="chart-card-menu" aria-label="More options">⋯</button>
      </div>
      <div className="chart-card-body">
        <div className="category-total">
          <span className="category-total-value">1,284</span>
          <span className="category-total-trend">↑ 15% {t('vs 30 Days')}</span>
        </div>

        {/* Stacked Bar */}
        <div className="category-bar">
          {categories.map((cat, i) => (
            <div
              key={i}
              className="category-bar-segment"
              style={{ width: `${cat.pct}%`, background: cat.color }}
            />
          ))}
        </div>

        {/* List */}
        <div className="category-list">
          {categories.map((cat, i) => (
            <div key={i} className="category-list-item">
              <div className="category-list-left">
                <span className="category-dot" style={{ background: cat.color }} />
                <span className="category-label">{t(cat.label)}</span>
              </div>
              <div className="category-list-right">
                <span className="category-value">{cat.value.toLocaleString()}</span>
                <span className="category-pct">({cat.pct}%)</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

