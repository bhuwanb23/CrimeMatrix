import { Users, AlertTriangle, Eye, UserX } from 'lucide-react'

export default function IntelligenceCriminalActivity({ activity }) {
  if (!activity) return null

  const stats = [
    { label: 'Active Criminals', value: activity.active_criminals || 0, icon: Users, color: '#ef4444' },
    { label: 'High Risk', value: activity.high_risk_offenders || 0, icon: AlertTriangle, color: '#f59e0b' },
    { label: 'Total Victims', value: activity.total_victims || 0, icon: Eye, color: '#3b82f6' },
    { label: 'Witnesses', value: activity.total_witnesses || 0, icon: UserX, color: '#10b981' },
  ]

  return (
    <div className="intel-criminal-widget">
      <div className="intel-widget-header">
        <h3><Users size={14} /> Criminal Activity</h3>
      </div>

      <div className="intel-criminal-grid">
        {stats.map((stat, i) => {
          const Icon = stat.icon
          return (
            <div key={i} className="intel-criminal-stat">
              <div className="intel-criminal-icon" style={{ color: stat.color }}>
                <Icon size={16} />
              </div>
              <div className="intel-criminal-info">
                <span className="intel-criminal-value">{stat.value}</span>
                <span className="intel-criminal-label">{stat.label}</span>
              </div>
            </div>
          )
        })}
      </div>

      {activity.high_risk_offenders > 0 && (
        <div className="intel-criminal-alert">
          <AlertTriangle size={12} />
          <span>{activity.high_risk_offenders} high-risk offenders require monitoring</span>
        </div>
      )}
    </div>
  )
}
