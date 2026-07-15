import { Bookmark, Play, Trash2 } from 'lucide-react'

const savedSearches = [
  { id: 1, query: 'Theft cases Bengaluru 2026', count: 24 },
  { id: 2, query: 'Unsolved fraud cases', count: 12 },
  { id: 3, query: 'Repeat offenders Koramangala', count: 8 },
  { id: 4, query: 'Cybercrime victims under 25', count: 15 },
]

export default function SavedSearches({ onRunSearch }) {
  return (
    <div className="sidebar-section">
      <h3 className="sidebar-section-title">
        <Bookmark size={14} />
        Saved Searches
      </h3>
      <div className="saved-list">
        {savedSearches.map((item) => (
          <div key={item.id} className="saved-item">
            <div className="saved-item-info">
              <span className="saved-item-query">{item.query}</span>
              <span className="saved-item-count">{item.count} results</span>
            </div>
            <div className="saved-item-actions">
              <button
                className="saved-action-btn"
                onClick={() => onRunSearch(item.query)}
                aria-label="Run search"
              >
                <Play size={12} />
              </button>
              <button className="saved-action-btn delete" aria-label="Delete">
                <Trash2 size={12} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
