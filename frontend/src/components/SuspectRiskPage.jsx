import { useState, useEffect } from 'react'
import { Shield, RefreshCw, AlertTriangle, TrendingUp, Users, ChevronRight, Zap } from 'lucide-react'
import { getSuspectRiskStats, getSuspectRiskRankings, batchScoreSuspects, getSuspectRiskScore, getSuspectRiskFactors } from '../services/suspectRisk'

const riskColors = { very_high: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }

const factorConfig = [
  { key: 'criminal_history', label: 'Criminal History', color: '#ef4444' },
  { key: 'offense_severity', label: 'Offense Severity', color: '#f59e0b' },
  { key: 'age_factor', label: 'Age Factor', color: '#3b82f6' },
  { key: 'location_risk', label: 'Location Risk', color: '#10b981' },
  { key: 'associate_risk', label: 'Associate Risk', color: '#8b5cf6' },
  { key: 'recency', label: 'Recency', color: '#06b6d4' },
  { key: 'network_influence', label: 'Network Influence', color: '#ec4899' },
  { key: 'mo_similarity', label: 'MO Similarity', color: '#f97316' },
  { key: 'investigation_links', label: 'Investigation Links', color: '#84cc16' },
  { key: 'behavioral', label: 'Behavioral', color: '#a855f7' },
]

export default function SuspectRiskPage() {
  const [stats, setStats] = useState(null)
  const [rankings, setRankings] = useState([])
  const [selectedSuspect, setSelectedSuspect] = useState(null)
  const [selectedScore, setSelectedScore] = useState(null)
  const [selectedFactors, setSelectedFactors] = useState([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState(false)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [statsRes, rankingsRes] = await Promise.all([getSuspectRiskStats(), getSuspectRiskRankings(10)])
      setStats(statsRes?.data || statsRes)
      const ranks = rankingsRes?.data || []
      setRankings(ranks)
      // Auto-select first suspect if available
      if (ranks.length > 0 && !selectedSuspect) {
        handleSelectSuspect(ranks[0].suspect_id)
      }
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

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
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center">
            <Shield size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Suspect Risk Scoring</h1>
            <p className="text-xs text-slate-500">Transparent, explainable risk assessment for suspects</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleBatchScore} disabled={scoring}
            className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg text-sm font-semibold hover:opacity-90 disabled:opacity-50 shadow-sm">
            {scoring ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
            {scoring ? 'Scoring...' : 'Batch Score All'}
          </button>
          <button onClick={loadData} disabled={loading}
            className="p-2 bg-white border border-slate-200 rounded-lg hover:border-amber-500">
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: 'Scored', value: stats.total_scored || 0, icon: Users, color: 'text-amber-500', bg: 'bg-amber-50' },
            { label: 'Critical', value: stats.critical || 0, icon: AlertTriangle, color: 'text-red-500', bg: 'bg-red-50' },
            { label: 'High Risk', value: stats.high || 0, icon: AlertTriangle, color: 'text-orange-500', bg: 'bg-orange-50' },
            { label: 'Avg Score', value: `${stats.avg_score || 0}%`, icon: TrendingUp, color: 'text-blue-500', bg: 'bg-blue-50' },
          ].map((card, i) => (
            <div key={i} className={`${card.bg} border border-slate-200 rounded-xl p-4`}>
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${card.color}`} style={{ background: `${card.color === 'text-amber-500' ? '#fef3c7' : card.color === 'text-red-500' ? '#fee2e2' : card.color === 'text-orange-500' ? '#ffedd5' : '#dbeafe'}` }}>
                  <card.icon size={18} />
                </div>
                <div>
                  <span className="block text-2xl font-bold text-slate-900">{card.value}</span>
                  <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wide">{card.label}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Main Content: Rankings + Breakdown */}
      <div className="grid grid-cols-5 gap-4">
        {/* Suspect Rankings (2/5) */}
        <div className="col-span-2 bg-white border border-slate-200 rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield size={14} className="text-amber-500" />
              <h3 className="text-sm font-semibold text-slate-900">Suspect Rankings</h3>
            </div>
            <span className="text-[10px] text-slate-400">{rankings.length} suspects</span>
          </div>
          <div className="divide-y divide-slate-100">
            {rankings.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-400">
                No suspects scored yet. Click "Batch Score All".
              </div>
            ) : (
              rankings.map((r, i) => {
                const color = riskColors[r.risk_level] || '#64748b'
                const isSelected = selectedSuspect === r.suspect_id
                return (
                  <div key={r.suspect_id || i}
                    className={`px-4 py-3 cursor-pointer transition-all hover:bg-slate-50 ${isSelected ? 'bg-amber-50 border-l-4 border-l-amber-500' : ''}`}
                    onClick={() => handleSelectSuspect(r.suspect_id)}>
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-amber-500 w-6">#{i + 1}</span>
                        <span className="text-sm font-medium text-slate-900">{r.name}</span>
                      </div>
                      <span className="text-xs font-bold" style={{ color }}>{r.overall_score}%</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${r.overall_score}%`, background: color }} />
                      </div>
                      <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded" style={{ color, background: `${color}15` }}>{r.risk_level}</span>
                    </div>
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-[10px] text-slate-400">{r.district}</span>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* Score Breakdown (3/5) */}
        <div className="col-span-3 bg-white border border-slate-200 rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle size={14} className="text-amber-500" />
              <h3 className="text-sm font-semibold text-slate-900">Score Breakdown</h3>
            </div>
            {selectedScore && (
              <span className="text-xs text-slate-400">
                {rankings.find(r => r.suspect_id === selectedSuspect)?.name || ''}
              </span>
            )}
          </div>

          {selectedScore ? (
            <div className="p-4">
              {/* Overall Score */}
              <div className="flex items-center gap-4 mb-4 pb-4 border-b border-slate-100">
                <div className="text-center">
                  <span className="text-4xl font-extrabold" style={{ color: riskColors[selectedScore.risk_level] }}>
                    {selectedScore.overall_score}%
                  </span>
                  <span className="block text-xs font-semibold uppercase mt-1" style={{ color: riskColors[selectedScore.risk_level] }}>
                    {selectedScore.risk_level}
                  </span>
                </div>
                <div className="flex-1">
                  {selectedScore.explanation?.slice(0, 2).map((exp, i) => (
                    <div key={i} className="flex items-start gap-1.5 text-xs text-slate-600 mb-1">
                      <AlertTriangle size={10} className="text-amber-500 mt-0.5 flex-shrink-0" />
                      <span>{exp}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Factor Bars */}
              <div className="space-y-2.5">
                {factorConfig.map((factor) => {
                  const value = selectedFactors.find(f => f.name === factor.key)?.value || 0
                  return (
                    <div key={factor.key} className="flex items-center gap-3">
                      <span className="text-xs text-slate-500 w-32 flex-shrink-0">{factor.label}</span>
                      <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${value}%`, background: factor.color }} />
                      </div>
                      <span className="text-xs font-semibold text-slate-700 w-10 text-right">{value}%</span>
                    </div>
                  )
                })}
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-16 text-slate-400">
              <AlertTriangle size={32} className="mb-2 opacity-30" />
              <p className="text-sm">Select a suspect from the rankings to view detailed breakdown</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
