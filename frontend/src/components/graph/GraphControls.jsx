import { ZoomIn, ZoomOut, Maximize2, Filter } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function GraphControls({ activeView, onViewChange, onZoomIn, onZoomOut, onReset, typeFilter = [], onToggleType }) {
  const { t } = useLanguage()

  const views = [
    { id: 'all', label: t('All Connections') },
    { id: 'criminal', label: t('Criminal Network') },
    { id: 'gang', label: t('Gang Network') },
    { id: 'evidence', label: t('Evidence Links') },
  ]

  const nodeTypes = [
    { id: 'suspect', label: t('Suspects'), color: '#ef4444' },
    { id: 'criminal', label: t('Criminals'), color: '#f59e0b' },
    { id: 'evidence', label: t('Evidence'), color: '#3b82f6' },
    { id: 'vehicle', label: t('Vehicles'), color: '#8b5cf6' },
    { id: 'phone', label: t('Phones'), color: '#10b981' },
  ]

  return (
    <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
      {/* View Buttons */}
      <div className="flex items-center gap-1.5 flex-wrap" role="group" aria-label="Graph views">
        {views.map((view) => (
          <button
            key={view.id}
            type="button"
            onClick={() => onViewChange(view.id)}
            className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap cursor-pointer transition-colors focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2 ${
              activeView === view.id
                ? 'bg-white text-slate-900 border-slate-300'
                : 'bg-slate-50 border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-800'
            }`}
          >
            {view.label}
          </button>
        ))}
      </div>

      {/* Divider */}
      <div className="w-px h-6 bg-slate-200 shrink-0 max-lg:hidden" aria-hidden="true" />

      {/* Type Filters */}
      {onToggleType && (
        <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
          <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 whitespace-nowrap">
            <Filter size={13} aria-hidden="true" />
            {t('Filter')}
          </span>
          <div className="flex items-center gap-1.5 flex-wrap" role="group" aria-label="Node type filters">
            {nodeTypes.map((nt) => {
              const isActive = typeFilter.includes(nt.id)
              return (
                <button
                  key={nt.id}
                  type="button"
                  onClick={() => onToggleType(nt.id)}
                  aria-pressed={isActive}
                  className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap cursor-pointer transition-colors focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2 ${
                    isActive
                      ? 'bg-white text-slate-900'
                      : 'bg-slate-50 border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-800'
                  }`}
                  style={isActive ? { borderColor: nt.color } : undefined}
                >
                  <span className="size-1.5 rounded-full shrink-0" style={{ background: nt.color }} aria-hidden="true" />
                  {nt.label}
                </button>
              )
            })}
          </div>
        </div>
      )}

      {/* Divider */}
      <div className="w-px h-6 bg-slate-200 shrink-0 max-lg:hidden" aria-hidden="true" />

      {/* Zoom Controls */}
      <div className="flex items-center gap-1.5 shrink-0">
        <button type="button" onClick={onZoomIn} aria-label={t("Zoom in")}
          className="inline-flex size-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-500 cursor-pointer transition-colors hover:border-slate-300 hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2">
          <ZoomIn size={16} />
        </button>
        <button type="button" onClick={onZoomOut} aria-label={t("Zoom out")}
          className="inline-flex size-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-500 cursor-pointer transition-colors hover:border-slate-300 hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2">
          <ZoomOut size={16} />
        </button>
        <button type="button" onClick={onReset} aria-label={t("Reset view")}
          className="inline-flex size-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-500 cursor-pointer transition-colors hover:border-slate-300 hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2">
          <Maximize2 size={16} />
        </button>
      </div>
    </div>
  )
}
