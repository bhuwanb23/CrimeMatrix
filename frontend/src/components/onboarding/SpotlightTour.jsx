import { useEffect, useLayoutEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { useLanguage } from '../../context/LanguageContext'
import { useOnboarding } from '../../context/OnboardingContext'

export const TOUR_STEPS = [
  {
    id: 'sidebar',
    target: 'sidebar',
    title: 'Navigation sidebar',
    body: 'Jump between Dashboard, Intelligence, Investigations, Search, Stations, and Reports from this rail.',
  },
  {
    id: 'header-nav',
    target: 'header-nav',
    title: 'Quick header links',
    body: 'Open AI Copilot, Analytics, Knowledge Graph, and Alerts without leaving the current page flow.',
  },
  {
    id: 'header-panel-toggle',
    target: 'header-panel-toggle',
    title: 'Activity panel toggle',
    body: 'Show or hide the right panel for live activity and a quick AI chat surface.',
  },
  {
    id: 'right-panel',
    target: 'right-panel',
    title: 'Right panel',
    body: 'Review today\'s overview, recent activity, and ask the AI Copilot short questions in place.',
  },
  {
    id: 'main-content',
    target: 'main-content',
    title: 'Main workspace',
    body: 'This is where each module renders — charts, maps, investigation tools, and reports live here.',
  },
]

function measureTarget(selector) {
  const el = document.querySelector(`[data-tour="${selector}"]`)
  if (!el) return null
  const rect = el.getBoundingClientRect()
  return {
    top: rect.top,
    left: rect.left,
    width: rect.width,
    height: rect.height,
  }
}

export default function SpotlightTour({ onStepChange }) {
  const { t } = useLanguage()
  const { complete, skip } = useOnboarding()
  const [index, setIndex] = useState(0)
  const [rect, setRect] = useState(null)

  const step = TOUR_STEPS[index]
  const isLast = index === TOUR_STEPS.length - 1

  const refreshRect = () => {
    setRect(measureTarget(step.target))
  }

  useLayoutEffect(() => {
    refreshRect()
    onStepChange?.(step)
  }, [index, step.target])

  useEffect(() => {
    function onResize() {
      refreshRect()
    }
    window.addEventListener('resize', onResize)
    window.addEventListener('scroll', onResize, true)
    return () => {
      window.removeEventListener('resize', onResize)
      window.removeEventListener('scroll', onResize, true)
    }
  }, [step.target])

  useEffect(() => {
    function onKey(e) {
      if (e.key === 'Escape') skip()
      else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        if (isLast) complete()
        else setIndex((i) => i + 1)
      } else if (e.key === 'ArrowLeft') {
        setIndex((i) => Math.max(0, i - 1))
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [complete, isLast, skip])

  const tooltipStyle = useMemo(() => {
    if (!rect) {
      return { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }
    }
    const gap = 14
    const tooltipWidth = Math.min(360, window.innerWidth - 32)
    let top = rect.top + rect.height + gap
    let left = rect.left

    if (top + 180 > window.innerHeight) {
      top = Math.max(16, rect.top - gap - 160)
    }
    if (left + tooltipWidth > window.innerWidth - 16) {
      left = window.innerWidth - tooltipWidth - 16
    }
    left = Math.max(16, left)

    return { top, left, width: tooltipWidth }
  }, [rect])

  const highlightStyle = rect
    ? {
        top: Math.max(8, rect.top - 8),
        left: Math.max(8, rect.left - 8),
        width: rect.width + 16,
        height: rect.height + 16,
      }
    : null

  return createPortal(
    <div className="onboarding-tour-root" role="dialog" aria-modal="true" aria-labelledby="onboarding-tour-title">
      <div className="onboarding-tour-mask" onClick={skip} />
      {highlightStyle && (
        <div className="onboarding-spotlight" style={highlightStyle} aria-hidden="true" />
      )}

      <div className="onboarding-tooltip" style={tooltipStyle}>
        <div className="onboarding-tooltip-progress">
          {t('Step')} {index + 1} {t('of')} {TOUR_STEPS.length}
        </div>
        <h3 id="onboarding-tour-title" className="onboarding-tooltip-title">
          {t(step.title)}
        </h3>
        <p className="onboarding-tooltip-body">{t(step.body)}</p>
        <div className="onboarding-tooltip-actions">
          <button type="button" className="onboarding-btn ghost" onClick={skip}>
            {t('Skip tour')}
          </button>
          <div className="onboarding-welcome-actions-right">
            {index > 0 && (
              <button type="button" className="onboarding-btn ghost" onClick={() => setIndex((i) => i - 1)}>
                {t('Back')}
              </button>
            )}
            <button
              type="button"
              className="onboarding-btn primary"
              onClick={() => {
                if (isLast) complete()
                else setIndex((i) => i + 1)
              }}
            >
              {isLast ? t('Finish') : t('Next')}
            </button>
          </div>
        </div>
      </div>
    </div>,
    document.body,
  )
}
