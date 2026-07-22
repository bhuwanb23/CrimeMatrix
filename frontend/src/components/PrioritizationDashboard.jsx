import { useState, useEffect, useCallback } from 'react'
import { Zap, RefreshCw, AlertTriangle, Users, BarChart3, TrendingUp } from 'lucide-react'
import { getPriorityStats, getPriorityRankings, batchScorePriorities, getWorkload } from '../services/priorities'

const priorityColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }

export default function PrioritizationDashboard() {
  const [stats, setStats] = useState(null)
  const [rankings, setRankings] = useState([])
  const [workload, setWorkload] = useState([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState(false)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [statsRes, rankRes, workloadRes] = await Promise.all([
        getPriorityStats(), getPriorityRankings(10), getWorkload()
      ])
      setStats(statsRes?.data || statsRes)
      setRankings(rankRes?.data || [])
      setWorkload(workloadRes?.data || [])
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }, [])

  useEffect(() => { loadData() }, [loadData])

  async function handleBatchScore() {
    setScoring(true)
    try { await batchScorePriorities(); await loadData() } catch (e) { console.error(e) } finally { setScoring(false) }
  }

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Zap size={22} className="text-amber-500" />
          <div>
            <h1 className="text-xl font-bold text-slate-900">Case Prioritization</h1>
            <p className="text-xs text-slate-500">Dynamic investigation prioritization</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleBatchScore} disabled={scoring} className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-slate-900 rounded-lg text-xs font-semibold hover:opacity-90 disabled:opacity-50">
            {scoring ? 'Scoring...' : 'Batch Score All'}
          </button>
          <button onClick={loadData} disabled={loading} className="p-1.5 bg-white border border-slate-200 rounded-lg hover:border-amber-500">
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: 'Scored', value: stats.total_scored || 0, icon: BarChart3, color: 'text-amber-500' },
            { label: 'Critical', value: stats.critical || 0, icon: AlertTriangle, color: 'text-red-500' },
            { label: 'High', value: stats.high || 0, icon: AlertTriangle, color: 'text-orange-500' },
            { label: 'Avg Score', value: `${stats.avg_score || 0}%`, icon: TrendingUp, color: 'text-blue-500' },
          ].map((card, i) => (
            <div key={i} className="flex items-center gap-3 bg-white border border-slate-200 rounded-xl p-3.5">
              <div className={`w-9 h-9 flex items-center justify-center bg-slate-50 rounded-lg ${card.color}`}>
                <card.icon size={18} />
              </div>
              <div>
                <span className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wide">{card.label}</span>
                <span className="text-xl font-bold text-slate-900">{card.value}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {/* Priority Queue */}
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Zap size={14} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-slate-900">Priority Queue</h3>
          </div>
          {rankings.length === 0 ? (
            <p className="text-xs text-slate-400 text-center py-8">No priorities scored yet</p>
          ) : (
            <div className="flex flex-col gap-2">
              {rankings.map((r, i) => {
                const color = priorityColors[r.priority_level] || '#64748b'
                return (
                  <div key={r.investigation_id || i}
                    className="flex items-center gap-2.5 p-2 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors"
                    onClick={() => {}}>
                    <span className="text-xs font-bold text-amber-500 w-5">#{i + 1}</span>
                    <div className="flex-1 min-w-0">
                      <span className="block text-xs font-medium text-slate-900 truncate">{r.title}</span>
                      <div className="h-1.5 bg-slate-200 rounded-full mt-1 overflow-hidden">
                        <div className="h-full rounded-full" style={{ width: `${r.overall_score}%`, background: color }} />
                      </div>
                      <div className="flex items-center justify-between mt-0.5">
                        <span className="text-[10px] text-slate-400">{r.district}</span>
                        <span className="text-[10px] font-semibold uppercase" style={{ color }}>{r.priority_level}</span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Officer Workload */}
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Users size={14} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-slate-900">Officer Workload</h3>
          </div>
          {workload.length === 0 ? (
            <p className="text-xs text-slate-400 text-center py-8">No workload data</p>
          ) : (
            <div className="flex flex-col gap-2">
              {workload.map((w, i) => (
                <div key={i} className="flex items-center justify-between p-2 bg-slate-50 rounded-lg">
                  <span className="text-xs font-medium text-slate-900">Officer #{w.officer_id}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] text-slate-500">{w.count} cases</span>
                    {w.high_priority > 0 && (
                      <span className="text-[10px] font-semibold text-red-500">{w.high_priority} high</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
