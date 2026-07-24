import { useState, useEffect } from 'react'
import { Fingerprint, RefreshCw, ArrowRight, Search, ChevronLeft, ChevronRight } from 'lucide-react'
import { getMOProfiles, compareMOs, batchFingerprint, getMOStats } from '../../services/mo'
import { useLanguage } from '../../context/LanguageContext'

const PAGE_SIZE = 10

export default function MOComparisonTab() {
  const { t } = useLanguage()
  const [profiles, setProfiles] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [batching, setBatching] = useState(false)
  const [compareResult, setCompareResult] = useState(null)
  const [selected1, setSelected1] = useState('')
  const [selected2, setSelected2] = useState('')
  const [comparing, setComparing] = useState(false)
  const [page, setPage] = useState(1)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [profilesRes, statsRes] = await Promise.all([getMOProfiles(), getMOStats()])
      setProfiles(profilesRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
      setPage(1)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  async function handleBatch() {
    setBatching(true)
    try { await batchFingerprint(); await loadData() } catch (e) { console.error(e) } finally { setBatching(false) }
  }

  async function handleCompare() {
    if (!selected1 || !selected2 || comparing) return
    setComparing(true)
    try { const res = await compareMOs(parseInt(selected1), parseInt(selected2)); setCompareResult(res?.data || res) }
    catch (e) { console.error(e) } finally { setComparing(false) }
  }

  const totalPages = Math.ceil(profiles.length / PAGE_SIZE)
  const pageData = profiles.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-6">
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center">
            <Fingerprint size={16} className="text-indigo-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">MO Fingerprinting</h3>
            <p className="text-[10px] text-slate-400">Modus operandi pattern analysis and comparison</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleBatch} disabled={batching}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {batching ? <RefreshCw size={12} className="animate-spin" /> : <Search size={12} />}
            {batching ? 'Processing...' : 'Batch Fingerprint'}
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
            <span className="text-lg font-bold text-slate-900">{stats.total_comparisons || 0}</span>
            <span className="text-[10px] text-slate-400">Comparisons</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-slate-900">{stats.avg_similarity || 0}%</span>
            <span className="text-[10px] text-slate-400">Avg Similarity</span>
          </div>
        </div>
      )}

      {/* Compare Form */}
      <div className="px-5 py-3 border-b border-slate-100 bg-slate-50">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1.5">
            <Search size={12} className="text-slate-400" />
            <span className="text-[10px] font-semibold text-slate-500">Compare:</span>
          </div>
          <select className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-amber-400"
            value={selected1} onChange={(e) => setSelected1(e.target.value)}>
            <option value="">Profile 1</option>
            {profiles.map((p) => <option key={p.id} value={p.id}>Crime #{p.crime_id}</option>)}
          </select>
          <ArrowRight size={14} className="text-slate-300" />
          <select className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-amber-400"
            value={selected2} onChange={(e) => setSelected2(e.target.value)}>
            <option value="">Profile 2</option>
            {profiles.map((p) => <option key={p.id} value={p.id}>Crime #{p.crime_id}</option>)}
          </select>
          <button onClick={handleCompare} disabled={!selected1 || !selected2 || comparing}
            className="flex items-center gap-1 px-3 py-1.5 bg-indigo-500 text-white hover:bg-indigo-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {comparing ? 'Comparing...' : 'Compare'}
          </button>
        </div>
      </div>

      {/* Compare Result */}
      {compareResult && (
        <div className="mx-5 mt-4 p-4 bg-indigo-50 border border-indigo-200 rounded-xl">
          <div className="flex items-center gap-4 mb-3">
            <div className="text-center">
              <span className="text-2xl font-bold text-indigo-600">{compareResult.similarity_score}%</span>
              <p className="text-[10px] text-slate-500">Similarity</p>
            </div>
            <span className={`text-xs font-bold px-2 py-0.5 rounded ${
              compareResult.match_level === 'high' ? 'bg-emerald-100 text-emerald-700' :
              compareResult.match_level === 'medium' ? 'bg-amber-100 text-amber-700' :
              'bg-slate-100 text-slate-600'
            }`}>{compareResult.match_level}</span>
          </div>
          {compareResult.shared_features && compareResult.shared_features.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {compareResult.shared_features.map((f, i) => (
                <span key={i} className="text-[10px] bg-white text-indigo-600 border border-indigo-200 px-2 py-0.5 rounded-full">{f}</span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* MO Profiles Table */}
      {profiles.length === 0 ? (
        <div className="text-center py-12 m-5 border border-dashed border-slate-200 rounded-xl">
          <Fingerprint size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No MO profiles yet</p>
          <p className="text-xs text-slate-400">Click "Batch Fingerprint" to analyze all crimes.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Crime ID</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">MO Description</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Fingerprint</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Confidence</th>
                </tr>
              </thead>
              <tbody>
                {pageData.map((p) => (
                  <tr key={p.id} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3">
                      <span className="text-xs font-semibold text-slate-900">Crime #{p.crime_id}</span>
                    </td>
                    <td className="px-5 py-3">
                      <p className="text-xs text-slate-600 max-w-[300px] truncate">{p.mo_text || 'No MO data'}</p>
                    </td>
                    <td className="px-5 py-3">
                      <div className="flex flex-wrap gap-1">
                        {p.fingerprint && Object.entries(p.fingerprint).map(([key, val]) => (
                          val && <span key={key} className="text-[9px] bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded">{key}: {val}</span>
                        ))}
                      </div>
                    </td>
                    <td className="px-5 py-3 text-right">
                      <span className={`text-xs font-bold ${p.confidence >= 70 ? 'text-emerald-600' : p.confidence >= 40 ? 'text-amber-600' : 'text-slate-500'}`}>
                        {p.confidence}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-5 py-3 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[10px] text-slate-400">
                Showing {((page - 1) * PAGE_SIZE) + 1}-{Math.min(page * PAGE_SIZE, profiles.length)} of {profiles.length}
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
    </div>
  )
}
