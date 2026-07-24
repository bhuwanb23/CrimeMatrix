import { useState, useEffect } from 'react'
import { LineChart, RefreshCw, TrendingUp, Map, BarChart3, Bot } from 'lucide-react'
import { generateForecast, getPredictionStats, getPredictionModels, listPredictions } from '../services/predictions'
import { get } from '../services/api'
import { listDistricts } from '../services/search'
import { useLanguage } from '../context/LanguageContext'
import PredictionSummaryCards from './predictions/PredictionSummaryCards'
import PredictionForecastChart from './predictions/PredictionForecastChart'
import DistrictPredictionMap from './predictions/DistrictPredictionMap'
import CrimeTypePredictions from './predictions/CrimeTypePredictions'
import ModelPerformance from './predictions/ModelPerformance'
import AIPredictionsPanel from './predictions/AIPredictionsPanel'
import SeasonalPatternsChart from './predictions/SeasonalPatternsChart'
import PredictionExplanationPanel from './predictions/PredictionExplanationPanel'
import ConfidenceBreakdown from './predictions/ConfidenceBreakdown'
import SourceReferences from './predictions/SourceReferences'

const tabs = [
  { id: 'district', label: 'District Predictions', icon: Map },
  { id: 'forecast', label: 'Crime Forecast', icon: BarChart3 },
  { id: 'ai', label: 'AI Predictions', icon: Bot },
]

export default function PredictionAnalyticsPage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState('district')
  const [stats, setStats] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [models, setModels] = useState([])
  const [predictions, setPredictions] = useState([])
  const [districts, setDistricts] = useState([])
  const [loading, setLoading] = useState(true)
  const [forecasting, setForecasting] = useState(false)
  const [selectedDistrict, setSelectedDistrict] = useState('')
  const [timeHorizon, setTimeHorizon] = useState(30)
  const [seasonal, setSeasonal] = useState(null)

  useEffect(() => {
    let cancelled = false

    async function loadAll() {
      setLoading(true)
      try {
        const [statsRes, modelsRes, predsRes, districtsRes, seasonalRes] = await Promise.all([
          getPredictionStats(),
          getPredictionModels(),
          listPredictions(),
          listDistricts().catch(() => ({ data: [] })),
          get(`/predictions/forecast/seasonal?days=365`).catch(() => ({ data: null })),
        ])
        if (cancelled) return
        setStats(statsRes?.data || statsRes)
        setModels(modelsRes?.data || [])
        setPredictions(predsRes?.data?.items || [])
        setDistricts(districtsRes?.data?.items || districtsRes?.data || [])
        setSeasonal(seasonalRes?.data || seasonalRes)

        try {
          const forecastRes = await generateForecast({ periods: timeHorizon })
          if (!cancelled) setForecast(forecastRes?.data || forecastRes)
        } catch (e) { console.error(e) }
      } catch (e) { console.error(e) } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadAll()
    return () => { cancelled = true }
  }, [timeHorizon])

  async function handleForecast() {
    setForecasting(true)
    try {
      const params = { periods: timeHorizon }
      if (selectedDistrict) params.district_id = parseInt(selectedDistrict)
      const res = await generateForecast(params)
      setForecast(res?.data || res)
    } catch (e) { console.error(e) } finally { setForecasting(false) }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 gap-3">
        <div className="w-8 h-8 border-2 border-slate-200 border-t-amber-500 rounded-full animate-spin" />
        <span className="text-sm text-slate-500">{t('Loading prediction analytics...')}</span>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-orange-500/20 shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <LineChart size={20} />
              </div>
              <div>
                <h1 className="text-lg font-bold">Predictive Crime Analytics</h1>
                <p className="text-white/80 text-xs">Forecast crime patterns with confidence indicators</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <select className="bg-white/20 backdrop-blur border border-white/30 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-white/60"
                value={selectedDistrict} onChange={e => setSelectedDistrict(e.target.value)}>
                <option value="" className="text-slate-900">{t('All Districts')}</option>
                {districts.map(d => <option key={d.id} value={d.id} className="text-slate-900">{t(d.name)}</option>)}
              </select>
              <div className="flex bg-white/20 backdrop-blur rounded-lg p-0.5">
                {[30, 60, 90].map(d => (
                  <button key={d} onClick={() => setTimeHorizon(d)}
                    className={`px-3 py-1 rounded text-xs font-medium transition-all ${timeHorizon === d ? 'bg-white text-orange-600' : 'text-white/80 hover:text-white'}`}>
                    {d}D
                  </button>
                ))}
              </div>
              <button onClick={handleForecast} disabled={forecasting}
                className="flex items-center gap-1.5 px-4 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                {forecasting ? <RefreshCw size={14} className="animate-spin" /> : <TrendingUp size={14} />}
                {forecasting ? t('Forecasting...') : t('Generate Forecast')}
              </button>
            </div>
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1 w-fit">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-orange-500 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'district' && (
          <DistrictPredictionsTab districts={districts} />
        )}
        {activeTab === 'forecast' && (
          <CrimeForecastTab forecast={forecast} seasonal={seasonal} predictions={predictions} />
        )}
        {activeTab === 'ai' && (
          <AIPredictionsTab stats={stats} models={models} predictions={predictions}
            forecast={forecast} districts={districts} />
        )}
      </div>
    </div>
  )
}

