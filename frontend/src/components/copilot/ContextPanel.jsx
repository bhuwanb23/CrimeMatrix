import {
  FileText, Download, BookmarkPlus, Share2, X,
} from 'lucide-react'
import SourceCard from './SourceCard'

const referencedSources = [
  { type: 'fir', title: 'FIR #4521/2026', subtitle: 'Theft — Malleshwaram, Bengaluru' },
  { type: 'suspect', title: 'Ravi Kumar', subtitle: 'Linked to 3 open cases' },
  { type: 'evidence', title: 'CCTV Footage — Main Road', subtitle: 'Captured at 2:15 AM' },
  { type: 'location', title: 'Malleshwaram, Bengaluru', subtitle: 'Crime hotspot zone' },
]

const actions = [
  { icon: FileText, label: 'Generate Report', color: '#3b82f6' },
  { icon: Download, label: 'Export Conversation', color: '#10b981' },
  { icon: BookmarkPlus, label: 'Save to Case', color: '#f59e0b' },
  { icon: Share2, label: 'Share with Team', color: '#8b5cf6' },
]

const relatedCases = [
  { id: 'FIR #4489', title: 'Robbery — Indiranagar', status: 'active' },
  { id: 'FIR #4501', title: 'Theft — Koramangala', status: 'pending' },
  { id: 'FIR #4515', title: 'Cyber fraud — Electronic City', status: 'active' },
]

export default function ContextPanel({ onClose }) {
  return (
    <div className="slide-panel-inner">
      <div className="slide-panel-header">
        <h2 className="slide-panel-title">Context</h2>
        <button className="slide-panel-close" onClick={onClose} aria-label="Close">
          <X size={18} strokeWidth={1.8} />
        </button>
      </div>

      <div className="slide-panel-body">
        <section className="context-section">
          <h3 className="context-section-title">Referenced Sources</h3>
          <div className="context-sources">
            {referencedSources.map((src, i) => (
              <SourceCard key={i} {...src} />
            ))}
          </div>
        </section>

        <section className="context-section">
          <h3 className="context-section-title">Actions</h3>
          <div className="context-actions">
            {actions.map((action, i) => (
              <button key={i} className="context-action-btn">
                <div className="context-action-icon" style={{ background: action.color + '12', color: action.color }}>
                  <action.icon size={14} strokeWidth={1.8} />
                </div>
                <span className="context-action-label">{action.label}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="context-section">
          <h3 className="context-section-title">Related Cases</h3>
          <div className="context-cases">
            {relatedCases.map((c, i) => (
              <div key={i} className="context-case-card">
                <div className="context-case-header">
                  <span className="context-case-id">{c.id}</span>
                  <span className={`context-case-status ${c.status}`}>{c.status}</span>
                </div>
                <p className="context-case-title">{c.title}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
