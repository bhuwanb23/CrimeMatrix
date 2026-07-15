import { ZoomIn, ZoomOut, Maximize2, Filter } from 'lucide-react'

const views = [
  { id: 'all', label: 'All Connections' },
  { id: 'criminal', label: 'Criminal Network' },
  { id: 'gang', label: 'Gang Network' },
  { id: 'evidence', label: 'Evidence Links' },
]

export default function GraphControls({ activeView, onViewChange, onZoomIn, onZoomOut, onReset }) {
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
