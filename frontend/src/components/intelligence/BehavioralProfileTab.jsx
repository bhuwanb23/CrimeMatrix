import { useState, useEffect } from 'react'
import { Brain, AlertTriangle, Shield, Crosshair, Target, DoorOpen, Clock, RefreshCw, Search } from 'lucide-react'
import { getBehaviorProfiles, getRiskAssessment, analyzeCriminal, getBehaviorStats } from '../../services/behavior'
import { useLanguage } from '../../context/LanguageContext'

const profileIcons = { timing: Clock, weapon: Crosshair, target: Target, method: Shield, entry: DoorOpen }
const riskColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }

export default function BehavioralProfileTab() {
  const { t } = useLanguage()
  const [profiles, setProfiles] = useState([])
  const [riskAssessment, setRiskAssessment] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [analyzeId, setAnalyzeId] = useState('')
  const [expandedProfile, setExpandedProfile] = useState(null)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [profilesRes, riskRes, statsRes] = await Promise.all([
        getBehaviorProfiles(),
        getRiskAssessment(),
        getBehaviorStats(),
      ])
      setProfiles(profilesRes?.data?.items || [])
      setRiskAssessment(riskRes?.data || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load behavior data', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    if (!analyzeId || analyzing) return
    setAnalyzing(true)
    try { await analyzeCriminal(parseInt(analyzeId)); await loadData(); setAnalyzeId('') } catch (e) { console.error(e) } finally { setAnalyzing(false) }
  }

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-6">
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        </div>
      </div>
    )
  }

  const hasData = profiles.length > 0 || riskAssessment.length > 0

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center">
            <Brain size={16} className="text-purple-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Behavioral Profiling</h3>
            <p className="text-[10px] text-slate-400">Analyze criminal behavior patterns</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <input className="w-28 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-amber-400"
            placeholder="Criminal ID" value={analyzeId} onChange={(e) => setAnalyzeId(e.target.value)} />
          <button onClick={handleAnalyze} disabled={analyzing || !analyzeId}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {analyzing ? <RefreshCw size={12} className="animate-spin" /> : <Search size={12} />}
            {analyzing ? 'Analyzing...' : 'Analyze'}
          </button>
          <button onClick={loadData} className="p-1.5 text-slate-400 hover:text-slate-600 transition-colors">
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="px-5 py-3 border-b border-slate-100 flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-slate-900">{stats.total_profiles || 0}</span>
            <span className="text-[10px] text-slate-400">Profiles</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-slate-900">{stats.criminals_profiled || 0}</span>
            <span className="text-[10px] text-slate-400">Criminals</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-red-500">{stats.high_risk || 0}</span>
            <span className="text-[10px] text-slate-400">High Risk</span>
          </div>
        </div>
      )}

      {!hasData ? (
        <div className="text-center py-12">
          <Brain size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No behavioral profiles yet</p>
          <p className="text-xs text-slate-400 mb-4">Enter a Criminal ID above and click Analyze to generate a behavioral profile.</p>
          <div className="inline-block bg-slate-50 rounded-lg px-4 py-3 text-[10px] text-slate-500 text-left max-w-xs">
            <p className="m-0 font-medium text-slate-600 mb-1">How profiling works:</p>
            <ul className="m-0 pl-3 space-y-0.5">
              <li>Analyze a criminal to extract behavior patterns</li>
              <li>Patterns include timing, weapon, target, method, entry</li>
              <li>Risk assessment rates criminals by behavior severity</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="p-5 space-y-5">
          {/* Risk Assessment */}
          {riskAssessment.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <AlertTriangle size={14} className="text-amber-500" />
                <h4 className="text-xs font-semibold text-slate-700">Risk Assessment</h4>
              </div>
              <div className="space-y-2">
                {riskAssessment.map((r, i) => (
                  <div key={i} className="p-3 bg-slate-50 rounded-lg">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-semibold text-slate-900">{r.alias}</span>
                      <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ color: riskColors[r.risk_level], background: `${riskColors[r.risk_level]}15` }}>
                        {r.risk_level}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full rounded-full" style={{ width: `${r.risk_score}%`, background: riskColors[r.risk_level] }} />
                      </div>
                      <span className="text-[10px] font-mono text-slate-400">{r.risk_score}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Profiles */}
          {profiles.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Shield size={14} className="text-emerald-500" />
                <h4 className="text-xs font-semibold text-slate-700">Behavioral Profiles</h4>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {profiles.map((p) => {
                  const Icon = profileIcons[p.profile_type] || Shield
                  const color = riskColors[p.risk_level] || '#10b981'
                  return (
                    <div key={p.id}
                      className="p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors"
                      onClick={() => setExpandedProfile(expandedProfile === p.id ? null : p.id)}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-1.5">
                          <Icon size={12} style={{ color }} />
                          <span className="text-[10px] font-semibold text-slate-700">{p.profile_type}</span>
                        </div>
                        <span className="text-[10px] font-mono text-slate-400">{p.confidence}%</span>
                      </div>
                      <p className="text-[10px] text-slate-500 mb-1.5">{p.pattern_description}</p>
                      <div className="h-1 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full rounded-full" style={{ width: `${p.confidence}%`, background: color }} />
                      </div>
                      {expandedProfile === p.id && (
                        <div className="mt-2 pt-2 border-t border-slate-200 text-[10px] text-slate-400 space-y-0.5">
                          <p className="m-0">Risk: {p.risk_level} ({p.risk_score}%)</p>
                          <p className="m-0">Last analyzed: {p.last_analyzed ? new Date(p.last_analyzed).toLocaleDateString() : 'Never'}</p>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
