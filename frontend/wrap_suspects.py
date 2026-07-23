import codecs
import os
import re
import json

files = [
    r'e:\CrimeMatrix\frontend\src\components\SuspectRiskPage.jsx',
    r'e:\CrimeMatrix\frontend\src\components\SuspectDetailPage.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\AssociatesTab.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\BehavioralTab.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\MOTab.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\ProfileTab.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\SuspectCard.jsx',
    r'e:\CrimeMatrix\frontend\src\components\suspects\TimelineTab.jsx'
]

extracted = set()

def wrap_text(match):
    text = match.group(1)
    if not text.strip() or '{' in text or '}' in text or text.strip().startswith('var('):
        return match.group(0)
    
    clean_text = text.strip()
    if re.match(r'^[\d\W_]+$', clean_text):
        return match.group(0)
        
    extracted.add(clean_text)
    
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    escaped_text = clean_text.replace("'", "\\'")
    
    return f'>{leading}{{t(\'{escaped_text}\')}}{trailing}<'

for path in files:
    with codecs.open(path, 'r', 'utf-8') as file:
        content = file.read()
    
    original = content
    content = re.sub(r'>([^<]+)<', wrap_text, content)
    
    content = content.replace('{t(t(', '{t(').replace("'))}}", "')}")
    
    if content != original:
        if 'useLanguage' not in content:
            rel = '../../context/LanguageContext' if 'suspects\\' in path else '../context/LanguageContext'
            import_statement = f"import {{ useLanguage }} from '{rel}'\n"
            first_import = content.find('import ')
            if first_import != -1:
                content = content[:first_import] + import_statement + content[first_import:]
        
        export_func = re.search(r'export default function (\w+)\s*\([^)]*\)\s*\{', content)
        if export_func:
            func_start = export_func.end()
            if 'const { t } = useLanguage()' not in content:
                content = content[:func_start] + '\n  const { t } = useLanguage()' + content[func_start:]
        
        with codecs.open(path, 'w', 'utf-8') as file:
            file.write(content)
        print(f'Wrapped strings in {os.path.basename(path)}')

with codecs.open(r'e:\CrimeMatrix\frontend\extracted_suspects.json', 'w', 'utf-8') as f:
    json.dump(list(extracted), f, indent=2, ensure_ascii=False)
print(f'Extracted {len(extracted)} strings.')
