import { useState, useEffect, useRef } from 'react'
import { Search, Mic, X, Clock, BookmarkPlus } from 'lucide-react'

const recentSearches = [
  'Theft cases in Bengaluru',
  'FIR #4521',
  'Ravi Kumar suspect',
  'Cyber fraud Electronic City',
]

import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function SearchBar({ value, onChange, onSearch, onSave }) {
  const { lang } = useLanguage()
  const [focused, setFocused] = useState(false)
  const [showRecent, setShowRecent] = useState(false)
  const debounceRef = useRef(null)

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (value) {
      debounceRef.current = setTimeout(() => {
        onSearch(value)
      }, 300)
    }
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [value, onSearch])

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
    onSearch('')
    setShowRecent(false)
  }

  return (
    <div className="search-bar-container">
      <div className={`search-bar ${focused ? 'focused' : ''}`}>
        <Search size={20} strokeWidth={1.8} className="search-bar-icon" />
        <input
          type="text"
          className="search-bar-input"
          placeholder={t('search_cases_placeholder', lang)}
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
        {value && (
          <button
            className="search-bar-save"
            onClick={() => onSave(value)}
            aria-label={t('save_search', lang)}
          >
            <BookmarkPlus size={16} strokeWidth={1.8} />
          </button>
        )}
        <button className="search-bar-voice" aria-label={t('voice_search', lang)}>
          <Mic size={16} strokeWidth={1.8} />
        </button>
        <button className="search-bar-btn" onClick={() => onSearch(value)}>
          {t('search', lang)}
        </button>
      </div>

      {showRecent && !value && (
        <div className="search-recent">
          <div className="search-recent-header">
            <Clock size={14} />
            <span>{t('recent_searches', lang)}</span>
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
