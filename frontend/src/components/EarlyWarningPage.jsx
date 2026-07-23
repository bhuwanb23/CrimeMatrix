import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect, useCallback } from 'react'
import { Bell, RefreshCw, CheckCircle, AlertTriangle, Shield, MapPin, TrendingUp } from 'lucide-react'
import { listAlerts, detectAlerts, getEarlyWarningStats, acknowledgeAlert } from '../services/earlyWarning'

const severityColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#10b981',
}

const alertTypeIcons = {
  spike: TrendingUp,
  hotspot: MapPin,
  serial: AlertTriangle,
  escalation: Shield,
}

export default function EarlyWarningPage() {
  const { t } = useLanguage()
  const [alerts, setAlerts] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)
  const [filter, setFilter] = useState('active')

  const loadAll = useCallback(async () => {
    setLoading(true)
    try {
      const [alertsRes, statsRes] = await Promise.all([
        listAlerts({ status: filter }),
        getEarlyWarningStats(),
      ])
      setAlerts(alertsRes?.data?.items || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load alerts', e)
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => {
    loadAll()
  }, [loadAll])

  async function handleDetect() {
    setDetecting(true)
    try {
      await detectAlerts()
      await loadAll()
    } catch (e) {
      console.error('Detection failed', e)
    } finally {
      setDetecting(false)
    }
  }

  async function handleAcknowledge(alertId) {
    try {
      await acknowledgeAlert(alertId)
      setAlerts(alerts.map(a => a.id === alertId ? { ...a, status: 'acknowledged' } : a))
    } catch (e) {
      console.error('Failed to acknowledge', e)
    }
  }

  return (
    <div className="early-warning-page">
      <div className="intel-header">
        <div className="intel-header-left">
          <Bell size={22} />
          <div>
            <h1>{t('Early Warning Alerts')}</h1>
            <p>{t('Real-time crime monitoring and risk detection')}</p>
          </div>
        </div>
        <div className="intel-header-actions">
          <button className="similar-btn similar-btn-primary" onClick={handleDetect} disabled={detecting}>
            {detecting ? 'Detecting...' : 'Run Detection'}
          </button>
          <button className="intel-refresh" onClick={loadAll} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="analytics-summary-cards">
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#ef4444' }}>
              <AlertTriangle size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{t('Active')}</span>
              <span className="analytics-pred-value">{stats.active || 0}</span>
            </div>
          </div>
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#ef4444' }}>
              <Shield size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{t('Critical')}</span>
              <span className="analytics-pred-value">{stats.critical || 0}</span>
            </div>
          </div>
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#f59e0b' }}>
              <AlertTriangle size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{t('High')}</span>
              <span className="analytics-pred-value">{stats.high || 0}</span>
            </div>
          </div>
          <div className="analytics-pred-card">
            <div className="analytics-pred-icon" style={{ color: '#3b82f6' }}>
              <Bell size={18} />
            </div>
            <div className="analytics-pred-info">
              <span className="analytics-pred-label">{t('Total')}</span>
              <span className="analytics-pred-value">{stats.total || 0}</span>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="timeline-controls">
        {['active', 'acknowledged', 'all'].map((f) => (
          <button
            key={f}
            className={`intel-time-btn ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Alerts */}
      {loading ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>{t('Loading alerts...')}</span>
        </div>
      {t(') : alerts.length === 0 ? (')}
        <div className="similar-empty">
          <Bell size={32} className="similar-empty-icon" />
          <p>{t('No alerts found')}</p>
          <span>{t('Click "Run Detection" to scan for early warning signals.')}</span>
        </div>
      ) : (
        <div className="ew-alerts-list">
          {alerts.map((alert) => {
            const Icon = alertTypeIcons[alert.alert_type] || AlertTriangle
            const color = severityColors[alert.severity] || '#64748b'
            return (
              <div key={alert.id} className={`ew-alert-card ${alert.status}`}>
                <div className="ew-alert-severity" style={{ background: color }} />
                <div className="ew-alert-icon" style={{ color }}>
                  <Icon size={16} />
                </div>
                <div className="ew-alert-content">
                  <div className="ew-alert-header">
                    <span className="ew-alert-title">{alert.title}</span>
                    <span className="ew-alert-badge" style={{ color, background: `${color}15` }}>
                      {alert.severity}
                    </span>
                  </div>
                  <p className="ew-alert-desc">{alert.description}</p>
                  <div className="ew-alert-meta">
                    <span>Confidence: {alert.confidence}%</span>
                    <span>{alert.created_at ? new Date(alert.created_at).toLocaleDateString() : ''}</span>
                  </div>
                  {alert.status === 'active' && (
                    <button className="similar-btn similar-btn-primary" onClick={() => handleAcknowledge(alert.id)}>
                      <CheckCircle size={12} /> {t('Acknowledge')}
                    </button>
                  )}
                  {alert.status === 'acknowledged' && (
                    <span className="ew-alert-ack">Acknowledged by {alert.acknowledged_by}</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
