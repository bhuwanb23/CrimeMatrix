import { Flame, AlertTriangle, MapPin, Clock } from 'lucide-react'
import { districts, hotspots } from './mapData'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function StatsBar() {
  const { lang } = useLanguage()
  const totalCases = districts.reduce((s, d) => s + d.cases, 0)
  const activeHotspots = hotspots.filter((h) => h.severity === 'high' || h.severity === 'medium').length

  return (
    <div className="map-stats-bar">
      <div className="map-stat-item">
        <Flame size={16} className="map-stat-icon" style={{ color: '#ef4444' }} />
        <div className="map-stat-info">
          <span className="map-stat-value">{activeHotspots}</span>
          <span className="map-stat-label">{t('recent_hotspots', lang)}</span>
        </div>
      </div>
      <div className="map-stat-item">
        <AlertTriangle size={16} className="map-stat-icon" style={{ color: '#f59e0b' }} />
        <div className="map-stat-info">
          <span className="map-stat-value">{totalCases.toLocaleString()}</span>
          <span className="map-stat-label">{t('total_cases', lang)}</span>
        </div>
      </div>
      <div className="map-stat-item">
        <MapPin size={16} className="map-stat-icon" style={{ color: '#3b82f6' }} />
        <div className="map-stat-info">
          <span className="map-stat-value">{districts.length}</span>
          <span className="map-stat-label">{t('districts', lang)}</span>
        </div>
      </div>
      <div className="map-stat-item">
        <Clock size={16} className="map-stat-icon" style={{ color: '#10b981' }} />
        <div className="map-stat-info">
          <span className="map-stat-value">{t('live', lang)}</span>
          <span className="map-stat-label">{t('last_updated', lang)}</span>
        </div>
      </div>
    </div>
  )
}
