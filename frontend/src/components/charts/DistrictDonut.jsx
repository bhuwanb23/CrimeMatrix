import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { useLanguage } from '../../context/LanguageContext'

const districts = [
  { name: 'Bengaluru Urban', value: 420, color: '#e57373' },
  { name: 'Bengaluru Rural', value: 210, color: '#ef9a9a' },
  { name: 'Mysuru', value: 180, color: '#ffcdd2' },
  { name: 'Mangaluru', value: 150, color: '#fbe9e7' },
  { name: 'Hubballi', value: 120, color: '#f5f5f5' },
  { name: 'Other', value: 204, color: '#e0e0e0' },
]

const total = districts.reduce((s, d) => s + d.value, 0)

export default function DistrictDonut() {
  const { t } = useLanguage()

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">{t('Cases by District')}</h3>
        <button className="chart-card-menu" aria-label="More options">⋯</button>
      </div>
      <div className="chart-card-body donut-body">
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
      </div>
    </div>
  )
}

