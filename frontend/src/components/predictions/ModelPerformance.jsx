import { Activity } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function ModelPerformance({ models }) {
  const { t } = useLanguage()
  if (!models || models.length === 0) {
    return (
      <div className="analytics-panel">
        <div className="analytics-panel-header">
          <Activity size={14} />
          <h3>{t('Model Performance')}</h3>
        </div>
        <div className="similar-empty"><p>{t('No models registered')}</p></div>
      </div>
    )
  }

  return (
    <div className="analytics-panel">
      <div className="analytics-panel-header">
        <Activity size={14} />
        <h3>{t('Model Performance')}</h3>
      </div>
      <div className="analytics-model-list">
        {models.map((m, i) => (
          <div key={m.id || i} className="analytics-model-item">
            <div className="analytics-model-header">
              <span className="analytics-model-name">{m.name}</span>
              <span className="analytics-model-version">v{m.version || '1.0'}</span>
            </div>
            <div className="analytics-model-bar">
              <div className="analytics-model-fill" style={{ width: `${m.accuracy || 0}%` }} />
            </div>
            <div className="analytics-model-meta">
              <span>{t('Accuracy:')} {m.accuracy || 0}%</span>
              <span className={`analytics-model-status ${m.status}`}>{t(m.status)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
