import { Bookmark, Play, Trash2, BookmarkPlus } from 'lucide-react'

export default function SavedSearches({ searches, onRunSearch, onDelete, onSave, currentQuery }) {
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <h3 className="sidebar-section-title">
          <Bookmark size={14} />
          Saved Searches
        </h3>
        {currentQuery && (
          <button
            className="sidebar-save-btn"
            onClick={() => onSave(currentQuery)}
            aria-label="Save current search"
          >
            <BookmarkPlus size={14} />
          </button>
        )}
      </div>
      <div className="saved-list">
        {searches.length === 0 ? (
          <p className="sidebar-empty">No saved searches</p>
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
                  aria-label="Run search"
                >
                  <Play size={12} />
                </button>
                <button
                  className="saved-action-btn delete"
                  onClick={() => onDelete(item.id)}
                  aria-label="Delete"
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
