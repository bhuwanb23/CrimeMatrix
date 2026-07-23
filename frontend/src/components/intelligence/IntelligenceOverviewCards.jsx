import { AlertTriangle, Users, Shield, FileText, TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function IntelligenceOverviewCards({ overview }) {
  const { t } = useLanguage()
  if (!overview) return null

  const cardConfig = [
    { key: 'total_crimes', label: t('Total Crimes'), icon: FileText, color: '#f59e0b' },
    { key: 'open_crimes', label: t('Open Cases'), icon: AlertTriangle, color: '#ef4444' },
    { key: 'resolution_rate', label: t('Resolution Rate'), icon: TrendingUp, color: '#10b981', suffix: '%' },
    { key: 'active_investigations', label: t('Active Investigations'), icon: Shield, color: '#3b82f6' },
    { key: 'active_criminals', label: t('Criminals at Large'), icon: Users, color: '#8b5cf6' },
  ]

  return (
    <div className="intel-overview-cards">
      {cardConfig.map((card) => {
        const value = overview[card.key] || 0
        const Icon = card.icon
        return (
          <div key={card.key} className="intel-stat-card">
            <div className="intel-stat-icon" style={{ color: card.color }}>
              <Icon size={18} />
            </div>
            <div className="intel-stat-info">
              <span className="intel-stat-label">{card.label}</span>
              <span className="intel-stat-value">{value}{card.suffix || ''}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

