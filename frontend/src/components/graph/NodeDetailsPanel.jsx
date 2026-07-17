import { X, FileText, Phone, Car, Users } from 'lucide-react'
import { edgeColors } from './graphData'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateNodeLabel, translateEdgeLabel } from '../../utils/translate'

const typeIcons = {
  suspect: Users,
  evidence: FileText,
  vehicle: Car,
  phone: Phone,
}

export default function NodeDetailsPanel({ node, edges, nodes, onClose }) {
  const { lang } = useLanguage()

  if (!node) {
    return (
      <div className="node-details-empty">
        <div className="node-details-empty-icon">🔍</div>
        <h3>{t('select_node', lang)}</h3>
        <p>{t('click_node_desc', lang)}</p>
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
          <span>{t(node.type, lang)}</span>
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
            <h3 className="node-details-name">{translateNodeLabel(node.label, lang)}</h3>
            <div className="node-details-stats">
              <div className="node-detail-stat">
                <span className="node-detail-stat-value">{node.risk}</span>
                <span className="node-detail-stat-label">{t('risk', lang)}</span>
              </div>
              <div className="node-detail-stat">
                <span className="node-detail-stat-value">{node.cases}</span>
                <span className="node-detail-stat-label">{t('cases', lang)}</span>
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="node-details-evidence-icon">{node.icon}</div>
            <h3 className="node-details-name">{translateNodeLabel(node.label, lang)}</h3>
          </>
        )}
      </div>

      <div className="node-details-connections">
        <h4>{t('connections', lang)} ({connections.length})</h4>
        <div className="connections-list">
          {connections.map((conn, i) => {
            const otherNodeId = conn.source === node.id ? conn.target : conn.source
            const otherNode = nodes.find((n) => n.id === otherNodeId)
            const connectionName = otherNode ? translateNodeLabel(otherNode.label, lang) : otherNodeId
            const connectionType = conn.label ? translateEdgeLabel(conn.label, lang) : t(conn.type, lang)
            return (
              <div key={i} className="connection-item">
                <div
                  className="connection-dot"
                  style={{ background: edgeColors[conn.type] }}
                />
                <div className="connection-info">
                  <span className="connection-name">{connectionName}</span>
                  <span className="connection-type">{connectionType}</span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {node.type === 'suspect' && (
        <div className="node-details-actions">
          <button className="node-action-btn">{t('view_full_profile', lang)}</button>
          <button className="node-action-btn secondary">{t('add_to_investigation', lang)}</button>
        </div>
      )}
    </div>
  )
}
