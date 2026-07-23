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
        <button className="graph-zoom-btn" onClick={onZoomIn} aria-label={t("Zoom in")}>
          <ZoomIn size={16} />
        </button>
        <button className="graph-zoom-btn" onClick={onZoomOut} aria-label={t("Zoom out")}>
          <ZoomOut size={16} />
        </button>
        <button className="graph-zoom-btn" onClick={onReset} aria-label={t("Reset view")}>
          <Maximize2 size={16} />
        </button>
      </div>
    </div>
  )
}

