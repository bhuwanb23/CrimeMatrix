import { MapPin } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function HotspotHeatmap({ hotspots }) {
  const { t } = useLanguage()
  
  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <MapPin size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Crime Heatmap')}</h3>
        </div>
        <div className="py-8 text-center text-xs text-[var(--text-muted)]">
          <MapPin size={24} className="mx-auto mb-2 text-[var(--text-muted)]" />
          <p>No heatmap data</p>
        </div>
      </div>
    )
  }

  const maxCount = Math.max(...hotspots.map(h => h.crime_count || 0), 1)

  function getHeatColor(count) {
    const ratio = count / maxCount
    if (ratio > 0.8) return '#ef4444'
    if (ratio > 0.6) return '#f59e0b'
    if (ratio > 0.4) return '#3b82f6'
    if (ratio > 0.2) return '#10b981'
    return '#64748b'
  }

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <MapPin size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Crime Heatmap')}</h3>
      </div>

      {/* Bubbles with labels */}
      <div className="flex flex-wrap items-end justify-center gap-4 py-4">
        {hotspots.map((h, i) => {
          const color = getHeatColor(h.crime_count || 0)
          const size = 40 + ((h.crime_count || 0) / maxCount) * 50
          return (
            <div key={h.id || i} className="flex flex-col items-center gap-1">
              <div
                className="rounded-full flex items-center justify-center text-xs font-bold text-white shadow-sm transition-transform hover:scale-110"
                style={{
                  background: color,
                  width: size,
                  height: size,
                }}
                title={`${t(h.name)}: ${h.crime_count} ${t('crimes')} (${t(h.risk_level)})`}
              >
                {h.crime_count}
              </div>
              <span className="text-[10px] text-[var(--text-muted)] text-center max-w-[80px] truncate">{t(h.name)}</span>
              <span className="text-[9px] text-[var(--text-muted)]">{h.risk_level || ''}</span>
            </div>
          )
        })}
      </div>

      {/* District list below bubbles */}
      <div className="border-t border-[var(--border)] pt-3 mt-2">
        <div className="space-y-1.5">
          {hotspots.slice(0, 6).map((h, i) => {
            const color = getHeatColor(h.crime_count || 0)
            const pct = maxCount > 0 ? ((h.crime_count || 0) / maxCount) * 100 : 0
            return (
              <div key={i} className="flex items-center gap-2 text-xs">
                <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: color }} />
                <span className="text-[var(--text-secondary)] flex-1 min-w-0 truncate">{t(h.name)}</span>
                <div className="w-20 h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden flex-shrink-0">
                  <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
                </div>
                <span className="text-[var(--text-muted)] w-6 text-right text-[10px]">{h.crime_count}</span>
              </div>
            )
          })}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 mt-3 pt-2 border-t border-[var(--border)]">
          <span className="text-[10px] text-[var(--text-muted)] font-medium">Risk:</span>
          <span className="flex items-center gap-1 text-[10px] text-[var(--text-muted)]"><span className="w-2 h-2 rounded-full bg-red-500" /> {t('Critical')}</span>
          <span className="flex items-center gap-1 text-[10px] text-[var(--text-muted)]"><span className="w-2 h-2 rounded-full bg-amber-500" /> {t('High')}</span>
          <span className="flex items-center gap-1 text-[10px] text-[var(--text-muted)]"><span className="w-2 h-2 rounded-full bg-blue-500" /> {t('Medium')}</span>
          <span className="flex items-center gap-1 text-[10px] text-[var(--text-muted)]"><span className="w-2 h-2 rounded-full bg-emerald-500" /> {t('Low')}</span>
        </div>
      </div>
    </div>
  )
}
