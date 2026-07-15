import { Bookmark, FileText, Download, Share2, Printer, BarChart3, Clock, StickyNote } from 'lucide-react'

export default function ToolsPanel({ investigation }) {
  if (!investigation) return null

  return (
    <div className="tools-panel">
      {/* Bookmarks */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <Bookmark size={14} />
          Bookmarks
        </h3>
        <div className="tools-bookmarks">
          {investigation.bookmarked ? (
            <div className="bookmark-active">
              <Bookmark size={14} />
              <span>Bookmarked</span>
            </div>
          ) : (
            <button className="bookmark-add">
              <Bookmark size={14} />
              Add Bookmark
            </button>
          )}
        </div>
      </div>

      {/* Reports */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <FileText size={14} />
          Reports
        </h3>
        <div className="tools-reports">
          <button className="tools-report-btn">
            <FileText size={14} />
            <span>Generate Report</span>
          </button>
          <button className="tools-report-btn">
            <Download size={14} />
            <span>Export PDF</span>
          </button>
          <button className="tools-report-btn">
            <Printer size={14} />
            <span>Print</span>
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="tools-section">
        <h3 className="tools-section-title">Quick Actions</h3>
        <div className="tools-actions">
          <button className="tools-action-btn">
            <Share2 size={14} />
            Share with Team
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          <BarChart3 size={14} />
          Investigation Stats
        </h3>
        <div className="tools-stats">
          <div className="tools-stat">
            <StickyNote size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.notes.length}</span>
              <span className="tools-stat-label">Notes</span>
            </div>
          </div>
          <div className="tools-stat">
            <FileText size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.evidence.length}</span>
              <span className="tools-stat-label">Evidence</span>
            </div>
          </div>
          <div className="tools-stat">
            <Clock size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.timeline.length}</span>
              <span className="tools-stat-label">Events</span>
            </div>
          </div>
          <div className="tools-stat">
            <BarChart3 size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.progress}%</span>
              <span className="tools-stat-label">Progress</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
