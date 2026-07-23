import { MapPin, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function DistrictForecastPanel({ district, forecast }) {
  const { t } = useLanguage()
  if (!forecast) return null

  const trend = forecast.trend || 'stable'
  const TrendIcon = trend === 'increasing' ? TrendingUp : trend === 'decreasing' ? TrendingDown : Minus
  const trendColor = trend === 'increasing' ? 'text-red-500' : trend === 'decreasing' ? 'text-green-500' : 'text-slate-400'

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <MapPin size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t(t('District Forecast'))}</h3>
        </div>
        <div className="flex items-center gap-1">
          <TrendIcon size={14} className={trendColor} />
          <span className={`text-xs font-semibold ${trendColor}`}>{trend}</span>
        </div>
      </div>

      {district && (
        <div className="mb-3 p-2 bg-slate-50 rounded-lg">
          <span className="text-xs text-slate-500">{t(t('District:'))}</span>
          <span className="text-xs font-semibold text-slate-900 ml-1">{district.name}</span>
        </div>
      )}

      <div className="flex items-center gap-2 mb-3">
        <span className="text-[10px] text-slate-400">{t(t('Confidence:'))}</span>
        <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
          <div className="h-full bg-amber-500 rounded-full" style={{ width: `${forecast.confidence || 0}%` }} />
        </div>
        <span className="text-[10px] font-semibold text-slate-700">{forecast.confidence || 0}%</span>
      </div>

      {forecast.forecast && forecast.forecast.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {forecast.forecast.slice(0, 5).map((f, i) => (
            <div key={i} className="text-center px-2 py-1 bg-slate-50 rounded text-[10px]">
              <span className="block font-semibold text-slate-900">{f.predicted}</span>
              <span className="text-slate-400">{f.date?.slice(-5)}</span>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-3 pt-2 border-t border-slate-100">
        <span className="text-[10px] text-slate-400">{forecast.data_points || 0} data points</span>
      </div>
    </div>
  )
}
