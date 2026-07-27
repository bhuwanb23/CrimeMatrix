import { useEffect, useState } from 'react'
import { useLanguage } from '../context/LanguageContext'
import { useTheme } from '../context/ThemeContext'
import { get } from '../services/api'

const languages = ['Kannada', 'English', 'Hindi', 'Tamil', 'Telugu']
const PREFS_KEY = 'cm_settings_prefs'

function loadPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY) || '{}')
  } catch {
    return {}
  }
}

export default function SettingsPage() {
  const { language, setLanguage, t } = useLanguage()
  const { theme, setTheme, resolvedTheme } = useTheme()
  const saved = loadPrefs()

  const [config, setConfig] = useState(null)
  const [configError, setConfigError] = useState(null)
  const [savedMsg, setSavedMsg] = useState('')

  const [secondaryLang, setSecondaryLang] = useState(saved.secondaryLang || 'English')
  const [notifications, setNotifications] = useState(saved.notifications || {
    push: true, email: true, sound: false, whisper: true,
  })
  const [voice, setVoice] = useState(saved.voice || {
    enabled: true, language: 'Kannada', speed: 1.0, autoTranscribe: true,
  })
  const [offline, setOffline] = useState(saved.offline || {
    enabled: true, sync: 'WiFi',
  })

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const res = await get('/config')
        if (!cancelled) setConfig(res?.data || null)
      } catch (e) {
        if (!cancelled) setConfigError(e?.message || 'Failed to load config')
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  function handleSave() {
    const prefs = { secondaryLang, theme, notifications, voice, offline }
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs))
    setSavedMsg(t('Preferences saved locally'))
    setTimeout(() => setSavedMsg(''), 2000)
  }

  const features = config?.features || {}
  const initials = 'IO'

  const Toggle = ({ checked, onChange }) => (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`relative h-[22px] w-10 shrink-0 rounded-full transition-colors duration-200 ${
        checked ? 'bg-[var(--color-accent)]' : 'bg-[var(--border-strong)]'
      }`}
    >
      <span
        className={`absolute top-[2px] left-[2px] h-[18px] w-[18px] rounded-full bg-[var(--bg-card)] shadow-sm transition-transform duration-200 ${
          checked ? 'translate-x-[18px]' : ''
        }`}
      />
    </button>
  )

  const Select = ({ value, onChange, options }) => (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="h-10 w-full cursor-pointer rounded-[10px] border border-[var(--border)] bg-[var(--bg-app)] px-3 text-[13px] text-[var(--text-primary)] outline-none transition-[border-color] duration-150 focus:border-[var(--color-accent)]"
    >
      {options.map((opt) => (
        <option key={opt} value={opt}>{opt}</option>
      ))}
    </select>
  )

  const themeOptions = [
    { id: 'light', label: 'light', hint: 'Always light' },
    { id: 'dark', label: 'dark', hint: 'Always dark' },
    { id: 'system', label: 'system', hint: `Match device (${resolvedTheme})` },
  ]

  return (
    <div className="w-full max-w-7xl mx-auto px-4 md:px-6">
      <div className="mb-6 flex flex-col items-start justify-between gap-3 md:flex-row md:items-center">
        <div>
          <h1 className="text-[22px] font-bold tracking-tight text-[var(--text-primary)]">
            {t('Settings')}
          </h1>
          <p className="mt-0.5 text-[13px] text-[var(--text-muted)]">
            {t('Personal preferences')}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {savedMsg && <span className="text-xs text-emerald-600">{savedMsg}</span>}
          <button
            type="button"
            onClick={handleSave}
            className="rounded-xl bg-[var(--btn-primary-bg)] px-5 py-2.5 text-[13px] font-semibold text-[var(--btn-primary-fg)] transition-all duration-150 hover:-translate-y-px hover:opacity-90"
          >
            {t('Save Changes')}
          </button>
        </div>
      </div>

      <div className="mb-3 rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Profile')}</h2>
        <div className="flex flex-col items-center gap-4 text-center md:flex-row md:text-left">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--border-strong)] text-xl font-bold text-[var(--text-on-dark)]">
            {initials}
          </div>
          <div className="min-w-0 flex-1">
            <div className="text-lg font-bold text-[var(--text-primary)]">{t('Investigation Officer')}</div>
            <div className="text-[13px] text-[var(--text-secondary)]">
              {config?.app_name || 'CrimeMatrix'} · {config?.environment || 'local'}
            </div>
            <div className="text-[13px] text-[var(--text-muted)]">
              {t('Auth not enabled')} · {config?.default_ai_provider ? `AI: ${config.default_ai_provider}` : ''}
            </div>
          </div>
        </div>
        {configError && <p className="mt-3 text-xs text-red-500 m-0">{configError}</p>}
      </div>

      {config && (
        <div className="mb-3 rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('System Features')}</h2>
          <div className="grid grid-cols-2 gap-2 md:grid-cols-3">
            {Object.entries(features).map(([key, enabled]) => (
              <div key={key} className="rounded-lg bg-[var(--bg-app)] px-3 py-2 text-xs">
                <span className="font-medium text-[var(--text-primary)]">{key}</span>
                <span className={`ml-2 ${enabled ? 'text-emerald-600' : 'text-[var(--text-muted)]'}`}>
                  {enabled ? t('on') : t('off')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Language')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">
                {t('Primary Language')}
              </label>
              <Select value={language} onChange={setLanguage} options={languages} />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">
                {t('Secondary Language')}
              </label>
              <Select value={secondaryLang} onChange={setSecondaryLang} options={languages} />
            </div>
          </div>
        </div>

        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Theme')}</h2>
          <p className="mb-3 text-[12px] text-[var(--text-muted)]">
            Applies immediately. Current:{' '}
            <span className="capitalize text-[var(--text-secondary)]">{resolvedTheme}</span>
          </p>
          <div className="flex flex-col gap-2">
            {themeOptions.map((th) => (
              <button
                key={th.id}
                type="button"
                onClick={() => setTheme(th.id)}
                className={`flex cursor-pointer items-center gap-3 rounded-[10px] border px-3 py-2.5 text-left transition-colors duration-150 ${
                  theme === th.id
                    ? 'border-[var(--color-accent)] bg-[var(--bg-active)]'
                    : 'border-[var(--border)] bg-[var(--bg-app)] hover:bg-[var(--bg-hover)]'
                }`}
              >
                <div
                  className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-colors duration-150 ${
                    theme === th.id ? 'border-[var(--color-accent)]' : 'border-[var(--border-strong)]'
                  }`}
                >
                  {theme === th.id && <div className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent)]" />}
                </div>
                <div className="min-w-0">
                  <div className="text-[13px] capitalize font-medium text-[var(--text-primary)]">{t(th.label)}</div>
                  <div className="text-[11px] text-[var(--text-muted)]">{th.hint}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Notifications')}</h2>
          <div className="flex flex-col gap-3.5">
            {[
              { key: 'push', label: 'Push Alerts' },
              { key: 'email', label: 'Email Alerts' },
              { key: 'sound', label: 'Sound' },
              { key: 'whisper', label: 'Whisper Alerts' },
            ].map(({ key, label }) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-[13px] text-[var(--text-secondary)]">{t(label)}</span>
                <Toggle
                  checked={notifications[key]}
                  onChange={(v) => setNotifications({ ...notifications, [key]: v })}
                />
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Voice Settings')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Voice Assistant')}</span>
              <Toggle checked={voice.enabled} onChange={(v) => setVoice({ ...voice, enabled: v })} />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">{t('Language')}</label>
              <Select value={voice.language} onChange={(v) => setVoice({ ...voice, language: v })} options={languages} />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">
                {t('Speed')}: {voice.speed}x
              </label>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={voice.speed}
                onChange={(e) => setVoice({ ...voice, speed: parseFloat(e.target.value) })}
                className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-[var(--border)] accent-[var(--color-accent)]"
              />
            </div>
          </div>
        </div>

        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Offline Sync')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Enable Offline')}</span>
              <Toggle checked={offline.enabled} onChange={(v) => setOffline({ ...offline, enabled: v })} />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">{t('Sync Frequency')}</label>
              <Select value={offline.sync} onChange={(v) => setOffline({ ...offline, sync: v })} options={['WiFi', 'Always', 'Manual']} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
