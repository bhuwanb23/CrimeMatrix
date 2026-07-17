import { useLanguage } from '../../context/LanguageContext'
import { translateText } from '../../utils/translate'

export default function ReasoningTab({ reasoning }) {
  const { lang } = useLanguage()

  return (
    <div className="reasoning-tab">
      <div className="reasoning-chain">
        {reasoning.map((step, i) => (
          <div key={i} className="reasoning-step">
            <div className="reasoning-step-num">{step.step}</div>
            <div className="reasoning-step-connector">
              <div className="reasoning-connector-line" />
              {i < reasoning.length - 1 && <div className="reasoning-connector-dot" />}
            </div>
            <div className="reasoning-step-content">
              <p className="reasoning-step-text">{translateText(step.text, lang)}</p>
              <div className="reasoning-confidence">
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{ width: `${step.confidence}%` }}
                  />
                </div>
                <span className="confidence-value">{step.confidence}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
