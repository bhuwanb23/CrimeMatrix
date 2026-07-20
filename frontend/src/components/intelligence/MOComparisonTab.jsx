import { useState, useEffect } from 'react'
import { Fingerprint, RefreshCw, ArrowRight, Search } from 'lucide-react'
import { getMOProfiles, compareMOs, batchFingerprint, getMOStats } from '../../services/mo'

export default function MOComparisonTab() {
  const [profiles, setProfiles] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [batching, setBatching] = useState(false)
  const [compareResult, setCompareResult] = useState(null)
  const [selected1, setSelected1] = useState('')
  const [selected2, setSelected2] = useState('')
  const [comparing, setComparing] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [profilesRes, statsRes] = await Promise.all([
        getMOProfiles(),
        getMOStats(),
      ])
      setProfiles(profilesRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load MO data', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleBatch() {
    setBatching(true)
    try {
      await batchFingerprint()
      await loadData()
    } catch (e) {
      console.error('Batch failed', e)
    } finally {
      setBatching(false)
    }
  }

  async function handleCompare() {
    if (!selected1 || !selected2 || comparing) return
    setComparing(true)
    try {
      const res = await compareMOs(parseInt(selected1), parseInt(selected2))
      setCompareResult(res?.data || res)
    } catch (e) {
      console.error('Compare failed', e)
    } finally {
      setComparing(false)
    }
  }

  if (loading) {
    return (
      <div className="mo-tab">
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading MO profiles...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="mo-tab">
      <div className="behavior-header">
        <div className="behavior-header-left">
          <Fingerprint size={16} />
          <h3>MO Fingerprinting</h3>
        </div>
        <div className="behavior-analyze">
          <button className="similar-btn similar-btn-primary" onClick={handleBatch} disabled={batching}>
            {batching ? 'Processing...' : 'Batch Fingerprint'}
          </button>
          <button className="intel-refresh" onClick={loadData} disabled={loading}>
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {stats && (
        <div className="behavior-stats">
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.total_profiles || 0}</span>
            <span className="behavior-stat-label">Profiles</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.total_comparisons || 0}</span>
            <span className="behavior-stat-label">Comparisons</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.avg_similarity || 0}%</span>
            <span className="behavior-stat-label">Avg Similarity</span>
          </div>
        </div>
      )}

      {/* MO Comparison Form */}
      <div className="mo-compare-form">
        <h4><Search size={14} /> Compare MO Profiles</h4>
        <div className="mo-compare-row">
          <select className="intel-filter-select" value={selected1} onChange={(e) => setSelected1(e.target.value)}>
            <option value="">Select Profile 1</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>Crime #{p.crime_id} — {p.mo_text?.slice(0, 40) || 'N/A'}</option>
            ))}
          </select>
          <ArrowRight size={16} className="mo-compare-arrow" />
          <select className="intel-filter-select" value={selected2} onChange={(e) => setSelected2(e.target.value)}>
            <option value="">Select Profile 2</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>Crime #{p.crime_id} — {p.mo_text?.slice(0, 40) || 'N/A'}</option>
            ))}
          </select>
          <button className="similar-btn similar-btn-primary" onClick={handleCompare} disabled={!selected1 || !selected2 || comparing}>
            {comparing ? 'Comparing...' : 'Compare'}
          </button>
        </div>
      </div>

      {/* Comparison Result */}
      {compareResult && (
        <div className="mo-compare-result">
          <div className="mo-compare-score">
            <span className="mo-compare-score-value">{compareResult.similarity_score}%</span>
            <span className="mo-compare-score-label">Similarity</span>
            <span className={`mo-compare-match ${compareResult.match_level}`}>{compareResult.match_level}</span>
          </div>
          {compareResult.shared_features && compareResult.shared_features.length > 0 && (
            <div className="mo-compare-features">
              <h5>Shared Features</h5>
              <div className="mo-feature-tags">
                {compareResult.shared_features.map((f, i) => (
                  <span key={i} className="mo-feature-tag">{f}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* MO Profiles List */}
      {profiles.length > 0 && (
        <div className="mo-profiles-section">
          <h4>MO Profiles ({profiles.length})</h4>
          <div className="mo-profiles-list">
            {profiles.map((p) => (
              <div key={p.id} className="mo-profile-card">
                <div className="mo-profile-header">
                  <span className="mo-profile-id">Crime #{p.crime_id}</span>
                  <span className="mo-profile-confidence">{p.confidence}%</span>
                </div>
                <p className="mo-profile-text">{p.mo_text || 'No MO data'}</p>
                <div className="mo-profile-features">
                  {p.fingerprint && Object.entries(p.fingerprint).map(([key, val]) => (
                    val && <span key={key} className="mo-feature-tag">{key}: {val}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {profiles.length === 0 && (
        <div className="similar-empty">
          <Fingerprint size={32} className="similar-empty-icon" />
          <p>No MO profiles yet</p>
          <span>Click "Batch Fingerprint" to analyze all crimes.</span>
        </div>
      )}
    </div>
  )
}
