import { Layers } from 'lucide-react'

const layers = [
  { id: 'crimes', label: 'Crimes', color: 'var(--color-accent)' },
  { id: 'hotspots', label: 'Hotspots', color: '#ef4444' },
  { id: 'stations', label: 'Stations', color: '#3b82f6' },
  { id: 'routes', label: 'Routes', color: '#8b5cf6' },
  { id: 'density', label: 'Density', color: '#10b981' },
]

export default function MapLayerControls({ activeLayers, onToggleLayer }) {
  return (
    <div className="map-layer-controls">
      <span className="map-control-label">
        <Layers size={13} aria-hidden="true" />
        Layers
      </span>
      <div className="map-chip-row" role="group" aria-label="Map layers">
        {layers.map((layer) => {
          const isActive = activeLayers.includes(layer.id)
          return (
            <button
              key={layer.id}
              type="button"
              className={`map-chip ${isActive ? 'active' : ''}`}
              onClick={() => onToggleLayer(layer.id)}
              aria-pressed={isActive}
              style={isActive ? { '--chip-accent': layer.color } : undefined}
            >
              <span
                className="map-chip-dot"
                style={{ background: layer.color }}
                aria-hidden="true"
              />
              {layer.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}
