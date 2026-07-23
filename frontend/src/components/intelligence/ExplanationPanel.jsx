import { X, Brain, ChevronRight, Shield } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const confidenceColors = {
  high: 'text-green-400 bg-green-500/10',
  medium: 'text-amber-400 bg-amber-500/10',
  low: 'text-red-400 bg-red-500/10',
}

const confidenceBarColors = {
  high: 'bg-green-400',
  medium: 'bg-amber-400',
  low: 'bg-red-400',
}

export default function ExplanationPanel({ explanation, onClose }) {
  const { t } = useLanguage()

  if (!explanation) return null

  const confidence = explanation.confidence || { score: 0, level: 'low' }
  const chain = explanation.reasoning_chain || []
  const evidence = explanation.supporting_evidence || []
  const actions = explanation.recommended_actions || []

  return (
    <div className="mt-2 mb-3 bg-gradient-to-br from-purple-500/5 to-indigo-500/5 border border-purple-500/20 rounded-xl p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Brain size={14} className="text-purple-400" />
          <span className="text-xs font-semibold text-purple-300">{t('AI Explanation')}</span>
        </div>
        <button onClick={onClose} className="text-white/30 hover:text-white/60 transition-colors">
          <X size={12} />
        </button>
      </div>

      {/* Confidence Bar */}
      <div className="flex items-center gap-3 mb-3">
        <span className="text-[10px] text-white/50">{t('Confidence')}</span>
        <div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${confidenceBarColors[confidence.level] || 'bg-slate-400'}`}
            style={{ width: `${confidence.score}%` }}
          />
        </div>
        <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${confidenceColors[confidence.level] || 'text-slate-400 bg-slate-500/10'}`}>
          {confidence.score}% {t(confidence.level?.toUpperCase() || 'LOW')}
        </span>
      </div>

      {/* Explanation */}
      {explanation.explanation && (
        <p className="text-xs text-white/70 leading-relaxed mb-3">{t(explanation.explanation)}</p>
      )}

      {/* Reasoning Chain */}
      {chain.length > 0 && (
        <div className="mb-3">
          <span className="text-[10px] text-white/40 font-medium uppercase tracking-wider">{t('Reasoning Chain')}</span>
          <div className="mt-1.5 space-y-1">
            {chain.map((step, i) => (
              <div key={i} className="flex items-start gap-2 text-[11px]">
                <span className="text-purple-400/60 font-mono text-[10px] mt-0.5 w-4 flex-shrink-0">
                  {step.step || i + 1}.
                </span>
                <div className="flex-1 min-w-0">
                  <span className="text-white/60">{t(step.claim)}</span>
                  <span className="text-white/30 ml-1">({step.confidence}%)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Supporting Evidence */}
      {evidence.length > 0 && (
        <div className="mb-3">
          <span className="text-[10px] text-white/40 font-medium uppercase tracking-wider">{t('Supporting Evidence')}</span>
          <div className="mt-1.5 space-y-1">
            {evidence.map((ev, i) => (
              <div key={i} className="flex items-center gap-2 text-[11px]">
                <Shield size={10} className="text-blue-400/60 flex-shrink-0" />
                <span className="text-white/60">{t(ev.description)}</span>
                <span className="text-white/30 text-[10px]">
                  ({Math.round((ev.strength || 0) * (ev.strength <= 1 ? 100 : 1))}%)
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommended Actions */}
      {actions.length > 0 && (
        <div>
          <span className="text-[10px] text-white/40 font-medium uppercase tracking-wider">{t('Suggested Actions')}</span>
          <div className="mt-1.5 flex flex-wrap gap-1">
            {actions.map((a, i) => (
              <span key={i} className="flex items-center gap-0.5 text-[10px] bg-white/5 text-white/50 px-2 py-0.5 rounded-lg">
                <ChevronRight size={8} className="text-purple-400/50" />
                {t(a)}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

