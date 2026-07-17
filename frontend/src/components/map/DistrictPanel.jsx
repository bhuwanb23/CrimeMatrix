import { MapPin, TrendingUp, AlertTriangle, Clock } from 'lucide-react'
import { hotspots, crimeDensity } from './mapData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateDistrictName, translateRisk, translateHotspot } from '../../utils/translate'

export default function DistrictPanel({ selectedDistrict }) {
  const { lang } = useLanguage()

  // Translate crime density labels
  const densityLabels = {
    'High (>100 cases)': 'High (>100 cases)',
    'Medium (50-100)': 'Medium (50-100)',
    'Low (<50)': 'Low (<50)',
  }
  const translateDensityLabel = (label) => {
    if (label.includes('High')) {
      return `${t('High', lang)} (>100 ${t('cases_label', lang)})`
    }
    if (label.includes('Medium')) {
      return `${t('Medium', lang)} (50-100)`
    }
    if (label.includes('Low')) {
      return `${t('Low', lang)} (<50)`
    }
    return label
  }

  return (
    <div className="district-panel">
      <div className="district-panel-header">
        <h3>{t('geo_intelligence', lang)}</h3>
      </div>

      {selectedDistrict ? (
        <div className="district-selected">
          <div className="district-selected-header">
            <MapPin size={16} />
            <h4>{translateDistrictName(selectedDistrict.name, lang)}</h4>
          </div>
          <div className="district-selected-stats">
            <div className="district-stat-row">
              <span className="district-stat-label">{t('total_cases', lang)}</span>
              <span className="district-stat-value">{selectedDistrict.cases}</span>
            </div>
            <div className="district-stat-row">
              <span className="district-stat-label">{t('hotspots', lang)}</span>
              <span className="district-stat-value">{selectedDistrict.hotspots}</span>
            </div>
            <div className="district-stat-row">
              <span className="district-stat-label">{t('risk_level', lang)}</span>
              <span className={`district-risk-badge ${selectedDistrict.risk}`}>
                {translateRisk(selectedDistrict.risk, lang)}
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div className="district-placeholder">
          <MapPin size={24} />
          <p>{t('click_district_desc', lang)}</p>
        </div>
      )}

      {/* Crime Density Legend */}
      <div className="district-section">
        <h4 className="district-section-title">
          <TrendingUp size={14} />
          {t('crime_density', lang)}
        </h4>
        <div className="density-legend">
          {crimeDensity.map((d, i) => (
            <div key={i} className="density-item">
              <span className="density-dot" style={{ background: d.color }} />
              <span className="density-label">{translateDensityLabel(d.label)}</span>
              <span className="density-count">{d.count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Hotspots */}
      <div className="district-section">
        <h4 className="district-section-title">
          <AlertTriangle size={14} />
          {t('recent_hotspots', lang)}
        </h4>
        <div className="hotspots-list">
          {hotspots.slice(0, 5).map((h, i) => (
            <div key={i} className="hotspot-item">
              <span className={`hotspot-dot ${h.severity}`} />
              <div className="hotspot-info">
                <span className="hotspot-name">{translateHotspot(h.name, lang)}</span>
                <span className="hotspot-cases">{h.cases} {t('cases_label', lang)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Route Info */}
      <div className="district-section">
        <h4 className="district-section-title">
          <Clock size={14} />
          {t('active_routes', lang)}
        </h4>
        <div className="route-legend">
          <div className="route-item">
            <span className="route-line" style={{ background: '#ef4444' }} />
            <span>{t('suspect_movement', lang)}</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#3b82f6' }} />
            <span>{t('evidence_link', lang)}</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#8b5cf6' }} />
            <span>{t('phone_records', lang)}</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#10b981' }} />
            <span>{t('case_connection', lang)}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
