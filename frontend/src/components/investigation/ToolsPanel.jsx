import { useState } from 'react'
import { Bookmark, FileText, Download, Share2, Printer, BarChart3, Clock, StickyNote, Save, Play } from 'lucide-react'
import { toggleSaveInvestigation } from '../../services/investigations'

export default function ToolsPanel({ investigation, onRefresh }) {
  const [toggling, setToggling] = useState(false)

  if (!investigation) return null

  const isSaved = investigation.status === 'saved'

  const handleToggleSave = async () => {
    if (toggling) return
    setToggling(true)
    try {
      await toggleSaveInvestigation(investigation.id)
      onRefresh?.(investigation.id)
    } catch (e) {
      console.error('Failed to toggle save', e)
    } finally {
      setToggling(false)
    }
  }

  return (
    <div className="tools-panel">
      {/* Save/Resume */}
      <div className="tools-section">
        <h3 className="tools-section-title">
          {isSaved ? <Play size={14} /> : <Save size={14} />}
          {isSaved ? 'Resume' : 'Save'}
        </h3>
        <div className="tools-bookmarks">
          <button
            className={`tools-save-btn ${isSaved ? 'tools-save-resume' : 'tools-save-active'}`}
            onClick={handleToggleSave}
            disabled={toggling}
          >
            {isSaved ? <Play size={14} /> : <Save size={14} />}
            <span>{toggling ? 'Updating...' : (isSaved ? 'Resume Investigation' : 'Save Investigation')}</span>
          </button>
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
              <span className="tools-stat-value">{investigation.notes?.length || 0}</span>
              <span className="tools-stat-label">Notes</span>
            </div>
          </div>
          <div className="tools-stat">
            <FileText size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.evidence?.length || 0}</span>
              <span className="tools-stat-label">Evidence</span>
            </div>
          </div>
          <div className="tools-stat">
            <Clock size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.timeline?.length || 0}</span>
              <span className="tools-stat-label">Events</span>
            </div>
          </div>
          <div className="tools-stat">
            <BarChart3 size={14} />
            <div className="tools-stat-info">
              <span className="tools-stat-value">{investigation.progress || 0}%</span>
              <span className="tools-stat-label">Progress</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
