import { useLanguage } from '../context/LanguageContext'
import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { ArrowLeft, Shield, AlertTriangle, Activity, Users, Fingerprint } from 'lucide-react'
import ProfileTab from './suspects/ProfileTab'
import BehavioralTab from './suspects/BehavioralTab'
import MOTab from './suspects/MOTab'
import TimelineTab from './suspects/TimelineTab'
import AssociatesTab from './suspects/AssociatesTab'
import { getSuspect } from '../services/search'
import { getSuspectRiskScore, getSuspectRiskFactors, scoreSuspect } from '../services/suspectRisk'
import { getSuspectTimeline } from '../services/criminalTimeline'

const tabs = [
  { id: 'profile', label: 'Profile', icon: Shield },
  { id: 'behavioral', label: 'Behavioral', icon: Activity },
  { id: 'mo', label: 'MO', icon: Fingerprint },
  { id: 'timeline', label: 'Timeline', icon: AlertTriangle },
  { id: 'associates', label: 'Associates', icon: Users },
]

const GRADIENTS = [
  'linear-gradient(135deg, #0f172a, #334155)',
  'linear-gradient(135deg, #1e3a5f, #3b82f6)',
  'linear-gradient(135deg, #7c2d12, #f59e0b)',
  'linear-gradient(135deg, #14532d, #22c55e)',
]

function initialsFromName(name = '') {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase() || '')
    .join('') || '?'
}

function normalizeSuspect(raw) {
  if (!raw || !raw.id) return null
  const name = raw.name || 'Unknown'
  return {
    id: raw.id,
    name,
    age: raw.age ?? '—',
    gender: raw.gender || '—',
    district: raw.district || '—',
    status: raw.status || 'Unknown',
    riskScore: raw.risk_score ?? raw.riskScore ?? 0,
    description: raw.description || 'No criminal summary available.',
    physicalDescription: raw.physical_description || raw.physicalDescription || 'No physical description available.',
    phone: raw.phone || '—',
    address: raw.address || '—',
    aliases: raw.aliases || [],
    cases: raw.cases ?? 0,
    moMatches: raw.moMatches ?? 0,
    lastActive: raw.lastActive || '—',
    initials: initialsFromName(name),
    gradient: GRADIENTS[Number(raw.id) % GRADIENTS.length],
    associates: raw.associates || [],
    timeline: raw.timeline || [],
    behavioralProfile: raw.behavioralProfile || {
      personality: 'Not enough data for a behavioral profile.',
      riskFactors: [],
      patterns: [],
    },
    moFingerprint: raw.moFingerprint || {
      entryMethod: '—',
      timing: '—',
      targetProfile: '—',
      weapon: '—',
      escapePattern: '—',
      crimeSequence: '—',
      matchScore: 0,
    },
  }
}

