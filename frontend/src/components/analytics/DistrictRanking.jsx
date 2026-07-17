import { districtRanking } from './analyticsData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateDistrictName } from '../../utils/translate'

const flagEmoji = {
  'Bengaluru Urban': '🏙️',
  'Mysuru': '🏰',
  'Mangaluru': '⚓',
  'Hubballi': '🏛️',
  'Other': '📍',
}

export default function DistrictRanking() {
  const { lang } = useLanguage()

  return (
    <div className="analytics-district-card">
      <div className="analytics-district-header">
        <h3>{t('top_districts', lang)}</h3>
        <span className="analytics-district-subtitle">{t('by_case_count', lang)}</span>
      </div>

      <div className="analytics-district-list">
        {districtRanking.map((d, i) => (
          <div key={i} className="district-item">
            <div className="district-item-left">
              <span className="district-flag">{flagEmoji[d.district] || '📍'}</span>
              <span className="district-name">{translateDistrictName(d.district, lang)}</span>
            </div>
            <div className="district-item-right">
              <span className="district-percentage">{d.percentage}%</span>
              <span className="district-cases">{d.cases.toLocaleString()} {t('cases_label', lang)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
