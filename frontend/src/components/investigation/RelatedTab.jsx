import { ExternalLink } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function RelatedTab({ caseId, relatedCases }) {
  const navigate = useNavigate()

  if (!relatedCases || relatedCases.length === 0) {
    return (
      <div className="related-empty">
        <p>No related cases found</p>
      </div>
    )
  }

  return (
    <div className="related-tab">
      <div className="related-list">
        {relatedCases.map((item, i) => {
          const score = item.overall_score || item.similarity || 0
          const reasons = item.reasons || []
          const connection = reasons.length > 0 ? reasons[0] : (item.connection || 'Similar')
          return (
            <div key={item.case_id || i} className="related-card">
              <div className="related-card-header">
                <span className="related-card-id">{item.case_number || `Case #${item.case_id}`}</span>
                <span className="related-card-connection">{connection}</span>
              </div>
              <p className="related-card-title">{item.title}</p>
              <div className="related-card-footer">
                <div className="related-similarity">
                  <div className="similarity-bar">
                    <div
                      className="similarity-fill"
                      style={{ width: `${score}%` }}
                    />
                  </div>
                  <span className="similarity-value">{score}% match</span>
                </div>
                <button className="related-view-btn" onClick={() => navigate(`/cases/${item.case_id}`)}>
                  <ExternalLink size={12} />
                  View
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
