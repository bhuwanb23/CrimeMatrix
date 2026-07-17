import { Clock, Play } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function SearchHistory({ history, onRunSearch }) {
  const { lang } = useLanguage()
  return (
    <div className="sidebar-section">
      <h3 className="sidebar-section-title">
        <Clock size={14} />
        {t('search_history', lang)}
      </h3>
      <div className="history-list">
        {history.length === 0 ? (
          <p className="sidebar-empty">{t('no_search_history', lang)}</p>
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
