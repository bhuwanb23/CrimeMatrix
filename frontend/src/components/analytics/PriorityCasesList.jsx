import { ClipboardList } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


const priorityColors = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#10b981',
}

export default function PriorityCasesList({ cases }) {
  const { t } = useLanguage()
  if (!cases || cases.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <ClipboardList size={14} />
          <h3>{t(t('Priority Cases'))}</h3>
        </div>
        <div className="similar-empty"><p>No priority cases</p></div>
      </div>
    )
  }

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <ClipboardList size={14} />
        <h3>{t(t('Priority Cases'))}</h3>
        <span className="similar-count">{cases.length}</span>
      </div>
      <div className="analytics-priority-list">
        {cases.map((c, i) => {
          const color = priorityColors[c.priority] || '#64748b'
          return (
            <div key={c.id || i} className="analytics-priority-item">
              <div className="analytics-priority-header">
                <span className="analytics-priority-title">{c.title}</span>
                <span className="analytics-priority-badge" style={{ color }}>{c.priority}</span>
              </div>
              <div className="analytics-priority-meta">
                <span>{c.district || 'N/A'}</span>
                <span>Progress: {c.progress || 0}%</span>
              </div>
              <div className="analytics-priority-bar">
                <div className="analytics-priority-fill" style={{ width: `${c.progress || 0}%`, background: color }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
