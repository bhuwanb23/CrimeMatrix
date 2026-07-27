import { Shield } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

export default function HighRiskSuspectsList({ suspects }) {
  const { t } = useLanguage()
  if (!suspects || suspects.length === 0) {
    return (
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden min-h-[300px]">
        <div className="px-4 py-3 border-b border-[var(--border)] flex items-center gap-2">
          <Shield size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('High-Risk Suspects')}</h3>
        </div>
        <div className="flex flex-col items-center justify-center py-10">
          <Shield size={28} className="text-[var(--text-muted)] mb-2" />
          <p className="text-xs font-medium text-[var(--text-muted)] mb-1">{t('No high-risk suspects')}</p>
          <p className="text-[10px] text-[var(--text-muted)] text-center max-w-[200px]">
            Suspects with risk scores above threshold will appear here. Run suspect risk scoring first.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden min-h-[300px]">
      <div className="px-4 py-3 border-b border-[var(--border)] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('High-Risk Suspects')}</h3>
        </div>
        <span className="text-[10px] bg-red-100 text-red-600 px-1.5 py-0.5 rounded-full font-medium">{suspects.length}</span>
      </div>
      <div className="divide-y divide-slate-50 max-h-[260px] overflow-y-auto">
        {suspects.map((s, i) => {
          const color = riskColors[s.risk_level] || '#64748b'
          return (
            <div key={s.id || i} className="px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-bold text-[var(--text-muted)] w-5">#{i + 1}</span>
                  <span className="text-xs font-semibold text-[var(--text-primary)]">{s.name}</span>
                </div>
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ color, background: `${color}15` }}>
                  {s.risk_level}
                </span>
              </div>
              <div className="flex items-center gap-2 ml-5">
                <div className="flex-1 h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(s.risk_score || 0, 100)}%`, background: color }} />
                </div>
                <span className="text-[10px] font-mono text-[var(--text-muted)] w-8 text-right">{s.risk_score || 0}%</span>
              </div>
              <div className="flex items-center gap-2 ml-5 mt-1 text-[10px] text-[var(--text-muted)]">
                <span>{s.offenses || 0} offenses</span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
