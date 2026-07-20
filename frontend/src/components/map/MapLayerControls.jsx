import { Layers, MapPin, Shield, Radio, Route, BarChart3 } from 'lucide-react'

const layers = [
  { id: 'crimes', label: 'Crimes', icon: MapPin, color: '#f59e0b' },
  { id: 'hotspots', label: 'Hotspots', icon: Shield, color: '#ef4444' },
  { id: 'stations', label: 'Stations', icon: Radio, color: '#3b82f6' },
  { id: 'routes', label: 'Routes', icon: Route, color: '#8b5cf6' },
  { id: 'density', label: 'Density', icon: BarChart3, color: '#10b981' },
]

export default function MapLayerControls({ activeLayers, onToggleLayer }) {
  return (
    <div className="map-layer-controls">
      <div className="map-layer-header">
        <Layers size={14} />
        <span>Layers</span>
      </div>
      {layers.map((layer) => {
        const Icon = layer.icon
        const isActive = activeLayers.includes(layer.id)
        return (
          <button
            key={layer.id}
            className={`map-layer-btn ${isActive ? 'active' : ''}`}
            onClick={() => onToggleLayer(layer.id)}
            style={isActive ? { borderColor: layer.color, color: layer.color } : {}}
          >
            <Icon size={14} />
            <span>{layer.label}</span>
          </button>
        )
      })}
    </div>
  )
}
