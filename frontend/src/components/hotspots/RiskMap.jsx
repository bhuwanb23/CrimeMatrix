import { Shield, AlertTriangle } from 'lucide-react'

export default function RiskMap({ riskData }) {
  if (!riskData) return null

  const zones = riskData.risk_zones || {}
  const levels = [
    { key: 'critical', label: 'Critical', color: '#ef4444', icon: AlertTriangle },
    { key: 'high', label: 'High', color: '#f59e0b', icon: AlertTriangle },
    { key: 'medium', label: 'Medium', color: '#3b82f6', icon: Shield },
    { key: 'low', label: 'Low', color: '#10b981', icon: Shield },
  ]

  return (
    <div className="risk-map-widget">
      <div className="intel-widget-header">
        <h3><Shield size={14} /> Risk Zones</h3>
      </div>

      <div className="risk-zones-grid">
        {levels.map((level) => {
          const items = zones[level.key] || []
          const Icon = level.icon
          return (
            <div key={level.key} className="risk-zone-card">
              <div className="risk-zone-header">
                <Icon size={14} style={{ color: level.color }} />
                <span className="risk-zone-label" style={{ color: level.color }}>{level.label}</span>
                <span className="risk-zone-count">{items.length}</span>
              </div>
              <div className="risk-zone-bar">
                <div
                  className="risk-zone-fill"
                  style={{
                    width: `${riskData.total > 0 ? (items.length / riskData.total) * 100 : 0}%`,
                    background: level.color,
                  }}
                />
              </div>
              {items.length > 0 && (
                <div className="risk-zone-items">
                  {items.slice(0, 2).map((item, i) => (
                    <span key={i} className="risk-zone-item">{item.name}</span>
                  ))}
                  {items.length > 2 && <span className="risk-zone-more">+{items.length - 2} more</span>}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
