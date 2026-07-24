import codecs
import re

new_translations = {
    'Filing': {'Kannada': 'ಫೈಲಿಂಗ್', 'Hindi': 'फाइलिंग', 'Tamil': 'தாக்கல்', 'Telugu': 'దాఖలు'},
    'Investigation': {'Kannada': 'ತನಿಖೆ', 'Hindi': 'जांच', 'Tamil': 'விசாரணை', 'Telugu': 'దర్యాప్తు'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'साक्ष्य', 'Tamil': 'ஆதாரம்', 'Telugu': 'సాక్ష్యం'},
    'Suspect': {'Kannada': 'ಶಂಕಿತ', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்', 'Telugu': 'అనుమానితుడు'},
    'Status Change': {'Kannada': 'ಸ್ಥಿತಿ ಬದಲಾವಣೆ', 'Hindi': 'स्थिति परिवर्तन', 'Tamil': 'நிலை மாற்றம்', 'Telugu': 'స్థితి మార్పు'},
    'All Types': {'Kannada': 'ಎಲ್ಲಾ ಪ್ರಕಾರಗಳು', 'Hindi': 'सभी प्रकार', 'Tamil': 'அனைத்து வகைகள்', 'Telugu': 'అన్ని రకాలు'},
    '7D': {'Kannada': '7 ದಿನಗಳು', 'Hindi': '7 दिन', 'Tamil': '7 நாட்கள்', 'Telugu': '7 రోజులు'},
    '30D': {'Kannada': '30 ದಿನಗಳು', 'Hindi': '30 दिन', 'Tamil': '30 நாட்கள்', 'Telugu': '30 రోజులు'},
    '90D': {'Kannada': '90 ದಿನಗಳು', 'Hindi': '90 दिन', 'Tamil': '90 நாட்கள்', 'Telugu': '90 రోజులు'},
    '1Y': {'Kannada': '1 ವರ್ಷ', 'Hindi': '1 वर्ष', 'Tamil': '1 வருடம்', 'Telugu': '1 సంవత్సరం'},
    'Search suspect...': {'Kannada': 'ಶಂಕಿತನನ್ನು ಹುಡುಕಿ...', 'Hindi': 'संदिग्ध को खोजें...', 'Tamil': 'சந்தேக நபரைத் தேடு...', 'Telugu': 'అనుమానితుడిని వెతకండి...'},
    'No timeline events found': {'Kannada': 'ಯಾವುದೇ ಟೈಮ್‌ಲೈನ್ ಈವೆಂಟ್‌ಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई टाइमलाइन ईवेंट नहीं मिला', 'Tamil': 'காலவரிசை நிகழ்வுகள் எதுவும் கிடைக்கவில்லை', 'Telugu': 'టైమ్‌లైన్ ఈవెంట్‌లు ఏవీ దొరకలేదు'},
    'Add events to investigations to see them here.': {'Kannada': 'ಅವುಗಳನ್ನು ಇಲ್ಲಿ ನೋಡಲು ತನಿಖೆಗಳಿಗೆ ಈವೆಂಟ್‌ಗಳನ್ನು ಸೇರಿಸಿ.', 'Hindi': 'उन्हें यहां देखने के लिए जांच में ईवेंट जोड़ें।', 'Tamil': 'அவற்றை இங்கே காண விசாரணைகளில் நிகழ்வுகளைச் சேர்க்கவும்.', 'Telugu': 'వాటిని ఇక్కడ చూడటానికి దర్యాప్తులకు ఈవెంట్‌లను జోడించండి.'},
    'Crime Trend': {'Kannada': 'ಅಪರಾಧ ಪ್ರವೃತ್ತಿ', 'Hindi': 'अपराध की प्रवृत्ति', 'Tamil': 'குற்ற போக்கு', 'Telugu': 'నేర ధోరణి'},
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
print("Updated translations.js with all Timeline component strings successfully.")
