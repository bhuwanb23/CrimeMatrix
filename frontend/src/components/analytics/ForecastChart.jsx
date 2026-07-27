import { TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function ForecastChart({ forecasts }) {
  const { t } = useLanguage()
  if (!forecasts) {
    return (
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-4 py-3 border-b border-[var(--border)] flex items-center gap-2">
          <TrendingUp size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Crime Forecast')}</h3>
        </div>
        <div className="flex flex-col items-center justify-center py-10">
          <TrendingUp size={28} className="text-[var(--text-muted)] mb-2" />
          <p className="text-xs text-[var(--text-muted)]">No forecast data available</p>
        </div>
      </div>
    )
  }

  const historical = forecasts.historical || []
  const forecast = forecasts.forecast || []
  const dataPoints = forecasts.data_points || historical.length
  const maxCount = Math.max(...historical.map(d => d.count || 0), 1)

  // Sparse data: show message when very few points
  if (historical.length <= 3) {
    return (
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-4 py-3 border-b border-[var(--border)] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp size={14} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Crime Forecast')}</h3>
          </div>
          <span className="text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded-full font-medium">{dataPoints} data points</span>
        </div>
        <div className="flex flex-col items-center justify-center py-10">
          <TrendingUp size={28} className="text-[var(--text-muted)] mb-2" />
          <p className="text-xs font-medium text-[var(--text-muted)] mb-1">Limited forecast data</p>
          <p className="text-[10px] text-[var(--text-muted)] text-center max-w-[220px]">
            Only {dataPoints} day(s) recorded. Need at least 7 days of data for accurate forecasting.
          </p>
          {historical.length > 0 && (
            <div className="mt-3 text-xs text-[var(--text-muted)]">
              <span>Current avg: <strong>{Math.round(historical.reduce((s, d) => s + (d.count || 0), 0) / historical.length)}</strong> crimes/day</span>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden min-h-[300px]">
      <div className="px-4 py-3 border-b border-[var(--border)] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TrendingUp size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Crime Forecast')}</h3>
        </div>
        <span className="text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded-full font-medium">{dataPoints} data points</span>
      </div>

      <div className="px-4 py-3">
        <div className="flex items-end gap-[3px]" style={{ height: 140 }}>
          {historical.slice(-14).map((d, i) => (
            <div key={i} className="flex flex-col items-center flex-1 min-w-0">
              <div className="w-full flex items-end" style={{ height: 120 }}>
                <div
                  className="w-full rounded-t bg-blue-400 hover:bg-blue-500 transition-colors"
                  style={{ height: `${((d.count || 0) / maxCount) * 100}%`, minHeight: d.count > 0 ? 4 : 1 }}
                  title={`${d.date}: ${d.count} crimes`}
                />
              </div>
              <span className="text-[8px] text-[var(--text-muted)] mt-1">{(d.date || '').slice(-5)}</span>
            </div>
          ))}
          {forecast.map((f, i) => (
            <div key={`f-${i}`} className="flex flex-col items-center flex-1 min-w-0">
              <div className="w-full flex items-end" style={{ height: 120 }}>
                <div
                  className="w-full rounded-t bg-amber-400 border-2 border-dashed border-amber-300"
                  style={{ height: `${((f.count || 0) / maxCount) * 100}%`, minHeight: 4 }}
                  title={`Predicted: ${f.count} crimes (${f.confidence}% confidence)`}
                />
              </div>
              <span className="text-[8px] text-amber-500 font-medium mt-1">pred</span>
            </div>
          ))}
        </div>
      </div>

      {forecast.length > 0 && (
        <div className="px-4 py-2 border-t border-[var(--border)] flex items-center gap-4 text-[10px] text-[var(--text-muted)]">
          <span>Predicted: <strong className="text-[var(--text-secondary)]">{forecast[0].count}</strong> crimes</span>
          <span>Confidence: <strong className="text-[var(--text-secondary)]">{forecast[0].confidence}%</strong></span>
        </div>
      )}
    </div>
  )
}
