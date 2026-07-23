import os
import re
import codecs
import json

files = [
    'AIAnalyticsPage.jsx', 'AlertsPage.jsx', 'AnalyticsPage.jsx', 'BookmarksPage.jsx', 
    'CaseDetailPage.jsx', 'ChatMessage.jsx', 'CopilotPage.jsx', 'CrimeIntelligencePage.jsx', 
    'CriminalTimelinePage.jsx', 'CrimePatternTimelinePage.jsx', 'Header.jsx', 'EarlyWarningPage.jsx', 
    'DashboardContent.jsx', 'PatternDiscoveryPage.jsx', 'PredictionAnalyticsPage.jsx', 
    'PrioritizationIntelligencePage.jsx', 'PrioritizationDashboard.jsx', 'ReportsPage.jsx', 
    'RightPanel.jsx', 'SettingsPage.jsx', 'Sidebar.jsx'
]

d = r'e:\CrimeMatrix\frontend\src\components'
extracted = set()

def wrap_text(match):
    text = match.group(1)
    if not text.strip() or '{' in text or '}' in text or text.strip().startswith('var('):
        return match.group(0)
    
    clean_text = text.strip()
    # If the text is just a number or symbol, ignore
    if re.match(r'^[\d\W_]+$', clean_text):
        return match.group(0)
        
    extracted.add(clean_text)
    
    # Check if there is leading/trailing whitespace
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    
    # Escape quotes
    escaped_text = clean_text.replace("'", "\\'")
    
    return f'>{leading}{{t(\'{escaped_text}\')}}{trailing}<'

for f in set(files):
    path = os.path.join(d, f)
    if not os.path.exists(path):
        continue
    with codecs.open(path, 'r', 'utf-8') as file:
        content = file.read()
    
    original = content
    
    # Wrap >text<
    content = re.sub(r'>([^<]+)<', wrap_text, content)
    
    if content != original:
        # Check if useLanguage is imported
        if 'useLanguage' not in content:
            import_statement = "import { useLanguage } from '../context/LanguageContext'\n"
            # find first import
            first_import = content.find('import ')
            if first_import != -1:
                content = content[:first_import] + import_statement + content[first_import:]
        
        # Check if const { t } = useLanguage() is in component
        # Find the export default function line
        export_func = re.search(r'export default function (\w+)\s*\([^)]*\)\s*\{', content)
        if export_func:
            func_start = export_func.end()
            if 'const { t } = useLanguage()' not in content:
                content = content[:func_start] + '\n  const { t } = useLanguage()' + content[func_start:]
        
        with codecs.open(path, 'w', 'utf-8') as file:
            file.write(content)
        print(f'Wrapped strings in {f}')

with codecs.open('extracted_strings.json', 'w', 'utf-8') as f:
    json.dump(list(extracted), f, indent=2, ensure_ascii=False)
print(f'Extracted {len(extracted)} strings.')
