import { Bot, Lightbulb, TrendingUp } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText } from '../../utils/translate'

export default function AITab({ aiInsights, suggestions }) {
  const { lang } = useLanguage()

  return (
    <div className="ai-tab">
      <div className="ai-insights-card">
        <div className="ai-insights-header">
          <Bot size={18} />
          <h4>{t('ai_analysis', lang)}</h4>
        </div>
        <p className="ai-insights-text">{translateText(aiInsights, lang)}</p>
      </div>

      <div className="ai-suggestions-card">
        <div className="ai-suggestions-header">
          <Lightbulb size={16} />
          <h4>{t('recommended_actions', lang)}</h4>
        </div>
        <div className="ai-suggestions-list">
          {suggestions.map((s, i) => (
            <div key={i} className="ai-suggestion-item">
              <div className="ai-suggestion-num">{i + 1}</div>
              <p className="ai-suggestion-text">{translateText(s, lang)}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="ai-pattern-card">
        <div className="ai-pattern-header">
          <TrendingUp size={16} />
          <h4>{t('pattern_analysis', lang)}</h4>
        </div>
        <p className="ai-pattern-text">
          {t('ai_pattern_text_desc', lang) || translateText('Based on historical data, cases with similar MO patterns have a 73% resolution rate when cross-district coordination is initiated within 48 hours.', lang)}
        </p>
      </div>
    </div>
  )
}
