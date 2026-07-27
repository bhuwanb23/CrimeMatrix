import { createContext, useCallback, useContext, useEffect, useLayoutEffect, useMemo, useState } from 'react'

const THEME_KEY = 'app-theme'
const PREFS_KEY = 'cm_settings_prefs'
const ThemeContext = createContext(null)

function getSystemTheme() {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function readStoredTheme() {
  try {
    const direct = localStorage.getItem(THEME_KEY)
    if (direct === 'light' || direct === 'dark' || direct === 'system') return direct
    const prefs = JSON.parse(localStorage.getItem(PREFS_KEY) || '{}')
    if (prefs.theme === 'light' || prefs.theme === 'dark' || prefs.theme === 'system') {
      return prefs.theme
    }
  } catch {
    /* ignore */
  }
  return 'system'
}

function applyDocumentTheme(theme) {
  const root = document.documentElement
  const resolved = theme === 'system' ? getSystemTheme() : theme

  if (theme === 'dark') {
    root.setAttribute('data-theme', 'dark')
  } else if (theme === 'light') {
    root.setAttribute('data-theme', 'light')
  } else {
    root.removeAttribute('data-theme')
  }

  root.style.colorScheme = resolved
  return resolved
}

function syncPrefsTheme(theme) {
  try {
    const prefs = JSON.parse(localStorage.getItem(PREFS_KEY) || '{}')
    prefs.theme = theme
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs))
  } catch {
    /* ignore */
  }
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => readStoredTheme())
  const [resolvedTheme, setResolvedTheme] = useState(() => {
    const initial = readStoredTheme()
    return applyDocumentTheme(initial)
  })

  const setTheme = useCallback((next) => {
    if (next !== 'light' && next !== 'dark' && next !== 'system') return
    setThemeState(next)
    localStorage.setItem(THEME_KEY, next)
    syncPrefsTheme(next)
    setResolvedTheme(applyDocumentTheme(next))
  }, [])

  const cycleTheme = useCallback(() => {
    const order = ['light', 'dark', 'system']
    const idx = order.indexOf(theme)
    setTheme(order[(idx + 1) % order.length])
  }, [theme, setTheme])

  useLayoutEffect(() => {
    setResolvedTheme(applyDocumentTheme(theme))
  }, [theme])

  useEffect(() => {
    if (theme !== 'system') return undefined
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = () => setResolvedTheme(applyDocumentTheme('system'))
    mq.addEventListener('change', onChange)
    return () => mq.removeEventListener('change', onChange)
  }, [theme])

  const value = useMemo(
    () => ({ theme, resolvedTheme, setTheme, cycleTheme }),
    [theme, resolvedTheme, setTheme, cycleTheme]
  )

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return ctx
}
