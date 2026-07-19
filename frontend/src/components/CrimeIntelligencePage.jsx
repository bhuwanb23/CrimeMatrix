import { useState, useEffect } from 'react'
import { Brain, RefreshCw } from 'lucide-react'
import { getIntelligenceSummary } from '../services/intelligence'
import IntelligenceFilters from './intelligence/IntelligenceFilters'
import IntelligenceOverviewCards from './intelligence/IntelligenceOverviewCards'
import IntelligenceTrendWidget from './intelligence/IntelligenceTrendWidget'
import IntelligenceHotspotPreview from './intelligence/IntelligenceHotspotPreview'
import IntelligenceCriminalActivity from './intelligence/IntelligenceCriminalActivity'
import IntelligenceAIPanel from './intelligence/IntelligenceAIPanel'
import RecommendationsPanel from './recommendations/RecommendationsPanel'

export default function CrimeIntelligencePage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ district: '', time_range: '30d', crime_type: '' })

  useEffect(() => {
    loadIntelligence()
  }, [filters])

  async function loadIntelligence() {
    setLoading(true)
    try {
      const res = await getIntelligenceSummary(filters)
      const d = res?.data || res
      setData(d)
    } catch (e) {
      console.error('Failed to load intelligence', e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="intel-page">
      <div className="intel-header">
        <div className="intel-header-left">
          <Brain size={22} />
          <div>
            <h1>Crime Intelligence Workspace</h1>
            <p>Unified intelligence from all crime data sources</p>
          </div>
        </div>
        <button className="intel-refresh" onClick={loadIntelligence} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          Refresh
        </button>
      </div>

      <IntelligenceFilters filters={filters} onChange={setFilters} />

      {loading && !data ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading intelligence data...</span>
        </div>
      ) : data ? (
        <div className="intel-grid">
          <IntelligenceOverviewCards overview={data.overview} />

          <div className="intel-row">
            <IntelligenceTrendWidget trends={data.trends} />
            <IntelligenceHotspotPreview hotspots={data.hotspots} />
          </div>

          <div className="intel-row">
            <IntelligenceCriminalActivity activity={data.criminal_activity} />
            <IntelligenceAIPanel insights={data.ai_insights} />
          </div>

          <RecommendationsPanel />
        </div>
      ) : (
        <div className="similar-empty">
          <p>Failed to load intelligence data</p>
        </div>
      )}
    </div>
  )
}
