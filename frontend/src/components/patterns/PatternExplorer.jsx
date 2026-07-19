import { useState, useEffect } from 'react'
import { X, Clock, MapPin, Crosshair, Layers, FileText } from 'lucide-react'
import { getPattern, getPatternOccurrences } from '../../services/patterns'

const typeConfig = {
  time: { icon: Clock, label: 'Time Pattern', color: '#3b82f6' },
  mo: { icon: Crosshair, label: 'MO Pattern', color: '#ef4444' },
  location: { icon: MapPin, label: 'Location Pattern', color: '#10b981' },
  type: { icon: Layers, label: 'Type Pattern', color: '#8b5cf6' },
}

export default function PatternExplorer({ patternId, onClose }) {
  const [pattern, setPattern] = useState(null)
  const [occurrences, setOccurrences] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (patternId) loadPattern()
  }, [patternId])

  async function loadPattern() {
    setLoading(true)
    try {
      const res = await getPattern(patternId)
      const data = res?.data || res
      setPattern(data)
      setOccurrences(data?.occurrences || [])
    } catch (e) {
      console.error('Failed to load pattern', e)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="pattern-overlay" onClick={onClose}>
        <div className="pattern-modal" onClick={e => e.stopPropagation()}>
          <div className="similar-loading"><div className="similar-spinner" /><span>Loading...</span></div>
        </div>
      </div>
    )
  }

  if (!pattern) return null

  const config = typeConfig[pattern.pattern_type] || typeConfig.time
  const Icon = config.icon

  return (
    <div className="pattern-overlay" onClick={onClose}>
      <div className="pattern-modal" onClick={e => e.stopPropagation()}>
        <div className="pattern-modal-header">
          <div className="pattern-modal-title">
            <Icon size={18} style={{ color: config.color }} />
            <div>
              <h3>{pattern.name}</h3>
              <span className="pattern-modal-type" style={{ color: config.color }}>{config.label}</span>
            </div>
          </div>
          <button className="comparison-close" onClick={onClose}><X size={18} /></button>
        </div>

        <div className="pattern-modal-body">
          <div className="pattern-detail-section">
            <h4>Description</h4>
            <p>{pattern.description}</p>
          </div>

          <div className="pattern-detail-grid">
            <div className="pattern-detail-item">
              <span className="pattern-detail-label">Confidence</span>
              <span className="pattern-detail-value">{pattern.confidence}%</span>
              <div className="similar-dim-bar">
                <div className="similar-dim-fill" style={{ width: `${pattern.confidence}%`, background: config.color }} />
              </div>
            </div>
            <div className="pattern-detail-item">
              <span className="pattern-detail-label">Frequency</span>
              <span className="pattern-detail-value">{pattern.frequency} crimes</span>
            </div>
            {pattern.time_pattern && (
              <div className="pattern-detail-item">
                <span className="pattern-detail-label">Time Pattern</span>
                <span className="pattern-detail-value">{pattern.time_pattern}</span>
              </div>
            )}
            {pattern.location_pattern && (
              <div className="pattern-detail-item">
                <span className="pattern-detail-label">Location</span>
                <span className="pattern-detail-value">{pattern.location_pattern}</span>
              </div>
            )}
          </div>

          {pattern.mo_summary && (
            <div className="pattern-detail-section">
              <h4><Crosshair size={12} /> MO Summary</h4>
              <p>{pattern.mo_summary}</p>
            </div>
          )}

          {occurrences.length > 0 && (
            <div className="pattern-detail-section">
              <h4><FileText size={12} /> Matching Crimes ({occurrences.length})</h4>
              <div className="pattern-occurrences-list">
                {occurrences.map((occ, i) => (
                  <div key={i} className="pattern-occurrence-item">
                    <span className="pattern-occurrence-id">Crime #{occ.crime_id}</span>
                    <div className="pattern-occurrence-score">
                      <div className="similar-dim-bar">
                        <div className="similar-dim-fill" style={{ width: `${occ.similarity_score}%` }} />
                      </div>
                      <span>{occ.similarity_score}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
