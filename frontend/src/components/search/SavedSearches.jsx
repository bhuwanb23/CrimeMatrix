import { Bookmark, Play, Trash2, BookmarkPlus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function SavedSearches({ searches, onRunSearch, onDelete, onSave, currentQuery }) {
  const { t } = useLanguage()
  return (
    <div className="sidebar-section">
          <p className="sidebar-empty">{t('{t('No saved searches')}')}</p>
        ) : (
          searches.map((item) => (
            <div key={item.id} className="saved-item">
              <button
                className="saved-item-info"
                onClick={() => onRunSearch(item.query)}
              >
                <span className="saved-item-query">{item.query}</span>
                <span className="saved-item-count">{item.count} results</span>
              </button>
              <div className="saved-item-actions">
                <button
                  className="saved-action-btn"
                  onClick={() => onRunSearch(item.query)}
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
