import { TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function ForecastChart({ forecasts }) {
  const { t } = useLanguage()
  if (!forecasts) return null

  const historical = forecasts.historical || []
  const forecast = forecasts.forecast || []
  const maxCount = Math.max(...historical.map(d => d.count || 0), 1)

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <TrendingUp size={14} />
        <h3>{t(t('Crime Forecast'))}</h3>
        <span className="similar-count">{forecasts.data_points || 0} data points</span>
      </div>

      <div className="analytics-forecast-chart">
        {historical.length === 0 ? (
          <div className="similar-empty"><p>No forecast data</p></div>
        ) : (
          <div className="analytics-forecast-bars">
            {historical.slice(-14).map((d, i) => (
              <div key={i} className="analytics-forecast-col">
                <div className="analytics-forecast-wrapper">
                  <div
                    className="analytics-forecast-bar"
                    style={{ height: `${((d.count || 0) / maxCount) * 100}%` }}
                  />
                </div>
                <span className="analytics-forecast-label">{(d.date || '').slice(-5)}</span>
              </div>
            ))}
            {forecast.map((f, i) => (
              <div key={`f-${i}`} className="analytics-forecast-col">
                <div className="analytics-forecast-wrapper">
                  <div
                    className="analytics-forecast-bar forecast"
                    style={{ height: `${((f.count || 0) / maxCount) * 100}%` }}
                  />
                </div>
                <span className="analytics-forecast-label forecast-label">pred</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {forecast.length > 0 && (
        <div className="analytics-forecast-info">
          <span>Predicted: {forecast[0].count} crimes</span>
          <span>Confidence: {forecast[0].confidence}%</span>
        </div>
      )}
    </div>
  )
}
