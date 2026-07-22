import { AlertTriangle, Users, Shield, FileText, TrendingUp } from 'lucide-react'

const cardConfig = [
  { key: 'total_crimes', label: 'Total Crimes', icon: FileText, color: '#f59e0b' },
  { key: 'open_crimes', label: 'Open Cases', icon: AlertTriangle, color: '#ef4444' },
  { key: 'resolution_rate', label: 'Resolution Rate', icon: TrendingUp, color: '#10b981', suffix: '%' },
  { key: 'active_investigations', label: 'Active Investigations', icon: Shield, color: '#3b82f6' },
  { key: 'active_criminals', label: 'Criminals at Large', icon: Users, color: '#8b5cf6' },
]

export default function IntelligenceOverviewCards({ overview }) {
  if (!overview) return null

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
