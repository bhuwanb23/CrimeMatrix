import { Plus, ChevronDown, ChevronRight, X, Trash2, Pin, Search } from 'lucide-react'
import { useState } from 'react'

const COLORS = ['bg-blue-100 text-blue-600', 'bg-amber-100 text-amber-600', 'bg-purple-100 text-purple-600',
                'bg-emerald-100 text-emerald-600', 'bg-rose-100 text-rose-600', 'bg-cyan-100 text-cyan-600']

function CollapsibleSection({ title, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="mb-2">
      <button className="w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider hover:bg-gray-50 rounded-lg transition-colors" onClick={() => setOpen(!open)}>
        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        {title}
      </button>
      {open && <div className="px-2">{children}</div>}
    </div>
  )
}

function ChatItem({ item, active, onClick, onPin }) {
  const colorIdx = Math.abs((item.session_id || '').charCodeAt(0) || 0) % COLORS.length
  const initial = (item.title || 'N')[0].toUpperCase()
  return (
    <button className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-150 mb-0.5 group ${active ? 'bg-blue-50 border border-blue-200' : 'hover:bg-gray-50'}`} onClick={onClick}>
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0 ${COLORS[colorIdx]}`}>{initial}</div>
      <span className="text-sm text-gray-700 truncate flex-1">{item.title || 'New Conversation'}</span>
      {item.is_pinned && <Pin size={12} className="text-amber-500 flex-shrink-0" />}
    </button>
  )
}

export default function ChatHistory({ sessions = [], activeChatId, onSelectChat, onNewChat, onDeleteChat, onDeleteAll, onSearch, onClose }) {
  const [searchQuery, setSearchQuery] = useState('')
  const today = new Date().toDateString()

  const filteredSessions = searchQuery
    ? (sessions || []).filter(s => (s.title || '').toLowerCase().includes(searchQuery.toLowerCase()))
    : sessions || []

  const pinned = filteredSessions.filter(s => s.is_pinned)
  const todaySessions = filteredSessions.filter(s => !s.is_pinned && s.created_at && new Date(s.created_at).toDateString() === today)
  const olderSessions = filteredSessions.filter(s => !s.is_pinned && (!s.created_at || new Date(s.created_at).toDateString() !== today))

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h2 className="text-sm font-semibold text-gray-800">Chat History</h2>
        <button onClick={onClose} className="w-7 h-7 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"><X size={16} /></button>
      </div>

      {/* Search */}
      <div className="px-3 pt-3">
        <div className="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2">
          <Search size={14} className="text-gray-400" />
          <input type="text" placeholder="Search conversations..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="flex-1 bg-transparent text-xs text-gray-700 outline-none placeholder-gray-400" />
        </div>
      </div>

      <button onClick={onNewChat} className="mx-3 mt-3 flex items-center justify-center gap-2 px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors">
        <Plus size={16} /> New Chat
      </button>

      <div className="flex-1 overflow-y-auto px-2 py-2">
        {pinned.length > 0 && (
          <CollapsibleSection title="Pinned" defaultOpen={true}>
            {pinned.map((chat) => (<ChatItem key={chat.session_id} item={chat} active={activeChatId === chat.session_id} onClick={() => onSelectChat(chat.session_id)} />))}
          </CollapsibleSection>
        )}
        {todaySessions.length > 0 && (
          <CollapsibleSection title="Today" defaultOpen={true}>
            {todaySessions.map((chat) => (<ChatItem key={chat.session_id} item={chat} active={activeChatId === chat.session_id} onClick={() => onSelectChat(chat.session_id)} />))}
          </CollapsibleSection>
        )}
        {olderSessions.length > 0 && (
          <CollapsibleSection title="Previous" defaultOpen={true}>
            {olderSessions.map((chat) => (<ChatItem key={chat.session_id} item={chat} active={activeChatId === chat.session_id} onClick={() => onSelectChat(chat.session_id)} />))}
          </CollapsibleSection>
        )}
        {filteredSessions.length === 0 && <div className="text-center text-gray-400 text-xs py-8">{searchQuery ? 'No matching conversations' : 'No conversations yet. Start a new chat!'}</div>}
      </div>

      {sessions.length > 0 && (
        <div className="px-3 py-3 border-t border-gray-200">
          <button onClick={onDeleteAll} className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-red-500 hover:bg-red-50 rounded-lg transition-colors border border-red-200">
            <Trash2 size={14} /> Delete All Conversations
          </button>
        </div>
      )}
    </div>
  )
}
