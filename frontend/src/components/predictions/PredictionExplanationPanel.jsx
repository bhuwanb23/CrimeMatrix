import { useState } from 'react'
import { HelpCircle, ChevronDown, ChevronRight, AlertTriangle } from 'lucide-react'
import { explainPrediction, getPredictionSources } from '../../services/predictions'

export default function PredictionExplanationPanel({ predictionId }) {
  const [explanation, setExplanation] = useState(null)
  const [expanded, setExpanded] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleExplain() {
    if (loading) return
    setLoading(true)
    try {
      const res = await explainPrediction(predictionId)
      setExplanation(res?.data || res)
      setExpanded(true)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <HelpCircle size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Why This Prediction?</h3>
        </div>
        <button onClick={handleExplain} disabled={loading} className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
          {loading ? 'Loading...' : explanation ? 'Refresh' : 'Explain'}
        </button>
      </div>

      {explanation && (
        <div className="space-y-3">
          {/* Contributing Factors */}
          <div>
            <h4 className="text-[11px] font-semibold text-slate-600 mb-1.5">Contributing Factors</h4>
            {explanation.factors?.map((f, i) => (
              <div key={i} className="flex items-center gap-2 mb-1">
                <span className="text-[10px] text-slate-500 w-28">{f.name}</span>
                <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${(f.weight || 0) * 100}%` }} />
                </div>
                <span className="text-[10px] font-semibold text-slate-700">{Math.round((f.weight || 0) * 100)}%</span>
              </div>
            ))}
          </div>

          {/* Model Explanation */}
          {explanation.model_explanation && (
            <div className="p-2 bg-slate-50 rounded-lg">
              <p className="text-[11px] text-slate-600 leading-relaxed">{explanation.model_explanation}</p>
            </div>
          )}

          {/* Evidence */}
          {explanation.evidence?.length > 0 && (
            <div>
              <h4 className="text-[11px] font-semibold text-slate-600 mb-1.5">Evidence Sources</h4>
              {explanation.evidence.map((e, i) => (
                <div key={i} className="flex items-center gap-2 text-[10px] text-slate-500">
                  <AlertTriangle size={8} className="text-amber-500" />
                  <span>{e.description}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!explanation && !loading && (
        <p className="text-[10px] text-slate-400">Click Explain to see why this prediction was made</p>
      )}
    </div>
  )
}
