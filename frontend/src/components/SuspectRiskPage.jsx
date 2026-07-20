import { useState, useEffect } from 'react'
import { Shield, RefreshCw, AlertTriangle, TrendingUp, Users } from 'lucide-react'
import { getSuspectRiskStats, getSuspectRiskRankings, batchScoreSuspects, getSuspectRiskScore, getSuspectRiskFactors } from '../services/suspectRisk'

const riskColors = {
  very_high: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

const factorColors = {
  criminal_history: '#ef4444',
  offense_severity: '#f59e0b',
  age_factor: '#3b82f6',
  location_risk: '#10b981',
  associate_risk: '#8b5cf6',
  recency: '#06b6d4',
  network_influence: '#ec4899',
  mo_similarity: '#f97316',
  investigation_links: '#84cc16',
  behavioral: '#a855f7',
}

export default function SuspectRiskPage() {
  const [stats, setStats] = useState(null)
  const [rankings, setRankings] = useState([])
  const [selectedSuspect, setSelectedSuspect] = useState(null)
  const [selectedScore, setSelectedScore] = useState(null)
  const [selectedFactors, setSelectedFactors] = useState([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [statsRes, rankingsRes] = await Promise.all([
        getSuspectRiskStats(),
        getSuspectRiskRankings(10),
      ])
      setStats(statsRes?.data || statsRes)
      setRankings(rankingsRes?.data || [])
    } catch (e) {
      console.error('Failed to load risk data', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleBatchScore() {
    setScoring(true)
    try {
      await batchScoreSuspects()
      await loadData()
    } catch (e) {
      console.error('Batch score failed', e)
    } finally {
      setScoring(false)
    }
  }

  async function handleSelectSuspect(suspectId) {
    if (selectedSuspect === suspectId) {
      setSelectedSuspect(null)
      setSelectedScore(null)
      setSelectedFactors([])
      return
    }
    setSelectedSuspect(suspectId)
    try {
      const [scoreRes, factorsRes] = await Promise.all([
        getSuspectRiskScore(suspectId),
        getSuspectRiskFactors(suspectId),
      ])
      setSelectedScore(scoreRes?.data || null)
      setSelectedFactors(factorsRes?.data?.items || [])
    } catch (e) {
      console.error('Failed to load suspect details', e)
    }
  }

  return (
    <div className="suspect-risk-page">
      <div className="intel-header">
        <div className="intel-header-left">
          <Shield size={22} />
          <div>
            <h1>Suspect Risk Scoring</h1>
            <p>Transparent, explainable risk assessment for suspects</p>
          </div>
        </div>
        <div className="intel-header-actions">
          <button className="similar-btn similar-btn-primary" onClick={handleBatchScore} disabled={scoring}>
            {scoring ? 'Scoring...' : 'Batch Score All'}
          </button>
          <button className="intel-refresh" onClick={loadData} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="analytics-summary-cards">
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#f59e0b' }}>
              <Users size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">Scored</span>
              <span className="analytics-pred-value">{stats.total_scored || 0}</span>
            </div>
          </div>
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#ef4444' }}>
              <AlertTriangle size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">High Risk</span>
              <span className="analytics-pred-value">{stats.high_risk || 0}</span>
            </div>
          </div>
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#3b82f6' }}>
              <TrendingUp size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">Avg Score</span>
              <span className="analytics-pred-value">{stats.avg_score || 0}%</span>
            </div>
          </div>
        </div>
      )}

      <div className="intel-row">
        {/* Rankings */}
        <div className="analytics-panel">
          <div className="analytics-panel-header">
            <Shield size={14} />
            <h3>Suspect Rankings</h3>
          </div>
          {rankings.length === 0 ? (
            <div className="similar-empty"><p>No suspects scored yet. Click Batch Score.</p></div>
          ) : (
            <div className="analytics-risk-list">
              {rankings.map((r, i) => {
                const color = riskColors[r.risk_level] || '#64748b'
                const isSelected = selectedSuspect === r.suspect_id
                return (
                  <div
                    key={r.suspect_id || i}
                    className={`analytics-risk-item ${isSelected ? 'selected' : ''}`}
                    onClick={() => handleSelectSuspect(r.suspect_id)}
                    style={{ cursor: 'pointer' }}
                  >
                    <div className="analytics-risk-rank">#{i + 1}</div>
                    <div className="analytics-risk-info">
                      <span className="analytics-risk-name">{r.name}</span>
                      <div className="analytics-risk-bar">
                        <div className="analytics-risk-fill" style={{ width: `${r.overall_score}%`, background: color }} />
                      </div>
                      <div className="analytics-risk-meta">
                        <span>{r.district}</span>
                        <span className="analytics-risk-badge" style={{ color }}>{r.risk_level}</span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Score Breakdown */}
        <div className="analytics-panel">
          <div className="analytics-panel-header">
            <AlertTriangle size={14} />
            <h3>Score Breakdown</h3>
          </div>
          {selectedScore ? (
            <div className="risk-breakdown">
              <div className="risk-overall">
                <span className="risk-overall-score" style={{ color: riskColors[selectedScore.risk_level] }}>
                  {selectedScore.overall_score}%
                </span>
                <span className="risk-overall-level" style={{ color: riskColors[selectedScore.risk_level] }}>
                  {selectedScore.risk_level}
                </span>
              </div>
              {selectedScore.explanation && selectedScore.explanation.map((exp, i) => (
                <div key={i} className="risk-explanation-item">
                  <AlertTriangle size={10} style={{ color: '#f59e0b' }} />
                  <span>{exp}</span>
                </div>
              ))}
              {selectedFactors.length > 0 && (
                <div className="risk-factors">
                  {selectedFactors.map((f, i) => (
                    <div key={i} className="risk-factor-item">
                      <span className="risk-factor-name">{f.name.replace(/_/g, ' ')}</span>
                      <div className="risk-factor-bar">
                        <div className="risk-factor-fill" style={{ width: `${f.value}%`, background: factorColors[f.name] || '#64748b' }} />
                      </div>
                      <span className="risk-factor-value">{f.value}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="similar-empty"><p>Select a suspect to view breakdown</p></div>
          )}
        </div>
      </div>
    </div>
  )
}
