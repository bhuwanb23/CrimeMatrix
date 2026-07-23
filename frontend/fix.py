import codecs
import re

files_to_check = [
    r'e:\CrimeMatrix\frontend\src\components\trends\CrimeTrendLine.jsx',
    r'e:\CrimeMatrix\frontend\src\components\trends\CaseTrendChart.jsx',
    r'e:\CrimeMatrix\frontend\src\components\copilot\ChatArea.jsx',
    r'e:\CrimeMatrix\frontend\src\components\copilot\ChatHistory.jsx',
    r'e:\CrimeMatrix\frontend\src\components\graph\GraphCanvas.jsx'
]

for file in files_to_check:
    try:
        with codecs.open(file, 'r', 'utf-8') as f:
            content = f.read()
        
        original = content
        
        idx_export = content.find('export default')
        if idx_export != -1:
            before_export = content[:idx_export]
            after_export = content[idx_export:]
            
            # Use regex to find t('string') in global space
            # but be careful not to remove it from helper functions that have 'const { t } = useLanguage()'
            if 'function' not in before_export:
                new_before = re.sub(r't\(([\'\"].*?[\'\"])\)', r'\1', before_export)
                content = new_before + after_export
            
        if content != original:
            with codecs.open(file, 'w', 'utf-8') as f:
                f.write(content)
            print(f'Fixed top-level t() in {file}')
    except Exception as e:
        print(e)
