import { Bookmark, FileText, Download, Share2, Printer, BarChart3, Clock, StickyNote } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function ToolsPanel({ investigation }) {
  const { lang } = useLanguage()

  if (!investigation) return null

  return (
    <div className="tools-panel">
      {/* Bookmarks */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <Bookmark size={14} />
          {t('bookmarks', lang)}
        </h3>
        <div className="tools-bookmarks">
          {investigation.bookmarked ? (
            <div className="bookmark-active">
              <Bookmark size={14} />
              <span>{t('bookmarked', lang)}</span>
            </div>
          ) : (
            <button className="bookmark-add">
              <Bookmark size={14} />
              {t('add_bookmark', lang)}
            </button>
          )}
        </div>
      </div>

      {/* Reports */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <FileText size={14} />
          {t('reports', lang)}
        </h3>
        <div className="tools-reports">
          <button className="tools-report-btn">
            <FileText size={14} />
            <span>{t('generate_report', lang)}</span>
          </button>
          <button className="tools-report-btn">
            <Download size={14} />
            <span>{t('export_pdf', lang)}</span>
          </button>
          <button className="tools-report-btn">
            <Printer size={14} />
            <span>{t('print', lang)}</span>
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="tools-section">
        <h3 className="tools-section-title">{t('quick_actions', lang)}</h3>
        <div className="tools-actions">
          <button className="tools-action-btn">
            <Share2 size={14} />
            {t('share_with_team', lang)}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <BarChart3 size={14} />
          {t('investigation_stats', lang)}
        </h3>
        <div className="tools-stats">
          <div className="tools-stat">
            <StickyNote size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.notes.length}</span>
              <span className="tools-stat-label">{t('notes', lang)}</span>
            </div>
          </div>
          <div className="tools-stat">
            <FileText size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.evidence.length}</span>
              <span className="tools-stat-label">{t('evidence', lang)}</span>
            </div>
          </div>
          <div className="tools-stat">
            <Clock size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.timeline.length}</span>
              <span className="tools-stat-label">{t('events', lang)}</span>
            </div>
          </div>
          <div className="tools-stat">
            <BarChart3 size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.progress}%</span>
              <span className="tools-stat-label">{t('progress', lang)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
