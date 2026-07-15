import { useState } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'

export default function Layout({ children, onNavigate, currentPage }) {
  const [rightPanelOpen, setRightPanelOpen] = useState(true)

  return (
    <div className="layout">
      <Header
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen(!rightPanelOpen)}
      />

      <div className="layout-body">
        <Sidebar onNavigate={onNavigate} currentPage={currentPage} />

        <main className="layout-content">
          {children}
        </main>

        <RightPanel isOpen={rightPanelOpen} />
      </div>
    </div>
  )
}
