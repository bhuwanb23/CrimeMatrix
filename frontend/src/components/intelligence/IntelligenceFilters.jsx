import { Search, RotateCcw } from 'lucide-react'

const timeRanges = [
  { value: '7d', label: '7 Days' },
  { value: '30d', label: '30 Days' },
  { value: '90d', label: '90 Days' },
  { value: '1y', label: '1 Year' },
]

const districts = [
  'All Districts', 'Bengaluru Urban', 'Bengaluru Rural', 'Mysuru',
  'Mangaluru', 'Hubballi', 'Belagavi', 'Kalaburagi', 'Ballari',
]

const crimeTypes = [
  'All Types', 'Theft', 'Robbery', 'Assault', 'Murder', 'Cybercrime',
  'Fraud', 'Missing', 'Burglary', 'Drug Offense',
]

export default function IntelligenceFilters({ filters, onChange }) {
  function handleReset() {
    onChange({ district: '', time_range: '30d', crime_type: '' })
  }

  return (
    <div className="intel-filters">
      <div className="intel-filter-group">
        <label className="intel-filter-label">District</label>
        <select
          className="intel-filter-select"
          value={filters.district || ''}
          onChange={(e) => onChange({ ...filters, district: e.target.value })}
        >
          {districts.map((d) => (
            <option key={d} value={d === 'All Districts' ? '' : d}>{d}</option>
          ))}
        </select>
      </div>

      <div className="intel-filter-group">
        <label className="intel-filter-label">Time Range</label>
        <div className="intel-time-btns">
          {timeRanges.map((tr) => (
            <button
              key={tr.value}
              className={`intel-time-btn ${filters.time_range === tr.value ? 'active' : ''}`}
              onClick={() => onChange({ ...filters, time_range: tr.value })}
            >
              {tr.label}
            </button>
          ))}
        </div>
      </div>

      <div className="intel-filter-group">
        <label className="intel-filter-label">Crime Type</label>
        <select
          className="intel-filter-select"
          value={filters.crime_type || ''}
          onChange={(e) => onChange({ ...filters, crime_type: e.target.value })}
        >
          {crimeTypes.map((ct) => (
            <option key={ct} value={ct === 'All Types' ? '' : ct}>{ct}</option>
          ))}
        </select>
      </div>

      <button className="intel-filter-reset" onClick={handleReset}>
        <RotateCcw size={12} />
        Reset
      </button>
    </div>
  )
}
