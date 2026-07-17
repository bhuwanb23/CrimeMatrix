import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function HeatmapOverlay({ districts }) {
  const { lang } = useLanguage()

  return (
    <g className="heatmap-overlay">
      {districts.map((d) => {
        const radius = 20 + Math.sqrt(d.cases) * 2
        const opacity = d.cases > 100 ? 0.25 : d.cases > 50 ? 0.15 : 0.08
        const color = d.risk === 'high' ? '#ef4444' : d.risk === 'medium' ? '#f59e0b' : '#10b981'

        return (
          <circle
            key={d.id}
            cx={d.x}
            cy={d.y}
            r={radius}
            fill={color}
            opacity={opacity}
            className="heatmap-circle"
          />
        )
      })}
    </g>
  )
}
