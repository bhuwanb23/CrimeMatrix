import codecs
import re

new_translations = {
    'Score All Investigations': {'Kannada': 'ಎಲ್ಲಾ ತನಿಖೆಗಳನ್ನು ಸ್ಕೋರ್ ಮಾಡಿ', 'Hindi': 'सभी जांचों का स्कोर करें', 'Tamil': 'அனைத்து விசாரணைகளுக்கும் மதிப்பெண் கொடுங்கள்', 'Telugu': 'అన్ని దర్యాప్తులకూ స్కోర్ చేయండి'},
    'items': {'Kannada': 'ಐಟಂಗಳು', 'Hindi': 'आइटम', 'Tamil': 'உருப்படிகள்', 'Telugu': 'అంశాలు'},
    'progress': {'Kannada': 'ಪ್ರಗತಿ', 'Hindi': 'प्रगति', 'Tamil': 'முன்னேற்றம்', 'Telugu': 'పురోగతి'},
    'Officer': {'Kannada': 'ಅಧಿಕಾರಿ', 'Hindi': 'अधिकारी', 'Tamil': 'அதிகாரி', 'Telugu': 'అధికారి'},
    'cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'high': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'அதிகம்', 'Telugu': 'ఎక్కువ'},
    'Scanning...': {'Kannada': 'ಸ್ಕ್ಯಾನ್ ಮಾಡಲಾಗುತ್ತಿದೆ...', 'Hindi': 'स्कैन कर रहा है...', 'Tamil': 'ஸ்கேன் செய்யப்படுகிறது...', 'Telugu': 'స్కాన్ చేస్తోంది...'},
    'Scan Now': {'Kannada': 'ಈಗ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ', 'Hindi': 'अभी स्कैन करें', 'Tamil': 'இப்போது ஸ்கேன் செய்யவும்', 'Telugu': 'ఇప్పుడే స్కాన్ చేయండి'},
    'Processing...': {'Kannada': 'ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ...', 'Hindi': 'प्रसंस्करण हो रहा है...', 'Tamil': 'செயலாக்கப்படுகிறது...', 'Telugu': 'ప్రాసెస్ చేస్తోంది...'},
    'Process Queue': {'Kannada': 'ಪ್ರಕ್ರಿಯೆ ಕ್ಯೂ', 'Hindi': 'प्रक्रिया कतार', 'Tamil': 'செயலாக்க வரிசை', 'Telugu': 'ప్రాసెస్ క్యూ'},
    'AI Intelligence Summary': {'Kannada': 'AI ಇಂಟೆಲಿಜೆನ್ಸ್ ಸಾರಾಂಶ', 'Hindi': 'AI इंटेलिजेंस सारांश', 'Tamil': 'AI உளவுத்துறை சுருக்கம்', 'Telugu': 'AI ఇంటెలిజెన్స్ సారాంశం'},
    'The AI Intelligence Engine continuously monitors incoming FIRs, evidence updates, and case changes to detect hidden relationships and recommend immediate actions.': {'Kannada': 'ಮುಂಬರುವ FIR ಗಳು, ಸಾಕ್ಷ್ಯ ನವೀಕರಣಗಳು ಮತ್ತು ಗುಪ್ತ ಸಂಬಂಧಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಮತ್ತು ತಕ್ಷಣದ ಕ್ರಮಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡಲು ಕೇಸ್ ಬದಲಾವಣೆಗಳನ್ನು AI ಇಂಟೆಲಿಜೆನ್ಸ್ ಎಂಜಿನ್ ನಿರಂತರವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡುತ್ತದೆ.', 'Hindi': 'AI इंटेलिजेंस इंजन लगातार आने वाली FIR, साक्ष्य अपडेट और छिपे हुए संबंधों का पता लगाने और तत्काल कार्रवाई की सिफारिश करने के लिए केस परिवर्तनों की निगरानी करता है।', 'Tamil': 'வரவிருக்கும் FIR-கள், ஆதாரப் புதுப்பிப்புகள் மற்றும் மறைக்கப்பட்ட உறவுகளைக் கண்டறிந்து உடனடி நடவடிக்கைகளைப் பரிந்துரைக்க வழக்கு மாற்றங்களை AI நுண்ணறிவு இயந்திரம் தொடர்ந்து கண்காணிக்கிறது.', 'Telugu': 'వచ్చే FIRలు, సాక్ష్యం నవీకరణలు మరియు దాచిన సంబంధాలను గుర్తించడానికి మరియు తక్షణ చర్యలను సిఫార్సు చేయడానికి కేసు మార్పులను AI ఇంటెలిజెన్స్ ఇంజిన్ నిరంతరం పర్యవేక్షిస్తుంది.'},
    'events waiting for processing': {'Kannada': 'ಪ್ರಕ್ರಿಯೆಗಾಗಿ ಕಾಯುತ್ತಿರುವ ಈವೆಂಟ್‌ಗಳು', 'Hindi': 'प्रसंस्करण की प्रतीक्षा कर रहे ईवेंट', 'Tamil': 'செயலாக்கத்திற்காக காத்திருக்கும் நிகழ்வுகள்', 'Telugu': 'ప్రాసెసింగ్ కోసం వేచి ఉన్న ఈవెంట్‌లు'},
    'events processed automatically': {'Kannada': 'ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾದ ಈವೆಂಟ್‌ಗಳು', 'Hindi': 'स्वचालित रूप से संसाधित ईवेंट', 'Tamil': 'தானாகவே செயலாக்கப்பட்ட நிகழ்வுகள்', 'Telugu': 'స్వయంచాలకంగా ప్రాసెస్ చేయబడిన ఈవెంట్‌లు'},
    'critical': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'மிகவும் முக்கியமானது', 'Telugu': 'క్లిష్టమైన'},
    'Priority Queue': {'Kannada': 'ಆದ್ಯತೆ ಕ್ಯೂ', 'Hindi': 'प्राथमिकता कतार', 'Tamil': 'முன்னுரிமை வரிசை', 'Telugu': 'ప్రాధాన్యతా క్యూ'},
    'Investigations ranked by urgency': {'Kannada': 'ತುರ್ತು ಆಧಾರದ ಮೇಲೆ ಶ್ರೇಣೀಕೃತ ತನಿಖೆಗಳು', 'Hindi': 'तात्कालिकता द्वारा रैंक की गई जांच', 'Tamil': 'அவசரத்தின் அடிப்படையில் தரவரிசைப்படுத்தப்பட்ட விசாரணைகள்', 'Telugu': 'ఆవశ్యకత ఆధారంగా దర్యాప్తుల ర్యాంకింగ్స్'},
    'No priorities scored yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಆದ್ಯತೆಗಳನ್ನು ಸ್ಕೋರ್ ಮಾಡಿಲ್ಲ', 'Hindi': 'अभी तक कोई प्राथमिकता स्कोर नहीं की गई है', 'Tamil': 'இதுவரை எந்த முன்னுரிமையும் மதிப்பெண் செய்யப்படவில்லை', 'Telugu': 'ఇంకా ప్రాధాన్యతలు ఏవీ స్కోర్ చేయబడలేదు'},
    'Officer Workload': {'Kannada': 'ಅಧಿಕಾರಿ ಕೆಲಸದ ಹೊರೆ', 'Hindi': 'अधिकारी कार्यभार', 'Tamil': 'அதிகாரி பணிச்சுமை', 'Telugu': 'అధికారి పనిభారం'},
    'Case distribution across officers': {'Kannada': 'ಅಧಿಕಾರಿಗಳಾದ್ಯಂತ ಪ್ರಕರಣ ಹಂಚಿಕೆ', 'Hindi': 'अधिकारियों के बीच मामले का वितरण', 'Tamil': 'அதிகாரிகள் முழுவதும் வழக்கு விநியோகம்', 'Telugu': 'అధికారుల మధ్య కేసు పంపిణీ'},
    'No workload data available': {'Kannada': 'ಯಾವುದೇ ಕೆಲಸದ ಹೊರೆ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ', 'Hindi': 'कोई कार्यभार डेटा उपलब्ध नहीं है', 'Tamil': 'எந்த பணிச்சுமை தரவும் கிடைக்கவில்லை', 'Telugu': 'పనిభారం డేటా అందుబాటులో లేదు'},
    'MEDIUM': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தரம்', 'Telugu': 'మధ్యస్థం'},
    'CRITICAL': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'மிகவும் முக்கியமானது', 'Telugu': 'క్లిష్టమైన'},
    'HIGH': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'அதிகம்', 'Telugu': 'ఎక్కువ'},
    'LOW': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'निम्न', 'Tamil': 'குறைவு', 'Telugu': 'తక్కువ'}
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
print("Updated translations.js with all Prioritization component strings successfully.")
