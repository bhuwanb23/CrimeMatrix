import { useState, useMemo } from 'react'
import AlertStats from './alerts/AlertStats'
import AlertFilters from './alerts/AlertFilters'
import AlertCard from './alerts/AlertCard'
import AlertMap from './alerts/AlertMap'
import { alerts as initialAlerts } from './alerts/alertsData'

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(initialAlerts)
  const [activeFilter, setActiveFilter] = useState('all')

  const filteredAlerts = useMemo(() => {
    if (activeFilter === 'all') return alerts
    return alerts.filter((a) => a.type === activeFilter)
  }, [alerts, activeFilter])

  const handleAccept = (id) => {
    setAlerts((prev) => prev.map((a) => a.id === id ? { ...a, status: 'resolved' } : a))
  }

  const handleReject = (id) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id))
  }

  const handleView = (alert) => {
    // Would navigate to case detail
    console.log('View alert:', alert)
  }

  return (
    <div className="alerts-page">
      <div className="alerts-header">
        <div>
          <h1 className="alerts-title">Intelligence Alerts</h1>
          <p className="alerts-subtitle">Proactive intelligence notifications</p>
        </div>
      </div>

      <AlertStats alerts={alerts} />

      <div className="alerts-body">
        <div className="alerts-feed">
          <AlertFilters activeFilter={activeFilter} onFilterChange={setActiveFilter} />

          <div className="alerts-list">
            {filteredAlerts.map((alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onAccept={handleAccept}
                onReject={handleReject}
                onView={handleView}
              />
            ))}

            {filteredAlerts.length === 0 && (
              <div className="alerts-empty">
                <p>No alerts matching this filter</p>
              </div>
            )}
          </div>
        </div>

        <AlertMap alerts={filteredAlerts} />
      </div>
    </div>
  )
}
