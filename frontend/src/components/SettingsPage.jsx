import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

const languages = ['Kannada', 'English', 'Hindi', 'Tamil', 'Telugu']

export default function SettingsPage() {
  const { language, setLanguage, t } = useLanguage()
  const [profile] = useState({
    name: 'SI Karthik',
    role: 'Investigation Officer',
    email: 'karthik@ksp.gov.in',
  })
  
  const [secondaryLang, setSecondaryLang] = useState('English')
  const [theme, setTheme] = useState('light')
  const [notifications, setNotifications] = useState({
    push: true, email: true, sound: false, whisper: true,
  })
  const [voice, setVoice] = useState({
    enabled: true, language: 'Kannada', speed: 1.0, autoTranscribe: true,
  })
  const [offline, setOffline] = useState({
    enabled: true, sync: 'WiFi', storage: '2.4 GB',
  })

  const Toggle = ({ checked, onChange }) => (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`relative h-[22px] w-10 shrink-0 rounded-full transition-colors duration-200 ${
        checked ? 'bg-[var(--color-accent)]' : 'bg-[var(--border-strong)]'
      }`}
    >
      <span
        className={`absolute top-[2px] left-[2px] h-[18px] w-[18px] rounded-full bg-white shadow-sm transition-transform duration-200 ${
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

  return (
    <div className="max-w-[900px]">
      <div className="mb-6 flex flex-col items-start justify-between gap-3 md:flex-row md:items-center">
        <div>
          <h1 className="text-[22px] font-bold tracking-tight text-[var(--text-primary)]">
            {t('Settings')}
          </h1>
          <p className="mt-0.5 text-[13px] text-[var(--text-muted)]">
            {t('Personal preferences')}
          </p>
        </div>
        <button
          type="button"
          className="rounded-xl bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-all duration-150 hover:-translate-y-px hover:bg-[#1e293b]"
        >
          {t('Save Changes')}
        </button>
      </div>

      {/* Profile */}
      <div className="mb-3 rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Profile')}</h2>
        <div className="flex flex-col items-center gap-4 text-center md:flex-row md:text-left">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[#334155] text-xl font-bold text-white">
            {t('SK')}
          </div>
          <div className="min-w-0 flex-1">
            <div className="text-lg font-bold text-[var(--text-primary)]">{profile.name}</div>
            <div className="text-[13px] text-[var(--text-secondary)]">{profile.role}</div>
            <div className="text-[13px] text-[var(--text-muted)]">{profile.email}</div>
          </div>
          <button
            type="button"
            className="rounded-[10px] border border-[var(--border)] px-4 py-2 text-[13px] font-medium text-[var(--text-secondary)] transition-all duration-150 hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
          >
            {t('Edit Profile')}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        {/* Language */}
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

        {/* Theme */}
        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Theme')}</h2>
          <div className="flex flex-col gap-2.5">
            {['light', 'dark', 'system'].map((th) => (
              <label
                key={th}
                className="flex cursor-pointer items-center gap-2.5 py-1"
                onClick={() => setTheme(th)}
              >
                <div
                  className={`flex h-5 w-5 items-center justify-center rounded-full border-2 transition-colors duration-150 ${
                    theme === th ? 'border-[var(--color-accent)]' : 'border-[var(--border-strong)]'
                  }`}
                >
                  {theme === th && (
                    <div className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent)]" />
                  )}
                </div>
                <span className="text-[13px] capitalize text-[var(--text-secondary)]">{t(th)}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Notifications */}
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

        {/* Voice Settings */}
        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Voice Settings')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Voice Assistant')}</span>
              <Toggle
                checked={voice.enabled}
                onChange={(v) => setVoice({ ...voice, enabled: v })}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">
                {t('Language')}
              </label>
              <Select
                value={voice.language}
                onChange={(v) => setVoice({ ...voice, language: v })}
                options={languages}
              />
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
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Auto-transcribe')}</span>
              <Toggle
                checked={voice.autoTranscribe}
                onChange={(v) => setVoice({ ...voice, autoTranscribe: v })}
              />
            </div>
          </div>
        </div>

        {/* Offline Sync */}
        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Offline Sync')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Enable Offline')}</span>
              <Toggle
                checked={offline.enabled}
                onChange={(v) => setOffline({ ...offline, enabled: v })}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[11px] font-semibold tracking-wide text-[var(--text-muted)] uppercase">
                {t('Sync Frequency')}
              </label>
              <Select
                value={offline.sync}
                onChange={(v) => setOffline({ ...offline, sync: v })}
                options={['WiFi', 'Always', 'Manual']}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-[var(--text-secondary)]">{t('Storage Used')}</span>
              <span className="text-[13px] font-semibold text-[var(--text-primary)]">
                {offline.storage}
              </span>
            </div>
            <button
              type="button"
              className="w-full rounded-lg border border-[var(--border)] px-2 py-2 text-center text-xs font-medium text-[var(--text-muted)] transition-all duration-150 hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
            >
              {t('Clear Cache')}
            </button>
          </div>
        </div>

        {/* Device Management */}
        <div className="rounded-[14px] border border-[var(--border)] bg-[var(--bg-card)] p-5">
          <h2 className="mb-4 text-sm font-semibold text-[var(--text-primary)]">{t('Device Management')}</h2>
          <div className="flex flex-col gap-3.5">
            <div className="rounded-[10px] bg-[var(--bg-app)] p-3">
              <div className="mb-1 flex items-center justify-between">
                <span className="text-[13px] font-semibold text-[var(--text-primary)]">{t('This Device')}</span>
                <span className="text-[10px] font-semibold text-[var(--color-success)]">{t('Active')}</span>
              </div>
              <div className="text-[11px] text-[var(--text-muted)]">{t('Last sync: 2 minutes ago')}</div>
              <button
                type="button"
                className="mt-2 rounded-lg bg-[var(--color-primary)] px-3 py-1.5 text-[11px] font-semibold text-white transition-all duration-150 hover:bg-[#1e293b]"
              >
                {t('Sync Now')}
              </button>
            </div>
            <div className="h-px bg-[var(--border)]" />
            <div className="text-[11px] font-semibold text-[var(--text-muted)]">{t('Other Devices (2)')}</div>
            <div className="text-xs text-[var(--text-secondary)]">{t('• Tablet — Last sync: 1 hr ago')}</div>
            <div className="text-xs text-[var(--text-secondary)]">{t('• Desktop — Last sync: 3 hrs ago')}</div>
            <button
              type="button"
              className="w-full rounded-lg border border-[var(--border)] px-2 py-2 text-center text-xs font-medium text-[var(--text-muted)] transition-all duration-150 hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
            >
              {t('Manage Devices')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
