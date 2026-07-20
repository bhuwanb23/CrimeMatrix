import { Filter } from 'lucide-react'

const crimeTypes = [
  { value: '', label: 'All Types' },
  { value: '1', label: 'Theft' },
  { value: '2', label: 'Robbery' },
  { value: '3', label: 'Assault' },
  { value: '4', label: 'Murder' },
  { value: '5', label: 'Cybercrime' },
  { value: '6', label: 'Fraud' },
  { value: '7', label: 'Missing' },
  { value: '8', label: 'Burglary' },
]

const riskLevels = [
  { value: '', label: 'All Risk' },
  { value: 'critical', label: 'Critical' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
]

export default function MapFilterPanel({ filters, onChange }) {
  return (
    <div className="map-filter-panel">
      <div className="map-filter-header">
        <Filter size={14} />
        <span>Filters</span>
      </div>
      <select
        className="map-filter-select"
        value={filters.crime_type || ''}
        onChange={(e) => onChange({ ...filters, crime_type: e.target.value })}
      >
        {crimeTypes.map((ct) => (
          <option key={ct.value} value={ct.value}>{ct.label}</option>
        ))}
      </select>
      <select
        className="map-filter-select"
        value={filters.risk_level || ''}
        onChange={(e) => onChange({ ...filters, risk_level: e.target.value })}
      >
        {riskLevels.map((rl) => (
          <option key={rl.value} value={rl.value}>{rl.label}</option>
        ))}
      </select>
    </div>
  )
}
