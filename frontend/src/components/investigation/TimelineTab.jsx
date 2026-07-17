import { FileText, Shield, Camera, AlertTriangle, Plus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText } from '../../utils/translate'

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
  const { lang } = useLanguage()

  // Translate timeline dates if month matches
  const translateDate = (date) => {
    // E.g., "Jul 15, 2026". We can keep as is, or localize month. Let's translate month names if needed
    const parts = date.split(' ')
    if (parts.length > 0) {
      const month = parts[0]
      const translatedMonth = t(month.toLowerCase(), lang)
      if (translatedMonth !== month.toLowerCase()) {
        return date.replace(month, translatedMonth)
      }
    }
    return date
  }

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
                <span className="timeline-visual-date">{translateDate(item.date)}</span>
                <p className="timeline-visual-event">{translateText(item.event, lang)}</p>
              </div>
            </div>
          )
        })}
      </div>
      <button className="timeline-add-btn">
        <Plus size={14} />
        {t('add_event', lang)}
      </button>
    </div>
  )
}
