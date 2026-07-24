import codecs
import re

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

languages = ['Kannada', 'Hindi', 'Tamil', 'Telugu']
keys_to_check = ['Draft', 'Filed', 'Final', 'Active', 'Pending', 'Investigation', 'Court Report', 'Export', 'FIR', 'SI', 'System', 'Inspector']

for lang in languages:
    print(f'\n--- {lang} ---')
    block_start = text.find(f'{lang}: {{')
    next_lang = {'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu', 'Telugu': 'None'}[lang]
    block_end = text.find(f'{next_lang}: {{') if next_lang != 'None' else len(text)
    block = text[block_start:block_end]
    
    for key in keys_to_check:
        match = re.search(r"'" + key + r"':\s*'([^']+)'", block)
        if match:
            print(f"{key}: {match.group(1)}")
        else:
            print(f"{key}: NOT FOUND")
