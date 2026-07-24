import { useState, useEffect } from 'react'
import { Link2, ArrowRight, FileText, Search, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react'
import { detectEvidenceLinks, listEvidenceLinks, getEvidenceLinkingStats } from '../../services/evidenceLinking'
import { explainEvidenceLink } from '../../services/proactive'
import ExplainButton from './ExplainButton'
import ExplanationPanel from './ExplanationPanel'
import { useLanguage } from '../../context/LanguageContext'

const linkTypeConfig = {
  same_type: { icon: FileText, label: 'Same Type', color: '#3b82f6' },
  description_match: { icon: Search, label: 'Description Match', color: '#f59e0b' },
}
const PAGE_SIZE = 10

export default function EvidenceLinkingSection() {
  const { t } = useLanguage()
  const [links, setLinks] = useState([])
  const [stats, setStats] = useState(null)
  const [detecting, setDetecting] = useState(false)
  const [explainingId, setExplainingId] = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [page, setPage] = useState(1)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    try {
      const [linksRes, statsRes] = await Promise.all([listEvidenceLinks(), getEvidenceLinkingStats()])
      setLinks(linksRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
      setPage(1)
    } catch (e) { console.error(e) }
  }

  async function handleDetect() {
    setDetecting(true)
    try { await detectEvidenceLinks(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleExplain(linkId) {
    if (explainingId === linkId) { setExplainingId(null); setExplanation(null); return }
    setExplainingId(linkId); setExplanation(null)
    try { const res = await explainEvidenceLink(linkId); setExplanation(res?.data || res) }
    catch (e) { console.error(e) } finally { setExplainingId(null) }
  }

  const totalPages = Math.ceil(links.length / PAGE_SIZE)
  const pageData = links.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
            <Link2 size={16} className="text-blue-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Evidence Linking</h3>
            <p className="text-[10px] text-slate-400">Automatic evidence correlation detection</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {stats && (
            <span className="text-[10px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">{links.length} links</span>
          )}
          <button onClick={handleDetect} disabled={detecting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white hover:bg-amber-600 rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
            {detecting ? <RefreshCw size={12} className="animate-spin" /> : null}
            {detecting ? 'Detecting...' : 'Detect Links'}
          </button>
        </div>
      </div>

      {/* Content */}
      {links.length === 0 ? (
        <div className="text-center py-12">
          <Link2 size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No evidence links found</p>
          <p className="text-xs text-slate-400">Click "Detect Links" to find evidence correlations.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Type</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Reason</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Evidence</th>
                  <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Confidence</th>
                  <th className="px-5 py-3 w-16"></th>
                </tr>
              </thead>
              <tbody>
                {pageData.map((l, i) => {
                  const config = linkTypeConfig[l.link_type] || { icon: Link2, label: 'Link', color: '#64748b' }
                  const Icon = config.icon
                  return (
                    <tr key={l.id || i} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                      <td className="px-5 py-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium`}
                          style={{ color: config.color, background: `${config.color}15`, border: `1px solid ${config.color}30` }}>
                          <Icon size={10} />
                          {config.label}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs font-medium text-slate-900">{l.link_reason}</td>
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-1.5 text-xs text-slate-600">
                          <span>Evidence #{l.evidence_id_1}</span>
                          <ArrowRight size={10} className="text-slate-300" />
                          <span>Evidence #{l.evidence_id_2}</span>
                        </div>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <span className={`text-xs font-bold ${l.confidence >= 70 ? 'text-emerald-600' : l.confidence >= 40 ? 'text-amber-600' : 'text-slate-500'}`}>
                          {l.confidence}%
                        </span>
                      </td>
                      <td className="px-5 py-3">
                        <ExplainButton onClick={() => handleExplain(l.id)} loading={explainingId === l.id} />
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
                Showing {((page - 1) * PAGE_SIZE) + 1}-{Math.min(page * PAGE_SIZE, links.length)} of {links.length}
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
