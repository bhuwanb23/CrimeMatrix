import { useState, useMemo, useCallback, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchBar from './search/SearchBar'
import FilterChips from './search/FilterChips'
import SearchResults from './search/SearchResults'
import SavedSearches from './search/SavedSearches'
import SearchHistory from './search/SearchHistory'
import { searchCrimes, getSuggestions, getFacets, listSavedSearches, saveSearch, deleteSavedSearch, listSearchHistory, recordSearch, semanticSearch } from '../services/search'

const ITEMS_PER_PAGE = 8

export default function SearchPage() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [activeFilters, setActiveFilters] = useState(['all'])
  const [page, setPage] = useState(1)
  const [results, setResults] = useState([])
  const [totalResults, setTotalResults] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [savedSearches, setSavedSearches] = useState([])
  const [searchHistory, setSearchHistory] = useState([])
  const [suggestions, setSuggestions] = useState([])
  const [semanticMode, setSemanticMode] = useState(false)

  // Load saved searches and history on mount
  useEffect(() => {
    loadSavedSearches()
    loadSearchHistory()
  }, [])

  const loadSavedSearches = async () => {
    try {
      const result = await listSavedSearches()
      setSavedSearches(result.data || [])
    } catch (e) {}
  }

  const loadSearchHistory = async () => {
    try {
      const result = await listSearchHistory()
      setSearchHistory(result.data || [])
    } catch (e) {}
  }

  const handleSearch = useCallback(async (searchQuery) => {
    setQuery(searchQuery)
    setPage(1)
    if (!searchQuery.trim()) {
      setResults([])
      setTotalResults(0)
      return
    }

    setIsLoading(true)
    try {
      let result
      if (semanticMode) {
        result = await semanticSearch(searchQuery, 20)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || data.count || 0)
      } else {
        const filters = activeFilters.includes('all') ? {} : { entity: activeFilters[0] }
        result = await searchCrimes(searchQuery, filters, 1, ITEMS_PER_PAGE)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || 0)
      }

      // Record search in history
      await recordSearch(searchQuery, data.total || 0)
      loadSearchHistory()
    } catch (e) {
      console.error('Search error:', e)
      setResults([])
      setTotalResults(0)
    }
    setIsLoading(false)
  }, [activeFilters, semanticMode])

  const handleToggleFilter = useCallback((filterId) => {
    if (filterId === 'all') {
      setActiveFilters(['all'])
    } else {
      setActiveFilters((prev) => {
        const next = prev.filter((f) => f !== 'all' && f !== filterId)
        if (!prev.includes(filterId)) next.push(filterId)
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

  const handleSaveSearch = useCallback(async (searchQuery) => {
    if (!searchQuery.trim()) return
    try {
      await saveSearch(searchQuery, searchQuery)
      loadSavedSearches()
    } catch (e) {}
  }, [])

  const handleDeleteSaved = useCallback(async (id) => {
    try {
      await deleteSavedSearch(id)
      loadSavedSearches()
    } catch (e) {}
  }, [])

  const handleRunSaved = useCallback((searchQuery) => {
    setQuery(searchQuery)
    handleSearch(searchQuery)
  }, [handleSearch])

  const totalPages = Math.ceil(totalResults / ITEMS_PER_PAGE)

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
          onSave={handleSaveSearch}
          suggestions={suggestions}
        />

        {/* Semantic Search Toggle */}
        <div className="flex items-center gap-2 mb-3">
          <button
            onClick={() => setSemanticMode(!semanticMode)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              semanticMode ? 'bg-purple-100 text-purple-700 border border-purple-300' : 'bg-gray-100 text-gray-500 border border-gray-200 hover:bg-gray-200'
            }`}
          >
            {semanticMode ? '🧠 Semantic Search ON' : '🧠 Semantic Search'}
          </button>
          {semanticMode && <span className="text-xs text-purple-500">Search by meaning, not keywords</span>}
        </div>

        <FilterChips
          activeFilters={activeFilters}
          onToggleFilter={handleToggleFilter}
          onClearAll={handleClearFilters}
        />

        <SearchResults
          results={results}
          page={page}
          totalPages={totalPages}
          onPageChange={setPage}
          onViewCase={handleViewCase}
          isLoading={isLoading}
          totalResults={totalResults}
        />
      </div>

      <aside className="search-sidebar">
        <SavedSearches
          searches={savedSearches}
          onRunSearch={handleRunSaved}
          onDelete={handleDeleteSaved}
          onSave={handleSaveSearch}
          currentQuery={query}
        />
        <SearchHistory
          history={searchHistory}
          onRunSearch={handleRunSaved}
        />
      </aside>
    </div>
  )
}
