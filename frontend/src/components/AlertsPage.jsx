import { useState, useMemo } from 'react'
import AlertStats from './alerts/AlertStats'
import AlertMap from './alerts/AlertMap'
import AlertFeed from './alerts/AlertFeed'
import AlertTypeChart from './alerts/AlertTypeChart'
import RecentActivity from './alerts/RecentActivity'
import { alerts as initialAlerts } from './alerts/alertsData'

const filters = [
  { id: 'all', label: 'All' },
  { id: 'whisper', label: 'Whisper' },
  { id: 'fir-match', label: 'FIR Match' },
  { id: 'cross-district', label: 'Cross-District' },
  { id: 'evidence', label: 'Evidence' },
  { id: 'ai', label: 'AI' },
]

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(initialAlerts)
  const [activeFilter, setActiveFilter] = useState('all')
  const [selectedAlert, setSelectedAlert] = useState(null)

  const filteredAlerts = useMemo(() => {
    if (activeFilter === 'all') return alerts
    return alerts.filter((a) => a.type === activeFilter)
  }, [alerts, activeFilter])

  const handleAlertSelect = (alert) => {
    setSelectedAlert((prev) => prev?.id === alert.id ? null : alert)
  }

  return (
    <div className="alerts-dashboard">
      <div className="alerts-dashboard-header">
        <div>
          <h1 className="alerts-dashboard-title">Intelligence Alerts</h1>
          <p className="alerts-dashboard-subtitle">Proactive intelligence & crime monitoring</p>
        </div>
        <div className="alerts-filter-tabs">
          {filters.map((f) => (
            <button
              key={f.id}
              className={`alerts-filter-tab ${activeFilter === f.id ? 'active' : ''}`}
              onClick={() => setActiveFilter(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <AlertStats alerts={alerts} />

      <div className="alerts-dashboard-grid">
        <div className="alerts-grid-left">
          <AlertMap
            alerts={filteredAlerts}
            onAlertSelect={handleAlertSelect}
            selectedAlert={selectedAlert}
          />
          <AlertTypeChart alerts={alerts} />
        </div>

        <div className="alerts-grid-right">
          <AlertFeed
            alerts={filteredAlerts}
            onAlertSelect={handleAlertSelect}
            selectedAlert={selectedAlert}
          />
          <RecentActivity />
        </div>
      </div>
    </div>
  )
}
