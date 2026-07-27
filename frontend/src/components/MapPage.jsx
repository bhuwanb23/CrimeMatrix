import { useState, useEffect, useCallback } from 'react'
import { useLanguage } from '../context/LanguageContext'
import { RefreshCw, MapPin, PanelRightClose, PanelRightOpen } from 'lucide-react'
import MapCanvas from './map/MapCanvas'
import DistrictPanel from './map/DistrictPanel'
import MapLayerControls from './map/MapLayerControls'
import MapTimeSlider from './map/MapTimeSlider'
import MapFilterPanel from './map/MapFilterPanel'
import { getCrimeMarkers, getDistrictGeoJSON, getHeatmapData, getHotspotMarkers, getStationMarkers, getRouteData, getMapStats } from '../services/maps'
import useMediaQuery from '../hooks/useMediaQuery'

export default function MapPage() {
  const { t } = useLanguage()
  const isMobile = useMediaQuery('(max-width: 1023px)')
  const [selectedDistrict, setSelectedDistrict] = useState(null)
  const [districtPanelOpen, setDistrictPanelOpen] = useState(() => {
    if (typeof window === 'undefined') return true
    return !window.matchMedia('(max-width: 1023px)').matches
  })
  const [districtPanelDesktopPreference, setDistrictPanelDesktopPreference] = useState(true)
  const [activeLayers, setActiveLayers] = useState(['crimes', 'hotspots', 'stations'])
  const [days, setDays] = useState(30)
  const [filters, setFilters] = useState({ crime_type: '' })
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

  useEffect(() => {
    if (isMobile) {
      setDistrictPanelOpen(false)
      return
    }
    setDistrictPanelOpen(districtPanelDesktopPreference)
  }, [districtPanelDesktopPreference, isMobile])

  function toggleLayer(layerId) {
    setActiveLayers((prev) =>
      prev.includes(layerId) ? prev.filter((l) => l !== layerId) : [...prev, layerId]
    )
  }

  function handleDistrictSelect(district) {
    setSelectedDistrict((prev) =>
      prev?.name === district?.name ? null : district
    )
    if (isMobile) {
      setDistrictPanelOpen(true)
    }
  }

  function handleToggleDistrictPanel() {
    setDistrictPanelOpen((prev) => {
      const next = !prev
      if (!isMobile) setDistrictPanelDesktopPreference(next)
      return next
    })
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
              <h1 className="text-lg font-bold">{t('Geo Intelligence')}</h1>
              <p className="text-white/80 text-xs">{t('Stations, spatial analysis & crime mapping')}</p>
            </div>
          </div>
          {stats && (
            <dl className="flex items-center m-0 min-w-0 overflow-x-auto">
              {statItems.map((item, i) => (
                <div key={item.key} className={`flex flex-col gap-0.5 px-3 whitespace-nowrap ${i > 0 ? 'border-l border-white/30' : ''}`}>
                  <dt className="m-0 text-[10px] font-medium uppercase tracking-wide text-white/60">{t(item.label)}</dt>
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
        className="flex items-center gap-3 flex-wrap px-3 py-2.5 bg-[var(--bg-card)] border border-[var(--border)] rounded-[10px] shrink-0"
      >
        <MapLayerControls activeLayers={activeLayers} onToggleLayer={toggleLayer} />
        <div className="w-px h-6 bg-[var(--bg-input)] shrink-0 max-lg:hidden" aria-hidden="true" />
        <MapTimeSlider days={days} onChange={setDays} />
        <div className="w-px h-6 bg-[var(--bg-input)] shrink-0 max-lg:hidden" aria-hidden="true" />
        <MapFilterPanel filters={filters} onChange={setFilters} />
        <button
          type="button"
          onClick={handleToggleDistrictPanel}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-[var(--border)] bg-[var(--bg-card)] text-xs font-medium text-[var(--text-secondary)] hover:bg-[var(--bg-hover)]"
          aria-label={districtPanelOpen ? t('Hide panel') : t('Show panel')}
        >
          {districtPanelOpen ? <PanelRightClose size={14} /> : <PanelRightOpen size={14} />}
          <span>{t('Panel')}</span>
        </button>
      </div>

      <div className="flex gap-3 flex-1 min-h-0 min-w-0 max-lg:flex-col">
        <div className="flex flex-1 flex-col min-w-0 min-h-0 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden max-lg:min-h-[min(52vh,480px)] max-lg:order-1 max-md:min-h-[360px]">
          <MapCanvas
            selectedDistrict={selectedDistrict}
            onDistrictSelect={handleDistrictSelect}
            activeLayers={activeLayers}
            mapData={mapData}
            loading={loading}
          />
        </div>

        {!isMobile && districtPanelOpen && (
          <DistrictPanel
            selectedDistrict={selectedDistrict}
            onClose={() => setSelectedDistrict(null)}
            mapData={mapData}
            stats={stats}
          />
        )}
      </div>

      {isMobile && districtPanelOpen && (
        <>
          <button
            type="button"
            className="page-right-drawer-backdrop"
            aria-label={t('Close district panel')}
            onClick={() => setDistrictPanelOpen(false)}
          />
          <div className="page-right-drawer page-right-drawer-open">
            <DistrictPanel
              selectedDistrict={selectedDistrict}
              onClose={() => setDistrictPanelOpen(false)}
              mapData={mapData}
              stats={stats}
              className="w-full max-w-none max-lg:max-h-none max-md:max-h-none h-full rounded-none border-0"
            />
          </div>
        </>
      )}
    </div>
  )
}
