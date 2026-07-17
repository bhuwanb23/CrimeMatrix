import { ExternalLink } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText } from '../../utils/translate'

export default function RelatedTab({ relatedCases }) {
  const { lang } = useLanguage()

  if (relatedCases.length === 0) {
    return (
      <div className="related-empty">
        <p>{t('no_related_cases_found', lang)}</p>
      </div>
    )
  }

  return (
    <div className="related-tab">
      <div className="related-list">
        {relatedCases.map((item, i) => (
          <div key={i} className="related-card">
            <div className="related-card-header">
              <span className="related-card-id">{item.id}</span>
              <span className="related-card-connection">{translateText(item.connection, lang)}</span>
            </div>
            <p className="related-card-title">{translateText(item.title, lang)}</p>
            <div className="related-card-footer">
              <div className="related-similarity">
                <div className="similarity-bar">
                  <div
                    className="similarity-fill"
                    style={{ width: `${item.similarity}%` }}
                  />
                </div>
                <span className="similarity-value">{item.similarity}% {t('match', lang)}</span>
              </div>
              <button className="related-view-btn">
                <ExternalLink size={12} />
                {t('view', lang)}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
