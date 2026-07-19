import { MapPin } from 'lucide-react'

export default function HotspotHeatmap({ hotspots }) {
  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="hotspot-heatmap">
        <div className="intel-widget-header">
          <h3><MapPin size={14} /> Crime Heatmap</h3>
        </div>
        <div className="similar-empty"><p>No heatmap data</p></div>
      </div>
    )
  }

  const maxCount = Math.max(...hotspots.map(h => h.crime_count || 0), 1)

  function getHeatColor(count) {
    const ratio = count / maxCount
    if (ratio > 0.8) return '#ef4444'
    if (ratio > 0.6) return '#f59e0b'
    if (ratio > 0.4) return '#3b82f6'
    if (ratio > 0.2) return '#10b981'
    return '#64748b'
  }

  return (
    <div className="hotspot-heatmap">
      <div className="intel-widget-header">
        <h3><MapPin size={14} /> Crime Heatmap</h3>
      </div>

      <div className="heatmap-visual">
        {hotspots.map((h, i) => {
          const color = getHeatColor(h.crime_count || 0)
          const size = 20 + ((h.crime_count || 0) / maxCount) * 40
          return (
            <div
              key={h.id || i}
              className="heatmap-point"
              style={{
                background: `${color}30`,
                borderColor: color,
                width: size,
                height: size,
              }}
              title={`${h.name}: ${h.crime_count} crimes (${h.risk_level})`}
            >
              <span className="heatmap-count">{h.crime_count}</span>
            </div>
          )
        })}
      </div>

      <div className="heatmap-legend">
        <span className="heatmap-legend-item"><span className="heatmap-dot" style={{ background: '#ef4444' }} /> Critical</span>
        <span className="heatmap-legend-item"><span className="heatmap-dot" style={{ background: '#f59e0b' }} /> High</span>
        <span className="heatmap-legend-item"><span className="heatmap-dot" style={{ background: '#3b82f6' }} /> Medium</span>
        <span className="heatmap-legend-item"><span className="heatmap-dot" style={{ background: '#10b981' }} /> Low</span>
      </div>
    </div>
  )
}
