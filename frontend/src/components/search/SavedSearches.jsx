import { Bookmark, Play, Trash2, BookmarkPlus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function SavedSearches({ searches, onRunSearch, onDelete, onSave, currentQuery }) {
  const { t } = useLanguage()
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <h3 className="sidebar-section-title">
          <Bookmark size={14} />
          {t('Saved Searches')}
        </h3>
        {currentQuery && (
          <button
            className="sidebar-save-btn"
            onClick={() => onSave(currentQuery)}
            aria-label={t('Save current search')}
          >
            <BookmarkPlus size={14} />
          </button>
        )}
      </div>
      <div className="saved-list">
        {searches.length === 0 ? (
          <p className="sidebar-empty">{t('No saved searches')}</p>
        ) : (
          searches.map((item) => (
            <div key={item.id} className="saved-item">
              <div className="saved-info">
                <span className="saved-name">{item.name}</span>
                <span className="saved-query">{item.query}</span>
              </div>
              <div className="saved-actions">
                <button
                  className="saved-action-btn"
                  onClick={() => onRunSearch(item.query, item.filters)}
                  aria-label={t('Run search')}
                >
                  <Play size={12} />
                </button>
                <button
                  className="saved-action-btn delete"
                  onClick={() => onDelete(item.id)}
                  aria-label={t('Delete')}
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
