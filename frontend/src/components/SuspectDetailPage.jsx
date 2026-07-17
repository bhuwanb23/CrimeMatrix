import { useParams, useNavigate } from 'react-router-dom'
import { getSuspectById } from './suspects/suspectsData'
import { useState } from 'react'
import { ArrowLeft, Shield, AlertTriangle, Activity, Users, Fingerprint } from 'lucide-react'
import ProfileTab from './suspects/ProfileTab'
import BehavioralTab from './suspects/BehavioralTab'
import MOTab from './suspects/MOTab'
import TimelineTab from './suspects/TimelineTab'
import AssociatesTab from './suspects/AssociatesTab'

const tabs = [
  { id: 'profile', label: 'Profile', icon: Shield },
  { id: 'behavioral', label: 'Behavioral', icon: Activity },
  { id: 'mo', label: 'MO', icon: Fingerprint },
  { id: 'timeline', label: 'Timeline', icon: AlertTriangle },
  { id: 'associates', label: 'Associates', icon: Users },
]
import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function SuspectDetailPage() {
  const { lang } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const suspect = getSuspectById(id)
  const [activeTab, setActiveTab] = useState('profile')

  if (!suspect) {
    return (
      <div className="case-detail-empty">
        <h2>{t('suspect_not_found', lang) || "Suspect not found"}</h2>
        <p>{t('no_suspect_found_with_id', lang) || "No suspect found with ID"}: {id}</p>
        <button className="case-back-btn" onClick={() => navigate('/suspects')}>
          <ArrowLeft size={16} /> {t('back_to_suspects', lang) || "Back to Suspects"}
        </button>
      </div>
    )
  }

  return (
    <div className="suspect-detail">
      {/* Header */}
      <div className="suspect-detail-header">
        <button className="case-back-btn" onClick={() => navigate('/suspects')}>
          <ArrowLeft size={16} /> {t('back_to_suspects', lang) || "Back to Suspects"}
        </button>

        <div className="suspect-detail-top">
          <div className="suspect-detail-avatar" style={{ background: suspect.gradient }}>
            {suspect.initials}
          </div>
          <div className="suspect-detail-info">
            <div className="suspect-detail-name-row">
              <h1 className="suspect-detail-name">{suspect.name}</h1>
              <span className={`status-badge ${suspect.status.toLowerCase().replace(' ', '-')}`}>
                {suspect.status}
              </span>
            </div>
            <p className="suspect-detail-meta">
              {suspect.age} years • {suspect.district} • ID: {suspect.id}
            </p>
          </div>
          <div className="suspect-risk-display">
            <span className="risk-display-label">{t('risk_score', lang) || "Risk Score"}</span>
            <span className="risk-display-value" style={{
              color: suspect.riskScore > 70 ? '#ef4444' : suspect.riskScore > 40 ? '#f59e0b' : '#10b981'
            }}>
              {suspect.riskScore}
            </span>
          </div>
        </div>

        {/* Stats Row */}
        <div className="suspect-stats-row">
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.cases}</span>
            <span className="suspect-stat-label">{t('cases', lang) || "Cases"}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.moMatches}</span>
            <span className="suspect-stat-label">{t('mo_matches', lang) || "MO Matches"}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.associates.length}</span>
            <span className="suspect-stat-label">{t('associates', lang) || "Associates"}</span>
          </div>
          <div className="suspect-stat">
            <span className="suspect-stat-value">{suspect.lastActive}</span>
            <span className="suspect-stat-label">{t('last_active', lang) || "Last Active"}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="suspect-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`suspect-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <tab.icon size={14} />
            {t(tab.id.toLowerCase(), lang) || tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
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
