import { MapPin, X, TrendingUp, AlertTriangle } from 'lucide-react'
import { hotspots, crimeDensity } from './mapData'

export default function DistrictPanel({ selectedDistrict, onClose }) {
  return (
    <aside
      className={`district-panel ${selectedDistrict ? 'is-open' : ''}`}
      aria-label="District details"
    >
      <div className="district-panel-header">
        <h2>{selectedDistrict ? selectedDistrict.name : 'Overview'}</h2>
        {selectedDistrict && (
          <button
            type="button"
            className="district-close-btn"
            onClick={onClose}
            aria-label="Close district details"
          >
            <X size={16} />
          </button>
        )}
      </div>

      <div className="district-panel-body">
        {selectedDistrict ? (
          <div className="district-selected">
            <div className="district-selected-header">
              <MapPin size={15} aria-hidden="true" />
              <span>Selected district</span>
            </div>
            <div className="district-selected-stats">
              <div className="district-stat-row">
                <span className="district-stat-label">Total cases</span>
                <span className="district-stat-value">{selectedDistrict.cases ?? selectedDistrict.crime_count ?? '—'}</span>
              </div>
              <div className="district-stat-row">
                <span className="district-stat-label">Hotspots</span>
                <span className="district-stat-value">{selectedDistrict.hotspots ?? '—'}</span>
              </div>
              <div className="district-stat-row">
                <span className="district-stat-label">Risk</span>
                <span className={`district-risk-badge ${selectedDistrict.risk || selectedDistrict.risk_level || 'low'}`}>
                  {selectedDistrict.risk || selectedDistrict.risk_level || '—'}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="district-placeholder">
            <MapPin size={20} aria-hidden="true" />
            <p>Select a district on the map</p>
          </div>
        )}

        <section className="district-section">
          <h3 className="district-section-title">
            <TrendingUp size={13} aria-hidden="true" />
            Density
          </h3>
          <div className="density-legend">
            {crimeDensity.map((d, i) => (
              <div key={i} className="density-item">
                <span className="density-dot" style={{ background: d.color }} />
                <span className="density-label">{d.label}</span>
                <span className="density-count">{d.count}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="district-section">
          <h3 className="district-section-title">
            <AlertTriangle size={13} aria-hidden="true" />
            Hotspots
          </h3>
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
        </section>
      </div>
    </aside>
  )
}
