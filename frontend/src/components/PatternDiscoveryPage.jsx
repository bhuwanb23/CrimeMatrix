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
    <div className="bg-white border border-slate-200 rounded-xl">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
            <GitBranch size={16} className="text-amber-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Crime Pattern Discovery</h3>
            <p className="text-[10px] text-slate-400">Automatically identify recurring crime patterns</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {stats && (
            <div className="flex items-center gap-3 text-[10px] text-slate-400 mr-2">
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
      <div className="px-5 py-3 border-b border-slate-100 flex items-center gap-1.5">
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

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-5 h-5 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        </div>
      ) : patterns.length === 0 ? (
        <div className="text-center py-12 border border-dashed border-slate-200 m-5 rounded-xl">
          <GitBranch size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No patterns detected yet</p>
          <p className="text-xs text-slate-400">Click "Detect Patterns" to analyze crime data.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Type</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Pattern Name</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Description</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Crimes</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Confidence</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Tags</th>
                  <th className="px-5 py-3 w-8"></th>
                </tr>
              </thead>
              <tbody>
                {pageData.map((p) => {
                  const config = typeConfig[p.pattern_type] || typeConfig.combined
                  const Icon = config.icon
                  return (
                    <tr key={p.id}
                      className="border-b border-slate-50 hover:bg-slate-50 transition-colors cursor-pointer"
                      onClick={() => setSelectedPattern(p)}>
                      <td className="px-5 py-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${config.bg} ${config.color} border ${config.border}`}>
                          <Icon size={10} />
                          {config.label}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs font-medium text-slate-900">{p.name}</td>
                      <td className="px-5 py-3 text-xs text-slate-500 max-w-[200px] truncate">{p.description}</td>
                      <td className="px-5 py-3 text-xs font-semibold text-slate-700 text-right">{p.frequency}</td>
                      <td className="px-5 py-3 text-right">
                        <span className={`text-xs font-bold ${p.confidence >= 70 ? 'text-emerald-600' : p.confidence >= 40 ? 'text-amber-600' : 'text-slate-500'}`}>
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
                        <ChevronRight size={14} className="text-slate-300 group-hover:text-slate-500" />
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-5 py-3 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[10px] text-slate-400">
                Showing {((page - 1) * PAGE_SIZE) + 1}-{Math.min(page * PAGE_SIZE, patterns.length)} of {patterns.length}
              </span>
              <div className="flex items-center gap-1">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                  className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30 transition-colors">
                  <ChevronLeft size={14} className="text-slate-500" />
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                  <button key={p} onClick={() => setPage(p)}
                    className={`w-7 h-7 rounded-lg text-xs font-medium transition-colors ${
                      p === page ? 'bg-amber-500 text-white' : 'text-slate-500 hover:bg-slate-100'
                    }`}>
                    {p}
                  </button>
                ))}
                <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}
                  className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30 transition-colors">
                  <ChevronRight size={14} className="text-slate-500" />
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
