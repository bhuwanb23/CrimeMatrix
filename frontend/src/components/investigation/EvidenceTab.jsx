import { Camera, FileText, Phone, MapPin, Fingerprint, Plus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText } from '../../utils/translate'

const typeIcons = {
  CCTV: Camera,
  'Phone Records': Phone,
  Fingerprint: Fingerprint,
  Witness: FileText,
  Digital: FileText,
  Financial: FileText,
  'IP Address': MapPin,
  Physical: Fingerprint,
}

export default function EvidenceTab({ evidence }) {
  const { lang } = useLanguage()

  // Translate evidence types
  const translateEvidenceType = (type) => {
    const key = type.toLowerCase().replace(' ', '_')
    const val = t(key, lang)
    return val === key ? type : val
  }

  // Translate evidence statuses
  const translateEvidenceStatus = (status) => {
    const key = status.toLowerCase().replace(' ', '_')
    const val = t(key, lang)
    return val === key ? status : val
  }

  return (
    <div className="evidence-tab">
      <div className="evidence-grid">
        {evidence.map((item, i) => {
          const Icon = typeIcons[item.type] || FileText
          return (
            <div key={i} className="evidence-card">
              <div className="evidence-card-header">
                <div className="evidence-card-icon">
                  <Icon size={16} />
                </div>
                <span className="evidence-card-type">{translateEvidenceType(item.type)}</span>
                <span className={`evidence-status-badge ${item.status.toLowerCase().replace(' ', '-')}`}>
                  {translateEvidenceStatus(item.status)}
                </span>
              </div>
              <p className="evidence-card-desc">{translateText(item.description, lang)}</p>
            </div>
          )
        })}
      </div>
      <button className="evidence-add-btn">
        <Plus size={14} />
        {t('add_evidence', lang)}
      </button>
    </div>
  )
}
