import { X } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


const filters = [
  { id: 'all', label: 'All' },
  { id: 'fir', label: 'FIR' },
  { id: 'suspects', label: 'Suspects' },
  { id: 'theft', label: 'Theft' },
  { id: 'fraud', label: 'Fraud' },
  { id: 'assault', label: 'Assault' },
  { id: 'cybercrime', label: 'Cybercrime' },
  { id: 'bengaluru', label: 'Bengaluru' },
  { id: 'mysuru', label: 'Mysuru' },
  { id: 'active', label: 'Active' },
  { id: 'pending', label: 'Pending' },
]

export default function FilterChips({ activeFilters, onToggleFilter, onClearAll }) {
  const { t } = useLanguage()
  return (
    <div className="filter-chips-row">
      <div className="filter-chips">
        {filters.map((filter) => (
          <button
            key={filter.id}
            className={`filter-chip ${activeFilters.includes(filter.id) ? 'active' : ''}`}
            onClick={() => onToggleFilter(filter.id)}
          >
            {t(filter.label)}
          </button>
        ))}
      </div>
      {activeFilters.length > 0 && (
        <button className="filter-clear" onClick={onClearAll}>
          <X size={14} />
          {t('Clear all')}
        </button>
      )}
    </div>
  )
}
