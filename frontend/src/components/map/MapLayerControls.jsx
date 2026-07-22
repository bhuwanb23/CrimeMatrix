import { Layers } from 'lucide-react'

const layers = [
  { id: 'crimes', label: 'Crimes', color: '#f59e0b' },
  { id: 'hotspots', label: 'Hotspots', color: '#ef4444' },
  { id: 'stations', label: 'Stations', color: '#3b82f6' },
  { id: 'routes', label: 'Routes', color: '#8b5cf6' },
  { id: 'density', label: 'Density', color: '#10b981' },
]

export default function MapLayerControls({ activeLayers, onToggleLayer }) {
  return (
    <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
      <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 whitespace-nowrap">
        <Layers size={13} aria-hidden="true" />
        Layers
      </span>
      <div className="flex items-center gap-1.5 flex-wrap" role="group" aria-label="Map layers">
        {layers.map((layer) => {
          const isActive = activeLayers.includes(layer.id)
          return (
            <button
              key={layer.id}
              type="button"
              onClick={() => onToggleLayer(layer.id)}
              aria-pressed={isActive}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap cursor-pointer transition-colors focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2 ${
                isActive
                  ? 'bg-white text-slate-900'
                  : 'bg-slate-50 border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-800'
              }`}
              style={isActive ? { borderColor: layer.color } : undefined}
            >
              <span
                className="size-1.5 rounded-full shrink-0"
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
