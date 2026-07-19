import { useState, useEffect } from 'react'
import { Search, Bookmark, ChevronDown, ChevronRight, RefreshCw, Plus, Clock } from 'lucide-react'
import { getRecentInvestigations } from '../../services/investigations'

export default function CaseListPanel({ investigations, selectedId, onSelectCase, loading, onRefresh, onCreated }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeSection, setActiveSection] = useState('active')
  const [recentItems, setRecentItems] = useState([])
  const [showCreate, setShowCreate] = useState(false)

  useEffect(() => {
    loadRecent()
  }, [investigations])

  async function loadRecent() {
    try {
      const res = await getRecentInvestigations(3)
      const data = res?.data || res
      setRecentItems(data?.items || [])
    } catch (e) {
      setRecentItems([])
    }
  }

  const filtered = investigations.filter((inv) => {
    const matchesSearch = (inv.case_id?.toString() || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (inv.title || '').toLowerCase().includes(searchQuery.toLowerCase())
    const matchesSection = activeSection === 'active'
      ? inv.status === 'active'
      : inv.status === 'saved'
    return matchesSearch && matchesSection
  })

  const activeCount = investigations.filter((i) => i.status === 'active').length
  const savedCount = investigations.filter((i) => i.status === 'saved').length

  function formatRelativeTime(dateStr) {
    if (!dateStr) return ''
    try {
      const d = new Date(dateStr)
      const now = new Date()
      const diff = Math.floor((now - d) / 1000)
      if (diff < 60) return 'Just now'
      if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
      if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
      return `${Math.floor(diff / 86400)}d ago`
    } catch {
      return ''
    }
  }

  return (
    <div className="case-list-panel">
      <div className="case-list-search">
        <Search size={14} />
        <input
          type="text"
          placeholder="Search investigations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {onRefresh && (
          <button className="case-list-refresh" onClick={onRefresh} disabled={loading}>
            <RefreshCw size={12} className={loading ? 'similar-spinning' : ''} />
          </button>
        )}
      </div>

      <button className="case-list-create-btn" onClick={() => setShowCreate(!showCreate)}>
        <Plus size={14} />
        New Investigation
      </button>

      {showCreate && (
        <CreateInvestigationInline
          onCreated={(inv) => {
            setShowCreate(false)
            onCreated?.(inv)
          }}
          onCancel={() => setShowCreate(false)}
        />
      )}

      {/* Recently Viewed */}
      {recentItems.length > 0 && !searchQuery && (
        <div className="case-list-section">
          <div className="case-list-section-header">
            <Clock size={12} />
            <span>Recently Viewed</span>
          </div>
          <div className="case-list-recent">
            {recentItems.map((inv) => (
              <button
                key={inv.id}
                className={`case-list-item case-list-item-recent ${selectedId === inv.id ? 'selected' : ''}`}
                onClick={() => onSelectCase(inv.id)}
              >
                <div className="case-list-item-top">
                  <span className="case-list-item-id">INV-{String(inv.id).padStart(3, '0')}</span>
                  <span className="case-list-item-time">{formatRelativeTime(inv.last_accessed)}</span>
                </div>
                <p className="case-list-item-title">{inv.title}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="case-list-sections">
        <button
          className={`case-list-section-btn ${activeSection === 'active' ? 'active' : ''}`}
          onClick={() => setActiveSection('active')}
        >
          {activeSection === 'active' ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          Active ({activeCount})
        </button>
        <button
          className={`case-list-section-btn ${activeSection === 'saved' ? 'active' : ''}`}
          onClick={() => setActiveSection('saved')}
        >
          {activeSection === 'saved' ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <Bookmark size={12} />
          Saved ({savedCount})
        </button>
      </div>

      <div className="case-list-items">
        {loading ? (
          <div className="similar-loading">
            <div className="similar-spinner" />
            <span>Loading...</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="similar-empty">
            <p>No investigations found</p>
          </div>
        ) : (
          filtered.map((inv) => (
            <button
              key={inv.id}
              className={`case-list-item ${selectedId === inv.id ? 'selected' : ''}`}
              onClick={() => onSelectCase(inv.id)}
            >
              <div className="case-list-item-top">
                <span className="case-list-item-id">INV-{String(inv.id).padStart(3, '0')}</span>
                <span className={`case-list-priority priority-${(inv.priority || 'medium').toLowerCase()}`}>
                  {inv.priority}
                </span>
              </div>
              <p className="case-list-item-title">{inv.title}</p>
              <div className="case-list-item-progress">
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${inv.progress || 0}%` }} />
                </div>
                <span className="progress-text">{inv.progress || 0}%</span>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}

function CreateInvestigationInline({ onCreated, onCancel }) {
  const [form, setForm] = useState({ title: '', priority: 'medium', district: 'Bengaluru Urban', status: 'active' })
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async () => {
    if (!form.title.trim() || submitting) return
    setSubmitting(true)
    try {
      const { createInvestigation } = await import('../../services/investigations')
      const res = await createInvestigation({
        case_id: Date.now(),
        title: form.title.trim(),
        priority: form.priority,
        district: form.district,
        status: form.status,
        progress: 0,
      })
      onCreated?.(res?.data || res)
    } catch (e) {
      console.error('Failed to create investigation', e)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="case-create-form">
      <input
        className="case-create-input"
        placeholder="Investigation title..."
        value={form.title}
        onChange={(e) => setForm({ ...form, title: e.target.value })}
        autoFocus
      />
      <div className="case-create-row">
        <select className="case-create-select" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
          <option value="high">High Priority</option>
          <option value="medium">Medium Priority</option>
          <option value="low">Low Priority</option>
        </select>
        <select className="case-create-select" value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })}>
          <option value="Bengaluru Urban">Bengaluru Urban</option>
          <option value="Bengaluru Rural">Bengaluru Rural</option>
          <option value="Mysuru">Mysuru</option>
          <option value="Mangaluru">Mangaluru</option>
          <option value="Hubballi">Hubballi</option>
        </select>
      </div>
      <div className="case-create-actions">
        <button className="similar-btn similar-btn-primary" onClick={handleSubmit} disabled={submitting || !form.title.trim()}>
          {submitting ? 'Creating...' : 'Create'}
        </button>
        <button className="similar-btn similar-btn-secondary" onClick={onCancel}>Cancel</button>
      </div>
    </div>
  )
}
