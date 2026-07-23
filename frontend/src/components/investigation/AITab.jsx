import { useLanguage } from '../../context/LanguageContext'
import { Bot, Lightbulb, TrendingUp } from 'lucide-react'

export default function AITab({ aiInsights, suggestions }) {
  const { t } = useLanguage()
  return (
    <div className="ai-tab">
      <div className="ai-insights-card">
        <div className="ai-insights-header">
          <Bot size={18} />
          <h4>{t('AI Analysis')}</h4>
        </div>
        <p className="ai-insights-text">{aiInsights}</p>
      </div>

      <div className="ai-suggestions-card">
        <div className="ai-suggestions-header">
          <Lightbulb size={16} />
          <h4>{t('Recommended Actions')}</h4>
        </div>
        <div className="ai-suggestions-list">
          {suggestions.map((s, i) => (
            <div key={i} className="ai-suggestion-item">
              <div className="ai-suggestion-num">{i + 1}</div>
              <p className="ai-suggestion-text">{s}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="ai-pattern-card">
        <div className="ai-pattern-header">
          <TrendingUp size={16} />
          <h4>{t('Pattern Analysis')}</h4>
        </div>
        <p className="ai-pattern-text">
          {t('Based on historical data, cases with similar MO patterns have a 73% resolution rate when cross-district coordination is initiated within 48 hours.')}
        </p>
      </div>
    </div>
  )
}
