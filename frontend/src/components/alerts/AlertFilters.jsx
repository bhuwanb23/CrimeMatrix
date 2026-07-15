import { alertTypes } from './alertsData'

const filters = [
  { id: 'all', label: 'All Alerts' },
  ...Object.entries(alertTypes).map(([id, info]) => ({ id, label: info.label })),
]

export default function AlertFilters({ activeFilter, onFilterChange }) {
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
