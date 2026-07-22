import { useState, useEffect, useCallback } from 'react'
import { Zap, RefreshCw, AlertTriangle, Users, BarChart3, Clock, ChevronRight, ArrowUpRight, TrendingUp } from 'lucide-react'
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-2xl p-6 text-white shadow-lg shadow-violet-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Zap size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Case Prioritization</h1>
                <p className="text-white/80 text-sm mt-0.5">Dynamic investigation prioritization engine</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button onClick={handleBatchScore} disabled={scoring}
                className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                {scoring ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
                {scoring ? 'Scoring...' : 'Score All Investigations'}
              </button>
              <button onClick={loadData} disabled={loading}
                className="p-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
                <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-4 gap-4">
            {[
              { label: 'Total Scored', value: stats.total_scored || 0, icon: BarChart3, gradient: 'from-violet-500 to-purple-500' },
              { label: 'Critical Priority', value: stats.critical || 0, icon: AlertTriangle, gradient: 'from-red-500 to-rose-500' },
              { label: 'High Priority', value: stats.high || 0, icon: AlertTriangle, gradient: 'from-amber-500 to-orange-500' },
              { label: 'Average Score', value: `${stats.avg_score || 0}%`, icon: TrendingUp, gradient: 'from-emerald-500 to-teal-500' },
            ].map((card, i) => (
              <div key={i} className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center text-white shadow-lg`}>
                    <card.icon size={18} />
                  </div>
                  <ArrowUpRight size={14} className="text-slate-300" />
                </div>
                <span className="block text-2xl font-bold text-slate-900">{card.value}</span>
                <span className="text-xs text-slate-400 font-medium">{card.label}</span>
              </div>
            ))}
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-12 gap-5">
          {/* Priority Queue (7 cols) */}
          <div className="col-span-7 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-violet-50 flex items-center justify-center">
                  <Zap size={16} className="text-violet-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Priority Queue</h3>
                  <p className="text-[10px] text-slate-400">Investigations ranked by urgency</p>
                </div>
              </div>
              <span className="text-[10px] text-slate-400">{rankings.length} items</span>
            </div>
            <div className="divide-y divide-slate-50">
              {rankings.length === 0 ? (
                <div className="py-12 text-center">
                  <Zap size={32} className="text-slate-200 mx-auto mb-2" />
                  <p className="text-xs text-slate-400">No priorities scored yet</p>
                  <button onClick={handleBatchScore} className="mt-2 text-xs text-violet-500 font-medium hover:underline">
                    Click "Score All" to begin
                  </button>
                </div>
              ) : (
                rankings.map((r, i) => {
                  const color = priorityColors[r.priority_level] || '#64748b'
                  return (
                    <div key={r.investigation_id || i}
                      className="px-5 py-3.5 hover:bg-slate-50 transition-all cursor-pointer">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500">
                            {i + 1}
                          </span>
                          <div>
                            <span className="text-sm font-semibold text-slate-900 block">{r.title}</span>
                            <span className="text-[10px] text-slate-400">{r.district} • {r.progress || 0}% progress</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className="text-lg font-bold" style={{ color }}>{r.overall_score}%</span>
                          <span className="block text-[10px] font-semibold uppercase" style={{ color }}>{r.priority_level}</span>
                        </div>
                      </div>
                      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${r.overall_score}%`, background: `linear-gradient(90deg, ${color}, ${color}aa)` }} />
                      </div>
                    </div>
                  )
                })
              )}
            </div>
          </div>

          {/* Officer Workload (5 cols) */}
          <div className="col-span-5 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Users size={16} className="text-blue-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Officer Workload</h3>
                  <p className="text-[10px] text-slate-400">Case distribution across officers</p>
                </div>
              </div>
            </div>
            <div className="divide-y divide-slate-50">
              {workload.length === 0 ? (
                <div className="py-12 text-center">
                  <Users size={32} className="text-slate-200 mx-auto mb-2" />
                  <p className="text-xs text-slate-400">No workload data available</p>
                </div>
              ) : (
                workload.map((w, i) => (
                  <div key={i} className="px-5 py-3.5 hover:bg-slate-50 transition-all">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                          <Users size={14} className="text-blue-500" />
                        </div>
                        <span className="text-sm font-semibold text-slate-900">Officer #{w.officer_id}</span>
                      </div>
                      <span className="text-xs text-slate-400">{w.count} cases</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-blue-500" style={{ width: `${Math.min(100, w.count * 10)}%` }} />
                      </div>
                      {w.high_priority > 0 && (
                        <span className="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded-full">
                          {w.high_priority} high
                        </span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
