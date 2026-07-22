import { useState, useEffect } from 'react'
import { LineChart, RefreshCw, TrendingUp } from 'lucide-react'
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

export default function PredictionAnalyticsPage() {
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
        <span className="text-sm text-slate-500">Loading prediction analytics...</span>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center">
            <LineChart size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Predictive Crime Analytics</h1>
            <p className="text-xs text-slate-500">Forecast crime patterns with confidence indicators</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <select className="bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-sm text-slate-700 focus:outline-none focus:border-amber-500"
            value={selectedDistrict} onChange={e => setSelectedDistrict(e.target.value)}>
            <option value="">All Districts</option>
            {districts.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
          </select>
          <div className="flex bg-white border border-slate-200 rounded-lg p-0.5">
            {[30, 60, 90].map(d => (
              <button key={d} onClick={() => setTimeHorizon(d)}
                className={`px-3 py-1 rounded text-xs font-medium transition-all ${timeHorizon === d ? 'bg-amber-500 text-white' : 'text-slate-500 hover:text-slate-700'}`}>
                {d}D
              </button>
            ))}
          </div>
          <button onClick={handleForecast} disabled={forecasting}
            className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg text-sm font-semibold hover:opacity-90 disabled:opacity-50 shadow-sm">
            {forecasting ? <RefreshCw size={14} className="animate-spin" /> : <TrendingUp size={14} />}
            {forecasting ? 'Forecasting...' : 'Generate Forecast'}
          </button>
        </div>
      </div>

      {/* Row 1: Summary Cards */}
      <PredictionSummaryCards stats={stats} />

      {/* Row 2: Forecast + District Map (balanced 50/50) */}
      <div className="grid grid-cols-2 gap-4">
        <PredictionForecastChart forecast={forecast} />
        <DistrictPredictionMap districts={districts} />
      </div>

      {/* Row 3: Seasonal + Confidence + Crime Types */}
      <div className="grid grid-cols-3 gap-4">
        <SeasonalPatternsChart patterns={seasonal} />
        <ConfidenceBreakdown forecast={forecast} />
        <CrimeTypePredictions predictions={predictions} />
      </div>

      {/* Row 4: AI Predictions + Model Performance */}
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2">
          <AIPredictionsPanel forecast={forecast} predictions={predictions} districts={districts} />
        </div>
        <ModelPerformance models={models} />
      </div>

      {/* Row 5: Explanation + Sources */}
      <div className="grid grid-cols-2 gap-4">
        <PredictionExplanationPanel predictionId={predictions[0]?.id} />
        <SourceReferences predictionId={predictions[0]?.id} />
      </div>
    </div>
  )
}
