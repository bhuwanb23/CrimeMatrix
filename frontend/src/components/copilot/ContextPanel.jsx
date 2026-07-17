import { FileText, Download, BookmarkPlus, Share2, X, Brain, MessageSquare, Clock } from 'lucide-react'

const actions = [
  { icon: FileText, label: 'Generate Report', color: 'text-blue-500 bg-blue-50' },
  { icon: Download, label: 'Export Conversation', color: 'text-emerald-500 bg-emerald-50' },
  { icon: BookmarkPlus, label: 'Save to Case', color: 'text-amber-500 bg-amber-50' },
  { icon: Share2, label: 'Share with Team', color: 'text-purple-500 bg-purple-50' },
]

export default function ContextPanel({ onClose, messages = [], sessionId }) {
  const messageCount = messages.length
  const userMessages = messages.filter(m => m.role === 'user').length
  const assistantMessages = messages.filter(m => m.role === 'assistant').length

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h2 className="text-sm font-semibold text-gray-800">Context</h2>
        <button onClick={onClose} className="w-7 h-7 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors">
          <X size={16} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-5">
        {/* Session Info */}
        <section>
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Session</h3>
          <div className="bg-gray-50 rounded-lg border border-gray-100 p-3 space-y-2">
            <div className="flex items-center gap-2">
              <Brain size={14} className="text-blue-500" />
              <span className="text-sm text-gray-700">CrimeMatrix AI</span>
            </div>
            {sessionId && (
              <div className="flex items-center gap-2">
                <MessageSquare size={14} className="text-gray-400" />
                <span className="text-xs text-gray-500">Session: {sessionId.slice(0, 8)}...</span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <Clock size={14} className="text-gray-400" />
              <span className="text-xs text-gray-500">{messageCount} messages ({userMessages} yours, {assistantMessages} from AI)</span>
            </div>
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

        {/* Recent Topics */}
        {userMessages > 0 && (
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Recent Topics</h3>
            <div className="space-y-1">
              {messages.filter(m => m.role === 'user').slice(-5).reverse().map((m, i) => (
                <div key={i} className="text-xs text-gray-600 bg-gray-50 rounded-lg px-3 py-2 border border-gray-100">
                  {m.content.length > 80 ? m.content.slice(0, 80) + '...' : m.content}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
