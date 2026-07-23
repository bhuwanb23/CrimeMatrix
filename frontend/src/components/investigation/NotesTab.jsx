import { useLanguage } from '../../context/LanguageContext'
import { useState } from 'react'
import { Send, User, Trash2 } from 'lucide-react'
import { createNote, deleteNote } from '../../services/investigations'

export default function NotesTab({ investigationId, notes: initialNotes }) {
  const { t } = useLanguage()
  const [notes, setNotes] = useState(initialNotes)
  const [newNote, setNewNote] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleAddNote = async () => {
    if (!newNote.trim() || submitting) return
    setSubmitting(true)
    try {
      const res = await createNote({
        investigation_id: investigationId,
        content: newNote.trim(),
      })
      const created = res?.data || res
      const note = {
        id: created?.id || Date.now(),
        content: newNote.trim(),
        author_id: null,
        created_at: new Date().toISOString(),
      }
      setNotes([note, ...notes])
      setNewNote('')
    } catch (e) {
      console.error('Failed to create note', e)
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteNote = async (noteId) => {
    try {
      await deleteNote(noteId)
      setNotes(notes.filter(n => n.id !== noteId))
    } catch (e) {
      console.error('Failed to delete note', e)
    }
  }

  function formatTime(dateStr) {
    if (!dateStr) return 'Just now'
    try {
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    } catch {
      return dateStr
    }
  }

  return (
    <div className="notes-tab">
      <div className="notes-input-area">
        <textarea
          className="notes-input"
          placeholder={t('Add an investigation note...')}
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
          disabled={!newNote.trim() || submitting}
        >
          <Send size={14} />
          {submitting ? t('Adding...') : t('Add Note')}
        </button>
      </div>

      <div className="notes-list">
        {notes.length === 0 ? (
          <div className="similar-empty"><p>{t('No notes yet')}</p></div>
        ) : (
          notes.map((note) => (
            <div key={note.id} className="note-card">
              <div className="note-header">
                <div className="note-author">
                  <User size={12} />
                  {note.author_id ? `Officer #${note.author_id}` : 'You'}
                </div>
                <div className="note-header-right">
                  <span className="note-time">{formatTime(note.created_at)}</span>
                  <button className="note-delete" onClick={() => handleDeleteNote(note.id)}>
                    <Trash2 size={12} />
                  </button>
                </div>
              </div>
              <p className="note-text">{note.content}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
