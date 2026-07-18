import { useState, useEffect, useCallback } from 'react'
import { Send, Paperclip, Mic, MicOff, ChevronDown, Volume2, VolumeX } from 'lucide-react'
import { startListening, stopListening, isSTTSupported } from '../../services/voice'

const sources = ['All Sources', 'FIR Database', 'Suspects', 'Evidence', 'Stations']
const languages = [
  { code: 'en', label: 'English' },
  { code: 'kn', label: 'Kannada' },
  { code: 'hi', label: 'Hindi' },
]

const suggestedQueries = [
  "Show all theft cases in Bengaluru",
  "Find suspects with high risk score",
  "Recent crimes in the last 7 days",
  "List open cases with high priority",
]

export default function ChatInput({ onSend, voiceEnabled = false, onVoiceToggle, language = 'en', onLanguageChange }) {
  const [value, setValue] = useState('')
  const [source, setSource] = useState('All Sources')
  const [sourceOpen, setSourceOpen] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const [isRecording, setIsRecording] = useState(false)
  const [langOpen, setLangOpen] = useState(false)

  const handleSend = useCallback(() => {
    if (!value.trim()) return
    onSend(value.trim(), source)
    setValue('')
    setShowSuggestions(false)
  }, [value, source, onSend])

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

  const toggleRecording = () => {
    if (isRecording) {
      stopListening()
      setIsRecording(false)
    } else {
      if (!isSTTSupported()) {
        alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.')
        return
      }
      setIsRecording(true)
      startListening(
        language,
        (transcript, isFinal) => {
          setValue(transcript)
          if (isFinal) {
            setIsRecording(false)
            setTimeout(() => {
              onSend(transcript, source)
              setValue('')
              setShowSuggestions(false)
            }, 300)
          }
        },
        () => setIsRecording(false),
        (error) => {
          console.error('STT error:', error)
          setIsRecording(false)
        }
      )
    }
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

      {/* Voice indicator */}
      {isRecording && (
        <div className="flex items-center justify-center gap-2 pb-2">
          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
          <span className="text-xs text-red-500 font-medium">Listening... Speak now</span>
          <div className="flex gap-0.5">
            {[1,2,3,4,5].map(i => (
              <div key={i} className="w-0.5 bg-red-400 rounded-full animate-pulse"
                style={{ height: `${8 + Math.random() * 12}px`, animationDelay: `${i * 0.1}s` }} />
            ))}
          </div>
        </div>
      )}

      {/* Input area */}
      <div className="flex items-center gap-2 bg-gray-100 rounded-2xl px-4 py-2">
        <input
          type="text"
          className="flex-1 bg-transparent text-sm text-gray-800 placeholder-gray-400 outline-none"
          placeholder={isRecording ? "Listening..." : "Ask me anything... (e.g., 'Show theft cases in Bengaluru')"}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isRecording}
        />

        {/* Language selector */}
        <div className="relative">
          <button
            onClick={() => setLangOpen(!langOpen)}
            className="flex items-center gap-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            {languages.find(l => l.code === language)?.label || 'EN'}
            <ChevronDown size={12} />
          </button>
          {langOpen && (
            <div className="absolute bottom-full right-0 mb-1 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50 min-w-[100px]">
              {languages.map((l) => (
                <button
                  key={l.code}
                  className={`w-full text-left px-3 py-1.5 text-xs hover:bg-gray-100 ${l.code === language ? 'text-blue-600 font-medium' : 'text-gray-700'}`}
                  onClick={() => { setLanguage(l.code); setLangOpen(false) }}
                >
                  {l.label}
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="w-px h-5 bg-gray-300" />

        {/* Mic button */}
        <button
          onClick={toggleRecording}
          className={`p-1.5 rounded-md transition-all duration-150 ${
            isRecording
              ? 'bg-red-100 text-red-600 animate-pulse'
              : 'text-gray-400 hover:text-gray-600 hover:bg-gray-200'
          }`}
          aria-label={isRecording ? 'Stop recording' : 'Start voice input'}
          title={isRecording ? 'Stop recording' : `Voice input (${languages.find(l => l.code === language)?.label})`}
        >
          {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
        </button>

        <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-md transition-colors" aria-label="Attach file">
          <Paperclip size={16} />
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
