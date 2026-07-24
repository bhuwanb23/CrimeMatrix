import codecs
import re

new_translations = {
    'Draft': {'Kannada': 'ಕರಡು', 'Hindi': 'मसौदा', 'Tamil': 'வரைவு', 'Telugu': 'చిత్తుప్రతి'},
    'Filed': {'Kannada': 'ದಾಖಲಿಸಲಾಗಿದೆ', 'Hindi': 'दायर', 'Tamil': 'தாக்கல்', 'Telugu': 'దాఖలు చేయబడింది'},
    'Final': {'Kannada': 'ಅಂತಿಮ', 'Hindi': 'अंतिम', 'Tamil': 'இறுதி', 'Telugu': 'తుది'},
    'Active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'సక్రియంగా'},
    'Pending': {'Kannada': 'ಬಾಕಿ ಇದೆ', 'Hindi': 'लंबित', 'Tamil': 'நிலுவையில்', 'Telugu': 'పెండింగ్‌లో'},
    'FIR': {'Kannada': 'ಎಫ್ಐಆರ್', 'Hindi': 'प्राथमिकी (FIR)', 'Tamil': 'முதல் தகவல் அறிக்கை (FIR)', 'Telugu': 'FIR'},
    'SI': {'Kannada': 'ಎಸ್.ಐ', 'Hindi': 'एस.आई', 'Tamil': 'எஸ்.ஐ', 'Telugu': 'ఎస్.ఐ'},
    'Inspector': {'Kannada': 'ಇನ್ಸ್ಪೆಕ್ಟರ್', 'Hindi': 'इंस्पेक्टर', 'Tamil': 'ஆய்வாளர்', 'Telugu': 'ఇన్స్పెక్టర్'},
    'System': {'Kannada': 'ವ್ಯವಸ್ಥೆ', 'Hindi': 'प्रणाली', 'Tamil': 'கணினி', 'Telugu': 'సిస్టమ్'},
    'Monthly': {'Kannada': 'ಮಾಸಿಕ', 'Hindi': 'मासिक', 'Tamil': 'மாதாந்திர', 'Telugu': 'నెలవారీ'},
    'Network': {'Kannada': 'ನೆಟ್ವರ್ಕ್', 'Hindi': 'नेटवर्क', 'Tamil': 'நெட்வொர்க்', 'Telugu': 'నెట్‌వర్క్'},
    'Investigation': {'Kannada': 'ತನಿಖೆ', 'Hindi': 'जांच', 'Tamil': 'விசாரணை', 'Telugu': 'దర్యాప్తు'},
    'Export': {'Kannada': 'ರಫ್ತು', 'Hindi': 'निर्यात', 'Tamil': 'ஏற்றுமதி', 'Telugu': 'ఎగుమతి'}
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
print('Updated translations.js with general cases terminology')
