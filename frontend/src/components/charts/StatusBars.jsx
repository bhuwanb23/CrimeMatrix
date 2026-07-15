const statuses = [
  { label: 'Active', value: 47, pct: 35, color: '#e57373' },
  { label: 'Pending Review', value: 28, pct: 21, color: '#ef9a9a' },
  { label: 'Under Investigation', value: 34, pct: 25, color: '#ffcdd2' },
  { label: 'Closed', value: 25, pct: 19, color: '#e0e0e0' },
]

const maxPct = Math.max(...statuses.map((s) => s.pct))

export default function StatusBars() {
  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">Cases by Status</h3>
        <button className="chart-card-menu" aria-label="More options">⋯</button>
      </div>
      <div className="chart-card-body">
        <div className="status-bars-list">
          {statuses.map((s, i) => (
            <div key={i} className="status-bar-item">
              <div className="status-bar-header">
                <span className="status-bar-label">{s.label}</span>
                <span className="status-bar-pct">{s.pct}%</span>
              </div>
              <div className="status-bar-track">
                <div
                  className="status-bar-fill"
                  style={{
                    width: `${s.pct}%`,
                    background: s.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
