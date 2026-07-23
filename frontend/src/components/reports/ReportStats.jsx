import {
  ResponsiveContainer, PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts'
import { reports, reportTypes, weeklyData } from './reportsData'
import { useLanguage } from '../../context/LanguageContext'


export default function ReportStats() {
  const { t } = useLanguage()
  const typeCounts = Object.entries(reportTypes).map(([id, info]) => ({
    name: info.label,
    value: reports.filter((r) => r.type === id).length,
    color: info.color,
  }))

  const totalReports = reports.length

  return (
    <div className="report-stats-section">
      {/* Donut Chart */}
      <div className="report-stats-card">
        <div className="report-stats-header">
          <h3>{t('Report Statistics')}</h3>
          <span className="report-stats-subtitle">{t('Today')}</span>
        </div>
        <div className="report-donut-area">
          <div className="report-donut-wrapper">
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={typeCounts}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {typeCounts.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="report-donut-center">
              <span className="report-donut-value">{totalReports}</span>
              <span className="report-donut-label">{t('Reports')}</span>
            </div>
          </div>
          <div className="report-donut-legend">
            {typeCounts.map((d, i) => (
              <div key={i} className="report-legend-item">
                <span className="report-legend-dot" style={{ background: d.color }} />
                <span className="report-legend-name">{d.name}</span>
                <span className="report-legend-count">{d.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bar Chart */}
      <div className="report-stats-card bar-card">
        <div className="report-stats-header">
          <h3>{t('Current Week')}</h3>
          <div className="report-bar-tags">
            {Object.entries(reportTypes).map(([id, info]) => (
              <span key={id} className="report-bar-tag" style={{ background: info.color + '15', color: info.color }}>
                {info.label}
              </span>
            ))}
          </div>
        </div>
        <div className="report-bar-chart">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={weeklyData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
              <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
              <Tooltip
                contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
              />
              <Bar dataKey="investigation" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="court" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="export" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
