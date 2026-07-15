import { FileText, Shield, Camera, AlertTriangle, Plus } from 'lucide-react'

const typeIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

const typeColors = {
  filing: '#3b82f6',
  investigation: '#8b5cf6',
  evidence: '#f59e0b',
  suspect: '#ef4444',
}

export default function TimelineTab({ timeline }) {
  return (
    <div className="timeline-tab">
      <div className="timeline-visual">
        {timeline.map((item, i) => {
          const Icon = typeIcons[item.type] || FileText
          const color = typeColors[item.type] || '#64748b'
          return (
            <div key={i} className="timeline-visual-item">
              <div className="timeline-visual-dot" style={{ background: color }}>
                <Icon size={12} color="white" />
              </div>
              <div className="timeline-visual-line" style={{ background: color + '30' }} />
              <div className="timeline-visual-content">
                <span className="timeline-visual-date">{item.date}</span>
                <p className="timeline-visual-event">{item.event}</p>
              </div>
            </div>
          )
        })}
      </div>
      <button className="timeline-add-btn">
        <Plus size={14} />
        Add Event
      </button>
    </div>
  )
}
