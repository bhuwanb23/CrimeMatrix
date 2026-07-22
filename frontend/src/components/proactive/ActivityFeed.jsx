import { AlertTriangle, FileText, Camera, Shield, Activity } from 'lucide-react'

const eventIcons = {
  crime_update: FileText,
  evidence_update: Camera,
  case_update: AlertTriangle,
  investigation: Shield,
}

const eventColors = {
  crime_update: '#ef4444',
  evidence_update: '#3b82f6',
  case_update: '#f59e0b',
  investigation: '#10b981',
}

export default function ActivityFeed({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <Activity size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Live Activity Feed</h3>
        </div>
        <div className="py-8 text-center text-xs text-slate-400">
          <Activity size={24} className="mx-auto mb-2 text-slate-200" />
          <p>No recent activity</p>
          <p>Events will appear here as new data comes in</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity size={14} className="text-amber-500" />
          <h3 className="text-sm font-semibold text-slate-900">Live Activity Feed</h3>
        </div>
        <span className="text-[10px] text-slate-400">{events.length} events</span>
      </div>
      <div className="divide-y divide-slate-50 max-h-96 overflow-y-auto">
        {events.map((event, i) => {
          const Icon = eventIcons[event.event_type] || FileText
          const color = eventColors[event.event_type] || '#64748b'
          return (
            <div key={event.id || i} className="px-4 py-3 hover:bg-slate-50 transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ background: `${color}15` }}>
                  <Icon size={14} style={{ color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-900 capitalize">{event.event_type?.replace('_', ' ')}</span>
                    <span className="text-[10px] text-slate-400">{event.created_at ? new Date(event.created_at).toLocaleTimeString() : ''}</span>
                  </div>
                  <p className="text-[10px] text-slate-500">
                    {event.entity_type ? `${event.entity_type} #${event.entity_id}` : 'System event'}
                    {event.status && ` • ${event.status}`}
                  </p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
