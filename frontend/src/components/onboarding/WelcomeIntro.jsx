import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { Shield, Search, MapPin, Bot, ArrowRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { useOnboarding } from '../../context/OnboardingContext'

const SCREENS = [
  {
    id: 'welcome',
    title: 'Welcome to CrimeMatrix',
    body: 'KSP crime intelligence for investigations, analytics, and proactive policing — in one workspace.',
  },
  {
    id: 'capabilities',
    title: 'What you can do',
    body: null,
    bullets: [
      { icon: Search, text: 'Search cases and run investigations with notes, evidence, and timelines' },
      { icon: MapPin, text: 'Explore maps, hotspots, and district patterns across Karnataka' },
      { icon: Bot, text: 'Ask the AI Copilot for summaries, leads, and quick analysis' },
      { icon: Shield, text: 'Track risk scores, priorities, alerts, and predictive insights' },
    ],
  },
  {
    id: 'ready',
    title: 'Ready for a quick tour?',
    body: 'We will highlight the sidebar, header shortcuts, right panel, and main workspace — about 30 seconds.',
  },
]

export default function WelcomeIntro() {
  const { t } = useLanguage()
  const { startTour, skip } = useOnboarding()
  const [step, setStep] = useState(0)
  const screen = SCREENS[step]
  const isLast = step === SCREENS.length - 1

  useEffect(() => {
    function onKey(e) {
      if (e.key === 'Escape') {
        skip()
      } else if (e.key === 'Enter') {
        if (isLast) startTour()
        else setStep((s) => Math.min(s + 1, SCREENS.length - 1))
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [isLast, skip, startTour])

  return createPortal(
    <div className="onboarding-overlay" role="dialog" aria-modal="true" aria-labelledby="onboarding-welcome-title">
      <div className="onboarding-welcome-card">
        <div className="onboarding-welcome-brand">
          <div className="onboarding-welcome-icon">
            <Shield size={22} />
          </div>
          <span>{t('CrimeMatrix')}</span>
        </div>

        <h2 id="onboarding-welcome-title" className="onboarding-welcome-title">
          {t(screen.title)}
        </h2>

        {screen.body && (
          <p className="onboarding-welcome-body">{t(screen.body)}</p>
        )}

        {screen.bullets && (
          <ul className="onboarding-welcome-list">
            {screen.bullets.map((item) => (
              <li key={item.text}>
                <item.icon size={16} aria-hidden="true" />
                <span>{t(item.text)}</span>
              </li>
            ))}
          </ul>
        )}

        <div className="onboarding-welcome-dots" aria-hidden="true">
          {SCREENS.map((s, i) => (
            <span key={s.id} className={`onboarding-dot ${i === step ? 'active' : ''}`} />
          ))}
        </div>

        <div className="onboarding-welcome-actions">
          <button type="button" className="onboarding-btn ghost" onClick={skip}>
            {t('Skip')}
          </button>
          <div className="onboarding-welcome-actions-right">
            {step > 0 && (
              <button type="button" className="onboarding-btn ghost" onClick={() => setStep((s) => s - 1)}>
                {t('Back')}
              </button>
            )}
            {isLast ? (
              <button type="button" className="onboarding-btn primary" onClick={startTour}>
                {t('Start tour')}
                <ArrowRight size={16} />
              </button>
            ) : (
              <button
                type="button"
                className="onboarding-btn primary"
                onClick={() => setStep((s) => s + 1)}
              >
                {t('Next')}
                <ArrowRight size={16} />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>,
    document.body,
  )
}
