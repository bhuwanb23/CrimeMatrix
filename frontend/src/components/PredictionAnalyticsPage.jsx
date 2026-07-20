import { useState, useEffect } from 'react'
import { LineChart, RefreshCw } from 'lucide-react'
import { generateForecast, getPredictionStats, getPredictionModels, listPredictions } from '../services/predictions'
import { listDistricts } from '../services/search'
import PredictionSummaryCards from './predictions/PredictionSummaryCards'
import PredictionForecastChart from './predictions/PredictionForecastChart'
import DistrictPredictionMap from './predictions/DistrictPredictionMap'
import CrimeTypePredictions from './predictions/CrimeTypePredictions'
import ModelPerformance from './predictions/ModelPerformance'
import AIPredictionsPanel from './predictions/AIPredictionsPanel'

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

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const [statsRes, modelsRes, predsRes, districtsRes] = await Promise.all([
        getPredictionStats(),
        getPredictionModels(),
        listPredictions(),
        listDistricts().catch(() => ({ data: [] })),
      ])
      setStats(statsRes?.data || statsRes)
      setModels(modelsRes?.data || [])
      setPredictions(predsRes?.data?.items || [])
      setDistricts(districtsRes?.data?.items || districtsRes?.data || [])
    } catch (e) {
      console.error('Failed to load prediction data', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleForecast() {
    setForecasting(true)
    try {
      const params = { periods: timeHorizon }
      if (selectedDistrict) params.district_id = parseInt(selectedDistrict)
      const res = await generateForecast(params)
      setForecast(res?.data || res)
    } catch (e) {
      console.error('Forecast failed', e)
    } finally {
      setForecasting(false)
    }
  }

  return (
    <div className="analytics-dashboard-page">
      <div className="intel-header">
        <div className="intel-header-left">
          <LineChart size={22} />
          <div>
            <h1>Predictive Crime Analytics</h1>
            <p>Forecast crime patterns with confidence indicators</p>
          </div>
        </div>
        <div className="intel-header-actions">
          <select className="intel-filter-select" value={selectedDistrict} onChange={(e) => setSelectedDistrict(e.target.value)}>
            <option value="">All Districts</option>
            {districts.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
          <div className="map-time-btns">
            {[30, 60, 90].map((d) => (
              <button key={d} className={`map-time-btn ${timeHorizon === d ? 'active' : ''}`} onClick={() => setTimeHorizon(d)}>
                {d}D
              </button>
            ))}
          </div>
          <button className="similar-btn similar-btn-primary" onClick={handleForecast} disabled={forecasting}>
            {forecasting ? 'Forecasting...' : 'Generate Forecast'}
          </button>
          <button className="intel-refresh" onClick={loadAll} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          </button>
        </div>
      </div>

      {loading && !stats ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading prediction analytics...</span>
        </div>
      ) : (
        <div className="intel-grid">
          <PredictionSummaryCards stats={stats} />

          <div className="intel-row">
            <PredictionForecastChart forecast={forecast} />
            <DistrictPredictionMap districts={districts} />
          </div>

          <div className="intel-row">
            <CrimeTypePredictions predictions={predictions} />
            <ModelPerformance models={models} />
          </div>

          <AIPredictionsPanel forecast={forecast} predictions={predictions} districts={districts} />
        </div>
      )}
    </div>
  )
}
