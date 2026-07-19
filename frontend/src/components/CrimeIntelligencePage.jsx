import { useState, useEffect } from 'react'
import { Brain, RefreshCw } from 'lucide-react'
import { getIntelligenceSummary } from '../services/intelligence'
import { getDailyTrends, getSeasonalPatterns } from '../services/trends'
import IntelligenceFilters from './intelligence/IntelligenceFilters'
import IntelligenceOverviewCards from './intelligence/IntelligenceOverviewCards'
import IntelligenceTrendWidget from './intelligence/IntelligenceTrendWidget'
import IntelligenceHotspotPreview from './intelligence/IntelligenceHotspotPreview'
import IntelligenceCriminalActivity from './intelligence/IntelligenceCriminalActivity'
import IntelligenceAIPanel from './intelligence/IntelligenceAIPanel'
import RecommendationsPanel from './recommendations/RecommendationsPanel'
import TrendMainChart from './trends/TrendMainChart'
import DistrictComparisonChart from './trends/DistrictComparisonChart'
import SeasonalPatterns from './trends/SeasonalPatterns'
import TrendInsights from './trends/TrendInsights'

export default function CrimeIntelligencePage() {
  const [data, setData] = useState(null)
  const [trendData, setTrendData] = useState(null)
  const [seasonalData, setSeasonalData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ district: '', time_range: '30d', crime_type: '' })

  useEffect(() => {
    loadAll()
  }, [filters])

  async function loadAll() {
    setLoading(true)
    try {
      const days = filters.time_range === '7d' ? 7 : filters.time_range === '90d' ? 90 : filters.time_range === '1y' ? 365 : 30
      const [intelRes, trendRes, seasonalRes] = await Promise.all([
        getIntelligenceSummary(filters),
        getDailyTrends({ days }),
        getSeasonalPatterns(365),
      ])
      setData(intelRes?.data || intelRes)
      setTrendData(trendRes?.data || trendRes)
      setSeasonalData(seasonalRes?.data || seasonalRes)
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
            <p>Unified intelligence — trends, patterns, hotspots, recommendations</p>
          </div>
        </div>
        <button className="intel-refresh" onClick={loadAll} disabled={loading}>
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

          {/* Trends Row — connected to time filters */}
          <div className="intel-row">
            <TrendMainChart
              data={trendData?.data || data.trends?.daily || []}
              title={`Crime Trend (${filters.time_range})`}
            />
            <IntelligenceHotspotPreview hotspots={data.hotspots} />
          </div>

          {/* District + Criminal Activity */}
          <div className="intel-row">
            <DistrictComparisonChart districts={{}} />
            <IntelligenceCriminalActivity activity={data.criminal_activity} />
          </div>

          {/* Seasonal Patterns — connected to intelligence */}
          <div className="intel-row">
            <SeasonalPatterns patterns={seasonalData} />
            <TrendInsights summary={data.trends} seasonal={seasonalData} />
          </div>

          {/* AI Panel + Recommendations — connected to all data */}
          <div className="intel-row">
            <IntelligenceAIPanel insights={data.ai_insights} />
            <RecommendationsPanel />
          </div>
        </div>
      ) : (
        <div className="similar-empty">
          <p>Failed to load intelligence data</p>
        </div>
      )}
    </div>
  )
}
