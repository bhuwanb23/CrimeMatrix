import { useEffect, useState } from 'react'
import CrimeDonut from './analytics/CrimeDonut'
import CrimeBreakdown from './analytics/CrimeBreakdown'
import CrimeTrendLine from './analytics/CrimeTrendLine'
import DistrictRanking from './analytics/DistrictRanking'
import ResolutionCohorts from './analytics/ResolutionCohorts'
import { useLanguage } from '../context/LanguageContext'
import { getStatistics } from '../services/analyticsLive'
import { getAnalyticsOverview, getResolutionTrends } from '../services/analyticsLive'

export default function AnalyticsPage() {
  const { t } = useLanguage()
  const [summary, setSummary] = useState({
    totalCases: 0,
    totalResolved: 0,
    resolutionRate: 0,
    avgResolutionDays: '—',
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [statsRes, overviewRes, resolutionRes] = await Promise.all([
          getStatistics().catch(() => null),
          getAnalyticsOverview().catch(() => null),
          getResolutionTrends().catch(() => null),
        ])
        if (cancelled) return
        const stats = statsRes?.data || {}
        const overview = overviewRes?.data || {}
        const resolution = resolutionRes?.data || {}
        const totalCases = overview.total_crimes ?? stats.totals?.cases ?? 0
        const totalResolved = overview.closed_crimes ?? stats.cases_by_status?.closed ?? resolution.resolved ?? 0
        const resolutionRate = overview.resolution_rate ?? stats.resolution_rate ?? resolution.resolution_rate ?? 0
        setSummary({
          totalCases,
          totalResolved,
          resolutionRate,
          avgResolutionDays: '—',
        })
      } catch (e) {
        console.error(e)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1 className="analytics-title">{t('Crime Analytics')}</h1>
          <p className="analytics-subtitle">{t('Everything analytical')}</p>
        </div>
        <div className="analytics-summary-cards">
          <div className="analytics-summary-card">
            <span className="summary-value">{loading ? '…' : summary.totalCases.toLocaleString()}</span>
            <span className="summary-label">{t('Total Cases')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{loading ? '…' : summary.totalResolved.toLocaleString()}</span>
            <span className="summary-label">{t('Resolved')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{loading ? '…' : `${summary.resolutionRate}%`}</span>
            <span className="summary-label">{t('Resolution Rate')}</span>
          </div>
          <div className="analytics-summary-card">
            <span className="summary-value">{summary.avgResolutionDays}</span>
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
