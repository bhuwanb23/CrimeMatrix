import { Search, Download, ChevronDown } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function ReportFilters({ filters, onFilterChange, onExport }) {
  const { t } = useLanguage()
  return (
    <div className="report-filters">
      <div className="report-search">
        <Search size={14} />
        <input
          type="text"
          placeholder={t('Search by report ID, title, case...')}
          value={filters.search}
          onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
        />
      </div>

      <div className="report-filter-group">
        <div className="report-filter-select">
          <span>{t('Date:')} {filters.date ? t(filters.date) : t('All period')}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>{t('Type:')} {filters.type ? t(filters.type) : t('All types')}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>{t('Status:')} {filters.status ? t(filters.status) : t('All statuses')}</span>
          <ChevronDown size={12} />
        </div>
      </div>

      <button className="report-export-btn" onClick={onExport}>
        <Download size={14} />
        {t('Export CSV')}
      </button>
    </div>
  )
}
