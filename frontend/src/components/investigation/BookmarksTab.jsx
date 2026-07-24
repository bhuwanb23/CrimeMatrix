import { useLanguage } from '../../context/LanguageContext'
import { Clock, User } from 'lucide-react'

export default function BookmarksTab({ investigationId: _investigationId, bookmarks }) {
  const { t } = useLanguage()
  if (!bookmarks || bookmarks.length === 0) {
    return (
      <div className="similar-empty">
        <p>{t('No status logs yet')}</p>
      </div>
    )
  }

  function formatDate(dateStr) {
    if (!dateStr) return ''
    try {
      return new Date(dateStr).toLocaleDateString('en-IN', {
        month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
      })
    } catch {
      return dateStr
    }
  }

  return (
    <div className="bookmarks-tab">
      <div className="status-logs-list">
        {bookmarks.map((log) => (
          <div key={log.id} className="status-log-card">
            <div className="status-log-header">
              <div className="status-log-statuses">
                {log.old_status && (
                  <span className={`status-badge ${log.old_status}`}>{log.old_status}</span>
                )}
                {log.old_status && <span className="status-log-arrow">→</span>}
                <span className={`status-badge ${log.new_status}`}>{log.new_status}</span>
              </div>
              <span className="status-log-time">
                <Clock size={12} />
                {formatDate(log.changed_at)}
              </span>
            </div>
            {log.notes && <p className="status-log-notes">{log.notes}</p>}
            {log.changed_by && (
              <span className="status-log-author">
                <User size={12} />
                Officer #{log.changed_by}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
