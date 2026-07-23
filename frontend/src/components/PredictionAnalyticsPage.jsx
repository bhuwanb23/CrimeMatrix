import { useState, useEffect } from 'react'
import { LineChart, RefreshCw, TrendingUp, Map, BarChart3, Bot } from 'lucide-react'
import { generateForecast, getPredictionStats, getPredictionModels, listPredictions } from '../services/predictions'
import { get } from '../services/api'
import { listDistricts } from '../services/search'
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
  return (
    <div className="space-y-5">
      <DistrictPredictionMap districts={districts} />
    </div>
  )
}

function CrimeForecastTab({ forecast, seasonal, predictions }) {
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
      <div className="grid grid-cols-3 gap-5">
        <div className="col-span-2">
          <AIPredictionsPanel forecast={forecast} predictions={predictions} districts={districts} />
        </div>
        <ModelPerformance models={models} />
      </div>
      <div className="grid grid-cols-3 gap-5">
        <ConfidenceBreakdown forecast={forecast} />
        <PredictionExplanationPanel predictionId={predictions[0]?.id} />
        <SourceReferences predictionId={predictions[0]?.id} />
      </div>
    </div>
  )
}
