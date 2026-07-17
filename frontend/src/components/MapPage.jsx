import { useState } from 'react'
import MapCanvas from './map/MapCanvas'
import DistrictPanel from './map/DistrictPanel'
import StatsBar from './map/StatsBar'

const views = [
  { id: 'all', label: 'All Layers' },
  { id: 'heatmap', label: 'Heatmap' },
  { id: 'hotspots', label: 'Hotspots' },
  { id: 'routes', label: 'Routes' },
]

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function MapPage() {
  const { lang } = useLanguage()
  const [selectedDistrict, setSelectedDistrict] = useState(null)
  const [activeView, setActiveView] = useState('all')

  return (
    <div className="map-page">
      <div className="map-main">
        <div className="map-header">
          <div>
            <h1 className="map-title">{t('geo_intelligence', lang)}</h1>
            <p className="map-subtitle">{t('crime_hotspots_density', lang)}</p>
          </div>
          <div className="map-view-btns">
            {views.map((v) => (
              <button
                key={v.id}
                className={`map-view-btn ${activeView === v.id ? 'active' : ''}`}
                onClick={() => setActiveView(v.id)}
              >
                {t(v.id.toLowerCase(), lang) || v.label}
              </button>
            ))}
          </div>
        </div>

        <MapCanvas
          selectedDistrict={selectedDistrict}
          onDistrictSelect={setSelectedDistrict}
          activeView={activeView}
        />

        <StatsBar />
      </div>

      <DistrictPanel selectedDistrict={selectedDistrict} />
    </div>
  )
}
