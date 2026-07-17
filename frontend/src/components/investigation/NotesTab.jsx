import { useState } from 'react'
import { Plus, Send, User } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText } from '../../utils/translate'

export default function NotesTab({ notes: initialNotes, onUpdateNotes }) {
  const { lang } = useLanguage()
  const [notes, setNotes] = useState(initialNotes)
  const [newNote, setNewNote] = useState('')

  const handleAddNote = () => {
    if (!newNote.trim()) return
    const note = {
      id: Date.now(),
      text: newNote.trim(),
      time: 'Just now',
      author: 'SI Karthik',
    }
    const updated = [note, ...notes]
    setNotes(updated)
    onUpdateNotes(updated)
    setNewNote('')
  }

  // Helper to translate author name if defined in dictionary
  const translateAuthor = (author) => {
    if (author === 'SI Karthik') return `SI ${t('si_karthik', lang) || 'Karthik'}`
    if (author === 'Inspector Deepak') return `${t('inspector_deepak', lang) || 'Inspector Deepak'}`
    if (author === 'Cyber Cell') return t('cyber_cell', lang) || author
    return author
  }

  // Helper to translate time labels if mock
  const translateTime = (time) => {
    if (time === 'Just now') return t('just_now', lang)
    // Example: Jul 15, 10:30 AM. Can keep as-is or translate month if desired
    return time
  }

  return (
    <div className="notes-tab">
      <div className="notes-input-area">
        <textarea
          className="notes-input"
          placeholder={t('add_note_placeholder', lang)}
          value={newNote}
          onChange={(e) => setNewNote(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              handleAddNote()
            }
          }}
          rows={2}
        />
        <button
          className="notes-submit"
          onClick={handleAddNote}
          disabled={!newNote.trim()}
        >
          <Send size={14} />
          {t('add_note', lang)}
        </button>
      </div>

      <div className="notes-list">
        {notes.map((note) => (
          <div key={note.id} className="note-card">
            <div className="note-header">
              <div className="note-author">
                <User size={12} />
                {translateAuthor(note.author)}
              </div>
              <span className="note-time">{translateTime(note.time)}</span>
            </div>
            <p className="note-text">{translateText(note.text, lang)}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
