import { useState, useEffect } from 'react'
import { MapPin, RefreshCw } from 'lucide-react'
import MapCanvas from './map/MapCanvas'
import DistrictPanel from './map/DistrictPanel'
import StatsBar from './map/StatsBar'
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
  }, [days])

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

  return (
    <div className="map-page">
      <div className="map-sidebar">
        <div className="map-sidebar-header">
          <MapPin size={18} />
          <div>
            <h1>Geo Intelligence</h1>
            <p>Crime maps & spatial analysis</p>
          </div>
        </div>

        <MapLayerControls activeLayers={activeLayers} onToggleLayer={toggleLayer} />
        <MapTimeSlider days={days} onChange={setDays} />
        <MapFilterPanel filters={filters} onChange={setFilters} />

        {stats && (
          <div className="map-stats-panel">
            <div className="map-stat-item">
              <span className="map-stat-value">{stats.total_crimes || 0}</span>
              <span className="map-stat-label">Crimes</span>
            </div>
            <div className="map-stat-item">
              <span className="map-stat-value">{stats.total_districts || 0}</span>
              <span className="map-stat-label">Districts</span>
            </div>
            <div className="map-stat-item">
              <span className="map-stat-value">{stats.total_stations || 0}</span>
              <span className="map-stat-label">Stations</span>
            </div>
            <div className="map-stat-item">
              <span className="map-stat-value">{stats.total_hotspots || 0}</span>
              <span className="map-stat-label">Hotspots</span>
            </div>
          </div>
        )}

        <button className="map-refresh-btn" onClick={loadMapData} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          Refresh Data
        </button>
      </div>

      <div className="map-main">
        <MapCanvas
          selectedDistrict={selectedDistrict}
          onDistrictSelect={setSelectedDistrict}
          activeLayers={activeLayers}
          mapData={mapData}
          loading={loading}
        />
      </div>

      <DistrictPanel selectedDistrict={selectedDistrict} />
    </div>
  )
}
