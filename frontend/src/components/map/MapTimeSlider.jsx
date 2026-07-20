import { Clock } from 'lucide-react'

const timeOptions = [
  { value: 7, label: '7D' },
  { value: 30, label: '30D' },
  { value: 90, label: '90D' },
  { value: 365, label: '1Y' },
]

export default function MapTimeSlider({ days, onChange }) {
  return (
    <div className="map-time-slider">
      <div className="map-time-header">
        <Clock size={14} />
        <span>Time Range</span>
      </div>
      <div className="map-time-btns">
        {timeOptions.map((opt) => (
          <button
            key={opt.value}
            className={`map-time-btn ${days === opt.value ? 'active' : ''}`}
            onClick={() => onChange(opt.value)}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  )
}
