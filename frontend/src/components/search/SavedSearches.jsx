import { Bookmark, Play, Trash2, BookmarkPlus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function SavedSearches({ searches, onRunSearch, onDelete, onSave, currentQuery }) {
  const { lang } = useLanguage()
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <h3 className="sidebar-section-title">
          <Bookmark size={14} />
          {t('saved_searches', lang)}
        </h3>
        {currentQuery && (
          <button
            className="sidebar-save-btn"
            onClick={() => onSave(currentQuery)}
            aria-label={t('save_current_search', lang)}
          >
            <BookmarkPlus size={14} />
          </button>
        )}
      </div>
      <div className="saved-list">
        {searches.length === 0 ? (
          <p className="sidebar-empty">{t('no_saved_searches', lang)}</p>
        ) : (
          searches.map((item) => (
            <div key={item.id} className="saved-item">
              <button
                className="saved-item-info"
                onClick={() => onRunSearch(item.query)}
              >
                <span className="saved-item-query">{item.query}</span>
                <span className="saved-item-count">{item.count} {t('results', lang)}</span>
              </button>
              <div className="saved-item-actions">
                <button
                  className="saved-action-btn"
                  onClick={() => onRunSearch(item.query)}
                  aria-label={t('run_search', lang)}
                >
                  <Play size={12} />
                </button>
                <button
                  className="saved-action-btn delete"
                  onClick={() => onDelete(item.id)}
                  aria-label={t('delete', lang)}
                >
                  <Trash2 size={12} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
