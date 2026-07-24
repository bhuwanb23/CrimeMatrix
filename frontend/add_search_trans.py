import codecs
import re

def process_file(path, replacements):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
    
    for old, new in replacements:
        text = text.replace(old, new)
        
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)

process_file(r'e:\CrimeMatrix\frontend\src\components\SearchPage.jsx', [
    ('import { useState, useCallback, useEffect } from \'react\'', 'import { useState, useCallback, useEffect } from \'react\'\nimport { useLanguage } from \'../context/LanguageContext\''),
    ('export default function SearchPage() {', 'export default function SearchPage() {\n  const { t } = useLanguage()'),
    ('Crime Search', '{t(\'Crime Search\')}'),
    ('{t(\'Crime Search\')} across', 'Crime Search across'), # fix accidental replacement
    ('Search across Karnataka — statewide intelligence', '{t(\'Search across Karnataka — statewide intelligence\')}'),
    ('🧠 Semantic ON', '🧠 {t(\'Semantic ON\')}'),
    ('🧠 Semantic', '🧠 {t(\'Semantic\')}'),
    ('`${selectedDistricts.length} Districts` : \'Districts\'', '`${selectedDistricts.length} ${t(\'Districts\')}` : t(\'Districts\')'),
    ('Select districts for cross-district search:', '{t(\'Select districts for cross-district search:\')}'),
    ('Clear all', '{t(\'Clear all\')}')
])

