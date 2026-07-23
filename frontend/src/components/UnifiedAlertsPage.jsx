import { useState, useEffect, useCallback } from 'react'
import { Bell, RefreshCw, CheckCircle, AlertTriangle, Shield, MapPin, TrendingUp, Search, BarChart3 } from 'lucide-react'
import { listAlerts, detectAlerts, acknowledgeAlert, getEarlyWarningStats } from '../services/earlyWarning'
import { alerts as legacyAlerts, alertTypes } from './alerts/alertsData'

const severityColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }
const alertTypeIcons = { spike: TrendingUp, hotspot: MapPin, serial: AlertTriangle, escalation: Shield }

const tabs = [
  { id: 'early-warning', label: 'Early Warning', icon: Bell },
  { id: 'analytics', label: 'Alert Analytics', icon: BarChart3 },
]

export default function UnifiedAlertsPage() {
  const [activeTab, setActiveTab] = useState('early-warning')
  const [ewAlerts, setEwAlerts] = useState([])
  const [ewStats, setEwStats] = useState(null)
  const [ewLoading, setEwLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)
  const [filter, setFilter] = useState('active')

  const loadEarlyWarning = useCallback(async () => {
    setEwLoading(true)
    try {
      const [alertsRes, statsRes] = await Promise.all([
        listAlerts({ status: filter }),
        getEarlyWarningStats(),
      ])
      setEwAlerts(alertsRes?.data?.items || [])
      setEwStats(statsRes?.data || statsRes)
    } catch (e) { console.error(e) } finally { setEwLoading(false) }
  }, [filter])

  useEffect(() => { loadEarlyWarning() }, [loadEarlyWarning])

  async function handleDetect() {
    setDetecting(true)
    try { await detectAlerts(); await loadEarlyWarning() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleAcknowledge(alertId) {
    try { await acknowledgeAlert(alertId); setEwAlerts(ewAlerts.map(a => a.id === alertId ? { ...a, status: 'acknowledged' } : a)) } catch (e) { console.error(e) }
  }

  const typeBreakdown = Object.entries(alertTypes).map(([id, info]) => ({
    name: info.label, value: legacyAlerts.filter(a => a.type === id).length, color: info.color,
  })).filter(d => d.value > 0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Bell size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Alerts & Early Warning</h1>
                <p className="text-white/80 text-sm mt-0.5">Proactive crime monitoring and risk detection</p>
              </div>
            </div>
            <button onClick={handleDetect} disabled={detecting}
              className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
              {detecting ? <RefreshCw size={14} className="animate-spin" /> : <Search size={14} />}
              {detecting ? 'Detecting...' : 'Run Detection'}
            </button>
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1 w-fit">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-orange-500 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'early-warning' && (
          <EarlyWarningTab
            alerts={ewAlerts} stats={ewStats} loading={ewLoading}
            filter={filter} setFilter={setFilter} onAcknowledge={handleAcknowledge}
          />
        )}
        {activeTab === 'analytics' && (
          <AlertAnalyticsTab typeBreakdown={typeBreakdown} />
        )}
      </div>
    </div>
  )
}

