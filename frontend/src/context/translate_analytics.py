import os
import re
import codecs

src_dirs = [
    r"e:\CrimeMatrix\frontend\src\components\analytics",
    r"e:\CrimeMatrix\frontend\src\components\predictions",
    r"e:\CrimeMatrix\frontend\src\components"
]
target_files = ['AIAnalyticsPage.jsx', 'PredictionAnalyticsPage.jsx']

strings_to_replace = [
    'AI Analytics Dashboard',
    'Predictive insights, risk assessments, and actionable recommendations',
    'AI MODELS',
    'ACCURACY',
    'PREDICTIONS',
    'ACTIVE',
    'Active Alerts',
    'No active alerts',
    'High-Risk Suspects',
    'No high-risk suspects',
    'Crime Forecast',
    'Priority Cases',
    'AI Recommendations',
    'Model Evaluation',
    'Accuracy Trend',
    'Feedback Summary',
    'Predictive Crime Analytics',
    'Forecast crime patterns with confidence indicators',
    'Generate Forecast',
    'FORECASTS',
    'AVG CONFIDENCE',
    'MODELS',
    'District Predictions',
    'Seasonal Patterns',
    'Confidence Breakdown',
    'Crime Type Predictions',
    'Data Quality',
    'Model Reliability',
    'Temporal Stability',
    'Statistical Confidence',
    'Overall confidence',
    'Low reliability',
    'Refresh',
    'Loading analytics dashboard...',
    'Loading predictions...',
    'No accuracy data yet',
    'No predictions yet',
    'Correct',
    'Incorrect',
    'Avg Rating',
    'METRICS',
    'FEEDBACK',
    'EVALUATIONS',
    'AVG RATING',
    'Run Evaluation',
    'By Hour',
    'By Day',
    'By Month',
    'Failed to load analytics dashboard',
    'Failed to load predictions'
]

