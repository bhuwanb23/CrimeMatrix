import { Target } from 'lucide-react'

export default function ConfidenceBreakdown({ forecast }) {
  if (!forecast) return null

  const confidence = forecast.confidence || 0
  const factors = [
    { label: 'Data Quality', value: Math.min(100, confidence + 10), color: '#10b981' },
    { label: 'Model Reliability', value: Math.min(100, confidence + 5), color: '#3b82f6' },
    { label: 'Temporal Stability', value: Math.max(0, confidence - 10), color: '#f59e0b' },
    { label: 'Statistical Confidence', value: confidence, color: '#8b5cf6' },
  ]

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Target size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-slate-900">Confidence Breakdown</h3>
      </div>

      <div className="space-y-2">
        {factors.map((f, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className="text-[10px] text-slate-500 w-28">{f.label}</span>
            <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${f.value}%`, background: f.color }} />
            </div>
            <span className="text-[10px] font-semibold text-slate-700">{f.value}%</span>
          </div>
        ))}
      </div>

      <div className="mt-3 pt-2 border-t border-slate-100">
        <p className="text-[10px] text-slate-400">
          Overall confidence: {confidence}% — {confidence >= 75 ? 'High reliability' : confidence >= 50 ? 'Moderate reliability' : 'Low reliability'}
        </p>
      </div>
    </div>
  )
}