export default function SuspectDetailPage() {
  const { t } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const numericId = Number.parseInt(String(id).replace(/\D/g, ''), 10) || null
  const [suspect, setSuspect] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('profile')

  useEffect(() => {
    let cancelled = false
    async function load() {
      if (!numericId) {
        setLoading(false)
        setError('Invalid suspect id')
        return
      }
      setLoading(true)
      setError(null)
      try {
        const res = await getSuspect(numericId)
        let normalized = normalizeSuspect(res?.data)
        if (normalized) {
          // Enrich from risk + timeline APIs (best-effort)
          const [riskRes, factorsRes, timelineRes] = await Promise.all([
            getSuspectRiskScore(numericId).catch(() => null),
            getSuspectRiskFactors(numericId).catch(() => null),
            getSuspectTimeline(normalized.name).catch(() => null),
          ])
          const risk = riskRes?.data
          if (risk) {
            normalized = {
              ...normalized,
              riskScore: risk.overall_score ?? risk.risk_score ?? risk.score ?? normalized.riskScore,
            }
          }
          const factors = factorsRes?.data?.items || factorsRes?.data || []
          if (Array.isArray(factors) && factors.length) {
            normalized = {
              ...normalized,
              behavioralProfile: {
                ...normalized.behavioralProfile,
                riskFactors: factors.map((f) => f.factor || f.name || f.description || String(f)),
                personality: normalized.behavioralProfile.personality,
              },
            }
          }
          const tl = timelineRes?.data?.items || timelineRes?.data || []
          if (Array.isArray(tl) && tl.length) {
            normalized = {
              ...normalized,
              timeline: tl.map((e) => ({
                date: e.event_date || e.date || e.created_at || '—',
                event: e.title || e.description || e.event_type || 'Event',
                type: e.event_type || 'event',
              })),
              lastActive: (tl[0]?.event_date || tl[0]?.created_at || normalized.lastActive || '').toString().slice(0, 10),
            }
          }
          // If no risk score yet, try scoring once
          if (!risk && (normalized.riskScore === 0 || normalized.riskScore == null)) {
            try {
              const scored = await scoreSuspect(numericId)
              const s = scored?.data
              if (s) {
                normalized = {
                  ...normalized,
                  riskScore: s.overall_score ?? s.risk_score ?? s.score ?? normalized.riskScore,
                }
              }
            } catch { /* ignore */ }
          }
        }
        if (!cancelled) {
          setSuspect(normalized)
          if (!normalized) setError(res?.message || 'Suspect not found')
        }
      } catch (err) {
        if (!cancelled) {
          setSuspect(null)
          setError(err?.message || 'Failed to load suspect')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [numericId])

  if (loading) {
    return (
      <div className="case-detail-empty">
        <h2>{t('Loading…')}</h2>
      </div>
    )
  }

  if (!suspect) {
    return (
      <div className="case-detail-empty">
        <h2>{t('Suspect not found')}</h2>
        <p>{error || `${t('No suspect found with ID:')} ${id}`}</p>
        <button className="case-back-btn" onClick={() => navigate('/suspects')}>
          <ArrowLeft size={16} /> {t('Back to Suspects')}
        </button>
      </div>
    )
  }

  return (
    <div className="suspect-detail">
      <div className="suspect-detail-header">
        <button className="case-back-btn" onClick={() => navigate('/suspects')}>
          <ArrowLeft size={16} /> {t('Back to Suspects')}
        </button>

        <div className="suspect-detail-top">
          <div className="suspect-detail-avatar" style={{ background: suspect.gradient }}>
            {suspect.initials}
          </div>
          <div className="suspect-detail-info">
            <div className="suspect-detail-name-row">
              <h1 className="suspect-detail-name">{suspect.name}</h1>
              <span className={`status-badge ${String(suspect.status).toLowerCase().replace(' ', '-')}`}>
                {t(suspect.status)}
              </span>
            </div>
            <p className="suspect-detail-meta">
              {suspect.age} {t('years')} • {t(suspect.district)} • ID: {suspect.id}
            </p>
          </div>
          <div className="suspect-risk-display">
            <span className="risk-display-label">{t('Risk Score')}</span>
            <span className="risk-display-value" style={{
              color: suspect.riskScore > 70 ? '#ef4444' : suspect.riskScore > 40 ? '#f59e0b' : '#10b981'
            }}>
              {suspect.riskScore}
            </span>
          </div>
        </div>

        <div className="suspect-stats-row">
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.cases}</span>
            <span className="suspect-stat-label">{t('Cases')}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.moMatches}</span>
            <span className="suspect-stat-label">{t('MO Matches')}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.associates.length}</span>
            <span className="suspect-stat-label">{t('Associates')}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.lastActive}</span>
            <span className="suspect-stat-label">{t('Last Active')}</span>
          </div>
        </div>
      </div>

      <div className="suspect-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`suspect-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <tab.icon size={14} />
            {t(tab.label)}
          </button>
        ))}
      </div>

      <div className="suspect-content" key={`${suspect.id}-${activeTab}`}>
        {activeTab === 'profile' && <ProfileTab suspect={suspect} />}
        {activeTab === 'behavioral' && <BehavioralTab suspect={suspect} />}
        {activeTab === 'mo' && <MOTab suspect={suspect} />}
        {activeTab === 'timeline' && <TimelineTab suspect={suspect} />}
        {activeTab === 'associates' && <AssociatesTab suspect={suspect} />}
      </div>
    </div>
  )
}