function EarlyWarningTab({ alerts, stats, loading, filter, setFilter, onAcknowledge }) {
  return (
    <div className="space-y-5">
      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: 'Active Alerts', value: stats.active || 0, color: 'text-red-500', bg: 'bg-red-50', border: 'border-red-200' },
            { label: 'Critical', value: stats.critical || 0, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' },
            { label: 'High Priority', value: stats.high || 0, color: 'text-orange-500', bg: 'bg-orange-50', border: 'border-orange-200' },
            { label: 'Total', value: stats.total || 0, color: 'text-blue-500', bg: 'bg-blue-50', border: 'border-blue-200' },
          ].map((card, i) => (
            <div key={i} className={`${card.bg} ${card.border} border rounded-xl p-4`}>
              <span className={`text-2xl font-bold ${card.color}`}>{card.value}</span>
              <span className="block text-[10px] font-semibold text-slate-500 uppercase mt-1">{card.label}</span>
            </div>
          ))}
        </div>
      )}

      {/* Filter */}
      <div className="flex gap-1">
        {['active', 'acknowledged', 'all'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === f ? 'bg-orange-500 text-white' : 'bg-white text-slate-500 border border-slate-200 hover:border-orange-300'
            }`}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Alerts List */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-orange-500 rounded-full animate-spin" />
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-xl p-8 text-center">
          <Bell size={32} className="text-slate-300 mx-auto mb-2" />
          <p className="text-sm text-slate-500">No alerts found</p>
          <p className="text-xs text-slate-400">Click "Run Detection" to scan for early warning signals</p>
        </div>
      ) : (
        <div className="space-y-2">
          {alerts.map(alert => {
            const Icon = alertTypeIcons[alert.alert_type] || AlertTriangle
            const color = severityColors[alert.severity] || '#64748b'
            return (
              <div key={alert.id} className={`bg-white border border-slate-200 rounded-xl p-4 flex items-start gap-3 transition-all hover:border-slate-300 ${alert.status === 'acknowledged' ? 'opacity-60' : ''}`}>
                <div className="w-2 h-full rounded-full flex-shrink-0" style={{ background: color }} />
                <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style={{ background: `${color}15` }}>
                  <Icon size={16} style={{ color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-slate-900">{alert.title}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase"
                      style={{ color, background: `${color}15` }}>{alert.severity}</span>
                  </div>
                  <p className="text-xs text-slate-500 mb-2">{alert.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] text-slate-400">Confidence: {alert.confidence}%</span>
                    {alert.status === 'active' && (
                      <button onClick={() => onAcknowledge(alert.id)}
                        className="flex items-center gap-1 text-[10px] font-medium text-orange-600 hover:text-orange-700">
                        <CheckCircle size={12} /> Acknowledge
                      </button>
                    )}
                    {alert.status === 'acknowledged' && (
                      <span className="text-[10px] text-slate-400 italic">Acknowledged</span>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

function AlertAnalyticsTab({ typeBreakdown }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Alert Type Breakdown */}
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">Alerts by Type</h3>
        <div className="space-y-2">
          {typeBreakdown.map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-20">{item.name}</span>
              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${(item.value / Math.max(...typeBreakdown.map(d => d.value), 1)) * 100}%`, background: item.color }} />
              </div>
              <span className="text-xs font-semibold text-slate-700 w-6 text-right">{item.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Alert Status */}
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">Alert Status</h3>
        <div className="space-y-2">
          {[
            { label: 'New', count: legacyAlerts.filter(a => a.status === 'new').length, color: '#ef4444' },
            { label: 'Pending', count: legacyAlerts.filter(a => a.status === 'pending').length, color: '#f59e0b' },
            { label: 'Resolved', count: legacyAlerts.filter(a => a.status === 'resolved').length, color: '#10b981' },
          ].map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ background: item.color }} />
              <span className="text-xs text-slate-500 flex-1">{item.label}</span>
              <span className="text-xs font-semibold text-slate-700">{item.count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Alerts Feed */}
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">Recent Alerts</h3>
        <div className="space-y-2">
          {legacyAlerts.slice(0, 4).map((alert, i) => {
            const typeInfo = alertTypes[alert.type] || { color: '#64748b', icon: '⚪' }
            return (
              <div key={i} className="flex items-start gap-2 p-2 bg-slate-50 rounded-lg">
                <div className="w-6 h-6 rounded flex items-center justify-center text-xs"
                  style={{ background: (typeInfo.color || '#64748b') + '20', color: typeInfo.color || '#64748b' }}>
                  {typeInfo.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-slate-900 truncate">{alert.title}</p>
                  <p className="text-[10px] text-slate-400">{alert.timestamp} • {alert.district}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
