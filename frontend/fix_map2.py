import codecs
import re

def process_file(path, replacements):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
    
    for old, new in replacements:
        text = text.replace(old, new)
        
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapLayerControls.jsx', [
    ('Layers\n      </span>', '{t(\'Layers\')}\n      </span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapTimeSlider.jsx', [
    ('Range\n      </span>', '{t(\'Range\')}\n      </span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapFilterPanel.jsx', [
    ('Filters\n      </span>', '{t(\'Filters\')}\n      </span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapCanvas.jsx', [
    ('{props.crime_count} crimes', '{props.crime_count} {t(\'crimes\')}'),
    ('/> Open', '/> {t(\'Open\')}'),
    ('/> Closed', '/> {t(\'Closed\')}'),
    ('/> Pending', '/> {t(\'Pending\')}'),
    ('/> Station', '/> {t(\'Station\')}'),
    ('{props.name}', '{typeof props.name === \'string\' ? props.name.replace(\'Hotspot:\', t(\'Hotspot\') + \':\') : props.name}')
])

new_translations = {
    'Hotspot': {'Kannada': 'ಹಾಟ್‌ಸ್ಪಾಟ್', 'Hindi': 'हॉटस्पॉट', 'Tamil': 'ஹாட்ஸ்பாட்', 'Telugu': 'హాట్‌స్పాట్'},
    'Layers': {'Kannada': 'ಪದರಗಳು', 'Hindi': 'परतें', 'Tamil': 'அடுக்குகள்', 'Telugu': 'పొరలు'},
    'Range': {'Kannada': 'ವ್ಯಾಪ್ತಿ', 'Hindi': 'सीमा', 'Tamil': 'வரம்பு', 'Telugu': 'పరిధి'},
    'Filters': {'Kannada': 'ಫಿಲ್ಟರ್‌ಗಳು', 'Hindi': 'फ़िल्टर', 'Tamil': 'வடிகட்டிகள்', 'Telugu': 'ఫిల్టర్లు'},
    'crimes': {'Kannada': 'ಅಪರಾಧಗಳು', 'Hindi': 'अपराध', 'Tamil': 'குற்றங்கள்', 'Telugu': 'నేరాలు'},
    'Open': {'Kannada': 'ತೆರೆದ', 'Hindi': 'खुला', 'Tamil': 'திறந்த', 'Telugu': 'తెరవండి'},
    'Closed': {'Kannada': 'ಮುಚ್ಚಲಾಗಿದೆ', 'Hindi': 'बंद', 'Tamil': 'மூடப்பட்ட', 'Telugu': 'మూసివేయబడింది'},
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

# fix any missing commas
text = re.sub(r"('[^']*'|\"[^\"]*\")(\s*\r?\n\s*)(['\"][a-zA-Z0-9\s\.\,\:\-\%]+['\"]\:)", r"\1,\2\3", text)

with codecs.open(trans_file, 'w', 'utf-8') as f:
    f.write(text)
print("Updated fix_map2 successfully.")
