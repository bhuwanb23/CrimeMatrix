import { Calendar } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function SeasonalPatternsChart({ patterns }) {
  const { t } = useLanguage()
  if (!patterns) return null

  const { by_hour = [], by_day_of_week = [], by_month = [] } = patterns

  function MiniBar({ data, label, valueKey = 'count', labelKey }) {
    const max = Math.max(...data.map(d => d[valueKey] || 0), 1)
    return (
      <div className="bg-slate-50 rounded-lg p-3">
        <h4 className="text-[11px] font-semibold text-slate-600 mb-2">{t(label)}</h4>
        <div className="flex items-end gap-0.5 h-14">
          {data.map((d, i) => (
            <div key={i} className="flex-1 flex flex-col items-center">
              <div className="w-full flex items-end justify-center" style={{ height: '100%' }}>
                <div
                  className="w-full bg-amber-500 rounded-t opacity-70 hover:opacity-100 transition-opacity"
                  style={{ height: `${((d[valueKey] || 0) / max) * 100}%`, minHeight: 1 }}
                />
              </div>
              <span className="text-[7px] text-slate-400 mt-0.5">{d[labelKey]}</span>
            </div>
          )}
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

      <div className="grid grid-cols-3 gap-2">
        {by_hour.length > 0 && <MiniBar data={by_hour} label="By Hour" labelKey="hour" />}
        {by_day_of_week.length > 0 && <MiniBar data={by_day_of_week} label="By Day" labelKey="day" />}
        {by_month.length > 0 && <MiniBar data={by_month} label="By Month" labelKey="month" />}
      </div>
    </div>
  )
}
