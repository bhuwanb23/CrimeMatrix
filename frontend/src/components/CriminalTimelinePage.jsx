import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect, useCallback } from 'react'
import { Clock, RefreshCw, User, FileText, Shield, Camera, AlertTriangle, ArrowRight } from 'lucide-react'
import { getFullTimeline, getTimelineStats, getSuspectTimeline } from '../services/criminalTimeline'

const typeConfig = {
  filing: { icon: FileText, label: 'Filing', color: '#3b82f6' },
  investigation: { icon: Shield, label: 'Investigation', color: '#8b5cf6' },
  evidence: { icon: Camera, label: 'Evidence', color: '#f59e0b' },
  suspect: { icon: AlertTriangle, label: 'Suspect', color: '#ef4444' },
  status: { icon: ArrowRight, label: 'Status Change', color: '#10b981' },
}

const eventTypes = [
  { value: '', label: 'All Types' },
  { value: 'filing', label: 'Filing' },
  { value: 'investigation', label: 'Investigation' },
  { value: 'evidence', label: 'Evidence' },
  { value: 'suspect', label: 'Suspect' },
]

const timeRanges = [
  { value: 7, label: '7D' },
  { value: 30, label: '30D' },
  { value: 90, label: '90D' },
  { value: 365, label: '1Y' },
]

export default function CriminalTimelinePage() {
  const { t } = useLanguage()
  const [timeline, setTimeline] = useState(null)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(90)
  const [eventType, setEventType] = useState('')
  const [suspectSearch, setSuspectSearch] = useState('')
  const [expandedGroup, setExpandedGroup] = useState(null)

  const loadTimeline = useCallback(async () => {
    setLoading(true)
    try {
      const [timelineRes, statsRes] = await Promise.all([
        getFullTimeline({ days, event_type: eventType || undefined }),
        getTimelineStats(),
      ])
      setTimeline(timelineRes?.data || timelineRes)
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load timeline', e)
    } finally {
      setLoading(false)
    }
  }, [days, eventType])

  useEffect(() => {
    loadTimeline()
  }, [loadTimeline])

  async function handleSuspectSearch() {
    if (!suspectSearch.trim()) return
    setLoading(true)
    try {
      const res = await getSuspectTimeline(suspectSearch.trim(), days)
      const data = res?.data || res
      setTimeline({ ...timeline, events: data?.events || [], grouped: {}, total: data?.total || 0 })
    } catch (e) {
      console.error('Failed to search suspect', e)
    } finally {
      setLoading(false)
    }
  }

  const grouped = timeline?.grouped || {}
  const groups = Object.entries(grouped).sort((a, b) => b[0].localeCompare(a[0]))

  return (
    <div className="timeline-page">
      <div className="timeline-header">
        <div className="timeline-header-left">
          <Clock size={22} />
          <div>
            <h1>{t('Criminal Timeline')}</h1>
            <p>{t('Evolution of cases and suspects over time')}</p>
          </div>
        </div>
        <button className="intel-refresh" onClick={loadTimeline} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          {t('Refresh')}
        </button>
      </div>

      {/* Controls */}
      <div className="timeline-controls">
        <div className="timeline-time-btns">
          {timeRanges.map((tr) => (
            <button
              key={tr.value}
              className={`intel-time-btn ${days === tr.value ? 'active' : ''}`}
              onClick={() => setDays(tr.value)}
            >
              {tr.label}
            </button>
          ))}
        </div>

        <select
          className="intel-filter-select"
          value={eventType}
          onChange={(e) => setEventType(e.target.value)}
        >
          {eventTypes.map((et) => (
            <option key={et.value} value={et.value}>{et.label}</option>
          ))}
        </select>

        <div className="timeline-suspect-search">
          <User size={14} />
          <input
            placeholder="Search suspect..."
            value={suspectSearch}
            onChange={(e) => setSuspectSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSuspectSearch()}
          />
          <button className="similar-btn similar-btn-primary" onClick={handleSuspectSearch} disabled={!suspectSearch.trim()}>
            {t('Search')}
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="timeline-stats">
          <div className="timeline-stat">
            <span className="timeline-stat-value">{stats.total_events || 0}</span>
            <span className="timeline-stat-label">{t('Total Events')}</span>
          </div>
          <div className="timeline-stat">
            <span className="timeline-stat-value">{stats.investigations_with_timeline || 0}</span>
            <span className="timeline-stat-label">{t('Investigations')}</span>
          </div>
          {stats.by_type && Object.entries(stats.by_type).map(([type, count]) => (
            <div key={type} className="timeline-stat">
              <span className="timeline-stat-value">{count}</span>
              <span className="timeline-stat-label">{type}</span>
            </div>
          ))}
        </div>
      )}

      {/* Timeline */}
      {loading ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>{t('Loading timeline...')}</span>
        </div>
      ) : groups.length === 0 ? (
        <div className="similar-empty">
          <Clock size={32} className="similar-empty-icon" />
          <p>{t('No timeline events found')}</p>
          <span>{t('Add events to investigations to see them here.')}</span>
        </div>
      ) : (
        <div className="timeline-groups">
          {groups.map(([date, events]) => (
            <div key={date} className="timeline-group">
              <button
                className="timeline-group-header"
                onClick={() => setExpandedGroup(expandedGroup === date ? null : date)}
              >
                <span className="timeline-group-date">{formatGroupDate(date)}</span>
                <span className="timeline-group-count">{events.length} events</span>
              </button>

              {(expandedGroup === date || expandedGroup === null) && (
                <div className="timeline-group-events">
                  {events.map((event, i) => {
                    const config = typeConfig[event.event_type] || typeConfig.investigation
                    const Icon = config.icon
                    return (
                      <div key={event.id || i} className="timeline-event-item">
                        <div className="timeline-event-dot" style={{ background: config.color }}>
                          <Icon size={10} color="white" />
                        </div>
                        <div className="timeline-event-line" style={{ background: config.color + '30' }} />
                        <div className="timeline-event-content">
                          <div className="timeline-event-header">
                            <span className="timeline-event-type" style={{ color: config.color }}>{config.label}</span>
                            <span className="timeline-event-source">{event.source}</span>
                          </div>
                          <p className="timeline-event-title">{event.title}</p>
                          {event.description && (
                            <p className="timeline-event-desc">{event.description}</p>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function formatGroupDate(dateStr) {
  if (!dateStr) return 'Unknown Date'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
  } catch {
    return dateStr
  }
}
