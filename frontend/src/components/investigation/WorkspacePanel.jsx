import { useState, useEffect } from 'react'
import { FileText, Camera, Clock, GitBranch, Link, Bot } from 'lucide-react'
import NotesTab from './NotesTab'
import EvidenceTab from './EvidenceTab'
import TimelineTab from './TimelineTab'
import ReasoningTab from './ReasoningTab'
import RelatedTab from './RelatedTab'
import AITab from './AITab'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateText, translateStatus, translateDistrictName } from '../../utils/translate'

const tabs = [
  { id: 'notes', labelKey: 'notes', icon: FileText },
  { id: 'evidence', labelKey: 'evidence', icon: Camera },
  { id: 'timeline', labelKey: 'timeline', icon: Clock },
  { id: 'reasoning', labelKey: 'reasoning', icon: GitBranch },
  { id: 'related', labelKey: 'related', icon: Link },
  { id: 'ai', labelKey: 'ai_copilot', icon: Bot },
]

export default function WorkspacePanel({ investigation }) {
  const { lang } = useLanguage()
  const [activeTab, setActiveTab] = useState('notes')

  useEffect(() => {
    setActiveTab('notes')
  }, [investigation?.id])

  if (!investigation) {
    return (
      <div className="workspace-empty">
        <div className="workspace-empty-icon">🔍</div>
        <h3>{t('select_investigation', lang)}</h3>
        <p>{t('choose_case_desc', lang)}</p>
      </div>
    )
  }

  // Translate timeline dates month names if match
  const translateDateStr = (date) => {
    const parts = date.split(' ')
    if (parts.length > 0) {
      const month = parts[0]
      const translatedMonth = t(month.toLowerCase(), lang)
      if (translatedMonth !== month.toLowerCase()) {
        return date.replace(month, translatedMonth)
      }
    }
    return date
  }

  return (
    <div className="workspace-panel">
      {/* Header */}
      <div className="workspace-header">
        <div className="workspace-header-top">
          <span className="workspace-case-id">{investigation.caseId}</span>
          <span className={`status-badge ${investigation.status}`}>{t(investigation.status, lang)}</span>
          <span className={`workspace-priority priority-${investigation.priority.toLowerCase()}`}>
            {t(investigation.priority.toLowerCase(), lang)}
          </span>
        </div>
        <h2 className="workspace-title">{translateText(investigation.title, lang)}</h2>
        <div className="workspace-meta">
          <span>{investigation.officer === 'SI Karthik' ? `SI ${t('si_karthik', lang) || 'Karthik'}` : investigation.officer}</span>
          <span>•</span>
          <span>{translateDistrictName(investigation.district, lang)}</span>
          <span>•</span>
          <span>{translateDateStr(investigation.startDate)}</span>
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
            {t(tab.labelKey, lang)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="workspace-content" key={`${investigation.id}-${activeTab}`}>
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
          <p className="ai-bar-text">{translateText(investigation.suggestions[0], lang)}</p>
        </div>
      )}
    </div>
  )
}
