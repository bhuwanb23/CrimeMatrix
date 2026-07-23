import os
import re
import codecs

translations = {
    'AI Predictions & Recommendations': {'Kannada': 'AI ಮುನ್ಸೂಚನೆಗಳು ಮತ್ತು ಶಿಫಾರಸುಗಳು', 'Hindi': 'एआई भविष्यवाणियां और सिफारिशें', 'Tamil': 'AI கணிப்புகள் மற்றும் பரிந்துரைகள்', 'Telugu': 'AI అంచనాలు & సిఫార్సులు'},
    'Avg Confidence': {'Kannada': 'ಸರಾಸರಿ ವಿಶ್ವಾಸ', 'Hindi': 'औसत विश्वास', 'Tamil': 'சராசரி நம்பிக்கை', 'Telugu': 'సగటు విశ్వాసం'},
    'Click Explain to see why this prediction was made': {'Kannada': 'ಈ ಮುನ್ಸೂಚನೆಯನ್ನು ಏಕೆ ಮಾಡಲಾಗಿದೆ ಎಂದು ನೋಡಲು ವಿವರಿಸಿ ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'यह भविष्यवाणी क्यों की गई, यह देखने के लिए समझाएं पर क्लिक करें', 'Tamil': 'இந்த கணிப்பு ஏன் செய்யப்பட்டது என்பதை அறிய விளக்கு என்பதைக் கிளிக் செய்யவும்', 'Telugu': 'ఈ అంచనా ఎందుకు చేయబడిందో చూడటానికి వివరించండి క్లిక్ చేయండి'},
    'Confidence:': {'Kannada': 'ವಿಶ್ವಾಸ:', 'Hindi': 'विश्वास:', 'Tamil': 'நம்பிக்கை:', 'Telugu': 'విశ్వాసం:'},
    'Contributing Factors': {'Kannada': 'ಕೊಡುಗೆ ನೀಡುವ ಅಂಶಗಳು', 'Hindi': 'योगदान करने वाले कारक', 'Tamil': 'பங்களிக்கும் காரணிகள்', 'Telugu': 'దోహదపడే అంశాలు'},
    'Data Sources': {'Kannada': 'ಡೇಟಾ ಮೂಲಗಳು', 'Hindi': 'डेटा स्रोत', 'Tamil': 'தரவு ஆதாரங்கள்', 'Telugu': 'డేటా మూలాలు'},
    'Data points': {'Kannada': 'ಡೇಟಾ ಬಿಂದುಗಳು', 'Hindi': 'डेटा बिंदु', 'Tamil': 'தரவு புள்ளிகள்', 'Telugu': 'డేటా పాయింట్లు'},
    'District Forecast': {'Kannada': 'ಜಿಲ್ಲಾ ಮುನ್ಸೂಚನೆ', 'Hindi': 'ज़िला पूर्वानुमान', 'Tamil': 'மாவட்ட முன்னறிவிப்பு', 'Telugu': 'జిల్లా సూచన'},
    'District:': {'Kannada': 'ಜಿಲ್ಲೆ:', 'Hindi': 'ज़िला:', 'Tamil': 'மாவட்டம்:', 'Telugu': 'జిల్లా:'},
    'Evidence Sources': {'Kannada': 'ಸಾಕ್ಷ್ಯದ ಮೂಲಗಳು', 'Hindi': 'साक्ष्य के स्रोत', 'Tamil': 'ஆதார ஆதாரங்கள்', 'Telugu': 'సాక్ష్యం మూలాలు'},
    'Forecast Confidence': {'Kannada': 'ಮುನ್ಸೂಚನೆ ವಿಶ್ವಾಸ', 'Hindi': 'पूर्वानुमान विश्वास', 'Tamil': 'முன்னறிவிப்பு நம்பிக்கை', 'Telugu': 'సూచన విశ్వాసం'},
    'Forecasts': {'Kannada': 'ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'पूर्वानुमान', 'Tamil': 'முன்னறிவிப்புகள்', 'Telugu': 'సూచనలు'},
    'Loading sources...': {'Kannada': 'ಮೂಲಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...', 'Hindi': 'स्रोत लोड हो रहे हैं...', 'Tamil': 'ஆதாரங்களை ஏற்றுகிறது...', 'Telugu': 'మూలాలను లోడ్ చేస్తోంది...'},
    'Model Performance': {'Kannada': 'ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ', 'Hindi': 'मॉडल का प्रदर्शन', 'Tamil': 'மாதிரி செயல்திறன்', 'Telugu': 'మోడల్ పనితీరు'},
    'Models': {'Kannada': 'ಮಾದರಿಗಳು', 'Hindi': 'मॉडल', 'Tamil': 'மாதிரிகள்', 'Telugu': 'నమూనాలు'},
    'No district predictions': {'Kannada': 'ಯಾವುದೇ ಜಿಲ್ಲಾ ಮುನ್ಸೂಚನೆಗಳಿಲ್ಲ', 'Hindi': 'कोई ज़िला भविष्यवाणी नहीं', 'Tamil': 'மாவட்ட கணிப்புகள் இல்லை', 'Telugu': 'జిల్లా అంచనాలు లేవు'},
    'No forecast data': {'Kannada': 'ಯಾವುದೇ ಮುನ್ಸೂಚನೆ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'कोई पूर्वानुमान डेटा नहीं', 'Tamil': 'முன்னறிவிப்பு தரவு இல்லை', 'Telugu': 'సూచన డేటా లేదు'},
    'No models registered': {'Kannada': 'ಯಾವುದೇ ಮಾದರಿಗಳನ್ನು ನೋಂದಾಯಿಸಲಾಗಿಲ್ಲ', 'Hindi': 'कोई मॉडल पंजीकृत नहीं', 'Tamil': 'எந்த மாதிரிகளும் பதிவு செய்யப்படவில்லை', 'Telugu': 'ఏ నమూనాలు నమోదు కాలేదు'},
    'Predictions': {'Kannada': 'ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'भविष्यवाणियां', 'Tamil': 'கணிப்புகள்', 'Telugu': 'అంచనాలు'},
    'Trend': {'Kannada': 'ಪ್ರವೃತ್ತಿ', 'Hindi': 'प्रवृत्ति', 'Tamil': 'போக்கு', 'Telugu': 'ట్రెండ్'},
    'Why This Prediction?': {'Kannada': 'ಈ ಮುನ್ಸೂಚನೆ ಏಕೆ?', 'Hindi': 'यह भविष्यवाणी क्यों?', 'Tamil': 'இந்த கணிப்பு ஏன்?', 'Telugu': 'ఈ అంచనా ఎందుకు?'},
    'Crime rate trending upward': {'Kannada': 'ಅಪರಾಧ ದರ ಮೇಲ್ಮುಖವಾಗಿದೆ', 'Hindi': 'अपराध दर ऊपर की ओर', 'Tamil': 'குற்ற விகிதம் மேல்நோக்கி செல்கிறது', 'Telugu': 'నేరాల రేటు పైకి ట్రెండ్ అవుతోంది'},
    'Crime rate trending downward': {'Kannada': 'ಅಪರಾಧ ದರ ಕೆಳಮುಖವಾಗಿದೆ', 'Hindi': 'अपराध दर नीचे की ओर', 'Tamil': 'குற்ற விகிதம் கீழ்நோக்கி செல்கிறது', 'Telugu': 'నేరాల రేటు క్రిందికి ట్రెండ్ అవుతోంది'},
    'Cross-district coordination recommended': {'Kannada': 'ಅಂತರ-ಜಿಲ್ಲಾ ಸಮನ್ವಯ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ', 'Hindi': 'अंतर-ज़िला समन्वय की सिफारिश की गई', 'Tamil': 'மாவட்டங்களுக்கு இடையேயான ஒருங்கிணைப்பு பரிந்துரைக்கப்படுகிறது', 'Telugu': 'క్రాస్-జిల్లా సమన్వయం సిఫార్సు చేయబడింది'}
}

trans_file = r"e:\CrimeMatrix\frontend\src\context\translations.js"
with codecs.open(trans_file, "r", "utf-8") as f:
    t_content = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']
for lang in languages:
    new_entries = []
    for eng_key, trans_dict in translations.items():
        val = eng_key if lang == 'English' else trans_dict[lang]
        eng_key_esc = eng_key.replace("'", "\\'")
        val_esc = val.replace("'", "\\'")
        new_entries.append(f"'{eng_key_esc}': '{val_esc}'")
    
    entries_str = ", ".join(new_entries)
    
    if lang != 'Telugu':
        next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}[lang]
        pattern = f"\n  }},\n  {next_lang}:"
        t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }},\n  {next_lang}:")
    else:
        pattern = f"\n  }}\n}}"
        t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }}\n}}")

