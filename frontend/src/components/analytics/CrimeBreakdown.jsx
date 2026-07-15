import { crimeTypes } from './analyticsData'

export default function CrimeBreakdown() {
  return (
    <div className="analytics-breakdown-card">
      <div className="analytics-breakdown-header">
        <h3>Crime Type Breakdown</h3>
      </div>

      <div className="analytics-breakdown-list">
        {crimeTypes.map((type, i) => (
          <div key={i} className="breakdown-item">
            <div className="breakdown-item-header">
              <span className="breakdown-name">{type.name}</span>
              <span className="breakdown-stats">
                {type.percentage}% • {type.count.toLocaleString()} cases
              </span>
            </div>
            <div className="breakdown-bar">
              <div
                className="breakdown-bar-fill"
                style={{ width: `${type.percentage}%`, background: type.color }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
