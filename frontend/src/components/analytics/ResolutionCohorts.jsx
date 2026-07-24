import { useEffect, useState } from 'react'
import { useLanguage } from '../../context/LanguageContext'
import { getCountsByStatus, getResolutionTrends } from '../../services/analyticsLive'

export default function ResolutionCohorts() {
  const { t } = useLanguage()
  const [cohorts, setCohorts] = useState([])
  const [totals, setTotals] = useState({ resolved: 0, total: 0, rate: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [statusRes, resRes] = await Promise.all([
          getCountsByStatus(),
          getResolutionTrends().catch(() => null),
        ])
        if (cancelled) return
        const rows = Array.isArray(statusRes?.data) ? statusRes.data : []
        const sum = rows.reduce((s, r) => s + (r.value || 0), 0)
        const mapped = rows.map((r) => {
          const value = r.value || 0
          const percentage = sum ? Math.round((value / sum) * 100) : 0
          return {
            period: r.key || 'unknown',
            resolved: String(r.key).toLowerCase() === 'closed' ? value : 0,
            total: value,
            percentage,
          }
        })
        const resolution = resRes?.data || {}
        setCohorts(mapped)
        setTotals({
          resolved: resolution.resolved ?? mapped.find((c) => c.period === 'closed')?.total ?? 0,
          total: resolution.total ?? sum,
          rate: resolution.resolution_rate ?? 0,
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

  const maxPercentage = Math.max(...cohorts.map((r) => r.percentage), 1)

  return (
    <div className="analytics-cohort-card">
      <div className="analytics-cohort-header">
        <h3>{t('Case Resolution')}</h3>
        <span className="analytics-cohort-subtitle">{t('by status')}</span>
      </div>

      <div className="analytics-cohort-chart">
        {loading ? (
          <p className="text-sm text-slate-400 m-0">{t('Loading...')}</p>
        ) : cohorts.length === 0 ? (
          <p className="text-sm text-slate-400 m-0">{t('No resolution data')}</p>
        ) : cohorts.map((cohort, i) => (
          <div key={i} className="cohort-item">
            <span className="cohort-label">{t(cohort.period)}</span>
            <div className="cohort-bar-container">
              <div className="cohort-bar-track">
                <div
                  className="cohort-bar-fill"
                  style={{
                    width: `${(cohort.percentage / maxPercentage) * 100}%`,
                    background: cohort.percentage >= 70 ? '#10b981' : cohort.percentage >= 50 ? '#f59e0b' : '#ef4444',
                  }}
                />
              </div>
              <span className="cohort-value">{cohort.percentage}%</span>
            </div>
            <span className="cohort-count">{cohort.total}</span>
          </div>
        ))}
      </div>

      <div className="analytics-cohort-summary">
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">{totals.resolved}</span>
          <span className="cohort-summary-label">{t('Total Resolved')}</span>
        </div>
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">{totals.total}</span>
          <span className="cohort-summary-label">{t('Total Cases')}</span>
        </div>
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">{totals.rate}%</span>
          <span className="cohort-summary-label">{t('Resolution Rate')}</span>
        </div>
      </div>
    </div>
  )
}
