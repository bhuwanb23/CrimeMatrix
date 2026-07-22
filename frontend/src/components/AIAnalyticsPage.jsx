import { useState, useEffect } from 'react'
import { BarChart3, RefreshCw } from 'lucide-react'
import { getDashboardSummary, getDashboardAlerts, getDashboardForecasts, getDashboardHighRisk, getDashboardPriority } from '../services/analyticsDashboard'
import PredictionSummaryCards from './analytics/PredictionSummaryCards'
import ActiveAlertsPanel from './analytics/ActiveAlertsPanel'
import ForecastChart from './analytics/ForecastChart'
import HighRiskSuspectsList from './analytics/HighRiskSuspectsList'
import PriorityCasesList from './analytics/PriorityCasesList'
import AIRecommendationsPanel from './analytics/AIRecommendationsPanel'
import ModelEvaluationPanel from './analytics/ModelEvaluationPanel'
import AccuracyTrendChart from './analytics/AccuracyTrendChart'
import FeedbackSummary from './analytics/FeedbackSummary'

export default function AIAnalyticsPage() {
  const [summary, setSummary] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [forecasts, setForecasts] = useState(null)
  const [highRisk, setHighRisk] = useState([])
  const [priority, setPriority] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAll()
  }, [])

  async function loadAll() {
    setLoading(true)
    try {
      const [summaryRes, alertsRes, forecastRes, highRiskRes, priorityRes] = await Promise.all([
        getDashboardSummary(),
        getDashboardAlerts(),
        getDashboardForecasts(),
        getDashboardHighRisk(),
        getDashboardPriority(),
      ])
      setSummary(summaryRes?.data || summaryRes)
      setAlerts(alertsRes?.data || [])
      setForecasts(forecastRes?.data || forecastRes)
      setHighRisk(highRiskRes?.data || [])
      setPriority(priorityRes?.data || [])
    } catch (e) {
      console.error('Failed to load analytics dashboard', e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <BarChart3 size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">AI Analytics Dashboard</h1>
                <p className="text-white/80 text-sm mt-0.5">Predictive insights, risk assessments, and actionable recommendations</p>
              </div>
            </div>
            <button onClick={loadAll} disabled={loading}
              className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              Refresh
            </button>
          </div>
        </div>

      {loading && !summary ? (
        <div className="similar-loading">
          <div className="similar-spinner" />
          <span>Loading analytics dashboard...</span>
        </div>
      ) : summary ? (
        <div className="intel-grid">
          {/* Prediction Summary Cards */}
          <PredictionSummaryCards predictions={summary.predictions} />

          {/* Alerts + High-Risk */}
          <div className="intel-row">
            <ActiveAlertsPanel alerts={alerts} />
            <HighRiskSuspectsList suspects={highRisk} />
          </div>

          {/* Forecast + Priority */}
          <div className="intel-row">
            <ForecastChart forecasts={forecasts} />
            <PriorityCasesList cases={priority} />
          </div>

          {/* AI Recommendations */}
          <AIRecommendationsPanel alerts={alerts} highRisk={highRisk} priority={priority} />

          {/* Model Evaluation Row */}
          <div className="grid grid-cols-3 gap-4">
            <ModelEvaluationPanel />
            <AccuracyTrendChart />
            <FeedbackSummary />
          </div>
        </div>
      ) : (
        <div className="similar-empty">
          <p>Failed to load analytics dashboard</p>
        </div>
      )}
      </div>
    </div>
  )
}
