import { useParams, useNavigate } from 'react-router-dom'
import { getCaseById } from './search/caseData'
import {
  ArrowLeft, Clock, User, FileText, Shield, AlertTriangle,
  Camera, Phone, MapPin, Bot, CheckCircle2, ExternalLink,
} from 'lucide-react'

const timelineIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}
import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function CaseDetailPage() {
  const { lang } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const caseData = getCaseById(id)

  if (!caseData) {
    return (
      <div className="case-detail-empty">
        <h2>{t('case_not_found', lang)}</h2>
        <p>{t('no_case_found_with_id', lang)}: {id}</p>
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('back_to_search', lang)}
        </button>
      </div>
    )
  }

  return (
    <div className="case-detail">
      {/* Header */}
      <div className="case-header">
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('back_to_search', lang)}
        </button>
        <div className="case-header-info">
          <h1 className="case-header-id">{caseData.id}</h1>
          <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
        </div>
        <p className="case-header-title">{caseData.title}</p>
      </div>

      {/* Main Grid */}
      <div className="case-grid">
        {/* Case Info */}
        <div className="case-card">
          <h3 className="case-card-title">{t('case_information', lang)}</h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">{t('type', lang)}</span>
              <span className="case-info-value">{caseData.type}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('district', lang)}</span>
              <span className="case-info-value">{caseData.district}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('priority', lang)}</span>
              <span className={`case-info-value priority-${caseData.priority.toLowerCase()}`}>{caseData.priority}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('officer', lang)}</span>
              <span className="case-info-value">{caseData.officer}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('date_filed', lang)}</span>
              <span className="case-info-value">{caseData.date}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('status', lang)}</span>
              <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Clock size={16} /> {t('timeline', lang)}
          </h3>
          <div className="case-timeline">
            {caseData.timeline.map((item, i) => {
              const Icon = timelineIcons[item.type] || FileText
              return (
                <div key={i} className="timeline-item">
                  <div className="timeline-dot">
                    <Icon size={14} />
                  </div>
                  <div className="timeline-content">
                    <span className="timeline-date">{item.date}</span>
                    <p className="timeline-event">{item.event}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Description */}
        <div className="case-card full-width">
          <h3 className="case-card-title">{t('description', lang)}</h3>
          <p className="case-description">{caseData.description}</p>
        </div>

        {/* Suspects */}
        <div className="case-card">
          <h3 className="case-card-title">
            <User size={16} /> {t('suspects', lang)}
          </h3>
          {caseData.suspects.length === 0 ? (
            <p className="case-empty-text">{t('no_suspects_identified', lang)}</p>
          ) : (
            <div className="case-suspects">
              {caseData.suspects.map((suspect, i) => (
                <div key={i} className="suspect-card">
                  <div className="suspect-header">
                    <span className="suspect-name">{suspect.name}</span>
                    <span className={`suspect-status ${suspect.status.toLowerCase().replace(' ', '-')}`}>
                      {suspect.status}
                    </span>
                  </div>
                  <div className="suspect-details">
                    {suspect.age > 0 && <span>{t('age', lang)}: {suspect.age}</span>}
                    <span>{t('relation', lang)}: {suspect.relation}</span>
                  </div>
                  <p className="suspect-notes">{suspect.notes}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Evidence */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Camera size={16} /> {t('evidence', lang)}
          </h3>
          {caseData.evidence.length === 0 ? (
            <p className="case-empty-text">{t('no_evidence_collected', lang)}</p>
          ) : (
            <div className="case-evidence">
              {caseData.evidence.map((item, i) => (
                <div key={i} className="evidence-item">
                  <div className="evidence-type">{item.type}</div>
                  <p className="evidence-desc">{item.description}</p>
                  <span className={`evidence-status ${item.status.toLowerCase().replace(' ', '-')}`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* AI Insights */}
        <div className="case-card full-width">
          <h3 className="case-card-title">
            <Bot size={16} /> {t('ai_insights', lang)}
          </h3>
          <div className="case-ai-insights">
            <p>{caseData.aiInsights}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
