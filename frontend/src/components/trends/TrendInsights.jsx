import { TrendingUp, TrendingDown, Minus, AlertTriangle, Lightbulb } from 'lucide-react'

export default function TrendInsights({ summary, seasonal }) {
  const insights = []

  if (summary) {
    if (summary.direction === 'up' && summary.change_pct > 10) {
      insights.push({
        type: 'spike',
        severity: 'high',
        icon: TrendingUp,
        color: '#ef4444',
        message: `Crime rate spiked ${Math.round(summary.change_pct)}% — requires immediate attention`,
      })
    } else if (summary.direction === 'down') {
      insights.push({
        type: 'decline',
        severity: 'positive',
        icon: TrendingDown,
        color: '#10b981',
        message: `Crime rate declined ${Math.abs(Math.round(summary.change_pct))}% — positive trend`,
      })
    }

    if (summary.peak && summary.peak.count > 0) {
      insights.push({
        type: 'peak',
        severity: 'info',
        icon: AlertTriangle,
        color: '#f59e0b',
        message: `Peak crime day: ${summary.peak.date} with ${summary.peak.count} crimes`,
      })
    }
  }

  if (seasonal) {
    const { by_hour = [], by_day_of_week = [] } = seasonal

    if (by_hour.length > 0) {
      const peakHour = by_hour.reduce((max, h) => (h.count > max.count ? h : max), by_hour[0])
      if (peakHour) {
        insights.push({
          type: 'hourly',
          severity: 'info',
          icon: Lightbulb,
          color: '#3b82f6',
          message: `Most crimes occur at ${peakHour.hour}:00 — consider increased patrols`,
        })
      }
    }

    if (by_day_of_week.length > 0) {
      const peakDay = by_day_of_week.reduce((max, d) => (d.count > max.count ? d : max), by_day_of_week[0])
      if (peakDay) {
        insights.push({
          type: 'daily',
          severity: 'info',
          icon: Lightbulb,
          color: '#8b5cf6',
          message: `${peakDay.day} has highest crime activity — schedule extra duty`,
        })
      }
    }
  }

  if (insights.length === 0) {
    insights.push({
      type: 'stable',
      severity: 'info',
      icon: Minus,
      color: 'var(--text-muted)',
      message: 'Crime trends are stable — no significant patterns detected',
    })
  }

  return (
    <div className="trend-chart-widget">
      <div className="intel-widget-header">
        <h3><TrendingUp size={14} /> Trend Insights</h3>
      </div>

      <div className="trend-insights-list">
        {insights.map((insight, i) => {
          const Icon = insight.icon
          return (
            <div key={i} className="trend-insight-item">
              <div className="trend-insight-icon" style={{ color: insight.color }}>
                <Icon size={14} />
              </div>
              <span className="trend-insight-msg">{insight.message}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
