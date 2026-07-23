import { TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function PredictionForecastChart({ forecast }) {
  const { t } = useLanguage()
  if (!forecast) return null

  const historical = forecast.historical || []
  const predictions = forecast.forecast || []
  const allData = [...historical.map(d => ({ ...d, type: 'historical' })), ...predictions.map(d => ({ ...d, count: d.predicted, type: 'forecast' }))]
  const maxCount = Math.max(...allData.map(d => d.count || 0), 1)

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <TrendingUp size={14} />
        <h3>{t(t('Crime Forecast'))}</h3>
        <span className={`intel-trend-badge intel-trend-${forecast.trend === 'increasing' ? 'up' : forecast.trend === 'decreasing' ? 'down' : 'stable'}`}>
          {forecast.trend}
        </span>
      </div>

      <div className="analytics-forecast-chart">
        {allData.length === 0 ? (
          <div className="similar-empty"><p>No forecast data</p></div>
        ) : (
          <div className="analytics-forecast-bars">
            {allData.slice(-20).map((d, i) => (
              <div key={i} className="analytics-forecast-col">
                <div className="analytics-forecast-wrapper">
                  <div
                    className={`analytics-forecast-bar ${d.type === 'forecast' ? 'forecast' : ''}`}
                    style={{ height: `${((d.count || 0) / maxCount) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="analytics-forecast-info">
        <span>Confidence: {forecast.confidence || 0}%</span>
        <span>Data points: {forecast.data_points || 0}</span>
      </div>
    </div>
  )
}
