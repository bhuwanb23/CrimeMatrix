import { Camera, FileText, Phone, MapPin, Fingerprint, Plus } from 'lucide-react'

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
                <span className="evidence-card-type">{item.type}</span>
                <span className={`evidence-status-badge ${item.status.toLowerCase().replace(' ', '-')}`}>
                  {item.status}
                </span>
              </div>
              <p className="evidence-card-desc">{item.description}</p>
            </div>
          )
        })}
      </div>
      <button className="evidence-add-btn">
        <Plus size={14} />
        Add Evidence
      </button>
    </div>
  )
}
