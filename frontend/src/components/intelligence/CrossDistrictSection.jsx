import { useState, useEffect } from 'react'
import { Globe, ArrowRight, MapPin, Shield, Phone, Car } from 'lucide-react'
import { detectCrossDistrict, listCrossDistrictMatches, getCrossDistrictStats } from '../../services/crossDistrict'
import { explainEvent } from '../../services/proactive'
import ExplainButton from './ExplainButton'
import ExplanationPanel from './ExplanationPanel'

const matchIcons = { suspect: Shield, vehicle: Car, phone: Phone, evidence: MapPin }
const matchColors = { suspect: '#ef4444', vehicle: '#8b5cf6', phone: '#10b981', evidence: '#3b82f6' }

export default function CrossDistrictSection() {
  const [matches, setMatches] = useState([])
  const [detecting, setDetecting] = useState(false)
  const [explainingId, setExplainingId] = useState(null)
  const [explanation, setExplanation] = useState(null)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    try {
      const [matchesRes] = await Promise.all([
        listCrossDistrictMatches(),
        getCrossDistrictStats(),
      ])
      setMatches(matchesRes?.data?.items || [])
    } catch (e) { console.error(e) }
  }

  async function handleDetect() {
    setDetecting(true)
    try { await detectCrossDistrict(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleExplain(matchId) {
    if (explainingId === matchId) {
      setExplainingId(null)
      setExplanation(null)
      return
    }
    setExplainingId(matchId)
    setExplanation(null)
    try {
      const res = await explainEvent(matchId)
      setExplanation(res?.data || res)
    } catch (e) { console.error('Explain failed', e) } finally { setExplainingId(null) }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Globe size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Cross-District Intelligence</h3>
          <span className="text-[10px] text-slate-400">{matches.length} matches</span>
        </div>
        <button onClick={handleDetect} disabled={detecting}
          className="text-[10px] text-amber-500 hover:underline disabled:opacity-50">
          {detecting ? 'Detecting...' : 'Detect Matches'}
        </button>
      </div>

      {matches.length === 0 ? (
        <div className="py-6 text-center text-xs text-slate-400">
          <Globe size={24} className="mx-auto mb-2 text-slate-200" />
          <p>No cross-district matches found</p>
          <p className="text-[10px] text-slate-300">Click "Detect Matches" to scan for connections</p>
        </div>
      ) : (
        <div className="space-y-2">
          {matches.slice(0, 5).map((m, i) => {
            const Icon = matchIcons[m.match_type] || Globe
            const color = matchColors[m.match_type] || '#64748b'
            return (
              <div key={m.id || i}>
                <div className="flex items-center gap-3 p-2 bg-slate-50 rounded-lg">
                  <div className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                    style={{ background: `${color}15` }}>
                    <Icon size={12} style={{ color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-medium text-slate-900">{m.match_reason}</p>
                      <ExplainButton onClick={() => handleExplain(m.id)} loading={explainingId === m.id} />
                    </div>
                    <div className="flex items-center gap-2 text-[10px] text-slate-400">
                      <span>{m.district_1}</span>
                      <ArrowRight size={10} />
                      <span>{m.district_2}</span>
                      <span>• {m.confidence}%</span>
                    </div>
                  </div>
                </div>
                {explanation && explainingId === null && explanation.event_id === m.id && (
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
