import { useState } from 'react'
import { ChevronLeft, ChevronRight, Briefcase, Clock } from 'lucide-react'

const weekDays = [
  { day: 'Sun', date: 5 },
  { day: 'Mon', date: 6 },
  { day: 'Tue', date: 7 },
  { day: 'Wed', date: 8 },
  { day: 'Thu', date: 9 },
  { day: 'Fri', date: 10 },
  { day: 'Sat', date: 11 },
]

const events = {
  hearings: [
    { title: 'Court Hearing — FIR #4489', time: '9:00 AM - 10:30 AM', type: 'hearing' },
    { title: 'Bail Review — Case #4512', time: '2:00 PM - 3:00 PM', type: 'hearing' },
  ],
  shifts: [
    { title: 'Shift Handover — Morning', time: '6:00 AM - 7:00 AM', type: 'shift' },
    { title: 'Night Patrol Briefing', time: '8:00 PM - 8:30 PM', type: 'shift' },
  ],
}

export default function InvestmentCalendar() {
  const [selectedDay, setSelectedDay] = useState(1) // Mon
  const [activeTab, setActiveTab] = useState('hearings')

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <h3 className="chart-card-title">Investigation Calendar</h3>
        <button className="chart-card-menu" aria-label="More options">⋯</button>
      </div>
      <div className="chart-card-body">
        {/* Week Navigation */}
        <div className="calendar-nav">
          <button className="calendar-nav-btn" aria-label="Previous week">
            <ChevronLeft size={16} />
          </button>
          <div className="calendar-days">
            {weekDays.map((d, i) => (
              <button
                key={i}
                className={`calendar-day ${i === selectedDay ? 'selected' : ''}`}
                onClick={() => setSelectedDay(i)}
              >
                <span className="calendar-day-name">{d.day}</span>
                <span className="calendar-day-date">{d.date}</span>
              </button>
            ))}
          </div>
          <button className="calendar-nav-btn" aria-label="Next week">
            <ChevronRight size={16} />
          </button>
        </div>

        {/* Tabs */}
        <div className="calendar-tabs">
          <button
            className={`calendar-tab ${activeTab === 'hearings' ? 'active' : ''}`}
            onClick={() => setActiveTab('hearings')}
          >
            <Briefcase size={14} />
            Hearings
          </button>
          <button
            className={`calendar-tab ${activeTab === 'shifts' ? 'active' : ''}`}
            onClick={() => setActiveTab('shifts')}
          >
            <Clock size={14} />
            Shifts
          </button>
        </div>

        {/* Events */}
        <div className="calendar-events">
          {events[activeTab].map((event, i) => (
            <div key={i} className="calendar-event">
              <div className="calendar-event-indicator" />
              <div className="calendar-event-content">
                <p className="calendar-event-title">{event.title}</p>
                <p className="calendar-event-time">{event.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
