import codecs
import re

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

start = text.find('English: {')
end = text.find('Kannada: {')
block = text[start:end]

for key in ['Draft', 'Filed', 'Final', 'Active', 'Pending']:
    match = re.search(r"'" + key + r"':\s*'([^']+)'", block)
    if match:
        print(f'{key}: {match.group(1)}')
    else:
        print(f'{key}: MISSING')
