import { useEffect, useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByStatus } from '../../services/analyticsLive'

const COLORS = ['#e57373', '#ef9a9a', '#ffcdd2', '#e0e0e0', '#bdbdbd']

export default function StatusBars() {
  const { t } = useLanguage()
  const [statuses, setStatuses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByStatus()
        const rows = Array.isArray(res?.data) ? res.data : []
        const sum = rows.reduce((s, r) => s + (r.value || 0), 0)
        const mapped = rows.map((r, i) => ({
          label: r.key || 'unknown',
          value: r.value || 0,
          pct: sum ? Math.round(((r.value || 0) / sum) * 100) : 0,
          color: COLORS[i % COLORS.length],
        }))
        if (!cancelled) setStatuses(mapped)
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">{t('Cases by Status')}</h3>
      </div>
      <div className="chart-card-body">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : statuses.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No status data')}</p>
        ) : (
          <div className="status-bars-list">
            {statuses.map((s, i) => (
              <div key={i} className="status-bar-item">
                <div className="status-bar-header">
                  <span className="status-bar-label">{t(s.label)}</span>
                  <span className="status-bar-pct">{s.pct}% ({s.value})</span>
                </div>
                <div className="status-bar-track">
                  <div
                    className="status-bar-fill"
                    style={{ width: `${s.pct}%`, background: s.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
