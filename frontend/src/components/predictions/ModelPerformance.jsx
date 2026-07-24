import { Activity } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function ModelPerformance({ models }) {
  const { t } = useLanguage()
  if (!models || models.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-violet-50 flex items-center justify-center">
            <Activity size={16} className="text-violet-500" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">{t('Model Performance')}</h3>
        </div>
        <div className="flex flex-col items-center justify-center py-12">
          <Activity size={28} className="text-slate-200 mb-2" />
          <p className="text-xs text-slate-400">No models registered yet</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
      <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-lg bg-violet-50 flex items-center justify-center">
          <Activity size={16} className="text-violet-500" />
        </div>
        <h3 className="text-sm font-bold text-slate-900">{t('Model Performance')}</h3>
      </div>
      <div className="divide-y divide-slate-50">
        {models.map((m, i) => (
          <div key={m.id || i} className="px-5 py-3 hover:bg-slate-50 transition-colors">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-semibold text-slate-900">{m.name}</span>
              <span className="text-[10px] text-slate-400">v{m.version || '1.0'}</span>
            </div>
            <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden mb-1">
              <div className="h-full rounded-full bg-emerald-400" style={{ width: `${m.accuracy || 0}%` }} />
            </div>
            <div className="flex items-center justify-between text-[10px] text-slate-400">
              <span>Accuracy: {m.accuracy || 0}%</span>
              <span className={`px-1.5 py-0.5 rounded font-medium ${
                m.status === 'active' ? 'bg-emerald-100 text-emerald-600' : 'bg-slate-100 text-slate-500'
              }`}>{m.status || 'inactive'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
