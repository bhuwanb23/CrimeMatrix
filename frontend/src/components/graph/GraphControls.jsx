import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

const views = [
  { id: 'all', labelKey: 'all_connections' },
  { id: 'criminal', labelKey: 'criminal_network' },
  { id: 'gang', labelKey: 'gang_network' },
  { id: 'evidence', labelKey: 'evidence_links' },
]

export default function GraphControls({ activeView, onViewChange, onZoomIn, onZoomOut, onReset }) {
  const { lang } = useLanguage()

  return (
    <div className="graph-controls">
      <div className="graph-view-btns">
        {views.map((view) => (
          <button
            key={view.id}
            className={`graph-view-btn ${activeView === view.id ? 'active' : ''}`}
            onClick={() => onViewChange(view.id)}
          >
            {t(view.labelKey, lang)}
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
