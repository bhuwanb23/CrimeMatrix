import { Search, Download, ChevronDown } from 'lucide-react'

export default function ReportFilters({ filters, onFilterChange, onExport }) {
  return (
    <div className="report-filters">
      <div className="report-search">
        <Search size={14} />
        <input
          type="text"
          placeholder="Search by report ID, title, case..."
          value={filters.search}
          onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
        />
      </div>

      <div className="report-filter-group">
        <div className="report-filter-select">
          <span>Date: {filters.date || 'All period'}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>Type: {filters.type || 'All types'}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>Status: {filters.status || 'All statuses'}</span>
          <ChevronDown size={12} />
        </div>
      </div>

      <button className="report-export-btn" onClick={onExport}>
        <Download size={14} />
        Export CSV
      </button>
    </div>
  )
}
