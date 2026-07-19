import { MapPin, AlertTriangle } from 'lucide-react'

export default function IntelligenceHotspotPreview({ hotspots }) {
  if (!hotspots) return null

  const districts = hotspots.districts || []
  const topTypes = hotspots.top_crime_types || []
  const maxCount = Math.max(...districts.map(d => d.count), 1)

  return (
    <div className="intel-hotspot-widget">
      <div className="intel-widget-header">
        <h3><MapPin size={14} /> Crime Hotspots</h3>
      </div>

      <div className="intel-hotspot-list">
        {districts.length === 0 ? (
          <div className="similar-empty"><p>No hotspot data</p></div>
        ) : (
          districts.map((d, i) => (
            <div key={i} className="intel-hotspot-item">
              <div className="intel-hotspot-rank">#{i + 1}</div>
              <div className="intel-hotspot-info">
                <span className="intel-hotspot-name">{d.name}</span>
                <div className="intel-hotspot-bar">
                  <div
                    className="intel-hotspot-fill"
                    style={{ width: `${(d.count / maxCount) * 100}%` }}
                  />
                </div>
              </div>
              <span className="intel-hotspot-count">{d.count}</span>
            </div>
          ))
        )}
      </div>

      {topTypes.length > 0 && (
        <div className="intel-hotspot-types">
          <h4><AlertTriangle size={12} /> Top Crime Types</h4>
          <div className="intel-type-tags">
            {topTypes.map((t, i) => (
              <span key={i} className="intel-type-tag">
                {t.name} <span className="intel-type-count">{t.count}</span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
