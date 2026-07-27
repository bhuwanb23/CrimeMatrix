import { useEffect, useLayoutEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { useLanguage } from '../../context/LanguageContext'
import { useOnboarding } from '../../context/OnboardingContext'
import { TOUR_STEPS } from './tourSteps'

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

  useLayoutEffect(() => {
    setRect(measureTarget(step.target))
    onStepChange?.(step)
    const timer = window.setTimeout(() => setRect(measureTarget(step.target)), 80)
    return () => window.clearTimeout(timer)
  }, [index, onStepChange, step])

  useEffect(() => {
    function onResize() {
      setRect(measureTarget(step.target))
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
      <button type="button" className="onboarding-tour-mask" aria-label={t('Skip tour')} onClick={skip} />
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
