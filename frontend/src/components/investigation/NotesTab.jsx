import { useState } from 'react'
import { Plus, Send, User } from 'lucide-react'

export default function NotesTab({ notes: initialNotes, onUpdateNotes }) {
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

  return (
    <div className="notes-tab">
      <div className="notes-input-area">
        <textarea
          className="notes-input"
          placeholder="Add an investigation note..."
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
          Add Note
        </button>
      </div>

      <div className="notes-list">
        {notes.map((note) => (
          <div key={note.id} className="note-card">
            <div className="note-header">
              <div className="note-author">
                <User size={12} />
                {note.author}
              </div>
              <span className="note-time">{note.time}</span>
            </div>
            <p className="note-text">{note.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
