import { useState, useEffect, useCallback } from 'react'
import { Brain, RefreshCw } from 'lucide-react'
import { getIntelligenceSummary } from '../services/intelligence'
import { getDailyTrends, getSeasonalPatterns } from '../services/trends'
import { listHotspots, getRiskMap, detectHotspots } from '../services/hotspots'
import IntelligenceFilters from './intelligence/IntelligenceFilters'
import IntelligenceOverviewCards from './intelligence/IntelligenceOverviewCards'
import IntelligenceHotspotPreview from './intelligence/IntelligenceHotspotPreview'
import IntelligenceCriminalActivity from './intelligence/IntelligenceCriminalActivity'
import IntelligenceAIPanel from './intelligence/IntelligenceAIPanel'
import RecommendationsPanel from './recommendations/RecommendationsPanel'
import TrendMainChart from './trends/TrendMainChart'
import DistrictComparisonChart from './trends/DistrictComparisonChart'
import SeasonalPatterns from './trends/SeasonalPatterns'
import HotspotRankings from './hotspots/HotspotRankings'
import HotspotHeatmap from './hotspots/HotspotHeatmap'
import RiskMap from './hotspots/RiskMap'
import BehavioralProfileTab from './intelligence/BehavioralProfileTab'
import RepeatOffenderTab from './intelligence/RepeatOffenderTab'
import MOComparisonTab from './intelligence/MOComparisonTab'
import CrossDistrictSection from './intelligence/CrossDistrictSection'
import EvidenceLinkingSection from './intelligence/EvidenceLinkingSection'

export default function CrimeIntelligencePage() {
  const [data, setData] = useState(null)
  const [trendData, setTrendData] = useState(null)
  const [seasonalData, setSeasonalData] = useState(null)
  const [hotspots, setHotspots] = useState([])
  const [riskData, setRiskData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ district: '', time_range: '30d', crime_type: '' })

  const loadAll = useCallback(async () => {
    setLoading(true)
    try {
      const days = filters.time_range === '7d' ? 7 : filters.time_range === '90d' ? 90 : filters.time_range === '1y' ? 365 : 30
      const [intelRes, trendRes, seasonalRes, hotspotRes, riskRes] = await Promise.all([
        getIntelligenceSummary(filters),
        getDailyTrends({ days }),
        getSeasonalPatterns(365),
        listHotspots().catch(() => ({ data: { items: [] } })),
        getRiskMap().catch(() => ({ data: null })),
      ])
      setData(intelRes?.data || intelRes)
      setTrendData(trendRes?.data || trendRes)
      setSeasonalData(seasonalRes?.data || seasonalRes)
      setHotspots(hotspotRes?.data?.items || [])
      setRiskData(riskRes?.data || riskRes)
    } catch (e) {
      console.error('Failed to load intelligence', e)
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    loadAll()
  }, [loadAll])

  async function handleDetectHotspots() {
    try {
      await detectHotspots()
      await loadAll()
    } catch (e) {
      console.error('Detection failed', e)
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
        <div className="intel-header-actions">
          <button className="intel-refresh" onClick={handleDetectHotspots} disabled={loading}>
            Detect Hotspots
          </button>
          <button className="intel-refresh" onClick={loadAll} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
            Refresh
          </button>
        </div>
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

          {/* Trends Row */}
          <div className="intel-row">
            <TrendMainChart
              data={trendData?.data || data.trends?.daily || []}
              title={`Crime Trend (${filters.time_range})`}
            />
            <IntelligenceHotspotPreview hotspots={data.hotspots} />
          </div>

          {/* Hotspot Detection Row */}
          <div className="intel-row">
            <HotspotHeatmap hotspots={hotspots} />
            <HotspotRankings hotspots={hotspots.slice(0, 5)} />
          </div>

          {/* Risk Map + District Comparison */}
          <div className="intel-row">
            <RiskMap riskData={riskData} />
            <DistrictComparisonChart districts={{}} />
          </div>

          {/* Seasonal + Criminal Activity */}
          <div className="intel-row">
            <SeasonalPatterns patterns={seasonalData} />
            <IntelligenceCriminalActivity activity={data.criminal_activity} />
          </div>

          {/* AI + Recommendations */}
          <div className="intel-row">
            <IntelligenceAIPanel insights={data.ai_insights} />
            <RecommendationsPanel />
          </div>

          {/* Behavioral Profiling + Repeat Offenders */}
          <div className="intel-row">
            <BehavioralProfileTab />
            <RepeatOffenderTab />
          </div>

          {/* MO Fingerprinting + Cross-District + Evidence Linking */}
          <div className="grid grid-cols-3 gap-4">
            <MOComparisonTab />
            <CrossDistrictSection />
            <EvidenceLinkingSection />
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
