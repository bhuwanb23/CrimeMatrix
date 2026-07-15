import { Fingerprint, Clock, Target, Crosshair, Route, ListOrdered } from 'lucide-react'

export default function MOTab({ suspect }) {
  const { moFingerprint } = suspect

  const moItems = [
    { icon: Fingerprint, label: 'Entry Method', value: moFingerprint.entryMethod },
    { icon: Clock, label: 'Timing', value: moFingerprint.timing },
    { icon: Target, label: 'Target Profile', value: moFingerprint.targetProfile },
    { icon: Crosshair, label: 'Weapon', value: moFingerprint.weapon },
    { icon: Route, label: 'Escape Pattern', value: moFingerprint.escapePattern },
    { icon: ListOrdered, label: 'Crime Sequence', value: moFingerprint.crimeSequence },
  ]

  return (
    <div className="mo-tab">
      <div className="mo-header">
        <Fingerprint size={20} />
        <h3>Modus Operandi Fingerprint</h3>
      </div>

      <div className="mo-grid">
        {moItems.map((item, i) => (
          <div key={i} className="mo-card">
            <div className="mo-card-icon">
              <item.icon size={16} />
            </div>
            <div className="mo-card-content">
              <span className="mo-card-label">{item.label}</span>
              <p className="mo-card-value">{item.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mo-comparison">
        <h4>MO Match Score</h4>
        <div className="mo-score-bar">
          <div className="mo-score-fill" style={{ width: `${suspect.moMatches * 20}%` }} />
        </div>
        <p className="mo-score-text">Matches {suspect.moMatches} known MO patterns</p>
      </div>
    </div>
  )
}
