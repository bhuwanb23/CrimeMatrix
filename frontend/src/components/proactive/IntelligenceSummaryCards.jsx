import { Activity, Clock, CheckCircle, Bell } from 'lucide-react'

export default function IntelligenceSummaryCards({ stats }) {
  if (!stats) return null

  const cards = [
    { label: 'Total Events', value: stats.total_events || 0, icon: Activity, color: 'text-blue-500', bg: 'bg-blue-50' },
    { label: 'Processed', value: stats.processed || 0, icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50' },
    { label: 'Pending', value: stats.pending || 0, icon: Clock, color: 'text-amber-500', bg: 'bg-amber-50' },
    { label: 'In Queue', value: stats.queued || 0, icon: Bell, color: 'text-purple-500', bg: 'bg-purple-50' },
  ]

  return (
    <div className="grid grid-cols-4 gap-3">
      {cards.map((card, i) => (
        <div key={i} className={`${card.bg} border border-slate-200 rounded-xl p-4`}>
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${card.color}`}>
              <card.icon size={18} />
            </div>
            <div>
              <span className="block text-2xl font-bold text-slate-900">{card.value}</span>
              <span className="text-[10px] font-semibold text-slate-400 uppercase">{card.label}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
