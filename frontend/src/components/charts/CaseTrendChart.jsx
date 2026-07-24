import { useEffect, useState } from 'react'
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip,
} from 'recharts'
import { useLanguage } from '../../context/LanguageContext'
import { getCrimeTrends, getResolutionTrends } from '../../services/analyticsLive'

function CustomTooltip({ active, payload, label, t }) {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <p className="chart-tooltip-label">{t(label)}</p>
      <p className="chart-tooltip-value">{payload[0].value} {t('cases')}</p>
    </div>
  )
}

function normalizeTrend(res) {
  const data = res?.data?.data || res?.data || []
  if (!Array.isArray(data)) return []
  return data.map((row) => ({
    day: row.date || row.day || row.label || '—',
    cases: row.count ?? row.value ?? row.cases ?? 0,
  }))
}

export default function CaseTrendChart() {
  const { t } = useLanguage()
  const [interval, setInterval] = useState('Weekly')
  const [data, setData] = useState([])
  const [resolved, setResolved] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      const period = interval === 'Monthly' ? 'monthly' : interval === 'Yearly' ? 'yearly' : 'daily'
      try {
        const [trendRes, resRes] = await Promise.all([
          getCrimeTrends(`period=${period}`),
          getResolutionTrends().catch(() => null),
        ])
        if (cancelled) return
        setData(normalizeTrend(trendRes))
        setResolved(resRes?.data?.resolved ?? 0)
      } catch (e) {
        console.error(e)
        if (!cancelled) setData([])
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [interval])

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <div className="chart-card-title-group">
          <h3 className="chart-card-title">{t('Case Trend')}</h3>
          <span className="chart-legend">
            <span className="chart-legend-dot" style={{ background: '#e57373' }} />
            {t('Resolved')}: {resolved}
          </span>
        </div>
        <div className="chart-card-actions">
          <span className="chart-card-label">{t('Time Interval:')}</span>
          <select
            className="chart-select"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
          >
            <option value="Weekly">{t('Weekly')}</option>
            <option value="Monthly">{t('Monthly')}</option>
            <option value="Yearly">{t('Yearly')}</option>
          </select>
        </div>
      </div>
      <div className="chart-card-body">
        {loading ? (
          <p className="text-sm text-slate-400 m-0 p-4">{t('Loading...')}</p>
        ) : data.length === 0 ? (
          <p className="text-sm text-slate-400 m-0 p-4">{t('No trend data')}</p>
        ) : (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
              <XAxis
                dataKey="day"
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
                tickFormatter={(v) => t(String(v).slice(5) || v)}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
              />
              <Tooltip content={<CustomTooltip t={t} />} />
              <Line
                type="monotone"
                dataKey="cases"
                stroke="#e57373"
                strokeWidth={2.5}
                dot={{ r: 4, fill: '#e57373', strokeWidth: 2, stroke: '#fff' }}
                activeDot={{ r: 6, stroke: '#e57373', strokeWidth: 2, fill: '#fff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
