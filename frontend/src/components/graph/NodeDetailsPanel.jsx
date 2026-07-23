import { X, FileText, Phone, Car, Users } from 'lucide-react'
import { edgeColors } from './graphData'
import { useLanguage } from '../../context/LanguageContext'

const typeIcons = {
  suspect: Users,
  evidence: FileText,
  vehicle: Car,
  phone: Phone,
}

export default function NodeDetailsPanel({ node, edges, nodes, onClose }) {
  const { t } = useLanguage()

  if (!node) {
    return (
      <div className="node-details-empty">
        <div className="node-details-empty-icon">🔍</div>
        <h3>{t('Select a Node')}</h3>
        <p>{t('Click on any node in the graph to view details')}</p>
      </div>
    )
  }

  const Icon = typeIcons[node.type] || Users
  const connections = edges.filter(
    (e) => e.source === node.id || e.target === node.id
  )

  return (
    <div className="node-details-panel">
      <div className="node-details-header">
        <div className="node-details-type">
          <Icon size={14} />
          <span>{t(node.type)}</span>
        </div>
        <button className="node-details-close" onClick={onClose}>
          <X size={16} />
        </button>
      </div>

      <div className="node-details-info">
        {node.type === 'suspect' ? (
          <>
            <div className="node-details-avatar" style={{ background: node.gradient }}>
              {node.id}
            </div>
            <h3 className="node-details-name">{t(node.label)}</h3>
            <div className="node-details-stats">
              <div className="node-detail-stat">
                <span className="node-detail-stat-value">{node.risk}</span>
                <span className="node-detail-stat-label">{t('Risk')}</span>
              </div>
              <div className="node-detail-stat">
                <span className="node-detail-stat-value">{node.cases}</span>
                <span className="node-detail-stat-label">{t('Cases')}</span>
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="node-details-evidence-icon">{node.icon}</div>
            <h3 className="node-details-name">{t(node.label)}</h3>
          </>
        )}
      </div>

      <div className="node-details-connections">
        <h4>{t('Connections')} ({connections.length})</h4>
        <div className="connections-list">
          {connections.map((conn, i) => {
            const otherNodeId = conn.source === node.id ? conn.target : conn.source
            const otherNode = nodes.find((n) => n.id === otherNodeId)
            return (
              <div key={i} className="connection-item">
                <div
                  className="connection-dot"
                  style={{ background: edgeColors[conn.type] }}
                />
                <div className="connection-info">
                  <span className="connection-name">{t(otherNode?.label || otherNodeId)}</span>
                  <span className="connection-type">{t(conn.label || conn.type)}</span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {node.type === 'suspect' && (
        <div className="node-details-actions">
          <button className="node-action-btn">{t('View Full Profile')}</button>
          <button className="node-action-btn secondary">{t('Add to Investigation')}</button>
        </div>
      )}
    </div>
  )
}

