import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react'

export default function IntelligenceTrendWidget({ trends }) {
  if (!trends) return null

  const daily = trends.daily || []
  const direction = trends.direction || 'stable'
  const changePct = trends.change_pct || 0

  const maxCount = Math.max(...daily.map(d => d.count), 1)

  const DirectionIcon = direction === 'up' ? ArrowUpRight : direction === 'down' ? ArrowDownRight : Minus

  return (
    <div className="intel-trend-widget">
      <div className="intel-widget-header">
        <h3>Crime Trends</h3>
        <div className={`intel-trend-badge intel-trend-${direction}`}>
          <DirectionIcon size={14} />
          <span>{Math.abs(changePct)}%</span>
        </div>
      </div>

      <div className="intel-trend-chart">
        {daily.length === 0 ? (
          <div className="similar-empty"><p>No trend data</p></div>
        ) : (
          <div className="intel-bar-chart">
            {daily.slice(-14).map((d, i) => (
              <div key={i} className="intel-bar-col">
                <div className="intel-bar-wrapper">
                  <div
                    className="intel-bar"
                    style={{ height: `${(d.count / maxCount) * 100}%` }}
                  />
                </div>
                <span className="intel-bar-label">
                  {d.date ? d.date.slice(-5) : ''}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="intel-trend-footer">
        <span className="intel-trend-period">Last {trends.period || '30d'}</span>
        <span className="intel-trend-summary">
          {daily.length} days · {daily.reduce((s, d) => s + d.count, 0)} total crimes
        </span>
      </div>
    </div>
  )
}
