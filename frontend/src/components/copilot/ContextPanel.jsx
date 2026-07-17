import { FileText, Download, BookmarkPlus, Share2, X } from 'lucide-react'

const referencedSources = [
  { type: 'fir', title: 'FIR #4521/2026', subtitle: 'Theft — Malleshwaram, Bengaluru' },
  { type: 'suspect', title: 'Ravi Kumar', subtitle: 'Linked to 3 open cases' },
  { type: 'evidence', title: 'CCTV Footage — Main Road', subtitle: 'Captured at 2:15 AM' },
  { type: 'location', title: 'Malleshwaram, Bengaluru', subtitle: 'Crime hotspot zone' },
]

const actions = [
  { icon: FileText, label: 'Generate Report', color: 'text-blue-500 bg-blue-50' },
  { icon: Download, label: 'Export Conversation', color: 'text-emerald-500 bg-emerald-50' },
  { icon: BookmarkPlus, label: 'Save to Case', color: 'text-amber-500 bg-amber-50' },
  { icon: Share2, label: 'Share with Team', color: 'text-purple-500 bg-purple-50' },
]

const relatedCases = [
  { id: 'FIR #4489', title: 'Robbery — Indiranagar', status: 'active' },
  { id: 'FIR #4501', title: 'Theft — Koramangala', status: 'pending' },
  { id: 'FIR #4515', title: 'Cyber fraud — Electronic City', status: 'active' },
]

const TYPE_COLORS = {
  fir: 'bg-blue-100 text-blue-600',
  suspect: 'bg-amber-100 text-amber-600',
  evidence: 'bg-emerald-100 text-emerald-600',
  location: 'bg-purple-100 text-purple-600',
}

export default function ContextPanel({ onClose }) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h2 className="text-sm font-semibold text-gray-800">Context</h2>
        <button onClick={onClose} className="w-7 h-7 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors">
          <X size={16} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-5">
        {/* Referenced Sources */}
        <section>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Referenced Sources</h3>
          <div className="space-y-2">
            {referencedSources.map((src, i) => (
              <div key={i} className="flex items-start gap-3 p-2.5 rounded-lg bg-gray-50 border border-gray-100">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0 ${TYPE_COLORS[src.type] || 'bg-gray-100 text-gray-500'}`}>
                  {src.title[0]}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">{src.title}</p>
                  <p className="text-xs text-gray-500 truncate">{src.subtitle}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Actions */}
        <section>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Actions</h3>
          <div className="grid grid-cols-2 gap-2">
            {actions.map((action, i) => (
              <button key={i} className={`flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm font-medium ${action.color} hover:opacity-80 transition-opacity`}>
                <action.icon size={14} />
                <span>{action.label}</span>
              </button>
            ))}
          </div>
        </section>

        {/* Related Cases */}
        <section>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Related Cases</h3>
          <div className="space-y-2">
            {relatedCases.map((c, i) => (
              <div key={i} className="p-2.5 rounded-lg bg-gray-50 border border-gray-100">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-mono text-gray-500">{c.id}</span>
                  <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${
                    c.status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                  }`}>{c.status}</span>
                </div>
                <p className="text-sm text-gray-700">{c.title}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
