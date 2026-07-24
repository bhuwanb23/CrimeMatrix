import { useState, useEffect, useCallback, useMemo } from 'react'
import { Bell, RefreshCw, CheckCircle, AlertTriangle, Shield, MapPin, TrendingUp, Search, BarChart3 } from 'lucide-react'
import { listAlerts, detectAlerts, acknowledgeAlert, getEarlyWarningStats } from '../services/earlyWarning'
import { useLanguage } from '../context/LanguageContext'

const severityColors = { critical: '#ef4444', high: '#f59e0b', medium: '#3b82f6', low: '#10b981' }
const alertTypeIcons = { spike: TrendingUp, hotspot: MapPin, serial: AlertTriangle, escalation: Shield }
const alertTypeMeta = {
  spike: { label: 'Spike', color: '#ef4444' },
  hotspot: { label: 'Hotspot', color: '#f59e0b' },
  serial: { label: 'Serial', color: '#8b5cf6' },
  escalation: { label: 'Escalation', color: '#3b82f6' },
}

const tabs = [
  { id: 'early-warning', label: 'Early Warning', icon: Bell },
  { id: 'analytics', label: 'Alert Analytics', icon: BarChart3 },
]

export default function UnifiedAlertsPage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState('early-warning')
  const [ewAlerts, setEwAlerts] = useState([])
  const [allAlerts, setAllAlerts] = useState([])
  const [ewStats, setEwStats] = useState(null)
  const [ewLoading, setEwLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)
  const [filter, setFilter] = useState('active')

  const loadEarlyWarning = useCallback(async () => {
    setEwLoading(true)
    try {
      const [alertsRes, allRes, statsRes] = await Promise.all([
        listAlerts({ status: filter === 'all' ? undefined : filter }),
        listAlerts({}),
        getEarlyWarningStats(),
      ])
      setEwAlerts(alertsRes?.data?.items || [])
      setAllAlerts(allRes?.data?.items || alertsRes?.data?.items || [])
      setEwStats(statsRes?.data || statsRes)
    } catch (e) { console.error(e) } finally { setEwLoading(false) }
  }, [filter])

  useEffect(() => { loadEarlyWarning() }, [loadEarlyWarning])

  async function handleDetect() {
    setDetecting(true)
    try { await detectAlerts(); await loadEarlyWarning() } catch (e) { console.error(e) } finally { setDetecting(false) }
  }

  async function handleAcknowledge(alertId) {
    try {
      await acknowledgeAlert(alertId)
      setEwAlerts(ewAlerts.map(a => a.id === alertId ? { ...a, status: 'acknowledged' } : a))
      setAllAlerts(allAlerts.map(a => a.id === alertId ? { ...a, status: 'acknowledged' } : a))
    } catch (e) { console.error(e) }
  }

  const typeBreakdown = useMemo(() => {
    const counts = {}
    for (const alert of allAlerts) {
      const key = alert.alert_type || alert.type || 'unknown'
      counts[key] = (counts[key] || 0) + 1
    }
    return Object.entries(counts).map(([id, value]) => ({
      name: alertTypeMeta[id]?.label || id,
      value,
      color: alertTypeMeta[id]?.color || severityColors[id] || '#64748b',
    }))
  }, [allAlerts])

  const statusBreakdown = useMemo(() => {
    const counts = { active: 0, acknowledged: 0, resolved: 0 }
    for (const alert of allAlerts) {
      const status = alert.status || 'active'
      if (status in counts) counts[status] += 1
      else counts.active += 1
    }
    return [
      { label: 'Active', count: counts.active, color: '#ef4444' },
      { label: 'Acknowledged', count: counts.acknowledged, color: '#f59e0b' },
      { label: 'Resolved', count: counts.resolved, color: '#10b981' },
    ]
  }, [allAlerts])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-orange-500/20 shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <Bell size={20} />
              </div>
              <div>
                <h1 className="text-lg font-bold">{t('Alerts & Early Warning')}</h1>
                <p className="text-white/80 text-xs">{t('Proactive crime monitoring and risk detection')}</p>
              </div>
            </div>
            <button onClick={handleDetect} disabled={detecting}
              className="flex items-center gap-1.5 px-4 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-xs font-semibold transition-all disabled:opacity-50">
              {detecting ? <RefreshCw size={14} className="animate-spin" /> : <Search size={14} />}
              {detecting ? t('Detecting...') : t('Run Detection')}
            </button>
          </div>
        </div>

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
                {t(tab.label)}
              </button>
            )
          })}
        </div>

        {activeTab === 'early-warning' && (
          <EarlyWarningTab
            alerts={ewAlerts} stats={ewStats} loading={ewLoading}
            filter={filter} setFilter={setFilter} onAcknowledge={handleAcknowledge}
            t={t}
          />
        )}
        {activeTab === 'analytics' && (
          <AlertAnalyticsTab
            typeBreakdown={typeBreakdown}
            statusBreakdown={statusBreakdown}
            recentAlerts={allAlerts.slice(0, 4)}
            t={t}
          />
        )}
      </div>
    </div>
  )
}

