import { useState, useMemo } from 'react'
import { Search } from 'lucide-react'
import SuspectCard from './suspects/SuspectCard'
import { suspects } from './suspects/suspectsData'

const filters = [
  { id: 'all', label: 'All' },
  { id: 'high-risk', label: 'High Risk' },
  { id: 'repeat', label: 'Repeat Offenders' },
  { id: 'at-large', label: 'At Large' },
  { id: 'under-trial', label: 'Under Trial' },
]

export default function SuspectsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeFilter, setActiveFilter] = useState('all')

  const filtered = useMemo(() => {
    let results = suspects

    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      results = results.filter(
        (s) =>
          s.name.toLowerCase().includes(q) ||
          s.id.toLowerCase().includes(q) ||
          s.district.toLowerCase().includes(q) ||
          s.aliases.some((a) => a.toLowerCase().includes(q))
      )
    }

    if (activeFilter !== 'all') {
      results = results.filter((s) => {
        switch (activeFilter) {
          case 'high-risk': return s.riskScore >= 70
          case 'repeat': return s.cases >= 3
          case 'at-large': return s.status === 'At Large'
          case 'under-trial': return s.status === 'Under Trial' || s.status === 'Under Investigation'
          default: return true
        }
      })
    }

    return results
  }, [searchQuery, activeFilter])

  return (
    <div className="suspects-page">
      <div className="suspects-header">
        <div className="suspects-header-top">
          <h1 className="suspects-title">Criminal Intelligence</h1>
          <p className="suspects-subtitle">Everything about suspects</p>
        </div>
        <div className="suspects-search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search suspects by name, ID, alias..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="suspects-filters">
        {filters.map((filter) => (
          <button
            key={filter.id}
            className={`suspects-filter-btn ${activeFilter === filter.id ? 'active' : ''}`}
            onClick={() => setActiveFilter(filter.id)}
          >
            {filter.label}
          </button>
        ))}
        <span className="suspects-count">{filtered.length} suspects</span>
      </div>

      <div className="suspects-grid">
        {filtered.map((suspect) => (
          <SuspectCard key={suspect.id} suspect={suspect} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="suspects-empty">
          <p>No suspects found matching your criteria</p>
        </div>
      )}
    </div>
  )
}
