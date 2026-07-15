import { alertTypes } from './alertsData'
import { districts, karnatakaOutline } from '../map/mapData'

export default function AlertMap({ alerts }) {
  return (
    <div className="alert-map-card">
      <div className="alert-map-header">
        <h3>Alert Locations</h3>
        <span className="alert-map-count">{alerts.length} alerts</span>
      </div>

      <div className="alert-map-container">
        <svg className="alert-map-svg" viewBox="100 50 500 450">
          <defs>
            <pattern id="alertGrid" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="0.5" fill="var(--border)" opacity="0.3" />
            </pattern>
            <radialGradient id="alertGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="var(--color-accent)" stopOpacity="0.15" />
              <stop offset="100%" stopColor="var(--color-accent)" stopOpacity="0" />
            </radialGradient>
          </defs>

          <rect width="100%" height="100%" fill="url(#alertGrid)" />
          <path d={karnatakaOutline} fill="none" stroke="var(--border)" strokeWidth="1.5" opacity="0.4" />

          {districts.map((d) => (
            <g key={d.id}>
              <circle cx={d.x} cy={d.y} r="3" fill="var(--border)" opacity="0.5" />
              <text x={d.x} y={d.y + 16} textAnchor="middle" fontSize="8" fill="var(--text-muted)" opacity="0.5">
                {d.name.split(' ')[0]}
              </text>
            </g>
          ))}

          {alerts.map((alert) => {
            const typeInfo = alertTypes[alert.type]
            return (
              <g key={alert.id} transform={`translate(${alert.x}, ${alert.y})`} className="alert-map-marker">
                <circle r="12" fill={typeInfo.color} opacity="0.15" />
                <circle r="6" fill={typeInfo.color} opacity="0.9" />
                <circle r="2.5" fill="white" />
              </g>
            )
          })}
        </svg>
      </div>

      <div className="alert-map-legend">
        {Object.entries(alertTypes).map(([id, info]) => (
          <div key={id} className="alert-legend-item">
            <span className="alert-legend-dot" style={{ background: info.color }} />
            <span className="alert-legend-label">{info.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
