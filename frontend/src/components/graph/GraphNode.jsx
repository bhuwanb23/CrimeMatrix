import { useLanguage } from '../../context/LanguageContext'

const nodeColors = {
  suspect: { fill: '#1e293b', stroke: '#ef4444', text: '#ffffff' },
  evidence: { fill: '#3b82f6', stroke: '#60a5fa', text: '#ffffff' },
  vehicle: { fill: '#8b5cf6', stroke: '#a78bfa', text: '#ffffff' },
  phone: { fill: '#10b981', stroke: '#34d399', text: '#ffffff' },
  criminal: { fill: '#f59e0b', stroke: '#fbbf24', text: '#ffffff' },
}

function getNodeColors(type) {
  return nodeColors[type] || { fill: '#64748b', stroke: '#94a3b8', text: '#ffffff' }
}

export default function GraphNode({ node, isSelected, isHighlighted, onClick, onMouseEnter, onMouseLeave }) {
  const { t } = useLanguage()
  const isSuspect = node.type === 'suspect'
  const size = isSuspect ? 38 + (node.cases || 0) * 2 : 30
  const colors = getNodeColors(node.type)
  const translatedLabel = t(node.label || '')
  const displayLabel = translatedLabel.length > 18 ? translatedLabel.slice(0, 16) + '...' : translatedLabel

  return (
    <g
      className="graph-node"
      transform={`translate(${node.x}, ${node.y})`}
      onClick={() => onClick(node)}
      onMouseEnter={() => onMouseEnter(node)}
      onMouseLeave={onMouseLeave}
      style={{ cursor: 'pointer' }}
    >
      {/* Glow for selected */}
      {isSelected && (
        <circle r={size / 2 + 10} fill="none" stroke={colors.stroke} strokeWidth="2.5" opacity="0.5" className="node-glow" />
      )}

      {/* Highlight ring for connected nodes */}
      {isHighlighted && !isSelected && (
        <circle r={size / 2 + 5} fill="none" stroke={colors.stroke} strokeWidth="1.5" opacity="0.3" strokeDasharray="4 2" />
      )}

      {/* Outer ring (color accent) */}
      <circle r={size / 2 + 3} fill="none" stroke={colors.stroke} strokeWidth="2" opacity={isSelected ? 1 : 0.6} />

      {/* Main node circle */}
      <circle r={size / 2} fill={colors.fill} stroke="white" strokeWidth="2" className="node-circle" />

      {/* Node content */}
      {isSuspect ? (
        <text textAnchor="middle" dominantBaseline="central" fill={colors.text} fontSize="11" fontWeight="700" fontFamily="var(--font-sans, sans-serif)">
          {node.id}
        </text>
      ) : (
        <text textAnchor="middle" dominantBaseline="central" fill={colors.text} fontSize="13" fontWeight="600">
          {node.icon}
        </text>
      )}

      {/* Label */}
      <text y={size / 2 + 15} textAnchor="middle" fill="#475569" fontSize="10" fontWeight="500" fontFamily="var(--font-sans, sans-serif)">
        {displayLabel}
      </text>

      {/* Risk badge for suspects */}
      {isSuspect && node.risk && (
        <>
          <circle cx={size / 2 - 2} cy={-size / 2 + 2} r="9" fill={node.risk > 70 ? '#ef4444' : node.risk > 40 ? '#f59e0b' : '#10b981'} stroke="white" strokeWidth="1.5" />
          <text x={size / 2 - 2} y={-size / 2 + 2} textAnchor="middle" dominantBaseline="central" fill="white" fontSize="7" fontWeight="700" fontFamily="var(--font-sans, sans-serif)">
            {node.risk}
          </text>
        </>
      )}
    </g>
  )
}
