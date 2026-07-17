import { useState } from 'react'
import { Send, Paperclip, Mic, ChevronDown } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

const sources = ['All Sources', 'FIR Database', 'Suspects', 'Evidence', 'Stations']

// Mapping of static source values to localization keys
const sourceKeys = {
  'All Sources': 'all_sources',
  'FIR Database': 'fir_database',
  'Suspects': 'suspects',
  'Evidence': 'evidence',
  'Stations': 'stations',
}

export default function ChatInput({ onSend }) {
  const { lang } = useLanguage()
  const [value, setValue] = useState('')
  const [source, setSource] = useState('All Sources')
  const [sourceOpen, setSourceOpen] = useState(false)

  const handleSend = () => {
    if (!value.trim()) return
    onSend(value.trim(), source)
    setValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-input-area">
      <div className="chat-input-wrapper">
        <input
          type="text"
          className="chat-input-field"
          placeholder={t('ask_anything_placeholder', lang)}
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
              {t(sourceKeys[source], lang)}
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
                    {t(sourceKeys[s], lang)}
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
