import { useState, useEffect } from 'react'
import { Link2, ArrowRight, FileText, Search } from 'lucide-react'
import { detectEvidenceLinks, listEvidenceLinks, getEvidenceLinkingStats } from '../../services/evidenceLinking'
import { explainEvidenceLink } from '../../services/proactive'
import ExplainButton from './ExplainButton'
import ExplanationPanel from './ExplanationPanel'
import { useLanguage } from '../../context/LanguageContext'

export default function EvidenceLinkingSection() {
  const { t } = useLanguage()
  const [links, setLinks] = useState([])
  const [detecting, setDetecting] = useState(false)
  const [explainingId, setExplainingId] = useState(null)
  const [explanation, setExplanation] = useState(null)

  const linkTypeConfig = {
    same_type: { icon: FileText, label: t('Same Type'), color: '#3b82f6' },
    description_match: { icon: Search, label: t('Description Match'), color: '#f59e0b' },
  }

  useEffect(() => { loadData() }, [])

  async function loadData() {
    try {
      const [linksRes] = await Promise.all([
        listEvidenceLinks(),
        getEvidenceLinkingStats(),
      ])
      setLinks(linksRes?.data?.items || [])
    } catch (e) { console.error(e) }
  }

  async function handleDetect() {
    setDetecting(true)
    try { await detectEvidenceLinks(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleExplain(linkId) {
    if (explainingId === linkId) {
      setExplainingId(null)
      setExplanation(null)
      return
    }
    setExplainingId(linkId)
    setExplanation(null)
    try {
      const res = await explainEvidenceLink(linkId)
      setExplanation(res?.data || res)
    } catch (e) { console.error('Explain failed', e) } finally { setExplainingId(null) }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Link2 size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">{t('Evidence Linking')}</h3>
          <span className="text-[10px] text-slate-400">{links.length} {t('links')}</span>
        </div>
        <button onClick={handleDetect} disabled={detecting}
          className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
          {detecting ? t('Detecting...') : t('Detect Links')}
        </button>
      </div>

      {links.length === 0 ? (
        <div className="py-6 text-center text-xs text-slate-400">
          <Link2 size={24} className="mx-auto mb-2 text-slate-200" />
          <p>{t('No evidence links found')}</p>
          <p className="text-[10px] text-slate-300">{t('Click "Detect Links" to find correlations')}</p>
        </div>
      ) : (
        <div className="space-y-2">
          {links.slice(0, 5).map((l, i) => {
            const config = linkTypeConfig[l.link_type] || { icon: Link2, label: t('Link'), color: '#64748b' }
            const Icon = config.icon
            return (
              <div key={l.id || i}>
                <div className="flex items-center gap-3 p-2 bg-slate-50 rounded-lg">
                  <div className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                    style={{ background: `${config.color}15` }}>
                    <Icon size={12} style={{ color: config.color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-medium text-slate-900">{t(l.link_reason)}</p>
                      <ExplainButton onClick={() => handleExplain(l.id)} loading={explainingId === l.id} />
                    </div>
                    <div className="flex items-center gap-2 text-[10px] text-slate-400">
                      <span>{t('Evidence')} #{l.evidence_id_1}</span>
                      <ArrowRight size={10} />
                      <span>{t('Evidence')} #{l.evidence_id_2}</span>
                      <span>• {l.confidence}%</span>
                    </div>
                  </div>
                </div>
                {explanation && explainingId === null && explanation.link_id === l.id && (
                  <ExplanationPanel explanation={explanation} onClose={() => setExplanation(null)} />
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

