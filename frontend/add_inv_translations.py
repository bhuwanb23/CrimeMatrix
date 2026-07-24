import codecs
import re

new_translations = {
    'Investigation Workspace': {'Kannada': 'ತನಿಖಾ ಕಾರ್ಯಸ್ಥಳ', 'Hindi': 'जांच कार्यक्षेत्र', 'Tamil': 'விசாரணை பணியிடம்', 'Telugu': 'దర్యాప్తు కార్యస్థలం'},
    'Command center for active investigations': {'Kannada': 'ಸಕ್ರಿಯ ತನಿಖೆಗಳಿಗೆ ಕಮಾಂಡ್ ಸೆಂಟರ್', 'Hindi': 'सक्रिय जांच के लिए कमांड सेंटर', 'Tamil': 'செயலில் உள்ள விசாரணைகளுக்கான கட்டளை மையம்', 'Telugu': 'క్రియాశీల దర్యాప్తు కోసం కమాండ్ సెంటర్'},
    'Search investigations...': {'Kannada': 'ತನಿಖೆಗಳನ್ನು ಹುಡುಕಿ...', 'Hindi': 'जांच खोजें...', 'Tamil': 'விசாரணைகளைத் தேடு...', 'Telugu': 'దర్యాప్తులను శోధించండి...'},
    'New Investigation': {'Kannada': 'ಹೊಸ ತನಿಖೆ', 'Hindi': 'नई जांच', 'Tamil': 'புதிய விசாரணை', 'Telugu': 'కొత్త దర్యాప్తు'},
    'Select an Investigation': {'Kannada': 'ತನಿಖೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ', 'Hindi': 'एक जांच चुनें', 'Tamil': 'ஒரு விசாரணையைத் தேர்ந்தெடுக்கவும்', 'Telugu': 'ఒక దర్యాప్తును ఎంచుకోండి'},
    'Choose a case from the list to start working': {'Kannada': 'ಕೆಲಸ ಮಾಡಲು ಪಟ್ಟಿಯಿಂದ ಪ್ರಕರಣವನ್ನು ಆಯ್ಕೆಮಾಡಿ', 'Hindi': 'काम शुरू करने के लिए सूची से एक मामला चुनें', 'Tamil': 'வேலையைத் தொடங்க பட்டியலிலிருந்து ஒரு வழக்கைத் தேர்ந்தெடுக்கவும்', 'Telugu': 'పనిని ప్రారంభించడానికి జాబితా నుండి ఒక కేసును ఎంచుకోండి'},
    'No investigations found': {'Kannada': 'ಯಾವುದೇ ತನಿಖೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई जांच नहीं मिली', 'Tamil': 'விசாரணைகள் எதுவும் காணப்படவில்லை', 'Telugu': 'దర్యాప్తులు ఏవీ కనుగొనబడలేదు'},
    'Investigation': {'Kannada': 'ತನಿಖೆ', 'Hindi': 'जांच', 'Tamil': 'விசாரணை', 'Telugu': 'దర్యాప్తు'},
    'Notes': {'Kannada': 'ಟಿಪ್ಪಣಿಗಳು', 'Hindi': 'नोट्स', 'Tamil': 'குறிப்புகள்', 'Telugu': 'గమనికలు'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'सबूत', 'Tamil': 'ஆதாரம்', 'Telugu': 'ఆధారాలు'},
    'Events': {'Kannada': 'ಘಟನೆಗಳು', 'Hindi': 'घटनाएँ', 'Tamil': 'நிகழ்வுகள்', 'Telugu': 'సంఘటనలు'},
    'Progress': {'Kannada': 'ಪ್ರಗತಿ', 'Hindi': 'प्रगति', 'Tamil': 'முன்னேற்றம்', 'Telugu': 'పురోగతి'},
    'Priority Score': {'Kannada': 'ಆದ್ಯತೆಯ ಸ್ಕೋರ್', 'Hindi': 'प्राथमिकता स्कोर', 'Tamil': 'முன்னுரிமை மதிப்பெண்', 'Telugu': 'ప్రాధాన్యత స్కోరు'},
    'Click Score to analyze priority': {'Kannada': 'ಆದ್ಯತೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಸ್ಕೋರ್ ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'प्राथमिकता का विश्लेषण करने के लिए स्कोर पर क्लिक करें', 'Tamil': 'முன்னுரிமையை பகுப்பாய்வு செய்ய மதிப்பெண்ணைக் கிளிக் செய்க', 'Telugu': 'ప్రాధాన్యతను విశ్లేషించడానికి స్కోర్‌ను క్లిక్ చేయండి'},
    'Reports': {'Kannada': 'ವರದಿಗಳು', 'Hindi': 'रिपोर्ट', 'Tamil': 'அறிக்கைகள்', 'Telugu': 'నివేదికలు'},
    'Generate Report': {'Kannada': 'ವರದಿಯನ್ನು ರಚಿಸಿ', 'Hindi': 'रिपोर्ट जनरेट करें', 'Tamil': 'அறிக்கையை உருவாக்கு', 'Telugu': 'నివేదికను రూపొందించండి'},
    'Export PDF': {'Kannada': 'ಪಿಡಿಎಫ್ ರಫ್ತು ಮಾಡಿ', 'Hindi': 'पीडीएफ निर्यात करें', 'Tamil': 'PDF ஐ ஏற்றுமதி செய்', 'Telugu': 'PDF ఎగుమతి చేయండి'},
    'Print': {'Kannada': 'ಮುದ್ರಿಸಿ', 'Hindi': 'प्रिंट', 'Tamil': 'அச்சிடு', 'Telugu': 'ముద్రించండి'},
    'Investigation Stats': {'Kannada': 'ತನಿಖಾ ಅಂಕಿಅಂಶಗಳು', 'Hindi': 'जांच के आँकड़े', 'Tamil': 'விசாரணை புள்ளிவிவரங்கள்', 'Telugu': 'దర్యాప్తు గణాంకాలు'},
    'No notes yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಟಿಪ್ಪಣಿಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई नोट्स नहीं', 'Tamil': 'இன்னும் குறிப்புகள் இல்லை', 'Telugu': 'ఇంకా గమనికలు లేవు'},
    'Add an investigation note...': {'Kannada': 'ತನಿಖಾ ಟಿಪ್ಪಣಿಯನ್ನು ಸೇರಿಸಿ...', 'Hindi': 'एक जांच नोट जोड़ें...', 'Tamil': 'ஒரு விசாரணை குறிப்பைச் சேர்க்கவும்...', 'Telugu': 'దర్యాప్తు గమనికను జోడించండి...'},
    'No evidence collected for this case': {'Kannada': 'ಈ ಪ್ರಕರಣಕ್ಕೆ ಯಾವುದೇ ಸಾಕ್ಷ್ಯವನ್ನು ಸಂಗ್ರಹಿಸಲಾಗಿಲ್ಲ', 'Hindi': 'इस मामले के लिए कोई सबूत एकत्र नहीं किया गया', 'Tamil': 'இந்த வழக்கில் எந்த ஆதாரமும் சேகரிக்கப்படவில்லை', 'Telugu': 'ఈ కేసు కోసం ఎలాంటి ఆధారాలు సేకరించబడలేదు'},
    'No timeline events yet': {'Kannada': 'ಇನ್ನೂ ಟೈಮ್‌ಲೈನ್ ಘಟನೆಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई समयरेखा घटनाएँ नहीं', 'Tamil': 'இன்னும் காலவரிசை நிகழ்வுகள் இல்லை', 'Telugu': 'ఇంకా టైమ్‌లైన్ ఈవెంట్‌లు లేవు'},
    'Event title': {'Kannada': 'ಘಟನೆಯ ಶೀರ್ಷಿಕೆ', 'Hindi': 'घटना का शीर्षक', 'Tamil': 'நிகழ்வு தலைப்பு', 'Telugu': 'ఈవెంట్ శీర్షిక'},
    'Description (optional)': {'Kannada': 'ವಿವರಣೆ (ಐಚ್ಛಿಕ)', 'Hindi': 'विवरण (वैकल्पिक)', 'Tamil': 'விளக்கம் (விரும்பினால்)', 'Telugu': 'వివరణ (ఐచ్ఛికం)'},
    'Add Event': {'Kannada': 'ಘಟನೆಯನ್ನು ಸೇರಿಸಿ', 'Hindi': 'घटना जोड़ें', 'Tamil': 'நிகழ்வைச் சேர்', 'Telugu': 'ఈవెంట్‌ను జోడించండి'},
    'Cancel': {'Kannada': 'ರದ್ದುಮಾಡಿ', 'Hindi': 'रद्द करें', 'Tamil': 'ரத்துசெய்', 'Telugu': 'రద్దు చేయండి'},
    'No related cases found': {'Kannada': 'ಯಾವುದೇ ಸಂಬಂಧಿತ ಪ್ರಕರಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई संबंधित मामले नहीं मिले', 'Tamil': 'தொடர்புடைய வழக்குகள் எதுவும் காணப்படவில்லை', 'Telugu': 'సంబంధిత కేసులు ఏవీ కనుగొనబడలేదు'},
    'View': {'Kannada': 'ವೀಕ್ಷಿಸಿ', 'Hindi': 'देखें', 'Tamil': 'காண்க', 'Telugu': 'చూడండి'},
    'No attachments yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಲಗತ್ತುಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई अनुलग्नक नहीं', 'Tamil': 'இன்னும் இணைப்புகள் இல்லை', 'Telugu': 'ఇంకా జోడింపులు లేవు'},
    'AI Investigation Assistant': {'Kannada': 'ಎಐ ತನಿಖಾ ಸಹಾಯಕ', 'Hindi': 'एआई जांच सहायक', 'Tamil': 'AI விசாரணை உதவியாளர்', 'Telugu': 'AI దర్యాప్తు సహాయకుడు'},
    'I can summarize evidence, suggest leads, find similar cases, and more.': {'Kannada': 'ನಾನು ಸಾಕ್ಷ್ಯವನ್ನು ಸಂಕ್ಷಿಪ್ತಗೊಳಿಸಬಹುದು, ಲೀಡ್‌ಗಳನ್ನು ಸೂಚಿಸಬಹುದು, ಒಂದೇ ರೀತಿಯ ಪ್ರಕರಣಗಳನ್ನು ಹುಡುಕಬಹುದು ಮತ್ತು ಹೆಚ್ಚಿನದನ್ನು ಮಾಡಬಹುದು.', 'Hindi': 'मैं सबूतों का सारांश दे सकता हूं, सुराग सुझा सकता हूं, समान मामले ढूंढ सकता हूं, और भी बहुत कुछ।', 'Tamil': 'நான் ஆதாரங்களை சுருக்கமாகக் கூறலாம், தடயங்களை பரிந்துரைக்கலாம், இதே போன்ற வழக்குகளைக் கண்டறியலாம் மற்றும் பலவற்றைச் செய்யலாம்.', 'Telugu': 'నేను సాక్ష్యాలను సంగ్రహించగలను, లీడ్‌లను సూచించగలను, ఇలాంటి కేసులను కనుగొనగలను మరియు మరిన్ని చేయగలను.'},
    'Ask me anything about this investigation': {'Kannada': 'ಈ ತನಿಖೆಯ ಬಗ್ಗೆ ನನ್ನನ್ನು ಏನನ್ನಾದರೂ ಕೇಳಿ', 'Hindi': 'इस जांच के बारे में मुझसे कुछ भी पूछें', 'Tamil': 'இந்த விசாரணையைப் பற்றி என்னிடம் எதையும் கேளுங்கள்', 'Telugu': 'ఈ దర్యాప్తు గురించి నన్ను ఏదైనా అడగండి'},
    'Ask about this investigation...': {'Kannada': 'ಈ ತನಿಖೆಯ ಬಗ್ಗೆ ಕೇಳಿ...', 'Hindi': 'इस जांच के बारे में पूछें...', 'Tamil': 'இந்த விசாரணையைப் பற்றி கேளுங்கள்...', 'Telugu': 'ఈ దర్యాప్తు గురించి అడగండి...'},
    'Analyzing investigation data...': {'Kannada': 'ತನಿಖಾ ದತ್ತಾಂಶವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...', 'Hindi': 'जांच डेटा का विश्लेषण किया जा रहा है...', 'Tamil': 'விசாரணை தரவு பகுப்பாய்வு செய்யப்படுகிறது...', 'Telugu': 'దర్యాప్తు డేటాను విశ్లేషిస్తోంది...'},
    'Loading investigation...': {'Kannada': 'ತನಿಖೆಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...', 'Hindi': 'जांच लोड हो रही है...', 'Tamil': 'விசாரணை ஏற்றப்படுகிறது...', 'Telugu': 'దర్యాప్తు లోడ్ అవుతోంది...'},
    'Loading...': {'Kannada': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'लोड हो रहा है...', 'Tamil': 'ஏற்றப்படுகிறது...', 'Telugu': 'లోడ్ అవుతోంది...'},
    'Recently Viewed': {'Kannada': 'ಇತ್ತೀಚೆಗೆ ವೀಕ್ಷಿಸಲಾಗಿದೆ', 'Hindi': 'हाल ही में देखा गया', 'Tamil': 'சமீபத்தில் பார்க்கப்பட்டது', 'Telugu': 'ఇటీవల చూసినవి'},
    'Investigation title...': {'Kannada': 'ತನಿಖೆಯ ಶೀರ್ಷಿಕೆ...', 'Hindi': 'जांच का शीर्षक...', 'Tamil': 'விசாரணை தலைப்பு...', 'Telugu': 'దర్యాప్తు శీర్షిక...'},
    'No status logs yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಸ್ಥಿತಿ ಲಾಗ್‌ಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई स्टेटस लॉग नहीं', 'Tamil': 'இன்னும் நிலை பதிவுகள் இல்லை', 'Telugu': 'ఇంకా స్థితి లాగ్‌లు లేవు'},
    'Recommended Actions': {'Kannada': 'ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮಗಳು', 'Hindi': 'अनुशंसित कार्रवाइयां', 'Tamil': 'பரிந்துரைக்கப்பட்ட செயல்கள்', 'Telugu': 'సిఫార్సు చేయబడిన చర్యలు'},
    'High Priority': {'Kannada': 'ಹೆಚ್ಚಿನ ಆದ್ಯತೆ', 'Hindi': 'उच्च प्राथमिकता', 'Tamil': 'உயர் முன்னுரிமை', 'Telugu': 'అధిక ప్రాధాన్యత'},
    'Medium Priority': {'Kannada': 'ಮಧ್ಯಮ ಆದ್ಯತೆ', 'Hindi': 'मध्यम प्राथमिकता', 'Tamil': 'நடுத்தர முன்னுரிமை', 'Telugu': 'మధ్యస్థ ప్రాధాన్యత'},
    'Low Priority': {'Kannada': 'ಕಡಿಮೆ ಆದ್ಯತೆ', 'Hindi': 'कम प्राथमिकता', 'Tamil': 'குறைந்த முன்னுரிமை', 'Telugu': 'తక్కువ ప్రాధాన్యత'},
    'Suspect': {'Kannada': 'ಶಂಕಿತ', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்', 'Telugu': 'అనుమానితుడు'},
    'Filing': {'Kannada': 'ಫೈಲಿಂಗ್', 'Hindi': 'फाइलिंग', 'Tamil': 'தாக்கல் செய்தல்', 'Telugu': 'ఫైలింగ్'},
    'AI Analysis': {'Kannada': 'ಎಐ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'एआई विश्लेषण', 'Tamil': 'AI பகுப்பாய்வு', 'Telugu': 'AI విశ్లేషణ'},
    'Pattern Analysis': {'Kannada': 'ಮಾದರಿ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'पैटर्न विश्लेषण', 'Tamil': 'முறை பகுப்பாய்வு', 'Telugu': 'నమూనా విశ్లేషణ'},
    'Bengaluru Urban': {'Kannada': 'ಬೆಂಗಳೂರು ನಗರ', 'Hindi': 'बेंगलुरु शहरी', 'Tamil': 'பெங்களூரு நகர்ப்புறம்', 'Telugu': 'బెంగళూరు అర్బన్'},
    'Bengaluru Rural': {'Kannada': 'ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ', 'Hindi': 'बेंगलुरु ग्रामीण', 'Tamil': 'பெங்களூரு ஊரகம்', 'Telugu': 'బెంగళూరు రూరల్'},
    'Mysuru': {'Kannada': 'ಮೈಸೂರು', 'Hindi': 'मैसूरु', 'Tamil': 'மைசூர்', 'Telugu': 'మైసూర్'},
    'Mangaluru': {'Kannada': 'ಮಂಗಳೂರು', 'Hindi': 'मंगलुरु', 'Tamil': 'மங்களூர்', 'Telugu': 'మంగళూరు'},
    'Hubballi': {'Kannada': 'ಹುಬ್ಬಳ್ಳಿ', 'Hindi': 'हुबली', 'Tamil': 'ஹூப்பள்ளி', 'Telugu': 'హుబ్లీ'},
    'Based on historical data, cases with similar MO patterns have a 73% resolution rate when cross-district coordination is initiated within 48 hours.': {
        'Kannada': 'ಐತಿಹಾಸಿಕ ಡೇಟಾವನ್ನು ಆಧರಿಸಿ, ಇದೇ ರೀತಿಯ MO ಮಾದರಿಗಳನ್ನು ಹೊಂದಿರುವ ಪ್ರಕರಣಗಳು 48 ಗಂಟೆಗಳ ಒಳಗೆ ಅಡ್ಡ-ಜಿಲ್ಲಾ ಸಮನ್ವಯವನ್ನು ಪ್ರಾರಂಭಿಸಿದಾಗ 73% ಪರಿಹಾರ ದರವನ್ನು ಹೊಂದಿರುತ್ತವೆ.',
        'Hindi': 'ऐतिहासिक डेटा के आधार पर, 48 घंटों के भीतर क्रॉस-डिस्ट्रिक्ट समन्वय शुरू होने पर समान MO पैटर्न वाले मामलों में 73% समाधान दर होती है।',
        'Tamil': 'வரலாற்றுத் தரவுகளின் அடிப்படையில், 48 மணி நேரத்திற்குள் குறுக்கு-மாவட்ட ஒருங்கிணைப்பு தொடங்கப்படும்போது இதேபோன்ற MO முறைகளைக் கொண்ட வழக்குகள் 73% தீர்வு விகிதத்தைக் கொண்டுள்ளன.',
        'Telugu': 'చారిత్రక డేటా ఆధారంగా, 48 గంటల్లోగా క్రాస్-డిస్ట్రిక్ట్ కోఆర్డినేషన్ ప్రారంభించినప్పుడు ఇలాంటి MO నమూనాలను కలిగి ఉన్న కేసులు 73% రిజల్యూషన్ రేటును కలిగి ఉంటాయి.'
    }
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
