import { useState, useEffect } from 'react'
import { Globe, RefreshCw, ArrowRight, MapPin, Shield, Phone, Car } from 'lucide-react'
import { detectCrossDistrict, listCrossDistrictMatches, getCrossDistrictStats } from '../../services/crossDistrict'

const matchIcons = { suspect: Shield, vehicle: Car, phone: Phone, evidence: MapPin }
const matchColors = { suspect: '#ef4444', vehicle: '#8b5cf6', phone: '#10b981', evidence: '#3b82f6' }

export default function CrossDistrictSection() {
  const [matches, setMatches] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [matchesRes, statsRes] = await Promise.all([
        listCrossDistrictMatches(),
        getCrossDistrictStats(),
      ])
      setMatches(matchesRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  async function handleDetect() {
    setDetecting(true)
    try { await detectCrossDistrict(); await loadData() } catch (e) { console.error(e) } finally { setDetecting(false) }
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
              <div key={m.id || i} className="flex items-center gap-3 p-2 bg-slate-50 rounded-lg">
                <div className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ background: `${color}15` }}>
                  <Icon size={12} style={{ color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-slate-900">{m.match_reason}</p>
                  <div className="flex items-center gap-2 text-[10px] text-slate-400">
                    <span>{m.district_1}</span>
                    <ArrowRight size={10} />
                    <span>{m.district_2}</span>
                    <span>• {m.confidence}%</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
