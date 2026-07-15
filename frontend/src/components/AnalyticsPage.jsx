import CrimeDonut from './analytics/CrimeDonut'
import CrimeBreakdown from './analytics/CrimeBreakdown'
import CrimeTrendLine from './analytics/CrimeTrendLine'
import DistrictRanking from './analytics/DistrictRanking'
import ResolutionCohorts from './analytics/ResolutionCohorts'
import { crimeSummary } from './analytics/analyticsData'

export default function AnalyticsPage() {
  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1 className="analytics-title">Crime Analytics</h1>
          <p className="analytics-subtitle">Everything analytical</p>
        </div>
        <div className="analytics-summary-cards">
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalCases.toLocaleString()}</span>
            <span className="summary-label">Total Cases</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalResolved.toLocaleString()}</span>
            <span className="summary-label">Resolved</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.resolutionRate}%</span>
            <span className="summary-label">Resolution Rate</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.avgResolutionDays} days</span>
            <span className="summary-label">Avg. Resolution</span>
          </div>
        </div>
      </div>

      <div className="analytics-grid-top">
        <CrimeDonut />
        <div className="analytics-grid-top-right">
          <CrimeBreakdown />
        </div>
      </div>

      <CrimeTrendLine />

      <div className="analytics-grid-bottom">
        <DistrictRanking />
        <ResolutionCohorts />
      </div>
    </div>
  )
}
