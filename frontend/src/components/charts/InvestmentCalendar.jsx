import { useEffect, useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, Briefcase, Clock } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { getActivityTimeseries } from '../../services/analyticsLive'
import { listInvestigations } from '../../services/investigations'

function buildWeekDays(anchor = new Date()) {
  const start = new Date(anchor)
  start.setDate(start.getDate() - start.getDay())
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    return {
      day: d.toLocaleDateString('en', { weekday: 'short' }),
      date: d.getDate(),
      iso: d.toISOString().slice(0, 10),
    }
  })
}

export default function InvestmentCalendar() {
  const { t } = useLanguage()
  const [weekOffset, setWeekOffset] = useState(0)
  const [selectedDay, setSelectedDay] = useState(new Date().getDay())
  const [activeTab, setActiveTab] = useState('activity')
  const [series, setSeries] = useState([])
  const [investigations, setInvestigations] = useState([])
  const [loading, setLoading] = useState(true)

  const weekDays = useMemo(() => {
    const anchor = new Date()
    anchor.setDate(anchor.getDate() + weekOffset * 7)
    return buildWeekDays(anchor)
  }, [weekOffset])

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const [actRes, invRes] = await Promise.all([
          getActivityTimeseries().catch(() => null),
          listInvestigations().catch(() => null),
        ])
        if (cancelled) return
        const act = actRes?.data
        setSeries(Array.isArray(act) ? act : act?.items || [])
        const invData = invRes?.data
        setInvestigations(Array.isArray(invData) ? invData : invData?.items || [])
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const selectedIso = weekDays[selectedDay]?.iso
  const dayActivity = series.filter((r) => (r.date || '').startsWith(selectedIso || ''))
  const dayInvestigations = investigations
    .filter((inv) => {
      const d = (inv.last_accessed || inv.updated_at || inv.created_at || '').slice(0, 10)
      return d === selectedIso
    })
    .slice(0, 5)

  const activityEvents = dayActivity.length
    ? dayActivity.map((r) => ({
        title: `${r.crimes ?? r.total ?? 0} crimes logged`,
        time: r.date || selectedIso,
      }))
    : [{ title: t('No activity recorded for this day'), time: selectedIso || '—' }]

  const invEvents = dayInvestigations.length
    ? dayInvestigations.map((inv) => ({
        title: inv.title || `Investigation #${inv.id}`,
        time: (inv.last_accessed || inv.updated_at || '').slice(0, 16).replace('T', ' '),
      }))
    : [{ title: t('No investigations for this day'), time: selectedIso || '—' }]

  const events = activeTab === 'activity' ? activityEvents : invEvents

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">{t('Investigation Calendar')}</h3>
      </div>
      <div className="chart-card-body">
        <div className="calendar-nav">
          <button type="button" className="calendar-nav-btn" aria-label="Previous week" onClick={() => setWeekOffset((w) => w - 1)}>
            <ChevronLeft size={16} />
          </button>
          <div className="calendar-days">
            {weekDays.map((d, i) => (
              <button
                key={d.iso}
                type="button"
                className={`calendar-day ${i === selectedDay ? 'selected' : ''}`}
                onClick={() => setSelectedDay(i)}
              >
                <span className="calendar-day-name">{t(d.day)}</span>
                <span className="calendar-day-date">{d.date}</span>
              </button>
            ))}
          </div>
          <button type="button" className="calendar-nav-btn" aria-label="Next week" onClick={() => setWeekOffset((w) => w + 1)}>
            <ChevronRight size={16} />
          </button>
        </div>

        <div className="calendar-tabs">
          <button
            type="button"
            className={`calendar-tab ${activeTab === 'activity' ? 'active' : ''}`}
            onClick={() => setActiveTab('activity')}
          >
            <Briefcase size={14} />
            {t('Activity')}
          </button>
          <button
            type="button"
            className={`calendar-tab ${activeTab === 'investigations' ? 'active' : ''}`}
            onClick={() => setActiveTab('investigations')}
          >
            <Clock size={14} />
            {t('Investigations')}
          </button>
        </div>

        <div className="calendar-events">
          {loading ? (
            <p className="text-xs text-slate-400 m-0">{t('Loading...')}</p>
          ) : events.map((event, i) => (
            <div key={i} className="calendar-event">
              <div className="calendar-event-indicator" />
              <div className="calendar-event-content">
                <p className="calendar-event-title">{t(event.title)}</p>
                <p className="calendar-event-time">{event.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
