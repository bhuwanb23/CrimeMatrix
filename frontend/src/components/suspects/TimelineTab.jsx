import { AlertCircle, CheckCircle, Search, Calendar } from 'lucide-react'

const typeConfig = {
  arrest: { icon: AlertCircle, color: '#ef4444', label: 'Arrest' },
  release: { icon: CheckCircle, color: '#10b981', label: 'Release' },
  incident: { icon: AlertCircle, color: '#f59e0b', label: 'Incident' },
  investigation: { icon: Search, color: '#3b82f6', label: 'Investigation' },
}

import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function TimelineTab({ suspect }) {
  const { lang } = useLanguage()
  return (
    <div className="timeline-tab">
      <div className="timeline-visual">
        {suspect.timeline.map((item, i) => {
          const config = typeConfig[item.type] || typeConfig.incident
          const Icon = config.icon
          return (
            <div key={i} className="timeline-visual-item">
              <div className="timeline-visual-dot" style={{ background: config.color }}>
                <Icon size={12} color="white" />
              </div>
              <div className="timeline-visual-line" style={{ background: config.color + '30' }} />
              <div className="timeline-visual-content">
                <div className="timeline-visual-header">
                  <span className="timeline-visual-date">{item.date}</span>
                  <span className="timeline-visual-type" style={{ color: config.color }}>{t(config.label.toLowerCase().replace(/ /g, '_'), lang) || config.label}</span>
                </div>
                <p className="timeline-visual-event">{item.event}</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
