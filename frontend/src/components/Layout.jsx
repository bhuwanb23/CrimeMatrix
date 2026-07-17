import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function Layout() {
  const { lang } = useLanguage()
  const [rightPanelOpen, setRightPanelOpen] = useState(true)

  return (
    <div className="layout">
      <Header
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen(!rightPanelOpen)}
      />

      <div className="layout-body">
        <Sidebar />

        <main className="layout-content">
          <Outlet />
        </main>

        <RightPanel isOpen={rightPanelOpen} />
      </div>
    </div>
  )
}
