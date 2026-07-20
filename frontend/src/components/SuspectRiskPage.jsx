import { useState, useEffect } from 'react'
import { Shield, RefreshCw, AlertTriangle, TrendingUp, Users } from 'lucide-react'
import { getSuspectRiskStats, getSuspectRiskRankings, batchScoreSuspects, getSuspectRiskScore, getSuspectRiskFactors } from '../services/suspectRisk'

const riskColors = {
  very_high: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

const factorColors = {
  criminal_history: '#ef4444',
  offense_severity: '#f59e0b',
  age_factor: '#3b82f6',
  location_risk: '#10b981',
  associate_risk: '#8b5cf6',
  recency: '#06b6d4',
  network_influence: '#ec4899',
  mo_similarity: '#f97316',
  investigation_links: '#84cc16',
  behavioral: '#a855f7',
}

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
      setRankings(rankingsRes?.data || [])
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  async function handleBatchScore() {
    setScoring(true)
    try { await batchScoreSuspects(); await loadData() } catch (e) { console.error(e) } finally { setScoring(false) }
  }

  async function handleSelectSuspect(suspectId) {
    if (selectedSuspect === suspectId) { setSelectedSuspect(null); setSelectedScore(null); setSelectedFactors([]); return }
    setSelectedSuspect(suspectId)
    try {
      const [scoreRes, factorsRes] = await Promise.all([getSuspectRiskScore(suspectId), getSuspectRiskFactors(suspectId)])
      setSelectedScore(scoreRes?.data || null)
      setSelectedFactors(factorsRes?.data?.items || [])
    } catch (e) { console.error(e) }
  }

  return (
    <div className="flex flex-col gap-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Shield size={22} className="text-amber-500" />
          <div>
            <h1 className="text-xl font-bold text-slate-900">Suspect Risk Scoring</h1>
            <p className="text-xs text-slate-500">Transparent, explainable risk assessment</p>
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

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Scored', value: stats.total_scored || 0, icon: Users, color: 'text-amber-500' },
            { label: 'High Risk', value: stats.high_risk || 0, icon: AlertTriangle, color: 'text-red-500' },
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
        {/* Rankings */}
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Shield size={14} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-slate-900">Suspect Rankings</h3>
          </div>
          {rankings.length === 0 ? (
            <p className="text-xs text-slate-400 text-center py-8">No suspects scored yet. Click Batch Score.</p>
          ) : (
            <div className="flex flex-col gap-2">
              {rankings.map((r, i) => {
                const color = riskColors[r.risk_level] || '#64748b'
                const isSelected = selectedSuspect === r.suspect_id
                return (
                  <div key={r.suspect_id || i}
                    className={`flex items-center gap-2.5 p-2 rounded-lg cursor-pointer transition-all ${isSelected ? 'bg-amber-50 border border-amber-400' : 'bg-slate-50 border border-transparent hover:border-slate-200'}`}
                    onClick={() => handleSelectSuspect(r.suspect_id)}>
                    <span className="text-xs font-bold text-amber-500 w-5">#{i + 1}</span>
                    <div className="flex-1 min-w-0">
                      <span className="block text-xs font-medium text-slate-900">{r.name}</span>
                      <div className="h-1.5 bg-slate-200 rounded-full mt-1 overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${r.overall_score}%`, background: color }} />
                      </div>
                      <div className="flex items-center justify-between mt-0.5">
                        <span className="text-[10px] text-slate-400">{r.district}</span>
                        <span className="text-[10px] font-semibold uppercase" style={{ color }}>{r.risk_level}</span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Score Breakdown */}
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle size={14} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-slate-900">Score Breakdown</h3>
          </div>
          {selectedScore ? (
            <div className="flex flex-col gap-2.5">
              <div className="flex items-center gap-2.5 pb-2.5 border-b border-slate-100">
                <span className="text-3xl font-extrabold" style={{ color: riskColors[selectedScore.risk_level] }}>
                  {selectedScore.overall_score}%
                </span>
                <span className="text-sm font-semibold uppercase" style={{ color: riskColors[selectedScore.risk_level] }}>
                  {selectedScore.risk_level}
                </span>
              </div>
              {selectedScore.explanation?.map((exp, i) => (
                <div key={i} className="flex items-center gap-1.5 text-[11px] text-slate-600">
                  <AlertTriangle size={10} className="text-amber-500" />
                  <span>{exp}</span>
                </div>
              ))}
              {selectedFactors.length > 0 && (
                <div className="flex flex-col gap-1.5 mt-2">
                  {selectedFactors.map((f, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <span className="text-[10px] text-slate-500 w-24 capitalize">{f.name.replace(/_/g, ' ')}</span>
                      <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${f.value}%`, background: factorColors[f.name] || '#64748b' }} />
                      </div>
                      <span className="text-[10px] font-semibold text-slate-900 w-7 text-right">{f.value}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-slate-400 text-center py-8">Select a suspect to view breakdown</p>
          )}
        </div>
      </div>
    </div>
  )
}
