import { Bell, CheckCircle, AlertTriangle } from 'lucide-react'

export default function NotificationCenter({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <Bell size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Notifications</h3>
        </div>
        <div className="py-8 text-center text-xs text-slate-400">
          <Bell size={24} className="mx-auto mb-2 text-slate-200" />
          <p>No notifications</p>
        </div>
      </div>
    )
  }

  const pending = events.filter(e => e.status === 'pending')
  const processed = events.filter(e => e.status === 'processed')

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Notifications</h3>
        </div>
        {pending.length > 0 && (
          <span className="text-[10px] font-bold px-2 py-0.5 bg-red-100 text-red-600 rounded-full">
            {pending.length} new
          </span>
        )}
      </div>
      <div className="divide-y divide-slate-50 max-h-64 overflow-y-auto">
        {pending.length > 0 && pending.map((event, i) => (
          <div key={event.id || i} className="px-4 py-3 bg-amber-50/50">
            <div className="flex items-center gap-2">
              <AlertTriangle size={12} className="text-amber-500" />
              <span className="text-xs font-semibold text-slate-900 capitalize">{event.event_type?.replace('_', ' ')}</span>
            </div>
            <p className="text-[10px] text-slate-500 mt-1">Needs attention</p>
          </div>
        ))}
        {processed.length > 0 && processed.slice(0, 5).map((event, i) => (
          <div key={event.id || i} className="px-4 py-2">
            <div className="flex items-center gap-2">
              <CheckCircle size={12} className="text-green-500" />
              <span className="text-xs text-slate-600 capitalize">{event.event_type?.replace('_', ' ')}</span>
            </div>
          </div>
        ))}
        {pending.length === 0 && processed.length === 0 && (
          <div className="py-8 text-center text-xs text-slate-400">
            <p>No notifications</p>
          </div>
        )}
      </div>
    </div>
  )
}
