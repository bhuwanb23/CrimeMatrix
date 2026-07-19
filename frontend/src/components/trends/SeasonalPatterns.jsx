import { Calendar } from 'lucide-react'

export default function SeasonalPatterns({ patterns }) {
  if (!patterns) return null

  const { by_hour = [], by_day_of_week = [], by_month = [] } = patterns

  function MiniBarChart({ data, label, valueKey = 'count', labelKey }) {
    const max = Math.max(...data.map(d => d[valueKey] || 0), 1)
    return (
      <div className="seasonal-chart">
        <h4>{label}</h4>
        <div className="seasonal-bars">
          {data.map((d, i) => (
            <div key={i} className="seasonal-bar-col">
              <div className="seasonal-bar-wrapper">
                <div
                  className="seasonal-bar"
                  style={{ height: `${((d[valueKey] || 0) / max) * 100}%` }}
                />
              </div>
              <span className="seasonal-bar-label">{d[labelKey]}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="trend-chart-widget">
      <div className="intel-widget-header">
        <h3><Calendar size={14} /> Seasonal Patterns</h3>
      </div>

      <div className="seasonal-grid">
        {by_hour.length > 0 && (
          <MiniBarChart data={by_hour} label="By Hour" labelKey="hour" />
        )}
        {by_day_of_week.length > 0 && (
          <MiniBarChart data={by_day_of_week} label="By Day" labelKey="day" />
        )}
        {by_month.length > 0 && (
          <MiniBarChart data={by_month} label="By Month" labelKey="month" />
        )}
      </div>
    </div>
  )
}
