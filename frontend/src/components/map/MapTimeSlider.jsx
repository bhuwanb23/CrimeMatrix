import { Clock } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

const timeOptions = [
  { value: 7, label: '7D' },
  { value: 30, label: '30D' },
  { value: 90, label: '90D' },
  { value: 365, label: '1Y' },
]

export default function MapTimeSlider({ days, onChange }) {
  const { t } = useLanguage()
  return (
    <div className="flex items-center gap-2 min-w-0 max-lg:w-full max-lg:flex-wrap">
      <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-[var(--text-muted)] whitespace-nowrap">
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
                  ? 'bg-amber-500 border-amber-500 text-[var(--text-primary)]'
                  : 'bg-[var(--bg-muted)] border-[var(--border)] text-[var(--text-muted)] hover:border-[var(--border-strong)] hover:text-[var(--text-primary)]'
              }`}
            >
              {t(opt.label)}
            </button>
          )
        })}
      </div>
    </div>
  )
}
