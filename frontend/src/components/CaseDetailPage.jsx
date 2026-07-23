import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getCaseById } from './search/caseData'
import {
  ArrowLeft, Clock, User, FileText, Shield, AlertTriangle,
  Camera, Bot, MapPin, Calendar, Hash,
} from 'lucide-react'
import SimilarCasesPanel from './similar/SimilarCasesPanel'
import FIRSuggestionsPanel from './case-detail/FIRSuggestionsPanel'
import BookmarkButton from './bookmarks/BookmarkButton'

const timelineIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

export default function CaseDetailPage() {
  const { t } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const caseData = getCaseById(id)

  if (!caseData) {
    return (
      <div className="case-detail-empty">
        <h2>{t('Case not found')}</h2>
        <p>No case found with ID: {id}</p>
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
      </div>
    )
  }

  return (
    <div className="case-detail">
      {/* Header */}
      <div className="case-header">
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
        <div className="case-header-info">
          <h1 className="case-header-id">{caseData.crime_no || caseData.id}</h1>
          <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
          <BookmarkButton entityType="case" entityId={caseData.id} />
        </div>
        <p className="case-header-title">{caseData.title}</p>
      </div>

      {/* Main Grid */}
      <div className="case-grid">
        {/* Case Information */}
        <div className="case-card">
          <h3 className="case-card-title">{t('Case Information')}</h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">{t('Crime No')}</span>
              <span className="case-info-value font-mono text-xs">{caseData.crime_no || '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Case No')}</span>
              <span className="case-info-value">{caseData.case_number || caseData.id}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Type')}</span>
              <span className="case-info-value">{caseData.type || caseData.crime_type}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('District')}</span>
              <span className="case-info-value">{caseData.district}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Priority')}</span>
              <span className={`case-info-value priority-${(caseData.priority || 'medium').toLowerCase()}`}>{caseData.priority || 'Medium'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Officer')}</span>
              <span className="case-info-value">{caseData.officer || `Officer #${caseData.officer_id || '—'}`}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Date Filed')}</span>
              <span className="case-info-value">{caseData.date || (caseData.created_at ? new Date(caseData.created_at).toLocaleDateString() : '—')}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Status')}</span>
              <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
            </div>
          </div>
        </div>

        {/* Incident Details (CaseMaster fields) */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Calendar size={16} /> {t('Incident Details')}
          </h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">{t('Incident From')}</span>
              <span className="case-info-value">
                {caseData.incident_from_date ? new Date(caseData.incident_from_date).toLocaleString() : '—'}
              </span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Incident To')}</span>
              <span className="case-info-value">
                {caseData.incident_to_date ? new Date(caseData.incident_to_date).toLocaleString() : '—'}
              </span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Info Received at PS')}</span>
              <span className="case-info-value">
                {caseData.info_received_ps_date ? new Date(caseData.info_received_ps_date).toLocaleString() : '—'}
              </span>
            </div>
            {caseData.latitude && caseData.longitude && (
              <div className="case-info-item">
                <span className="case-info-label">{t('Location')}</span>
                <span className="case-info-value flex items-center gap-1">
                  <MapPin size={12} />
                  {caseData.latitude.toFixed(4)}, {caseData.longitude.toFixed(4)}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Classification (Lookup references) */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Hash size={16} /> {t('Classification')}
          </h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">{t('Case Category')}</span>
              <span className="case-info-value">{caseData.case_category_id ? `#${caseData.case_category_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Gravity Offence')}</span>
              <span className="case-info-value">{caseData.gravity_offence_id ? `#${caseData.gravity_offence_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Crime Head')}</span>
              <span className="case-info-value">{caseData.crime_major_head_id ? `#${caseData.crime_major_head_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Court')}</span>
              <span className="case-info-value">{caseData.court_id ? `#${caseData.court_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Station')}</span>
              <span className="case-info-value">{caseData.police_station_id ? `#${caseData.police_station_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Case Status (Master)')}</span>
              <span className="case-info-value">{caseData.case_status_id ? `#${caseData.case_status_id}` : '—'}</span>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Clock size={16} /> {t('Timeline')}
          </h3>
          <div className="case-timeline">
            {caseData.timeline && caseData.timeline.map((item, i) => {
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
            {(!caseData.timeline || caseData.timeline.length === 0) && (
              <p className="case-empty-text">{t('No timeline events')}</p>
            )}
          </div>
        </div>

        {/* Description / Brief Facts */}
        <div className="case-card full-width">
          <h3 className="case-card-title">{t('Description')}</h3>
          <p className="case-description">{caseData.description || 'No description available'}</p>
          {caseData.brief_facts && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold text-slate-500 uppercase mb-1">{t('Brief Facts')}</h4>
              <p className="case-description text-slate-600">{caseData.brief_facts}</p>
            </div>
          )}
        </div>

        {/* Suspects */}
        <div className="case-card">
          <h3 className="case-card-title">
            <User size={16} /> {t('Suspects')}
          </h3>
          {(!caseData.suspects || caseData.suspects.length === 0) ? (
            <p className="case-empty-text">{t('No suspects identified')}</p>
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
                    {suspect.age > 0 && <span>Age: {suspect.age}</span>}
                    <span>Relation: {suspect.relation}</span>
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
            <Camera size={16} /> {t('Evidence')}
          </h3>
          {(!caseData.evidence || caseData.evidence.length === 0) ? (
            <p className="case-empty-text">{t('No evidence collected')}</p>
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
            <Bot size={16} /> {t('AI Insights')}
          </h3>
          <div className="case-ai-insights">
            <p>{caseData.aiInsights || 'No AI insights available'}</p>
          </div>
        </div>

        {/* Similar Cases */}
        <div className="case-card full-width">
          <SimilarCasesPanel caseId={caseData.id} />
        </div>

        {/* FIR Intelligence Suggestions */}
        <div className="case-card full-width">
          <FIRSuggestionsPanel firId={caseData.id} />
        </div>
      </div>
    </div>
  )
}
