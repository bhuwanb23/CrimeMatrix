import { useState } from 'react'
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip,
} from 'recharts'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateCalendarDay } from '../../utils/translate'

const data = [
  { day: 'Sun', cases: 18, resolved: 14 },
  { day: 'Mon', cases: 24, resolved: 20 },
  { day: 'Tue', cases: 21, resolved: 18 },
  { day: 'Wed', cases: 28, resolved: 22 },
  { day: 'Thu', cases: 22, resolved: 19 },
  { day: 'Fri', cases: 30, resolved: 25 },
  { day: 'Sat', cases: 15, resolved: 12 },
]

function CustomTooltip({ active, payload, label }) {
  const { lang } = useLanguage()
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <p className="chart-tooltip-label">{translateCalendarDay(label, lang)}</p>
      <p className="chart-tooltip-value">{payload[0].value} {t('cases_label', lang)}</p>
    </div>
  )
}

export default function CaseTrendChart() {
  const { lang } = useLanguage()
  const [interval, setInterval] = useState('Weekly')

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <div className="chart-card-title-group">
          <h3 className="chart-card-title">{t('case_trend', lang)}</h3>
          <span className="chart-legend">
            <span className="chart-legend-dot" style={{ background: '#e57373' }} />
            {t('resolved', lang)}: 130
          </span>
        </div>
        <div className="chart-card-actions">
          <span className="chart-card-label">{t('time_interval', lang)}</span>
          <select
            className="chart-select"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
          >
            <option value="Weekly">{t('weekly', lang)}</option>
            <option value="Monthly">{t('monthly', lang)}</option>
            <option value="Yearly">{t('yearly', lang)}</option>
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
              tickFormatter={(v) => translateCalendarDay(v, lang)}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
              tickFormatter={(v) => `${v}`}
            />
            <Tooltip content={<CustomTooltip />} />
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
