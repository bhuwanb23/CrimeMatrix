import { useState } from 'react'
import { alertTypes } from './alertsData'
import { districts, hotspots, karnatakaOutline } from '../map/mapData'

export default function AlertMap({ alerts, onAlertSelect, selectedAlert }) {
  const [hoveredAlert, setHoveredAlert] = useState(null)

  return (
    <div className="alert-map-card">
      <div className="alert-map-header">
        <h3>Crime Heatmap</h3>
        <div className="alert-map-legend">
          {Object.entries(alertTypes).map(([id, info]) => (
            <div key={id} className="alert-legend-item">
              <span className="alert-legend-dot" style={{ background: info.color }} />
              <span className="alert-legend-label">{info.label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="alert-map-container">
        <svg className="alert-map-svg" viewBox="100 50 500 450">
          <defs>
            <pattern id="alertGrid" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="0.5" fill="var(--border)" opacity="0.3" />
            </pattern>
          </defs>

          <rect width="100%" height="100%" fill="url(#alertGrid)" />
          <path d={karnatakaOutline} fill="none" stroke="var(--border)" strokeWidth="1.5" opacity="0.4" />

          {/* Heatmap circles for districts */}
          {districts.map((d) => {
            const radius = 15 + Math.sqrt(d.cases) * 1.5
            const opacity = d.risk === 'high' ? 0.2 : d.risk === 'medium' ? 0.12 : 0.06
            const color = d.risk === 'high' ? '#ef4444' : d.risk === 'medium' ? '#f59e0b' : '#10b981'
            return (
              <circle key={d.id} cx={d.x} cy={d.y} r={radius} fill={color} opacity={opacity} />
            )
          })}

          {/* District labels */}
          {districts.map((d) => (
            <text key={d.id} x={d.x} y={d.y + 25} textAnchor="middle" fontSize="8" fill="var(--text-muted)" opacity="0.5">
              {d.name.split(' ')[0]}
            </text>
          ))}

          {/* Alert markers */}
          {alerts.map((alert) => {
            const typeInfo = alertTypes[alert.type]
            const isSelected = selectedAlert?.id === alert.id
            const isHovered = hoveredAlert === alert.id
            const size = isSelected ? 10 : isHovered ? 8 : 6

            return (
              <g
                key={alert.id}
                transform={`translate(${alert.x}, ${alert.y})`}
                className="alert-map-marker"
                onClick={() => onAlertSelect(alert)}
                onMouseEnter={() => setHoveredAlert(alert.id)}
                onMouseLeave={() => setHoveredAlert(null)}
                style={{ cursor: 'pointer' }}
              >
                {isSelected && <circle r={size + 8} fill={typeInfo.color} opacity={0.15} />}
                <circle r={size} fill={typeInfo.color} opacity={0.9} />
                <circle r={2.5} fill="white" />
              </g>
            )
          })}
        </svg>

        {/* Selected alert tooltip */}
        {selectedAlert && (
          <div className="alert-map-tooltip">
            <div className="alert-tooltip-header">
              <span className="alert-tooltip-type" style={{ background: alertTypes[selectedAlert.type].color + '20', color: alertTypes[selectedAlert.type].color }}>
                {alertTypes[selectedAlert.type].label}
              </span>
              <span className={`alert-tooltip-priority ${selectedAlert.priority}`}>{selectedAlert.priority}</span>
            </div>
            <h4>{selectedAlert.title}</h4>
            <p>{selectedAlert.district} • {selectedAlert.timestamp}</p>
          </div>
        )}
      </div>
    </div>
  )
}
