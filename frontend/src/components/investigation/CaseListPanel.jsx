import { useState } from 'react'
import { Search, Bookmark, ChevronDown, ChevronRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText, translateStatus } from '../../utils/translate'

export default function CaseListPanel({ investigations, selectedId, onSelectCase }) {
  const { lang } = useLanguage()
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
          placeholder={t('search_investigations_placeholder', lang)}
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
          {t('active', lang)} ({investigations.filter((i) => i.status === 'active').length})
        </button>
        <button
          className={`case-list-section-btn ${activeSection === 'saved' ? 'active' : ''}`}
          onClick={() => setActiveSection('saved')}
        >
          {activeSection === 'saved' ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <Bookmark size={12} />
          {t('saved', lang)} ({investigations.filter((i) => i.bookmarked).length})
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
                {t(inv.priority.toLowerCase(), lang)}
              </span>
            </div>
            <p className="case-list-item-title">{translateText(inv.title, lang)}</p>
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
