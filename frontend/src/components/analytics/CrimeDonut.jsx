import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByType } from '../../services/analyticsLive'

const COLORS = ['#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#94a3b8', '#10b981']

export default function CrimeDonut() {
  const { t } = useLanguage()
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByType()
        const list = Array.isArray(res?.data) ? res.data : []
        if (!cancelled) setRows(list.filter((r) => (r.value || 0) > 0))
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const data = rows.map((r) => ({ name: r.key, value: r.value }))
  const total = data.reduce((s, d) => s + d.value, 0)
  const top = rows.slice(0, 3)

  return (
    <div className="analytics-donut-card">
      <div className="analytics-donut-header">
        <h3>{t("Today's Cases")}</h3>
        <span className="analytics-donut-badge">{t('Live')}</span>
      </div>

      {loading ? (
        <p className="text-sm text-slate-400 p-4 m-0">{t('Loading...')}</p>
      ) : data.length === 0 ? (
        <p className="text-sm text-slate-400 p-4 m-0">{t('No case data')}</p>
      ) : (
        <>
          <div className="analytics-donut-chart">
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {data.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="analytics-donut-center">
              <span className="analytics-donut-value">{total}</span>
              <span className="analytics-donut-label">{t('Total Cases')}</span>
            </div>
          </div>

          <div className="analytics-donut-stats">
            {top.map((r, i) => (
              <div key={r.key} className="analytics-mini-stat">
                <span className="mini-stat-icon" style={{ background: `${COLORS[i]}20`, color: COLORS[i] }}>●</span>
                <div className="mini-stat-info">
                  <span className="mini-stat-value">{r.value}</span>
                  <span className="mini-stat-label">{t(r.key)}</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
