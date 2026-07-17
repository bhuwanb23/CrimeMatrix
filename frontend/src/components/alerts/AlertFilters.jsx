import { alertTypes } from './alertsData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateAlertType } from '../../utils/translate'

export default function AlertFilters({ activeFilter, onFilterChange }) {
  const { lang } = useLanguage()

  const filters = [
    { id: 'all', label: t('all_alerts', lang) },
    ...Object.entries(alertTypes).map(([id]) => ({ id, label: translateAlertType(id, lang) })),
  ]

  return (
    <div className="alert-filters">
      <div className="alert-filters-scroll">
        {filters.map((filter) => (
          <button
            key={filter.id}
            className={`alert-filter-chip ${activeFilter === filter.id ? 'active' : ''}`}
            onClick={() => onFilterChange(filter.id)}
          >
            {filter.id !== 'all' && (
              <span
                className="filter-chip-dot"
                style={{ background: alertTypes[filter.id]?.color || 'var(--text-muted)' }}
              />
            )}
            {filter.label}
          </button>
        ))}
      </div>
    </div>
  )
}
