import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import {
  clearOnboardingComplete,
  isOnboardingComplete,
  markOnboardingComplete,
} from '../utils/onboardingPrefs'

const OnboardingContext = createContext(null)

export function OnboardingProvider({ children }) {
  const [phase, setPhase] = useState(() => (isOnboardingComplete() ? 'idle' : 'welcome'))

  const startTour = useCallback(() => {
    setPhase('tour')
  }, [])

  const skip = useCallback(() => {
    markOnboardingComplete()
    setPhase('idle')
  }, [])

  const complete = useCallback(() => {
    markOnboardingComplete()
    setPhase('idle')
  }, [])

  const restart = useCallback(() => {
    clearOnboardingComplete()
    setPhase('welcome')
  }, [])

  const value = useMemo(
    () => ({
      phase,
      shouldShowIntro: phase === 'welcome',
      shouldShowTour: phase === 'tour',
      startTour,
      skip,
      complete,
      restart,
    }),
    [complete, phase, restart, skip, startTour],
  )

  return (
    <OnboardingContext.Provider value={value}>
      {children}
    </OnboardingContext.Provider>
  )
}

export function useOnboarding() {
  const ctx = useContext(OnboardingContext)
  if (!ctx) {
    throw new Error('useOnboarding must be used within OnboardingProvider')
  }
  return ctx
}
