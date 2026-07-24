import codecs
import re

new_translations = {
    'Investigation Report': {'Kannada': 'ತನಿಖಾ ವರದಿ', 'Hindi': 'जांच रिपोर्ट', 'Tamil': 'விசாரணை அறிக்கை', 'Telugu': 'దర్యాప్తు నివేదిక'},
    'Court Report': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ', 'Hindi': 'अदालत की रिपोर्ट', 'Tamil': 'நீதிமன்ற அறிக்கை', 'Telugu': 'కోర్టు నివేదిక'},
    'Theft Case': {'Kannada': 'ಕಳ್ಳತನ ಪ್ರಕರಣ', 'Hindi': 'चोरी का मामला', 'Tamil': 'திருட்டு வழக்கு', 'Telugu': 'దొంగతనం కేసు'},
    'Fraud Case': {'Kannada': 'ವಂಚನೆ ಪ್ರಕರಣ', 'Hindi': 'धोखाधड़ी का मामला', 'Tamil': 'மோசடி வழக்கு', 'Telugu': 'మోసం కేసు'},
    'Assault Case': {'Kannada': 'ಹಲ್ಲೆ ಪ್ರಕರಣ', 'Hindi': 'हमला मामला', 'Tamil': 'தாக்குதல் வழக்கு', 'Telugu': 'దాడి కేసు'},
    'Cybercrime': {'Kannada': 'ಸೈಬರ್ ಅಪರಾಧ', 'Hindi': 'साइबर अपराध', 'Tamil': 'சைபர் கிரைம்', 'Telugu': 'సైబర్‌క్రైమ్'},
    'Monthly Summary July': {'Kannada': 'ಮಾಸಿಕ ಸಾರಾಂಶ ಜುಲೈ', 'Hindi': 'मासिक सारांश जुलाई', 'Tamil': 'மாதாந்திர சுருக்கம் ஜூலை', 'Telugu': 'నెలవారీ సారాంశం జూలై'},
    'Suspect Network Report': {'Kannada': 'ಶಂಕಿತ ನೆಟ್‌ವರ್ಕ್ ವರದಿ', 'Hindi': 'संदिग्ध नेटवर्क रिपोर्ट', 'Tamil': 'சந்தேக நபர் பிணைய அறிக்கை', 'Telugu': 'అనుమానిత నెట్‌వర్క్ నివేదిక'}
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
print('Updated translations.js successfully')