function DistrictPredictionsTab({ districts }) {
  const { t } = useLanguage()

  if (!districts || districts.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
            <Map size={16} className="text-emerald-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">District Predictions</h3>
            <p className="text-[10px] text-slate-400">Crime prediction breakdown by district</p>
          </div>
        </div>
        <div className="text-center py-12">
          <Map size={32} className="mx-auto text-slate-200 mb-3" />
          <p className="text-sm font-medium text-slate-500 mb-1">No district data available</p>
          <p className="text-xs text-slate-400">District predictions will appear once crime data is loaded with district information.</p>
        </div>
      </div>
    )
  }

  const maxCount = Math.max(...districts.map(d => d.crime_count || d.total || 0), 1)

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
            <Map size={16} className="text-emerald-500" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">District Predictions</h3>
            <p className="text-[10px] text-slate-400">Crime prediction breakdown by district</p>
          </div>
        </div>
        <span className="text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-medium">{districts.length} districts</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-slate-100">
              <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">District</th>
              <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Crime Count</th>
              <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider w-[40%]">Distribution</th>
              <th className="px-5 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-wider text-right">Risk</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((d, i) => {
              const count = d.crime_count || d.total || 0
              const risk = d.risk || (count > maxCount * 0.7 ? 'high' : count > maxCount * 0.3 ? 'medium' : 'low')
              const color = risk === 'high' ? '#ef4444' : risk === 'medium' ? '#f59e0b' : '#10b981'
              return (
                <tr key={i} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                  <td className="px-5 py-3 text-xs font-medium text-slate-900">{d.name || d.district || `District ${i + 1}`}</td>
                  <td className="px-5 py-3 text-xs font-bold text-slate-700">{count}</td>
                  <td className="px-5 py-3">
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${(count / maxCount) * 100}%`, background: color }} />
                    </div>
                  </td>
                  <td className="px-5 py-3 text-right">
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded capitalize" style={{ color, background: `${color}15` }}>
                      {risk}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function CrimeForecastTab({ forecast, seasonal, predictions }) {
  const { t } = useLanguage()

  return (
    <div className="space-y-5">
      <PredictionForecastChart forecast={forecast} />
      <div className="grid grid-cols-2 gap-5">
        <SeasonalPatternsChart patterns={seasonal} />
        <CrimeTypePredictions predictions={predictions} />
      </div>
    </div>
  )
}

function AIPredictionsTab({ stats, models, predictions, forecast, districts }) {
  return (
    <div className="space-y-5">
      <PredictionSummaryCards stats={stats} />
      <div className="grid grid-cols-12 gap-5">
        <div className="col-span-8">
          <AIPredictionsPanel forecast={forecast} predictions={predictions} districts={districts} />
        </div>
        <div className="col-span-4">
          <ModelPerformance models={models} />
        </div>
      </div>
      <div className="grid grid-cols-3 gap-5">
        <ConfidenceBreakdown forecast={forecast} />
        <PredictionExplanationPanel predictionId={predictions[0]?.id} />
        <SourceReferences predictionId={predictions[0]?.id} />
      </div>
    </div>
  )
}
