import { useState } from 'react'
import { Send, Paperclip, Mic, ChevronDown } from 'lucide-react'

const sources = ['All Sources', 'FIR Database', 'Suspects', 'Evidence', 'Stations']

const suggestedQueries = [
  "Show all theft cases in Bengaluru",
  "Find suspects with high risk score",
  "Recent crimes in the last 7 days",
  "List open cases with high priority",
  "Show robbery cases in Mysore district",
  "What are the most common crime types?",
  "Find all evidence for case #1",
  "Show suspects linked to recent cases",
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
    setValue(query)
    setShowSuggestions(false)
    onSend(query, source)
  }

  return (
    <div className="chat-input-area">
      {showSuggestions && (
        <div className="chat-suggestions-row">
          {suggestedQueries.slice(0, 4).map((q, i) => (
            <button key={i} className="chat-suggestion-chip" onClick={() => handleSuggestionClick(q)}>
              {q}
            </button>
          ))}
        </div>
      )}
      <div className="chat-input-wrapper">
        <input
          type="text"
          className="chat-input-field"
          placeholder="Ask me anything... (e.g., 'Show theft cases in Bengaluru')"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <div className="chat-input-actions">
          <div className="chat-source-dropdown">
            <button
              className="chat-source-btn"
              onClick={() => setSourceOpen(!sourceOpen)}
            >
              {source}
              <ChevronDown size={12} />
            </button>
            {sourceOpen && (
              <div className="chat-source-menu">
                {sources.map((s) => (
                  <button
                    key={s}
                    className={`chat-source-option ${s === source ? 'active' : ''}`}
                    onClick={() => { setSource(s); setSourceOpen(false) }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="chat-input-divider" />

          <button className="chat-input-icon-btn" aria-label="Attach file">
            <Paperclip size={16} strokeWidth={1.8} />
          </button>
          <button className="chat-input-icon-btn" aria-label="Voice input">
            <Mic size={16} strokeWidth={1.8} />
          </button>
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={!value.trim()}
            aria-label="Send message"
          >
            <Send size={16} strokeWidth={1.8} />
          </button>
        </div>
      </div>
    </div>
  )
}
