import { useState, useEffect } from 'react'
import { X, BarChart3 } from 'lucide-react'
import { compareCases } from '../../services/similarCases'

const DIMENSIONS = [
  { key: 'mo', label: 'Modus Operandi', icon: '🔍', color: '#f59e0b' },
  { key: 'location', label: 'Location', icon: '📍', color: '#3b82f6' },
  { key: 'time', label: 'Timing', icon: '⏰', color: '#10b981' },
  { key: 'suspects', label: 'Suspects', icon: '👤', color: '#8b5cf6' },
  { key: 'evidence', label: 'Evidence', icon: '🔬', color: '#ef4444' },
  { key: 'vehicles', label: 'Vehicles', icon: '🚗', color: '#06b6d4' },
]

function ScoreBar({ score, color, label }) {
  return (
    <div className="comparison-score-row">
      <span className="comparison-score-label">{label}</span>
      <div className="comparison-score-bar">
        <div
          className="comparison-score-fill"
          style={{ width: `${score}%`, backgroundColor: color }}
        />
      </div>
      <span className="comparison-score-value">{score}%</span>
    </div>
  )
}

function DimensionDetail({ dim, data }) {
  return (
    <div className="comparison-dimension">
      <div className="comparison-dim-header">
        <span className="comparison-dim-icon">{dim.icon}</span>
        <span className="comparison-dim-label">{dim.label}</span>
        <span className="comparison-dim-score" style={{ color: dim.color }}>
          {data.score}%
        </span>
      </div>
      <ScoreBar score={data.score} color={dim.color} label="" />
      <p className="comparison-dim-detail">{data.detail}</p>
      <span className="comparison-dim-weight">Weight: {(data.weight * 100).toFixed(0)}% | Weighted: {data.weighted}%</span>
    </div>
  )
}

export default function ComparisonView({ caseId1, caseId2, case2Title: _case2Title, onClose }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadComparison() {
      setLoading(true)
      setError(null)
      try {
        const res = await compareCases(caseId1, caseId2)
        setData(res?.data || res)
      } catch {
        setError('Failed to load comparison')
      } finally {
        setLoading(false)
      }
    }
    loadComparison()
  }, [caseId1, caseId2])

  return (
    <div className="comparison-overlay" onClick={onClose}>
      <div className="comparison-modal" onClick={e => e.stopPropagation()}>
        <div className="comparison-header">
          <div className="comparison-header-left">
            <BarChart3 size={18} />
            <h3>Case Comparison</h3>
          </div>
          <button className="comparison-close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {loading ? (
          <div className="comparison-loading">
            <div className="similar-spinner" />
            <span>Loading comparison...</span>
          </div>
        ) : error ? (
          <div className="comparison-error">{error}</div>
        ) : data ? (
          <>
            <div className="comparison-case-headers">
              <div className="comparison-case-col">
                <span className="comparison-case-id">Case #{caseId1}</span>
                <span className="comparison-case-label">Case A</span>
              </div>
              <div className="comparison-overall">
                <span className="comparison-overall-score">{data.overall_score}%</span>
                <span className="comparison-overall-label">Overall Match</span>
              </div>
              <div className="comparison-case-col">
                <span className="comparison-case-id">Case #{caseId2}</span>
                <span className="comparison-case-label">Case B</span>
              </div>
            </div>

            <div className="comparison-overall-bar">
              <div
                className="comparison-overall-fill"
                style={{ width: `${data.overall_score}%` }}
              />
            </div>

            <div className="comparison-dimensions">
              {DIMENSIONS.map(dim => {
                const dimData = data.dimension_scores?.[dim.key]
                if (!dimData) return null
                return <DimensionDetail key={dim.key} dim={dim} data={dimData} />
              })}
            </div>

            {data.reasons && data.reasons.length > 0 && (
              <div className="comparison-reasons">
                <h4>Similarity Reasons</h4>
                <div className="comparison-reasons-list">
                  {data.reasons.map((r, i) => (
                    <span key={i} className="similar-reason-tag">{r}</span>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : null}
      </div>
    </div>
  )
}