with codecs.open(trans_file, "w", "utf-8") as f:
    f.write(t_content)

directory = r"e:\CrimeMatrix\frontend\src\components\predictions"
for root, _, files in os.walk(directory):
    for file in files:
        if not file.endswith(".jsx"): continue
        
        filepath = os.path.join(root, file)
        with codecs.open(filepath, "r", "utf-8") as f:
            content = f.read()
        
        original_content = content
        
        for s in translations.keys():
            # Match exact string between tags
            content = content.replace(f">{s}<", f">{{t('{s}')}}<")
            # Replace strings inside title="..." or placeholder="..."
            content = re.sub(rf'title="{s}"', rf"title={{t('{s}')}}", content)
            content = re.sub(rf'placeholder="{s}"', rf"placeholder={{t('{s}')}}", content)
            # Replace exactly 'String' in javascript 
            content = content.replace(f"'{s}'", f"t('{s}')")

        if content != original_content:
            if 'useLanguage' not in content:
                imp = "import { useLanguage } from '../../context/LanguageContext'\n"
                
                imports_end = 0
                for m in re.finditer(r'^import .*$', content, re.MULTILINE):
                    imports_end = m.end()
                
                content = content[:imports_end] + "\n" + imp + content[imports_end:]
            
            func_match = re.search(r'export default function (\w+)\s*\([^)]*\)\s*\{', content)
            if func_match and 'const { t } = useLanguage()' not in content:
                insert_idx = func_match.end()
                content = content[:insert_idx] + "\n  const { t } = useLanguage()" + content[insert_idx:]
            
            with codecs.open(filepath, "w", "utf-8") as f:
                f.write(content)
            print(f"Updated {file}")
