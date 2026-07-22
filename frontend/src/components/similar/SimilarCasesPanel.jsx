import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Link2, BarChart3, ChevronDown, ChevronRight, RefreshCw, ExternalLink } from 'lucide-react'
import { getSimilarCases, computeSimilarities } from '../../services/similarCases'
import ComparisonView from './ComparisonView'

const DIMENSIONS = [
  { key: 'mo_score', label: 'MO', color: '#f59e0b' },
  { key: 'location_score', label: 'Location', color: '#3b82f6' },
  { key: 'time_score', label: 'Time', color: '#10b981' },
  { key: 'suspects_score', label: 'Suspects', color: '#8b5cf6' },
  { key: 'evidence_score', label: 'Evidence', color: '#ef4444' },
  { key: 'vehicles_score', label: 'Vehicles', color: '#06b6d4' },
]

function DimensionBar({ label, score, color }) {
  return (
    <div className="similar-dim-row">
      <span className="similar-dim-label">{label}</span>
      <div className="similar-dim-bar">
        <div
          className="similar-dim-fill"
          style={{ width: `${score}%`, backgroundColor: color }}
        />
      </div>
      <span className="similar-dim-value">{score}%</span>
    </div>
  )
}

function SimilarCaseCard({ item, onCompare, expanded, onToggle }) {
  const navigate = useNavigate()

  return (
    <div className={`similar-card ${expanded ? 'similar-card-expanded' : ''}`}>
      <div className="similar-card-header" onClick={onToggle}>
        <div className="similar-card-header-left">
          <span className="similar-card-id">{item.case_number || `Case #${item.case_id}`}</span>
          <span className={`similar-card-type ${item.crime_type?.toLowerCase().replace(/\s+/g, '-')}`}>
            {item.crime_type}
          </span>
        </div>
        <div className="similar-card-header-right">
          <span className="similar-card-score">{item.overall_score}%</span>
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </div>
      </div>

      <p className="similar-card-title">{item.title}</p>
      <div className="similar-card-meta">
        <span>{item.district}</span>
        <span className={`status-badge ${item.status}`}>{item.status}</span>
      </div>

      <div className="similar-card-score-bar">
        <div className="similar-score-fill" style={{ width: `${item.overall_score}%` }} />
      </div>

      {expanded && (
        <div className="similar-card-details">
          {DIMENSIONS.map(dim => (
            <DimensionBar
              key={dim.key}
              label={dim.label}
              score={item[dim.key] || 0}
              color={dim.color}
            />
          ))}
          {item.reasons && item.reasons.length > 0 && (
            <div className="similar-card-reasons">
              <span className="similar-reasons-label">Reasons:</span>
              {item.reasons.map((r, i) => (
                <span key={i} className="similar-reason-tag">{r}</span>
              ))}
            </div>
          )}
          <div className="similar-card-actions">
            <button className="similar-btn similar-btn-primary" onClick={() => navigate(`/cases/${item.case_id}`)}>
              <ExternalLink size={12} /> View Case
            </button>
            <button className="similar-btn similar-btn-secondary" onClick={() => onCompare(item)}>
              <BarChart3 size={12} /> Compare
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default function SimilarCasesPanel({ caseId }) {
  const [similarCases, setSimilarCases] = useState([])
  const [loading, setLoading] = useState(false)
  const [computing, setComputing] = useState(false)
  const [expandedId, setExpandedId] = useState(null)
  const [compareTarget, setCompareTarget] = useState(null)
  const [error, setError] = useState(null)

  const loadSimilar = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await getSimilarCases(caseId, 10)
      const data = res?.data || res
      setSimilarCases(data?.similar_cases || [])
    } catch {
      setError('Failed to load similar cases')
    } finally {
      setLoading(false)
    }
  }, [caseId])

  useEffect(() => {
    if (caseId) loadSimilar()
  }, [caseId, loadSimilar])

  async function handleCompute() {
    setComputing(true)
    try {
      await computeSimilarities(caseId, true)
      await loadSimilar()
    } catch {
      setError('Failed to compute similarities')
    } finally {
      setComputing(false)
    }
  }

  if (loading) {
    return (
      <div className="similar-panel">
        <div className="similar-panel-header">
          <Link2 size={16} />
          <h3>Similar Cases</h3>
        </div>
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading similar cases...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="similar-panel">
      <div className="similar-panel-header">
        <div className="similar-panel-title">
          <Link2 size={16} />
          <h3>Similar Cases</h3>
          <span className="similar-count">{similarCases.length}</span>
        </div>
        <button
          className="similar-compute-btn"
          onClick={handleCompute}
          disabled={computing}
        >
          <RefreshCw size={14} className={computing ? 'similar-spinning' : ''} />
          {computing ? 'Computing...' : 'Compute'}
        </button>
      </div>

      {error && <div className="similar-error">{error}</div>}

      {similarCases.length === 0 ? (
        <div className="similar-empty">
          <Link2 size={32} className="similar-empty-icon" />
          <p>No similar cases found</p>
          <button className="similar-compute-btn" onClick={handleCompute} disabled={computing}>
            <RefreshCw size={14} />
            Compute Similarities
          </button>
        </div>
      ) : (
        <div className="similar-list">
          {similarCases.map((item) => (
            <SimilarCaseCard
              key={item.case_id}
              item={item}
              expanded={expandedId === item.case_id}
              onToggle={() => setExpandedId(expandedId === item.case_id ? null : item.case_id)}
              onCompare={(target) => setCompareTarget(target)}
            />
          ))}
        </div>
      )}

      {compareTarget && (
        <ComparisonView
          caseId1={caseId}
          caseId2={compareTarget.case_id}
          case2Title={compareTarget.title}
          onClose={() => setCompareTarget(null)}
        />
      )}
    </div>
  )
}
