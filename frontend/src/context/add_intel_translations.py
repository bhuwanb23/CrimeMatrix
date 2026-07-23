import codecs

translations = {
    'District': {'Kannada': 'ಜಿಲ್ಲೆ', 'Hindi': 'ज़िला', 'Tamil': 'மாவட்டம்', 'Telugu': 'జిల్లా'},
    'All Districts': {'Kannada': 'ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು', 'Hindi': 'सभी जिले', 'Tamil': 'அனைத்து மாவட்டங்களும்', 'Telugu': 'అన్ని జిల్లాలు'},
    'Time Range': {'Kannada': 'ಸಮಯದ ಶ್ರೇಣಿ', 'Hindi': 'समय सीमा', 'Tamil': 'நேர வரம்பு', 'Telugu': 'సమయ పరిధి'},
    '7 Days': {'Kannada': '7 ದಿನಗಳು', 'Hindi': '7 दिन', 'Tamil': '7 நாட்கள்', 'Telugu': '7 రోజులు'},
    '30 Days': {'Kannada': '30 ದಿನಗಳು', 'Hindi': '30 दिन', 'Tamil': '30 நாட்கள்', 'Telugu': '30 రోజులు'},
    '90 Days': {'Kannada': '90 ದಿನಗಳು', 'Hindi': '90 दिन', 'Tamil': '90 நாட்கள்', 'Telugu': '90 రోజులు'},
    '1 Year': {'Kannada': '1 ವರ್ಷ', 'Hindi': '1 वर्ष', 'Tamil': '1 வருடம்', 'Telugu': '1 సంవత్సరం'},
    'Crime Type': {'Kannada': 'ಅಪರಾಧ ಪ್ರಕಾರ', 'Hindi': 'अपराध का प्रकार', 'Tamil': 'குற்ற வகை', 'Telugu': 'నేర రకం'},
    'All Types': {'Kannada': 'ಎಲ್ಲಾ ಪ್ರಕಾರಗಳು', 'Hindi': 'सभी प्रकार', 'Tamil': 'அனைத்து வகைகளும்', 'Telugu': 'అన్ని రకాలు'},
    'Reset': {'Kannada': 'ಮರುಹೊಂದಿಸಿ', 'Hindi': 'रीसेट', 'Tamil': 'மீட்டமை', 'Telugu': 'రీసెట్ చేయండి'},
    'Total Crimes': {'Kannada': 'ಒಟ್ಟು ಅಪರಾಧಗಳು', 'Hindi': 'कुल अपराध', 'Tamil': 'மொத்த குற்றங்கள்', 'Telugu': 'మొత్తం నేరాలు'},
    'Open Cases': {'Kannada': 'ತೆರೆದ ಪ್ರಕರಣಗಳು', 'Hindi': 'खुले मामले', 'Tamil': 'திறந்த வழக்குகள்', 'Telugu': 'ఓపెన్ కేసులు'},
    'Resolution Rate': {'Kannada': 'ಪರಿಹಾರ ದರ', 'Hindi': 'समाधान दर', 'Tamil': 'தீர்வு விகிதம்', 'Telugu': 'రిజల్యూషన్ రేటు'},
    'Active Investigations': {'Kannada': 'ಸಕ್ರಿಯ ತನಿಖೆಗಳು', 'Hindi': 'सक्रिय जांच', 'Tamil': 'செயலில் உள்ள விசாரணைகள்', 'Telugu': 'చురుకైన దర్యాప్తులు'},
    'Criminals at large': {'Kannada': 'ತಲೆಮರೆಸಿಕೊಂಡಿರುವ ಅಪರಾಧಿಗಳು', 'Hindi': 'फ़रार अपराधी', 'Tamil': 'தலைமறைவாக உள்ள குற்றவாளிகள்', 'Telugu': 'పరారీలో ఉన్న నేరస్థులు'},
    'Crime Trend (30d)': {'Kannada': 'ಅಪರಾಧ ಪ್ರವೃತ್ತಿ (30 ದಿನಗಳು)', 'Hindi': 'अपराध प्रवृत्ति (30 दिन)', 'Tamil': 'குற்றப் போக்கு (30நா)', 'Telugu': 'నేరాల ట్రెండ్ (30 రోజులు)'},
    'avg': {'Kannada': 'ಸರಾಸರಿ', 'Hindi': 'औसत', 'Tamil': 'சராசரி', 'Telugu': 'సగటు'},
    'Total': {'Kannada': 'ಒಟ್ಟು', 'Hindi': 'कुल', 'Tamil': 'மொத்தம்', 'Telugu': 'మొత్తం'},
    'periods': {'Kannada': 'ಅವಧಿಗಳು', 'Hindi': 'अवधि', 'Tamil': 'காலங்கள்', 'Telugu': 'పీరియడ్స్'},
    'Crime Heatmap': {'Kannada': 'ಅಪರಾಧ ಹೀಟ್‌ಮ್ಯಾಪ್', 'Hindi': 'अपराध हीटमैप', 'Tamil': 'குற்ற வெப்ப வரைபடம்', 'Telugu': 'క్రైమ్ హీట్‌మ్యాప్'},
    'No heatmap data': {'Kannada': 'ಯಾವುದೇ ಹೀಟ್‌ಮ್ಯಾಪ್ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'कोई हीटमैप डेटा नहीं', 'Tamil': 'வெப்ப வரைபட தரவு இல்லை', 'Telugu': 'హీట్‌మ్యాప్ డేటా లేదు'},
    'Top Crime Types': {'Kannada': 'ಉನ್ನತ ಅಪರಾಧ ಪ್ರಕಾರಗಳು', 'Hindi': 'शीर्ष अपराध प्रकार', 'Tamil': 'சிறந்த குற்ற வகைகள்', 'Telugu': 'టాప్ క్రైమ్ రకాలు'},
    'Hotspot Rankings': {'Kannada': 'ಹಾಟ್‌ಸ್ಪಾಟ್ ಶ್ರೇಯಾಂಕಗಳು', 'Hindi': 'हॉटस्पॉट रैंकिंग', 'Tamil': 'ஹாட்ஸ்பாட் தரவரிசை', 'Telugu': 'హాట్‌స్పాట్ ర్యాంకింగ్‌లు'},
    'No hotspots detected': {'Kannada': 'ಯಾವುದೇ ಹಾಟ್‌ಸ್ಪಾಟ್‌ಗಳು ಪತ್ತೆಯಾಗಿಲ್ಲ', 'Hindi': 'कोई हॉटस्पॉट नहीं मिला', 'Tamil': 'ஹாட்ஸ்பாட்கள் எதுவும் கண்டறியப்படவில்லை', 'Telugu': 'హాట్‌స్పాట్‌లు ఏవీ కనుగొనబడలేదు'},
    'Risk Zones': {'Kannada': 'ಅಪಾಯದ ವಲಯಗಳು', 'Hindi': 'जोखिम क्षेत्र', 'Tamil': 'ஆபத்து மண்டலங்கள்', 'Telugu': 'ప్రమాద మండలాలు'},
    'District Comparison': {'Kannada': 'ಜಿಲ್ಲಾ ಹೋಲಿಕೆ', 'Hindi': 'ज़िला तुलना', 'Tamil': 'மாவட்ட ஒப்பீடு', 'Telugu': 'జిల్లా పోలిక'},
    'No district data': {'Kannada': 'ಯಾವುದೇ ಜಿಲ್ಲಾ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'कोई ज़िला डेटा नहीं', 'Tamil': 'மாவட்ட தரவு இல்லை', 'Telugu': 'జిల్లా డేటా లేదు'},
    'Seasonal Patterns': {'Kannada': 'ಋತುಮಾನದ ಮಾದರಿಗಳು', 'Hindi': 'मौसमी पैटर्न', 'Tamil': 'பருவகால வடிவங்கள்', 'Telugu': 'కాలానుగుణ నమూనాలు'},
    'By Hour': {'Kannada': 'ಗಂಟೆಯ ಪ್ರಕಾರ', 'Hindi': 'घंटे के अनुसार', 'Tamil': 'மணிநேரப்படி', 'Telugu': 'గంట ద్వారా'},
    'By Day': {'Kannada': 'ದಿನದ ಪ್ರಕಾರ', 'Hindi': 'दिन के अनुसार', 'Tamil': 'நாளின்படி', 'Telugu': 'రోజు ద్వారా'},
    'By Month': {'Kannada': 'ತಿಂಗಳ ಪ್ರಕಾರ', 'Hindi': 'महीने के अनुसार', 'Tamil': 'மாதப்படி', 'Telugu': 'నెల ద్వారా'},
    'Active Criminals': {'Kannada': 'ಸಕ್ರಿಯ ಅಪರಾಧಿಗಳು', 'Hindi': 'सक्रिय अपराधी', 'Tamil': 'செயலில் உள்ள குற்றவாளிகள்', 'Telugu': 'యాక్టివ్ క్రిమినల్స్'},
    'High Risk': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯ', 'Hindi': 'उच्च जोखिम', 'Tamil': 'அதிக ஆபத்து', 'Telugu': 'అధిక ప్రమాదం'},
    'Total Victims': {'Kannada': 'ಒಟ್ಟು ಬಲಿಪಶುಗಳು', 'Hindi': 'कुल पीड़ित', 'Tamil': 'மொத்த பாதிக்கப்பட்டவர்கள்', 'Telugu': 'మొత్తం బాధితులు'},
    'Witnesses': {'Kannada': 'ಸಾಕ್ಷಿಗಳು', 'Hindi': 'गवाह', 'Tamil': 'சாட்சிகள்', 'Telugu': 'సాక్షులు'},
    'Insights': {'Kannada': 'ಒಳನೋಟಗಳು', 'Hindi': 'अंतर्दृष्टि', 'Tamil': 'நுண்ணறிவு', 'Telugu': 'అంతర్దృష్టులు'},
    'Recommendations': {'Kannada': 'ಶಿಫಾರಸುಗಳು', 'Hindi': 'सिफारिशें', 'Tamil': 'பரிந்துரைகள்', 'Telugu': 'సిఫార్సులు'},
    'AI Generate': {'Kannada': 'AI ರಚಿಸಿ', 'Hindi': 'एआई जनरेट करें', 'Tamil': 'AI உருவாக்கு', 'Telugu': 'AI రూపొందించండి'},
    'All': {'Kannada': 'ಎಲ್ಲಾ', 'Hindi': 'सभी', 'Tamil': 'அனைத்து', 'Telugu': 'అన్ని'},
    'No recommendations yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಶಿಫಾರಸುಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई सिफारिश नहीं', 'Tamil': 'பரிந்துரைகள் ஏதும் இல்லை', 'Telugu': 'ఇంకా సిఫార్సులు లేవు'},
    'Patterns & Timeline': {'Kannada': 'ಮಾದರಿಗಳು ಮತ್ತು ಟೈಮ್‌ಲೈನ್', 'Hindi': 'पैटर्न और टाइमलाइन', 'Tamil': 'வடிவங்கள் மற்றும் காலவரிசை', 'Telugu': 'నమూనాలు & టైమ్‌లైన్'},
    'Crime pattern discovery and criminal timeline tracking': {'Kannada': 'ಅಪರಾಧ ಮಾದರಿ ಅನ್ವೇಷಣೆ ಮತ್ತು ಅಪರಾಧದ ಟೈಮ್‌ಲೈನ್ ಟ್ರ್ಯಾಕಿಂಗ್', 'Hindi': 'अपराध पैटर्न की खोज और आपराधिक टाइमलाइन ट्रैकिंग', 'Tamil': 'குற்ற முறை கண்டுபிடிப்பு மற்றும் குற்றவியல் காலவரிசை கண்காணிப்பு', 'Telugu': 'క్రైమ్ ప్యాటర్న్ డిస్కవరీ మరియు క్రిమినల్ టైమ్‌లైన్ ట్రాకింగ్'},
    'Patterns': {'Kannada': 'ಮಾದರಿಗಳು', 'Hindi': 'पैटर्न', 'Tamil': 'வடிவங்கள்', 'Telugu': 'నమూనాలు'},
    'Crime Pattern Discovery': {'Kannada': 'ಅಪರಾಧ ಮಾದರಿ ಅನ್ವೇಷಣೆ', 'Hindi': 'अपराध पैटर्न की खोज', 'Tamil': 'குற்ற முறை கண்டுபிடிப்பு', 'Telugu': 'క్రైమ్ ప్యాటర్న్ డిస్కవరీ'},
    'Automatically identify recurring crime patterns': {'Kannada': 'ಮರುಕಳಿಸುವ ಅಪರಾಧ ಮಾದರಿಗಳನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಗುರುತಿಸಿ', 'Hindi': 'बार-बार होने वाले अपराध पैटर्न को स्वचालित रूप से पहचानें', 'Tamil': 'மீண்டும் மீண்டும் நிகழும் குற்ற முறைகளை தானாகவே கண்டறியவும்', 'Telugu': 'పునరావృతమయ్యే నేరాల నమూనాలను స్వయంచాలకంగా గుర్తించండి'},
    'Detect Patterns': {'Kannada': 'ಮಾದರಿಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿ', 'Hindi': 'पैटर्न का पता लगाएं', 'Tamil': 'வடிவங்களைக் கண்டறியவும்', 'Telugu': 'నమూనాలను గుర్తించండి'},
    'patterns': {'Kannada': 'ಮಾದರಿಗಳು', 'Hindi': 'पैटर्न', 'Tamil': 'வடிவங்கள்', 'Telugu': 'నమూనాలు'},
    'occurrences': {'Kannada': 'ಸಂಭವಿಸುವಿಕೆಗಳು', 'Hindi': 'घटनाएं', 'Tamil': 'நிகழ்வுகள்', 'Telugu': 'సంభవాలు'},
    'clusters': {'Kannada': 'ಕ್ಲಸ್ಟರ್‌ಗಳು', 'Hindi': 'क्लस्टर', 'Tamil': 'கொத்துகள்', 'Telugu': 'క్లస్టర్లు'},
    'Time': {'Kannada': 'ಸಮಯ', 'Hindi': 'समय', 'Tamil': 'நேரம்', 'Telugu': 'సమయం'},
    'MO': {'Kannada': 'MO', 'Hindi': 'MO', 'Tamil': 'MO', 'Telugu': 'MO'},
    'Location': {'Kannada': 'ಸ್ಥಳ', 'Hindi': 'स्थान', 'Tamil': 'இடம்', 'Telugu': 'స్థానం'},
    'No patterns detected yet': {'Kannada': 'ಯಾವುದೇ ಮಾದರಿಗಳು ಪತ್ತೆಯಾಗಿಲ್ಲ', 'Hindi': 'अभी तक कोई पैटर्न नहीं मिला', 'Tamil': 'வடிவங்கள் எதுவும் கண்டறியப்படவில்லை', 'Telugu': 'ఇంకా నమూనాలు ఏవీ కనుగొనబడలేదు'},
    'Click "Detect Patterns" to analyze crime data for recurring patterns.': {'Kannada': 'ಮರುಕಳಿಸುವ ಮಾದರಿಗಳಿಗಾಗಿ ಅಪರಾಧ ಡೇಟಾವನ್ನು ವಿಶ್ಲೇಷಿಸಲು "ಮಾದರಿಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿ" ಕ್ಲಿಕ್ ಮಾಡಿ.', 'Hindi': 'बार-बार होने वाले पैटर्न के लिए अपराध डेटा का विश्लेषण करने के लिए "पैटर्न का पता लगाएं" पर क्लिक करें।', 'Tamil': 'மீண்டும் நிகழும் வடிவங்களுக்கு குற்றத் தரவை பகுப்பாய்வு செய்ய "வடிவங்களைக் கண்டறி" என்பதைக் கிளிக் செய்யவும்.', 'Telugu': 'పునరావృతమయ్యే నమూనాల కోసం క్రైమ్ డేటాను విశ్లేషించడానికి "నమూనాలను గుర్తించండి" క్లిక్ చేయండి.'}
}

file_path = r"e:\CrimeMatrix\frontend\src\context\translations.js"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']

for lang in languages:
    new_entries = []
    for eng_key, trans_dict in translations.items():
        val = eng_key if lang == 'English' else trans_dict[lang]
        # Escape single quotes
        eng_key_esc = eng_key.replace("'", "\\'")
        val_esc = val.replace("'", "\\'")
        new_entries.append(f"'{eng_key_esc}': '{val_esc}'")
    
    entries_str = ", ".join(new_entries)
    
    if lang != 'Telugu':
        next_langs = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}
        next_lang = next_langs[lang]
        pattern = f"\n  }},\n  {next_lang}:"
        content = content.replace(pattern, f",\n    {entries_str}\n  }},\n  {next_lang}:")
    else:
        pattern = f"\n  }}\n}}"
        content = content.replace(pattern, f",\n    {entries_str}\n  }}\n}}")

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)
