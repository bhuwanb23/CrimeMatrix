import { useState, useEffect, useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Brain, RefreshCw, LayoutGrid, Users, Fingerprint, Globe, Link2 } from 'lucide-react'
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
import { useLanguage } from '../context/LanguageContext'

const tabs = [
  { id: 'workspace', label: 'Workspace', icon: LayoutGrid, path: '/intelligence' },
  { id: 'profiling', label: 'Profiling', icon: Users, path: '/intelligence/profiling' },
  { id: 'mo', label: 'MO Fingerprinting', icon: Fingerprint, path: '/intelligence/mo' },
  { id: 'cross-district', label: 'Cross-District', icon: Globe, path: '/intelligence/cross-district' },
  { id: 'evidence-linking', label: 'Evidence Linking', icon: Link2, path: '/intelligence/evidence-linking' },
]

function getActiveTab(pathname) {
  if (pathname.startsWith('/intelligence/profiling')) return 'profiling'
  if (pathname.startsWith('/intelligence/mo')) return 'mo'
  if (pathname.startsWith('/intelligence/cross-district')) return 'cross-district'
  if (pathname.startsWith('/intelligence/evidence-linking')) return 'evidence-linking'
  return 'workspace'
}

export default function CrimeIntelligencePage() {
  const location = useLocation()
  const navigate = useNavigate()
  const activeTab = getActiveTab(location.pathname)
  const { t } = useLanguage()

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

  useEffect(() => { loadAll() }, [loadAll])

  async function handleDetectHotspots() {
    try { await detectHotspots(); await loadAll() } catch (e) { console.error('Detection failed', e) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Brain size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">{t('Crime Intelligence Workspace')}</h1>
                <p className="text-white/80 text-sm mt-0.5">{t('Unified intelligence — trends, patterns, hotspots, recommendations')}</p>
              </div>
            </div>
            {activeTab === 'workspace' && (
              <div className="flex items-center gap-3">
                <button onClick={handleDetectHotspots} disabled={loading}
                  className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                  {t('Detect Hotspots')}
                </button>
                <button onClick={loadAll} disabled={loading}
                  className="p-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
                  <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => navigate(tab.path)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'bg-orange-500 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={15} />
                {t(tab.label)}
              </button>
            )
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'workspace' && (
          <WorkspaceTab
            data={data} trendData={trendData} seasonalData={seasonalData}
            hotspots={hotspots} riskData={riskData} loading={loading}
            filters={filters} setFilters={setFilters}
          />
        )}
        {activeTab === 'profiling' && <ProfilingTab />}
        {activeTab === 'mo' && <MOTab />}
        {activeTab === 'cross-district' && <CrossDistrictTab />}
        {activeTab === 'evidence-linking' && <EvidenceLinkingTab />}
      </div>
    </div>
  )
}

function WorkspaceTab({ data, trendData, seasonalData, hotspots, riskData, loading, filters, setFilters }) {
  const { t } = useLanguage()
  if (loading && !data) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="w-6 h-6 border-2 border-blue-400/30 border-t-blue-400 rounded-full animate-spin" />
        <span className="ml-3 text-slate-500 text-sm">{t('Loading intelligence data...')}</span>
      </div>
    )
  }
  if (!data) {
    return (
      <div className="text-center py-16 bg-white border border-slate-200 rounded-2xl">
        <p className="text-slate-500">{t('Failed to load intelligence data')}</p>
      </div>
    )
  }

  return (
    <div className="space-y-5">
      <IntelligenceFilters filters={filters} onChange={setFilters} />

      <IntelligenceOverviewCards overview={data.overview} />

      <div className="grid grid-cols-2 gap-5">
        <TrendMainChart data={trendData?.data || data.trends?.daily || []} title={`${t('Crime Trend')} (${filters.time_range})`} />
        <IntelligenceHotspotPreview hotspots={data.hotspots} />
      </div>

      <div className="grid grid-cols-2 gap-5">
        <HotspotHeatmap hotspots={hotspots} />
        <HotspotRankings hotspots={hotspots.slice(0, 5)} />
      </div>

      <div className="grid grid-cols-2 gap-5">
        <RiskMap riskData={riskData} />
        <DistrictComparisonChart districts={{}} />
      </div>

      <div className="grid grid-cols-2 gap-5">
        <SeasonalPatterns patterns={seasonalData} />
        <IntelligenceCriminalActivity activity={data.criminal_activity} />
      </div>

      <div className="grid grid-cols-2 gap-5">
        <IntelligenceAIPanel insights={data.ai_insights} />
        <RecommendationsPanel />
      </div>
    </div>
  )
}

function ProfilingTab() {
  return (
    <div className="grid grid-cols-2 gap-5">
      <BehavioralProfileTab />
      <RepeatOffenderTab />
    </div>
  )
}

function MOTab() {
  return (
    <div className="max-w-3xl mx-auto">
      <MOComparisonTab />
    </div>
  )
}

function CrossDistrictTab() {
  return (
    <div className="max-w-3xl mx-auto">
      <CrossDistrictSection />
    </div>
  )
}

function EvidenceLinkingTab() {
  return (
    <div className="max-w-3xl mx-auto">
      <EvidenceLinkingSection />
    </div>
  )
}
