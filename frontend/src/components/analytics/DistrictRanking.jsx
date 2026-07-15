import { districtRanking } from './analyticsData'

const flagEmoji = {
  'Bengaluru Urban': '🏙️',
  'Mysuru': '🏰',
  'Mangaluru': '⚓',
  'Hubballi': '🏛️',
  'Other': '📍',
}

export default function DistrictRanking() {
  return (
    <div className="analytics-district-card">
      <div className="analytics-district-header">
        <h3>Top Districts</h3>
        <span className="analytics-district-subtitle">by case count</span>
      </div>

      <div className="analytics-district-list">
        {districtRanking.map((d, i) => (
          <div key={i} className="district-item">
            <div className="district-item-left">
              <span className="district-flag">{flagEmoji[d.district] || '📍'}</span>
              <span className="district-name">{d.district}</span>
            </div>
            <div className="district-item-right">
              <span className="district-percentage">{d.percentage}%</span>
              <span className="district-cases">{d.cases.toLocaleString()} cases</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
