import codecs
import re

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

for lang in ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']:
    start = text.find(f'{lang}: {{')
    next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu', 'Telugu': None}[lang]
    end = text.find(f'{next_lang}: {{') if next_lang else len(text)
    block = text[start:end]
    match = re.search(r"'FIR':\s*'([^']+)'", block)
    if match:
        print(f'{lang}: FOUND')
    else:
        print(f'{lang}: MISSING')
