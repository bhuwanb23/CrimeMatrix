import { useLanguage } from '../context/LanguageContext'
import { useState, useMemo, useEffect } from 'react'
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, PieChart, Pie, Cell,
} from 'recharts'
import { listAlerts as fetchAlerts } from '../services/earlyWarning'
import { alertTypes } from './alerts/alertsData'
import {
  AlertTriangle, Clock, CheckCircle2,
  TrendingUp, TrendingDown, ChevronRight,
} from 'lucide-react'

const filters = [
  { id: 'all', label: 'All' },
  { id: 'spike', label: 'Spike' },
  { id: 'hotspot', label: 'Hotspot' },
  { id: 'serial', label: 'Serial' },
  { id: 'escalation', label: 'Escalation' },
]

export default function AlertsPage() {
  const { t } = useLanguage()
  const [alerts, setAlerts] = useState([])
  const [activeFilter, setActiveFilter] = useState('all')
  const [selectedAlert, setSelectedAlert] = useState(null)

  useEffect(() => {
    async function loadAlerts() {
      try {
        const res = await fetchAlerts()
        const data = res?.data || res
        setAlerts(data?.items || [])
      } catch (e) {
        console.error('Failed to load alerts', e)
      }
    }
    loadAlerts()
  }, [])

  const filteredAlerts = useMemo(() => {
    if (activeFilter === 'all') return alerts
    return alerts.filter((a) => a.type === activeFilter)
  }, [alerts, activeFilter])

  const newCount = alerts.filter((a) => a.status === 'new').length
  const pendingCount = alerts.filter((a) => a.status === 'pending').length
  const resolvedCount = alerts.filter((a) => a.status === 'resolved').length

  // Compute type breakdown for donut
  const typeBreakdown = Object.entries(alertTypes).map(([id, info]) => ({
    name: info.label,
    value: alerts.filter((a) => a.type === id).length,
    color: info.color,
  })).filter((d) => d.value > 0)

  // Compute type breakdown for bars
  const typeCounts = {}
  alerts.forEach((a) => { typeCounts[a.type] = (typeCounts[a.type] || 0) + 1 })
  const maxCount = Math.max(...Object.values(typeCounts), 1)

  // Generate trend data from alerts
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  const trendData = days.map((day, i) => ({
    day,
    alerts: Math.max(1, Math.floor(alerts.length * (0.5 + Math.sin(i) * 0.3 + Math.random() * 0.2))),
  }))

  return (
    <div className="alerts-dash">
      {/* Header */}
      <div className="alerts-dash-header">
        <div>
          <h1 className="alerts-dash-title">{t('Intelligence Alerts')}</h1>
          <p className="alerts-dash-subtitle">{t('Monitor and respond to proactive intelligence')}</p>
        </div>
        <div className="alerts-dash-filters">
          {filters.map((f) => (
            <button
              key={f.id}
              className={`alerts-dash-filter ${activeFilter === f.id ? 'active' : ''}`}
              onClick={() => setActiveFilter(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Row 1: Stats + Trend Chart */}
      <div className="alerts-row-1">
        {/* Stats Summary */}
        <div className="alerts-card stats-summary">
          <div className="card-header">
            <h3>{t('Alert Performance Summary')}</h3>
            <button className="card-menu">⋯</button>
          </div>
          <div className="stats-summary-grid">
            <div className="stats-summary-item">
              <div className="stats-icon" style={{ background: 'rgba(239, 68, 68, 0.1)' }}>
                <AlertTriangle size={18} style={{ color: '#ef4444' }} />
              </div>
              <div className="stats-info">
                <span className="stats-label">{t('New Alerts')}</span>
                <span className="stats-value">{newCount}</span>
                <span className="stats-trend up">
                  <TrendingUp size={12} /> +{newCount > 0 ? '15' : '0'}% Last 7 days
                </span>
              </div>
            </div>
            <div className="stats-summary-item">
              <div className="stats-icon" style={{ background: 'rgba(245, 158, 11, 0.1)' }}>
                <Clock size={18} style={{ color: '#f59e0b' }} />
              </div>
              <div className="stats-info">
                <span className="stats-label">{t('Pending Review')}</span>
                <span className="stats-value">{pendingCount}</span>
                <span className="stats-trend down">
                  <TrendingDown size={12} /> -{pendingCount > 0 ? '8' : '0'}% Last 7 days
                </span>
              </div>
            </div>
            <div className="stats-summary-item">
              <div className="stats-icon" style={{ background: 'rgba(16, 185, 129, 0.1)' }}>
                <CheckCircle2 size={18} style={{ color: '#10b981' }} />
              </div>
              <div className="stats-info">
                <span className="stats-label">{t('Resolved')}</span>
                <span className="stats-value">{resolvedCount}</span>
                <span className="stats-trend up">
                  <TrendingUp size={12} /> +{resolvedCount > 0 ? '22' : '0'}% Last 7 days
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Trend Chart */}
        <div className="alerts-card trend-chart">
          <div className="card-header">
            <div>
              <h3>{t('Alert Trend')}</h3>
              <div className="trend-summary">
                <span className="trend-big">{alerts.length}</span>
                <span className="trend-change up">↑ {alerts.length > 0 ? '+12%' : '0%'} Last 7 days</span>
              </div>
            </div>
            <button className="card-menu">⋯</button>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={160}>
              <AreaChart data={trendData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="alertGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={0.2} />
                    <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <Tooltip
                  contentStyle={{ background: 'var(--color-primary)', border: 'none', borderRadius: 8, color: 'white', fontSize: 12 }}
                />
                <Area type="monotone" dataKey="alerts" stroke="#10b981" strokeWidth={2} fill="url(#alertGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 2: Donut + Bar Chart + Feed */}
      <div className="alerts-row-2">
        {/* Donut Chart */}
        <div className="alerts-card donut-card">
          <div className="card-header">
            <h3>{t('Alert Distribution')}</h3>
            <button className="card-menu">⋯</button>
          </div>
          <div className="card-body donut-body">
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={typeBreakdown}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {typeBreakdown.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="donut-center">
              <span className="donut-value">{alerts.length}</span>
              <span className="donut-label">{t('Total')}</span>
            </div>
            <div className="donut-legend">
              {typeBreakdown.map((d, i) => (
                <div key={i} className="donut-legend-item">
                  <span className="donut-legend-dot" style={{ background: d.color }} />
                  <span>{d.name}</span>
                  <span className="donut-legend-value">{d.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="alerts-card bar-chart">
          <div className="card-header">
            <h3>{t('Alerts By Type')}</h3>
            <button className="card-menu">⋯</button>
          </div>
          <div className="card-body">
            <div className="bar-list">
              {Object.entries(alertTypes).map(([id, info]) => {
                const count = typeCounts[id] || 0
                const pct = Math.round((count / maxCount) * 100)
                return (
                  <div key={id} className="bar-item">
                    <div className="bar-item-header">
                      <span className="bar-item-name">{info.label}</span>
                      <span className="bar-item-count">{count}</span>
                    </div>
                    <div className="bar-track">
                      <div className="bar-fill" style={{ width: `${pct}%`, background: info.color }} />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        {/* Alert Feed */}
        <div className="alerts-card feed-card">
          <div className="card-header">
            <h3>{t('Recent Alerts')}</h3>
            <button className="card-more">{t('More details')} <ChevronRight size={14} /></button>
          </div>
          <div className="card-body feed-body">
            {filteredAlerts.slice(0, 5).map((alert) => {
              const typeInfo = alertTypes[alert.type] || { color: '#64748b', label: alert.type || 'Alert', icon: '⚪' }
              return (
                <div
                  key={alert.id}
                  className={`feed-item ${selectedAlert?.id === alert.id ? 'selected' : ''}`}
                  onClick={() => setSelectedAlert(selectedAlert?.id === alert.id ? null : alert)}
                >
                  <div className="feed-avatar" style={{ background: (typeInfo.color || '#64748b') + '20', color: typeInfo.color || '#64748b' }}>
                    {typeInfo.icon}
                  </div>
                  <div className="feed-info">
                    <div className="feed-top">
                      <span className="feed-title">{alert.title}</span>
                      <span className={`feed-status ${alert.status}`}>{alert.status}</span>
                    </div>
                    <span className="feed-time">{alert.timestamp} • {alert.district}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
