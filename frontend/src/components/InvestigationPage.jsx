import { useState, useEffect } from 'react'
import { ClipboardList } from 'lucide-react'
import CaseListPanel from './investigation/CaseListPanel'
import WorkspacePanel from './investigation/WorkspacePanel'
import ToolsPanel from './investigation/ToolsPanel'
import { listInvestigations, getInvestigation } from '../services/investigations'

export default function InvestigationPage() {
  const [investigations, setInvestigations] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [selectedInvestigation, setSelectedInvestigation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    loadInvestigations()
  }, [])

  useEffect(() => {
    if (selectedId) {
      loadInvestigationDetail(selectedId)
    } else {
      setSelectedInvestigation(null)
    }
  }, [selectedId])

  async function loadInvestigations() {
    setLoading(true)
    try {
      const res = await listInvestigations()
      const data = res?.data || res
      setInvestigations(data?.items || [])
    } catch (e) {
      console.error('Failed to load investigations', e)
    } finally {
      setLoading(false)
    }
  }

  async function loadInvestigationDetail(id) {
    setDetailLoading(true)
    try {
      const res = await getInvestigation(id)
      const data = res?.data || res
      setSelectedInvestigation(data)
    } catch (e) {
      console.error('Failed to load investigation', e)
    } finally {
      setDetailLoading(false)
    }
  }

  function handleCreated(inv) {
    loadInvestigations()
    if (inv?.id) setSelectedId(inv.id)
  }

  return (
    <div className="flex flex-col gap-4 h-[calc(100vh-var(--header-height))]">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 text-white shadow-lg shadow-orange-500/20 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
            <ClipboardList size={20} />
          </div>
          <div>
            <h1 className="text-lg font-bold">Investigation Workspace</h1>
            <p className="text-white/80 text-xs">Command center for active investigations</p>
          </div>
          <div className="ml-auto flex items-center gap-2 text-white/80 text-xs">
            <span>{investigations.length} investigations</span>
            {selectedId && <span className="text-white/60">• Viewing #{selectedId}</span>}
          </div>
        </div>
      </div>
      <div className="investigation-page flex-1 min-h-0">
      <CaseListPanel
        investigations={investigations}
        selectedId={selectedId}
        onSelectCase={setSelectedId}
        loading={loading}
        onRefresh={loadInvestigations}
        onCreated={handleCreated}
      />
      <WorkspacePanel investigation={selectedInvestigation} loading={detailLoading} />
      <ToolsPanel investigation={selectedInvestigation} onRefresh={loadInvestigationDetail} />
      </div>
    </div>
  )
}
