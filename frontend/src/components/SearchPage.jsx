import { useState, useCallback, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchBar from './search/SearchBar'
import FilterChips from './search/FilterChips'
import SearchResults from './search/SearchResults'
import { searchCrimes, listAllCrimes, semanticSearch, crossDistrictSearch, listDistricts } from '../services/search'

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
  const [selectedDistricts, setSelectedDistricts] = useState([])
  const [showDistrictPicker, setShowDistrictPicker] = useState(false)
  const [districts, setDistricts] = useState([])

  const loadDistricts = useCallback(async () => {
    try {
      const result = await listDistricts()
      setDistricts(result.data || [])
    } catch {
    }
  }, [])

  const loadAllCrimes = useCallback(async () => {
    setIsLoading(true)
    try {
      const result = await listAllCrimes(1, 50)
      const data = result.data || {}
      setResults(data.items || data.results || [])
      setTotalResults(data.total || 0)
    } catch {
    }
    setIsLoading(false)
  }, [])

  useEffect(() => {
    loadAllCrimes()
    loadDistricts()
  }, [loadAllCrimes, loadDistricts])

  const handleSearch = useCallback(async (searchQuery) => {
    setQuery(searchQuery)
    setPage(1)
    if (!searchQuery.trim()) { loadAllCrimes(); return }
    setIsLoading(true)
    try {
      if (selectedDistricts.length > 0) {
        const result = await crossDistrictSearch(searchQuery, selectedDistricts, 30)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || 0)
      } else if (semanticMode) {
        const result = await semanticSearch(searchQuery, 20)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || data.count || 0)
      } else {
        const result = await searchCrimes(searchQuery, {}, 1, 20)
        const data = result.data || {}
        setResults(data.results || [])
        setTotalResults(data.total || 0)
      }
    } catch {
      setResults([])
      setTotalResults(0)
    }
    setIsLoading(false)
  }, [selectedDistricts, semanticMode, loadAllCrimes])

  const handleToggleDistrict = useCallback((district) => {
    setSelectedDistricts(prev => {
      if (prev.includes(district)) return prev.filter(d => d !== district)
      return [...prev, district]
    })
  }, [])

  const handleToggleFilter = useCallback((filterId) => {
    if (filterId === 'all') { setActiveFilters(['all']); return }
    setActiveFilters(prev => {
      const next = prev.filter(f => f !== 'all' && f !== filterId)
      if (!prev.includes(filterId)) next.push(filterId)
      return next.length === 0 ? ['all'] : next
    })
    setPage(1)
  }, [])

  const handleViewCase = useCallback((caseId) => { navigate(`/cases/${caseId}`) }, [navigate])

  const totalPages = Math.ceil(totalResults / ITEMS_PER_PAGE)

  return (
    <div className="flex flex-col h-full p-6">
      <div className="max-w-6xl mx-auto w-full">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Crime Search</h1>
          <p className="text-sm text-gray-500">Search across Karnataka — statewide intelligence</p>
        </div>

        <SearchBar value={query} onChange={setQuery} onSearch={handleSearch} />

        {/* Controls Row */}
        <div className="flex items-center gap-3 mt-3 mb-4 flex-wrap">
          <button onClick={() => setSemanticMode(!semanticMode)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${semanticMode ? 'bg-purple-100 text-purple-700 border border-purple-300' : 'bg-gray-100 text-gray-500 border border-gray-200 hover:bg-gray-200'}`}>
            {semanticMode ? '🧠 Semantic ON' : '🧠 Semantic'}
          </button>

          <button onClick={() => setShowDistrictPicker(!showDistrictPicker)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${selectedDistricts.length > 0 ? 'bg-blue-100 text-blue-700 border border-blue-300' : 'bg-gray-100 text-gray-500 border border-gray-200 hover:bg-gray-200'}`}>
            🗺️ {selectedDistricts.length > 0 ? `${selectedDistricts.length} Districts` : 'Districts'}
          </button>

          {selectedDistricts.length > 0 && (
            <div className="flex items-center gap-1">
              {selectedDistricts.map(d => (
                <span key={d} onClick={() => handleToggleDistrict(d)}
                  className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 text-xs cursor-pointer hover:bg-blue-100">
                  {d} ×
                </span>
              ))}
            </div>
          )}
        </div>

        {/* District Picker */}
        {showDistrictPicker && (
          <div className="mb-4 p-3 bg-white border border-gray-200 rounded-xl shadow-sm">
            <p className="text-xs text-gray-500 mb-2">Select districts for cross-district search:</p>
            <div className="flex flex-wrap gap-2">
              {districts.map(d => (
                <button key={d.id} onClick={() => handleToggleDistrict(d.name)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selectedDistricts.includes(d.name) ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}>
                  {d.name}
                </button>
              ))}
            </div>
            {selectedDistricts.length > 0 && (
              <button onClick={() => setSelectedDistricts([])} className="mt-2 text-xs text-red-500 hover:text-red-700">Clear all</button>
            )}
          </div>
        )}

        <FilterChips activeFilters={activeFilters} onToggleFilter={handleToggleFilter} />

        <div className="mt-4">
          <SearchResults results={results} page={page} totalPages={totalPages}
            onPageChange={setPage} onViewCase={handleViewCase} isLoading={isLoading} totalResults={totalResults} />
        </div>
      </div>
    </div>
  )
}
