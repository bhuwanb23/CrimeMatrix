import os
import re
import codecs
import json

d = r'e:\CrimeMatrix\frontend\src\components\analytics'
files = [f for f in os.listdir(d) if f.endswith('.jsx')]

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

for f in files:
    path = os.path.join(d, f)
    with codecs.open(path, 'r', 'utf-8') as file:
        content = file.read()
    
    original = content
    content = re.sub(r'>([^<]+)<', wrap_text, content)
    
    # We want to remove {t('...')} for the following bad matches:
    # They start with ) and contain ? or :
    # Specifically, they are JSX ternary operators caught by > <
    def unwrap(match):
        text = match.group(1)
        if ') :' in text or ') \\n' in text or '=>' in text or text.startswith(')'):
            return text
        return match.group(0)
    
    content = re.sub(r'\{t\(\'([^\']*)\'\)\}', unwrap, content)
    
    if content != original:
        if 'useLanguage' not in content:
            import_statement = "import { useLanguage } from '../../context/LanguageContext'\n"
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

with codecs.open(r'e:\CrimeMatrix\frontend\extracted_analytics.json', 'w', 'utf-8') as f:
    json.dump(list(extracted), f, indent=2, ensure_ascii=False)
print(f'Extracted {len(extracted)} strings.')
