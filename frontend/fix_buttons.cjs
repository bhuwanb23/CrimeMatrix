const fs = require('fs');

let content = fs.readFileSync('e:/CrimeMatrix/frontend/src/components/SettingsPage.jsx', 'utf8');

// Fix carriage returns
content = content.replace(/\r/g, '');

// Fix buttons that missed replacement
content = content.replace(
  />\s*Edit Profile\s*<\/button>/g,
  ">{activeAction === 'edit_profile' ? (t('opening', lang) || 'Opening...') : (t('edit_profile', lang) || 'Edit Profile')}</button>"
);

content = content.replace(
  />\s*Clear Cache\s*<\/button>/g,
  ">{activeAction === 'clear_cache' ? (t('cleared', lang) || 'Cleared!') : (t('clear_cache', lang) || 'Clear Cache')}</button>"
);

content = content.replace(
  />\s*Manage Devices\s*<\/button>/g,
  ">{activeAction === 'manage_devices' ? (t('opening', lang) || 'Opening...') : (t('manage_devices', lang) || 'Manage Devices')}</button>"
);

content = content.replace(
  />\s*Sync Now\s*<\/button>/g,
  ">{activeAction === 'sync_now' ? (t('synced', lang) || 'Synced!') : (t('sync_now', lang) || 'Sync Now')}</button>"
);

fs.writeFileSync('e:/CrimeMatrix/frontend/src/components/SettingsPage.jsx', content);
console.log('Fixed buttons and removed CRLF');
