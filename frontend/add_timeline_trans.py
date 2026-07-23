import codecs
import re

new_translations = {
    'Just now': {'Kannada': 'ಈಗಷ್ಟೆ', 'Hindi': 'अभी-अभी', 'Tamil': 'சற்று முன்', 'Telugu': 'ఇప్పుడే'},
    'm ago': {'Kannada': 'ನಿಮಿಷಗಳ ಹಿಂದೆ', 'Hindi': 'मिनट पहले', 'Tamil': 'நிமிடங்களுக்கு முன்', 'Telugu': 'నిమిషాల క్రితం'},
    'h ago': {'Kannada': 'ಗಂಟೆಗಳ ಹಿಂದೆ', 'Hindi': 'घंटे पहले', 'Tamil': 'மணிநேரங்களுக்கு முன்', 'Telugu': 'గంటల క్రితం'},
    'd ago': {'Kannada': 'ದಿನಗಳ ಹಿಂದೆ', 'Hindi': 'दिन पहले', 'Tamil': 'நாட்களுக்கு முன்', 'Telugu': 'రోజుల క్రితం'},
    'Intelligence Timeline': {'Kannada': 'ಇಂಟೆಲಿಜೆನ್ಸ್ ಟೈಮ್‌ಲೈನ್', 'Hindi': 'इंटेलिजेंस टाइमलाइन', 'Tamil': 'உளவுத்துறை காலவரிசை', 'Telugu': 'ఇంటెలిజెన్స్ కాలక్రమం'},
    'Complete audit trail of AI-generated intelligence': {'Kannada': 'AI-ಉತ್ಪಾದಿತ ಬುದ್ಧಿಮತ್ತೆಯ ಸಂಪೂರ್ಣ ಆಡಿಟ್ ಟ್ರಯಲ್', 'Hindi': 'AI-जनित बुद्धिमत्ता का पूरा ऑडिट ट्रेल', 'Tamil': 'AI-உருவாக்கிய உளவுத்துறையின் முழுமையான தணிக்கை பாதை', 'Telugu': 'AI-ఉత్పత్తి చేసిన మేధస్సు యొక్క పూర్తి ఆడిట్ కాలిబాట'},
    'Total Entries': {'Kannada': 'ಒಟ್ಟು ನಮೂದುಗಳು', 'Hindi': 'कुल प्रविष्टियां', 'Tamil': 'மொத்த உள்ளீடுகள்', 'Telugu': 'మొత్తం ఎంట్రీలు'},
    'Events': {'Kannada': 'ಈವೆಂಟ್‌ಗಳು', 'Hindi': 'ईवेंट', 'Tamil': 'நிகழ்வுகள்', 'Telugu': 'ఈవెంట్‌లు'},
    'Alerts': {'Kannada': 'ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'अलर्ट', 'Tamil': 'விழிப்பூட்டல்கள்', 'Telugu': 'హెచ్చరికలు'},
    'Evidence Links': {'Kannada': 'ಸಾಕ್ಷ್ಯ ಲಿಂಕ್‌ಗಳು', 'Hindi': 'साक्ष्य लिंक', 'Tamil': 'ஆதார இணைப்புகள்', 'Telugu': 'సాక్ష్యం లింకులు'},
    'Recommendations': {'Kannada': 'ಶಿಫಾರಸುಗಳು', 'Hindi': 'सिफारिशें', 'Tamil': 'பரிந்துரைகள்', 'Telugu': 'సిఫార్సులు'},
    'All': {'Kannada': 'ಎಲ್ಲಾ', 'Hindi': 'सभी', 'Tamil': 'அனைத்து', 'Telugu': 'అన్ని'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'साक्ष्य', 'Tamil': 'ஆதாரம்', 'Telugu': 'సాక్ష్యం'},
    'Risk': {'Kannada': 'ಅಪಾಯ', 'Hindi': 'जोखिम', 'Tamil': 'ஆபத்து', 'Telugu': 'ప్రమాదం'},
    'Matches': {'Kannada': 'ಹೊಂದಾಣಿಕೆಗಳು', 'Hindi': 'मैच', 'Tamil': 'பொருத்தங்கள்', 'Telugu': 'మ్యాచ్‌లు'},
    'Loading timeline...': {'Kannada': 'ಟೈಮ್‌ಲೈನ್ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'टाइमलाइन लोड हो रही है...', 'Tamil': 'காலவரிசை ஏற்றப்படுகிறது...', 'Telugu': 'టైమ్‌లైన్ లోడ్ అవుతోంది...'},
    'No timeline entries': {'Kannada': 'ಯಾವುದೇ ಟೈಮ್‌ಲೈನ್ ನಮೂದುಗಳಿಲ್ಲ', 'Hindi': 'कोई टाइमलाइन प्रविष्टियां नहीं हैं', 'Tamil': 'காலவரிசை உள்ளீடுகள் இல்லை', 'Telugu': 'టైమ్‌లైన్ ఎంట్రీలు లేవు'},
    'Intelligence activity will appear here as events are processed': {'Kannada': 'ಈವೆಂಟ್‌ಗಳನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಿದಂತೆ ಗುಪ್ತಚರ ಚಟುವಟಿಕೆ ಇಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತದೆ', 'Hindi': 'ईवेंट संसाधित होने पर इंटेलिजेंस गतिविधि यहां दिखाई देगी', 'Tamil': 'நிகழ்வுகள் செயலாக்கப்படும்போது உளவுத்துறை செயல்பாடு இங்கே தோன்றும்', 'Telugu': 'ఈవెంట్‌లు ప్రాసెస్ చేయబడుతున్నందున ఇంటెలిజెన్స్ కార్యాచరణ ఇక్కడ కనిపిస్తుంది'},
    'Unknown Date': {'Kannada': 'ಅಪರಿಚಿತ ದಿನಾಂಕ', 'Hindi': 'अज्ञात तिथि', 'Tamil': 'தெரியாத தேதி', 'Telugu': 'తెలియని తేదీ'},
    'entries': {'Kannada': 'ನಮೂದುಗಳು', 'Hindi': 'प्रविष्टियां', 'Tamil': 'உள்ளீடுகள்', 'Telugu': 'ఎంట్రీలు'},
    'Event': {'Kannada': 'ಈವೆಂಟ್', 'Hindi': 'ईवेंट', 'Tamil': 'நிகழ்வு', 'Telugu': 'ఈవెంట్'},
    'Alert': {'Kannada': 'ಎಚ್ಚರಿಕೆ', 'Hindi': 'अलर्ट', 'Tamil': 'விழிப்பூட்டல்', 'Telugu': 'హెచ్చరిక'},
    'Recommendation': {'Kannada': 'ಶಿಫಾರಸು', 'Hindi': 'सिफारिश', 'Tamil': 'பரிந்துரை', 'Telugu': 'సిఫార్సు'},
    'Risk/Priority': {'Kannada': 'ಅಪಾಯ/ಆದ್ಯತೆ', 'Hindi': 'जोखिम/प्राथमिकता', 'Tamil': 'ஆபத்து/முன்னுரிமை', 'Telugu': 'ప్రమాదం/ప్రాధాన్యత'},
    'Cross-District': {'Kannada': 'ಅಡ್ಡ-ಜಿಲ್ಲೆ', 'Hindi': 'अंतर-जिला', 'Tamil': 'மாவட்டங்களுக்கு இடையே', 'Telugu': 'క్రాస్-డిస్ట్రిక్ట్'}
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
