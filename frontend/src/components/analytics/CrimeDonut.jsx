import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { crimeTypes, todayStats } from './analyticsData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateCrimeType } from '../../utils/translate'

export default function CrimeDonut() {
  const { lang } = useLanguage()
  const data = crimeTypes.map((t) => ({ name: translateCrimeType(t.name, lang), value: t.count }))
  const colors = crimeTypes.map((t) => t.color)

  return (
    <div className="analytics-donut-card">
      <div className="analytics-donut-header">
        <h3>{t('todays_cases', lang)}</h3>
        <span className="analytics-donut-badge">{t('live', lang)}</span>
      </div>

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
                <Cell key={i} fill={colors[i]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="analytics-donut-center">
          <span className="analytics-donut-value">{todayStats.total}</span>
          <span className="analytics-donut-label">{t('total_cases', lang)}</span>
        </div>
      </div>

      <div className="analytics-donut-stats">
        <div className="analytics-mini-stat">
          <span className="mini-stat-icon" style={{ background: '#f59e0b20', color: '#f59e0b' }}>🔥</span>
          <div className="mini-stat-info">
            <span className="mini-stat-value">{todayStats.theft}</span>
            <span className="mini-stat-label">{t('theft', lang)}</span>
          </div>
        </div>
        <div className="analytics-mini-stat">
          <span className="mini-stat-icon" style={{ background: '#3b82f620', color: '#3b82f6' }}>💳</span>
          <div className="mini-stat-info">
            <span className="mini-stat-value">{todayStats.fraud}</span>
            <span className="mini-stat-label">{t('fraud', lang)}</span>
          </div>
        </div>
        <div className="analytics-mini-stat">
          <span className="mini-stat-icon" style={{ background: '#8b5cf620', color: '#8b5cf6' }}>💻</span>
          <div className="mini-stat-info">
            <span className="mini-stat-value">{todayStats.cyber}</span>
            <span className="mini-stat-label">{t('cybercrime', lang)}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
