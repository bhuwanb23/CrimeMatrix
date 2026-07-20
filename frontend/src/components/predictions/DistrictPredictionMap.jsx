import { MapPin } from 'lucide-react'

export default function DistrictPredictionMap({ districts }) {
  if (!districts || districts.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <MapPin size={14} />
          <h3>District Predictions</h3>
        </div>
        <div className="similar-empty"><p>No district predictions</p></div>
      </div>
    )
  }

  const maxCount = Math.max(...districts.map(d => d.crime_count || 0), 1)

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <MapPin size={14} />
        <h3>District Predictions</h3>
      </div>
      <div className="analytics-district-list">
        {districts.map((d, i) => {
          const color = d.risk === 'high' ? '#ef4444' : d.risk === 'medium' ? '#f59e0b' : '#10b981'
          return (
            <div key={i} className="analytics-district-item">
              <div className="analytics-district-header">
                <span className="analytics-district-name">{d.name}</span>
                <span className="analytics-district-count">{d.crime_count || 0}</span>
              </div>
              <div className="analytics-district-bar">
                <div className="analytics-district-fill" style={{ width: `${((d.crime_count || 0) / maxCount) * 100}%`, background: color }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
