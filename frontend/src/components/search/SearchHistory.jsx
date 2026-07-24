import { Clock, Play } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function SearchHistory({ history, onRunSearch }) {
  const { t } = useLanguage()
  return (
    <div className="sidebar-section">
      <h3 className="sidebar-section-title">
        <Clock size={14} />
        Search History
      </h3>
      <div className="history-list">
        {history.length === 0 ? (
          <p className="sidebar-empty">{t('No search history')}</p>
        ) : (
          history.map((item) => (
            <button
              key={item.id}
              className="history-item"
              onClick={() => onRunSearch(item.query)}
            >
              <div className="history-item-info">
                <span className="history-item-query">{item.query}</span>
                <span className="history-item-time">{item.time}</span>
              </div>
              <Play size={12} className="history-item-run" />
            </button>
          ))
        )}
      </div>
    </div>
  )
}
