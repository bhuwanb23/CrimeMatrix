import CrimeDonut from './analytics/CrimeDonut'
import CrimeBreakdown from './analytics/CrimeBreakdown'
import CrimeTrendLine from './analytics/CrimeTrendLine'
import DistrictRanking from './analytics/DistrictRanking'
import ResolutionCohorts from './analytics/ResolutionCohorts'
import { crimeSummary } from './analytics/analyticsData'
import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function AnalyticsPage() {
  const { lang } = useLanguage()
  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1 className="analytics-title">{t('crime_analytics', lang)}</h1>
          <p className="analytics-subtitle">{t('everything_analytical', lang)}</p>
        </div>
        <div className="analytics-summary-cards">
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalCases.toLocaleString()}</span>
            <span className="summary-label">{t('total_cases', lang)}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalResolved.toLocaleString()}</span>
            <span className="summary-label">{t('resolved', lang)}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.resolutionRate}%</span>
            <span className="summary-label">{t('resolution_rate', lang)}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.avgResolutionDays} {t('days_label', lang)}</span>
            <span className="summary-label">{t('avg_resolution', lang)}</span>
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
