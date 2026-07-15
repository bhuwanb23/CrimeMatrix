import { Brain, AlertTriangle, Activity } from 'lucide-react'

export default function BehavioralTab({ suspect }) {
  const { behavioralProfile } = suspect

  return (
    <div className="behavioral-tab">
      <div className="behavioral-grid">
        <div className="behavioral-card">
          <div className="behavioral-card-header">
            <Brain size={16} />
            <h4>Personality Profile</h4>
          </div>
          <p className="behavioral-card-text">{behavioralProfile.personality}</p>
        </div>

        <div className="behavioral-card">
          <div className="behavioral-card-header">
            <AlertTriangle size={16} />
            <h4>Risk Factors</h4>
          </div>
          <div className="behavioral-tags">
            {behavioralProfile.riskFactors.map((factor, i) => (
              <span key={i} className="behavioral-risk-tag">{factor}</span>
            ))}
          </div>
        </div>

        <div className="behavioral-card full-width">
          <div className="behavioral-card-header">
            <Activity size={16} />
            <h4>Behavioral Patterns</h4>
          </div>
          <div className="behavioral-patterns">
            {behavioralProfile.patterns.map((pattern, i) => (
              <div key={i} className="behavioral-pattern-item">
                <div className="pattern-dot" />
                <span>{pattern}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
