import codecs
import re

new_translations = {
    'Investigation Report — FIR #4521': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4521', 'Hindi': 'जांच रिपोर्ट — FIR #4521', 'Tamil': 'விசாரணை அறிக்கை — FIR #4521', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4521'},
    'Court Report — Theft Case #4489': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ — ಕಳ್ಳತನ ಪ್ರಕರಣ #4489', 'Hindi': 'अदालत की रिपोर्ट — चोरी का मामला #4489', 'Tamil': 'நீதிமன்ற அறிக்கை — திருட்டு வழக்கு #4489', 'Telugu': 'కోర్టు నివేదిక — దొంగతనం కేసు #4489'},
    'Investigation Report — FIR #4515': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4515', 'Hindi': 'जांच रिपोर्ट — FIR #4515', 'Tamil': 'விசாரணை அறிக்கை — FIR #4515', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4515'},
    'Court Report — Fraud Case #4498': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ — ವಂಚನೆ ಪ್ರಕರಣ #4498', 'Hindi': 'अदालत की रिपोर्ट — धोखाधड़ी का मामला #4498', 'Tamil': 'நீதிமன்ற அறிக்கை — மோசடி வழக்கு #4498', 'Telugu': 'కోర్టు నివేదిక — మోసం కేసు #4498'},
    'Investigation Report — FIR #4508': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4508', 'Hindi': 'जांच रिपोर्ट — FIR #4508', 'Tamil': 'விசாரணை அறிக்கை — FIR #4508', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4508'},
    'Export — Monthly Summary July': {'Kannada': 'ರಫ್ತು — ಮಾಸಿಕ ಸಾರಾಂಶ ಜುಲೈ', 'Hindi': 'निर्यात — मासिक सारांश जुलाई', 'Tamil': 'ஏற்றுமதி — மாதாந்திர சுருக்கம் ஜூலை', 'Telugu': 'ఎగుమతి — నెలవారీ సారాంశం జూలై'},
    'Court Report — Assault Case #4495': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ — ಹಲ್ಲೆ ಪ್ರಕರಣ #4495', 'Hindi': 'अदालत की रिपोर्ट — हमला मामला #4495', 'Tamil': 'நீதிமன்ற அறிக்கை — தாக்குதல் வழக்கு #4495', 'Telugu': 'కోర్టు నివేదిక — దాడి కేసు #4495'},
    'Investigation Report — FIR #4501': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4501', 'Hindi': 'जांच रिपोर्ट — FIR #4501', 'Tamil': 'விசாரணை அறிக்கை — FIR #4501', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4501'},
    'Export — Suspect Network Report': {'Kannada': 'ರಫ್ತು — ಶಂಕಿತ ನೆಟ್‌ವರ್ಕ್ ವರದಿ', 'Hindi': 'निर्यात — संदिग्ध नेटवर्क रिपोर्ट', 'Tamil': 'ஏற்றுமதி — சந்தேக நபர் பிணைய அறிக்கை', 'Telugu': 'ఎగుమతి — అనుమానిత నెట్‌వర్క్ నివేదిక'},
    'Investigation Report — FIR #4485': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4485', 'Hindi': 'जांच रिपोर्ट — FIR #4485', 'Tamil': 'விசாரணை அறிக்கை — FIR #4485', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4485'},
    'Court Report — Cybercrime #4485': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ — ಸೈಬರ್ ಅಪರಾಧ #4485', 'Hindi': 'अदालत की रिपोर्ट — साइबर अपराध #4485', 'Tamil': 'நீதிமன்ற அறிக்கை — சைபர் கிரைம் #4485', 'Telugu': 'కోర్టు నివేదిక — సైబర్‌క్రైమ్ #4485'},
    'Investigation Report — FIR #4475': {'Kannada': 'ತನಿಖಾ ವರದಿ — FIR #4475', 'Hindi': 'जांच रिपोर्ट — FIR #4475', 'Tamil': 'விசாரணை அறிக்கை — FIR #4475', 'Telugu': 'దర్యాప్తు నివేదిక — FIR #4475'},

    'FIR #4521': {'Kannada': 'FIR #4521', 'Hindi': 'FIR #4521', 'Tamil': 'FIR #4521', 'Telugu': 'FIR #4521'},
    'FIR #4489': {'Kannada': 'FIR #4489', 'Hindi': 'FIR #4489', 'Tamil': 'FIR #4489', 'Telugu': 'FIR #4489'},
    'FIR #4515': {'Kannada': 'FIR #4515', 'Hindi': 'FIR #4515', 'Tamil': 'FIR #4515', 'Telugu': 'FIR #4515'},
    'FIR #4498': {'Kannada': 'FIR #4498', 'Hindi': 'FIR #4498', 'Tamil': 'FIR #4498', 'Telugu': 'FIR #4498'},
    'FIR #4508': {'Kannada': 'FIR #4508', 'Hindi': 'FIR #4508', 'Tamil': 'FIR #4508', 'Telugu': 'FIR #4508'},
    'Monthly': {'Kannada': 'ಮಾಸಿಕ', 'Hindi': 'मासिक', 'Tamil': 'மாதாந்திர', 'Telugu': 'నెలవారీ'},
    'FIR #4495': {'Kannada': 'FIR #4495', 'Hindi': 'FIR #4495', 'Tamil': 'FIR #4495', 'Telugu': 'FIR #4495'},
    'FIR #4501': {'Kannada': 'FIR #4501', 'Hindi': 'FIR #4501', 'Tamil': 'FIR #4501', 'Telugu': 'FIR #4501'},
    'Network': {'Kannada': 'ನೆಟ್ವರ್ಕ್', 'Hindi': 'नेटवर्क', 'Tamil': 'நெட்வொர்க்', 'Telugu': 'నెట్‌వర్క్'},
    'FIR #4485': {'Kannada': 'FIR #4485', 'Hindi': 'FIR #4485', 'Tamil': 'FIR #4485', 'Telugu': 'FIR #4485'},
    'FIR #4475': {'Kannada': 'FIR #4475', 'Hindi': 'FIR #4475', 'Tamil': 'FIR #4475', 'Telugu': 'FIR #4475'},

    'SI Karthik': {'Kannada': 'SI ಕಾರ್ತಿಕ್', 'Hindi': 'SI कार्तिक', 'Tamil': 'SI கார்த்திக்', 'Telugu': 'SI కార్తీక్'},
    'Inspector Deepak': {'Kannada': 'ಇನ್ಸ್ಪೆಕ್ಟರ್ ದೀಪಕ್', 'Hindi': 'इंस्पेक्टर दीपक', 'Tamil': 'இன்ஸ்பெக்டர் தீபக்', 'Telugu': 'ఇన్స్పెక్టర్ దీపక్'},
    'SI Priya': {'Kannada': 'SI ಪ್ರಿಯಾ', 'Hindi': 'SI प्रिया', 'Tamil': 'SI பிரியா', 'Telugu': 'SI ప్రియా'},
    'System': {'Kannada': 'ಸಿಸ್ಟಮ್', 'Hindi': 'सिस्टम', 'Tamil': 'கணினி', 'Telugu': 'సిస్టమ్'},

    'Jul 15, 2026': {'Kannada': 'ಜುಲೈ 15, 2026', 'Hindi': 'जुलाई 15, 2026', 'Tamil': 'ஜூலை 15, 2026', 'Telugu': 'జూలై 15, 2026'},
    'Jul 14, 2026': {'Kannada': 'ಜುಲೈ 14, 2026', 'Hindi': 'जुलाई 14, 2026', 'Tamil': 'ஜூலை 14, 2026', 'Telugu': 'జూలై 14, 2026'},
    'Jul 13, 2026': {'Kannada': 'ಜುಲೈ 13, 2026', 'Hindi': 'जुलाई 13, 2026', 'Tamil': 'ஜூலை 13, 2026', 'Telugu': 'జూలై 13, 2026'},
    'Jul 12, 2026': {'Kannada': 'ಜುಲೈ 12, 2026', 'Hindi': 'जुलाई 12, 2026', 'Tamil': 'ஜூலை 12, 2026', 'Telugu': 'జూలై 12, 2026'},
    'Jul 11, 2026': {'Kannada': 'ಜುಲೈ 11, 2026', 'Hindi': 'जुलाई 11, 2026', 'Tamil': 'ஜூலை 11, 2026', 'Telugu': 'జూలై 11, 2026'},
    'Jul 10, 2026': {'Kannada': 'ಜುಲೈ 10, 2026', 'Hindi': 'जुलाई 10, 2026', 'Tamil': 'ஜூலை 10, 2026', 'Telugu': 'జూలై 10, 2026'},
    'Jul 9, 2026': {'Kannada': 'ಜುಲೈ 9, 2026', 'Hindi': 'जुलाई 9, 2026', 'Tamil': 'ஜூலை 9, 2026', 'Telugu': 'జూலை 9, 2026'},
    'Jul 8, 2026': {'Kannada': 'ಜುಲೈ 8, 2026', 'Hindi': 'जुलाई 8, 2026', 'Tamil': 'ஜூலை 8, 2026', 'Telugu': 'జూలై 8, 2026'},
    'Jul 7, 2026': {'Kannada': 'ಜುಲೈ 7, 2026', 'Hindi': 'जुलाई 7, 2026', 'Tamil': 'ஜூலை 7, 2026', 'Telugu': 'జూలై 7, 2026'},
    'Jul 6, 2026': {'Kannada': 'ಜುಲೈ 6, 2026', 'Hindi': 'जुलाई 6, 2026', 'Tamil': 'ஜூலை 6, 2026', 'Telugu': 'జూలై 6, 2026'},
    'Jul 5, 2026': {'Kannada': 'ಜುಲೈ 5, 2026', 'Hindi': 'जुलाई 5, 2026', 'Tamil': 'ஜூலை 5, 2026', 'Telugu': 'జూలై 5, 2026'},
    'Jul 4, 2026': {'Kannada': 'ಜುಲೈ 4, 2026', 'Hindi': 'जुलाई 4, 2026', 'Tamil': 'ஜூலை 4, 2026', 'Telugu': 'జూలై 4, 2026'}
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
