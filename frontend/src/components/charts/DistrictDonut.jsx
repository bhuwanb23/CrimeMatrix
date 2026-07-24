import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByDistrict } from '../../services/analyticsLive'

const COLORS = ['#e57373', '#ef9a9a', '#ffcdd2', '#fbe9e7', '#f5f5f5', '#e0e0e0']

export default function DistrictDonut() {
  const { t } = useLanguage()
  const [districts, setDistricts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await getCountsByDistrict()
        const rows = Array.isArray(res?.data) ? res.data : []
        const mapped = rows
          .filter((r) => (r.value || 0) > 0)
          .slice(0, 6)
          .map((r, i) => ({
            name: r.key || 'Other',
            value: r.value || 0,
            color: COLORS[i % COLORS.length],
          }))
        if (!cancelled) setDistricts(mapped)
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const total = districts.reduce((s, d) => s + d.value, 0)

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">{t('Cases by District')}</h3>
      </div>
      <div className="chart-card-body donut-body">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : districts.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No district data')}</p>
        ) : (
          <>
            <div className="donut-chart-wrapper">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={districts}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={85}
                    paddingAngle={2}
                    dataKey="value"
                    strokeWidth={0}
                  >
                    {districts.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="donut-center">
                <span className="donut-center-value">{total.toLocaleString()}</span>
                <span className="donut-center-label">{t('Total')}</span>
              </div>
            </div>
            <div className="donut-legend">
              {districts.map((d, i) => (
                <div key={i} className="donut-legend-item">
                  <span className="donut-legend-dot" style={{ background: d.color }} />
                  <span className="donut-legend-name">{t(d.name)}</span>
                  <span className="donut-legend-value">{d.value}</span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
