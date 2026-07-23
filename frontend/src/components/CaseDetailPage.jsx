import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getCaseById } from './search/caseData'
import {
  ArrowLeft, Clock, User, FileText, Shield, AlertTriangle,
  Camera, Bot, MapPin, Calendar, Hash, Users, Scale, BookOpen,
} from 'lucide-react'
import SimilarCasesPanel from './similar/SimilarCasesPanel'
import FIRSuggestionsPanel from './case-detail/FIRSuggestionsPanel'
import BookmarkButton from './bookmarks/BookmarkButton'
import { getComplainant, getVictims, getActSections } from '../services/lookups'

const timelineIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

export default function CaseDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [complainant, setComplainant] = useState(null)
  const [victims, setVictims] = useState([])
  const [actSections, setActSections] = useState([])
  const caseData = getCaseById(id)

  useEffect(() => {
    if (id) {
      const numericId = parseInt(id.replace(/\D/g, ''), 10)
      if (numericId) {
        getComplainant(numericId).then(res => setComplainant(res?.data || null)).catch(() => {})
        getVictims(numericId).then(res => setVictims(res?.data?.items || [])).catch(() => {})
        getActSections(numericId).then(res => setActSections(res?.data?.items || [])).catch(() => {})
      }
    }
  }, [id])

  if (!caseData) {
    return (
      <div className="case-detail-empty">
        <h2>Case not found</h2>
        <p>No case found with ID: {id}</p>
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> Back to Search
        </button>
      </div>
    )
  }

  return (
    <div className="case-detail">
      {/* Header */}
      <div className="case-header">
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> Back to Search
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
          <h3 className="case-card-title">Case Information</h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">Crime No</span>
              <span className="case-info-value font-mono text-xs">{caseData.crime_no || '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Case No</span>
              <span className="case-info-value">{caseData.case_number || caseData.id}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Type</span>
              <span className="case-info-value">{caseData.type || caseData.crime_type}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">District</span>
              <span className="case-info-value">{caseData.district}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Priority</span>
              <span className={`case-info-value priority-${(caseData.priority || 'medium').toLowerCase()}`}>{caseData.priority || 'Medium'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Officer</span>
              <span className="case-info-value">{caseData.officer || `Officer #${caseData.officer_id || '—'}`}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Date Filed</span>
              <span className="case-info-value">{caseData.date || (caseData.created_at ? new Date(caseData.created_at).toLocaleDateString() : '—')}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Status</span>
              <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
            </div>
          </div>
        </div>

        {/* Incident Details (CaseMaster fields) */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Calendar size={16} /> Incident Details
          </h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">Incident From</span>
              <span className="case-info-value">
                {caseData.incident_from_date ? new Date(caseData.incident_from_date).toLocaleString() : '—'}
              </span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Incident To</span>
              <span className="case-info-value">
                {caseData.incident_to_date ? new Date(caseData.incident_to_date).toLocaleString() : '—'}
              </span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Info Received at PS</span>
              <span className="case-info-value">
                {caseData.info_received_ps_date ? new Date(caseData.info_received_ps_date).toLocaleString() : '—'}
              </span>
            </div>
            {caseData.latitude && caseData.longitude && (
              <div className="case-info-item">
                <span className="case-info-label">Location</span>
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
            <Hash size={16} /> Classification
          </h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">Case Category</span>
              <span className="case-info-value">{caseData.case_category_id ? `#${caseData.case_category_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Gravity Offence</span>
              <span className="case-info-value">{caseData.gravity_offence_id ? `#${caseData.gravity_offence_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Crime Head</span>
              <span className="case-info-value">{caseData.crime_major_head_id ? `#${caseData.crime_major_head_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Court</span>
              <span className="case-info-value">{caseData.court_id ? `#${caseData.court_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Station</span>
              <span className="case-info-value">{caseData.police_station_id ? `#${caseData.police_station_id}` : '—'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">Case Status (Master)</span>
              <span className="case-info-value">{caseData.case_status_id ? `#${caseData.case_status_id}` : '—'}</span>
            </div>
          </div>
        </div>

        {/* Complainant Details */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Users size={16} /> Complainant Details
          </h3>
          {complainant ? (
            <div className="case-info-grid">
              <div className="case-info-item">
                <span className="case-info-label">Name</span>
                <span className="case-info-value">{complainant.name}</span>
              </div>
              <div className="case-info-item">
                <span className="case-info-label">Age</span>
                <span className="case-info-value">{complainant.age_year ? `${complainant.age_year} years` : '—'}</span>
              </div>
              <div className="case-info-item">
                <span className="case-info-label">Gender</span>
                <span className="case-info-value">{complainant.gender_name || '—'}</span>
              </div>
              <div className="case-info-item">
                <span className="case-info-label">Occupation</span>
                <span className="case-info-value">{complainant.occupation_name || '—'}</span>
              </div>
              <div className="case-info-item">
                <span className="case-info-label">Religion</span>
                <span className="case-info-value">{complainant.religion_name || '—'}</span>
              </div>
              <div className="case-info-item">
                <span className="case-info-label">Caste</span>
                <span className="case-info-value">{complainant.caste_name || '—'}</span>
              </div>
            </div>
          ) : (
            <p className="case-empty-text">No complainant details recorded</p>
          )}
        </div>

        {/* Victims */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Users size={16} /> Victims
          </h3>
          {victims.length > 0 ? (
            <div className="space-y-2">
              {victims.map((v, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-slate-900">{v.name}</span>
                    {v.is_police && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full">Police</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 text-[11px] text-slate-500">
                    {v.age_year && <span>Age: {v.age_year}</span>}
                    {v.gender_name && <span>Gender: {v.gender_name}</span>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="case-empty-text">No victims recorded</p>
          )}
        </div>

        {/* Legal Sections */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Scale size={16} /> Legal Sections
          </h3>
          {actSections.length > 0 ? (
            <div className="space-y-2">
              {actSections.map((a, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="flex items-center gap-2 mb-1">
                    <BookOpen size={12} className="text-slate-400" />
                    <span className="text-sm font-semibold text-slate-900">{a.act_name || `Act #${a.act_id}`}</span>
                  </div>
                  <div className="text-xs text-slate-500">
                    <span className="font-medium">Section {a.section_code || `#${a.section_id}`}</span>
                    {a.section_name && <span className="text-slate-400 ml-1">— {a.section_name}</span>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="case-empty-text">No legal sections recorded</p>
          )}
        </div>

        {/* Timeline */}
        <div className="case-card">
          <h3 className="case-card-title">
            <Clock size={16} /> Timeline
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
              <p className="case-empty-text">No timeline events</p>
            )}
          </div>
        </div>

        {/* Description / Brief Facts */}
        <div className="case-card full-width">
          <h3 className="case-card-title">Description</h3>
          <p className="case-description">{caseData.description || 'No description available'}</p>
          {caseData.brief_facts && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold text-slate-500 uppercase mb-1">Brief Facts</h4>
              <p className="case-description text-slate-600">{caseData.brief_facts}</p>
            </div>
          )}
        </div>

        {/* Suspects */}
        <div className="case-card">
          <h3 className="case-card-title">
            <User size={16} /> Suspects
          </h3>
          {(!caseData.suspects || caseData.suspects.length === 0) ? (
            <p className="case-empty-text">No suspects identified</p>
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
            <Camera size={16} /> Evidence
          </h3>
          {(!caseData.evidence || caseData.evidence.length === 0) ? (
            <p className="case-empty-text">No evidence collected</p>
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
            <Bot size={16} /> AI Insights
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
