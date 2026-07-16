import { useState } from 'react'

const languages = ['Kannada', 'English', 'Hindi', 'Tamil', 'Telugu']

export default function SettingsPage() {
  const [profile, setProfile] = useState({
    name: 'SI Karthik',
    role: 'Investigation Officer',
    email: 'karthik@ksp.gov.in',
  })
  const [primaryLang, setPrimaryLang] = useState('Kannada')
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
      onClick={() => onChange(!checked)}
      className={`relative w-10 h-[22px] rounded-full transition-colors duration-200 ${checked ? 'bg-[var(--color-accent)]' : 'bg-[var(--border-strong)]'}`}
    >
      <span className={`absolute top-[2px] left-[2px] w-[18px] h-[18px] rounded-full bg-white shadow transition-transform duration-200 ${checked ? 'translate-x-[18px]' : ''}`} />
    </button>
  )

  const Select = ({ value, onChange, options }) => (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full h-10 px-3 rounded-lg border text-sm bg-[var(--bg-app)] border-[var(--border)] text-[var(--text-primary)] focus:border-[var(--color-accent)] focus:ring-2 focus:ring-[rgba(245,158,11,0.1)] outline-none transition-all cursor-pointer"
    >
      {options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
    </select>
  )

  return (
    <div className="max-w-[900px]">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-[22px] font-bold text-[var(--text-primary)] tracking-tight">Settings</h1>
          <p className="text-[13px] text-[var(--text-muted)] mt-0.5">Personal preferences</p>
        </div>
        <button className="px-5 py-2.5 rounded-xl bg-[var(--color-primary)] text-white text-sm font-semibold hover:bg-[#1e293b] transition-colors">
          Save Changes
        </button>
      </div>

      {/* Profile */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6 mb-4">
        <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Profile</h2>
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[#334155] flex items-center justify-center text-white text-xl font-bold">
            SK
          </div>
          <div className="flex-1">
            <div className="text-lg font-bold text-[var(--text-primary)]">{profile.name}</div>
            <div className="text-sm text-[var(--text-secondary)]">{profile.role}</div>
            <div className="text-sm text-[var(--text-muted)]">{profile.email}</div>
          </div>
          <button className="px-4 py-2 rounded-lg border border-[var(--border)] text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--bg-hover)] transition-colors">
            Edit Profile
          </button>
        </div>
      </div>

      {/* Two-Column Grid */}
      <div className="grid grid-cols-2 gap-4">
        {/* Language */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Language</h2>
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-[var(--text-muted)] block mb-1.5">Primary Language</label>
              <Select value={primaryLang} onChange={setPrimaryLang} options={languages} />
            </div>
            <div>
              <label className="text-xs font-medium text-[var(--text-muted)] block mb-1.5">Secondary Language</label>
              <Select value={secondaryLang} onChange={setSecondaryLang} options={languages} />
            </div>
          </div>
        </div>

        {/* Theme */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Theme</h2>
          <div className="space-y-3">
            {['light', 'dark', 'system'].map((t) => (
              <label key={t} className="flex items-center gap-3 cursor-pointer group">
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${theme === t ? 'border-[var(--color-accent)]' : 'border-[var(--border-strong)]'}`}>
                  {theme === t && <div className="w-2.5 h-2.5 rounded-full bg-[var(--color-accent)]" />}
                </div>
                <span className="text-sm capitalize text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] transition-colors">{t}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Notifications</h2>
          <div className="space-y-4">
            {[
              { key: 'push', label: 'Push Alerts' },
              { key: 'email', label: 'Email Alerts' },
              { key: 'sound', label: 'Sound' },
              { key: 'whisper', label: 'Whisper Alerts' },
            ].map(({ key, label }) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-sm text-[var(--text-secondary)]">{label}</span>
                <Toggle checked={notifications[key]} onChange={(v) => setNotifications({ ...notifications, [key]: v })} />
              </div>
            ))}
          </div>
        </div>

        {/* Voice Settings */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Voice Settings</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-[var(--text-secondary)]">Voice Assistant</span>
              <Toggle checked={voice.enabled} onChange={(v) => setVoice({ ...voice, enabled: v })} />
            </div>
            <div>
              <label className="text-xs font-medium text-[var(--text-muted)] block mb-1.5">Language</label>
              <Select value={voice.language} onChange={(v) => setVoice({ ...voice, language: v })} options={languages} />
            </div>
            <div>
              <label className="text-xs font-medium text-[var(--text-muted)] block mb-1.5">Speed: {voice.speed}x</label>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={voice.speed}
                onChange={(e) => setVoice({ ...voice, speed: parseFloat(e.target.value) })}
                className="w-full h-1.5 bg-[var(--border)] rounded-full appearance-none cursor-pointer accent-[var(--color-accent)]"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[var(--text-secondary)]">Auto-transcribe</span>
              <Toggle checked={voice.autoTranscribe} onChange={(v) => setVoice({ ...voice, autoTranscribe: v })} />
            </div>
          </div>
        </div>

        {/* Offline Sync */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Offline Sync</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-[var(--text-secondary)]">Enable Offline</span>
              <Toggle checked={offline.enabled} onChange={(v) => setOffline({ ...offline, enabled: v })} />
            </div>
            <div>
              <label className="text-xs font-medium text-[var(--text-muted)] block mb-1.5">Sync Frequency</label>
              <Select value={offline.sync} onChange={(v) => setOffline({ ...offline, sync: v })} options={['WiFi', 'Always', 'Manual']} />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[var(--text-secondary)]">Storage Used</span>
              <span className="text-sm font-medium text-[var(--text-primary)]">{offline.storage}</span>
            </div>
            <button className="w-full py-2 rounded-lg border border-[var(--border)] text-sm font-medium text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] transition-colors">
              Clear Cache
            </button>
          </div>
        </div>

        {/* Device Management */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Device Management</h2>
          <div className="space-y-4">
            <div className="p-3 bg-[var(--bg-app)] rounded-xl">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-[var(--text-primary)]">This Device</span>
                <span className="text-xs font-medium text-[var(--color-success)]">Active</span>
              </div>
              <div className="text-xs text-[var(--text-muted)]">Last sync: 2 minutes ago</div>
              <button className="mt-2 px-3 py-1.5 rounded-lg bg-[var(--color-primary)] text-white text-xs font-semibold hover:bg-[#1e293b] transition-colors">
                Sync Now
              </button>
            </div>
            <div className="border-t border-[var(--border)] pt-3">
              <div className="text-xs font-medium text-[var(--text-muted)] mb-2">Other Devices (2)</div>
              <div className="text-sm text-[var(--text-secondary)]">• Tablet — Last sync: 1 hr ago</div>
              <div className="text-sm text-[var(--text-secondary)]">• Desktop — Last sync: 3 hrs ago</div>
            </div>
            <button className="w-full py-2 rounded-lg border border-[var(--border)] text-sm font-medium text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] transition-colors">
              Manage Devices
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
