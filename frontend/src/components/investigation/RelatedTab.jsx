import { ExternalLink } from 'lucide-react'

export default function RelatedTab({ relatedCases }) {
  if (relatedCases.length === 0) {
    return (
      <div className="related-empty">
        <p>No related cases found</p>
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
              <span className="related-card-connection">{item.connection}</span>
            </div>
            <p className="related-card-title">{item.title}</p>
            <div className="related-card-footer">
              <div className="related-similarity">
                <div className="similarity-bar">
                  <div
                    className="similarity-fill"
                    style={{ width: `${item.similarity}%` }}
                  />
                </div>
                <span className="similarity-value">{item.similarity}% match</span>
              </div>
              <button className="related-view-btn">
                <ExternalLink size={12} />
                View
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
