import { Users, ExternalLink } from 'lucide-react'

const statusColors = {
  'Arrested': '#10b981',
  'At large': '#ef4444',
  'Under investigation': '#f59e0b',
  'Under watch': '#8b5cf6',
  'Victim': '#64748b',
  'Unknown': '#94a3b8',
}

import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function AssociatesTab({ suspect }) {
  const { lang } = useLanguage()
  return (
    <div className="associates-tab">
      <div className="associates-header">
        <Users size={18} />
        <h3>{t('known_associates', lang) || "Known Associates"} ({suspect.associates.length})</h3>
      </div>

      <div className="associates-grid">
        {suspect.associates.map((assoc, i) => (
          <div key={i} className="associate-card">
            <div className="associate-avatar" style={{ background: statusColors[assoc.status] + '20', color: statusColors[assoc.status] }}>
              {assoc.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="associate-info">
              <span className="associate-name">{assoc.name}</span>
              <span className="associate-relation">{assoc.relation}</span>
            </div>
            <div className="associate-meta">
              <span className="associate-cases">{assoc.cases} {t('cases', lang) || "cases"}</span>
              <span className="associate-status" style={{ color: statusColors[assoc.status] }}>
                {assoc.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="associates-network">
        <h4>{t('network_summary', lang) || "Network Summary"}</h4>
        <p className="network-text">
          {suspect.name} is connected to {suspect.associates.length} known associates across{' '}
          {new Set(suspect.associates.map(a => a.relation)).size} different roles.
          {suspect.associates.filter(a => a.status === 'At large').length > 0 && (
            <span className="network-warning">
              {' '}{suspect.associates.filter(a => a.status === 'At large').length} associates are currently at large.
            </span>
          )}
        </p>
      </div>
    </div>
  )
}
