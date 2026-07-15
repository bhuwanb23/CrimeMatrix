import { edgeColors } from './graphData'

export default function GraphEdge({ edge, sourceNode, targetNode, isHighlighted }) {
  const color = edgeColors[edge.type] || '#94a3b8'
  const strokeWidth = isHighlighted ? 3 : 1.5
  const opacity = isHighlighted ? 1 : 0.4

  // Calculate path
  const dx = targetNode.x - sourceNode.x
  const dy = targetNode.y - sourceNode.y
  const dist = Math.sqrt(dx * dx + dy * dy)

  // Offset for curved edges
  const midX = (sourceNode.x + targetNode.x) / 2
  const midY = (sourceNode.y + targetNode.y) / 2
  const curveOffset = dist * 0.15

  // Perpendicular offset for curve
  const nx = -dy / dist
  const ny = dx / dist
  const cx = midX + nx * curveOffset
  const cy = midY + ny * curveOffset

  const pathD = `M ${sourceNode.x} ${sourceNode.y} Q ${cx} ${cy} ${targetNode.x} ${targetNode.y}`

  return (
    <g className={`graph-edge ${isHighlighted ? 'highlighted' : ''}`}>
      {/* Shadow */}
      {isHighlighted && (
        <path
          d={pathD}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth + 4}
          opacity={0.15}
          strokeLinecap="round"
        />
      )}

      {/* Edge line */}
      <path
        d={pathD}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        opacity={opacity}
        strokeLinecap="round"
        strokeDasharray={edge.type === 'phone' ? '4 4' : 'none'}
        className="edge-path"
      />

      {/* Label */}
      {isHighlighted && edge.label && (
        <text
          x={cx}
          y={cy - 8}
          textAnchor="middle"
          fill={color}
          fontSize="9"
          fontWeight="600"
          fontFamily="var(--font-sans)"
          className="edge-label"
        >
          {edge.label}
        </text>
      )}
    </g>
  )
}
