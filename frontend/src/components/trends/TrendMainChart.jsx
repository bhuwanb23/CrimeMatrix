import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function TrendMainChart({ data, title = "Crime Trend", height = 200 }) {
  const { t } = useLanguage()
  if (!data || data.length === 0) {
    return (
      <div className="trend-chart-widget">
        <div className="intel-widget-header">
          <h3>{t(title)}</h3>
        </div>
        <div className="similar-empty"><p>{t('No trend data')}</p></div>
      </div>
    )
  }

  const maxCount = Math.max(...data.map(d => d.count || 0), 1)
  const total = data.reduce((s, d) => s + (d.count || 0), 0)
  const avg = Math.round(total / data.length)

  const recent = data.slice(-7)
  const earlier = data.slice(0, 7)
  const recentAvg = recent.reduce((s, d) => s + (d.count || 0), 0) / Math.max(recent.length, 1)
  const earlierAvg = earlier.reduce((s, d) => s + (d.count || 0), 0) / Math.max(earlier.length, 1)
  const changePct = earlierAvg > 0 ? ((recentAvg - earlierAvg) / earlierAvg * 100) : 0
  const direction = changePct > 5 ? 'up' : changePct < -5 ? 'down' : 'stable'

  const DirectionIcon = direction === 'up' ? ArrowUpRight : direction === 'down' ? ArrowDownRight : Minus

  return (
    <div className="trend-chart-widget">
      <div className="intel-widget-header">
        <h3>{t(title)}</h3>
        <div className={`intel-trend-badge intel-trend-${direction}`}>
          <DirectionIcon size={14} />
          <span>{Math.abs(Math.round(changePct))}%</span>
        </div>
      </div>

      <div className="trend-chart-area">
        <div className="trend-chart-bars" style={{ height }}>
          {data.map((d, i) => (
            <div key={i} className="trend-bar-col">
              <div className="trend-bar-wrapper">
                <div
                  className="trend-bar"
                  style={{ height: `${((d.count || 0) / maxCount) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
        <div className="trend-chart-avg" style={{ bottom: `${(avg / maxCount) * 100}%` }}>
          <span className="trend-avg-label">{t('avg')}: {avg}</span>
        </div>
      </div>

      <div className="trend-chart-labels">
        {data.filter((_, i) => i % Math.ceil(data.length / 8) === 0 || i === data.length - 1).map((d, i) => (
          <span key={i} className="trend-label">{(d.date || d.period || '').slice(-5)}</span>
        ))}
      </div>

      <div className="trend-chart-footer">
        <span>{t('Total')}: {total}</span>
        <span>{data.length} {t('periods')}</span>
      </div>
    </div>
  )
}
