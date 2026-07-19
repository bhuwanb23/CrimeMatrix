import { useState, useEffect } from 'react'
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
    <div className="investigation-page">
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
  )
}
