import { useState, useEffect } from 'react'
import { FileText, Camera, Clock, GitBranch, Link, Bot, Paperclip, Bookmark } from 'lucide-react'
import NotesTab from './NotesTab'
import EvidenceTab from './EvidenceTab'
import TimelineTab from './TimelineTab'
import ReasoningTab from './ReasoningTab'
import RelatedTab from './RelatedTab'
import AITab from './AITab'
import InvestigationAI from './InvestigationAI'
import AttachmentsTab from './AttachmentsTab'
import BookmarksTab from './BookmarksTab'
import { getSimilarCases } from '../../services/similarCases'

const tabs = [
  { id: 'notes', label: 'Notes', icon: FileText },
  { id: 'evidence', label: 'Evidence', icon: Camera },
  { id: 'timeline', label: 'Timeline', icon: Clock },
  { id: 'reasoning', label: 'Reasoning', icon: GitBranch },
  { id: 'related', label: 'Related', icon: Link },
  { id: 'attachments', label: 'Files', icon: Paperclip },
  { id: 'bookmarks', label: 'Bookmarks', icon: Bookmark },
  { id: 'ai', label: 'AI', icon: Bot },
]

export default function WorkspacePanel({ investigation, loading }) {
  const [activeTab, setActiveTab] = useState('notes')
  const [relatedCases, setRelatedCases] = useState([])

  useEffect(() => {
    setActiveTab('notes')
  }, [investigation?.id])

  useEffect(() => {
    if (investigation?.case_id && activeTab === 'related') {
      loadRelated()
    }
  }, [investigation?.case_id, activeTab])

  async function loadRelated() {
    try {
      const res = await getSimilarCases(investigation.case_id, 5)
      const data = res?.data || res
      setRelatedCases(data?.similar_cases || [])
    } catch (e) {
      setRelatedCases([])
    }
  }

  if (loading) {
    return (
      <div className="workspace-empty">
        <div className="similar-spinner" />
        <p>Loading investigation...</p>
      </div>
    )
  }

  if (!investigation) {
    return (
      <div className="workspace-empty">
        <div className="workspace-empty-icon">🔍</div>
        <h3>Select an Investigation</h3>
        <p>Choose a case from the list to start working</p>
      </div>
    )
  }

  const caseId = investigation.case_id
  const invId = investigation.id

  return (
    <div className="workspace-panel">
      {/* Header */}
      <div className="workspace-header">
        <div className="workspace-header-top">
          <span className="workspace-case-id">INV-{String(invId).padStart(3, '0')}</span>
          <span className={`status-badge ${investigation.status}`}>{investigation.status}</span>
          <span className={`workspace-priority priority-${(investigation.priority || 'medium').toLowerCase()}`}>
            {investigation.priority}
          </span>
        </div>
        <h2 className="workspace-title">{investigation.title}</h2>
        <div className="workspace-meta">
          {investigation.district && <span>{investigation.district}</span>}
          {investigation.district && <span>•</span>}
          {investigation.progress !== undefined && <span>{investigation.progress}% complete</span>}
        </div>
      </div>

      {/* Tab Bar */}
      <div className="workspace-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`workspace-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <tab.icon size={14} />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="workspace-content" key={`${invId}-${activeTab}`}>
        {activeTab === 'notes' && (
          <NotesTab investigationId={invId} notes={investigation.notes || []} />
        )}
        {activeTab === 'evidence' && (
          <EvidenceTab caseId={caseId} evidence={investigation.evidence || []} />
        )}
        {activeTab === 'timeline' && (
          <TimelineTab investigationId={invId} timeline={investigation.timeline || []} />
        )}
        {activeTab === 'reasoning' && <ReasoningTab reasoning={[]} />}
        {activeTab === 'related' && <RelatedTab caseId={caseId} relatedCases={relatedCases} />}
        {activeTab === 'attachments' && (
          <AttachmentsTab investigationId={invId} attachments={investigation.attachments || []} />
        )}
        {activeTab === 'bookmarks' && (
          <BookmarksTab investigationId={invId} bookmarks={investigation.status_logs || []} />
        )}
        {activeTab === 'ai' && (
          <InvestigationAI investigationId={invId} investigation={investigation} />
        )}
      </div>
    </div>
  )
}
