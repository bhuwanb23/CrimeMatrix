import { useState, useEffect } from 'react'
import { Bookmark } from 'lucide-react'
import { toggleBookmark, checkBookmark } from '../../services/bookmarks'
import { useLanguage } from '../../context/LanguageContext'

export default function BookmarkButton({ entityType, entityId, onToggle, size = 16 }) {
  const { t } = useLanguage()
  const [bookmarked, setBookmarked] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function checkStatus() {
      try {
        const res = await checkBookmark(entityType, entityId)
        const data = res?.data || res
        setBookmarked(data?.bookmarked || false)
      } catch {
        setBookmarked(false)
      }
    }
    checkStatus()
  }, [entityType, entityId])

  async function handleToggle(e) {
    e.stopPropagation()
    if (loading) return
    setLoading(true)
    try {
      const res = await toggleBookmark(entityType, entityId)
      const data = res?.data || res
      setBookmarked(data?.bookmarked || false)
      onToggle?.(data?.bookmarked)
    } catch (err) {
      console.error('Bookmark toggle failed', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      className={`bookmark-btn ${bookmarked ? 'bookmark-btn-active' : ''}`}
      onClick={handleToggle}
      disabled={loading}
      title={bookmarked ? t('Remove bookmark') : t('Add bookmark')}
    >
      <Bookmark size={size} fill={bookmarked ? 'currentColor' : 'none'} />
    </button>
  )
}

