import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [rightPanelOpen, setRightPanelOpen] = useState(true)

  // On smaller screens, right panel starts closed
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1280px)')
    setRightPanelOpen(mq.matches)
    const handler = (e) => setRightPanelOpen(e.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [])

  return (
    <div className="layout">
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      <div className={`layout-main ${sidebarOpen ? '' : 'sidebar-closed'}`}>
        <Header
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          rightPanelOpen={rightPanelOpen}
          onToggleRightPanel={() => setRightPanelOpen(!rightPanelOpen)}
        />

        <main className="layout-content">
          {children}
        </main>
      </div>

      <RightPanel
        isOpen={rightPanelOpen}
        onClose={() => setRightPanelOpen(false)}
      />
    </div>
  )
}
