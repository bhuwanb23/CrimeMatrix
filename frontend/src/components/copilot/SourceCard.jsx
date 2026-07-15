import { FileText, User, MapPin, Camera } from 'lucide-react'

const iconMap = {
  fir: FileText,
  suspect: User,
  location: MapPin,
  evidence: Camera,
}

const colorMap = {
  fir: { bg: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' },
  suspect: { bg: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' },
  location: { bg: 'rgba(16, 185, 129, 0.1)', color: '#10b981' },
  evidence: { bg: 'rgba(139, 92, 246, 0.1)', color: '#8b5cf6' },
}

export default function SourceCard({ type, title, subtitle }) {
  const Icon = iconMap[type] || FileText
  const colors = colorMap[type] || colorMap.fir

  return (
    <div className="source-card">
      <div className="source-card-icon" style={{ background: colors.bg, color: colors.color }}>
        <Icon size={14} strokeWidth={1.8} />
      </div>
      <div className="source-card-info">
        <span className="source-card-title">{title}</span>
        <span className="source-card-subtitle">{subtitle}</span>
      </div>
    </div>
  )
}
