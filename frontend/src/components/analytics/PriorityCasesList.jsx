import { ClipboardList } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const priorityColors = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#10b981',
}

export default function PriorityCasesList({ cases }) {
  const { t } = useLanguage()
  if (!cases || cases.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
          <ClipboardList size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('Priority Cases')}</h3>
        </div>
        <div className="flex flex-col items-center justify-center py-10">
          <ClipboardList size={28} className="text-slate-200 mb-2" />
          <p className="text-xs font-medium text-slate-500 mb-1">{t('No priority cases')}</p>
          <p className="text-[10px] text-slate-400 text-center max-w-[200px]">
            Active investigations with priority scores will appear here.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden min-h-[300px]">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ClipboardList size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('Priority Cases')}</h3>
        </div>
        <span className="text-[10px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded-full font-medium">{cases.length}</span>
      </div>
      <div className="divide-y divide-slate-50 max-h-[260px] overflow-y-auto">
        {cases.map((c, i) => {
          const color = priorityColors[c.priority] || '#64748b'
          return (
            <div key={c.id || i} className="px-4 py-3 hover:bg-slate-50 transition-colors">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-semibold text-slate-900 truncate">{c.title}</span>
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded ml-2 flex-shrink-0" style={{ color, background: `${color}15` }}>
                  {c.priority}
                </span>
              </div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-[10px] text-slate-400">{c.district || 'N/A'}</span>
                <span className="text-[10px] text-slate-400">•</span>
                <span className="text-[10px] text-slate-400">Progress: {c.progress || 0}%</span>
              </div>
              <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full rounded-full transition-all" style={{ width: `${c.progress || 0}%`, background: color }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
