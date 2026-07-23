import { useState, useEffect } from 'react'
import { Brain, AlertTriangle, Shield, Crosshair, Target, DoorOpen, Clock, RefreshCw } from 'lucide-react'
import { getBehaviorProfiles, getRiskAssessment, analyzeCriminal, getBehaviorStats } from '../../services/behavior'
import { useLanguage } from '../../context/LanguageContext'

const profileIcons = {
  timing: Clock,
  weapon: Crosshair,
  target: Target,
  method: Shield,
  entry: DoorOpen,
}

const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

export default function BehavioralProfileTab() {
  const { t } = useLanguage()
  const [profiles, setProfiles] = useState([])
  const [riskAssessment, setRiskAssessment] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [analyzeId, setAnalyzeId] = useState('')
  const [expandedProfile, setExpandedProfile] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [profilesRes, riskRes, statsRes] = await Promise.all([
        getBehaviorProfiles(),
        getRiskAssessment(),
        getBehaviorStats(),
      ])
      setProfiles(profilesRes?.data?.items || [])
      setRiskAssessment(riskRes?.data || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load behavior data', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    if (!analyzeId || analyzing) return
    setAnalyzing(true)
    try {
      await analyzeCriminal(parseInt(analyzeId))
      await loadData()
      setAnalyzeId('')
    } catch (e) {
      console.error('Analysis failed', e)
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return (
      <div className="behavior-tab">
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>{t('Loading behavioral profiles...')}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="behavior-tab">
      {/* Header */}
      <div className="behavior-header">
        <div className="behavior-header-left">
          <Brain size={16} />
          <h3>{t('Behavioral Profiling')}</h3>
        </div>
        <div className="behavior-analyze">
          <input
            className="behavior-analyze-input"
            placeholder={t('Criminal ID')}
            value={analyzeId}
            onChange={(e) => setAnalyzeId(e.target.value)}
          />
          <button className="similar-btn similar-btn-primary" onClick={handleAnalyze} disabled={analyzing || !analyzeId}>
            {analyzing ? t('Analyzing...') : t('Analyze')}
          </button>
          <button className="intel-refresh" onClick={loadData} disabled={loading}>
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="behavior-stats">
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.total_profiles || 0}</span>
            <span className="behavior-stat-label">{t('Profiles')}</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.criminals_profiled || 0}</span>
            <span className="behavior-stat-label">{t('Criminals')}</span>
          </div>
          <div className="behavior-stat">
            <span className="behavior-stat-value">{stats.high_risk || 0}</span>
            <span className="behavior-stat-label">{t('High Risk')}</span>
          </div>
        </div>
      )}

      {/* Risk Assessment */}
      {riskAssessment.length > 0 && (
        <div className="behavior-risk-section">
          <h4><AlertTriangle size={14} /> {t('Risk Assessment')}</h4>
          <div className="behavior-risk-list">
            {riskAssessment.map((r, i) => (
              <div key={i} className="behavior-risk-item">
                <div className="behavior-risk-header">
                  <span className="behavior-risk-name">{r.alias}</span>
                  <span className="behavior-risk-badge" style={{ color: riskColors[r.risk_level], background: `${riskColors[r.risk_level]}15` }}>
                    {t(r.risk_level)}
                  </span>
                </div>
                <div className="behavior-risk-bar">
                  <div className="behavior-risk-fill" style={{ width: `${r.risk_score}%`, background: riskColors[r.risk_level] }} />
                </div>
                <span className="behavior-risk-score">{r.risk_score}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Profiles */}
      {profiles.length > 0 && (
        <div className="behavior-profiles-section">
          <h4><Shield size={14} /> {t('Behavioral Profiles')}</h4>
          <div className="behavior-profiles-grid">
            {profiles.map((p) => {
              const Icon = profileIcons[p.profile_type] || Shield
              const color = riskColors[p.risk_level] || '#10b981'
              return (
                <div
                  key={p.id}
                  className={`behavior-profile-card ${expandedProfile === p.id ? 'expanded' : ''}`}
                  onClick={() => setExpandedProfile(expandedProfile === p.id ? null : p.id)}
                >
                  <div className="behavior-profile-header">
                    <Icon size={14} style={{ color }} />
                    <span className="behavior-profile-type">{t(p.profile_type)}</span>
                    <span className="behavior-profile-confidence">{p.confidence}%</span>
                  </div>
                  <p className="behavior-profile-desc">{t(p.pattern_description)}</p>
                  <div className="behavior-profile-bar">
                    <div className="behavior-profile-fill" style={{ width: `${p.confidence}%`, background: color }} />
                  </div>
                  {expandedProfile === p.id && (
                    <div className="behavior-profile-details">
                      <span className="behavior-profile-risk">{t('Risk:')} {t(p.risk_level)} ({p.risk_score}%)</span>
                      <span className="behavior-profile-date">{t('Last analyzed:')} {p.last_analyzed ? new Date(p.last_analyzed).toLocaleDateString() : t('Never')}</span>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}

      {profiles.length === 0 && riskAssessment.length === 0 && (
        <div className="similar-empty">
          <Brain size={32} className="similar-empty-icon" />
          <p>{t('No behavioral profiles yet')}</p>
          <span>{t('Enter a Criminal ID and click Analyze to generate a behavioral profile.')}</span>
        </div>
      )}
    </div>
  )
}

