import { useLanguage } from '../../context/LanguageContext'

export default function GraphNode({ node, isSelected, isHighlighted, onClick, onMouseEnter, onMouseLeave }) {
  const { t } = useLanguage()
  const size = node.type === 'suspect' ? 36 + (node.cases || 0) * 2 : 28
  const fontSize = node.type === 'suspect' ? 12 : 14

  const translatedLabel = t(node.label || '')
  const displayLabel = translatedLabel.length > 16 ? translatedLabel.slice(0, 14) + '...' : translatedLabel

  return (
    <g
      className={`graph-node ${isSelected ? 'selected' : ''} ${isHighlighted ? 'highlighted' : ''}`}
      transform={`translate(${node.x}, ${node.y})`}
      onClick={() => onClick(node)}
      onMouseEnter={() => onMouseEnter(node)}
      onMouseLeave={onMouseLeave}
      style={{ cursor: 'pointer' }}
    >
      {/* Glow effect */}
      {isSelected && (
        <circle
          r={size + 8}
          fill="none"
          stroke="var(--color-accent)"
          strokeWidth="2"
          opacity="0.4"
          className="node-glow"
        />
      )}

      {/* Node circle */}
      <circle
        r={size / 2}
        fill={node.type === 'suspect' ? node.gradient || '#0f172a' : getNodeBg(node.type)}
        stroke={isSelected ? 'var(--color-accent)' : 'white'}
        strokeWidth="2"
        className="node-circle"
      />

      {/* Node content */}
      {node.type === 'suspect' ? (
        <text
          textAnchor="middle"
          dominantBaseline="central"
          fill="white"
          fontSize="11"
          fontWeight="700"
          fontFamily="var(--font-sans)"
        >
          {node.id}
        </text>
      ) : (
        <text
          textAnchor="middle"
          dominantBaseline="central"
          fontSize={fontSize}
        >
          {node.icon}
        </text>
      )}

      {/* Label */}
      <text
        y={size / 2 + 14}
        textAnchor="middle"
        fill="var(--text-secondary)"
        fontSize="10"
        fontWeight="500"
        fontFamily="var(--font-sans)"
        className="node-label"
      >
        {displayLabel}
      </text>

      {/* Risk badge for suspects */}
      {node.type === 'suspect' && node.risk && (
        <>
          <circle
            cx={size / 2 - 4}
            cy={-size / 2 + 4}
            r="8"
            fill={node.risk > 70 ? '#ef4444' : node.risk > 40 ? '#f59e0b' : '#10b981'}
          />
          <text
            x={size / 2 - 4}
            y={-size / 2 + 4}
            textAnchor="middle"
            dominantBaseline="central"
            fill="white"
            fontSize="7"
            fontWeight="700"
            fontFamily="var(--font-sans)"
          >
            {node.risk}
          </text>
        </>
      )}
    </g>
  )
}

function getNodeBg(type) {
  switch (type) {
    case 'evidence': return 'rgba(59, 130, 246, 0.15)'
    case 'vehicle': return 'rgba(139, 92, 246, 0.15)'
    case 'phone': return 'rgba(16, 185, 129, 0.15)'
    default: return '#f1f5f9'
  }
}

