import { useState, useEffect } from 'react'
import { UserX, RefreshCw, AlertTriangle, Clock, MapPin, Shield, TrendingUp, Search } from 'lucide-react'
import { listRepeatOffenders, getRepeatOffenderStats, analyzeRepeatOffenders } from '../../services/repeatOffenders'
import { useLanguage } from '../../context/LanguageContext'

const riskColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }

export default function RepeatOffenderTab() {
  const { t } = useLanguage()
  const dimensionConfig = [
    { key: 'frequency_score', label: t('Frequency'), icon: TrendingUp, color: '#f59e0b' },
    { key: 'recency_score', label: t('Recency'), icon: Clock, color: '#ef4444' },
    { key: 'severity_score', label: t('Severity'), icon: Shield, color: '#8b5cf6' },
    { key: 'geographic_score', label: t('Geographic'), icon: MapPin, color: '#3b82f6' },
  ]

  const [offenders, setOffenders] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [expandedId, setExpandedId] = useState(null)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [offendersRes, statsRes] = await Promise.all([
        listRepeatOffenders(),
        getRepeatOffenderStats(),
      ])
      setOffenders(offendersRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load repeat offenders', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    setAnalyzing(true)
    try { await analyzeRepeatOffenders(); await loadData() } catch (e) { console.error(e) } finally { setAnalyzing(false) }
  }

  if (loading) {
    return (
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-[var(--border)] border-t-amber-500 rounded-full animate-spin" />
        </div>
      </div>
    )
  }

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-[var(--border)] flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
            <UserX size={16} className="text-red-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-[var(--text-primary)]">Repeat Offender Tracking</h3>
            <p className="text-[10px] text-[var(--text-muted)]">Identify and track repeat criminal activity</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleAnalyze} disabled={analyzing}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {analyzing ? <RefreshCw size={12} className="animate-spin" /> : <Search size={12} />}
            {analyzing ? 'Analyzing...' : 'Analyze Offenders'}
          </button>
          <button onClick={loadData} className="p-1.5 text-[var(--text-muted)] hover:text-[var(--text-secondary)] transition-colors">
            <RefreshCw size={12} />
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="px-5 py-3 border-b border-[var(--border)] flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-[var(--text-primary)]">{stats.total_offenders || 0}</span>
            <span className="text-[10px] text-[var(--text-muted)]">Offenders</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-red-500">{stats.critical || 0}</span>
            <span className="text-[10px] text-[var(--text-muted)]">Critical</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-amber-500">{stats.high || 0}</span>
            <span className="text-[10px] text-[var(--text-muted)]">High Risk</span>
          </div>
        </div>
      )}

      {/* Content */}
      {offenders.length === 0 ? (
        <div className="text-center py-12">
          <UserX size={32} className="mx-auto text-[var(--text-muted)] mb-3" />
          <p className="text-sm font-medium text-[var(--text-muted)] mb-1">No repeat offenders identified</p>
          <p className="text-xs text-[var(--text-muted)] mb-4">Click "Analyze Offenders" to scan crime data for repeat offenders.</p>
          <div className="inline-block bg-[var(--bg-muted)] rounded-lg px-4 py-3 text-[10px] text-[var(--text-muted)] text-left max-w-xs">
            <p className="m-0 font-medium text-[var(--text-secondary)] mb-1">How repeat offender detection works:</p>
            <ul className="m-0 pl-3 space-y-0.5">
              <li>Analyzes frequency of offenses per suspect</li>
              <li>Checks recency of criminal activity</li>
              <li>Evaluates severity and geographic spread</li>
              <li>Generates overall risk score per offender</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="p-5 space-y-3">
          {offenders.map((o, i) => (
            <div key={o.id || i}
              className="border border-[var(--border)] rounded-xl overflow-hidden hover:border-[var(--border-strong)] transition-colors">
              {/* Header row */}
              <div className="px-4 py-3 flex items-center gap-3 cursor-pointer"
                onClick={() => setExpandedId(expandedId === o.id ? null : o.id)}>
                <span className="w-6 h-6 rounded-lg bg-[var(--bg-input)] flex items-center justify-center text-[10px] font-bold text-[var(--text-muted)] flex-shrink-0">
                  #{i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <span className="text-xs font-semibold text-[var(--text-primary)] block">{o.offender_name}</span>
                  <span className="text-[10px] text-[var(--text-muted)]">{o.total_offenses} offenses</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-[var(--text-primary)]">{o.overall_score}%</span>
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ color: riskColors[o.risk_level], background: `${riskColors[o.risk_level]}15` }}>
                    {o.risk_level}
                  </span>
                </div>
              </div>

              {/* Dimension bars */}
              <div className="px-4 pb-3 space-y-1.5">
                {dimensionConfig.map((dim) => (
                  <div key={dim.key} className="flex items-center gap-2">
                    <span className="text-[10px] text-[var(--text-muted)] w-16 flex-shrink-0">{dim.label}</span>
                    <div className="flex-1 h-1.5 bg-[var(--bg-input)] rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${o[dim.key] || 0}%`, background: dim.color }} />
                    </div>
                    <span className="text-[10px] font-mono text-[var(--text-muted)] w-8 text-right">{Math.round(o[dim.key] || 0)}%</span>
                  </div>
                ))}
              </div>

              {/* Expanded risk factors */}
              {expandedId === o.id && o.risk_factors && o.risk_factors.length > 0 && (
                <div className="px-4 pb-3 border-t border-[var(--border)] pt-2">
                  <p className="text-[10px] font-semibold text-[var(--text-muted)] mb-1">Risk Factors</p>
                  <div className="space-y-0.5">
                    {o.risk_factors.map((f, fi) => (
                      <div key={fi} className="flex items-center gap-1.5 text-[10px] text-[var(--text-muted)]">
                        <AlertTriangle size={9} className="text-amber-500 flex-shrink-0" />
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
