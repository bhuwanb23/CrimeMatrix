import { useState, useEffect } from 'react'
import { UserX, RefreshCw, AlertTriangle, Clock, MapPin, Shield, TrendingUp } from 'lucide-react'
import { listRepeatOffenders, getRepeatOffenderStats, analyzeRepeatOffenders } from '../../services/repeatOffenders'

const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

const dimensionConfig = [
  { key: 'frequency_score', label: 'Frequency', icon: TrendingUp, color: '#f59e0b' },
  { key: 'recency_score', label: 'Recency', icon: Clock, color: '#ef4444' },
  { key: 'severity_score', label: 'Severity', icon: Shield, color: '#8b5cf6' },
  { key: 'geographic_score', label: 'Geographic', icon: MapPin, color: '#3b82f6' },
]

export default function RepeatOffenderTab() {
  const [offenders, setOffenders] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [expandedId, setExpandedId] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [offendersRes, statsRes] = await Promise.all([
        listRepeatOffenders(),
        getRepeatOffenderStats(),
      ])
      setOffenders(offendersRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load repeat offenders', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    setAnalyzing(true)
    try {
      await analyzeRepeatOffenders()
      await loadData()
    } catch (e) {
      console.error('Analysis failed', e)
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return (
      <div className="repeat-tab">
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading repeat offenders...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="repeat-tab">
      <div className="behavior-header">
        <div className="behavior-header-left">
          <UserX size={16} />
          <h3>Repeat Offender Tracking</h3>
        </div>
        <div className="behavior-analyze">
          <button className="similar-btn similar-btn-primary" onClick={handleAnalyze} disabled={analyzing}>
            {analyzing ? 'Analyzing...' : 'Analyze Offenders'}
          </button>
          <button className="intel-refresh" onClick={loadData} disabled={loading}>
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {stats && (
        <div className="behavior-stats">
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.total_offenders || 0}</span>
            <span className="behavior-stat-label">Offenders</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value" style={{ color: '#ef4444' }}>{stats.critical || 0}</span>
            <span className="behavior-stat-label">Critical</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value" style={{ color: '#f59e0b' }}>{stats.high || 0}</span>
            <span className="behavior-stat-label">High Risk</span>
          </div>
        </div>
      )}

      {offenders.length === 0 ? (
        <div className="similar-empty">
          <UserX size={32} className="similar-empty-icon" />
          <p>No repeat offenders identified</p>
          <span>Click "Analyze Offenders" to scan crime data for repeat offenders.</span>
        </div>
      ) : (
        <div className="repeat-list">
          {offenders.map((o, i) => (
            <div
              key={o.id || i}
              className={`repeat-card ${expandedId === o.id ? 'expanded' : ''}`}
              onClick={() => setExpandedId(expandedId === o.id ? null : o.id)}
            >
              <div className="repeat-card-header">
                <div className="repeat-card-rank">#{i + 1}</div>
                <div className="repeat-card-info">
                  <span className="repeat-card-name">{o.offender_name}</span>
                  <span className="repeat-card-offenses">{o.total_offenses} offenses</span>
                </div>
                <div className="repeat-card-score">
                  <span className="repeat-card-overall">{o.overall_score}%</span>
                  <span className="repeat-risk-badge" style={{ color: riskColors[o.risk_level], background: `${riskColors[o.risk_level]}15` }}>
                    {o.risk_level}
                  </span>
                </div>
              </div>

              <div className="repeat-card-dimensions">
                {dimensionConfig.map((dim) => (
                  <div key={dim.key} className="repeat-dim-row">
                    <span className="repeat-dim-label">{dim.label}</span>
                    <div className="repeat-dim-bar">
                      <div className="repeat-dim-fill" style={{ width: `${o[dim.key] || 0}%`, background: dim.color }} />
                    </div>
                    <span className="repeat-dim-value">{Math.round(o[dim.key] || 0)}%</span>
                  </div>
                ))}
              </div>

              {expandedId === o.id && o.risk_factors && o.risk_factors.length > 0 && (
                <div className="repeat-card-factors">
                  <h5>Risk Factors</h5>
                  {o.risk_factors.map((f, fi) => (
                    <div key={fi} className="repeat-factor-item">
                      <AlertTriangle size={10} />
                      <span>{f}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
