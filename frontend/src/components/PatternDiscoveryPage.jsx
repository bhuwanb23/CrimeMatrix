import { useState, useEffect, useCallback } from 'react'
import { GitBranch, RefreshCw, Layers, Search, AlertTriangle } from 'lucide-react'
import { detectPatterns, listPatterns, getPatternStats } from '../services/patterns'
import PatternCard from './patterns/PatternCard'
import PatternExplorer from './patterns/PatternExplorer'
import { useLanguage } from '../context/LanguageContext'

const typeFilters = [
  { value: '', label: 'All Types' },
  { value: 'time', label: 'Time' },
  { value: 'mo', label: 'MO' },
  { value: 'location', label: 'Location' },
  { value: 'type', label: 'Crime Type' },
]

export default function PatternDiscoveryPage() {
  const { t } = useLanguage()
  const [patterns, setPatterns] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)
  const [typeFilter, setTypeFilter] = useState('')
  const [selectedPattern, setSelectedPattern] = useState(null)
  const [detectResult, setDetectResult] = useState(null)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [patternsRes, statsRes] = await Promise.all([
        listPatterns(typeFilter ? { pattern_type: typeFilter } : {}),
        getPatternStats(),
      ])
      const pData = patternsRes?.data || patternsRes
      const sData = statsRes?.data || statsRes
      setPatterns(pData?.items || [])
      setStats(sData || {})
    } catch (e) {
      console.error('Failed to load patterns', e)
    } finally {
      setLoading(false)
    }
  }, [typeFilter])

  useEffect(() => { loadData() }, [loadData])

  async function handleDetect() {
    setDetecting(true)
    setDetectResult(null)
    try {
      const res = await detectPatterns()
      const data = res?.data || res
      setDetectResult(data)
      await loadData()
    } catch (e) {
      console.error('Detection failed', e)
    } finally {
      setDetecting(false)
    }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <GitBranch size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Crime Pattern Discovery</h3>
          <span className="text-[10px] text-slate-400">Automatically identify recurring patterns</span>
        </div>
        <button onClick={handleDetect} disabled={detecting}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
          {detecting ? <RefreshCw size={12} className="animate-spin" /> : <Search size={12} />}
          {detecting ? 'Detecting...' : 'Detect Patterns'}
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="flex items-center gap-4 mb-3 text-[10px] text-slate-500">
          <span className="flex items-center gap-1"><Layers size={10} /> {stats.total_patterns || 0} patterns</span>
          <span>{stats.total_occurrences || 0} occurrences</span>
          <span>{stats.total_clusters || 0} clusters</span>
        </div>
      )}

      {/* Detection result feedback */}
      {detectResult && (
        <div className={`mb-3 p-3 rounded-lg text-xs ${
          (detectResult.patterns_found || 0) > 0
            ? 'bg-emerald-50 border border-emerald-200 text-emerald-700'
            : 'bg-amber-50 border border-amber-200 text-amber-700'
        }`}>
          {(detectResult.patterns_found || 0) > 0 ? (
            <p className="m-0 font-medium">
              Detected {detectResult.patterns_found} pattern(s): {detectResult.time_patterns || 0} time, {detectResult.mo_patterns || 0} MO, {detectResult.location_patterns || 0} location
            </p>
          ) : (
            <div>
              <p className="m-0 font-medium">No new patterns detected</p>
              <p className="m-0 mt-1 text-[10px] opacity-80">
                Pattern detection requires at least 2 crimes sharing similar characteristics (time, MO, or location). Add more crime records to enable pattern discovery.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-1 mb-3">
        {typeFilters.map((f) => (
          <button key={f.value}
            className={`px-2.5 py-1 rounded-lg text-[10px] font-medium transition-all ${
              typeFilter === f.value
                ? 'bg-amber-100 text-amber-700 border border-amber-300'
                : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50 border border-transparent'
            }`}
            onClick={() => setTypeFilter(f.value)}>
            {t(f.label)}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="w-5 h-5 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        </div>
      ) : patterns.length === 0 ? (
        <div className="text-center py-10 border border-dashed border-slate-200 rounded-xl">
          <GitBranch size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No patterns detected yet</p>
          <p className="text-xs text-slate-400 mb-3">Click "Detect Patterns" to analyze crime data for recurring patterns.</p>
          <div className="inline-block bg-slate-50 rounded-lg px-3 py-2 text-[10px] text-slate-500 text-left max-w-xs">
            <p className="m-0 font-medium text-slate-600 mb-1">How pattern detection works:</p>
            <ul className="m-0 pl-3 space-y-0.5">
              <li><strong>Time patterns:</strong> 2+ crimes in the same time window</li>
              <li><strong>MO patterns:</strong> 2+ crimes sharing method-of-operation keywords</li>
              <li><strong>Location patterns:</strong> 2+ crimes in the same district</li>
            </ul>
            <p className="m-0 mt-1.5 text-slate-400">More crime records = more patterns discovered.</p>
          </div>
        </div>
      ) : (
        <div className="space-y-2">
          {patterns.map((p) => (
            <PatternCard key={p.id} pattern={p} onClick={setSelectedPattern} />
          ))}
        </div>
      )}

      {selectedPattern && (
        <PatternExplorer patternId={selectedPattern.id} onClose={() => setSelectedPattern(null)} />
      )}
    </div>
  )
}
