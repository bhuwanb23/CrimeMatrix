import { useEffect, useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByType } from '../../services/analyticsLive'

const COLORS = ['#e57373', '#ef9a9a', '#ffcdd2', '#fbe9e7', '#f5f5f5', '#e0e0e0', '#bdbdbd']

export default function CrimeTypeChart() {
  const { t } = useLanguage()
  const [categories, setCategories] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByType()
        const rows = res?.data || []
        const list = Array.isArray(rows) ? rows : []
        const sum = list.reduce((s, r) => s + (r.value || 0), 0)
        const mapped = list.slice(0, 6).map((r, i) => ({
          label: r.key || 'Other',
          value: r.value || 0,
          pct: sum ? Math.round(((r.value || 0) / sum) * 100) : 0,
          color: COLORS[i % COLORS.length],
        }))
        if (!cancelled) {
          setCategories(mapped)
          setTotal(sum)
        }
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
        <h3 className="chart-card-title">{t('Cases by Crime Type')}</h3>
      </div>
      <div className="chart-card-body">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : categories.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No crime type data')}</p>
        ) : (
          <>
            <div className="category-total">
              <span className="category-total-value">{total.toLocaleString()}</span>
              <span className="category-total-trend">{t('from live API')}</span>
            </div>
            <div className="category-bar">
              {categories.map((cat, i) => (
                <div
                  key={i}
                  className="category-bar-segment"
                  style={{ width: `${cat.pct}%`, background: cat.color }}
                />
              ))}
            </div>
            <div className="category-list">
              {categories.map((cat, i) => (
                <div key={i} className="category-list-item">
                  <div className="category-list-left">
                    <span className="category-dot" style={{ background: cat.color }} />
                    <span className="category-label">{t(cat.label)}</span>
                  </div>
                  <div className="category-list-right">
                    <span className="category-value">{cat.value.toLocaleString()}</span>
                    <span className="category-pct">({cat.pct}%)</span>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
