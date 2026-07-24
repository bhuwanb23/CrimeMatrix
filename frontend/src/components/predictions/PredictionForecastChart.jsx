import { TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function PredictionForecastChart({ forecast }) {
  const { t } = useLanguage()

  if (!forecast) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center">
            <TrendingUp size={16} className="text-indigo-500" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">{t('Crime Forecast')}</h3>
        </div>
        <div className="flex flex-col items-center justify-center py-12">
          <TrendingUp size={28} className="text-slate-200 mb-2" />
          <p className="text-xs text-slate-400">No forecast data available</p>
        </div>
      </div>
    )
  }

  const historical = forecast.historical || []
  const forecastData = forecast.forecast || []
  const dataPoints = forecast.data_points || historical.length
  const maxCount = Math.max(...historical.map(d => d.count || 0), ...forecastData.map(d => d.predicted || d.count || 0), 1)

  // Sparse data message
  if (historical.length <= 3) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center">
              <TrendingUp size={16} className="text-indigo-500" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">{t('Crime Forecast')}</h3>
          </div>
          <span className="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-medium">{dataPoints} data points</span>
        </div>
        <div className="flex flex-col items-center justify-center py-12">
          <TrendingUp size={28} className="text-slate-200 mb-2" />
          <p className="text-xs font-medium text-slate-500 mb-1">Limited forecast data</p>
          <p className="text-[10px] text-slate-400 text-center max-w-[220px]">
            Only {dataPoints} day(s) recorded. Need at least 7 days for accurate forecasting.
          </p>
          {historical.length > 0 && (
            <p className="mt-3 text-xs text-slate-500">Avg: <strong>{Math.round(historical.reduce((s, d) => s + (d.count || 0), 0) / historical.length)}</strong> crimes/day</p>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center">
            <TrendingUp size={16} className="text-indigo-500" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">{t('Crime Forecast')}</h3>
          <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
            forecast.trend === 'increasing' ? 'bg-red-100 text-red-600' :
            forecast.trend === 'decreasing' ? 'bg-emerald-100 text-emerald-600' :
            'bg-slate-100 text-slate-600'
          }`}>{forecast.trend || 'stable'}</span>
        </div>
        <span className="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-medium">{dataPoints} data points</span>
      </div>

      {/* Chart */}
      <div className="px-5 py-4">
        <div className="flex items-end gap-[3px]" style={{ height: 160 }}>
          {historical.slice(-20).map((d, i) => (
            <div key={i} className="flex flex-col items-center flex-1 min-w-0">
              <div className="w-full flex items-end" style={{ height: 140 }}>
                <div
                  className="w-full rounded-t bg-indigo-400 hover:bg-indigo-500 transition-colors"
                  style={{ height: `${((d.count || 0) / maxCount) * 100}%`, minHeight: d.count > 0 ? 4 : 1 }}
                  title={`${d.date}: ${d.count} crimes`}
                />
              </div>
              <span className="text-[7px] text-slate-400 mt-1 truncate">{(d.date || '').slice(-5)}</span>
            </div>
          ))}
          {forecastData.map((f, i) => (
            <div key={`f-${i}`} className="flex flex-col items-center flex-1 min-w-0">
              <div className="w-full flex items-end" style={{ height: 140 }}>
                <div
                  className="w-full rounded-t bg-amber-400 border-2 border-dashed border-amber-300"
                  style={{ height: `${((f.predicted || f.count || 0) / maxCount) * 100}%`, minHeight: 4 }}
                  title={`Predicted: ${f.predicted || f.count}`}
                />
              </div>
              <span className="text-[7px] text-amber-500 font-medium mt-1">pred</span>
            </div>
          ))}
        </div>
      </div>

      {/* Info */}
      <div className="px-5 py-3 border-t border-slate-100 flex items-center gap-6 text-[10px] text-slate-500">
        <span>Confidence: <strong className="text-slate-700">{forecast.confidence || 0}%</strong></span>
        <span>Data points: <strong className="text-slate-700">{dataPoints}</strong></span>
        <span>Trend: <strong className="text-slate-700">{forecast.trend || 'stable'}</strong></span>
      </div>
    </div>
  )
}
