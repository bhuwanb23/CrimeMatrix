const fs = require('fs');

let content = fs.readFileSync('e:/CrimeMatrix/frontend/src/components/SettingsPage.jsx', 'utf8');

// Replace standard strings
content = content.replace(/Settings<\/h1>/g, "{t('settings', lang) || 'Settings'}</h1>");
content = content.replace(/Personal preferences<\/p>/g, "{t('personal_preferences', lang) || 'Personal preferences'}</p>");
content = content.replace(/Save Changes<\/button>/g, "{isSaving ? (t('saving', lang) || 'Saving...') : saveSuccess ? (t('saved', lang) || 'Saved!') : (t('save_changes', lang) || 'Save Changes')}</button>");
content = content.replace(/Profile<\/h2>/g, "{t('profile', lang) || 'Profile'}</h2>");
content = content.replace(/Edit Profile<\/button>/g, "{t('edit_profile', lang) || 'Edit Profile'}</button>");
content = content.replace(/Language<\/h2>/g, "{t('language', lang) || 'Language'}</h2>");
content = content.replace(/Primary Language<\/label>/g, "{t('primary_language', lang) || 'Primary Language'}</label>");
content = content.replace(/Secondary Language<\/label>/g, "{t('secondary_language', lang) || 'Secondary Language'}</label>");
content = content.replace(/UI Language \(App\)<\/label>/g, "{t('ui_language', lang) || 'UI Language (App)'}</label>");
content = content.replace(/Theme<\/h2>/g, "{t('theme', lang) || 'Theme'}</h2>");
content = content.replace(/Notifications<\/h2>/g, "{t('notifications', lang) || 'Notifications'}</h2>");
content = content.replace(/{label}<\/span>/g, "{t(key, lang) || label}</span>");
content = content.replace(/Voice Settings<\/h2>/g, "{t('voice_settings', lang) || 'Voice Settings'}</h2>");
content = content.replace(/Voice Assistant<\/span>/g, "{t('voice_assistant', lang) || 'Voice Assistant'}</span>");
content = content.replace(/<label(.*?)>(\s*)Language(\s*)<\/label>/g, "<label$1>$2{t('language', lang) || 'Language'}$3</label>");
content = content.replace(/Speed: {voice\.speed}x<\/label>/g, "{t('speed', lang) || 'Speed'}: {voice.speed}x</label>");
content = content.replace(/Auto-transcribe<\/span>/g, "{t('auto_transcribe', lang) || 'Auto-transcribe'}</span>");
content = content.replace(/Offline Sync<\/h2>/g, "{t('offline_sync', lang) || 'Offline Sync'}</h2>");
content = content.replace(/Enable Offline<\/span>/g, "{t('enable_offline', lang) || 'Enable Offline'}</span>");
content = content.replace(/Sync Frequency<\/label>/g, "{t('sync_frequency', lang) || 'Sync Frequency'}</label>");
content = content.replace(/Storage Used<\/span>/g, "{t('storage_used', lang) || 'Storage Used'}</span>");
content = content.replace(/Clear Cache<\/button>/g, "{t('clear_cache', lang) || 'Clear Cache'}</button>");
content = content.replace(/Device Management<\/h2>/g, "{t('device_management', lang) || 'Device Management'}</h2>");
content = content.replace(/This Device<\/span>/g, "{t('this_device', lang) || 'This Device'}</span>");
content = content.replace(/Active<\/span>/g, "{t('active', lang) || 'Active'}</span>");
content = content.replace(/Last sync: 2 minutes ago<\/div>/g, "{t('last_sync', lang) || 'Last sync'}: 2 {t('minutes_ago', lang) || 'minutes ago'}</div>");
content = content.replace(/Sync Now<\/button>/g, "{t('sync_now', lang) || 'Sync Now'}</button>");
content = content.replace(/Other Devices \(2\)<\/div>/g, "{t('other_devices', lang) || 'Other Devices'} (2)</div>");
content = content.replace(/• Tablet — Last sync: 1 hr ago<\/div>/g, "• {t('tablet', lang) || 'Tablet'} — {t('last_sync', lang) || 'Last sync'}: 1 hr ago</div>");
content = content.replace(/• Desktop — Last sync: 3 hrs ago<\/div>/g, "• {t('desktop', lang) || 'Desktop'} — {t('last_sync', lang) || 'Last sync'}: 3 hrs ago</div>");
content = content.replace(/Manage Devices<\/button>/g, "{t('manage_devices', lang) || 'Manage Devices'}</button>");

// Subcomponents update
content = content.replace(/<option key={opt} value={opt}>{opt}<\/option>/g, "<option key={opt} value={opt}>{t(opt.toLowerCase(), lang) || opt}</option>");
content = content.replace(/<span className="text-\[13px\] capitalize text-\[var\(--text-secondary\)\]">{t}<\/span>/g, "<span className=\"text-[13px] capitalize text-[var(--text-secondary)]\">{t(t, lang) || t}</span>");

// Save button style update
content = content.replace(/className="rounded-xl bg-\[var\(--color-primary\)\] px-5 py-2\.5 text-\[13px\] font-semibold text-white transition-all duration-150 hover:-translate-y-px hover:bg-\[#1e293b\]"/g, 
"onClick={handleSave} disabled={isSaving} className={`rounded-xl px-5 py-2.5 text-[13px] font-semibold text-white transition-all duration-150 hover:-translate-y-px ${saveSuccess ? 'bg-[var(--color-success)]' : 'bg-[var(--color-primary)] hover:bg-[#1e293b]'}`}");

// Add state and effect logic
let hooksInsert = `  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)

  useEffect(() => {
    document.documentElement.className = theme
    localStorage.setItem('theme', theme)
  }, [theme])

  const handleSave = () => {
    setIsSaving(true)
    setTimeout(() => {
      setIsSaving(false)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 2000)
    }, 600)
  }`;

content = content.replace(/  const \[theme, setTheme\] = useState\('light'\)/, hooksInsert);
content = content.replace(/import { useState } from 'react'/, "import { useState, useEffect } from 'react'");

fs.writeFileSync('e:/CrimeMatrix/frontend/src/components/SettingsPage.jsx', content);
console.log('Successfully updated SettingsPage.jsx');
