import { MapPin, X, TrendingUp, AlertTriangle } from 'lucide-react'

const riskBadgeClass = {
  critical: 'bg-red-500/10 text-red-500',
  high: 'bg-red-500/10 text-red-500',
  medium: 'bg-amber-500/10 text-amber-500',
  low: 'bg-emerald-500/10 text-emerald-500',
}

const hotspotDotClass = {
  critical: 'bg-red-500',
  high: 'bg-amber-500',
  medium: 'bg-blue-500',
  low: 'bg-emerald-500',
}

const DENSITY_COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6']

function buildDensity(mapData, stats) {
  if (stats?.district_density && Array.isArray(stats.district_density)) {
    return stats.district_density.map((d, i) => ({
      label: d.name || d.district || `District ${i + 1}`,
      count: d.count ?? d.crime_count ?? 0,
      color: d.color || DENSITY_COLORS[i % DENSITY_COLORS.length],
    }))
  }
  const features = mapData?.districts?.features || []
  if (features.length) {
    return features.slice(0, 8).map((f, i) => {
      const props = f.properties || {}
      return {
        label: props.name || props.district || `District ${i + 1}`,
        count: props.crime_count ?? props.cases ?? props.count ?? 0,
        color: DENSITY_COLORS[i % DENSITY_COLORS.length],
      }
    })
  }
  return []
}

function buildHotspots(mapData) {
  const features = mapData?.hotspots?.features || []
  if (features.length) {
    return features.slice(0, 5).map((f) => {
      const props = f.properties || {}
      return {
        name: props.name || props.label || 'Hotspot',
        cases: props.cases ?? props.crime_count ?? props.count ?? 0,
        severity: (props.severity || props.risk || props.risk_level || 'medium').toLowerCase(),
      }
    })
  }
  const points = mapData?.heatmap?.points || []
  return points.slice(0, 5).map((p, i) => ({
    name: p.name || p.label || `Cluster ${i + 1}`,
    cases: p.weight ?? p.count ?? 0,
    severity: (p.severity || 'medium').toLowerCase(),
  }))
}

export default function DistrictPanel({ selectedDistrict, onClose, mapData = null, stats = null }) {
  const risk = selectedDistrict?.risk || selectedDistrict?.risk_level || 'low'
  const density = buildDensity(mapData, stats)
  const hotspots = buildHotspots(mapData)

  return (
    <aside
      className="flex w-[280px] shrink-0 flex-col overflow-hidden rounded-xl border border-slate-200 bg-white max-lg:order-2 max-lg:w-full max-lg:max-h-60 max-md:max-h-[280px]"
      aria-label="District details"
    >
      <div className="flex items-center justify-between gap-2 border-b border-slate-200 px-3.5 py-3">
        <h2 className="m-0 min-w-0 text-[13px] font-semibold text-slate-900 [overflow-wrap:anywhere]">
          {selectedDistrict ? selectedDistrict.name : 'Overview'}
        </h2>
        {selectedDistrict && (
          <button
            type="button"
            onClick={onClose}
            aria-label="Close district details"
            className="inline-flex size-7 shrink-0 items-center justify-center rounded-md border-0 bg-transparent text-slate-400 cursor-pointer hover:bg-slate-50 hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2"
          >
            <X size={16} />
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto">
        {selectedDistrict ? (
          <div className="border-b border-slate-200 p-3.5">
            <div className="mb-3 flex items-center gap-1.5 text-[11px] font-medium text-slate-400">
              <MapPin size={15} className="text-amber-500" aria-hidden="true" />
              <span>Selected district</span>
            </div>
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-slate-400">Total cases</span>
                <span className="text-[13px] font-semibold text-slate-900">
                  {selectedDistrict.cases ?? selectedDistrict.crime_count ?? '—'}
                </span>
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-slate-400">Hotspots</span>
                <span className="text-[13px] font-semibold text-slate-900">
                  {selectedDistrict.hotspots ?? '—'}
                </span>
              </div>
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-slate-400">Risk</span>
                <span className={`rounded-lg px-2 py-0.5 text-[10px] font-semibold capitalize ${riskBadgeClass[risk] || riskBadgeClass.low}`}>
                  {selectedDistrict.risk || selectedDistrict.risk_level || '—'}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center gap-2 border-b border-slate-200 px-4 py-7 text-center text-slate-400">
            <MapPin size={20} aria-hidden="true" />
            <p className="m-0 max-w-[16ch] text-xs leading-snug">
              Select a district on the map
            </p>
          </div>
        )}

        <section className="border-b border-slate-200 p-3.5">
          <h3 className="mb-2.5 mt-0 flex items-center gap-1.5 text-[11px] font-semibold text-slate-400">
            <TrendingUp size={13} aria-hidden="true" />
            Density
          </h3>
          <div className="flex flex-col gap-2">
            {density.length === 0 ? (
              <p className="m-0 text-xs text-slate-400">No density data from API</p>
            ) : density.map((d, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-slate-500">
                <span className="size-2 shrink-0 rounded-full" style={{ background: d.color }} />
                <span className="min-w-0 flex-1 text-slate-900">{d.label}</span>
                <span className="whitespace-nowrap text-[11px] text-slate-400">{d.count}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="p-3.5">
          <h3 className="mb-2.5 mt-0 flex items-center gap-1.5 text-[11px] font-semibold text-slate-400">
            <AlertTriangle size={13} aria-hidden="true" />
            Hotspots
          </h3>
          <div className="flex flex-col gap-2">
            {hotspots.length === 0 ? (
              <p className="m-0 text-xs text-slate-400">No hotspot data from API</p>
            ) : hotspots.map((h, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-slate-500">
                <span className={`size-2 shrink-0 rounded-full ${hotspotDotClass[h.severity] || 'bg-slate-400'}`} />
                <div className="flex min-w-0 flex-col gap-px">
                  <span className="text-slate-900">{h.name}</span>
                  <span className="whitespace-nowrap text-[11px] text-slate-400">{h.cases} cases</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </aside>
  )
}
