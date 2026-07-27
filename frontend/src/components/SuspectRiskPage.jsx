import { useLanguage } from '../context/LanguageContext'
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
  const { t } = useLanguage()
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
      const raw = rankingsRes?.data || []
      const list = Array.isArray(raw) ? raw : (raw.items || [])
      const seen = new Set()
      const unique = list.filter((r) => {
        const id = String(r.suspect_id ?? r.id ?? '')
        if (!id || seen.has(id)) return false
        seen.add(id)
        return true
      })
      setRankings(unique)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }, [])

  useEffect(() => { loadData() }, [loadData])

  useEffect(() => {
    if (rankings.length > 0 && selectedSuspect == null) {
      handleSelectSuspect(rankings[0].suspect_id)
    }
  }, [rankings, selectedSuspect])

  async function handleBatchScore() {
    setScoring(true)
    try { await batchScoreSuspects(); await loadData() } catch (e) { console.error(e) } finally { setScoring(false) }
  }

  async function handleSelectSuspect(suspectId) {
    const id = suspectId == null ? null : String(suspectId)
    setSelectedSuspect(id)
    try {
      const [scoreRes, factorsRes] = await Promise.all([getSuspectRiskScore(suspectId), getSuspectRiskFactors(suspectId)])
      setSelectedScore(scoreRes?.data || null)
      setSelectedFactors(factorsRes?.data?.items || [])
    } catch (e) { console.error(e) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[var(--bg-gradient-from)] to-[var(--bg-gradient-to)] p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-amber-500/20 shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <Shield size={20} />
              </div>
              <div>
                <h1 className="text-lg font-bold">Suspect Risk Scoring</h1>
                <p className="text-white/80 text-xs">Transparent, evidence-backed risk assessment engine</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={handleBatchScore} disabled={scoring}
                className="flex items-center gap-1.5 px-4 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-xs font-semibold transition-all disabled:opacity-50">
                {scoring ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
                {scoring ? t('Scoring...') : t('Score All Suspects')}
              </button>
              <button onClick={loadData} disabled={loading}
                className="p-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
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
              <div key={i} className="bg-[var(--bg-card)] rounded-2xl p-5 shadow-sm border border-[var(--border)] hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center text-white shadow-lg`}>
                    <card.icon size={18} />
                  </div>
                  <ArrowUpRight size={14} className="text-[var(--text-muted)]" />
                </div>
                <span className="block text-2xl font-bold text-[var(--text-primary)]">{card.value}</span>
                <span className="text-xs text-[var(--text-muted)] font-medium">{t(card.label)}</span>
              </div>
            ))}
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-12 gap-5">
          {/* Suspect Rankings (4 cols) */}
          <div className="col-span-4 bg-[var(--bg-card)] rounded-2xl shadow-sm border border-[var(--border)] overflow-hidden">
            <div className="px-5 py-4 border-b border-[var(--border)] flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[var(--bg-active)] flex items-center justify-center">
                  <Shield size={16} className="text-amber-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-[var(--text-primary)]">{t('Suspect Rankings')}</h3>
                  <p className="text-[10px] text-[var(--text-muted)]">{rankings.length} analyzed</p>
                </div>
              </div>
            </div>
            <div className="divide-y divide-[var(--border)] max-h-[520px] overflow-y-auto">
              {rankings.length === 0 ? (
                <div className="py-12 text-center">
                  <UserX size={32} className="text-[var(--text-muted)] mx-auto mb-2" />
                  <p className="text-xs text-[var(--text-muted)]">{t('No suspects scored yet')}</p>
                  <button onClick={handleBatchScore} className="mt-2 text-xs text-amber-500 font-medium hover:underline">
                    {t('Click "Score All" to begin')}
                  </button>
                </div>
              ) : (
                rankings.map((r, i) => {
                  const color = riskColors[r.risk_level] || '#64748b'
                  const rowId = String(r.suspect_id ?? '')
                  const isSelected = selectedSuspect != null && selectedSuspect === rowId
                  return (
                    <div key={`${rowId}-${i}`}
                      className={`px-5 py-3.5 cursor-pointer transition-all duration-200 hover:bg-[var(--bg-hover)] ${isSelected ? 'bg-[var(--bg-active)] border-l-4 border-l-amber-500' : 'border-l-4 border-l-transparent'}`}
                      onClick={() => handleSelectSuspect(r.suspect_id)}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className="w-7 h-7 rounded-lg bg-[var(--bg-input)] flex items-center justify-center text-xs font-bold text-[var(--text-muted)]">
                            {i + 1}
                          </span>
                          <div>
                            <span className="text-sm font-semibold text-[var(--text-primary)] block">{r.name}</span>
                            <span className="text-[10px] text-[var(--text-muted)]">{r.district}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className="text-lg font-bold" style={{ color }}>{r.overall_score}%</span>
                          <span className="block text-[10px] font-semibold uppercase" style={{ color }}>{t(r.risk_level)}</span>
                        </div>
                      </div>
                      <div className="h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-700 ease-out" style={{ width: `${r.overall_score}%`, background: `linear-gradient(90deg, ${color}, ${color}aa)` }} />
                      </div>
                    </div>
                  )
                })
              )}
            </div>
          </div>

          {/* Score Breakdown (8 cols) */}
          <div className="col-span-8 bg-[var(--bg-card)] rounded-2xl shadow-sm border border-[var(--border)] overflow-hidden">
            <div className="px-5 py-4 border-b border-[var(--border)] flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[var(--bg-active)] flex items-center justify-center">
                  <Activity size={16} className="text-blue-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-[var(--text-primary)]">{t('Risk Analysis')}</h3>
                  <p className="text-[10px] text-[var(--text-muted)]">
                    {selectedScore ? `${t('Analyzing')} ${rankings.find(r => String(r.suspect_id) === String(selectedSuspect))?.name || t('suspect')}` : t('Select a suspect to analyze')}
                  </p>
                </div>
              </div>
            </div>

            {selectedScore ? (
              <div className="p-5">
                {/* Score Hero */}
                <div className="flex items-center gap-6 mb-6 pb-6 border-b border-[var(--border)]">
                  <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${riskGradients[selectedScore.risk_level] || 'from-[var(--text-muted)] to-[var(--text-secondary)]'} flex flex-col items-center justify-center text-white shadow-lg`}>
                    <span className="text-2xl font-extrabold">{selectedScore.overall_score}%</span>
                    <span className="text-[9px] font-bold uppercase tracking-wider opacity-80">{t(selectedScore.risk_level)}</span>
                  </div>
                  <div className="flex-1 space-y-2">
                    {selectedScore.explanation?.slice(0, 3).map((exp, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm text-[var(--text-secondary)]">
                        <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                        <span>{t(exp)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Factor Analysis */}
                <div>
                  <h4 className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider mb-3">{t('Contributing Factors')}</h4>
                  <div className="space-y-3">
                    {factorConfig.map((factor) => {
                      const value = selectedFactors.find(f => f.name === factor.key)?.value || 0
                      return (
                        <div key={factor.key} className="group">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-medium text-[var(--text-secondary)]">{t(factor.label)}</span>
                            <span className="text-xs font-bold text-[var(--text-primary)]">{value}%</span>
                          </div>
                          <div className="h-2 bg-[var(--bg-input)] rounded-full overflow-hidden">
                            <div className="h-full rounded-full transition-all duration-700 ease-out group-hover:opacity-100 opacity-90"
                              style={{ width: `${value}%`, background: `linear-gradient(90deg, ${factor.color}, ${factor.color}cc)` }} />
                          </div>
                          <span className="text-[10px] text-[var(--text-muted)] mt-0.5 block">{t(factor.desc)}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-20">
                <div className="w-16 h-16 rounded-2xl bg-[var(--bg-input)] flex items-center justify-center mb-4">
                  <AlertTriangle size={24} className="text-[var(--text-muted)]" />
                </div>
                <p className="text-sm font-medium text-[var(--text-muted)] mb-1">{t('No suspect selected')}</p>
                <p className="text-xs text-[var(--text-muted)]">{t('Click on a suspect from the rankings to view their detailed risk analysis')}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
