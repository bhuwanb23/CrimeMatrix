import re
import codecs

translations = {
    'All Connections': {
        'Kannada': 'ಎಲ್ಲಾ ಸಂಪರ್ಕಗಳು', 'Hindi': 'सभी कनेक्शन', 'Tamil': 'அனைத்து இணைப்புகளும்', 'Telugu': 'అన్ని కనెక్షన్లు'
    },
    'Criminal Network': {
        'Kannada': 'ಕ್ರಿಮಿನಲ್ ನೆಟ್ವರ್ಕ್', 'Hindi': 'आपराधिक नेटवर्क', 'Tamil': 'குற்றவியல் நெட்வொர்க்', 'Telugu': 'క్రిమినల్ నెట్‌వర్క్'
    },
    'Gang Network': {
        'Kannada': 'ಗ್ಯಾಂಗ್ ನೆಟ್ವರ್ಕ್', 'Hindi': 'गैंग नेटवर्क', 'Tamil': 'கும்பல் நெட்வொர்க்', 'Telugu': 'గ్యాంగ్ నెట్‌వర్క్'
    },
    'Evidence Links': {
        'Kannada': 'ಸಾಕ್ಷ್ಯದ ಲಿಂಕ್‌ಗಳು', 'Hindi': 'साक्ष्य लिंक', 'Tamil': 'ஆதார இணைப்புகள்', 'Telugu': 'సాక్ష్యం లింక్‌లు'
    },
    'Suspects': {
        'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்கள்', 'Telugu': 'అనుమానితులు'
    },
    'Criminals': {
        'Kannada': 'ಅಪರಾಧಿಗಳು', 'Hindi': 'अपराधी', 'Tamil': 'குற்றவாளிகள்', 'Telugu': 'నేరస్థులు'
    },
    'Evidence': {
        'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'साक्ष्य', 'Tamil': 'ஆதாரம்', 'Telugu': 'సాక్ష్యం'
    },
    'Vehicles': {
        'Kannada': 'ವಾಹನಗಳು', 'Hindi': 'वाहन', 'Tamil': 'வாகனங்கள்', 'Telugu': 'వాహనాలు'
    },
    'Phones': {
        'Kannada': 'ಫೋನ್‌ಗಳು', 'Hindi': 'फ़ोन', 'Tamil': 'தொலைபேசிகள்', 'Telugu': 'ఫోన్‌లు'
    },
    'Zoom in': {
        'Kannada': 'ಜೂಮ್ ಇನ್', 'Hindi': 'ज़ूम इन', 'Tamil': 'பெரிதாக்கு', 'Telugu': 'జూమ్ ఇన్'
    },
    'Zoom out': {
        'Kannada': 'ಜೂಮ್ ಔಟ್', 'Hindi': 'ज़ूम आउट', 'Tamil': 'சிறிதாக்கு', 'Telugu': 'జూమ్ అవుట్'
    },
    'Reset view': {
        'Kannada': 'ವೀಕ್ಷಣೆಯನ್ನು ಮರುಹೊಂದಿಸಿ', 'Hindi': 'दृश्य रीसेट करें', 'Tamil': 'காட்சியை மீட்டமை', 'Telugu': 'వీక్షణను రీసెట్ చేయండి'
    },
    'Cases Today': {
        'Kannada': 'ಇಂದು ಪ್ರಕರಣಗಳು', 'Hindi': 'आज के मामले', 'Tamil': 'இன்றைய வழக்குகள்', 'Telugu': 'ఈరోజు కేసులు'
    },
    'Pending': {
        'Kannada': 'ಬಾಕಿ ಇದೆ', 'Hindi': 'लंबित', 'Tamil': 'நிலுவையில்', 'Telugu': 'పెండింగ్‌లో ఉంది'
    },
    'Resolution': {
        'Kannada': 'ರೆಸಲ್ಯೂಶನ್', 'Hindi': 'संकल्प', 'Tamil': 'தீர்வு', 'Telugu': 'రిజల్యూషన్'
    },
    'Activity': {
        'Kannada': 'ಚಟುವಟಿಕೆ', 'Hindi': 'गतिविधि', 'Tamil': 'செயல்பாடு', 'Telugu': 'కార్యకలాపం'
    },
    'Today\\'s Overview': {
        'Kannada': 'ಇಂದಿನ ಅವಲೋಕನ', 'Hindi': 'आज का अवलोकन', 'Tamil': 'இன்றைய கண்ணோட்டம்', 'Telugu': 'నేటి అవలోకనం'
    },
    'Recent Activity': {
        'Kannada': 'ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ', 'Hindi': 'हाल की गतिविधि', 'Tamil': 'சமீபத்திய செயல்பாடு', 'Telugu': 'ఇటీవలి కార్యాచరణ'
    },
    'Ask about cases...': {
        'Kannada': 'ಪ್ರಕರಣಗಳ ಬಗ್ಗೆ ಕೇಳಿ...', 'Hindi': 'मामलों के बारे में पूछें...', 'Tamil': 'வழக்குகள் பற்றி கேளுங்கள்...', 'Telugu': 'కేసుల గురించి అడగండి...'
    },
    'Dashboard': {
        'Kannada': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'Hindi': 'डैशबोर्ड', 'Tamil': 'கட்டுப்பாட்டகம்', 'Telugu': 'డాష్‌బోర్డ్'
    },
    'Pattern-Timeline': {
        'Kannada': 'ಮಾದರಿ-ಟೈಮ್‌ಲೈನ್', 'Hindi': 'पैटर्न-टाइमलाइन', 'Tamil': 'வடிவம்-காலவரிசை', 'Telugu': 'నమూనా-టైమ్‌లైన్'
    },
    'Predictions': {
        'Kannada': 'ಭವಿಷ್ಯವಾಣಿಗಳು', 'Hindi': 'भविष्यवाणियां', 'Tamil': 'கணிப்புகள்', 'Telugu': 'అంచనాలు'
    },
    'Risk Score': {
        'Kannada': 'ಅಪಾಯದ ಅಂಕ', 'Hindi': 'जोखिम स्कोर', 'Tamil': 'ஆபத்து மதிப்பெண்', 'Telugu': 'ప్రమాద స్కోర్'
    },
    'Priority & Proactive': {
        'Kannada': 'ಆದ್ಯತೆ ಮತ್ತು ಪೂರ್ವಭಾವಿ', 'Hindi': 'प्राथमिकता और सक्रिय', 'Tamil': 'முன்னுரிமை & செயலில்', 'Telugu': 'ప్రాధాన్యత & చురుకైనది'
    },
    'Timeline': {
        'Kannada': 'ಟೈಮ್‌ಲೈನ್', 'Hindi': 'टाइमलाइन', 'Tamil': 'காலவரிசை', 'Telugu': 'టైమ్‌లైన్'
    },
    'Search': {
        'Kannada': 'ಹುಡುಕಾಟ', 'Hindi': 'खोज', 'Tamil': 'தேடல்', 'Telugu': 'శోధన'
    },
    'Stations': {
        'Kannada': 'ನಿಲ್ದಾಣಗಳು', 'Hindi': 'स्टेशन', 'Tamil': 'நிலையங்கள்', 'Telugu': 'స్టేషన్లు'
    },
    'Investigations': {
        'Kannada': 'ತನಿಖೆಗಳು', 'Hindi': 'जांच', 'Tamil': 'விசாரணைகள்', 'Telugu': 'దర్యాప్తులు'
    },
    'Reports': {
        'Kannada': 'ವರದಿಗಳು', 'Hindi': 'रिपोर्ट', 'Tamil': 'அறிக்கைகள்', 'Telugu': 'నివేదికలు'
    },
    'Settings': {
        'Kannada': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು', 'Hindi': 'सेटिंग्स', 'Tamil': 'அமைப்புகள்', 'Telugu': 'సెట్టింగ్‌లు'
    },
    'Analytics': {
        'Kannada': 'ಅನಾಲಿಟಿಕ್ಸ್', 'Hindi': 'एनालिटिक्स', 'Tamil': 'பகுப்பாய்வு', 'Telugu': 'ఎనలిటిక్స్'
    },
    'Knowledge Graph': {
        'Kannada': 'ನಾಲೆಡ್ಜ್ ಗ್ರಾಫ್', 'Hindi': 'नॉलेज ग्राफ', 'Tamil': 'அறிவு வரைபடம்', 'Telugu': 'నాలెడ్జ్ గ్రాఫ్'
    },
    'CrimeMatrix': {
        'Kannada': 'ಕ್ರೈಮ್‌ಮ್ಯಾಟ್ರಿಕ್ಸ್', 'Hindi': 'क्राइममैट्रिक्स', 'Tamil': 'க்ரைம்மேட்ரிக்ஸ்', 'Telugu': 'క్రైమ్‌మ్యాట్రిక్స్'
    },
    'Alerts': {
        'Kannada': 'ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'अलर्ट', 'Tamil': 'எச்சரிக்கைகள்', 'Telugu': 'అలర్ట్‌లు'
    }
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
    
    # We will replace `\n  },\n  Kannada:` with `,\n    ` + entries_str + `\n  },\n  Kannada:`
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
