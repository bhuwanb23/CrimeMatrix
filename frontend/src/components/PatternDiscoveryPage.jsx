import { useState, useEffect, useCallback } from 'react'
import { GitBranch, RefreshCw, Layers, Search } from 'lucide-react'
import { detectPatterns, listPatterns, getPatternStats } from '../services/patterns'
import PatternCard from './patterns/PatternCard'
import PatternExplorer from './patterns/PatternExplorer'
import { useLanguage } from '../context/LanguageContext'

const typeFilters = [
  { value: '', label: 'All Types' },
  { value: 'time', label: 'Time' },
  { value: 'mo', label: 'MO' },
  { value: 'location', label: 'Location' },
  { value: 'type', label: 'Crime Type' },
]

export default function PatternDiscoveryPage() {
  const { t } = useLanguage()
  const [patterns, setPatterns] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detecting, setDetecting] = useState(false)
  const [typeFilter, setTypeFilter] = useState('')
  const [selectedPattern, setSelectedPattern] = useState(null)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [patternsRes, statsRes] = await Promise.all([
        listPatterns(typeFilter ? { pattern_type: typeFilter } : {}),
        getPatternStats(),
      ])
      const pData = patternsRes?.data || patternsRes
      const sData = statsRes?.data || statsRes
      setPatterns(pData?.items || [])
      setStats(sData || {})
    } catch (e) {
      console.error('Failed to load patterns', e)
    } finally {
      setLoading(false)
    }
  }, [typeFilter])

  useEffect(() => {
    loadData()
  }, [loadData])

  async function handleDetect() {
    setDetecting(true)
    try {
      await detectPatterns()
      await loadData()
    } catch (e) {
      console.error('Detection failed', e)
    } finally {
      setDetecting(false)
    }
  }

  return (
    <div className="pattern-page">
      <div className="pattern-header">
        <div className="pattern-header-left">
          <GitBranch size={22} />
          <div>
            <h1>{t('Crime Pattern Discovery')}</h1>
            <p>{t('Automatically identify recurring crime patterns')}</p>
          </div>
        </div>
        <button className="intel-refresh" onClick={handleDetect} disabled={detecting}>
          {detecting ? <RefreshCw size={14} className="similar-spinning" /> : <Search size={14} />}
          {detecting ? t('Detecting...') : t('Detect Patterns')}
        </button>
      </div>

      {stats && (
        <div className="pattern-stats">
          <div className="pattern-stat">
            <Layers size={14} />
            <span>{stats.total_patterns || 0} {t('patterns')}</span>
          </div>
          <div className="pattern-stat">
            <span>{stats.total_occurrences || 0} {t('occurrences')}</span>
          </div>
          <div className="pattern-stat">
            <span>{stats.total_clusters || 0} {t('clusters')}</span>
          </div>
        </div>
      )}

      <div className="pattern-filters">
        {typeFilters.map((f) => (
          <button
            key={f.value}
            className={`pattern-filter-btn ${typeFilter === f.value ? 'active' : ''}`}
            onClick={() => setTypeFilter(f.value)}
          >
            {t(f.label)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>{t('Loading patterns...')}</span>
        </div>
      ) : patterns.length === 0 ? (
        <div className="similar-empty">
          <GitBranch size={32} className="similar-empty-icon" />
          <p>{t('No patterns detected yet')}</p>
          <span>{t('Click "Detect Patterns" to analyze crime data for recurring patterns.')}</span>
        </div>
      ) : (
        <div className="pattern-grid">
          {patterns.map((p) => (
            <PatternCard key={p.id} pattern={p} onClick={setSelectedPattern} />
          ))}
        </div>
      )}

      {selectedPattern && (
        <PatternExplorer patternId={selectedPattern.id} onClose={() => setSelectedPattern(null)} />
      )}
    </div>
  )
}
