import codecs
import re

new_translations = {
    'Download': {'Kannada': 'ಡೌನ್‌ಲೋಡ್', 'Hindi': 'डाउनलोड करें', 'Tamil': 'பதிவிறக்கம்', 'Telugu': 'డౌన్‌లోడ్'}
}

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']
for lang in languages:
    block_start = text.find(f'{lang}: {{')
    if block_start == -1: continue
    
    if lang != 'Telugu':
        next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}[lang]
        block_end = text.find(f'{next_lang}: {{', block_start)
    else:
        block_end = len(text)
        
    block = text[block_start:block_end]
    
    new_entries = []
    for k, v in new_translations.items():
        escaped_k = k.replace("'", "\\'")
        if f"'{escaped_k}':" not in block:
            val = k if lang == 'English' else v[lang]
            val = val.replace("'", "\\'")
            new_entries.append(f"    '{escaped_k}': '{val}',")
            
    if new_entries:
        insert_pos = block.rfind('}')
        updated_block = block[:insert_pos] + '\n' + '\n'.join(new_entries) + '\n  ' + block[insert_pos:]
        text = text[:block_start] + updated_block + text[block_end:]

text = re.sub(r"('[^']*'|\"[^\"]*\")(\s*\r?\n\s*)(['\"][a-zA-Z0-9\s\.\,\:\-\%\#]+['\"]\:)", r"\1,\2\3", text)

with codecs.open(trans_file, 'w', 'utf-8') as f:
    f.write(text)
print('Updated translations.js with Download')
