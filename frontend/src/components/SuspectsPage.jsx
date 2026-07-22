import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Eye, RefreshCw, Filter } from 'lucide-react'
import { listSuspects } from '../services/search'

const statusFilters = [
  { id: 'all', label: 'All' },
  { id: 'at_large', label: 'At Large' },
  { id: 'arrested', label: 'Arrested' },
  { id: 'under_trial', label: 'Under Trial' },
]

export default function SuspectsPage() {
  const [suspects, setSuspects] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [activeFilter, setActiveFilter] = useState('all')
  const [sortBy, setSortBy] = useState('name')
  const navigate = useNavigate()

  const loadSuspects = useCallback(async () => {
    setLoading(true)
    try {
      const res = await listSuspects(page, 20, searchQuery)
      const data = res?.data || res
      setSuspects(data?.items || [])
      setTotal(data?.total || 0)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }, [page, searchQuery])

  useEffect(() => { loadSuspects() }, [loadSuspects])

  const filtered = suspects.filter(s => {
    if (activeFilter === 'all') return true
    return s.status === activeFilter
  })

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === 'risk') return (b.risk_score || 0) - (a.risk_score || 0)
    if (sortBy === 'name') return (a.name || '').localeCompare(b.name || '')
    return 0
  })

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-slate-900">Suspects</h1>
          <p className="text-xs text-slate-500">{total} suspects in database</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={loadSuspects} className="p-1.5 bg-white border border-slate-200 rounded-lg hover:border-amber-500">
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="flex items-center gap-3">
        <div className="flex-1 flex items-center gap-2 bg-white border border-slate-200 rounded-xl px-4 py-2 focus-within:border-amber-500 transition-colors">
          <Search size={16} className="text-slate-400" />
          <input className="flex-1 bg-transparent border-none outline-none text-sm text-slate-900 placeholder-slate-400"
            placeholder="Search by name, alias, district, status..."
            value={searchQuery}
            onChange={e => { setSearchQuery(e.target.value); setPage(1) }}
          />
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex items-center gap-2 flex-wrap">
        <Filter size={14} className="text-slate-400" />
        {statusFilters.map(f => (
          <button key={f.id} onClick={() => { setActiveFilter(f.id); setPage(1) }}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
              activeFilter === f.id
                ? 'bg-amber-500 text-white'
                : 'bg-white text-slate-500 border border-slate-200 hover:border-amber-300'
            }`}>
            {f.label}
          </button>
        ))}
        <span className="ml-auto text-xs text-slate-400">{sorted.length} results</span>
      </div>

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        </div>
      ) : (
        <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">ID</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">
                  <button onClick={() => setSortBy('name')} className="flex items-center gap-1 hover:text-slate-700">Name</button>
                </th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Alias</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">District</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Status</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">
                  <button onClick={() => setSortBy('risk')} className="flex items-center gap-1 hover:text-slate-700">Risk</button>
                </th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {sorted.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50 cursor-pointer transition-colors" onClick={() => navigate(`/suspects/${s.id}`)}>
                  <td className="px-4 py-3">
                    <span className="text-xs font-mono text-amber-600 font-semibold">CRIM-{String(s.id).padStart(3, '0')}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm font-medium text-slate-900">{s.name || 'Unknown'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs text-slate-500">{s.alias || '—'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs text-slate-500">{s.district || '—'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                      s.status === 'at_large' ? 'bg-red-50 text-red-600' :
                      s.status === 'arrested' ? 'bg-green-50 text-green-600' :
                      s.status === 'under_trial' ? 'bg-amber-50 text-amber-600' :
                      'bg-slate-50 text-slate-600'
                    }`}>{s.status || 'Unknown'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full rounded-full" style={{
                          width: `${s.risk_score || 0}%`,
                          background: (s.risk_score || 0) > 70 ? '#ef4444' : (s.risk_score || 0) > 40 ? '#f59e0b' : '#10b981'
                        }} />
                      </div>
                      <span className="text-xs text-slate-500">{s.risk_score || 0}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <button className="p-1 text-slate-400 hover:text-amber-500 transition-colors" onClick={e => { e.stopPropagation(); navigate(`/suspects/${s.id}`) }}>
                      <Eye size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {sorted.length === 0 && (
            <div className="py-8 text-center text-sm text-slate-400">No suspects found</div>
          )}

          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200">
            <span className="text-xs text-slate-500">Showing {sorted.length} of {total}</span>
            <div className="flex items-center gap-1">
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                className="px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 rounded disabled:opacity-50">
                Prev
              </button>
              <span className="px-2 text-xs text-slate-500">Page {page}</span>
              <button onClick={() => setPage(p => p + 1)} disabled={sorted.length < 20}
                className="px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 rounded disabled:opacity-50">
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
