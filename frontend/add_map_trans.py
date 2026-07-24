import codecs
import re

new_translations = {
    'Geo Intelligence': {'Kannada': 'ಜಿಯೋ ಇಂಟೆಲಿಜೆನ್ಸ್', 'Hindi': 'जियो इंटेलिजेंस', 'Tamil': 'புவி உளவுத்துறை', 'Telugu': 'జియో ఇంటెలిజెన్స్'},
    'Stations, spatial analysis & crime mapping': {'Kannada': 'ನಿಲ್ದಾಣಗಳು, ಪ್ರಾದೇಶಿಕ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಅಪರಾಧ ಮ್ಯಾಪಿಂಗ್', 'Hindi': 'स्टेशन, स्थानिक विश्लेषण और अपराध मानचित्रण', 'Tamil': 'நிலையங்கள், இடஞ்சார்ந்த பகுப்பாய்வு மற்றும் குற்ற வரைபடம்', 'Telugu': 'స్టేషన్లు, ప్రాదేశిక విశ్లేషణ మరియు క్రైమ్ మ్యాపింగ్'},
    'Refresh': {'Kannada': 'ರಿಫ್ರೆಶ್', 'Hindi': 'रीफ्रेश', 'Tamil': 'புதுப்பி', 'Telugu': 'రిఫ్రెష్'},
    'Crimes': {'Kannada': 'ಅಪರಾಧಗಳು', 'Hindi': 'अपराध', 'Tamil': 'குற்றங்கள்', 'Telugu': 'నేరాలు'},
    'Districts': {'Kannada': 'ಜಿಲ್ಲೆಗಳು', 'Hindi': 'जिले', 'Tamil': 'மாவட்டங்கள்', 'Telugu': 'జిల్లాలు'},
    'Stations': {'Kannada': 'ನಿಲ್ದಾಣಗಳು', 'Hindi': 'स्टेशन', 'Tamil': 'நிலையங்கள்', 'Telugu': 'స్టేషన్లు'},
    'Hotspots': {'Kannada': 'ಹಾಟ್‌ಸ್ಪಾಟ್‌ಗಳು', 'Hindi': 'हॉटस्पॉट', 'Tamil': 'ஹாட்ஸ்பாட்கள்', 'Telugu': 'హాట్‌స్పాట్‌లు'},
    'Layers': {'Kannada': 'ಪದರಗಳು', 'Hindi': 'परतें', 'Tamil': 'அடுக்குகள்', 'Telugu': 'పొరలు'},
    'Routes': {'Kannada': 'ಮಾರ್ಗಗಳು', 'Hindi': 'मार्ग', 'Tamil': 'வழித்தடங்கள்', 'Telugu': 'మార్గాలు'},
    'Density': {'Kannada': 'ಸಾಂದ್ರತೆ', 'Hindi': 'घनत्व', 'Tamil': 'அடர்த்தி', 'Telugu': 'సాంద్రత'},
    'All types': {'Kannada': 'ಎಲ್ಲಾ ಪ್ರಕಾರಗಳು', 'Hindi': 'सभी प्रकार', 'Tamil': 'அனைத்து வகைகள்', 'Telugu': 'అన్ని రకాలు'},
    'Robbery': {'Kannada': 'ದರೋಡೆ', 'Hindi': 'लूट', 'Tamil': 'கொள்ளை', 'Telugu': 'దోపిడీ'},
    'Assault': {'Kannada': 'ಹಲ್ಲೆ', 'Hindi': 'हमला', 'Tamil': 'தாக்குதல்', 'Telugu': 'దాడి'},
    'Murder': {'Kannada': 'ಕೊಲೆ', 'Hindi': 'हत्या', 'Tamil': 'கொலை', 'Telugu': 'హత్య'},
    'Missing': {'Kannada': 'ಕಾಣೆಯಾಗಿದೆ', 'Hindi': 'लापता', 'Tamil': 'காணவில்லை', 'Telugu': 'కనిపించడం లేదు'},
    'Burglary': {'Kannada': 'ಕಳ್ಳತನ', 'Hindi': 'सेंधमारी', 'Tamil': 'கன்னமிடுதல்', 'Telugu': 'దొంగతనం'},
    'All risk': {'Kannada': 'ಎಲ್ಲಾ ಅಪಾಯ', 'Hindi': 'सभी जोखिम', 'Tamil': 'அனைத்து ஆபத்து', 'Telugu': 'అన్ని ప్రమాదాలు'},
    'Critical': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'முக்கியமான', 'Telugu': 'క్లిష్టమైన'},
    'High': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'Medium': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தர', 'Telugu': 'మధ్యస్థం'},
    'Low': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'कम', 'Tamil': 'குறைந்த', 'Telugu': 'తక్కువ'},
    'Overview': {'Kannada': 'ಅವಲೋಕನ', 'Hindi': 'अवलोकन', 'Tamil': 'கண்ணோட்டம்', 'Telugu': 'అవలోకనం'},
    'Selected district': {'Kannada': 'ಆಯ್ಕೆಮಾಡಿದ ಜಿಲ್ಲೆ', 'Hindi': 'चयनित जिला', 'Tamil': 'தேர்ந்தெடுக்கப்பட்ட மாவட்டம்', 'Telugu': 'ఎంచుకున్న జిల్లా'},
    'Total cases': {'Kannada': 'ಒಟ್ಟು ಪ್ರಕರಣಗಳು', 'Hindi': 'कुल मामले', 'Tamil': 'மொத்த வழக்குகள்', 'Telugu': 'మొత్తం కేసులు'},
    'Risk': {'Kannada': 'ಅಪಾಯ', 'Hindi': 'जोखिम', 'Tamil': 'ஆபத்து', 'Telugu': 'ప్రమాదం'},
    'cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'Select a district on the map': {'Kannada': 'ನಕ್ಷೆಯಲ್ಲಿ ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ', 'Hindi': 'मानचित्र पर एक जिले का चयन करें', 'Tamil': 'வரைபடத்தில் ஒரு மாவட்டத்தைத் தேர்ந்தெடுக்கவும்', 'Telugu': 'మ్యాప్‌లో జిల్లాను ఎంచుకోండి'},
    'Pending': {'Kannada': 'ಬಾಕಿ ಉಳಿದಿದೆ', 'Hindi': 'लंबित', 'Tamil': 'நிலுவையில்', 'Telugu': 'పెండింగ్‌లో ఉంది'},
    'Station': {'Kannada': 'ನಿಲ್ದಾಣ', 'Hindi': 'स्टेशन', 'Tamil': 'நிலையம்', 'Telugu': 'స్టేషన్'},
    'High (>100 cases)': {'Kannada': 'ಹೆಚ್ಚು (>100 ಪ್ರಕರಣಗಳು)', 'Hindi': 'उच्च (>100 मामले)', 'Tamil': 'உயர் (>100 வழக்குகள்)', 'Telugu': 'అధిక (>100 కేసులు)'},
    'Medium (50-100)': {'Kannada': 'ಮಧ್ಯಮ (50-100)', 'Hindi': 'मध्यम (50-100)', 'Tamil': 'நடுத்தர (50-100)', 'Telugu': 'మధ్యస్థం (50-100)'},
    'Low (<50)': {'Kannada': 'ಕಡಿಮೆ (<50)', 'Hindi': 'कम (<50)', 'Tamil': 'குறைந்த (<50)', 'Telugu': 'తక్కువ (<50)'},
    'critical': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'முக்கியமான', 'Telugu': 'క్లిష్టమైన'},
    'high': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'medium': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தர', 'Telugu': 'మధ్యస్థం'},
    'low': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'कम', 'Tamil': 'குறைந்த', 'Telugu': 'తక్కువ'},
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
