import codecs
import re

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

missing_any = False
for lang in ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']:
    start = text.find(f'{lang}: {{')
    next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu', 'Telugu': None}[lang]
    end = text.find(f'{next_lang}: {{') if next_lang else len(text)
    block = text[start:end]
    
    for key in ['Reports', 'Current Week', 'Report Statistics', 'Today']:
        match = re.search(r"'" + key + r"':\s*'([^']+)'", block)
        if not match:
            print(f'{lang} {key}: MISSING')
            missing_any = True

if not missing_any:
    print("All stats labels are translated!")
