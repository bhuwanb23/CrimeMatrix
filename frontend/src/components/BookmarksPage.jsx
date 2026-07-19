import { useState, useEffect } from 'react'
import { Bookmark, FileText, User, Clock, Camera } from 'lucide-react'
import { getGroupedBookmarks } from '../services/bookmarks'
import BookmarkCard from './bookmarks/BookmarkCard'

const filterTabs = [
  { id: 'all', label: 'All', icon: Bookmark },
  { id: 'case', label: 'Cases', icon: FileText },
  { id: 'evidence', label: 'Evidence', icon: Camera },
  { id: 'criminal', label: 'Criminals', icon: User },
  { id: 'investigation', label: 'Investigations', icon: Clock },
]

export default function BookmarksPage() {
  const [grouped, setGrouped] = useState({})
  const [loading, setLoading] = useState(true)
  const [activeFilter, setActiveFilter] = useState('all')

  useEffect(() => {
    loadBookmarks()
  }, [])

  async function loadBookmarks() {
    setLoading(true)
    try {
      const res = await getGroupedBookmarks()
      const data = res?.data || res
      setGrouped(data || {})
    } catch (e) {
      console.error('Failed to load bookmarks', e)
    } finally {
      setLoading(false)
    }
  }

  function getFilteredItems() {
    if (activeFilter === 'all') {
      return Object.entries(grouped).flatMap(([type, items]) => items)
    }
    return grouped[activeFilter] || []
  }

  function getCount(type) {
    if (type === 'all') {
      return Object.values(grouped).reduce((sum, items) => sum + items.length, 0)
    }
    return (grouped[type] || []).length
  }

  const items = getFilteredItems()

  return (
    <div className="bookmarks-page">
      <div className="bookmarks-header">
        <div className="bookmarks-title">
          <Bookmark size={20} />
          <h1>Bookmarks</h1>
          <span className="similar-count">{getCount('all')}</span>
        </div>
      </div>

      <div className="bookmarks-filters">
        {filterTabs.map((tab) => (
          <button
            key={tab.id}
            className={`bookmarks-filter-btn ${activeFilter === tab.id ? 'active' : ''}`}
            onClick={() => setActiveFilter(tab.id)}
          >
            <tab.icon size={14} />
            {tab.label}
            <span className="bookmarks-filter-count">{getCount(tab.id)}</span>
          </button>
        ))}
      </div>

      <div className="bookmarks-content">
        {loading ? (
          <div className="similar-loading">
            <div className="similar-spinner" />
            <span>Loading bookmarks...</span>
          </div>
        ) : items.length === 0 ? (
          <div className="similar-empty">
            <Bookmark size={32} className="similar-empty-icon" />
            <p>No bookmarks yet</p>
            <span>Bookmark cases, evidence, criminals, and investigations to find them here.</span>
          </div>
        ) : (
          <div className="bookmarks-list">
            {items.map((bookmark) => (
              <BookmarkCard
                key={bookmark.id}
                bookmark={bookmark}
                onRemoved={(id) => {
                  setGrouped((prev) => {
                    const next = { ...prev }
                    for (const key of Object.keys(next)) {
                      next[key] = next[key].filter((b) => b.id !== id)
                    }
                    return next
                  })
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
