import { useState, useMemo } from 'react'
import SearchBar from './search/SearchBar'
import FilterChips from './search/FilterChips'
import SearchResults from './search/SearchResults'
import SavedSearches from './search/SavedSearches'
import SearchHistory from './search/SearchHistory'

const allCases = [
  { id: 'FIR #4521', title: 'Theft at Malleshwaram residence', type: 'Theft', district: 'Bengaluru Urban', status: 'active', date: 'Jul 15, 2026' },
  { id: 'FIR #4519', title: 'Vehicle accident — Mysuru Road', type: 'Accident', district: 'Mysuru', status: 'pending', date: 'Jul 15, 2026' },
  { id: 'FIR #4515', title: 'Cyber fraud — Electronic City', type: 'Cybercrime', district: 'Bengaluru Urban', status: 'active', date: 'Jul 14, 2026' },
  { id: 'FIR #4512', title: 'Missing person — Koramangala', type: 'Missing', district: 'Bengaluru Urban', status: 'active', date: 'Jul 14, 2026' },
  { id: 'FIR #4508', title: 'Robbery attempt — Whitefield', type: 'Assault', district: 'Bengaluru Urban', status: 'closed', date: 'Jul 13, 2026' },
  { id: 'FIR #4501', title: 'Theft at commercial complex', type: 'Theft', district: 'Bengaluru Rural', status: 'pending', date: 'Jul 12, 2026' },
  { id: 'FIR #4498', title: 'Fraud — online payment scam', type: 'Fraud', district: 'Mangaluru', status: 'active', date: 'Jul 11, 2026' },
  { id: 'FIR #4495', title: 'Assault near bus stand', type: 'Assault', district: 'Hubballi', status: 'closed', date: 'Jul 10, 2026' },
  { id: 'FIR #4489', title: 'Robbery — Indiranagar', type: 'Theft', district: 'Bengaluru Urban', status: 'active', date: 'Jul 9, 2026' },
  { id: 'FIR #4485', title: 'Cybercrime — phishing attack', type: 'Cybercrime', district: 'Bengaluru Urban', status: 'pending', date: 'Jul 8, 2026' },
  { id: 'FIR #4480', title: 'Theft from parking lot', type: 'Theft', district: 'Mysuru', status: 'closed', date: 'Jul 7, 2026' },
  { id: 'FIR #4475', title: 'Fraud — insurance claim', type: 'Fraud', district: 'Bengaluru Rural', status: 'active', date: 'Jul 6, 2026' },
  { id: 'FIR #4470', title: 'Assault — domestic dispute', type: 'Assault', district: 'Mangaluru', status: 'pending', date: 'Jul 5, 2026' },
  { id: 'FIR #4465', title: 'Missing juvenile — Hebbal', type: 'Missing', district: 'Bengaluru Urban', status: 'active', date: 'Jul 4, 2026' },
  { id: 'FIR #4460', title: 'Cybercrime — data breach', type: 'Cybercrime', district: 'Hubballi', status: 'closed', date: 'Jul 3, 2026' },
]

const ITEMS_PER_PAGE = 8

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [activeFilters, setActiveFilters] = useState(['all'])
  const [page, setPage] = useState(1)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = (searchQuery) => {
    setQuery(searchQuery)
    setHasSearched(true)
    setPage(1)
  }

  const handleToggleFilter = (filterId) => {
    if (filterId === 'all') {
      setActiveFilters(['all'])
    } else {
      setActiveFilters((prev) => {
        const next = prev.filter((f) => f !== 'all' && f !== filterId)
        if (!prev.includes(filterId)) {
          next.push(filterId)
        }
        return next.length === 0 ? ['all'] : next
      })
    }
    setPage(1)
  }

  const handleClearFilters = () => {
    setActiveFilters(['all'])
    setPage(1)
  }

  const filteredResults = useMemo(() => {
    let results = allCases

    if (query) {
      const q = query.toLowerCase()
      results = results.filter(
        (c) =>
          c.id.toLowerCase().includes(q) ||
          c.title.toLowerCase().includes(q) ||
          c.type.toLowerCase().includes(q) ||
          c.district.toLowerCase().includes(q)
      )
    }

    if (!activeFilters.includes('all')) {
      results = results.filter((c) => {
        const typeMatch = activeFilters.some(
          (f) => c.type.toLowerCase() === f
        )
        const districtMatch = activeFilters.some(
          (f) => c.district.toLowerCase().includes(f)
        )
        const statusMatch = activeFilters.some(
          (f) => c.status === f
        )
        const firMatch = activeFilters.includes('fir')
        return typeMatch || districtMatch || statusMatch || firMatch
      })
    }

    return results
  }, [query, activeFilters])

  const totalPages = Math.ceil(filteredResults.length / ITEMS_PER_PAGE)
  const paginatedResults = filteredResults.slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  )

  return (
    <div className="search-page">
      <div className="search-main">
        <div className="search-header">
          <h1 className="search-title">Crime Search</h1>
          <p className="search-subtitle">Search everything from one place</p>
        </div>

        <SearchBar
          value={query}
          onChange={setQuery}
          onSearch={handleSearch}
        />

        <FilterChips
          activeFilters={activeFilters}
          onToggleFilter={handleToggleFilter}
          onClearAll={handleClearFilters}
        />

        <SearchResults
          results={paginatedResults}
          page={page}
          totalPages={totalPages}
          onPageChange={setPage}
        />
      </div>

      <aside className="search-sidebar">
        <SavedSearches onRunSearch={handleSearch} />
        <SearchHistory onRunSearch={handleSearch} />
      </aside>
    </div>
  )
}
