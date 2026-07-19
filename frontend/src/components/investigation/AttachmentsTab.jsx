import { useState, useRef } from 'react'
import { Paperclip, Upload, Trash2, FileText, Image, Film, File } from 'lucide-react'
import { uploadAttachment, deleteAttachment } from '../../services/investigations'

const fileTypeIcons = {
  'application/pdf': FileText,
  'image/': Image,
  'video/': Film,
}

function getFileIcon(mimeType) {
  if (!mimeType) return File
  for (const [pattern, Icon] of Object.entries(fileTypeIcons)) {
    if (mimeType.startsWith(pattern)) return Icon
  }
  return File
}

function formatSize(bytes) {
  if (!bytes) return 'Unknown size'
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default function AttachmentsTab({ investigationId, attachments: initialAttachments }) {
  const [attachments, setAttachments] = useState(initialAttachments)
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file || uploading) return
    setUploading(true)
    try {
      const res = await uploadAttachment(investigationId, file)
      const created = res?.data || res
      setAttachments([...attachments, {
        id: created?.id || Date.now(),
        filename: file.name,
        file_size: file.size,
        file_type: file.type,
        created_at: new Date().toISOString(),
      }])
    } catch (err) {
      console.error('Upload failed', err)
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteAttachment(id)
      setAttachments(attachments.filter(a => a.id !== id))
    } catch (err) {
      console.error('Delete failed', err)
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return ''
    try {
      return new Date(dateStr).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
    } catch {
      return dateStr
    }
  }

  return (
    <div className="attachments-tab">
      <input
        ref={fileInputRef}
        type="file"
        style={{ display: 'none' }}
        onChange={handleUpload}
      />

      {attachments.length === 0 ? (
        <div className="similar-empty">
          <Paperclip size={24} className="similar-empty-icon" />
          <p>No attachments yet</p>
          <button
            className="similar-btn similar-btn-primary"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            <Upload size={14} />
            {uploading ? 'Uploading...' : 'Upload File'}
          </button>
        </div>
      ) : (
        <>
          <div className="attachments-list">
            {attachments.map((att) => {
              const Icon = getFileIcon(att.file_type)
              return (
                <div key={att.id} className="attachment-card">
                  <div className="attachment-icon">
                    <Icon size={18} />
                  </div>
                  <div className="attachment-info">
                    <span className="attachment-name">{att.filename}</span>
                    <span className="attachment-meta">
                      {formatSize(att.file_size)} • {formatDate(att.created_at)}
                    </span>
                  </div>
                  <button className="note-delete" onClick={() => handleDelete(att.id)}>
                    <Trash2 size={12} />
                  </button>
                </div>
              )
            })}
          </div>
          <button
            className="similar-btn similar-btn-primary"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            style={{ marginTop: 12 }}
          >
            <Upload size={14} />
            {uploading ? 'Uploading...' : 'Upload File'}
          </button>
        </>
      )}
    </div>
  )
}
