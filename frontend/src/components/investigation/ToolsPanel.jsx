import { useState, useEffect, useCallback } from 'react'
import { FileText, Download, Printer, BarChart3, Clock, StickyNote, Save, Play, Zap, AlertTriangle } from 'lucide-react'
import { toggleSaveInvestigation } from '../../services/investigations'
import { scoreInvestigation, getPriorityExplain } from '../../services/priorities'

const priorityColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }

export default function ToolsPanel({ investigation, onRefresh }) {
  const [toggling, setToggling] = useState(false)
  const [priority, setPriority] = useState(null)
  const [explanations, setExplanations] = useState([])
  const [scoringPriority, setScoringPriority] = useState(false)

  const loadPriority = useCallback(async () => {
    if (!investigation?.id) return
    try {
      const [priRes, rankRes] = await Promise.all([
        getPriorityExplain(investigation.id),
        fetch(`${window.location.origin}/api/v1/priorities/rankings?limit=50`).then(r => r.json()),
      ])
      setExplanations(priRes?.data?.items || [])
      const found = (rankRes?.data || []).find(r => r.investigation_id === investigation.id)
      if (found) setPriority(found)
    } catch { /* ignore */ }
  }, [investigation?.id])

  useEffect(() => {
    loadPriority()
  }, [loadPriority])

  async function handleScorePriority() {
    setScoringPriority(true)
    try { await scoreInvestigation(investigation.id); await loadPriority() } catch (e) { console.error(e) } finally { setScoringPriority(false) }
  }

  if (!investigation) return null

  const isSaved = investigation.status === 'saved'

  const handleToggleSave = async () => {
    if (toggling) return
    setToggling(true)
    try { await toggleSaveInvestigation(investigation.id); onRefresh?.(investigation.id) } catch (e) { console.error(e) } finally { setToggling(false) }
  }

  return (
    <div className="tools-panel">
      {/* Save/Resume */}
      <div className="tools-section">
        <h3 className="tools-section-title">{isSaved ? <Play size={14} /> : <Save size={14} />} {isSaved ? 'Resume' : 'Save'}</h3>
        <button className={`tools-save-btn ${isSaved ? 'tools-save-resume' : 'tools-save-active'}`} onClick={handleToggleSave} disabled={toggling}>
          {isSaved ? <Play size={14} /> : <Save size={14} />}
          <span>{toggling ? 'Updating...' : (isSaved ? 'Resume Investigation' : 'Save Investigation')}</span>
        </button>
      </div>

      {/* Priority Score */}
      <div className="tools-section">
        <div className="flex items-center justify-between mb-2">
          <h3 className="tools-section-title"><Zap size={14} /> Priority Score</h3>
          <button onClick={handleScorePriority} disabled={scoringPriority} className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
            {scoringPriority ? 'Scoring...' : 'Score'}
          </button>
        </div>
        {priority ? (
          <div className="p-2 bg-slate-50 rounded-lg">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg font-bold" style={{ color: priorityColors[priority.priority_level] }}>{priority.overall_score}%</span>
              <span className="text-[10px] font-semibold uppercase" style={{ color: priorityColors[priority.priority_level] }}>{priority.priority_level}</span>
            </div>
            {explanations.length > 0 && (
              <div className="mt-1.5 space-y-1">
                {explanations.slice(0, 3).map((exp, i) => (
                  <div key={i} className="flex items-start gap-1 text-[10px] text-slate-600">
                    <AlertTriangle size={9} className="text-amber-500 mt-0.5 flex-shrink-0" />
                    <span>{exp.factor}: {exp.score}%</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <p className="text-[10px] text-slate-400">Click Score to analyze priority</p>
        )}
      </div>

      {/* Reports */}
      <div className="tools-section">
        <h3 className="tools-section-title"><FileText size={14} /> Reports</h3>
        <div className="tools-reports">
          <button className="tools-report-btn"><FileText size={14} /><span>Generate Report</span></button>
          <button className="tools-report-btn"><Download size={14} /><span>Export PDF</span></button>
          <button className="tools-report-btn"><Printer size={14} /><span>Print</span></button>
        </div>
      </div>

      {/* Stats */}
      <div className="tools-section">
        <h3 className="tools-section-title"><BarChart3 size={14} /> Investigation Stats</h3>
        <div className="tools-stats">
          <div className="tools-stat"><StickyNote size={14} /><div className="tools-stat-info"><span className="tools-stat-value">{investigation.notes?.length || 0}</span><span className="tools-stat-label">Notes</span></div></div>
          <div className="tools-stat"><FileText size={14} /><div className="tools-stat-info"><span className="tools-stat-value">{investigation.evidence?.length || 0}</span><span className="tools-stat-label">Evidence</span></div></div>
          <div className="tools-stat"><Clock size={14} /><div className="tools-stat-info"><span className="tools-stat-value">{investigation.timeline?.length || 0}</span><span className="tools-stat-label">Events</span></div></div>
          <div className="tools-stat"><BarChart3 size={14} /><div className="tools-stat-info"><span className="tools-stat-value">{investigation.progress || 0}%</span><span className="tools-stat-label">Progress</span></div></div>
        </div>
      </div>
    </div>
  )
}
