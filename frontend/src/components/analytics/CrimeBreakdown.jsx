import { useEffect, useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByType } from '../../services/analyticsLive'

const COLORS = ['#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#94a3b8']

export default function CrimeBreakdown() {
  const { t } = useLanguage()
  const [types, setTypes] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByType()
        const list = Array.isArray(res?.data) ? res.data : []
        const sum = list.reduce((s, r) => s + (r.value || 0), 0)
        const mapped = list.map((r, i) => ({
          name: r.key || 'Other',
          count: r.value || 0,
          percentage: sum ? Math.round(((r.value || 0) / sum) * 1000) / 10 : 0,
          color: COLORS[i % COLORS.length],
        }))
        if (!cancelled) setTypes(mapped)
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
    <div className="analytics-breakdown-card">
      <div className="analytics-breakdown-header">
        <h3>{t('Crime Type Breakdown')}</h3>
      </div>

      <div className="analytics-breakdown-list">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : types.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No breakdown data')}</p>
        ) : types.map((type, i) => (
          <div key={i} className="breakdown-item">
            <div className="breakdown-item-header">
              <span className="breakdown-name">{t(type.name)}</span>
              <span className="breakdown-stats">
                {type.percentage}% • {type.count.toLocaleString()} {t('cases')}
              </span>
            </div>
            <div className="breakdown-bar">
              <div
                className="breakdown-bar-fill"
                style={{ width: `${type.percentage}%`, background: type.color }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
