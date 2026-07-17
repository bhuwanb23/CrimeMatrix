import { useState } from 'react'
import { Send, Paperclip, Mic, ChevronDown } from 'lucide-react'

const sources = ['All Sources', 'FIR Database', 'Suspects', 'Evidence', 'Stations']

const suggestedQueries = [
  "Show all theft cases in Bengaluru",
  "Find suspects with high risk score",
  "Recent crimes in the last 7 days",
  "List open cases with high priority",
]

export default function ChatInput({ onSend }) {
  const [value, setValue] = useState('')
  const [source, setSource] = useState('All Sources')
  const [sourceOpen, setSourceOpen] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)

  const handleSend = () => {
    if (!value.trim()) return
    onSend(value.trim(), source)
    setValue('')
    setShowSuggestions(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestionClick = (query) => {
    onSend(query, source)
    setShowSuggestions(false)
  }

  return (
    <div className="border-t border-gray-200 bg-white px-6 py-3 flex-shrink-0">
      {/* Suggestion chips */}
      {showSuggestions && (
        <div className="flex gap-2 pb-3 justify-center flex-wrap">
          {suggestedQueries.map((q, i) => (
            <button
              key={i}
              onClick={() => handleSuggestionClick(q)}
              className="px-4 py-1.5 rounded-full border border-gray-200 bg-gray-50 text-gray-600 text-xs hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-150 whitespace-nowrap"
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Input area */}
      <div className="flex items-center gap-2 bg-gray-100 rounded-2xl px-4 py-2">
        <input
          type="text"
          className="flex-1 bg-transparent text-sm text-gray-800 placeholder-gray-400 outline-none"
          placeholder="Ask me anything... (e.g., 'Show theft cases in Bengaluru')"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        {/* Source dropdown */}
        <div className="relative">
          <button
            onClick={() => setSourceOpen(!sourceOpen)}
            className="flex items-center gap-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            {source}
            <ChevronDown size={12} />
          </button>
          {sourceOpen && (
            <div className="absolute bottom-full right-0 mb-1 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50 min-w-[140px]">
              {sources.map((s) => (
                <button
                  key={s}
                  className={`w-full text-left px-3 py-1.5 text-xs hover:bg-gray-100 ${s === source ? 'text-blue-600 font-medium' : 'text-gray-700'}`}
                  onClick={() => { setSource(s); setSourceOpen(false) }}
                >
                  {s}
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="w-px h-5 bg-gray-300" />

        <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-md transition-colors" aria-label="Attach file">
          <Paperclip size={16} />
        </button>
        <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-md transition-colors" aria-label="Voice input">
          <Mic size={16} />
        </button>
        <button
          onClick={handleSend}
          disabled={!value.trim()}
          className={`p-2 rounded-xl transition-all duration-150 ${
            value.trim()
              ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-sm'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
          aria-label="Send message"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  )
}
