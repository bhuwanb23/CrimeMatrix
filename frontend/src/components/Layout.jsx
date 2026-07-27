import { useCallback, useEffect, useRef, useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import RightPanel from './RightPanel'
import WelcomeIntro from './onboarding/WelcomeIntro'
import SpotlightTour from './onboarding/SpotlightTour'
import useMediaQuery from '../hooks/useMediaQuery'
import { useOnboarding } from '../context/useOnboarding'

export default function Layout() {
  const isMobile = useMediaQuery('(max-width: 1023px)')
  const { shouldShowIntro, shouldShowTour } = useOnboarding()
  const [rightPanelOpen, setRightPanelOpen] = useState(() => {
    if (typeof window === 'undefined') return true
    return !window.matchMedia('(max-width: 1023px)').matches
  })
  const [desktopPanelPreference, setDesktopPanelPreference] = useState(true)
  const panelBeforeTour = useRef(null)

  useEffect(() => {
    if (shouldShowTour) return
    if (isMobile) {
      setRightPanelOpen(false)
      return
    }
    setRightPanelOpen(desktopPanelPreference)
  }, [desktopPanelPreference, isMobile, shouldShowTour])

  function handleToggleRightPanel() {
    setRightPanelOpen((prev) => {
      const next = !prev
      if (!isMobile) setDesktopPanelPreference(next)
      return next
    })
  }

  const handleTourStepChange = useCallback((step) => {
    if (!step) return
    const needsPanel = step.target === 'right-panel' || step.target === 'header-panel-toggle'
    if (!needsPanel) return
    setRightPanelOpen((prev) => {
      if (panelBeforeTour.current === null) {
        panelBeforeTour.current = prev
      }
      return true
    })
  }, [])

  useEffect(() => {
    if (shouldShowTour) return
    if (panelBeforeTour.current === null) return
    const restore = panelBeforeTour.current
    panelBeforeTour.current = null
    if (isMobile) {
      setRightPanelOpen(false)
    } else {
      setRightPanelOpen(restore)
      setDesktopPanelPreference(restore)
    }
  }, [isMobile, shouldShowTour])

  return (
    <div className="layout">
      <Header
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={handleToggleRightPanel}
      />

      <div className="layout-body">
        <Sidebar />

        <main className="layout-content" data-tour="main-content">
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

      {shouldShowIntro && <WelcomeIntro />}
      {shouldShowTour && <SpotlightTour onStepChange={handleTourStepChange} />}
    </div>
  )
}
