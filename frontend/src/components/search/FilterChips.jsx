import { X } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


const filters = [
  { id: 'all', label: t('All') },
  { id: 'fir', label: t('FIR') },
  { id: 'suspects', label: t('Suspects') },
  { id: 'theft', label: t('Theft') },
  { id: 'fraud', label: t('Fraud') },
  { id: 'assault', label: t('Assault') },
  { id: 'cybercrime', label: t('Cybercrime') },
  { id: 'bengaluru', label: t('Bengaluru') },
  { id: 'mysuru', label: t('Mysuru') },
  { id: 'active', label: t('Active') },
  { id: 'pending', label: t('Pending') },
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
            {filter.label}
          </button>
        ))}
      </div>
      {activeFilters.length > 0 && (
        <button className="filter-clear" onClick={onClearAll}>
          <X size={14} />
          Clear all
        </button>
      )}
    </div>
  )
}
