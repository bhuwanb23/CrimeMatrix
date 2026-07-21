import { useState } from 'react'
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  CartesianGrid, Tooltip,
} from 'recharts'
import { monthlyTrend } from './analyticsData'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

function CustomTooltip({ active, payload, label, lang }) {
  if (!active || !payload?.length) return null
  return (
    <div className="analytics-tooltip">
      <p className="analytics-tooltip-label">{label} 2026</p>
      <div className="analytics-tooltip-row">
        <span className="tooltip-dot" style={{ background: '#f59e0b' }} />
        <span>{payload[0].value} {t('cases_label', lang)}</span>
      </div>
      {payload[1] && (
        <div className="analytics-tooltip-row">
          <span className="tooltip-dot" style={{ background: '#10b981' }} />
          <span>{payload[1].value} {t('resolved', lang)}</span>
        </div>
      )}
    </div>
  )
}

export default function CrimeTrendLine() {
  const { lang } = useLanguage()
  const [period, setPeriod] = useState('monthly')

  return (
    <div className="analytics-trend-card">
      <div className="analytics-trend-header">
        <h3>{t('crime_trend', lang)}</h3>
        <div className="analytics-trend-filters">
          {['daily', 'weekly', 'monthly', 'annually'].map((p) => (
            <button
              key={p}
              className={`trend-filter-btn ${period === p ? 'active' : ''}`}
              onClick={() => setPeriod(p)}
            >
              {t(p, lang)}
            </button>
          ))}
        </div>
      </div>

      <div className="analytics-trend-chart">
        <ResponsiveContainer width="100%" height={240}>
          <AreaChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <defs>
              <linearGradient id="gradientCases" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.2} />
                <stop offset="100%" stopColor="#f59e0b" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="gradientResolved" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.2} />
                <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
            <XAxis
              dataKey="month"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
            />
            <Tooltip content={<CustomTooltip lang={lang} />} />
            <Area
              type="monotone"
              dataKey="cases"
              stroke="#f59e0b"
              strokeWidth={2}
              fill="url(#gradientCases)"
            />
            <Area
              type="monotone"
              dataKey="resolved"
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#gradientResolved)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="analytics-trend-legend">
        <div className="legend-item">
          <span className="legend-dot" style={{ background: '#f59e0b' }} />
          <span>{t('cases_filed', lang)}</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot" style={{ background: '#10b981' }} />
          <span>{t('resolved', lang)}</span>
        </div>
      </div>
    </div>
  )
}
