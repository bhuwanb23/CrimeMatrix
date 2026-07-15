import { alertTypes } from './alertsData'
import { districts, karnatakaOutline } from '../map/mapData'

export default function AlertMap({ alerts }) {
  return (
    <div className="alert-map-card">
      <h3 className="alert-map-title">Alert Locations</h3>
      <svg className="alert-map-svg" viewBox="100 50 500 450">
        <defs>
          <pattern id="alertGrid" width="20" height="20" patternUnits="userSpaceOnUse">
            <circle cx="10" cy="10" r="0.5" fill="var(--border)" opacity="0.3" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#alertGrid)" />
        <path d={karnatakaOutline} fill="none" stroke="var(--border)" strokeWidth="1.5" opacity="0.5" />

        {districts.map((d) => (
          <text key={d.id} x={d.x} y={d.y + 20} textAnchor="middle" fontSize="8" fill="var(--text-muted)" opacity="0.6">
            {d.name.split(' ')[0]}
          </text>
        ))}

        {alerts.map((alert) => {
          const typeInfo = alertTypes[alert.type]
          return (
            <g key={alert.id} transform={`translate(${alert.x}, ${alert.y})`}>
              <circle r="6" fill={typeInfo.color} opacity="0.8" />
              <circle r="3" fill="white" />
            </g>
          )
        })}
      </svg>
    </div>
  )
}
