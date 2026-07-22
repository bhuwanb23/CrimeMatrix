import { useState, useEffect, useCallback } from 'react'
import { Shield, RefreshCw, AlertTriangle, TrendingUp, Users, Zap, ArrowUpRight, Activity, UserX } from 'lucide-react'
import { getSuspectRiskStats, getSuspectRiskRankings, batchScoreSuspects, getSuspectRiskScore, getSuspectRiskFactors } from '../services/suspectRisk'

const riskColors = { very_high: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }
const riskGradients = {
  very_high: 'from-red-500 to-rose-600',
  high: 'from-amber-500 to-orange-500',
  medium: 'from-blue-500 to-indigo-500',
  low: 'from-emerald-500 to-teal-500',
}

const factorConfig = [
  { key: 'criminal_history', label: 'Criminal History', color: '#ef4444', desc: 'Prior offense records' },
  { key: 'offense_severity', label: 'Offense Severity', color: '#f59e0b', desc: 'Severity of past crimes' },
  { key: 'age_factor', label: 'Age Factor', color: '#3b82f6', desc: 'Age-related risk assessment' },
  { key: 'location_risk', label: 'Location Risk', color: '#10b981', desc: 'High-risk area indicators' },
  { key: 'associate_risk', label: 'Associate Risk', color: '#8b5cf6', desc: 'Known criminal associates' },
  { key: 'recency', label: 'Recency', color: '#06b6d4', desc: 'Time since last offense' },
  { key: 'network_influence', label: 'Network Influence', color: '#ec4899', desc: 'Criminal network connections' },
  { key: 'mo_similarity', label: 'MO Similarity', color: '#f97316', desc: 'Modus operandi pattern match' },
  { key: 'investigation_links', label: 'Investigation Links', color: '#84cc16', desc: 'Active investigation connections' },
  { key: 'behavioral', label: 'Behavioral', color: '#a855f7', desc: 'Behavioral profile analysis' },
]

