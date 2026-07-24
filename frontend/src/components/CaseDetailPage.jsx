import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  ArrowLeft, Clock, User, FileText, Shield, AlertTriangle,
  Camera, Bot, MapPin, Calendar, Hash, Users, Scale, BookOpen,
  Fingerprint, ShieldCheck,
} from 'lucide-react'
import SimilarCasesPanel from './similar/SimilarCasesPanel'
import FIRSuggestionsPanel from './case-detail/FIRSuggestionsPanel'
import BookmarkButton from './bookmarks/BookmarkButton'
import { getCrime, getCase } from '../services/search'
import {
  getComplainant, getVictims, getActSections, getAccused, getArrestSurrender, getChargesheetDetails,
} from '../services/lookups'

const timelineIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

/**
 * Case detail is crime-primary (GET /crimes/{id}) because Search lists crimes.
 * CaseMaster sub-resources (GET /cases/{id}/…) load when a matching cases row exists;
 * empty sections are expected when crime.id has no CaseMaster counterpart.
 */
export default function CaseDetailPage() {
  const { t } = useLanguage()
  const { id } = useParams()
  const navigate = useNavigate()
  const numericId = Number.parseInt(String(id).replace(/\D/g, ''), 10) || null

  const [caseData, setCaseData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [complainant, setComplainant] = useState(null)
  const [victims, setVictims] = useState([])
  const [actSections, setActSections] = useState([])
  const [accused, setAccused] = useState([])
  const [arrests, setArrests] = useState([])
  const [chargesheets, setChargesheets] = useState([])

  useEffect(() => {
    let cancelled = false
    async function load() {
      if (!numericId) {
        setLoading(false)
        setError('Invalid case id')
        return
      }
      setLoading(true)
      setError(null)
      try {
        const crimeRes = await getCrime(numericId)
        const crime = crimeRes?.data
        if (!crime || !crime.id) {
          if (!cancelled) {
            setCaseData(null)
            setError(crimeRes?.message || 'Crime not found')
          }
          return
        }

        let caseMaster = null
        try {
          const caseRes = await getCase(numericId)
          caseMaster = caseRes?.data || null
        } catch {
          caseMaster = null
        }

        const merged = {
          ...crime,
          ...(caseMaster || {}),
          id: crime.id,
          title: crime.title || caseMaster?.title,
          description: crime.description || caseMaster?.brief_facts,
          status: crime.status || caseMaster?.status,
          priority: crime.priority || 'medium',
          crime_no: caseMaster?.crime_no,
          case_number: caseMaster?.case_number,
          timeline: caseMaster?.timeline || [],
          suspects: caseMaster?.suspects || [],
          evidence: caseMaster?.evidence || [],
          aiInsights: caseMaster?.aiInsights || null,
        }
        if (!cancelled) setCaseData(merged)

        const loadSub = async (fn, setter, pick) => {
          try {
            const res = await fn(numericId)
            if (!cancelled) setter(pick(res))
          } catch {
            if (!cancelled) setter(pick(null))
          }
        }
        await Promise.all([
          loadSub(getComplainant, setComplainant, (r) => r?.data || null),
          loadSub(getVictims, setVictims, (r) => r?.data?.items || []),
          loadSub(getActSections, setActSections, (r) => r?.data?.items || []),
          loadSub(getAccused, setAccused, (r) => r?.data?.items || []),
          loadSub(getArrestSurrender, setArrests, (r) => r?.data?.items || []),
          loadSub(getChargesheetDetails, setChargesheets, (r) => r?.data?.items || []),
        ])
      } catch (err) {
        if (!cancelled) {
          setCaseData(null)
          setError(err?.message || 'Failed to load case')
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

  if (!caseData) {
    return (
      <div className="case-detail-empty">
        <h2>{t('Case not found')}</h2>
        <p>{error || `No case found with ID: ${id}`}</p>
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
      </div>
    )
  }

  return (
    <div className="case-detail">
      <div className="case-header">
        <button className="case-back-btn" onClick={() => navigate('/cases')}>
          <ArrowLeft size={16} /> {t('Back to Search')}
        </button>
        <div className="case-header-info">
          <h1 className="case-header-id">{caseData.crime_no || `#${caseData.id}`}</h1>
          <span className={`status-badge ${caseData.status}`}>{caseData.status}</span>
          <BookmarkButton entityType="case" entityId={numericId} />
        </div>
        <p className="case-header-title">{caseData.title}</p>
      </div>

      <div className="case-grid">
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
              <span className="case-info-value">{caseData.type || caseData.crime_type || (caseData.crime_type_id ? `#${caseData.crime_type_id}` : '—')}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('District')}</span>
              <span className="case-info-value">{caseData.district || (caseData.district_id ? `#${caseData.district_id}` : '—')}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Priority')}</span>
              <span className={`case-info-value priority-${(caseData.priority || 'medium').toLowerCase()}`}>{caseData.priority || 'Medium'}</span>
            </div>
            <div className="case-info-item">
              <span className="case-info-label">{t('Officer')}</span>
              <span className="case-info-value">{caseData.officer || `Officer #${caseData.officer_id || caseData.reported_by || '—'}`}</span>
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

        <div className="case-card">
          <h3 className="case-card-title">
            <Calendar size={16} /> {t('Incident Details')}
          </h3>
          <div className="case-info-grid">
            <div className="case-info-item">
              <span className="case-info-label">{t('Incident From')}</span>
              <span className="case-info-value">
                {caseData.incident_from_date || caseData.occurred_at
                  ? new Date(caseData.incident_from_date || caseData.occurred_at).toLocaleString()
                  : '—'}
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
                  {Number(caseData.latitude).toFixed(4)}, {Number(caseData.longitude).toFixed(4)}
                </span>
              </div>
            )}
          </div>
        </div>

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

        <div className="case-card">
          <h3 className="case-card-title">
            <Fingerprint size={16} /> Accused
          </h3>
          {accused.length > 0 ? (
            <div className="space-y-2">
              {accused.map((a, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-slate-900">{a.name}</span>
                    {a.person_id && (
                      <span className="text-[10px] font-mono bg-slate-200 text-slate-600 px-1.5 py-0.5 rounded">{a.person_id}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 text-[11px] text-slate-500">
                    {a.age_year && <span>Age: {a.age_year}</span>}
                    {a.gender_name && <span>Gender: {a.gender_name}</span>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="case-empty-text">No accused recorded</p>
          )}
        </div>

        <div className="case-card">
          <h3 className="case-card-title">
            <ShieldCheck size={16} /> Arrest / Surrender
          </h3>
          {arrests.length > 0 ? (
            <div className="space-y-2">
              {arrests.map((a, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-slate-900">{a.type_name || 'Unknown'}</span>
                    <div className="flex items-center gap-2">
                      {a.is_accused && (
                        <span className="text-[10px] font-semibold px-2 py-0.5 bg-red-100 text-red-700 rounded-full">Primary</span>
                      )}
                      {a.is_complainant_accused && (
                        <span className="text-[10px] font-semibold px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full">Complainant-Accused</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-[11px] text-slate-500">
                    {a.date && <span>{new Date(a.date).toLocaleDateString()}</span>}
                    {a.accused_name && <span>Accused: {a.accused_name}</span>}
                    {a.state_name && <span>State: {a.state_name}</span>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="case-empty-text">No arrest/surrender records</p>
          )}
        </div>

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

        <div className="case-card">
          <h3 className="case-card-title">
            <FileText size={16} /> Chargesheet Details
          </h3>
          {chargesheets.length > 0 ? (
            <div className="space-y-2">
              {chargesheets.map((cs, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-slate-900">
                      {cs.cs_type === 'A' ? 'Chargesheet' : cs.cs_type === 'B' ? 'False Case' : cs.cs_type === 'C' ? 'Undetected' : cs.cs_type || 'Type not set'}
                    </span>
                    {cs.cs_date && (
                      <span className="text-[10px] text-slate-400">{new Date(cs.cs_date).toLocaleDateString()}</span>
                    )}
                  </div>
                  {cs.officer_name && (
                    <div className="text-[11px] text-slate-500">IO: {cs.officer_name}</div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="case-empty-text">No chargesheet filed</p>
          )}
        </div>

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
                    <span className={`suspect-status ${(suspect.status || '').toLowerCase().replace(' ', '-')}`}>
                      {suspect.status}
                    </span>
                  </div>
                  <div className="suspect-details">
                    {suspect.age > 0 && <span>Age: {suspect.age}</span>}
                    {suspect.relation && <span>Relation: {suspect.relation}</span>}
                  </div>
                  {suspect.notes && <p className="suspect-notes">{suspect.notes}</p>}
                </div>
              ))}
            </div>
          )}
        </div>

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
                  {item.status && (
                    <span className={`evidence-status ${String(item.status).toLowerCase().replace(' ', '-')}`}>
                      {item.status}
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="case-card full-width">
          <h3 className="case-card-title">
            <Bot size={16} /> {t('AI Insights')}
          </h3>
          <div className="case-ai-insights">
            <p>{caseData.aiInsights || 'No AI insights available'}</p>
          </div>
        </div>

        <div className="case-card full-width">
          <SimilarCasesPanel caseId={numericId} />
        </div>

        <div className="case-card full-width">
          <FIRSuggestionsPanel firId={numericId} />
        </div>
      </div>
    </div>
  )
}
