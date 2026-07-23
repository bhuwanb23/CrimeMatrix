import { MapPin, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

const trendIcons = {
  up: TrendingUp,
  down: TrendingDown,
  stable: Minus,
}

export default function HotspotRankings({ hotspots, loading }) {
  const { t } = useLanguage()

  if (loading) {
    return (
      <div className="hotspot-rankings">
        <div className="intel-widget-header">
          <h3><MapPin size={14} /> {t('Hotspot Rankings')}</h3>
        </div>
        <div className="similar-loading"><div className="similar-spinner" /></div>
      </div>
    )
  }

  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="hotspot-rankings">
        <div className="intel-widget-header">
          <h3><MapPin size={14} /> {t('Hotspot Rankings')}</h3>
        </div>
        <div className="similar-empty"><p>{t('No hotspots detected')}</p></div>
      </div>
    )
  }

  const maxCount = Math.max(...hotspots.map(h => h.crime_count || 0), 1)

  return (
    <div className="hotspot-rankings">
      <div className="intel-widget-header">
        <h3><MapPin size={14} /> {t('Hotspot Rankings')}</h3>
        <span className="similar-count">{hotspots.length}</span>
      </div>

      <div className="hotspot-rankings-list">
        {hotspots.map((h, i) => {
          const riskColor = riskColors[h.risk_level] || '#10b981'
          const TrendIcon = trendIcons[h.trend_direction] || Minus
          return (
            <div key={h.id || i} className="hotspot-ranking-item">
              <div className="hotspot-rank">#{i + 1}</div>
              <div className="hotspot-info">
                <div className="hotspot-info-top">
                  <span className="hotspot-name">{t(h.name)}</span>
                  <span className="hotspot-risk-badge" style={{ color: riskColor, background: `${riskColor}15` }}>
                    {t(h.risk_level)}
                  </span>
                </div>
                <div className="hotspot-bar">
                  <div
                    className="hotspot-bar-fill"
                    style={{ width: `${(h.crime_count / maxCount) * 100}%`, background: riskColor }}
                  />
                </div>
                <div className="hotspot-meta">
                  <span>{h.crime_count} {t('crimes')}</span>
                  {h.dominant_crime_type && <span>• {t(h.dominant_crime_type)}</span>}
                  {h.trend_direction && (
                    <span className={`hotspot-trend hotspot-trend-${h.trend_direction}`}>
                      <TrendIcon size={10} />
                      {h.trend_change_pct ? `${Math.abs(h.trend_change_pct)}%` : ''}
                    </span>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

