import { Filter } from 'lucide-react'

const crimeTypes = [
  { value: '', label: 'All types' },
  { value: '1', label: 'Theft' },
  { value: '2', label: 'Robbery' },
  { value: '3', label: 'Assault' },
  { value: '4', label: 'Murder' },
  { value: '5', label: 'Cybercrime' },
  { value: '6', label: 'Fraud' },
  { value: '7', label: 'Missing' },
  { value: '8', label: 'Burglary' },
]

const selectClass =
  'bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-[inherit] min-w-[110px] max-w-[160px] focus:outline-none focus:border-amber-500'

export default function MapFilterPanel({ filters, onChange }) {
  return (
    <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
      <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 whitespace-nowrap">
        <Filter size={13} aria-hidden="true" />
        Filters
      </span>
      <div className="flex items-center gap-1.5 flex-wrap">
        <label className="block min-w-0">
          <span className="sr-only">Crime type</span>
          <select
            className={selectClass}
            value={filters.crime_type || ''}
            onChange={(e) => onChange({ ...filters, crime_type: e.target.value })}
          >
            {crimeTypes.map((ct) => (
              <option key={ct.value} value={ct.value}>{ct.label}</option>
            ))}
          </select>
        </label>
      </div>
    </div>
  )
}
