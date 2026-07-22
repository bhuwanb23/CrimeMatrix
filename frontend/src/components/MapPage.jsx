import { useState, useEffect, useCallback } from 'react'
import { RefreshCw, MapPin } from 'lucide-react'
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

  const loadMapData = useCallback(async () => {
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
  }, [days, filters.crime_type])

  useEffect(() => {
    loadMapData()
  }, [loadMapData])

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
    <div className="flex flex-col gap-3 -m-6 p-4 h-[calc(100vh-var(--header-height))] min-h-0 overflow-hidden max-md:-m-4 max-md:p-3 max-md:h-auto max-md:min-h-[calc(100vh-var(--header-height))]">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 text-white shadow-lg shadow-orange-500/20 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
              <MapPin size={20} />
            </div>
            <div>
              <h1 className="text-lg font-bold">Geo Intelligence</h1>
              <p className="text-white/80 text-xs">Stations, spatial analysis & crime mapping</p>
            </div>
          </div>
          {stats && (
            <dl className="flex items-center m-0 min-w-0 overflow-x-auto">
              {statItems.map((item, i) => (
                <div key={item.key} className={`flex flex-col gap-0.5 px-3 whitespace-nowrap ${i > 0 ? 'border-l border-white/30' : ''}`}>
                  <dt className="m-0 text-[10px] font-medium uppercase tracking-wide text-white/60">{item.label}</dt>
                  <dd className="m-0 text-[15px] font-bold tabular-nums text-white">{stats[item.key] ?? 0}</dd>
                </div>
              ))}
            </dl>
          )}
          <button type="button" onClick={loadMapData} disabled={loading}
            className="inline-flex items-center gap-1.5 px-3 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-lg text-xs font-medium text-white whitespace-nowrap shrink-0 transition-colors disabled:opacity-60">
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>
      </div>

      <div
        role="toolbar"
        aria-label="Map controls"
        className="flex items-center gap-3 flex-wrap px-3 py-2.5 bg-white border border-slate-200 rounded-[10px] shrink-0"
      >
        <MapLayerControls activeLayers={activeLayers} onToggleLayer={toggleLayer} />
        <div className="w-px h-6 bg-slate-200 shrink-0 max-lg:hidden" aria-hidden="true" />
        <MapTimeSlider days={days} onChange={setDays} />
        <div className="w-px h-6 bg-slate-200 shrink-0 max-lg:hidden" aria-hidden="true" />
        <MapFilterPanel filters={filters} onChange={setFilters} />
      </div>

      <div className="flex gap-3 flex-1 min-h-0 min-w-0 max-lg:flex-col">
        <div className="flex flex-1 flex-col min-w-0 min-h-0 bg-white border border-slate-200 rounded-xl overflow-hidden max-lg:min-h-[min(52vh,480px)] max-lg:order-1 max-md:min-h-[360px]">
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
