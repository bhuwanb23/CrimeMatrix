import { useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'
import useMediaQuery from '../hooks/useMediaQuery'

export default function Layout() {
  const isMobile = useMediaQuery('(max-width: 1023px)')
  const [rightPanelOpen, setRightPanelOpen] = useState(() => {
    if (typeof window === 'undefined') return true
    return !window.matchMedia('(max-width: 1023px)').matches
  })
  const [desktopPanelPreference, setDesktopPanelPreference] = useState(true)

  useEffect(() => {
    if (isMobile) {
      setRightPanelOpen(false)
      return
    }
    setRightPanelOpen(desktopPanelPreference)
  }, [desktopPanelPreference, isMobile])

  function handleToggleRightPanel() {
    setRightPanelOpen((prev) => {
      const next = !prev
      if (!isMobile) setDesktopPanelPreference(next)
      return next
    })
  }

  return (
    <div className="layout">
      <Header
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={handleToggleRightPanel}
      />

      <div className="layout-body">
        <Sidebar />

        <main className="layout-content">
          <Outlet />
        </main>

        {isMobile && rightPanelOpen && (
          <button
            type="button"
            className="right-panel-backdrop"
            aria-label="Close panel"
            onClick={() => setRightPanelOpen(false)}
          />
        )}
        <RightPanel isOpen={rightPanelOpen} />
      </div>
    </div>
  )
}
