import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles, FileText, User, MapPin, AlertTriangle, ChevronRight, RefreshCw } from 'lucide-react'
import { getDashboardRecommendations, getCaseRecommendations } from '../../services/recommendations'

const typeConfig = {
  similar_case: { icon: FileText, label: 'Similar Case', color: '#f59e0b', route: '/cases' },
  suspect_alert: { icon: User, label: 'Suspect Alert', color: '#ef4444', route: '/suspects' },
  cross_district: { icon: MapPin, label: 'Cross-District', color: '#3b82f6', route: '/cases' },
  mo_pattern: { icon: AlertTriangle, label: 'MO Pattern', color: '#8b5cf6', route: '/cases' },
}

export default function RecommendationsPanel({ caseId = null, compact = false }) {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadRecommendations()
  }, [caseId])

  async function loadRecommendations() {
    setLoading(true)
    try {
      const res = caseId
        ? await getCaseRecommendations(caseId)
        : await getDashboardRecommendations()
      const data = res?.data || res
      setRecommendations(data?.recommendations || [])
    } catch (e) {
      console.error('Failed to load recommendations', e)
    } finally {
      setLoading(false)
    }
  }

  function handleClick(rec) {
    const config = typeConfig[rec.type] || typeConfig.similar_case
    const id = rec.case_id || rec.suspect_id
    if (id) navigate(`${config.route}/${id}`)
  }

  if (loading) {
    return (
      <div className="rec-panel">
        <div className="rec-header">
          <Sparkles size={16} />
          <h3>Recommended for Investigation</h3>
        </div>
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="rec-panel">
      <div className="rec-header">
        <div className="rec-header-left">
          <Sparkles size={16} />
          <h3>Recommended for Investigation</h3>
          <span className="similar-count">{recommendations.length}</span>
        </div>
        <button className="rec-refresh" onClick={loadRecommendations}>
          <RefreshCw size={12} />
        </button>
      </div>

      {recommendations.length === 0 ? (
        <div className="similar-empty">
          <Sparkles size={24} className="similar-empty-icon" />
          <p>No recommendations yet</p>
        </div>
      ) : (
        <div className="rec-list">
          {recommendations.map((rec, i) => {
            const config = typeConfig[rec.type] || typeConfig.similar_case
            const Icon = config.icon
            return (
              <div
                key={i}
                className="rec-card"
                onClick={() => handleClick(rec)}
                style={{ animationDelay: `${i * 0.05}s` }}
              >
                <div className="rec-card-icon" style={{ color: config.color }}>
                  <Icon size={14} />
                </div>
                <div className="rec-card-info">
                  <div className="rec-card-top">
                    <span className="rec-card-type" style={{ color: config.color }}>
                      {config.label}
                    </span>
                    <span className="rec-card-score">{rec.score}%</span>
                  </div>
                  <p className="rec-card-title">
                    {rec.title || rec.name || rec.message || 'Unknown'}
                  </p>
                  {rec.reasons && rec.reasons.length > 0 && (
                    <span className="rec-card-reason">{rec.reasons[0]}</span>
                  )}
                  {rec.description && (
                    <span className="rec-card-desc">{rec.description}</span>
                  )}
                </div>
                <ChevronRight size={14} className="rec-card-arrow" />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
