import re
import codecs

translations = {
    'Select a Node': {
        'Kannada': 'ಒಂದು ನೋಡ್ ಅನ್ನು ಆಯ್ಕೆಮಾಡಿ', 'Hindi': 'एक नोड चुनें', 'Tamil': 'ஒரு முனையைத் தேர்ந்தெடுக்கவும்', 'Telugu': 'ఒక నోడ్‌ని ఎంచుకోండి'
    },
    'Click on any node in the graph to view details': {
        'Kannada': 'ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಗ್ರಾಫ್‌ನಲ್ಲಿರುವ ಯಾವುದೇ ನೋಡ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'विवरण देखने के लिए ग्राफ़ में किसी भी नोड पर क्लिक करें', 'Tamil': 'விவரங்களைப் பார்க்க வரைபடத்தில் உள்ள எந்த முனையிலும் கிளிக் செய்யவும்', 'Telugu': 'వివరాలను వీక్షించడానికి గ్రాఫ్‌లోని ఏదైనా నోడ్‌పై క్లిక్ చేయండి'
    },
    'Risk': {
        'Kannada': 'ಅಪಾಯ', 'Hindi': 'जोखिम', 'Tamil': 'ஆபத்து', 'Telugu': 'ప్రమాదం'
    },
    'Cases': {
        'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'
    },
    'Connections': {
        'Kannada': 'ಸಂಪರ್ಕಗಳು', 'Hindi': 'कनेक्शन', 'Tamil': 'இணைப்புகள்', 'Telugu': 'కనెక్షన్లు'
    },
    'View Full Profile': {
        'Kannada': 'ಪೂರ್ಣ ಪ್ರೊಫೈಲ್ ವೀಕ್ಷಿಸಿ', 'Hindi': 'पूरी प्रोफ़ाइल देखें', 'Tamil': 'முழு சுயவிவரத்தைக் காண்க', 'Telugu': 'పూర్తి ప్రొఫైల్‌ను వీక్షించండి'
    },
    'Add to Investigation': {
        'Kannada': 'ತನಿಖೆಗೆ ಸೇರಿಸಿ', 'Hindi': 'जांच में जोड़ें', 'Tamil': 'விசாரணையில் சேர்க்கவும்', 'Telugu': 'దర్యాప్తుకు జోడించండి'
    },
    'Suspect': {
        'Kannada': 'ಶಂಕಿತ', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்', 'Telugu': 'అనుమానితుడు'
    },
    'Vehicle': {
        'Kannada': 'ವಾಹನ', 'Hindi': 'वाहन', 'Tamil': 'வாகனம்', 'Telugu': 'వాహనం'
    },
    'Phone': {
        'Kannada': 'ಫೋನ್', 'Hindi': 'फ़ोन', 'Tamil': 'தொலைபேசி', 'Telugu': 'ఫోన్'
    },
    'Criminal': {
        'Kannada': 'ಅಪರಾಧಿ', 'Hindi': 'अपराधी', 'Tamil': 'குற்றவாளி', 'Telugu': 'నేరస్థుడు'
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
