import { useState, useEffect } from 'react'
import { Activity, RefreshCw } from 'lucide-react'
import { getEvaluationStats, runEvaluation, getEvaluationResults } from '../../services/analytics'
import { useLanguage } from '../../context/LanguageContext'


export default function ModelEvaluationPanel() {
  const { t } = useLanguage()
  const [stats, setStats] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [statsRes, resultsRes] = await Promise.all([getEvaluationStats(), getEvaluationResults()])
      setStats(statsRes?.data || statsRes)
      setResults(resultsRes?.data?.items || [])
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  async function handleRun() {
    setRunning(true)
    try { await runEvaluation(); await loadData() } catch (e) { console.error(e) } finally { setRunning(false) }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Activity size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('Model Evaluation')}</h3>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleRun} disabled={running} className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
            {running ? t('Running...') : t('Run Evaluation')}
          </button>
          <button onClick={loadData} disabled={loading} className="p-1 hover:bg-slate-100 rounded">
            <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-2 mb-3">
          {[
            { label: t('Metrics'), value: stats.total_metrics || 0 },
            { label: t('Feedback'), value: stats.total_feedback || 0 },
            { label: t('Evaluations'), value: stats.total_evaluations || 0 },
            { label: t('Avg Rating'), value: `${stats.avg_rating || 0}/5` },
          ].map((s, i) => (
            <div key={i} className="text-center p-2 bg-slate-50 rounded-lg">
              <span className="block text-lg font-bold text-slate-900">{s.value}</span>
              <span className="text-[9px] text-slate-400 uppercase">{s.label}</span>
            </div>
          ))}
        </div>
      )}

      {results.length > 0 && (
        <div className="space-y-1.5">
          {results.slice(0, 5).map((r, i) => (
            <div key={i} className="flex items-center justify-between p-1.5 bg-slate-50 rounded text-[10px]">
              <span className="text-slate-600">{r.model_name} — {t(r.evaluation_type)}</span>
              <div className="flex items-center gap-2">
                <span className="text-slate-500">{t('Acc:')} {r.accuracy}%</span>
                <span className="text-slate-500">{t('F1:')} {r.f1_score}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
