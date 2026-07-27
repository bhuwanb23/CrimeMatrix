import { useState } from 'react'
import { HelpCircle, AlertTriangle } from 'lucide-react'
import { explainPrediction } from '../../services/predictions'
import { useLanguage } from '../../context/LanguageContext'

export default function PredictionExplanationPanel({ predictionId }) {
  const { t } = useLanguage()
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleExplain() {
    if (loading) return
    setLoading(true)
    try {
      const res = await explainPrediction(predictionId)
      setExplanation(res?.data || res)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <HelpCircle size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Why This Prediction?')}</h3>
        </div>
        <button onClick={handleExplain} disabled={loading} className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
          {loading ? t('Loading...') : explanation ? t('Refresh') : t('Explain')}
        </button>
      </div>

      {explanation && (
        <div className="space-y-3">
          {/* Contributing Factors */}
          <div>
            <h4 className="text-[11px] font-semibold text-[var(--text-secondary)] mb-1.5">{t('Contributing Factors')}</h4>
            {explanation.factors?.map((f, i) => (
              <div key={i} className="flex items-center gap-2 mb-1">
                <span className="text-[10px] text-[var(--text-muted)] w-28">{t(f.name)}</span>
                <div className="flex-1 h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden">
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${(f.weight || 0) * 100}%` }} />
                </div>
                <span className="text-[10px] font-semibold text-[var(--text-secondary)]">{Math.round((f.weight || 0) * 100)}%</span>
              </div>
            ))}
          </div>

          {/* Model Explanation */}
          {explanation.model_explanation && (
            <div className="p-2 bg-[var(--bg-muted)] rounded-lg">
              <p className="text-[11px] text-[var(--text-secondary)] leading-relaxed">{t(explanation.model_explanation)}</p>
            </div>
          )}

          {/* Evidence */}
          {explanation.evidence?.length > 0 && (
            <div>
              <h4 className="text-[11px] font-semibold text-[var(--text-secondary)] mb-1.5">{t('Evidence Sources')}</h4>
              {explanation.evidence.map((e, i) => (
                <div key={i} className="flex items-center gap-2 text-[10px] text-[var(--text-muted)]">
                  <AlertTriangle size={8} className="text-amber-500" />
                  <span>{t(e.description)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!explanation && !loading && (
        <p className="text-[10px] text-[var(--text-muted)]">{t('Click Explain to see why this prediction was made')}</p>
      )}
    </div>
  )
}
