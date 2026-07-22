import { useState, useRef, useCallback, useEffect } from 'react'
import MapMarker from './MapMarker'
import HeatmapOverlay from './HeatmapOverlay'
import { districts as fallbackDistricts, hotspots as fallbackHotspots, routes as fallbackRoutes, karnatakaOutline } from './mapData'

const routeColors = {
  'suspect-movement': '#ef4444',
  'evidence-link': '#3b82f6',
  'case-link': '#10b981',
  'phone-link': '#8b5cf6',
}

// Convert lat/lng to SVG coordinates (simple projection for Karnataka)
function latLngToSvg(lat, lng) {
  const minLat = 11.0, maxLat = 18.5
  const minLng = 74.0, maxLng = 78.5
  const svgWidth = 600, svgHeight = 500
  const x = ((lng - minLng) / (maxLng - minLng)) * svgWidth
  const y = ((maxLat - lat) / (maxLat - minLat)) * svgHeight
  return { x, y }
}

export default function MapCanvas({ selectedDistrict, onDistrictSelect, activeLayers = [], mapData, loading }) {
  const svgRef = useRef(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [hoveredMarker, setHoveredMarker] = useState(null)

  const handleWheel = useCallback((e) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? -0.1 : 0.1
    setZoom((z) => Math.max(0.5, Math.min(3, z + delta)))
  }, [])

  useEffect(() => {
    const svg = svgRef.current
    if (svg) {
      svg.addEventListener('wheel', handleWheel, { passive: false })
      return () => svg.removeEventListener('wheel', handleWheel)
    }
  }, [handleWheel])

  const handleMouseDown = (e) => {
    if (e.target === svgRef.current || e.target.classList.contains('map-bg')) {
      setIsPanning(true)
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
    }
  }

  const handleMouseMove = (e) => {
    if (isPanning) {
      setPan({ x: e.clientX - panStart.x, y: e.clientY - panStart.y })
    }
  }

  const handleMouseUp = () => setIsPanning(false)

  const handleZoomIn = () => setZoom((z) => Math.min(3, z + 0.2))
  const handleZoomOut = () => setZoom((z) => Math.max(0.5, z - 0.2))
  const handleReset = () => { setZoom(1); setPan({ x: 0, y: 0 }) }

  // Use real data if available, fallback to hardcoded
  const crimeFeatures = mapData?.crimes?.features || []
  const districtFeatures = mapData?.districts?.features || []
  const heatmapPoints = mapData?.heatmap?.points || []
  const hotspotFeatures = mapData?.hotspots?.features || []
  const stationFeatures = mapData?.stations?.features || []
  const routeData = mapData?.routes?.routes || []

  const showCrimes = activeLayers.includes('crimes')
  const showHotspots = activeLayers.includes('hotspots')
  const showStations = activeLayers.includes('stations')
  const showRoutes = activeLayers.includes('routes')
  const showDensity = activeLayers.includes('density')

  return (
    <div className="relative h-full w-full bg-slate-50">
      {loading && (
        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-2 bg-slate-50/70 text-xs text-slate-900">
          <div className="similar-spinner" />
          <span>Loading map data...</span>
        </div>
      )}

      <svg
        ref={svgRef}
        className="h-full w-full cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <defs>
          <pattern id="gridPattern" width="30" height="30" patternUnits="userSpaceOnUse">
            <circle cx="15" cy="15" r="0.8" fill="var(--border)" opacity="0.3" />
          </pattern>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <radialGradient id="heatGradient">
            <stop offset="0%" stopColor="#ef4444" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#ef4444" stopOpacity="0" />
          </radialGradient>
        </defs>

        <rect className="map-bg" width="100%" height="100%" fill="url(#gridPattern)" />

        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {/* Karnataka outline */}
          <path
            d={karnatakaOutline}
            fill="none"
            stroke="var(--border-strong)"
            strokeWidth="2"
            className="map-outline"
          />

          {/* Density / Heatmap layer */}
          {showDensity && heatmapPoints.map((p, i) => {
            const pos = latLngToSvg(p.lat, p.lng)
            const radius = 15 + Math.sqrt(p.count) * 3
            const color = p.count > 10 ? '#ef4444' : p.count > 5 ? '#f59e0b' : '#10b981'
            return (
              <circle
                key={`heat-${i}`}
                cx={pos.x}
                cy={pos.y}
                r={radius}
                fill={color}
                opacity={0.2}
                className="map-heat-circle"
              />
            )
          })}

          {/* Crime markers */}
          {showCrimes && crimeFeatures.slice(0, 200).map((f, i) => {
            const [lng, lat] = f.geometry.coordinates
            const pos = latLngToSvg(lat, lng)
            const props = f.properties
            const color = props.status === 'open' ? '#ef4444' : props.status === 'closed' ? '#10b981' : '#f59e0b'
            return (
              <g key={`crime-${i}`} onMouseEnter={() => setHoveredMarker(props)} onMouseLeave={() => setHoveredMarker(null)}>
                <circle cx={pos.x} cy={pos.y} r={4} fill={color} stroke="white" strokeWidth={1} className="cursor-pointer" />
              </g>
            )
          })}

          {/* District markers */}
          {districtFeatures.map((f, i) => {
            const [lng, lat] = f.geometry.coordinates
            const pos = latLngToSvg(lat, lng)
            const props = f.properties
            const riskColor = props.risk_level === 'high' ? '#ef4444' : props.risk_level === 'medium' ? '#f59e0b' : '#10b981'
            return (
              <g key={`district-${i}`} onClick={() => onDistrictSelect?.(props)} className="cursor-pointer">
                <circle cx={pos.x} cy={pos.y} r={12} fill={riskColor} opacity={0.3} />
                <circle cx={pos.x} cy={pos.y} r={6} fill={riskColor} stroke="white" strokeWidth={2} />
                <text x={pos.x} y={pos.y - 16} textAnchor="middle" fontSize={10} fill="var(--text-primary)" fontWeight="600">
                  {props.name}
                </text>
                <text x={pos.x} y={pos.y + 20} textAnchor="middle" fontSize={9} fill="var(--text-muted)">
                  {props.crime_count} crimes
                </text>
              </g>
            )
          })}

          {/* Hotspot markers */}
          {showHotspots && hotspotFeatures.map((f, i) => {
            const [lng, lat] = f.geometry.coordinates
            const pos = latLngToSvg(lat, lng)
            const props = f.properties
            const riskColor = props.risk_level === 'critical' ? '#ef4444' : props.risk_level === 'high' ? '#f59e0b' : '#3b82f6'
            return (
              <g key={`hotspot-${i}`} className="map-hotspot-marker">
                <circle cx={pos.x} cy={pos.y} r={16} fill={riskColor} opacity={0.15} />
                <circle cx={pos.x} cy={pos.y} r={8} fill={riskColor} opacity={0.4} />
                <circle cx={pos.x} cy={pos.y} r={4} fill={riskColor} stroke="white" strokeWidth={1.5} />
                <text x={pos.x} y={pos.y - 22} textAnchor="middle" fontSize={9} fill={riskColor} fontWeight="600">
                  {props.name}
                </text>
              </g>
            )
          })}

          {/* Station markers */}
          {showStations && stationFeatures.map((f, i) => {
            const [lng, lat] = f.geometry.coordinates
            const pos = latLngToSvg(lat, lng)
            const props = f.properties
            return (
              <g key={`station-${i}`} className="map-station-marker">
                <rect x={pos.x - 5} y={pos.y - 5} width={10} height={10} fill="#3b82f6" stroke="white" strokeWidth={1.5} rx={2} />
                <text x={pos.x} y={pos.y - 10} textAnchor="middle" fontSize={8} fill="#3b82f6">
                  {props.name}
                </text>
              </g>
            )
          })}

          {/* Route lines */}
          {showRoutes && routeData.map((route, i) => {
            const from = latLngToSvg(route.from.lat, route.from.lng)
            const to = latLngToSvg(route.to.lat, route.to.lng)
            const midX = (from.x + to.x) / 2
            const midY = (from.y + to.y) / 2 - 20
            const color = routeColors[route.type] || '#8b5cf6'
            return (
              <g key={`route-${i}`} className="map-route">
                <path
                  d={`M ${from.x} ${from.y} Q ${midX} ${midY} ${to.x} ${to.y}`}
                  fill="none"
                  stroke={color}
                  strokeWidth="2"
                  strokeDasharray="6 4"
                  opacity="0.6"
                />
              </g>
            )
          })}
        </g>

        {/* Zoom controls */}
        <g className="map-zoom-controls">
          <rect x="20" y="20" width="36" height="80" rx="8" fill="var(--bg-card)" stroke="var(--border)" />
          <text x="38" y="46" textAnchor="middle" fontSize="16" fill="var(--text-muted)" style={{ cursor: 'pointer' }} onClick={handleZoomIn}>+</text>
          <line x1="28" y1="56" x2="48" y2="56" stroke="var(--border)" />
          <text x="38" y="76" textAnchor="middle" fontSize="16" fill="var(--text-muted)" style={{ cursor: 'pointer' }} onClick={handleZoomOut}>−</text>
          <line x1="28" y1="86" x2="48" y2="86" stroke="var(--border)" />
          <text x="38" y="94" textAnchor="middle" fontSize="10" fill="var(--text-muted)" style={{ cursor: 'pointer' }} onClick={handleReset}>⟳</text>
        </g>

        {/* Tooltip */}
        {hoveredMarker && (
          <g className="pointer-events-none">
            <rect x="50" y="20" width="180" height="60" rx="6" fill="var(--bg-card)" stroke="var(--border)" />
            <text x="60" y="38" fontSize="11" fontWeight="600" fill="var(--text-primary)">{hoveredMarker.title || hoveredMarker.name}</text>
            <text x="60" y="52" fontSize="9" fill="var(--text-muted)">{hoveredMarker.crime_type || hoveredMarker.district}</text>
            <text x="60" y="66" fontSize="9" fill="var(--text-muted)">Status: {hoveredMarker.status || 'N/A'}</text>
          </g>
        )}
      </svg>

      <div className="absolute bottom-4 left-4 z-5 flex flex-wrap gap-3 rounded-lg border border-slate-200 bg-white px-3 py-2 text-[10px] text-slate-400 max-md:inset-x-2 max-md:bottom-2 max-md:left-2">
        <div className="flex items-center gap-1 whitespace-nowrap">
          <span className="size-2 rounded-full bg-red-500" /> Open
        </div>
        <div className="flex items-center gap-1 whitespace-nowrap">
          <span className="size-2 rounded-full bg-emerald-500" /> Closed
        </div>
        <div className="flex items-center gap-1 whitespace-nowrap">
          <span className="size-2 rounded-full bg-amber-500" /> Pending
        </div>
        <div className="flex items-center gap-1 whitespace-nowrap">
          <span className="size-2 rounded-full bg-blue-500" /> Station
        </div>
      </div>
    </div>
  )
}