export default function SuspectRiskPage() {
  const [stats, setStats] = useState(null)
  const [rankings, setRankings] = useState([])
  const [selectedSuspect, setSelectedSuspect] = useState(null)
  const [selectedScore, setSelectedScore] = useState(null)
  const [selectedFactors, setSelectedFactors] = useState([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState(false)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [statsRes, rankingsRes] = await Promise.all([getSuspectRiskStats(), getSuspectRiskRankings(10)])
      setStats(statsRes?.data || statsRes)
      const ranks = rankingsRes?.data || []
      setRankings(ranks)
      if (ranks.length > 0 && !selectedSuspect) {
        handleSelectSuspect(ranks[0].suspect_id)
      }
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }, [selectedSuspect])

  async function handleBatchScore() {
    setScoring(true)
    try { await batchScoreSuspects(); await loadData() } catch (e) { console.error(e) } finally { setScoring(false) }
  }

  async function handleSelectSuspect(suspectId) {
    setSelectedSuspect(suspectId)
    try {
      const [scoreRes, factorsRes] = await Promise.all([getSuspectRiskScore(suspectId), getSuspectRiskFactors(suspectId)])
      setSelectedScore(scoreRes?.data || null)
      setSelectedFactors(factorsRes?.data?.items || [])
    } catch (e) { console.error(e) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 rounded-2xl p-6 text-white shadow-lg shadow-amber-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Shield size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Suspect Risk Scoring</h1>
                <p className="text-white/80 text-sm mt-0.5">Transparent, evidence-backed risk assessment engine</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button onClick={handleBatchScore} disabled={scoring}
                className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                {scoring ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
                {scoring ? 'Scoring...' : 'Score All Suspects'}
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
              { label: 'Total Scored', value: stats.total_scored || 0, icon: Users, gradient: 'from-blue-500 to-indigo-500' },
              { label: 'Critical Risk', value: stats.critical || 0, icon: AlertTriangle, gradient: 'from-red-500 to-rose-500' },
              { label: 'High Risk', value: stats.high || 0, icon: AlertTriangle, gradient: 'from-amber-500 to-orange-500' },
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
          {/* Suspect Rankings (4 cols) */}
          <div className="col-span-4 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
                  <Shield size={16} className="text-amber-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Suspect Rankings</h3>
                  <p className="text-[10px] text-slate-400">{rankings.length} analyzed</p>
                </div>
              </div>
            </div>
            <div className="divide-y divide-slate-50">
              {rankings.length === 0 ? (
                <div className="py-12 text-center">
                  <UserX size={32} className="text-slate-200 mx-auto mb-2" />
                  <p className="text-xs text-slate-400">No suspects scored yet</p>
                  <button onClick={handleBatchScore} className="mt-2 text-xs text-amber-500 font-medium hover:underline">
                    Click "Score All" to begin
                  </button>
                </div>
              ) : (
                rankings.map((r, i) => {
                  const color = riskColors[r.risk_level] || '#64748b'
                  const isSelected = selectedSuspect === r.suspect_id
                  return (
                    <div key={r.suspect_id || i}
                      className={`px-5 py-3.5 cursor-pointer transition-all duration-200 hover:bg-slate-50 ${isSelected ? 'bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-l-amber-500' : ''}`}
                      onClick={() => handleSelectSuspect(r.suspect_id)}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500">
                            {i + 1}
                          </span>
                          <div>
                            <span className="text-sm font-semibold text-slate-900 block">{r.name}</span>
                            <span className="text-[10px] text-slate-400">{r.district}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className="text-lg font-bold" style={{ color }}>{r.overall_score}%</span>
                          <span className="block text-[10px] font-semibold uppercase" style={{ color }}>{r.risk_level}</span>
                        </div>
                      </div>
                      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-700 ease-out" style={{ width: `${r.overall_score}%`, background: `linear-gradient(90deg, ${color}, ${color}aa)` }} />
                      </div>
                    </div>
                  )
                })
              )}
            </div>
          </div>

          {/* Score Breakdown (8 cols) */}
          <div className="col-span-8 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Activity size={16} className="text-blue-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Risk Analysis</h3>
                  <p className="text-[10px] text-slate-400">
                    {selectedScore ? `Analyzing ${rankings.find(r => r.suspect_id === selectedSuspect)?.name || 'suspect'}` : 'Select a suspect to analyze'}
                  </p>
                </div>
              </div>
            </div>

            {selectedScore ? (
              <div className="p-5">
                {/* Score Hero */}
                <div className="flex items-center gap-6 mb-6 pb-6 border-b border-slate-100">
                  <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${riskGradients[selectedScore.risk_level] || 'from-slate-400 to-slate-500'} flex flex-col items-center justify-center text-white shadow-lg`}>
                    <span className="text-2xl font-extrabold">{selectedScore.overall_score}%</span>
                    <span className="text-[9px] font-bold uppercase tracking-wider opacity-80">{selectedScore.risk_level}</span>
                  </div>
                  <div className="flex-1 space-y-2">
                    {selectedScore.explanation?.slice(0, 3).map((exp, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm text-slate-600">
                        <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                        <span>{exp}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Factor Analysis */}
                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Contributing Factors</h4>
                  <div className="space-y-3">
                    {factorConfig.map((factor) => {
                      const value = selectedFactors.find(f => f.name === factor.key)?.value || 0
                      return (
                        <div key={factor.key} className="group">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-medium text-slate-600">{factor.label}</span>
                            <span className="text-xs font-bold text-slate-900">{value}%</span>
                          </div>
                          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                            <div className="h-full rounded-full transition-all duration-700 ease-out group-hover:opacity-100 opacity-90"
                              style={{ width: `${value}%`, background: `linear-gradient(90deg, ${factor.color}, ${factor.color}cc)` }} />
                          </div>
                          <span className="text-[10px] text-slate-400 mt-0.5 block">{factor.desc}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-20">
                <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
                  <AlertTriangle size={24} className="text-slate-300" />
                </div>
                <p className="text-sm font-medium text-slate-500 mb-1">No suspect selected</p>
                <p className="text-xs text-slate-400">Click on a suspect from the rankings to view their detailed risk analysis</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
