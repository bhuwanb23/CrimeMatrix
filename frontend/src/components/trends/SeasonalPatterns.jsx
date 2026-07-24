import { Calendar } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function SeasonalPatterns({ patterns }) {
  const { t } = useLanguage()
  if (!patterns) return null

  const { by_hour = [], by_day_of_week = [], by_month = [] } = patterns
  const hasData = by_hour.length > 0 || by_day_of_week.length > 0 || by_month.length > 0

  if (!hasData) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <Calendar size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('Seasonal Patterns')}</h3>
        </div>
        <div className="py-8 text-center">
          <Calendar size={28} className="mx-auto text-slate-200 mb-2" />
          <p className="text-xs text-slate-400">No seasonal data available yet</p>
          <p className="text-[10px] text-slate-300 mt-1">Data will appear as more crime records accumulate</p>
        </div>
      </div>
    )
  }

  function MiniBarChart({ data, label, valueKey = 'count', labelKey }) {
    if (!data || data.length === 0) return null
    const max = Math.max(...data.map(d => d[valueKey] || 0), 1)
    const showLabels = data.length <= 12

    return (
      <div className="seasonal-chart flex-1">
        <h4 className="text-[11px] font-semibold text-slate-600 mb-2">{t(label)}</h4>
        <div className="seasonal-bars flex items-end gap-[2px]" style={{ height: 120 }}>
          {data.map((d, i) => {
            const val = d[valueKey] || 0
            const pct = max > 0 ? (val / max) * 100 : 0
            const barHeight = Math.max(pct, val > 0 ? 8 : 0)
            return (
              <div key={i} className="seasonal-bar-col flex flex-col items-center flex-1 min-w-0">
                <div className="seasonal-bar-wrapper w-full flex items-end" style={{ height: 100 }}>
                  <div
                    className="seasonal-bar w-full rounded-t-sm bg-amber-400"
                    style={{ height: `${barHeight}%`, minHeight: val > 0 ? 6 : 1 }}
                    title={`${d[labelKey]}: ${val}`}
                  />
                </div>
                {showLabels && (
                  <span className="text-[8px] text-slate-400 mt-0.5 truncate w-full text-center">
                    {d[labelKey]}
                  </span>
                )}
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Calendar size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-slate-900">{t('Seasonal Patterns')}</h3>
      </div>

      <div className="grid grid-cols-3 gap-4">
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

      {/* Summary */}
      <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
        <span>{by_hour.length} hours • {by_day_of_week.length} days • {by_month.length} months tracked</span>
        <span>{t('Updated periodically')}</span>
      </div>
    </div>
  )
}
