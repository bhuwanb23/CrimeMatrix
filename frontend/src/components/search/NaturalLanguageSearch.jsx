import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Sparkles, Loader2, FileText, User } from 'lucide-react'
import { naturalLanguageSearch } from '../../services/recommendations'
import { useLanguage } from '../../context/LanguageContext'


export default function NaturalLanguageSearch() {
  const { t } = useLanguage()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const navigate = useNavigate()

  async function handleSearch() {
    if (!query.trim() || loading) return
    setLoading(true)
    setShowResults(true)
    try {
      const res = await naturalLanguageSearch(query.trim())
      const data = res?.data || res
      setResults(data?.results || [])
    } catch (e) {
      console.error('Search failed', e)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  function handleClick(result) {
    if (result.type === 'case') navigate(`/cases/${result.id}`)
    else if (result.type === 'suspect') navigate(`/suspects/${result.id}`)
    setShowResults(false)
  }

  return (
    <div className="nl-search">
      <div className="nl-search-bar">
        <div className="nl-search-icon">
          <Sparkles size={14} />
        </div>
        <input
          className="nl-search-input"
          placeholder={t(\'Search naturally — e.g. "thefts in Bengaluru last month"\')}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button className="nl-search-btn" onClick={handleSearch} disabled={loading || !query.trim()}>
          {loading ? <Loader2 size={14} className="similar-spinning" /> : <Search size={14} />}
        </button>
      </div>

      {showResults && (
        <div className="nl-results">
          {loading ? (
            <div className="similar-loading">
              <div className="similar-spinner" />
              <span>{t('Searching...')}</span>
            </div>
          ) : results.length === 0 ? (
            <div className="similar-empty">
              <p>No results found for "{query}"</p>
            </div>
          ) : (
            <div className="nl-results-list">
              <span className="nl-results-count">{results.length} results</span>
              {results.map((r, i) => (
                <div key={i} className="nl-result-card" onClick={() => handleClick(r)}>
                  <div className="nl-result-icon">
                    {r.type === 'case' ? <FileText size={14} /> : <User size={14} />}
                  </div>
                  <div className="nl-result-info">
                    <span className="nl-result-type">{r.type === 'case' ? 'Case' : 'Suspect'}</span>
                    <span className="nl-result-title">
                      {r.title || r.name || `#${r.id}`}
                    </span>
                    <span className="nl-result-meta">
                      {r.crime_type && `${r.crime_type} • `}
                      {r.district}
                      {r.relevance && ` • ${r.relevance}% match`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
          <button className="nl-results-close" onClick={() => setShowResults(false)}>
            Close
          </button>
        </div>
      )}
    </div>
  )
}