function EarlyWarningTab({ alerts, stats, loading, filter, setFilter, onAcknowledge, t }) {
  return (
    <div className="space-y-5">
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
              <span className="block text-[10px] font-semibold text-slate-500 uppercase mt-1">{t(card.label)}</span>
            </div>
          ))}
        </div>
      )}

      <div className="flex gap-1">
        {['active', 'acknowledged', 'all'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === f ? 'bg-orange-500 text-white' : 'bg-white text-slate-500 border border-slate-200 hover:border-orange-300'
            }`}>
            {t(f.charAt(0).toUpperCase() + f.slice(1))}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-orange-500 rounded-full animate-spin" />
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-xl p-8 text-center">
          <Bell size={32} className="text-slate-300 mx-auto mb-2" />
          <p className="text-sm text-slate-500">{t('No alerts found')}</p>
          <p className="text-xs text-slate-400">{t('Click "Run Detection" to scan for early warning signals')}</p>
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
                      style={{ color, background: `${color}15` }}>{t(alert.severity)}</span>
                  </div>
                  <p className="text-xs text-slate-500 mb-2">{alert.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] text-slate-400">{t('Confidence')}: {alert.confidence}%</span>
                    {alert.status === 'active' && (
                      <button onClick={() => onAcknowledge(alert.id)}
                        className="flex items-center gap-1 text-[10px] font-medium text-orange-600 hover:text-orange-700">
                        <CheckCircle size={12} /> {t('Acknowledge')}
                      </button>
                    )}
                    {alert.status === 'acknowledged' && (
                      <span className="text-[10px] text-slate-400 italic">{t('Acknowledged')}</span>
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

function AlertAnalyticsTab({ typeBreakdown, statusBreakdown, recentAlerts, t }) {
  const maxType = Math.max(...typeBreakdown.map(d => d.value), 1)

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">{t('Alerts by Type')}</h3>
        {typeBreakdown.length === 0 ? (
          <p className="text-xs text-slate-400 m-0">{t('No alert data yet')}</p>
        ) : (
          <div className="space-y-2">
            {typeBreakdown.map((item, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-20">{t(item.name)}</span>
                <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${(item.value / maxType) * 100}%`, background: item.color }} />
                </div>
                <span className="text-xs font-semibold text-slate-700 w-6 text-right">{item.value}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">{t('Alert Status')}</h3>
        <div className="space-y-2">
          {statusBreakdown.map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ background: item.color }} />
              <span className="text-xs text-slate-500 flex-1">{t(item.label)}</span>
              <span className="text-xs font-semibold text-slate-700">{item.count}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-3">{t('Recent Alerts')}</h3>
        {recentAlerts.length === 0 ? (
          <p className="text-xs text-slate-400 m-0">{t('No recent alerts')}</p>
        ) : (
          <div className="space-y-2">
            {recentAlerts.map((alert) => {
              const color = severityColors[alert.severity] || '#64748b'
              return (
                <div key={alert.id} className="flex items-start gap-2 p-2 bg-slate-50 rounded-lg">
                  <div className="w-6 h-6 rounded flex items-center justify-center text-xs"
                    style={{ background: `${color}20`, color }}>
                    <AlertTriangle size={12} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-slate-900 truncate">{alert.title}</p>
                    <p className="text-[10px] text-slate-400">
                      {alert.alert_type || alert.type || 'alert'}
                      {alert.district ? ` • ${alert.district}` : ''}
                    </p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
