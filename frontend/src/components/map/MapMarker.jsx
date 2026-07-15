export default function MapMarker({ marker, isSelected, onClick, type = 'district' }) {
  const isDistrict = type === 'district'
  const size = isDistrict ? 8 + Math.sqrt(marker.cases) * 0.5 : 6 + marker.cases * 0.3
  const color = marker.risk === 'high' || marker.severity === 'high' ? '#ef4444'
    : marker.risk === 'medium' || marker.severity === 'medium' ? '#f59e0b'
    : '#10b981'

  return (
    <g
      className={`map-marker ${isSelected ? 'selected' : ''}`}
      transform={`translate(${marker.x}, ${marker.y})`}
      onClick={() => onClick(marker)}
      style={{ cursor: 'pointer' }}
    >
      {/* Pulse ring for high severity */}
      {(marker.risk === 'high' || marker.severity === 'high') && (
        <circle r={size + 8} fill="none" stroke={color} strokeWidth="1" opacity="0.3" className="marker-pulse" />
      )}

      {/* Main circle */}
      <circle r={size} fill={color} opacity="0.8" className="marker-circle" />

      {/* Inner dot */}
      <circle r={3} fill="white" />

      {/* Label */}
      {isDistrict && (
        <text
          y={size + 14}
          textAnchor="middle"
          fill="var(--text-secondary)"
          fontSize="10"
          fontWeight="600"
          fontFamily="var(--font-sans)"
          className="marker-label"
        >
          {marker.name}
        </text>
      )}

      {isDistrict && (
        <text
          y={size + 26}
          textAnchor="middle"
          fill="var(--text-muted)"
          fontSize="9"
          fontFamily="var(--font-sans)"
        >
          {marker.cases} cases
        </text>
      )}
    </g>
  )
}
