const PREFS_KEY = 'cm_settings_prefs'
export const ONBOARDING_VERSION = 1

export function readPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY) || '{}')
  } catch {
    return {}
  }
}

export function writePrefs(patch) {
  try {
    const prefs = { ...readPrefs(), ...patch }
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs))
    return prefs
  } catch {
    return patch
  }
}

export function isOnboardingComplete() {
  const prefs = readPrefs()
  return Boolean(prefs.onboardingCompleted) && prefs.onboardingVersion === ONBOARDING_VERSION
}

export function markOnboardingComplete() {
  return writePrefs({
    onboardingCompleted: true,
    onboardingVersion: ONBOARDING_VERSION,
  })
}

export function clearOnboardingComplete() {
  return writePrefs({
    onboardingCompleted: false,
    onboardingVersion: ONBOARDING_VERSION,
  })
}
