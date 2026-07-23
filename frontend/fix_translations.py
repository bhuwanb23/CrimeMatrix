import codecs
import re

translations = {
    'Report ID': {'Kannada': 'ವರದಿ ಐಡಿ', 'Hindi': 'रिपोर्ट आईडी', 'Tamil': 'அறிக்கை ஐடி', 'Telugu': 'నివేదిక ID'},
    'Title': {'Kannada': 'ಶೀರ್ಷಿಕೆ', 'Hindi': 'शीर्षक', 'Tamil': 'தலைப்பு', 'Telugu': 'శీర్షిక'},
    'Type': {'Kannada': 'ಪ್ರಕಾರ', 'Hindi': 'प्रकार', 'Tamil': 'வகை', 'Telugu': 'రకం'},
    'Case': {'Kannada': 'ಪ್ರಕರಣ', 'Hindi': 'मामला', 'Tamil': 'வழக்கு', 'Telugu': 'కేసు'},
    'Officer': {'Kannada': 'ಅಧಿಕಾರಿ', 'Hindi': 'अधिकारी', 'Tamil': 'அதிகாரி', 'Telugu': 'అధికారి'},
    'Date': {'Kannada': 'ದಿನಾಂಕ', 'Hindi': 'दिनांक', 'Tamil': 'தேதி', 'Telugu': 'తేదీ'},
    'Pages': {'Kannada': 'ಪುಟಗಳು', 'Hindi': 'पृष्ठ', 'Tamil': 'பக்கங்கள்', 'Telugu': 'పేజీలు'},
    'Status': {'Kannada': 'ಸ್ಥಿತಿ', 'Hindi': 'स्थिति', 'Tamil': 'நிலை', 'Telugu': 'స్థితి'},
    'Actions': {'Kannada': 'ಕ್ರಿಯೆಗಳು', 'Hindi': 'कार्रवाइयां', 'Tamil': 'செயல்கள்', 'Telugu': 'చర్యలు'},
    
    'Reports & Documentation': {'Kannada': 'ವರದಿಗಳು ಮತ್ತು ದಾಖಲೆಗಳು', 'Hindi': 'रिपोर्ट और दस्तावेज़ीकरण', 'Tamil': 'அறிக்கைகள் மற்றும் ஆவணங்கள்', 'Telugu': 'నివేదికలు & డాక్యుమెంటేషన్'},
    'Investigation reports, court documents, and exports': {'Kannada': 'ತನಿಖಾ ವರದಿಗಳು, ನ್ಯಾಯಾಲಯದ ದಾಖಲೆಗಳು ಮತ್ತು ರಫ್ತುಗಳು', 'Hindi': 'जांच रिपोर्ट, अदालत के दस्तावेज़ और निर्यात', 'Tamil': 'விசாரணை அறிக்கைகள், நீதிமன்ற ஆவணங்கள் மற்றும் ஏற்றுமதிகள்', 'Telugu': 'దర్యాప్తు నివేదికలు, కోర్టు పత్రాలు మరియు ఎగుమతులు'},
    
    'Report Statistics': {'Kannada': 'ವರದಿ ಅಂಕಿಅಂಶಗಳು', 'Hindi': 'रिपोर्ट सांख्यिकी', 'Tamil': 'அறிக்கை புள்ளிவிவரங்கள்', 'Telugu': 'నివేదిక గణాంకాలు'},
    'Today': {'Kannada': 'ಇಂದು', 'Hindi': 'आज', 'Tamil': 'இன்று', 'Telugu': 'నేడు'},
    'Current Week': {'Kannada': 'ಪ್ರಸ್ತುತ ವಾರ', 'Hindi': 'वर्तमान सप्ताह', 'Tamil': 'நடப்பு வாரம்', 'Telugu': 'ప్రస్తుత వారం'},
    'Mon': {'Kannada': 'ಸೋಮ', 'Hindi': 'सोम', 'Tamil': 'திங்கள்', 'Telugu': 'సోమ'},
    'Tue': {'Kannada': 'ಮಂಗಳ', 'Hindi': 'मंगल', 'Tamil': 'செவ்வாய்', 'Telugu': 'మంగళ'},
    'Wed': {'Kannada': 'ಬುಧ', 'Hindi': 'बुध', 'Tamil': 'புதன்', 'Telugu': 'బుధ'},
    'Thu': {'Kannada': 'ಗುರು', 'Hindi': 'गुरु', 'Tamil': 'வியாழன்', 'Telugu': 'గురు'},
    'Fri': {'Kannada': 'ಶುಕ್ರ', 'Hindi': 'शुक्र', 'Tamil': 'வெள்ளி', 'Telugu': 'శుక్ర'},
    'Sat': {'Kannada': 'ಶನಿ', 'Hindi': 'शनि', 'Tamil': 'சனி', 'Telugu': 'శని'},
    'Sun': {'Kannada': 'ಭಾನು', 'Hindi': 'रवि', 'Tamil': 'ஞாயிறு', 'Telugu': 'ఆది'},
    
    'Date:': {'Kannada': 'ದಿನಾಂಕ:', 'Hindi': 'दिनांक:', 'Tamil': 'தேதி:', 'Telugu': 'తేదీ:'},
    'Type:': {'Kannada': 'ಪ್ರಕಾರ:', 'Hindi': 'प्रकार:', 'Tamil': 'வகை:', 'Telugu': 'రకం:'},
    'Status:': {'Kannada': 'ಸ್ಥಿತಿ:', 'Hindi': 'स्थिति:', 'Tamil': 'நிலை:', 'Telugu': 'స్థితి:'},
    'All period': {'Kannada': 'ಎಲ್ಲಾ ಅವಧಿ', 'Hindi': 'सभी अवधि', 'Tamil': 'அனைத்து காலகட்டம்', 'Telugu': 'అన్ని కాలం'},
    'All types': {'Kannada': 'ಎಲ್ಲಾ ಪ್ರಕಾರಗಳು', 'Hindi': 'सभी प्रकार', 'Tamil': 'அனைத்து வகைகள்', 'Telugu': 'అన్ని రకాలు'},
    'All statuses': {'Kannada': 'ಎಲ್ಲಾ ಸ್ಥಿತಿಗಳು', 'Hindi': 'सभी स्थितियाँ', 'Tamil': 'அனைத்து நிலைகள்', 'Telugu': 'అన్ని స్థితులు'},
    
    'Investigation': {'Kannada': 'ತನಿಖೆ', 'Hindi': 'जांच', 'Tamil': 'விசாரணை', 'Telugu': 'దర్యాప్తు'},
    'Court Report': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ', 'Hindi': 'न्यायालय रिपोर्ट', 'Tamil': 'நீதிமன்ற அறிக்கை', 'Telugu': 'కోర్టు నివేదిక'},
    'Export': {'Kannada': 'ರಫ್ತು', 'Hindi': 'निर्यात', 'Tamil': 'ஏற்றுமதி', 'Telugu': 'ఎగుమతి'},
    'Export CSV': {'Kannada': 'CSV ರಫ್ತು ಮಾಡಿ', 'Hindi': 'CSV निर्यात करें', 'Tamil': 'CSV ஏற்றுமதி செய்', 'Telugu': 'CSV ఎగుమతి చేయండి'}
}

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    text = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']
for lang in languages:
    # Find the block for this language
    block_start = text.find(f'{lang}: {{')
    if block_start == -1: continue
    
    # Extract the block
    if lang != 'Telugu':
        next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}[lang]
        block_end = text.find(f'{next_lang}: {{', block_start)
    else:
        block_end = len(text)
        
    block = text[block_start:block_end]
    
    # Add keys if missing
    new_entries = []
    for k, v in translations.items():
        if f"'{k}':" not in block:
            val = k if lang == 'English' else v[lang]
            new_entries.append(f"    '{k}': '{val}',")
            
    if new_entries:
        insert_pos = block.rfind('}')
        updated_block = block[:insert_pos] + '\n' + '\n'.join(new_entries) + '\n  ' + block[insert_pos:]
        text = text[:block_start] + updated_block + text[block_end:]

with codecs.open(trans_file, 'w', 'utf-8') as f:
    f.write(text)
print("Updated translations.js successfully.")
