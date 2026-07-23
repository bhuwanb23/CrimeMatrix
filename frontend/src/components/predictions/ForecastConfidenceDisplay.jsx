import { Info } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function ForecastConfidenceDisplay({ forecast }) {
  const { t } = useLanguage()
  if (!forecast) return null

  const confidence = forecast.confidence || 0
  const level = confidence >= 75 ? 'high' : confidence >= 50 ? 'medium' : 'low'
  const colors = { high: 'text-green-500 bg-green-50', medium: 'text-amber-500 bg-amber-50', low: 'text-red-500 bg-red-50' }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Info size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-slate-900">{t('Forecast Confidence')}</h3>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: `${confidence}%` < 50 ? 'rgba(239,68,68,0.1)' : `${confidence}%` < 75 ? 'rgba(245,158,11,0.1)' : 'rgba(16,185,129,0.1)' }}>
          <span className="text-lg font-bold text-slate-900">{confidence}</span>
        </div>
        <div>
          <span className={`text-xs font-semibold px-2 py-0.5 rounded ${colors[level]}`}>{level} confidence</span>
          <p className="text-[10px] text-slate-400 mt-1">
            {level === 'high' ? 'Forecast is reliable based on sufficient data' :
             level === 'medium' ? 'Forecast has moderate reliability' :
             'Insufficient data for reliable forecast'}
          </p>
        </div>
      </div>

      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">{t('Data points')}</span>
          <span className="font-semibold text-slate-700">{forecast.data_points || 0}</span>
        </div>
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">{t('Trend')}</span>
          <span className="font-semibold text-slate-700">{forecast.trend || 'stable'}</span>
        </div>
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">{t('Predictions')}</span>
          <span className="font-semibold text-slate-700">{forecast.forecast?.length || 0}</span>
        </div>
      </div>
    </div>
  )
}
