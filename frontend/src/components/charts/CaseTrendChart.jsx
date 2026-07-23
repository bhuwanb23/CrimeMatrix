import { useState } from 'react'
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip,
} from 'recharts'
import { useLanguage } from '../../context/LanguageContext'

const data = [
  { day: 'Sun', cases: 18, resolved: 14 },
  { day: 'Mon', cases: 24, resolved: 20 },
  { day: 'Tue', cases: 21, resolved: 18 },
  { day: 'Wed', cases: 28, resolved: 22 },
  { day: 'Thu', cases: 22, resolved: 19 },
  { day: 'Fri', cases: 30, resolved: 25 },
  { day: 'Sat', cases: 15, resolved: 12 },
]

function CustomTooltip({ active, payload, label, t }) {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <p className="chart-tooltip-label">{t(label)}</p>
      <p className="chart-tooltip-value">{payload[0].value} {t('cases')}</p>
    </div>
  )
}

export default function CaseTrendChart() {
  const { t } = useLanguage()
  const [interval, setInterval] = useState('Weekly')

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <div className="chart-card-title-group">
          <h3 className="chart-card-title">{t('Case Trend')}</h3>
          <span className="chart-legend">
            <span className="chart-legend-dot" style={{ background: '#e57373' }} />
            {t('Resolved')}: 130
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
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
            <XAxis
              dataKey="day"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
              tickFormatter={(v) => t(v)}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
              tickFormatter={(v) => `${v}`}
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
      </div>
    </div>
  )
}

