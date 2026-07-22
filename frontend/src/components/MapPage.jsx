import { useState, useEffect } from 'react'
import { RefreshCw } from 'lucide-react'
import MapCanvas from './map/MapCanvas'
import DistrictPanel from './map/DistrictPanel'
import MapLayerControls from './map/MapLayerControls'
import MapTimeSlider from './map/MapTimeSlider'
import MapFilterPanel from './map/MapFilterPanel'
import { getCrimeMarkers, getDistrictGeoJSON, getHeatmapData, getHotspotMarkers, getStationMarkers, getRouteData, getMapStats } from '../services/maps'

export default function MapPage() {
  const [selectedDistrict, setSelectedDistrict] = useState(null)
  const [activeLayers, setActiveLayers] = useState(['crimes', 'hotspots', 'stations'])
  const [days, setDays] = useState(30)
  const [filters, setFilters] = useState({ crime_type: '', risk_level: '' })
  const [mapData, setMapData] = useState({ crimes: null, districts: null, heatmap: null, hotspots: null, stations: null, routes: null })
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMapData()
  }, [days, filters.crime_type])

  async function loadMapData() {
    setLoading(true)
    try {
      const [crimesRes, districtsRes, heatmapRes, hotspotsRes, stationsRes, routesRes, statsRes] = await Promise.all([
        getCrimeMarkers({ days, crime_type_id: filters.crime_type || undefined }),
        getDistrictGeoJSON(),
        getHeatmapData(days),
        getHotspotMarkers(),
        getStationMarkers(),
        getRouteData(),
        getMapStats(),
      ])
      setMapData({
        crimes: crimesRes?.data || crimesRes,
        districts: districtsRes?.data || districtsRes,
        heatmap: heatmapRes?.data || heatmapRes,
        hotspots: hotspotsRes?.data || hotspotsRes,
        stations: stationsRes?.data || stationsRes,
        routes: routesRes?.data || routesRes,
      })
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load map data', e)
    } finally {
      setLoading(false)
    }
  }

  function toggleLayer(layerId) {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((l) => l !== layerId) : [...prev, layerId]
    )
  }

  function handleDistrictSelect(district) {
    setSelectedDistrict((prev) =>
      prev?.name === district?.name ? null : district
    )
  }

  const statItems = [
    { key: 'total_crimes', label: 'Crimes' },
    { key: 'total_districts', label: 'Districts' },
    { key: 'total_stations', label: 'Stations' },
    { key: 'total_hotspots', label: 'Hotspots' },
  ]

  return (
    <div className="map-page">
      <header className="map-top">
        <div className="map-top-title">
          <h1>Stations</h1>
          <p>Geo intelligence &amp; spatial analysis</p>
        </div>

        {stats && (
          <dl className="map-top-stats">
            {statItems.map((item) => (
              <div key={item.key} className="map-top-stat">
                <dt>{item.label}</dt>
                <dd>{stats[item.key] ?? 0}</dd>
              </div>
            ))}
          </dl>
        )}

        <button
          type="button"
          className="map-refresh-btn"
          onClick={loadMapData}
          disabled={loading}
          aria-label="Refresh map data"
        >
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          <span>Refresh</span>
        </button>
      </header>

      <div className="map-toolbar" role="toolbar" aria-label="Map controls">
        <MapLayerControls activeLayers={activeLayers} onToggleLayer={toggleLayer} />
        <div className="map-toolbar-divider" aria-hidden="true" />
        <MapTimeSlider days={days} onChange={setDays} />
        <div className="map-toolbar-divider" aria-hidden="true" />
        <MapFilterPanel filters={filters} onChange={setFilters} />
      </div>

      <div className="map-stage">
        <div className="map-main">
          <MapCanvas
            selectedDistrict={selectedDistrict}
            onDistrictSelect={handleDistrictSelect}
            activeLayers={activeLayers}
            mapData={mapData}
            loading={loading}
          />
        </div>

        <DistrictPanel
          selectedDistrict={selectedDistrict}
          onClose={() => setSelectedDistrict(null)}
        />
      </div>
    </div>
  )
}
