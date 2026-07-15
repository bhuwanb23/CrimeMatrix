import { useState } from 'react'
import { FileText, Camera, Clock, GitBranch, Link, Bot } from 'lucide-react'
import NotesTab from './NotesTab'
import EvidenceTab from './EvidenceTab'
import TimelineTab from './TimelineTab'
import ReasoningTab from './ReasoningTab'
import RelatedTab from './RelatedTab'
import AITab from './AITab'

const tabs = [
  { id: 'notes', label: 'Notes', icon: FileText },
  { id: 'evidence', label: 'Evidence', icon: Camera },
  { id: 'timeline', label: 'Timeline', icon: Clock },
  { id: 'reasoning', label: 'Reasoning', icon: GitBranch },
  { id: 'related', label: 'Related', icon: Link },
  { id: 'ai', label: 'AI', icon: Bot },
]

export default function WorkspacePanel({ investigation }) {
  const [activeTab, setActiveTab] = useState('notes')

  if (!investigation) {
    return (
      <div className="workspace-empty">
        <div className="workspace-empty-icon">🔍</div>
        <h3>Select an Investigation</h3>
        <p>Choose a case from the list to start working</p>
      </div>
    )
  }

  return (
    <div className="workspace-panel">
      {/* Header */}
      <div className="workspace-header">
        <div className="workspace-header-top">
          <span className="workspace-case-id">{investigation.caseId}</span>
          <span className={`status-badge ${investigation.status}`}>{investigation.status}</span>
          <span className={`workspace-priority priority-${investigation.priority.toLowerCase()}`}>
            {investigation.priority}
          </span>
        </div>
        <h2 className="workspace-title">{investigation.title}</h2>
        <div className="workspace-meta">
          <span>{investigation.officer}</span>
          <span>•</span>
          <span>{investigation.district}</span>
          <span>•</span>
          <span>{investigation.startDate}</span>
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
      <div className="workspace-content">
        {activeTab === 'notes' && (
          <NotesTab
            notes={investigation.notes}
            onUpdateNotes={(notes) => { /* would update state */ }}
          />
        )}
        {activeTab === 'evidence' && <EvidenceTab evidence={investigation.evidence} />}
        {activeTab === 'timeline' && <TimelineTab timeline={investigation.timeline} />}
        {activeTab === 'reasoning' && <ReasoningTab reasoning={investigation.reasoning} />}
        {activeTab === 'related' && <RelatedTab relatedCases={investigation.relatedCases} />}
        {activeTab === 'ai' && (
          <AITab
            aiInsights={investigation.aiInsights}
            suggestions={investigation.suggestions}
          />
        )}
      </div>

      {/* AI Suggestions Bar */}
      {investigation.suggestions.length > 0 && (
        <div className="workspace-ai-bar">
          <div className="ai-bar-icon">🤖</div>
          <p className="ai-bar-text">{investigation.suggestions[0]}</p>
        </div>
      )}
    </div>
  )
}
