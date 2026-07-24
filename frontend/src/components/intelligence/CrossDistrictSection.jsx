import { useState, useEffect } from 'react'
import { Globe, ArrowRight, Shield, Phone, Car, MapPin, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react'
import { detectCrossDistrict, listCrossDistrictMatches, getCrossDistrictStats } from '../../services/crossDistrict'
import { explainEvent } from '../../services/proactive'
import ExplainButton from './ExplainButton'
import ExplanationPanel from './ExplanationPanel'
import { useLanguage } from '../../context/LanguageContext'

const matchIcons = { suspect: Shield, vehicle: Car, phone: Phone, evidence: MapPin }
const matchColors = { suspect: '#ef4444', vehicle: '#8b5cf6', phone: '#10b981', evidence: '#3b82f6' }
const PAGE_SIZE = 10

export default function CrossDistrictSection() {
  const { t } = useLanguage()
  const [matches, setMatches] = useState([])
  const [stats, setStats] = useState(null)
  const [detecting, setDetecting] = useState(false)
  const [explainingId, setExplainingId] = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [page, setPage] = useState(1)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    try {
      const [matchesRes, statsRes] = await Promise.all([listCrossDistrictMatches(), getCrossDistrictStats()])
      setMatches(matchesRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
      setPage(1)
    } catch (e) { console.error(e) }
  }

  async function handleDetect() {
    setDetecting(true)
    try { await detectCrossDistrict(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleExplain(matchId) {
    if (explainingId === matchId) { setExplainingId(null); setExplanation(null); return }
    setExplainingId(matchId); setExplanation(null)
    try { const res = await explainEvent(matchId); setExplanation(res?.data || res) }
    catch (e) { console.error(e) } finally { setExplainingId(null) }
  }

  const totalPages = Math.ceil(matches.length / PAGE_SIZE)
  const pageData = matches.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-cyan-50 flex items-center justify-center">
            <Globe size={16} className="text-cyan-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Cross-District Intelligence</h3>
            <p className="text-[10px] text-slate-400">Statewide connection detection across districts</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {stats && (
            <span className="text-[10px] bg-cyan-100 text-cyan-700 px-2 py-0.5 rounded-full font-medium">{matches.length} matches</span>
          )}
          <button onClick={handleDetect} disabled={detecting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {detecting ? <RefreshCw size={12} className="animate-spin" /> : null}
            {detecting ? 'Detecting...' : 'Detect Matches'}
          </button>
        </div>
      </div>

      {/* Content */}
      {matches.length === 0 ? (
        <div className="text-center py-12">
          <Globe size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No cross-district matches found</p>
          <p className="text-xs text-slate-400">Click "Detect Matches" to scan for statewide connections.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Type</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Match Reason</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Districts</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Confidence</th>
                  <th className="px-5 py-3 w-16"></th>
                </tr>
              </thead>
              <tbody>
                {pageData.map((m, i) => {
                  const Icon = matchIcons[m.match_type] || Globe
                  const color = matchColors[m.match_type] || '#64748b'
                  return (
                    <tr key={m.id || i} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                      <td className="px-5 py-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium`}
                          style={{ color, background: `${color}15`, border: `1px solid ${color}30` }}>
                          <Icon size={10} />
                          {m.match_type || 'match'}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs font-medium text-slate-900">{m.match_reason}</td>
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-1.5 text-xs text-slate-600">
                          <span>{m.district_1}</span>
                          <ArrowRight size={10} className="text-slate-300" />
                          <span>{m.district_2}</span>
                        </div>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <span className={`text-xs font-bold ${m.confidence >= 70 ? 'text-emerald-600' : m.confidence >= 40 ? 'text-amber-600' : 'text-slate-500'}`}>
                          {m.confidence}%
                        </span>
                      </td>
                      <td className="px-5 py-3">
                        <ExplainButton onClick={() => handleExplain(m.id)} loading={explainingId === m.id} />
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Explanation inline */}
          {explanation && explainingId === null && (
            <div className="px-5 pb-4">
              <ExplanationPanel explanation={explanation} onClose={() => setExplanation(null)} />
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-5 py-3 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[10px] text-slate-400">
                Showing {((page - 1) * PAGE_SIZE) + 1}-{Math.min(page * PAGE_SIZE, matches.length)} of {matches.length}
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
