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
      className="toggle-switch"
      style={{ background: checked ? 'var(--color-accent)' : 'var(--border-strong)' }}
    >
      <span className="toggle-knob" style={{ transform: checked ? 'translateX(18px)' : '' }} />
    </button>
  )

  const Select = ({ value, onChange, options }) => (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="settings-select"
    >
      {options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
    </select>
  )

  return (
    <div className="settings-page">
      <div className="settings-header">
        <div>
          <h1 className="settings-title">Settings</h1>
          <p className="settings-subtitle">Personal preferences</p>
        </div>
        <button className="settings-save-btn">Save Changes</button>
      </div>

      {/* Profile */}
      <div className="settings-card">
        <h2 className="settings-card-title">Profile</h2>
        <div className="settings-profile">
          <div className="settings-avatar">
            <span>SK</span>
          </div>
          <div className="settings-profile-info">
            <div className="settings-profile-name">{profile.name}</div>
            <div className="settings-profile-role">{profile.role}</div>
            <div className="settings-profile-email">{profile.email}</div>
          </div>
          <button className="settings-edit-btn">Edit Profile</button>
        </div>
      </div>

      <div className="settings-grid">
        {/* Language */}
        <div className="settings-card">
          <h2 className="settings-card-title">Language</h2>
          <div className="settings-fields">
            <div className="settings-field">
              <label className="settings-label">Primary Language</label>
              <Select value={primaryLang} onChange={setPrimaryLang} options={languages} />
            </div>
            <div className="settings-field">
              <label className="settings-label">Secondary Language</label>
              <Select value={secondaryLang} onChange={setSecondaryLang} options={languages} />
            </div>
          </div>
        </div>

        {/* Theme */}
        <div className="settings-card">
          <h2 className="settings-card-title">Theme</h2>
          <div className="settings-theme-list">
            {['light', 'dark', 'system'].map((t) => (
              <label key={t} className="settings-theme-option" onClick={() => setTheme(t)}>
                <div className={`settings-radio ${theme === t ? 'active' : ''}`}>
                  {theme === t && <div className="settings-radio-dot" />}
                </div>
                <span className="settings-theme-label">{t}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Notifications */}
        <div className="settings-card">
          <h2 className="settings-card-title">Notifications</h2>
          <div className="settings-fields">
            {[
              { key: 'push', label: 'Push Alerts' },
              { key: 'email', label: 'Email Alerts' },
              { key: 'sound', label: 'Sound' },
              { key: 'whisper', label: 'Whisper Alerts' },
            ].map(({ key, label }) => (
              <div key={key} className="settings-toggle-row">
                <span className="settings-toggle-label">{label}</span>
                <Toggle checked={notifications[key]} onChange={(v) => setNotifications({ ...notifications, [key]: v })} />
              </div>
            ))}
          </div>
        </div>

        {/* Voice Settings */}
        <div className="settings-card">
          <h2 className="settings-card-title">Voice Settings</h2>
          <div className="settings-fields">
            <div className="settings-toggle-row">
              <span className="settings-toggle-label">Voice Assistant</span>
              <Toggle checked={voice.enabled} onChange={(v) => setVoice({ ...voice, enabled: v })} />
            </div>
            <div className="settings-field">
              <label className="settings-label">Language</label>
              <Select value={voice.language} onChange={(v) => setVoice({ ...voice, language: v })} options={languages} />
            </div>
            <div className="settings-field">
              <label className="settings-label">Speed: {voice.speed}x</label>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={voice.speed}
                onChange={(e) => setVoice({ ...voice, speed: parseFloat(e.target.value) })}
                className="settings-range"
              />
            </div>
            <div className="settings-toggle-row">
              <span className="settings-toggle-label">Auto-transcribe</span>
              <Toggle checked={voice.autoTranscribe} onChange={(v) => setVoice({ ...voice, autoTranscribe: v })} />
            </div>
          </div>
        </div>

        {/* Offline Sync */}
        <div className="settings-card">
          <h2 className="settings-card-title">Offline Sync</h2>
          <div className="settings-fields">
            <div className="settings-toggle-row">
              <span className="settings-toggle-label">Enable Offline</span>
              <Toggle checked={offline.enabled} onChange={(v) => setOffline({ ...offline, enabled: v })} />
            </div>
            <div className="settings-field">
              <label className="settings-label">Sync Frequency</label>
              <Select value={offline.sync} onChange={(v) => setOffline({ ...offline, sync: v })} options={['WiFi', 'Always', 'Manual']} />
            </div>
            <div className="settings-toggle-row">
              <span className="settings-toggle-label">Storage Used</span>
              <span className="settings-toggle-value">{offline.storage}</span>
            </div>
            <button className="settings-outline-btn">Clear Cache</button>
          </div>
        </div>

        {/* Device Management */}
        <div className="settings-card">
          <h2 className="settings-card-title">Device Management</h2>
          <div className="settings-fields">
            <div className="settings-device">
              <div className="settings-device-header">
                <span className="settings-device-name">This Device</span>
                <span className="settings-device-status">Active</span>
              </div>
              <div className="settings-device-meta">Last sync: 2 minutes ago</div>
              <button className="settings-small-btn">Sync Now</button>
            </div>
            <div className="settings-device-divider" />
            <div className="settings-device-label">Other Devices (2)</div>
            <div className="settings-device-item">• Tablet — Last sync: 1 hr ago</div>
            <div className="settings-device-item">• Desktop — Last sync: 3 hrs ago</div>
            <button className="settings-outline-btn">Manage Devices</button>
          </div>
        </div>
      </div>
    </div>
  )
}
