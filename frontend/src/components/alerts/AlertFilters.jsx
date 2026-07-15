import { alertTypes } from './alertsData'

const filters = [
  { id: 'all', label: 'All' },
  ...Object.entries(alertTypes).map(([id, info]) => ({ id, label: info.label })),
]

export default function AlertFilters({ activeFilter, onFilterChange }) {
  return (
    <div className="alert-filters">
      {filters.map((filter) => (
        <button
          key={filter.id}
          className={`alert-filter-btn ${activeFilter === filter.id ? 'active' : ''}`}
          onClick={() => onFilterChange(filter.id)}
        >
          {filter.label}
        </button>
      ))}
    </div>
  )
}
