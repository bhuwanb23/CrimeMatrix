import { MapPin, TrendingUp, AlertTriangle, Clock } from 'lucide-react'
import { hotspots, crimeDensity } from './mapData'

export default function DistrictPanel({ selectedDistrict }) {
  return (
    <div className="district-panel">
      <div className="district-panel-header">
        <h3>Geo Intelligence</h3>
      </div>

      {selectedDistrict ? (
        <div className="district-selected">
          <div className="district-selected-header">
            <MapPin size={16} />
            <h4>{selectedDistrict.name}</h4>
          </div>
          <div className="district-selected-stats">
            <div className="district-stat-row">
              <span className="district-stat-label">Total Cases</span>
              <span className="district-stat-value">{selectedDistrict.cases}</span>
            </div>
            <div className="district-stat-row">
              <span className="district-stat-label">Hotspots</span>
              <span className="district-stat-value">{selectedDistrict.hotspots}</span>
            </div>
            <div className="district-stat-row">
              <span className="district-stat-label">Risk Level</span>
              <span className={`district-risk-badge ${selectedDistrict.risk}`}>
                {selectedDistrict.risk}
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div className="district-placeholder">
          <MapPin size={24} />
          <p>Click a district on the map to view details</p>
        </div>
      )}

      {/* Crime Density Legend */}
      <div className="district-section">
        <h4 className="district-section-title">
          <TrendingUp size={14} />
          Crime Density
        </h4>
        <div className="density-legend">
          {crimeDensity.map((d, i) => (
            <div key={i} className="density-item">
              <span className="density-dot" style={{ background: d.color }} />
              <span className="density-label">{d.label}</span>
              <span className="density-count">{d.count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Hotspots */}
      <div className="district-section">
        <h4 className="district-section-title">
          <AlertTriangle size={14} />
          Recent Hotspots
        </h4>
        <div className="hotspots-list">
          {hotspots.slice(0, 5).map((h, i) => (
            <div key={i} className="hotspot-item">
              <span className={`hotspot-dot ${h.severity}`} />
              <div className="hotspot-info">
                <span className="hotspot-name">{h.name}</span>
                <span className="hotspot-cases">{h.cases} cases</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Route Info */}
      <div className="district-section">
        <h4 className="district-section-title">
          <Clock size={14} />
          Active Routes
        </h4>
        <div className="route-legend">
          <div className="route-item">
            <span className="route-line" style={{ background: '#ef4444' }} />
            <span>Suspect Movement</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#3b82f6' }} />
            <span>Evidence Link</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#8b5cf6' }} />
            <span>Phone Records</span>
          </div>
          <div className="route-item">
            <span className="route-line" style={{ background: '#10b981' }} />
            <span>Case Connection</span>
          </div>
        </div>
      </div>
    </div>
  )
}
