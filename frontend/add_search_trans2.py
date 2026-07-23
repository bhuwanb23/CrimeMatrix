import codecs
import re

new_translations = {
    'Cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'Suspects': {'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்கள்', 'Telugu': 'అనుమానితులు'},
    'Search cases, suspects, and investigate connections': {'Kannada': 'ಪ್ರಕರಣಗಳು, ಶಂಕಿತರು ಮತ್ತು ತನಿಖಾ ಸಂಪರ್ಕಗಳನ್ನು ಹುಡುಕಿ', 'Hindi': 'मामले, संदिग्ध खोजें, और कनेक्शन की जांच करें', 'Tamil': 'வழக்குகள், சந்தேக நபர்களைத் தேடுங்கள் மற்றும் தொடர்புகளை விசாரிக்கவும்', 'Telugu': 'కేసులు, అనుమానితులను శోధించండి మరియు కనెక్షన్‌లను దర్యాప్తు చేయండి'},
    'Open': {'Kannada': 'ತೆರೆದ', 'Hindi': 'खुला', 'Tamil': 'திறந்த', 'Telugu': 'తెరవండి'},
    'Closed': {'Kannada': 'ಮುಚ್ಚಲಾಗಿದೆ', 'Hindi': 'बंद', 'Tamil': 'மூடப்பட்ட', 'Telugu': 'మూసివేయబడింది'},
    'Crime Search': {'Kannada': 'ಅಪರಾಧ ಹುಡುಕಾಟ', 'Hindi': 'अपराध खोज', 'Tamil': 'குற்றத் தேடல்', 'Telugu': 'నేర శోధನೆ'}
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
print("Updated translations.js successfully.")
