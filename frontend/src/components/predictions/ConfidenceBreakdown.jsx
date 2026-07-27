import { Target } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function ConfidenceBreakdown({ forecast }) {
  const { t } = useLanguage()
  if (!forecast) return null

  const confidence = forecast.confidence || 0
  const factors = [
    { label: t('Data Quality'), value: Math.min(100, confidence + 10), color: '#10b981' },
    { label: t('Model Reliability'), value: Math.min(100, confidence + 5), color: '#3b82f6' },
    { label: t('Temporal Stability'), value: Math.max(0, confidence - 10), color: '#f59e0b' },
    { label: t('Statistical Confidence'), value: confidence, color: '#8b5cf6' },
  ]

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Target size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Confidence Breakdown')}</h3>
      </div>

      <div className="space-y-2">
        {factors.map((f, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className="text-[10px] text-[var(--text-muted)] w-28">{f.label}</span>
            <div className="flex-1 h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${f.value}%`, background: f.color }} />
            </div>
            <span className="text-[10px] font-semibold text-[var(--text-secondary)]">{f.value}%</span>
          </div>
        ))}
      </div>

      <div className="mt-3 pt-2 border-t border-[var(--border)]">
        <p className="text-[10px] text-[var(--text-muted)]">
          {t('Overall confidence:')} {confidence}% — {confidence >= 75 ? t('High reliability') : confidence >= 50 ? t('Moderate reliability') : t('Low reliability')}
        </p>
      </div>
    </div>
  )
}
