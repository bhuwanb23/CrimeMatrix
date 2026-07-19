import { Camera, FileText, Phone, MapPin, Fingerprint } from 'lucide-react'

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

export default function EvidenceTab({ caseId, evidence }) {
  return (
    <div className="evidence-tab">
      {evidence.length === 0 ? (
        <div className="similar-empty">
          <p>No evidence collected for this case</p>
        </div>
      ) : (
        <div className="evidence-grid">
          {evidence.map((item, i) => {
            const Icon = typeIcons[item.evidence_type] || typeIcons[item.type] || FileText
            const type = item.evidence_type || item.type || 'Unknown'
            const status = item.status || 'Pending'
            return (
              <div key={item.id || i} className="evidence-card">
                <div className="evidence-card-header">
                  <div className="evidence-card-icon">
                    <Icon size={16} />
                  </div>
                  <span className="evidence-card-type">{type}</span>
                  <span className={`evidence-status-badge ${status.toLowerCase().replace(' ', '-')}`}>
                    {status}
                  </span>
                </div>
                <p className="evidence-card-desc">{item.description}</p>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
