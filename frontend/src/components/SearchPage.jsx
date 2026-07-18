import { useState, useCallback, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchBar from './search/SearchBar'
import FilterChips from './search/FilterChips'
import SearchResults from './search/SearchResults'
import { searchCrimes, listAllCrimes, semanticSearch } from '../services/search'

const ITEMS_PER_PAGE = 8

export default function SearchPage() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [activeFilters, setActiveFilters] = useState(['all'])
  const [page, setPage] = useState(1)
  const [results, setResults] = useState([])
  const [totalResults, setTotalResults] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [semanticMode, setSemanticMode] = useState(false)

  useEffect(() => {
    loadAllCrimes()
  }, [])

  const loadAllCrimes = async () => {
    setIsLoading(true)
    try {
      const result = await listAllCrimes(1, 50)
      const data = result.data || {}
      setResults(data.items || data.results || [])
      setTotalResults(data.total || 0)
    } catch (e) {
      console.error('Load error:', e)
    }
    setIsLoading(false)
  }

  const handleSearch = useCallback(async (searchQuery) => {
    setQuery(searchQuery)
    setPage(1)
    if (!searchQuery.trim()) {
      loadAllCrimes()
      return
    }
    setIsLoading(true)
    try {
      if (semanticMode) {
        const result = await semanticSearch(searchQuery, 20)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || data.count || 0)
      } else {
        const filters = activeFilters.includes('all') ? {} : { entity: activeFilters[0] }
        const result = await searchCrimes(searchQuery, filters, 1, 20)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || 0)
      }
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

  const totalPages = Math.ceil(totalResults / ITEMS_PER_PAGE)

  return (
    <div className="flex flex-col h-full p-6">
      <div className="max-w-6xl mx-auto w-full">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Crime Search</h1>
          <p className="text-sm text-gray-500">Search everything from one place</p>
        </div>

        <SearchBar
          value={query}
          onChange={setQuery}
          onSearch={handleSearch}
        />

        <div className="flex items-center gap-2 mt-3 mb-4">
          <button
            onClick={() => setSemanticMode(!semanticMode)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              semanticMode ? 'bg-purple-100 text-purple-700 border border-purple-300' : 'bg-gray-100 text-gray-500 border border-gray-200 hover:bg-gray-200'
            }`}
          >
            {semanticMode ? '🧠 Semantic ON' : '🧠 Semantic'}
          </button>
          {semanticMode && <span className="text-xs text-purple-500">Search by meaning, not keywords</span>}
        </div>

        <FilterChips
          activeFilters={activeFilters}
          onToggleFilter={handleToggleFilter}
          onClearAll={handleClearFilters}
        />

        <div className="mt-4">
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
      </div>
    </div>
  )
}
