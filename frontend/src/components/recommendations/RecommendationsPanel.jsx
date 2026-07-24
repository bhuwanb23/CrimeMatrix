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
import { explainRecommendation } from '../../services/proactive'
import ExplainButton from '../intelligence/ExplainButton'
import ExplanationPanel from '../intelligence/ExplanationPanel'
import { useLanguage } from '../../context/LanguageContext'

const typeConfig = {
  similar_case: { icon: FileText, label: 'Similar Case', color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200', route: '/cases' },
  suspect_alert: { icon: User, label: 'Suspect Alert', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200', route: '/search/suspects' },
  cross_district: { icon: MapPin, label: 'Cross-District', color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200', route: '/cases' },
  mo_pattern: { icon: AlertTriangle, label: 'MO Pattern', color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200', route: '/cases' },
  evidence_review: { icon: Search, label: 'Evidence Review', color: 'text-sky-600', bg: 'bg-sky-50', border: 'border-sky-200', route: '/cases' },
  officer_assignment: { icon: UserCheck, label: 'Officer Assignment', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200', route: '/cases' },
  priority_escalation: { icon: AlertTriangle, label: 'Priority Escalation', color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200', route: '/cases' },
  related_investigation: { icon: Link, label: 'Related Investigation', color: 'text-violet-600', bg: 'bg-violet-50', border: 'border-violet-200', route: '/cases' },
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
  const { t } = useLanguage()
  const [recommendations, setRecommendations] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [feedbackMap, setFeedbackMap] = useState({})
  const [explainingId, setExplainingId] = useState(null)
  const [explanation, setExplanation] = useState(null)
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
    } catch (e) { console.error('Feedback failed', e) }
  }

  async function handleExplain(recId) {
    if (explainingId === recId) {
      setExplainingId(null)
      setExplanation(null)
      return
    }
    setExplainingId(recId)
    setExplanation(null)
    try {
      const res = await explainRecommendation(recId)
      setExplanation(res?.data || res)
    } catch (e) { console.error('Explain failed', e) } finally { setExplainingId(null) }
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
    const key = r.rec_type || r.type
    tabCounts[key] = (tabCounts[key] || 0) + 1
  })

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles size={16} className="text-amber-500" />
          <h3 className="text-slate-900 font-semibold text-sm">{t('Recommendations')}</h3>
        </div>
        <div className="flex items-center justify-center py-8">
          <div className="w-5 h-5 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
          <span className="ml-3 text-slate-400 text-sm">{t('Loading...')}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-amber-500" />
          <h3 className="text-slate-900 font-semibold text-sm">{t('Recommendations')}</h3>
          <span className="text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded-full font-medium">
            {recommendations.length}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="text-[10px] bg-purple-100 text-purple-700 hover:bg-purple-200 px-2 py-1 rounded-lg transition-colors font-medium disabled:opacity-50"
          >
            {generating ? t('Generating...') : t('AI Generate')}
          </button>
          <button onClick={loadRecommendations} className="text-slate-400 hover:text-slate-600 transition-colors p-1">
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
                  ? 'bg-amber-100 text-amber-700 border border-amber-300'
                  : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50 border border-transparent'
              }`}
            >
              <TabIcon size={10} />
              {t(tab.label)}
              {count > 0 && <span className="text-[9px] opacity-60">{count}</span>}
            </button>
          )
        })}
      </div>

      {/* Recommendation List */}
      {displayItems.length === 0 ? (
        <div className="text-center py-8">
          <Sparkles size={28} className="mx-auto text-slate-200 mb-2" />
          <p className="text-slate-400 text-sm">{t('No recommendations')}</p>
          <p className="text-slate-300 text-xs mt-1">{t('Click "AI Generate" to create recommendations')}</p>
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
                className={`group relative rounded-xl border p-3 cursor-pointer transition-all hover:shadow-sm ${
                  fb === 'accepted'
                    ? 'border-green-300 bg-green-50'
                    : fb === 'dismissed'
                    ? 'border-slate-200 bg-slate-50 opacity-50'
                    : `${config.border} ${config.bg}`
                }`}
              >
                {/* Top row: type badge + score */}
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-1.5">
                    <Icon size={12} className={config.color} />
                    <span className={`text-[10px] font-semibold uppercase tracking-wider ${config.color}`}>
                      {t(config.label)}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-slate-400">{rec.score || rec.confidence || 0}%</span>
                </div>

                {/* Title */}
                <p className="text-slate-900 text-xs font-medium leading-relaxed">
                  {rec.title || rec.name || rec.message || 'Recommendation'}
                </p>

                {/* Description */}
                {rec.description && (
                  <p className="text-slate-500 text-[11px] mt-1 line-clamp-2">{rec.description}</p>
                )}

                {/* Reasons */}
                {rec.reasons && rec.reasons.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {rec.reasons.slice(0, 2).map((r, j) => (
                      <span key={j} className="text-[10px] bg-white text-slate-500 border border-slate-200 px-1.5 py-0.5 rounded">
                        {r}
                      </span>
                    ))}
                  </div>
                )}

                {/* Action Buttons */}
                {rec.id && (
                  <div className="flex items-center gap-1 mt-2 pt-2 border-t border-slate-100">
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'accepted') }}
                      className={`flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'accepted'
                          ? 'bg-green-100 text-green-700'
                          : 'text-slate-400 hover:text-green-600 hover:bg-green-50'
                      }`}
                      title="Accept"
                    >
                      <CheckCircle size={10} />
                      <span>{t('Accept')}</span>
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'dismissed') }}
                      className={`flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'dismissed'
                          ? 'bg-red-100 text-red-700'
                          : 'text-slate-400 hover:text-red-600 hover:bg-red-50'
                      }`}
                      title={t('Dismiss')}
                    >
                      <XCircle size={10} />
                      <span>{t('Dismiss')}</span>
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'rated_up') }}
                      className={`flex items-center text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'rated_up'
                          ? 'bg-amber-100 text-amber-700'
                          : 'text-slate-400 hover:text-amber-600 hover:bg-amber-50'
                      }`}
                      title={t('Useful')}
                    >
                      <ThumbsUp size={10} />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleFeedback(rec.id, 'rated_down') }}
                      className={`flex items-center text-[10px] px-1.5 py-0.5 rounded transition-colors ${
                        fb === 'rated_down'
                          ? 'bg-slate-100 text-slate-600'
                          : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
                      }`}
                      title={t('Not useful')}
                    >
                      <ThumbsDown size={10} />
                    </button>
                    <ExplainButton onClick={() => handleExplain(rec.id)} loading={explainingId === rec.id} />
                    <ChevronRight size={12} className="ml-auto text-slate-300 group-hover:text-slate-500 transition-colors" />
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
