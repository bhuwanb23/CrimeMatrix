import os
import re
import codecs
import json

d = r'e:\CrimeMatrix\frontend\src\components'
files = ['InvestigationPage.jsx']
inv_dir = os.path.join(d, 'investigation')
for f in os.listdir(inv_dir):
    if f.endswith('.jsx'):
        files.append(f'investigation/{f}')

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

for f in set(files):
    path = os.path.join(d, f)
    if not os.path.exists(path):
        continue
    with codecs.open(path, 'r', 'utf-8') as file:
        content = file.read()
    
    original = content
    
    content = re.sub(r'>([^<]+)<', wrap_text, content)
    
    # Also wrap placeholder="..."
    def wrap_placeholder(match):
        text = match.group(1)
        if not text.strip() or '{' in text or '}' in text:
            return match.group(0)
        clean_text = text.strip()
        escaped_text = clean_text.replace("'", "\\'")
        extracted.add(clean_text)
        return f'placeholder={{t(\'{escaped_text}\')}}'
        
    content = re.sub(r'placeholder="([^"]+)"', wrap_placeholder, content)
    
    if content != original:
        if 'useLanguage' not in content:
            # Need to figure out the path to context
            # if 'investigation/' in f it's '../../context/LanguageContext', else '../context/LanguageContext'
            import_path = "'../../context/LanguageContext'" if '/' in f else "'../context/LanguageContext'"
            import_statement = f"import {{ useLanguage }} from {import_path}\n"
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
        print(f'Wrapped strings in {f}')

with codecs.open('extracted_inv.json', 'w', 'utf-8') as f:
    json.dump(list(extracted), f, indent=2, ensure_ascii=False)
print(f'Extracted {len(extracted)} strings.')
