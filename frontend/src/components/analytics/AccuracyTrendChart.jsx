import { TrendingUp } from 'lucide-react'
import { useState, useEffect } from 'react'
import { getAccuracyTrend } from '../../services/analytics'

export default function AccuracyTrendChart() {
  const [trend, setTrend] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { loadTrend() }, [])

  async function loadTrend() {
    setLoading(true)
    try {
      const res = await getAccuracyTrend()
      setTrend(res?.data || [])
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  const maxVal = Math.max(...trend.map(t => t.value || 0), 1)

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <TrendingUp size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-slate-900">Accuracy Trend</h3>
      </div>

      {loading ? (
        <p className="text-[10px] text-slate-400 text-center py-4">Loading...</p>
      ) : trend.length === 0 ? (
        <p className="text-[10px] text-slate-400 text-center py-4">No accuracy data yet</p>
      ) : (
        <div className="flex items-end gap-0.5 h-20">
          {trend.slice(-14).map((t, i) => (
            <div key={i} className="flex-1 flex flex-col items-center">
              <div className="w-full flex items-end justify-center" style={{ height: '100%' }}>
                <div className="w-full bg-amber-500 rounded-t opacity-70 hover:opacity-100 transition-opacity"
                  style={{ height: `${((t.value || 0) / maxVal) * 100}%`, minHeight: 2 }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
