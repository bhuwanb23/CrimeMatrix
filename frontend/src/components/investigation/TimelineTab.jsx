import { useState } from 'react'
import { FileText, Shield, Camera, AlertTriangle, Plus, Trash2 } from 'lucide-react'
import { createTimelineEvent, deleteTimelineEvent } from '../../services/investigations'

const typeIcons = {
  filing: FileText,
  investigation: Shield,
  evidence: Camera,
  suspect: AlertTriangle,
}

const typeColors = {
  filing: '#3b82f6',
  investigation: '#8b5cf6',
  evidence: '#f59e0b',
  suspect: '#ef4444',
}

export default function TimelineTab({ investigationId, timeline }) {
  const [events, setEvents] = useState(timeline)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', description: '', event_type: 'investigation', event_date: '' })
  const [submitting, setSubmitting] = useState(false)

  const handleAdd = async () => {
    if (!form.title.trim() || submitting) return
    setSubmitting(true)
    try {
      const res = await createTimelineEvent({
        investigation_id: investigationId,
        title: form.title.trim(),
        description: form.description.trim() || null,
        event_type: form.event_type,
        event_date: form.event_date || null,
      })
      const created = res?.data || res
      setEvents([{ ...created, event_type: form.event_type }, ...events])
      setForm({ title: '', description: '', event_type: 'investigation', event_date: '' })
      setShowForm(false)
    } catch (e) {
      console.error('Failed to create event', e)
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (eventId) => {
    try {
      await deleteTimelineEvent(eventId)
      setEvents(events.filter(e => e.id !== eventId))
    } catch (e) {
      console.error('Failed to delete event', e)
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return ''
    try {
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
    } catch {
      return dateStr
    }
  }

  return (
    <div className="timeline-tab">
      <div className="timeline-visual">
        {events.length === 0 ? (
          <div className="similar-empty"><p>No timeline events yet</p></div>
        ) : (
          events.map((item, i) => {
            const Icon = typeIcons[item.event_type] || typeIcons[item.type] || FileText
            const color = typeColors[item.event_type] || typeColors[item.type] || '#64748b'
            return (
              <div key={item.id || i} className="timeline-visual-item">
                <div className="timeline-visual-dot" style={{ background: color }}>
                  <Icon size={12} color="white" />
                </div>
                <div className="timeline-visual-line" style={{ background: color + '30' }} />
                <div className="timeline-visual-content">
                  <div className="timeline-visual-header">
                    <span className="timeline-visual-date">{formatDate(item.event_date || item.created_at)}</span>
                    <button className="note-delete" onClick={() => handleDelete(item.id)}>
                      <Trash2 size={12} />
                    </button>
                  </div>
                  <p className="timeline-visual-event">{item.title || item.event}</p>
                  {item.description && <p className="timeline-visual-desc">{item.description}</p>}
                </div>
              </div>
            )
          })
        )}
      </div>

      {showForm ? (
        <div className="timeline-form">
          <input
            className="timeline-form-input"
            placeholder="Event title"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
          <textarea
            className="timeline-form-input"
            placeholder="Description (optional)"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            rows={2}
          />
          <div className="timeline-form-row">
            <select
              className="timeline-form-select"
              value={form.event_type}
              onChange={(e) => setForm({ ...form, event_type: e.target.value })}
            >
              <option value="filing">Filing</option>
              <option value="investigation">Investigation</option>
              <option value="evidence">Evidence</option>
              <option value="suspect">Suspect</option>
            </select>
            <input
              className="timeline-form-input"
              type="date"
              value={form.event_date}
              onChange={(e) => setForm({ ...form, event_date: e.target.value })}
            />
          </div>
          <div className="timeline-form-actions">
            <button className="similar-btn similar-btn-primary" onClick={handleAdd} disabled={submitting || !form.title.trim()}>
              {submitting ? 'Adding...' : 'Add Event'}
            </button>
            <button className="similar-btn similar-btn-secondary" onClick={() => setShowForm(false)}>
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <button className="timeline-add-btn" onClick={() => setShowForm(true)}>
          <Plus size={14} />
          Add Event
        </button>
      )}
    </div>
  )
}
