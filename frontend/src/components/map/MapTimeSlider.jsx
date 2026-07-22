import { Clock } from 'lucide-react'

const timeOptions = [
  { value: 7, label: '7D' },
  { value: 30, label: '30D' },
  { value: 90, label: '90D' },
  { value: 365, label: '1Y' },
]

export default function MapTimeSlider({ days, onChange }) {
  return (
    <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
      <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 whitespace-nowrap">
        <Clock size={13} aria-hidden="true" />
        Range
      </span>
      <div className="flex items-center gap-1.5 flex-wrap" role="group" aria-label="Time range">
        {timeOptions.map((opt) => {
          const isActive = days === opt.value
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => onChange(opt.value)}
              aria-pressed={isActive}
              className={`inline-flex items-center justify-center min-w-10 px-2.5 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap cursor-pointer transition-colors focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2 ${
                isActive
                  ? 'bg-amber-500 border-amber-500 text-slate-900'
                  : 'bg-slate-50 border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-800'
              }`}
            >
              {opt.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}
