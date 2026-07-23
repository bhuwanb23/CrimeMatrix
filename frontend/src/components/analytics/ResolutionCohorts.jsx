import { resolutionCohorts } from './analyticsData'
import { useLanguage } from '../../context/LanguageContext'

export default function ResolutionCohorts() {
  const { t } = useLanguage()
  const maxPercentage = Math.max(...resolutionCohorts.map((r) => r.percentage))

  return (
    <div className="analytics-cohort-card">
      <div className="analytics-cohort-header">
        <h3>{t('Case Resolution')}</h3>
        <span className="analytics-cohort-subtitle">{t('by time period')}</span>
      </div>

      <div className="analytics-cohort-chart">
        {resolutionCohorts.map((cohort, i) => (
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
            <span className="cohort-count">{cohort.resolved}/{cohort.total}</span>
          </div>
        ))}
      </div>

      <div className="analytics-cohort-summary">
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">{resolutionCohorts.reduce((s, r) => s + r.resolved, 0)}</span>
          <span className="cohort-summary-label">{t('Total Resolved')}</span>
        </div>
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">{resolutionCohorts.reduce((s, r) => s + r.total, 0)}</span>
          <span className="cohort-summary-label">{t('Total Cases')}</span>
        </div>
        <div className="cohort-summary-item">
          <span className="cohort-summary-value">42 {t('days')}</span>
          <span className="cohort-summary-label">{t('Avg. Resolution')}</span>
        </div>
      </div>
    </div>
  )
}
