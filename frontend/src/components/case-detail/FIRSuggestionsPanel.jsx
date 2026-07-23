import { useState, useEffect, useCallback } from 'react'
import { Lightbulb, ExternalLink, Shield, MapPin, Crosshair } from 'lucide-react'
import { analyzeFIR, getFIRSuggestions } from '../../services/firIntelligence'
import { useLanguage } from '../../context/LanguageContext'

const typeConfig = {
  similar_case: { icon: ExternalLink, label: 'Similar Case', color: '#3b82f6' },
  mo_match: { icon: Crosshair, label: 'MO Match', color: '#f59e0b' },
  suspect: { icon: Shield, label: 'Suspect', color: '#ef4444' },
  vehicle: { icon: MapPin, label: 'Vehicle', color: '#8b5cf6' },
  phone: { icon: Shield, label: 'Phone', color: '#10b981' },
}

export default function FIRSuggestionsPanel({ firId }) {
  const { t } = useLanguage()
  const [suggestions, setSuggestions] = useState([])
  const [loading, setLoading] = useState(false)
  const [analyzed, setAnalyzed] = useState(false)

  const loadSuggestions = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getFIRSuggestions(firId)
      const data = res?.data || res
      setSuggestions(data?.items || [])
      setAnalyzed((data?.items || []).length > 0)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }, [firId])

  useEffect(() => {
    if (firId) loadSuggestions()
  }, [firId, loadSuggestions])

  async function handleAnalyze() {
    setLoading(true)
    try {
      await analyzeFIR(firId)
      await loadSuggestions()
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Lightbulb size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('FIR Intelligence')}</h3>
        </div>
        {!analyzed && (
          <button onClick={handleAnalyze} disabled={loading}
            className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
            {loading ? t('Analyzing...') : t('Analyze FIR')}
          </button>
        )}
      </div>

      {loading && suggestions.length === 0 ? (
        <div className="py-8 text-center">
          <div className="w-5 h-5 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs text-slate-400">{t('Analyzing FIR...')}</p>
        </div>
      ) : suggestions.length === 0 ? (
        <div className="py-8 text-center">
          <Lightbulb size={24} className="text-slate-200 mx-auto mb-2" />
          <p className="text-xs text-slate-400">{t('No suggestions yet')}</p>
          <p className="text-[10px] text-slate-300">{t('Click "Analyze FIR" to generate intelligence')}</p>
        </div>
      ) : (
        <div className="divide-y divide-slate-50">
          {suggestions.map((s, i) => {
            const config = typeConfig[s.suggestion_type] || { icon: Lightbulb, label: 'Suggestion', color: '#64748b' }
            const Icon = config.icon
            return (
              <div key={s.id || i} className="px-4 py-3 hover:bg-slate-50 transition-colors">
                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                    style={{ background: `${config.color}15` }}>
                    <Icon size={12} style={{ color: config.color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-0.5">
                      <span className="text-[10px] font-semibold uppercase" style={{ color: config.color }}>{t(config.label)}</span>
                      <span className="text-[10px] text-slate-400">{s.confidence}%</span>
                    </div>
                    <p className="text-xs text-slate-600">{s.suggestion_text}</p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

