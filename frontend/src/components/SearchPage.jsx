import { useState, useMemo, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchBar from './search/SearchBar'
import FilterChips from './search/FilterChips'
import SearchResults from './search/SearchResults'
import SavedSearches from './search/SavedSearches'
import SearchHistory from './search/SearchHistory'
import { cases } from './search/caseData'

const ITEMS_PER_PAGE = 8

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function SearchPage() {
  const { lang } = useLanguage()
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [activeFilters, setActiveFilters] = useState(['all'])
  const [page, setPage] = useState(1)
  const [savedSearches, setSavedSearches] = useState([
    { id: 1, query: 'Theft cases Bengaluru 2026', count: 24 },
    { id: 2, query: 'Unsolved fraud cases', count: 12 },
    { id: 3, query: 'Repeat offenders Koramangala', count: 8 },
    { id: 4, query: 'Cybercrime victims under 25', count: 15 },
  ])
  const [searchHistory, setSearchHistory] = useState([
    { id: 1, query: 'FIR #4521 theft', time: '2 min ago' },
    { id: 2, query: 'Ravi Kumar suspect network', time: '15 min ago' },
    { id: 3, query: 'Active cases Mysuru', time: '1 hr ago' },
    { id: 4, query: 'Cyber fraud patterns', time: '2 hrs ago' },
    { id: 5, query: 'Missing person Koramangala', time: 'Yesterday' },
    { id: 6, query: 'Vehicle KA-01-AB-1234', time: 'Yesterday' },
  ])
  const [nextId, setNextId] = useState(100)

  const handleSearch = useCallback((searchQuery) => {
    setQuery(searchQuery)
    setPage(1)
    if (searchQuery.trim()) {
      setSearchHistory((prev) => {
        const newEntry = {
          id: nextId,
          query: searchQuery,
          time: 'Just now',
        }
        return [newEntry, ...prev.slice(0, 9)]
      })
      setNextId((prev) => prev + 1)
    }
  }, [nextId])

  const handleToggleFilter = useCallback((filterId) => {
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
  }, [])

  const handleClearFilters = useCallback(() => {
    setActiveFilters(['all'])
    setPage(1)
  }, [])

  const handleViewCase = useCallback((caseId) => {
    navigate(`/cases/${caseId}`)
  }, [navigate])

  const handleSaveSearch = useCallback((searchQuery) => {
    if (!searchQuery.trim()) return
    setSavedSearches((prev) => {
      const exists = prev.some((s) => s.query === searchQuery)
      if (exists) return prev
      return [
        { id: nextId, query: searchQuery, count: 0 },
        ...prev,
      ]
    })
    setNextId((prev) => prev + 1)
  }, [nextId])

  const handleDeleteSaved = useCallback((id) => {
    setSavedSearches((prev) => prev.filter((s) => s.id !== id))
  }, [])

  const filteredResults = useMemo(() => {
    let results = cases

    if (query) {
      const q = query.toLowerCase()
      results = results.filter(
        (c) =>
          c.id.toLowerCase().includes(q) ||
          c.title.toLowerCase().includes(q) ||
          c.type.toLowerCase().includes(q) ||
          c.district.toLowerCase().includes(q) ||
          c.description.toLowerCase().includes(q)
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
          <h1 className="search-title">{t('crime_search', lang)}</h1>
          <p className="search-subtitle">{t('search_everything', lang)}</p>
        </div>

        <SearchBar
          value={query}
          onChange={setQuery}
          onSearch={handleSearch}
          onSave={handleSaveSearch}
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
          onViewCase={handleViewCase}
        />
      </div>

      <aside className="search-sidebar">
        <SavedSearches
          searches={savedSearches}
          onRunSearch={handleSearch}
          onDelete={handleDeleteSaved}
          onSave={handleSaveSearch}
          currentQuery={query}
        />
        <SearchHistory
          history={searchHistory}
          onRunSearch={handleSearch}
        />
      </aside>
    </div>
  )
}
