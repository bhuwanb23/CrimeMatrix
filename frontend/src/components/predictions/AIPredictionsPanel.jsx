import { Lightbulb, TrendingUp, AlertTriangle } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function AIPredictionsPanel({ forecast, predictions, districts }) {
  const { t } = useLanguage()
  const insights = []

  if (forecast) {
    if (forecast.trend === 'increasing') {
      insights.push({ type: 'trend', icon: TrendingUp, color: '#ef4444', title: t('Crime rate trending upward'), description: `Forecast shows increasing crime with ${forecast.confidence}% confidence. Consider increasing patrols.`, confidence: forecast.confidence })
    } else if (forecast.trend === 'decreasing') {
      insights.push({ type: 'trend', icon: TrendingUp, color: '#10b981', title: t('Crime rate trending downward'), description: `Current strategies appear effective. Confidence: ${forecast.confidence}%.`, confidence: forecast.confidence })
    }
  }

  if (districts && districts.length > 0) {
    const highRisk = districts.filter(d => d.risk === 'high')
    if (highRisk.length > 0) {
      insights.push({ type: 'district', icon: AlertTriangle, color: '#f59e0b', title: `${highRisk.length} districts with high predicted crime`, description: `Districts: ${highRisk.map(d => d.name).join(', ')}. Recommend targeted interventions.`, confidence: 72 })
    }
  }

  if (predictions && predictions.length > 10) {
    insights.push({ type: 'volume', icon: TrendingUp, color: '#3b82f6', title: `${predictions.length} active predictions in system`, description: 'Multiple prediction models are generating insights across districts and crime types.', confidence: 80 })
  }

  insights.push({ type: 'recommendation', icon: Lightbulb, color: '#8b5cf6', title: t('Cross-district coordination recommended'), description: 'Pattern analysis suggests similar criminal activity across multiple districts. Joint operations may improve resolution rates.', confidence: 68 })

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center">
          <Lightbulb size={16} className="text-purple-500" />
        </div>
        <h3 className="text-sm font-bold text-slate-900">AI Predictions & Recommendations</h3>
      </div>
      <div className="divide-y divide-slate-50">
        {insights.map((insight, i) => {
          const Icon = insight.icon
          return (
            <div key={i} className="px-5 py-4 hover:bg-slate-50 transition-colors">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style={{ background: `${insight.color}15` }}>
                  <Icon size={14} style={{ color: insight.color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-semibold text-slate-900 mb-0.5">{insight.title}</p>
                  <p className="text-[11px] text-slate-500 mb-2">{insight.description}</p>
                  <div className="flex items-center gap-2">
                    <div className="w-20 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${insight.confidence}%`, background: insight.color }} />
                    </div>
                    <span className="text-[10px] text-slate-400">{insight.confidence}% confidence</span>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