new_translations = {
    'Crime Search': {'Kannada': 'ಅಪರಾಧ ಹುಡುಕಾಟ', 'Hindi': 'अपराध खोज', 'Tamil': 'குற்றத் தேடல்', 'Telugu': 'నేర శోధನೆ'},
    'Search across Karnataka — statewide intelligence': {'Kannada': 'ಕರ್ನಾಟಕದಾದ್ಯಂತ ಹುಡುಕಿ — ರಾಜ್ಯವ್ಯಾಪಿ ಬುದ್ಧಿಮತ್ತೆ', 'Hindi': 'पूरे कर्नाटक में खोजें - राज्यव्यापी खुफिया जानकारी', 'Tamil': 'கர்நாடகா முழுவதும் தேடுங்கள் - மாநில அளவிலான உளவுத்துறை', 'Telugu': 'కర్ణాటక అంతటా శోధించండి — రాష్ట్రవ్యాప్త మేధస్సు'},
    'Semantic ON': {'Kannada': 'ಸೆಮ್ಯಾಂಟಿಕ್ ಆನ್', 'Hindi': 'सिमेंटिक चालू', 'Tamil': 'பொருள் சார்ந்த ஆன்', 'Telugu': 'సెమాంటిక్ ఆన్'},
    'Semantic': {'Kannada': 'ಸೆಮ್ಯಾಂಟಿಕ್', 'Hindi': 'सिमेंटिक', 'Tamil': 'பொருள் சார்ந்த', 'Telugu': 'సెమాంటిక్'},
    'Districts': {'Kannada': 'ಜಿಲ್ಲೆಗಳು', 'Hindi': 'जिले', 'Tamil': 'மாவட்டங்கள்', 'Telugu': 'జిల్లాలు'},
    'Select districts for cross-district search:': {'Kannada': 'ಅಡ್ಡ-ಜಿಲ್ಲಾ ಹುಡುಕಾಟಕ್ಕಾಗಿ ಜಿಲ್ಲೆಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ:', 'Hindi': 'अंतर-जिला खोज के लिए जिलों का चयन करें:', 'Tamil': 'மாவட்டங்களுக்கு இடையேயான தேடலுக்கு மாவட்டங்களைத் தேர்ந்தெடுக்கவும்:', 'Telugu': 'క్రాస్-డిస్ట్రిక్ట్ శోధన కోసం జిల్లాలను ఎంచుకోండి:'},
    'Clear all': {'Kannada': 'ಎಲ್ಲವನ್ನೂ ತೆರವುಗೊಳಿಸಿ', 'Hindi': 'सभी साफ़ करें', 'Tamil': 'அனைத்தையும் அழிக்கவும்', 'Telugu': 'అన్నింటినీ క్లియర్ చేయండి'},
    'All': {'Kannada': 'ಎಲ್ಲಾ', 'Hindi': 'सभी', 'Tamil': 'அனைத்து', 'Telugu': 'అన్ని'},
    'FIR': {'Kannada': 'ಎಫ್ಐಆರ್', 'Hindi': 'प्राथमिकी', 'Tamil': 'FIR', 'Telugu': 'FIR'},
    'Suspects': {'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்கள்', 'Telugu': 'అనుమానితులు'},
    'Theft': {'Kannada': 'ಕಳ್ಳತನ', 'Hindi': 'चोरी', 'Tamil': 'திருட்டு', 'Telugu': 'దొంగతనం'},
    'Fraud': {'Kannada': 'ವಂಚನೆ', 'Hindi': 'धोखाधड़ी', 'Tamil': 'மோசடி', 'Telugu': 'మోసం'},
    'Assault': {'Kannada': 'ಹಲ್ಲೆ', 'Hindi': 'हमला', 'Tamil': 'தாக்குதல்', 'Telugu': 'దాడి'},
    'Cybercrime': {'Kannada': 'ಸೈಬರ್ ಅಪರಾಧ', 'Hindi': 'साइबर अपराध', 'Tamil': 'சைபர் குற்றம்', 'Telugu': 'సైబర్ నేరం'},
    'Bengaluru': {'Kannada': 'ಬೆಂಗಳೂರು', 'Hindi': 'बेंगलुरु', 'Tamil': 'Bengaluru', 'Telugu': 'బెంగళూరు'},
    'Mysuru': {'Kannada': 'ಮೈಸೂರು', 'Hindi': 'मैसूर', 'Tamil': 'மைசூர்', 'Telugu': 'మైసూర్'},
    'Active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకుగా'},
    'Pending': {'Kannada': 'ಬಾಕಿ ಉಳಿದಿದೆ', 'Hindi': 'लंबित', 'Tamil': 'நிலுவையில்', 'Telugu': 'పెండింగ్‌లో ఉంది'},
    'Saved Searches': {'Kannada': 'ಉಳಿಸಿದ ಹುಡುಕಾಟಗಳು', 'Hindi': 'सहेजी गई खोजें', 'Tamil': 'சேமிக்கப்பட்ட தேடல்கள்', 'Telugu': 'సేవ్ చేసిన శోధనలు'},
    'Save current': {'Kannada': 'ಪ್ರಸ್ತುತವನ್ನು ಉಳಿಸಿ', 'Hindi': 'वर्तमान को सहेजें', 'Tamil': 'தற்போதையதைச் சேமி', 'Telugu': 'ప్రస్తుతాన్ని సేవ్ చేయి'},
    'No saved searches': {'Kannada': 'ಯಾವುದೇ ಉಳಿಸಿದ ಹುಡುಕಾಟಗಳಿಲ್ಲ', 'Hindi': 'कोई सहेजी गई खोज नहीं', 'Tamil': 'சேமிக்கப்பட்ட தேடல்கள் எதுவும் இல்லை', 'Telugu': 'సేవ్ చేసిన శోధనలు లేవు'},
    'Run search': {'Kannada': 'ಹುಡುಕಾಟವನ್ನು ಚಲಾಯಿಸಿ', 'Hindi': 'खोज चलाएं', 'Tamil': 'தேடலை இயக்கவும்', 'Telugu': 'శోధనను రన్ చేయండి'},
    'Delete': {'Kannada': 'ಅಳಿಸಿ', 'Hindi': 'हटाएं', 'Tamil': 'நீக்கு', 'Telugu': 'తొలగించు'},
    'Search crimes, suspects, FIRs, evidence...': {'Kannada': 'ಅಪರಾಧಗಳು, ಶಂಕಿತರು, ಎಫ್ಐಆರ್ಗಳು, ಸಾಕ್ಷ್ಯಗಳನ್ನು ಹುಡುಕಿ...', 'Hindi': 'अपराध, संदिग्ध, प्राथमिकी, साक्ष्य खोजें...', 'Tamil': 'குற்றங்கள், சந்தேக நபர்கள், FIR-கள், ஆதாரங்களைத் தேடுங்கள்...', 'Telugu': 'నేరాలు, అనుమానితులు, FIRలు, సాక్ష్యాలను శోధించండి...'},
    'to search': {'Kannada': 'ಹುಡುಕಲು', 'Hindi': 'खोजने के लिए', 'Tamil': 'தேட', 'Telugu': 'శోధించడానికి'},
    'Recent Searches': {'Kannada': 'ಇತ್ತೀಚಿನ ಹುಡುಕಾಟಗಳು', 'Hindi': 'हाल की खोजें', 'Tamil': 'சமீபத்திய தேடல்கள்', 'Telugu': 'ఇటీవలి శోధనలు'},
    'Suggestions': {'Kannada': 'ಸಲಹೆಗಳು', 'Hindi': 'सुझाव', 'Tamil': 'பரிந்துரைகள்', 'Telugu': 'సూచనలు'},
    'Clear search': {'Kannada': 'ಹುಡುಕಾಟವನ್ನು ತೆರವುಗೊಳಿಸಿ', 'Hindi': 'खोज साफ़ करें', 'Tamil': 'தேடலை அழிக்கவும்', 'Telugu': 'శోధనను క్లియర్ చేయండి'},
    'Save search': {'Kannada': 'ಹುಡುಕಾಟವನ್ನು ಉಳಿಸಿ', 'Hindi': 'खोज सहेजें', 'Tamil': 'தேடலைச் சேமி', 'Telugu': 'శోధనను సేవ్ చేయండి'},
    'Search History': {'Kannada': 'ಹುಡುಕಾಟ ಇತಿಹಾಸ', 'Hindi': 'खोज इतिहास', 'Tamil': 'தேடல் வரலாறு', 'Telugu': 'శోధన చరిత్ర'},
    'No search history': {'Kannada': 'ಯಾವುದೇ ಹುಡುಕಾಟ ಇತಿಹಾಸವಿಲ್ಲ', 'Hindi': 'कोई खोज इतिहास नहीं', 'Tamil': 'தேடல் வரலாறு இல்லை', 'Telugu': 'శోధన చరిత్ర లేదు'},
    'results found': {'Kannada': 'ಫಲಿತಾಂಶಗಳು ಕಂಡುಬಂದಿವೆ', 'Hindi': 'परिणाम मिले', 'Tamil': 'முடிவுகள் கிடைத்தன', 'Telugu': 'ఫలితాలు కనుగొనబడ్డాయి'},
    'Crime ID': {'Kannada': 'ಅಪರಾಧ ಐಡಿ', 'Hindi': 'अपराध आईडी', 'Tamil': 'குற்ற எண்', 'Telugu': 'క్రైమ్ ID'},
    'Title': {'Kannada': 'ಶೀರ್ಷಿಕೆ', 'Hindi': 'शीर्षक', 'Tamil': 'தலைப்பு', 'Telugu': 'శీర్షిక'},
    'Type': {'Kannada': 'ಪ್ರಕಾರ', 'Hindi': 'प्रकार', 'Tamil': 'குற்ற வகை', 'Telugu': 'రకం'},
    'District': {'Kannada': 'ಜಿಲ್ಲೆ', 'Hindi': 'ज़िला', 'Tamil': 'மாவட்டம்', 'Telugu': 'జిల్లా'},
    'Status': {'Kannada': 'ಸ್ಥಿತಿ', 'Hindi': 'स्थिति', 'Tamil': 'நிலை', 'Telugu': 'స్థితి'},
    'Date': {'Kannada': 'ದಿನಾಂಕ', 'Hindi': 'दिनांक', 'Tamil': 'தேதி', 'Telugu': 'తేదీ'},
    'Actions': {'Kannada': 'ಕ್ರಿಯೆಗಳು', 'Hindi': 'कार्रवाइयां', 'Tamil': 'செயல்கள்', 'Telugu': 'చర్యలు'},
    'No results found': {'Kannada': 'ಯಾವುದೇ ಫಲಿತಾಂಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई परिणाम नहीं मिला', 'Tamil': 'எந்த முடிவுகளும் கிடைக்கவில்லை', 'Telugu': 'ఫలితాలు ఏవీ కనుగొనబడలేదు'},
    'Try adjusting your search or filters.': {'Kannada': 'ನಿಮ್ಮ ಹುಡುಕಾಟ ಅಥವಾ ಫಿಲ್ಟರ್‌ಗಳನ್ನು ಹೊಂದಿಸಲು ಪ್ರಯತ್ನಿಸಿ.', 'Hindi': 'अपनी खोज या फ़िल्टर समायोजित करने का प्रयास करें।', 'Tamil': 'உங்கள் தேடல் அல்லது வடிப்பான்களைச் சரிசெய்ய முயற்சிக்கவும்.', 'Telugu': 'మీ శోధన లేదా ఫిల్టర్‌లను సర్దుబాటు చేయడానికి ప్రయత్నించండి.'}
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
print("Updated translations.js with all Search component strings successfully.")
