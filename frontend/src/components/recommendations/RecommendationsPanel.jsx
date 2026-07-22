import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Sparkles, FileText, User, MapPin, AlertTriangle, ChevronRight, RefreshCw,
  CheckCircle, XCircle, ThumbsUp, ThumbsDown, Search, UserCheck, Link,
} from 'lucide-react'
import {
  getDashboardRecommendations, getCaseRecommendations, getInvestigationRecommendations,
  getAllRecommendations, submitFeedback, generateRecommendations,
} from '../../services/recommendations'

const typeConfig = {
  similar_case: { icon: FileText, label: 'Similar Case', color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/30', route: '/cases' },
  suspect_alert: { icon: User, label: 'Suspect Alert', color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', route: '/search/suspects' },
  cross_district: { icon: MapPin, label: 'Cross-District', color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/30', route: '/cases' },
  mo_pattern: { icon: AlertTriangle, label: 'MO Pattern', color: 'text-purple-400', bg: 'bg-purple-500/10', border: 'border-purple-500/30', route: '/cases' },
  evidence_review: { icon: Search, label: 'Evidence Review', color: 'text-sky-400', bg: 'bg-sky-500/10', border: 'border-sky-500/30', route: '/cases' },
  officer_assignment: { icon: UserCheck, label: 'Officer Assignment', color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/30', route: '/cases' },
  priority_escalation: { icon: AlertTriangle, label: 'Priority Escalation', color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/30', route: '/cases' },
  related_investigation: { icon: Link, label: 'Related Investigation', color: 'text-violet-400', bg: 'bg-violet-500/10', border: 'border-violet-500/30', route: '/cases' },
}

const tabs = [
  { key: null, label: 'All', icon: Sparkles },
  { key: 'similar_case', label: 'Cases', icon: FileText },
  { key: 'suspect_alert', label: 'Suspects', icon: User },
  { key: 'evidence_review', label: 'Evidence', icon: Search },
  { key: 'officer_assignment', label: 'Assign', icon: UserCheck },
  { key: 'priority_escalation', label: 'Escalation', icon: AlertTriangle },
  { key: 'related_investigation', label: 'Related', icon: Link },
]

export default function RecommendationsPanel({ caseId = null, investigationId = null, compact = false, maxItems }) {
  const [recommendations, setRecommendations] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [feedbackMap, setFeedbackMap] = useState({})
  const navigate = useNavigate()

  const loadRecommendations = useCallback(async () => {
    setLoading(true)
    try {
      let res
      if (caseId) {
        res = await getCaseRecommendations(caseId)
      } else if (investigationId) {
        res = await getInvestigationRecommendations(investigationId)
      } else {
        const persisted = await getAllRecommendations({ status: 'active', limit: 20 })
        const pData = persisted?.data || persisted
        const persistedRecs = pData?.recommendations || []
        if (persistedRecs.length > 0) {
          setRecommendations(persistedRecs)
          setLoading(false)
          return
        }
        res = await getDashboardRecommendations()
      }
      const data = res?.data || res
      setRecommendations(data?.recommendations || [])
    } catch (e) {
      console.error('Failed to load recommendations', e)
    } finally {
      setLoading(false)
    }
  }, [caseId, investigationId])

  const handleGenerate = useCallback(async () => {
    setGenerating(true)
    try {
      await generateRecommendations(caseId ? 'case' : investigationId ? 'investigation' : 'dashboard', caseId || investigationId)
      await loadRecommendations()
    } catch (e) {
      console.error('Failed to generate recommendations', e)
    } finally {
      setGenerating(false)
    }
  }, [caseId, investigationId, loadRecommendations])

  useEffect(() => { loadRecommendations() }, [loadRecommendations])

  async function handleFeedback(recId, feedback) {
    try {
      await submitFeedback(recId, feedback)
      setFeedbackMap(prev => ({ ...prev, [recId]: feedback }))
    } catch (e) {
      console.error('Feedback failed', e)
    }
  }

  function handleClick(rec) {
    const config = typeConfig[rec.rec_type || rec.type] || typeConfig.similar_case
    const id = rec.entity_id || rec.case_id || rec.suspect_id
    if (id) navigate(`${config.route}/${id}`)
  }

  const filtered = activeTab
    ? recommendations.filter(r => (r.rec_type || r.type) === activeTab)
    : recommendations
  const displayItems = maxItems ? filtered.slice(0, maxItems) : (compact ? filtered.slice(0, 5) : filtered)

  const tabCounts = {}
  recommendations.forEach(r => {
    const t = r.rec_type || r.type
    tabCounts[t] = (tabCounts[t] || 0) + 1
  })

  if (loading) {
    return (
      <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-5">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles size={16} className="text-cyan-400" />
          <h3 className="text-white font-semibold text-sm">Recommendations</h3>
        </div>
        <div className="flex items-center justify-center py-8">
          <div className="w-5 h-5 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin" />
          <span className="ml-3 text-white/50 text-sm">Loading...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-cyan-400" />
          <h3 className="text-white font-semibold text-sm">Recommendations</h3>
          <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-1.5 py-0.5 rounded-full font-medium">
            {recommendations.length}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="text-[10px] bg-purple-500/20 text-purple-300 hover:bg-purple-500/30 px-2 py-1 rounded-lg transition-colors disabled:opacity-50"
          >
            {generating ? 'Generating...' : 'AI Generate'}
          </button>
          <button onClick={loadRecommendations} className="text-white/40 hover:text-white/70 transition-colors p-1">
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-4 overflow-x-auto pb-1 -mx-1 px-1">
        {tabs.map(tab => {
          const count = tab.key ? (tabCounts[tab.key] || 0) : recommendations.length
          if (tab.key && count === 0) return null
          const TabIcon = tab.icon
          return (
            <button
              key={tab.key || 'all'}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-medium whitespace-nowrap transition-all ${
                activeTab === tab.key
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                  : 'text-white/40 hover:text-white/60 hover:bg-white/5 border border-transparent'
              }`}
            >
              <TabIcon size={10} />
              {tab.label}
              {count > 0 && <span className="text-[9px] opacity-60">{count}</span>}
            </button>
          )
        })}
      </div>

      {/* Recommendation List */}
      {displayItems.length === 0 ? (
        <div className="text-center py-8">
          <Sparkles size={28} className="mx-auto text-white/20 mb-2" />
          <p className="text-white/40 text-sm">No recommendations</p>
          <p className="text-white/25 text-xs mt-1">Click "AI Generate" to create recommendations</p>
        </div>
      ) : (
        <div className="space-y-2">
          {displayItems.map((rec, i) => {
            const recType = rec.rec_type || rec.type
            const config = typeConfig[recType] || typeConfig.similar_case
            const Icon = config.icon
            const fb = feedbackMap[rec.id] || rec.feedback
            return (
              <div
                key={rec.id || i}
                onClick={() => handleClick(rec)}
                className={`group relative rounded-xl border p-3 cursor-pointer transition-all hover:bg-white/5 ${
                  fb === 'accepted'
                    ? 'border-green-500/30 bg-green-500/5'
                    : fb === 'dismissed'
                    ? 'border-white/5 bg-white/[0.02] opacity-50'
                    : `${config.border} ${config.bg}`
                }`}
              >
                {/* Top row: type badge + score */}
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-1.5">
                    <Icon size={12} className={config.color} />
                    <span className={`text-[10px] font-semibold uppercase tracking-wider ${config.color}`}>
                      {config.label}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-white/50">{rec.score || rec.confidence || 0}%</span>
                </div>

                {/* Title */}
                <p className="text-white/90 text-xs font-medium leading-relaxed">
                  {rec.title || rec.name || rec.message || 'Recommendation'}
                </p>

                {/* Description */}
                {rec.description && (
                  <p className="text-white/40 text-[11px] mt-1 line-clamp-2">{rec.description}</p>
                )}

                {/* Reasons */}
                {rec.reasons && rec.reasons.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {rec.reasons.slice(0, 2).map((r, j) => (
                      <span key={j} className="text-[10px] bg-white/5 text-white/50 px-1.5 py-0.5 rounded">
                        {r}
                      </span>
                    ))}
                  </div>
                )}

                {/* Action Buttons */}
                {rec.id && (
                  <div className="flex items-center gap-1 mt-2 pt-2 border-t border-white/5">
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'accepted') }}
                      className={`flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'accepted'
                          ? 'bg-green-500/20 text-green-400'
                          : 'text-white/30 hover:text-green-400 hover:bg-green-500/10'
                      }`}
                      title="Accept"
                    >
                      <CheckCircle size={10} />
                      <span>Accept</span>
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'dismissed') }}
                      className={`flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'dismissed'
                          ? 'bg-red-500/20 text-red-400'
                          : 'text-white/30 hover:text-red-400 hover:bg-red-500/10'
                      }`}
                      title="Dismiss"
                    >
                      <XCircle size={10} />
                      <span>Dismiss</span>
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'rated_up') }}
                      className={`flex items-center text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'rated_up'
                          ? 'bg-amber-500/20 text-amber-400'
                          : 'text-white/30 hover:text-amber-400 hover:bg-amber-500/10'
                      }`}
                      title="Useful"
                    >
                      <ThumbsUp size={10} />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'rated_down') }}
                      className={`flex items-center text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'rated_down'
                          ? 'bg-slate-500/20 text-slate-400'
                          : 'text-white/30 hover:text-slate-400 hover:bg-slate-500/10'
                      }`}
                      title="Not useful"
                    >
                      <ThumbsDown size={10} />
                    </button>
                    <ChevronRight size={12} className="ml-auto text-white/20 group-hover:text-white/40 transition-colors" />
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
