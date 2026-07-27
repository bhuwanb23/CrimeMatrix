import { useState, useEffect, useCallback } from 'react'
import { GitBranch, RefreshCw, Layers, Search, Clock, MapPin, Crosshair, ChevronLeft, ChevronRight } from 'lucide-react'
import { detectPatterns, listPatterns, getPatternStats } from '../services/patterns'
import PatternExplorer from './patterns/PatternExplorer'
import { useLanguage } from '../context/LanguageContext'

const PAGE_SIZE = 10

const typeConfig = {
  time: { icon: Clock, label: 'Time', color: 'text-blue-500', bg: 'bg-blue-50', border: 'border-blue-200' },
  mo: { icon: Crosshair, label: 'MO', color: 'text-red-500', bg: 'bg-red-50', border: 'border-red-200' },
  location: { icon: MapPin, label: 'Location', color: 'text-emerald-500', bg: 'bg-emerald-50', border: 'border-emerald-200' },
  type: { icon: Layers, label: 'Crime Type', color: 'text-purple-500', bg: 'bg-purple-50', border: 'border-purple-200' },
  combined: { icon: Layers, label: 'Combined', color: 'text-amber-500', bg: 'bg-amber-50', border: 'border-amber-200' },
}

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
  const [page, setPage] = useState(1)

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
      setPage(1)
    } catch (e) {
      console.error('Failed to load patterns', e)
    } finally {
      setLoading(false)
    }
  }, [typeFilter])

  useEffect(() => { loadData() }, [loadData])

  async function handleDetect() {
    setDetecting(true)
    try { await detectPatterns(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  const totalPages = Math.ceil(patterns.length / PAGE_SIZE)
  const pageData = patterns.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
      {/* Header */}
      <div className="px-5 py-4 border-b border-[var(--border)] flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
            <GitBranch size={16} className="text-amber-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-[var(--text-primary)]">Crime Pattern Discovery</h3>
            <p className="text-[10px] text-[var(--text-muted)]">Automatically identify recurring crime patterns</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {stats && (
            <div className="flex items-center gap-3 text-[10px] text-[var(--text-muted)] mr-2">
              <span className="flex items-center gap-1"><Layers size={10} /> {stats.total_patterns || 0} patterns</span>
              <span>{stats.total_occurrences || 0} occurrences</span>
            </div>
          )}
          <button onClick={handleDetect} disabled={detecting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {detecting ? <RefreshCw size={12} className="animate-spin" /> : <Search size={12} />}
            {detecting ? 'Detecting...' : 'Detect Patterns'}
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="px-5 py-3 border-b border-[var(--border)] flex items-center gap-1.5">
        {typeFilters.map((f) => (
          <button key={f.value}
            className={`px-2.5 py-1 rounded-lg text-[10px] font-medium transition-all ${
              typeFilter === f.value
                ? 'bg-amber-100 text-amber-700 border border-amber-300'
                : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] border border-transparent'
            }`}
            onClick={() => setTypeFilter(f.value)}>
            {t(f.label)}
          </button>
        ))}
      </div>

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-5 h-5 border-2 border-[var(--border)] border-t-amber-500 rounded-full animate-spin" />
        </div>
      ) : patterns.length === 0 ? (
        <div className="text-center py-12 border border-dashed border-[var(--border)] m-5 rounded-xl">
          <GitBranch size={32} className="mx-auto text-[var(--text-muted)] mb-3" />
          <p className="text-sm font-medium text-[var(--text-muted)] mb-1">No patterns detected yet</p>
          <p className="text-xs text-[var(--text-muted)]">Click "Detect Patterns" to analyze crime data.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-[var(--border)]">
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider">Type</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider">Pattern Name</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider">Description</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider text-right">Crimes</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider text-right">Confidence</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-[var(--text-muted)] uppercase tracking-wider">Tags</th>
                  <th className="px-5 py-3 w-8"></th>
                </tr>
              </thead>
              <tbody>
                {pageData.map((p) => {
                  const config = typeConfig[p.pattern_type] || typeConfig.combined
                  const Icon = config.icon
                  return (
                    <tr key={p.id}
                      className="border-b border-[var(--border)] hover:bg-[var(--bg-hover)] transition-colors cursor-pointer"
                      onClick={() => setSelectedPattern(p)}>
                      <td className="px-5 py-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${config.bg} ${config.color} border ${config.border}`}>
                          <Icon size={10} />
                          {config.label}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs font-medium text-[var(--text-primary)]">{p.name}</td>
                      <td className="px-5 py-3 text-xs text-[var(--text-muted)] max-w-[200px] truncate">{p.description}</td>
                      <td className="px-5 py-3 text-xs font-semibold text-[var(--text-secondary)] text-right">{p.frequency}</td>
                      <td className="px-5 py-3 text-right">
                        <span className={`text-xs font-bold ${p.confidence >= 70 ? 'text-emerald-600' : p.confidence >= 40 ? 'text-amber-600' : 'text-[var(--text-muted)]'}`}>
                          {p.confidence}%
                        </span>
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex gap-1">
                          {p.time_pattern && <span className="text-[9px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded">{p.time_pattern}</span>}
                          {p.location_pattern && <span className="text-[9px] bg-emerald-50 text-emerald-600 px-1.5 py-0.5 rounded">{p.location_pattern}</span>}
                        </div>
                      </td>
                      <td className="px-5 py-3">
                        <ChevronRight size={14} className="text-[var(--text-muted)] group-hover:text-[var(--text-muted)]" />
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-5 py-3 border-t border-[var(--border)] flex items-center justify-between">
              <span className="text-[10px] text-[var(--text-muted)]">
                Showing {((page - 1) * PAGE_SIZE) + 1}-{Math.min(page * PAGE_SIZE, patterns.length)} of {patterns.length}
              </span>
              <div className="flex items-center gap-1">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                  className="p-1.5 rounded-lg hover:bg-[var(--bg-hover)] disabled:opacity-30 transition-colors">
                  <ChevronLeft size={14} className="text-[var(--text-muted)]" />
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                  <button key={p} onClick={() => setPage(p)}
                    className={`w-7 h-7 rounded-lg text-xs font-medium transition-colors ${
                      p === page ? 'bg-amber-500 text-white' : 'text-[var(--text-muted)] hover:bg-[var(--bg-hover)]'
                    }`}>
                    {p}
                  </button>
                ))}
                <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}
                  className="p-1.5 rounded-lg hover:bg-[var(--bg-hover)] disabled:opacity-30 transition-colors">
                  <ChevronRight size={14} className="text-[var(--text-muted)]" />
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {selectedPattern && (
        <PatternExplorer patternId={selectedPattern.id} onClose={() => setSelectedPattern(null)} />
      )}
    </div>
  )
}
