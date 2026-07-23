import codecs
import re

translations = {
    'High': {'Kannada': 'ಹೆಚ್ಚಿನ', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'Medium': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தர', 'Telugu': 'మధ్యస్థ'},
    'Low': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'निम्न', 'Tamil': 'குறைந்த', 'Telugu': 'తక్కువ'},
    'Critical': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'மிக முக்கியமானது', 'Telugu': 'కీలకమైన'},
    'more': {'Kannada': 'ಇನ್ನಷ್ಟು', 'Hindi': 'अधिक', 'Tamil': 'மேலும்', 'Telugu': 'మరిన్ని'},
    'No trend data': {'Kannada': 'ಯಾವುದೇ ಪ್ರವೃತ್ತಿ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'कोई प्रवृत्ति डेटा नहीं', 'Tamil': 'போக்கு தரவு இல்லை', 'Telugu': 'ట్రెండ్ డేటా లేదు'},
    'Crime Trend': {'Kannada': 'ಅಪರಾಧ ಪ್ರವೃತ್ತಿ', 'Hindi': 'अपराध प्रवृत्ति', 'Tamil': 'குற்றப் போக்கு', 'Telugu': 'నేరాల ట్రెండ్'},
    'Accept': {'Kannada': 'ಸ್ವೀಕರಿಸಿ', 'Hindi': 'स्वीकार करें', 'Tamil': 'ஏற்றுக்கொள்', 'Telugu': 'అంగీకరించండి'},
    'Dismiss': {'Kannada': 'ವಜಾಗೊಳಿಸಿ', 'Hindi': 'खारिज करें', 'Tamil': 'நிராகரி', 'Telugu': 'తిరస్కరించండి'},
    'Loading...': {'Kannada': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'लोड हो रहा है...', 'Tamil': 'ஏற்றுகிறது...', 'Telugu': 'లోడ్ అవుతోంది...'},
    'Generating...': {'Kannada': 'ರಚಿಸಲಾಗುತ್ತಿದೆ...', 'Hindi': 'जनरेट हो रहा है...', 'Tamil': 'உருவாக்குகிறது...', 'Telugu': 'ఉత్పత్తి చేస్తోంది...'},
    'No recommendations': {'Kannada': 'ಯಾವುದೇ ಶಿಫಾರಸುಗಳಿಲ್ಲ', 'Hindi': 'कोई सिफारिश नहीं', 'Tamil': 'பரிந்துரைகள் இல்லை', 'Telugu': 'సిఫార్సులు లేవు'},
    'Click "AI Generate" to create recommendations': {'Kannada': 'ಶಿಫಾರಸುಗಳನ್ನು ರಚಿಸಲು "AI ರಚಿಸಿ" ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'सिफारिशें बनाने के लिए "एआई जनरेट करें" पर क्लिक करें', 'Tamil': 'பரிந்துரைகளை உருவாக்க "AI உருவாக்கு" என்பதைக் கிளிக் செய்யவும்', 'Telugu': 'సిఫార్సులను సృష్టించడానికి "AI రూపొందించండి" క్లిక్ చేయండి'}
}

# The missing tab labels for RecommendationsPanel
rec_tabs = {
    'Cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'Suspects': {'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்கள்', 'Telugu': 'అనుమానితులు'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'सबूत', 'Tamil': 'ஆதாரம்', 'Telugu': 'సాక్ష్యం'},
    'Assign': {'Kannada': 'ನಿಯೋಜಿಸಿ', 'Hindi': 'सौंपें', 'Tamil': 'ஒதுக்கு', 'Telugu': 'కేటాయించండి'},
    'Escalation': {'Kannada': 'ಉಲ್ಬಣ', 'Hindi': 'वृद्धि', 'Tamil': 'தீவிரமடைதல்', 'Telugu': 'తీవ్రతరం'},
    'Related': {'Kannada': 'ಸಂಬಂಧಿತ', 'Hindi': 'संबंधित', 'Tamil': 'தொடர்புடைய', 'Telugu': 'సంబంధిత'}
}
translations.update(rec_tabs)

file_path = r"e:\CrimeMatrix\frontend\src\context\translations.js"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']

for lang in languages:
    new_entries = []
    for eng_key, trans_dict in translations.items():
        # Check if already exists in English block (to prevent dupes)
        # Actually I can just prepend or append. Prepending might overwrite if key exists? No, JS uses last defined. Let's just append.
        val = eng_key if lang == 'English' else trans_dict[lang]
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
