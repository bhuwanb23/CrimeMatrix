import { useLanguage } from '../context/LanguageContext'
import { useState, useEffect } from 'react'
import { ClipboardList, PanelRightClose, PanelRightOpen } from 'lucide-react'
import CaseListPanel from './investigation/CaseListPanel'
import WorkspacePanel from './investigation/WorkspacePanel'
import ToolsPanel from './investigation/ToolsPanel'
import { listInvestigations, getInvestigation } from '../services/investigations'
import useMediaQuery from '../hooks/useMediaQuery'

export default function InvestigationPage() {
  const { t } = useLanguage()
  const isMobile = useMediaQuery('(max-width: 1023px)')
  const [investigations, setInvestigations] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [selectedInvestigation, setSelectedInvestigation] = useState(null)
  const [toolsPanelOpen, setToolsPanelOpen] = useState(() => {
    if (typeof window === 'undefined') return true
    return !window.matchMedia('(max-width: 1023px)').matches
  })
  const [toolsPanelDesktopPreference, setToolsPanelDesktopPreference] = useState(true)
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

  useEffect(() => {
    if (isMobile) {
      setToolsPanelOpen(false)
      return
    }
    setToolsPanelOpen(toolsPanelDesktopPreference)
  }, [isMobile, toolsPanelDesktopPreference])

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

  function handleToggleToolsPanel() {
    setToolsPanelOpen((prev) => {
      const next = !prev
      if (!isMobile) setToolsPanelDesktopPreference(next)
      return next
    })
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
            <h1 className="text-lg font-bold">{t('Investigation Workspace')}</h1>
            <p className="text-white/80 text-xs">{t('Command center for active investigations')}</p>
          </div>
          <div className="ml-auto flex items-center gap-2 text-white/80 text-xs">
            <span>{investigations.length} {t('investigations')}</span>
            {selectedId && <span className="text-white/60">• {t('Viewing')} #{selectedId}</span>}
            <button
              type="button"
              onClick={handleToggleToolsPanel}
              disabled={!selectedInvestigation}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-white/30 bg-white/15 text-white text-xs font-medium hover:bg-white/25 disabled:opacity-50"
              aria-label={toolsPanelOpen ? t('Hide panel') : t('Show panel')}
            >
              {toolsPanelOpen ? <PanelRightClose size={14} /> : <PanelRightOpen size={14} />}
              <span>{t('Tools')}</span>
            </button>
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
      {!isMobile && toolsPanelOpen && (
        <ToolsPanel investigation={selectedInvestigation} onRefresh={loadInvestigationDetail} />
      )}
      </div>
      {isMobile && toolsPanelOpen && selectedInvestigation && (
        <>
          <button
            type="button"
            className="page-right-drawer-backdrop"
            aria-label={t('Close tools panel')}
            onClick={() => setToolsPanelOpen(false)}
          />
          <div className="page-right-drawer page-right-drawer-open">
            <ToolsPanel
              investigation={selectedInvestigation}
              onRefresh={loadInvestigationDetail}
              className="w-full min-w-0 h-full rounded-none border-0 p-4 overflow-y-auto"
            />
          </div>
        </>
      )}
    </div>
  )
}
