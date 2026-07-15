import { useState } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'

export default function Layout({ children, onNavigate, currentPage }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="layout">
      <Header
        sidebarOpen={sidebarOpen}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />

      <div className="layout-body">
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          onNavigate={onNavigate}
          currentPage={currentPage}
        />

        <main className="layout-content">
          {children}
        </main>

        <RightPanel />
      </div>
    </div>
  )
}
