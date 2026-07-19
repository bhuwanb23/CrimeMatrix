import { useState, useEffect } from 'react'
import { Search, Bookmark, ChevronDown, ChevronRight, RefreshCw } from 'lucide-react'

export default function CaseListPanel({ investigations, selectedId, onSelectCase, loading, onRefresh }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeSection, setActiveSection] = useState('active')

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
