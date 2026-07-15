import { useState } from 'react'
import CaseListPanel from './investigation/CaseListPanel'
import WorkspacePanel from './investigation/WorkspacePanel'
import ToolsPanel from './investigation/ToolsPanel'
import { investigations } from './investigation/investigationData'

export default function InvestigationPage() {
  const [selectedId, setSelectedId] = useState(null)

  const selectedInvestigation = investigations.find((inv) => inv.id === selectedId)

  return (
    <div className="investigation-page">
      <CaseListPanel
        investigations={investigations}
        selectedId={selectedId}
        onSelectCase={setSelectedId}
      />
      <WorkspacePanel investigation={selectedInvestigation} />
      <ToolsPanel investigation={selectedInvestigation} />
    </div>
  )
}
