import { ZoomIn, ZoomOut, Maximize2, Filter } from 'lucide-react'

const views = [
  { id: 'all', label: 'All Connections' },
  { id: 'criminal', label: 'Criminal Network' },
  { id: 'gang', label: 'Gang Network' },
  { id: 'evidence', label: 'Evidence Links' },
]

const nodeTypes = [
  { id: 'suspect', label: 'Suspects', color: '#ef4444' },
  { id: 'criminal', label: 'Criminals', color: '#f59e0b' },
  { id: 'evidence', label: 'Evidence', color: '#3b82f6' },
  { id: 'vehicle', label: 'Vehicles', color: '#8b5cf6' },
  { id: 'phone', label: 'Phones', color: '#10b981' },
]

export default function GraphControls({ activeView, onViewChange, onZoomIn, onZoomOut, onReset, typeFilter = [], onToggleType }) {
  return (
    <div className="graph-controls">
      <div className="graph-view-btns">
        {views.map((view) => (
          <button
            key={view.id}
            className={`graph-view-btn ${activeView === view.id ? 'active' : ''}`}
            onClick={() => onViewChange(view.id)}
          >
            {view.label}
          </button>
        ))}
      </div>

      {onToggleType && (
        <div className="graph-type-filters">
          <Filter size={12} />
          {nodeTypes.map((nt) => (
            <button
              key={nt.id}
              className={`graph-type-btn ${typeFilter.includes(nt.id) ? 'active' : ''}`}
              onClick={() => onToggleType(nt.id)}
              style={typeFilter.includes(nt.id) ? { borderColor: nt.color, color: nt.color } : {}}
            >
              <span className="graph-type-dot" style={{ background: nt.color }} />
              {nt.label}
            </button>
          ))}
        </div>
      )}

      <div className="graph-zoom-btns">
        <button className="graph-zoom-btn" onClick={onZoomIn} aria-label="Zoom in">
          <ZoomIn size={16} />
        </button>
        <button className="graph-zoom-btn" onClick={onZoomOut} aria-label="Zoom out">
          <ZoomOut size={16} />
        </button>
        <button className="graph-zoom-btn" onClick={onReset} aria-label="Reset view">
          <Maximize2 size={16} />
        </button>
      </div>
    </div>
  )
}
