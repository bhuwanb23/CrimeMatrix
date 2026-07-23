import { RotateCcw } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function IntelligenceFilters({ filters, onChange }) {
  const { t } = useLanguage()

  const timeRanges = [
    { value: '7d', label: t('7 Days') },
    { value: '30d', label: t('30 Days') },
    { value: '90d', label: t('90 Days') },
    { value: '1y', label: t('1 Year') },
  ]

  const districts = [
    t('All Districts'), t('Bengaluru Urban'), t('Bengaluru Rural'), t('Mysuru'),
    t('Mangaluru'), t('Hubballi'), t('Belagavi'), t('Kalaburagi'), t('Ballari'),
  ]

  const crimeTypes = [
    t('All Types'), t('Theft'), t('Robbery'), t('Assault'), t('Murder'), t('Cybercrime'),
    t('Fraud'), t('Missing'), t('Burglary'), t('Drug Offense'),
  ]

  function handleReset() {
    onChange({ district: '', time_range: '30d', crime_type: '' })
  }

  return (
    <div className="intel-filters">
      <div className="intel-filter-group">
        <label className="intel-filter-label">{t('District')}</label>
        <select
          className="intel-filter-select"
          value={filters.district || ''}
          onChange={(e) => onChange({ ...filters, district: e.target.value })}
        >
          {districts.map((d) => (
            <option key={d} value={d === t('All Districts') ? '' : d}>{d}</option>
          ))}
        </select>
      </div>

      <div className="intel-filter-group">
        <label className="intel-filter-label">{t('Time Range')}</label>
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
        <label className="intel-filter-label">{t('Crime Type')}</label>
        <select
          className="intel-filter-select"
          value={filters.crime_type || ''}
          onChange={(e) => onChange({ ...filters, crime_type: e.target.value })}
        >
          {crimeTypes.map((ct) => (
            <option key={ct} value={ct === t('All Types') ? '' : ct}>{ct}</option>
          ))}
        </select>
      </div>

      <button className="intel-filter-reset" onClick={handleReset}>
        <RotateCcw size={12} />
        {t('Reset')}
      </button>
    </div>
  )
}

