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
    <div className="flex flex-col gap-3 -m-6 p-4 h-[calc(100vh-var(--header-height))] min-h-0 overflow-hidden max-md:-m-4 max-md:p-3 max-md:h-auto max-md:min-h-[calc(100vh-var(--header-height))]">
      <header className="flex items-center gap-4 min-w-0 shrink-0 flex-wrap md:flex-nowrap">
        <div className="min-w-0 shrink-0">
          <h1 className="m-0 text-lg font-bold tracking-tight text-slate-900 [overflow-wrap:anywhere]">
            Stations
          </h1>
          <p className="m-0 mt-0.5 text-xs text-slate-400">
            Geo intelligence &amp; spatial analysis
          </p>
        </div>

        {stats && (
          <dl className="flex items-center m-0 ml-auto min-w-0 overflow-x-auto max-md:order-3 max-md:w-full max-md:ml-0 max-md:pt-1">
            {statItems.map((item, i) => (
              <div
                key={item.key}
                className={`flex flex-col gap-0.5 px-3.5 whitespace-nowrap ${i > 0 ? 'border-l border-slate-200' : 'max-md:pl-0'}`}
              >
                <dt className="m-0 text-[10px] font-medium uppercase tracking-wide text-slate-400">
                  {item.label}
                </dt>
                <dd className="m-0 text-[15px] font-bold tabular-nums text-slate-900">
                  {stats[item.key] ?? 0}
                </dd>
              </div>
            ))}
          </dl>
        )}

        <button
          type="button"
          onClick={loadMapData}
          disabled={loading}
          aria-label="Refresh map data"
          className="inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-white border border-slate-200 rounded-lg text-xs font-medium text-slate-500 whitespace-nowrap shrink-0 cursor-pointer transition-colors hover:border-amber-500 hover:text-amber-500 disabled:opacity-60 disabled:cursor-not-allowed focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2 max-md:ml-auto"
        >
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          <span className="max-md:hidden">Refresh</span>
        </button>
      </header>

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
