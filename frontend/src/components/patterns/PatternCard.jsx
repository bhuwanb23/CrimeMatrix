import { Clock, MapPin, Crosshair, Layers, ChevronRight } from 'lucide-react'

const typeConfig = {
  time: { icon: Clock, label: 'Time Pattern', color: '#3b82f6' },
  mo: { icon: Crosshair, label: 'MO Pattern', color: '#ef4444' },
  location: { icon: MapPin, label: 'Location Pattern', color: '#10b981' },
  type: { icon: Layers, label: 'Type Pattern', color: '#8b5cf6' },
  combined: { icon: Layers, label: 'Combined', color: '#f59e0b' },
}

export default function PatternCard({ pattern, onClick }) {
  const config = typeConfig[pattern.pattern_type] || typeConfig.combined
  const Icon = config.icon

  return (
    <div className="pattern-card" onClick={() => onClick?.(pattern)}>
      <div className="pattern-card-header">
        <div className="pattern-card-icon" style={{ color: config.color }}>
          <Icon size={16} />
        </div>
        <div className="pattern-card-meta">
          <span className="pattern-card-type" style={{ color: config.color }}>{config.label}</span>
          <span className="pattern-card-freq">{pattern.frequency} crimes</span>
        </div>
        <div className="pattern-card-confidence">
          <span className="pattern-card-score">{pattern.confidence}%</span>
        </div>
      </div>

      <h4 className="pattern-card-name">{pattern.name}</h4>
      <p className="pattern-card-desc">{pattern.description}</p>

      {pattern.mo_summary && (
        <div className="pattern-card-mo">
          <span className="pattern-card-mo-label">MO:</span>
          <span className="pattern-card-mo-value">{pattern.mo_summary}</span>
        </div>
      )}

      <div className="pattern-card-footer">
        {pattern.time_pattern && <span className="pattern-card-tag">{pattern.time_pattern}</span>}
        {pattern.location_pattern && <span className="pattern-card-tag">{pattern.location_pattern}</span>}
        <ChevronRight size={14} className="pattern-card-arrow" />
      </div>
    </div>
  )
}
