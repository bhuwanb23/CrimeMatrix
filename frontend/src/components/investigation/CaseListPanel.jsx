import { useState } from 'react'
import { Search, Bookmark, ChevronDown, ChevronRight } from 'lucide-react'

export default function CaseListPanel({ investigations, selectedId, onSelectCase }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeSection, setActiveSection] = useState('active')

  const filtered = investigations.filter((inv) => {
    const matchesSearch = inv.caseId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      inv.title.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesSection = activeSection === 'active'
      ? inv.status === 'active'
      : inv.bookmarked
    return matchesSearch && matchesSection
  })

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
      </div>

      <div className="case-list-sections">
        <button
          className={`case-list-section-btn ${activeSection === 'active' ? 'active' : ''}`}
          onClick={() => setActiveSection('active')}
        >
          {activeSection === 'active' ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          Active ({investigations.filter((i) => i.status === 'active').length})
        </button>
        <button
          className={`case-list-section-btn ${activeSection === 'saved' ? 'active' : ''}`}
          onClick={() => setActiveSection('saved')}
        >
          {activeSection === 'saved' ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <Bookmark size={12} />
          Saved ({investigations.filter((i) => i.bookmarked).length})
        </button>
      </div>

      <div className="case-list-items">
        {filtered.map((inv) => (
          <button
            key={inv.id}
            className={`case-list-item ${selectedId === inv.id ? 'selected' : ''}`}
            onClick={() => onSelectCase(inv.id)}
          >
            <div className="case-list-item-top">
              <span className="case-list-item-id">{inv.caseId}</span>
              <span className={`case-list-priority priority-${inv.priority.toLowerCase()}`}>
                {inv.priority}
              </span>
            </div>
            <p className="case-list-item-title">{inv.title}</p>
            <div className="case-list-item-progress">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${inv.progress}%` }} />
              </div>
              <span className="progress-text">{inv.progress}%</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