# Create translation dictionary for these strings
translations = {
    'AI Analytics Dashboard': {'Kannada': 'AI ಅನಾಲಿಟಿಕ್ಸ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'Hindi': 'एआई एनालिटिक्स डैशबोर्ड', 'Tamil': 'AI பகுப்பாய்வு டாஷ்போர்டு', 'Telugu': 'AI అనలిటిక్స్ డాష్‌బోర్డ్'},
    'Predictive insights, risk assessments, and actionable recommendations': {'Kannada': 'ಮುನ್ಸೂಚಕ ಒಳನೋಟಗಳು, ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನಗಳು', 'Hindi': 'भविष्य कहनेवाला अंतर्दृष्टि, जोखिम आकलन', 'Tamil': 'முன்கணிப்பு நுண்ணறிவு, ஆபத்து மதிப்பீடுகள்', 'Telugu': 'ప్రిడిక్టివ్ అంతర్దృష్టులు, ప్రమాద అంచనాలు'},
    'AI MODELS': {'Kannada': 'AI ಮಾದರಿಗಳು', 'Hindi': 'एआई मॉडल', 'Tamil': 'AI மாதிரிகள்', 'Telugu': 'AI నమూనాలు'},
    'ACCURACY': {'Kannada': 'ನಿಖರತೆ', 'Hindi': 'सटीकता', 'Tamil': 'துல்லியம்', 'Telugu': 'ఖచ్చితత్వం'},
    'PREDICTIONS': {'Kannada': 'ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'भविष्यवाणियां', 'Tamil': 'கணிப்புகள்', 'Telugu': 'అంచనాలు'},
    'ACTIVE': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకుగా'},
    'Active Alerts': {'Kannada': 'ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'सक्रिय अलर्ट', 'Tamil': 'செயலில் உள்ள விழிப்பூட்டல்கள்', 'Telugu': 'క్రియాశీల హెచ్చరికలు'},
    'No active alerts': {'Kannada': 'ಯಾವುದೇ ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳಿಲ್ಲ', 'Hindi': 'कोई सक्रिय अलर्ट नहीं', 'Tamil': 'செயலில் உள்ள விழிப்பூட்டல்கள் இல்லை', 'Telugu': 'క్రియాశీల హెచ్చరికలు లేవు'},
    'High-Risk Suspects': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ಶಂಕಿತರು', 'Hindi': 'उच्च जोखिम वाले संदिग्ध', 'Tamil': 'அதிக ஆபத்துள்ள சந்தேக நபர்கள்', 'Telugu': 'అధిక-ప్రమాద అనుమానితులు'},
    'No high-risk suspects': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ಶಂಕಿತರು ಇಲ್ಲ', 'Hindi': 'कोई उच्च जोखिम वाला संदिग्ध नहीं', 'Tamil': 'அதிக ஆபத்துள்ள சந்தேக நபர்கள் இல்லை', 'Telugu': 'అధిక-ప్రమాద అనుమానితులు లేరు'},
    'Crime Forecast': {'Kannada': 'ಅಪರಾಧ ಮುನ್ಸೂಚನೆ', 'Hindi': 'अपराध पूर्वानुमान', 'Tamil': 'குற்ற முன்னறிவிப்பு', 'Telugu': 'క్రైమ్ సూచన'},
    'Priority Cases': {'Kannada': 'ಆದ್ಯತೆಯ ಪ್ರಕರಣಗಳು', 'Hindi': 'प्राथमिकता वाले मामले', 'Tamil': 'முன்னுரிமை வழக்குகள்', 'Telugu': 'ప్రాధాನ್ಯత కేసులు'},
    'AI Recommendations': {'Kannada': 'AI ಶಿಫಾರಸುಗಳು', 'Hindi': 'एआई सिफारिशें', 'Tamil': 'AI பரிந்துரைகள்', 'Telugu': 'AI సిఫార్సులు'},
    'Model Evaluation': {'Kannada': 'ಮಾದರಿ ಮೌಲ್ಯಮಾಪನ', 'Hindi': 'मॉडल मूल्यांकन', 'Tamil': 'மாதிரி மதிப்பீடு', 'Telugu': 'మోడల్ మూల్యాంకనం'},
    'Accuracy Trend': {'Kannada': 'ನಿಖರತೆಯ ಪ್ರವೃತ್ತಿ', 'Hindi': 'सटीकता की प्रवृत्ति', 'Tamil': 'துல்லிய போக்கு', 'Telugu': 'ఖచ్చితత్వ ధోరణి'},
    'Feedback Summary': {'Kannada': 'ಪ್ರತಿಕ್ರಿಯೆ ಸಾರಾಂಶ', 'Hindi': 'प्रतिक्रिया सारांश', 'Tamil': 'கருத்து சுருக்கம்', 'Telugu': 'అభిప్రాయ సారాంశం'},
    'Predictive Crime Analytics': {'Kannada': 'ಮುನ್ಸೂಚಕ ಅಪರಾಧ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'भविष्य कहनेवाला अपराध विश्लेषण', 'Tamil': 'முன்கணிப்பு குற்ற பகுப்பாய்வு', 'Telugu': 'ప్రిడిక్టివ్ క్రైమ్ అనలిటిక్స్'},
    'Forecast crime patterns with confidence indicators': {'Kannada': 'ವಿಶ್ವಾಸಾರ್ಹತೆಯ ಸೂಚಕಗಳೊಂದಿಗೆ ಅಪರಾಧ ಮಾದರಿಗಳನ್ನು ಮುನ್ಸೂಚಿಸಿ', 'Hindi': 'विश्वास संकेतकों के साथ अपराध पैटर्न का पूर्वानुमान करें', 'Tamil': 'நம்பிக்கை குறிகாட்டிகளுடன் குற்ற முறைகளை கணிக்கவும்', 'Telugu': 'విశ్వాస సూచికలతో నేర నమూనాలను అంచనా వేయండి'},
    'Generate Forecast': {'Kannada': 'ಮುನ್ಸೂಚನೆಯನ್ನು ರಚಿಸಿ', 'Hindi': 'पूर्वानुमान उत्पन्न करें', 'Tamil': 'முன்னறிவிப்பை உருவாக்கு', 'Telugu': 'సూచనను రూపొందించండి'},
    'FORECASTS': {'Kannada': 'ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'पूर्वानुमान', 'Tamil': 'முன்னறிவிப்புகள்', 'Telugu': 'సూచనలు'},
    'AVG CONFIDENCE': {'Kannada': 'ಸರಾಸರಿ ವಿಶ್ವಾಸ', 'Hindi': 'औसत विश्वास', 'Tamil': 'சராசரி நம்பிக்கை', 'Telugu': 'సగటు విశ్వాసం'},
    'MODELS': {'Kannada': 'ಮಾದರಿಗಳು', 'Hindi': 'मॉडल', 'Tamil': 'மாதிரிகள்', 'Telugu': 'నమూనాలు'},
    'District Predictions': {'Kannada': 'ಜಿಲ್ಲಾ ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'ज़िला भविष्यवाणियां', 'Tamil': 'மாவட்ட கணிப்புகள்', 'Telugu': 'జిల్లా అంచనాలు'},
    'Seasonal Patterns': {'Kannada': 'ಋತುಮಾನದ ಮಾದರಿಗಳು', 'Hindi': 'मौसमी पैटर्न', 'Tamil': 'பருவகால வடிவங்கள்', 'Telugu': 'కాలానుగుణ నమూనాలు'},
    'Confidence Breakdown': {'Kannada': 'ವಿಶ್ವಾಸದ ವಿಭಜನೆ', 'Hindi': 'विश्वास का टूटना', 'Tamil': 'நம்பிக்கை முறிவு', 'Telugu': 'విశ్వాస విచ్ఛిన్నం'},
    'Crime Type Predictions': {'Kannada': 'ಅಪರಾಧ ಪ್ರಕಾರದ ಮುನ್ಸೂಚನೆಗಳು', 'Hindi': 'अपराध प्रकार की भविष्यवाणियां', 'Tamil': 'குற்ற வகை கணிப்புகள்', 'Telugu': 'నేర రకం అంచనాలు'},
    'Data Quality': {'Kannada': 'ಡೇಟಾ ಗುಣಮಟ್ಟ', 'Hindi': 'डेटा की गुणवत्ता', 'Tamil': 'தரவு தரம்', 'Telugu': 'డేటా నాణ్యత'},
    'Model Reliability': {'Kannada': 'ಮಾದರಿ ವಿಶ್ವಾಸಾರ್ಹತೆ', 'Hindi': 'मॉडल विश्वसनीयता', 'Tamil': 'மாதிரி நம்பகத்தன்மை', 'Telugu': 'మోడల్ విశ్వసనీయత'},
    'Temporal Stability': {'Kannada': 'ತಾತ್ಕಾಲಿಕ ಸ್ಥಿರತೆ', 'Hindi': 'अस्थायी स्थिरता', 'Tamil': 'தற்காலிக நிலைத்தன்மை', 'Telugu': 'తాత్కాలిక స్థిరత్వం'},
    'Statistical Confidence': {'Kannada': 'ಸಂಖ್ಯಾಶಾಸ್ತ್ರೀಯ ವಿಶ್ವಾಸ', 'Hindi': 'सांख्यिकीय विश्वास', 'Tamil': 'புள்ளியியல் நம்பிக்கை', 'Telugu': 'గణాంక విశ్వాసం'},
    'Overall confidence': {'Kannada': 'ಒಟ್ಟಾರೆ ವಿಶ್ವಾಸ', 'Hindi': 'समग्र विश्वास', 'Tamil': 'ஒட்டுமொத்த நம்பிக்கை', 'Telugu': 'మొత్తం విశ్వాసం'},
    'Low reliability': {'Kannada': 'ಕಡಿಮೆ ವಿಶ್ವಾಸಾರ್ಹತೆ', 'Hindi': 'कम विश्वसनीयता', 'Tamil': 'குறைந்த நம்பகத்தன்மை', 'Telugu': 'తక్కువ విశ్వసనీయత'},
    'Refresh': {'Kannada': 'ರಿಫ್ರೆಶ್', 'Hindi': 'रीफ्रेश', 'Tamil': 'புதுப்பி', 'Telugu': 'రిఫ్రెష్'},
    'Loading analytics dashboard...': {'Kannada': 'ಅನಾಲಿಟಿಕ್ಸ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'एनालिटिक्स डैशबोर्ड लोड हो रहा है...', 'Tamil': 'பகுப்பாய்வு டாஷ்போர்டு ஏற்றப்படுகிறது...', 'Telugu': 'అనలిటిక్స్ డాష్‌బోర్డ్ లోడ్ అవుతోంది...'},
    'Loading predictions...': {'Kannada': 'ಮುನ್ಸೂಚನೆಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...', 'Hindi': 'भविष्यवाणियां लोड हो रही हैं...', 'Tamil': 'கணிப்புகள் ஏற்றப்படுகின்றன...', 'Telugu': 'అంచనాలు లోడ్ అవుతున్నాయి...'},
    'No accuracy data yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ನಿಖರತೆಯ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'अभी तक कोई सटीकता डेटा नहीं', 'Tamil': 'துல்லியமான தரவு இன்னும் இல்லை', 'Telugu': 'ఇంకా ఖచ్చితత్వ డేటా లేదు'},
    'No predictions yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಮುನ್ಸೂಚನೆಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई भविष्यवाणी नहीं', 'Tamil': 'கணிப்புகள் இன்னும் இல்லை', 'Telugu': 'ఇంకా అంచనాలు లేవు'},
    'Correct': {'Kannada': 'ಸರಿ', 'Hindi': 'सही', 'Tamil': 'சரி', 'Telugu': 'సరైనది'},
    'Incorrect': {'Kannada': 'ತಪ್ಪು', 'Hindi': 'गलत', 'Tamil': 'தவறு', 'Telugu': 'తప్పు'},
    'Avg Rating': {'Kannada': 'ಸರಾಸರಿ ರೇಟಿಂಗ್', 'Hindi': 'औसत रेटिंग', 'Tamil': 'சராசரி மதிப்பீடு', 'Telugu': 'సగటు రేటింగ్'},
    'METRICS': {'Kannada': 'ಮೆಟ್ರಿಕ್ಸ್', 'Hindi': 'मैट्रिक्स', 'Tamil': 'அளவீடுகள்', 'Telugu': 'కొలమానాలు'},
    'FEEDBACK': {'Kannada': 'ಪ್ರತಿಕ್ರಿಯೆ', 'Hindi': 'प्रतिक्रिया', 'Tamil': 'பின்னூட்டம்', 'Telugu': 'అభిప్రాయం'},
    'EVALUATIONS': {'Kannada': 'ಮೌಲ್ಯಮಾಪನಗಳು', 'Hindi': 'मूल्यांकन', 'Tamil': 'மதிப்பீடுகள்', 'Telugu': 'మూల్యాంకనాలు'},
    'AVG RATING': {'Kannada': 'ಸರಾಸರಿ ರೇಟಿಂಗ್', 'Hindi': 'औसत रेटिंग', 'Tamil': 'சராசரி மதிப்பீடு', 'Telugu': 'సగటు రేటింగ్'},
    'Run Evaluation': {'Kannada': 'ಮೌಲ್ಯಮಾಪನವನ್ನು ಚಲಾಯಿಸಿ', 'Hindi': 'मूल्यांकन चलाएं', 'Tamil': 'மதிப்பீட்டை இயக்கவும்', 'Telugu': 'మూల్యాంకనాన్ని అమలు చేయండి'},
    'By Hour': {'Kannada': 'ಗಂಟೆಯ ಪ್ರಕಾರ', 'Hindi': 'घंटे के अनुसार', 'Tamil': 'மணிநேரப்படி', 'Telugu': 'గంట ద్వారా'},
    'By Day': {'Kannada': 'ದಿನದ ಪ್ರಕಾರ', 'Hindi': 'दिन के अनुसार', 'Tamil': 'நாளின்படி', 'Telugu': 'రోజు ద్వారా'},
    'By Month': {'Kannada': 'ತಿಂಗಳ ಪ್ರಕಾರ', 'Hindi': 'महीने के अनुसार', 'Tamil': 'மாதப்படி', 'Telugu': 'నెల ద్వారా'},
    'Failed to load analytics dashboard': {'Kannada': 'ಲೋಡ್ ಮಾಡಲು ವಿಫಲವಾಗಿದೆ', 'Hindi': 'लोड करने में विफल', 'Tamil': 'ஏற்றத் தவறியது', 'Telugu': 'లోడ్ చేయడంలో విఫలమైంది'},
    'Failed to load predictions': {'Kannada': 'ಲೋಡ್ ಮಾಡಲು ವಿಫಲವಾಗಿದೆ', 'Hindi': 'लोड करने में विफल', 'Tamil': 'ஏற்றத் தவறியது', 'Telugu': 'లోడ్ చేయడంలో విఫలమైంది'}
}

# 1. Update translations.js
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


# 2. Add useLanguage and wrap texts in JSX files
for d in src_dirs:
    for root, _, files in os.walk(d):
        if d.endswith("components") and root != d:
            continue # Don't traverse subdirectories for the root components dir
        for file in files:
            if not file.endswith(".jsx"): continue
            if d.endswith("components") and file not in target_files: continue
            
            filepath = os.path.join(root, file)
            with codecs.open(filepath, "r", "utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Replace occurrences of strings
            for s in strings_to_replace:
                # Replace exact >String< with >{t('String')}<
                content = content.replace(f">{s}<", f">{{t('{s}')}}<")
                # Replace strings inside title="..." or placeholder="..."
                content = re.sub(rf'title="{s}"', rf"title={{t('{s}')}}", content)
                content = re.sub(rf'placeholder="{s}"', rf"placeholder={{t('{s}')}}", content)
                # Replace 'String' if it is inside conditionals like `{generating ? 'Generate Forecast' : 'Refresh'}`
                # We can't do generic replace for all 'String' but we can do it for exact matches
                content = content.replace(f"'{s}'", f"t('{s}')")
                # But wait, replacing '{s}' with t('{s}') can break imports or object keys if we are not careful.
                # Since these are specific UI strings, hopefully they aren't used as keys. Let's undo the single quote replacement and use a safer regex.
                # Actually, in JSX, usually `>{s}<` covers 90%.
                # For ternary operators: `? '{s}' :` -> `? t('{s}') :`
                content = content.replace(f"? '{s}'", f"? t('{s}')")
                content = content.replace(f": '{s}'", f": t('{s}')")

            # Check if any replacement happened
            if content != original_content:
                # Add useLanguage import if missing
                if 'useLanguage' not in content:
                    # find relative path
                    if d.endswith("components"):
                        imp = "import { useLanguage } from '../context/LanguageContext'\n"
                    else:
                        imp = "import { useLanguage } from '../../context/LanguageContext'\n"
                    
                    # insert after last import
                    imports_end = 0
                    for m in re.finditer(r'^import .*$', content, re.MULTILINE):
                        imports_end = m.end()
                    
                    content = content[:imports_end] + "\n" + imp + content[imports_end:]
                
                # Add const { t } = useLanguage() inside component
                # find export default function ...
                func_match = re.search(r'export default function (\w+)\s*\([^)]*\)\s*\{', content)
                if func_match and 'const { t } = useLanguage()' not in content:
                    insert_idx = func_match.end()
                    content = content[:insert_idx] + "\n  const { t } = useLanguage()" + content[insert_idx:]
                
                with codecs.open(filepath, "w", "utf-8") as f:
                    f.write(content)
                print(f"Updated {file}")
