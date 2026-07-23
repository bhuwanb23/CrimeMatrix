import { useState, useEffect, useRef } from 'react'
import { Search, X, BookmarkPlus } from 'lucide-react'
import { getSuggestions } from '../../services/search'
import { useLanguage } from '../../context/LanguageContext'


export default function SearchBar({ value, onChange, onSearch, onSave }) {
  const { t } = useLanguage()
  const [focused, setFocused] = useState(false)
  const [show{t('Suggestions')}, setShow{t('Suggestions')}] = useState(false)
  const [suggestions, set{t('Suggestions')}] = useState([])
  const debounceRef = useRef(null)

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (value && value.length >= 2) {
      debounceRef.current = setTimeout(async () => {
        try {
          const result = await getSuggestions(value)
          set{t('Suggestions')}(result.data || [])
        } catch {
        }
      }, 300)
    } else {
      set{t('Suggestions')}([])
    }
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current) }
  }, [value])

  const handleFocus = () => {
    setFocused(true)
    if (!value) setShow{t('Suggestions')}(true)
  }

  const handleBlur = () => {
    setFocused(false)
    setTimeout(() => setShow{t('Suggestions')}(false), 200)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      setShow{t('Suggestions')}(false)
      onSearch(value)
    }
  }

  return (
    <div className="relative">
      <div className={`flex items-center gap-3 bg-white rounded-xl border px-4 py-3 transition-all ${focused ? 'border-blue-400 shadow-md' : 'border-gray-200'}`}>
        <Search size={18} className="text-gray-400 flex-shrink-0" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          placeholder={t('Search crimes, suspects, FIRs, evidence...')}
          className="flex-1 outline-none text-sm text-gray-800 placeholder-gray-400"
        />
        {value && (
          <button onClick={() => { onChange(''); set{t('Suggestions')}([]) }} className="p-1 hover:bg-gray-100 rounded">
            <X size={14} className="text-gray-400" />
          </button>
        )}
        <button onClick={() => onSave(value)} className="p-1 hover:bg-gray-100 rounded" title={t('Save search')}>
          <BookmarkPlus size={14} className="text-gray-400" />
        </button>
      </div>

      {show{t('Suggestions')} && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-60 overflow-y-auto">
          {suggestions.map((s, i) => (
            <button key={i} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2" onClick={() => { onChange(s); onSearch(s); setShow{t('Suggestions')}(false) }}>
              <Search size={12} className="text-gray-400" />
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
