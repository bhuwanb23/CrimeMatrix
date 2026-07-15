import { useState } from 'react'
import { Search, Mic, X, Clock } from 'lucide-react'

const recentSearches = [
  'Theft cases in Bengaluru',
  'FIR #4521',
  'Ravi Kumar suspect',
  'Cyber fraud Electronic City',
]

export default function SearchBar({ value, onChange, onSearch }) {
  const [focused, setFocused] = useState(false)
  const [showRecent, setShowRecent] = useState(false)

  const handleFocus = () => {
    setFocused(true)
    if (!value) setShowRecent(true)
  }

  const handleBlur = () => {
    setFocused(false)
    setTimeout(() => setShowRecent(false), 200)
  }

  const handleSelectRecent = (term) => {
    onChange(term)
    onSearch(term)
    setShowRecent(false)
  }

  const handleClear = () => {
    onChange('')
    setShowRecent(false)
  }

  return (
    <div className="search-bar-container">
      <div className={`search-bar ${focused ? 'focused' : ''}`}>
        <Search size={20} strokeWidth={1.8} className="search-bar-icon" />
        <input
          type="text"
          className="search-bar-input"
          placeholder="Search cases, suspects, FIRs, evidence..."
          value={value}
          onChange={(e) => {
            onChange(e.target.value)
            setShowRecent(false)
          }}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onKeyDown={(e) => e.key === 'Enter' && onSearch(value)}
        />
        {value && (
          <button className="search-bar-clear" onClick={handleClear}>
            <X size={16} strokeWidth={1.8} />
          </button>
        )}
        <button className="search-bar-voice" aria-label="Voice search">
          <Mic size={16} strokeWidth={1.8} />
        </button>
        <button className="search-bar-btn" onClick={() => onSearch(value)}>
          Search
        </button>
      </div>

      {showRecent && !value && (
        <div className="search-recent">
          <div className="search-recent-header">
            <Clock size={14} />
            <span>Recent searches</span>
          </div>
          {recentSearches.map((term, i) => (
            <button
              key={i}
              className="search-recent-item"
              onMouseDown={() => handleSelectRecent(term)}
            >
              <Search size={14} />
              {term}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
