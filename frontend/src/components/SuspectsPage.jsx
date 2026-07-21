import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Eye, RefreshCw } from 'lucide-react'
import { listSuspects } from '../services/search'

export default function SuspectsPage() {
  const [suspects, setSuspects] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const navigate = useNavigate()

  useEffect(() => { loadSuspects() }, [page, searchQuery])

  async function loadSuspects() {
    setLoading(true)
    try {
      const res = await listSuspects(page, 20, searchQuery)
      const data = res?.data || res
      setSuspects(data?.items || [])
      setTotal(data?.total || 0)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  const filtered = suspects.filter(s => {
    if (!searchQuery) return true
    const q = searchQuery.toLowerCase()
    return (s.name || s.title || '').toLowerCase().includes(q) ||
           (s.id?.toString() || '').includes(q) ||
           (s.status || '').toLowerCase().includes(q)
  })

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-slate-900">Suspects</h1>
          <p className="text-xs text-slate-500">{total} suspects in database</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-lg px-3 py-1.5">
            <Search size={14} className="text-slate-400" />
            <input className="bg-transparent border-none outline-none text-sm text-slate-900 placeholder-slate-400 w-48"
              placeholder="Search suspects..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
          </div>
          <button onClick={loadSuspects} className="p-1.5 bg-white border border-slate-200 rounded-lg hover:border-amber-500">
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

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
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Name</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Alias</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Status</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Risk</th>
                <th className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50 cursor-pointer transition-colors" onClick={() => navigate(`/suspects/${s.id}`)}>
                  <td className="px-4 py-3">
                    <span className="text-xs font-mono text-amber-600 font-semibold">CRIM-{String(s.id).padStart(3, '0')}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm font-medium text-slate-900">{s.name || s.title || 'Unknown'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs text-slate-500">{s.alias || '—'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                      s.status === 'At Large' ? 'bg-red-50 text-red-600' :
                      s.status === 'Arrested' ? 'bg-green-50 text-green-600' :
                      s.status === 'Under Trial' ? 'bg-amber-50 text-amber-600' :
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

          {filtered.length === 0 && (
            <div className="py-8 text-center text-sm text-slate-400">No suspects found</div>
          )}

          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200">
            <span className="text-xs text-slate-500">Showing {filtered.length} of {total}</span>
            <div className="flex items-center gap-1">
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                className="px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 rounded disabled:opacity-50">
                Prev
              </button>
              <span className="px-2 text-xs text-slate-500">Page {page}</span>
              <button onClick={() => setPage(p => p + 1)} disabled={filtered.length < 20}
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
