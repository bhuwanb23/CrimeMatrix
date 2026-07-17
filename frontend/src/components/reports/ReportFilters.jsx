import { Search, Download, ChevronDown } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function ReportFilters({ filters, onFilterChange, onExport }) {
  const { lang } = useLanguage()
  return (
    <div className="report-filters">
      <div className="report-search">
        <Search size={14} />
        <input
          type="text"
          placeholder={t('search_reports_placeholder', lang)}
          value={filters.search}
          onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
        />
      </div>

      <div className="report-filter-group">
        <div className="report-filter-select">
          <span>{t('date', lang)}: {filters.date || t('all_period', lang)}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>{t('type', lang)}: {filters.type || t('all_types', lang)}</span>
          <ChevronDown size={12} />
        </div>
        <div className="report-filter-select">
          <span>{t('status', lang)}: {filters.status || t('all_statuses', lang)}</span>
          <ChevronDown size={12} />
        </div>
      </div>

      <button className="report-export-btn" onClick={onExport}>
        <Download size={14} />
        {t('export_csv', lang)}
      </button>
    </div>
  )
}
