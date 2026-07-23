import CrimeDonut from './analytics/CrimeDonut'
import CrimeBreakdown from './analytics/CrimeBreakdown'
import CrimeTrendLine from './analytics/CrimeTrendLine'
import DistrictRanking from './analytics/DistrictRanking'
import ResolutionCohorts from './analytics/ResolutionCohorts'
import { crimeSummary } from './analytics/analyticsData'
import { useLanguage } from '../context/LanguageContext'

export default function AnalyticsPage() {
  const { t } = useLanguage()

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1 className="analytics-title">{t('Crime Analytics')}</h1>
          <p className="analytics-subtitle">{t('Everything analytical')}</p>
        </div>
        <div className="analytics-summary-cards">
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalCases.toLocaleString()}</span>
            <span className="summary-label">{t('Total Cases')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.totalResolved.toLocaleString()}</span>
            <span className="summary-label">{t('Resolved')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.resolutionRate}%</span>
            <span className="summary-label">{t('Resolution Rate')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{crimeSummary.avgResolutionDays} {t('days')}</span>
            <span className="summary-label">{t('Avg. Resolution')}</span>
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

