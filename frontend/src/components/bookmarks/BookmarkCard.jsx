import { useNavigate } from 'react-router-dom'
import { FileText, User, Clock, Camera, ExternalLink, Trash2 } from 'lucide-react'
import { removeBookmark } from '../../services/bookmarks'

const entityConfig = {
  case: { icon: FileText, label: 'Case', color: '#f59e0b', route: '/cases' },
  evidence: { icon: Camera, label: 'Evidence', color: '#3b82f6', route: '/cases' },
  criminal: { icon: User, label: 'Criminal', color: '#ef4444', route: '/suspects' },
  investigation: { icon: Clock, label: 'Investigation', color: '#8b5cf6', route: '/investigations' },
  search_result: { icon: FileText, label: 'Search Result', color: '#10b981', route: '/cases' },
}

export default function BookmarkCard({ bookmark, onRemoved }) {
  const navigate = useNavigate()
  const config = entityConfig[bookmark.entity_type] || entityConfig.case
  const Icon = config.icon

  function formatDate(dateStr) {
    if (!dateStr) return ''
    try {
      return new Date(dateStr).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
    } catch {
      return dateStr
    }
  }

  async function handleRemove(e) {
    e.stopPropagation()
    try {
      await removeBookmark(bookmark.id)
      onRemoved?.(bookmark.id)
    } catch (err) {
      console.error('Failed to remove bookmark', err)
    }
  }

  function handleClick() {
    if (bookmark.entity_type === 'case') {
      navigate(`/cases/${bookmark.entity_id}`)
    } else if (bookmark.entity_type === 'criminal') {
      navigate(`/suspects/${bookmark.entity_id}`)
    } else if (bookmark.entity_type === 'investigation') {
      navigate('/investigations')
    } else {
      navigate(config.route)
    }
  }

  return (
    <div className="bookmark-card" onClick={handleClick}>
      <div className="bookmark-card-icon" style={{ color: config.color }}>
        <Icon size={16} />
      </div>
      <div className="bookmark-card-info">
        <div className="bookmark-card-header">
          <span className="bookmark-card-type" style={{ color: config.color }}>{config.label}</span>
          <span className="bookmark-card-id">#{bookmark.entity_id}</span>
        </div>
        {bookmark.bookmark_note && (
          <p className="bookmark-card-note">{bookmark.bookmark_note}</p>
        )}
        <span className="bookmark-card-date">{formatDate(bookmark.created_at)}</span>
      </div>
      <div className="bookmark-card-actions">
        <button className="bookmark-card-go" onClick={(e) => { e.stopPropagation(); handleClick() }}>
          <ExternalLink size={12} />
        </button>
        <button className="bookmark-card-remove" onClick={handleRemove}>
          <Trash2 size={12} />
        </button>
      </div>
    </div>
  )
}
