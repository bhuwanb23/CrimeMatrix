import { useState, useEffect } from 'react'
import { BarChart3, RefreshCw } from 'lucide-react'
import { getDashboardSummary, getDashboardAlerts, getDashboardForecasts, getDashboardHighRisk, getDashboardPriority } from '../services/analyticsDashboard'
import PredictionSummaryCards from './analytics/PredictionSummaryCards'
import ActiveAlertsPanel from './analytics/ActiveAlertsPanel'
import ForecastChart from './analytics/ForecastChart'
import HighRiskSuspectsList from './analytics/HighRiskSuspectsList'
import PriorityCasesList from './analytics/PriorityCasesList'
import AIRecommendationsPanel from './analytics/AIRecommendationsPanel'

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
    <div className="analytics-dashboard-page">
      <div className="intel-header">
        <div className="intel-header-left">
          <BarChart3 size={22} />
          <div>
            <h1>AI Analytics Dashboard</h1>
            <p>Predictive insights, risk assessments, and actionable recommendations</p>
          </div>
        </div>
        <button className="intel-refresh" onClick={loadAll} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
          Refresh
        </button>
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
  )
}
