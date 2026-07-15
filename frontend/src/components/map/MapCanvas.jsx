import { useState, useRef, useCallback, useEffect } from 'react'
import MapMarker from './MapMarker'
import HeatmapOverlay from './HeatmapOverlay'
import { districts, hotspots, routes, karnatakaOutline } from './mapData'

const routeColors = {
  'suspect-movement': '#ef4444',
  'evidence-link': '#3b82f6',
  'case-link': '#10b981',
  'phone-link': '#8b5cf6',
}

export default function MapCanvas({ selectedDistrict, onDistrictSelect, activeView }) {
  const svgRef = useRef(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })

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

  const showHeatmap = activeView === 'all' || activeView === 'heatmap'
  const showHotspots = activeView === 'all' || activeView === 'hotspots'
  const showRoutes = activeView === 'all' || activeView === 'routes'

  return (
    <div className="map-canvas-container">
      <svg
        ref={svgRef}
        className="map-svg"
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

          {/* Heatmap overlay */}
          {showHeatmap && <HeatmapOverlay districts={districts} />}

          {/* Routes */}
          {showRoutes && routes.map((route, i) => {
            const from = districts.find((d) => d.id === route.from)
            const to = districts.find((d) => d.id === route.to)
            if (!from || !to) return null

            const midX = (from.x + to.x) / 2
            const midY = (from.y + to.y) / 2 - 20

            return (
              <g key={i} className="map-route">
                <path
                  d={`M ${from.x} ${from.y} Q ${midX} ${midY} ${to.x} ${to.y}`}
                  fill="none"
                  stroke={routeColors[route.type]}
                  strokeWidth="2"
                  strokeDasharray="6 4"
                  opacity="0.6"
                  className="route-path"
                />
              </g>
            )
          })}

          {/* District markers */}
          {districts.map((d) => (
            <MapMarker
              key={d.id}
              marker={d}
              type="district"
              isSelected={selectedDistrict?.id === d.id}
              onClick={onDistrictSelect}
            />
          ))}

          {/* Hotspot markers */}
          {showHotspots && hotspots.map((h) => (
            <MapMarker
              key={h.id}
              marker={h}
              type="hotspot"
              isSelected={false}
              onClick={() => {}}
            />
          ))}
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
      </svg>
    </div>
  )
}
