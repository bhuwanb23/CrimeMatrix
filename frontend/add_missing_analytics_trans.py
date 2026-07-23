import codecs
import re

translations = {
    'HIGH': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'MEDIUM': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தர', 'Telugu': 'మధ్యస్థ'},
    'LOW': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'निम्न', 'Tamil': 'குறைந்த', 'Telugu': 'తక్కువ'},
    'Progress:': {'Kannada': 'ಪ್ರಗತಿ:', 'Hindi': 'प्रगति:', 'Tamil': 'முன்னேற்றம்:', 'Telugu': 'ప్రగతి:'},
    'data points': {'Kannada': 'ಡೇಟಾ ಪಾಯಿಂಟ್ಸ್', 'Hindi': 'डेटा बिंदु', 'Tamil': 'தரவு புள்ளிகள்', 'Telugu': 'డేటా పాయింట్లు'},
    'Acc:': {'Kannada': 'ನಿಖರತೆ:', 'Hindi': 'सटीकता:', 'Tamil': 'துல்லியம்:', 'Telugu': 'ఖచ్చితత్వం:'},
    'F1:': {'Kannada': 'F1:', 'Hindi': 'F1:', 'Tamil': 'F1:', 'Telugu': 'F1:'},
    'Metrics': {'Kannada': 'ಮೆಟ್ರಿಕ್ಸ್', 'Hindi': 'मैट्रिक्स', 'Tamil': 'அளவீடுகள்', 'Telugu': 'కొలమానాలు'},
    'Feedback': {'Kannada': 'ಪ್ರತಿಕ್ರಿಯೆ', 'Hindi': 'प्रतिक्रिया', 'Tamil': 'பின்னூட்டம்', 'Telugu': 'అభిప్రాయం'},
    'Evaluations': {'Kannada': 'ಮೌಲ್ಯಮಾಪನಗಳು', 'Hindi': 'मूल्यांकन', 'Tamil': 'மதிப்பீடுகள்', 'Telugu': 'మూల్యాంకనాలు'},
    'Avg Rating': {'Kannada': 'ಸರಾಸರಿ ರೇಟಿಂಗ್', 'Hindi': 'औसत रेटिंग', 'Tamil': 'சராசரி மதிப்பீடு', 'Telugu': 'సగటు రేటింగ్'},
    'Running...': {'Kannada': 'ಚಾಲನೆಯಲ್ಲಿದೆ...', 'Hindi': 'चल रहा है...', 'Tamil': 'இயங்குகிறது...', 'Telugu': 'నడుస్తోంది...'},
    'Run Evaluation': {'Kannada': 'ಮೌಲ್ಯಮಾಪನವನ್ನು ಚಲಾಯಿಸಿ', 'Hindi': 'मूल्यांकन चलाएं', 'Tamil': 'மதிப்பீட்டை இயக்கவும்', 'Telugu': 'మూల్యాంకనాన్ని అమలు చేయండి'},
    'active alerts require attention': {'Kannada': 'ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳಿಗೆ ಗಮನ ಬೇಕು', 'Hindi': 'सक्रिय अलर्ट पर ध्यान देने की आवश्यकता है', 'Tamil': 'செயலில் உள்ள விழிப்பூட்டல்களுக்கு கவனம் தேவை', 'Telugu': 'క్రియాశీల హెచ్చరికలకు శ్రద్ధ అవసరం'},
    'Review high-severity alerts and take action on priority items.': {'Kannada': 'ಹೆಚ್ಚಿನ ತೀವ್ರತೆಯ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಆದ್ಯತೆಯ ಮೇರೆಗೆ ಕ್ರಮ ತೆಗೆದುಕೊಳ್ಳಿ.', 'Hindi': 'उच्च-गंभीरता अलर्ट की समीक्षा करें और प्राथमिकता वाले मदों पर कार्रवाई करें।', 'Tamil': 'அதிக தீவிரமான விழிப்பூட்டல்களை மதிப்பாய்வு செய்து முன்னுரிமை உருப்படிகள் மீது நடவடிக்கை எடுக்கவும்.', 'Telugu': 'అధిక-తీవ్రత హెచ్చరికలను సమీక్షించండి మరియు ప్రాధాన్యత అంశాలపై చర్య తీసుకోండి.'},
    'high-risk suspects need monitoring': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ಶಂಕಿತರಿಗೆ ನಿಗಾ ಬೇಕು', 'Hindi': 'उच्च जोखिम वाले संदिग्धों को निगरानी की आवश्यकता है', 'Tamil': 'அதிக ஆபத்துள்ள சந்தேக நபர்களுக்கு கண்காணிப்பு தேவை', 'Telugu': 'అధిక ప్రమాదమున్న అనుమానితుల పర్యవేక్షణ అవసరం'},
    'Consider increasing surveillance on repeat offenders with high risk scores.': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ಅಂಕಗಳನ್ನು ಹೊಂದಿರುವ ಪುನರಾವರ್ತಿತ ಅಪರಾಧಿಗಳ ಮೇಲೆ ಕಣ್ಗಾವಲು ಹೆಚ್ಚಿಸುವುದನ್ನು ಪರಿಗಣಿಸಿ.', 'Hindi': 'उच्च जोखिम स्कोर वाले बार-बार अपराध करने वालों पर निगरानी बढ़ाने पर विचार करें।', 'Tamil': 'அதிக ஆபத்து மதிப்பெண்களைக் கொண்ட மீண்டும் மீண்டும் குற்றம் செய்பவர்கள் மீதான கண்காணிப்பை அதிகரிப்பதைக் கவனியுங்கள்.', 'Telugu': 'అధిక రిస్క్ స్కోర్లు ఉన్న పునరావృత నేరస్థులపై నిఘా పెంచడాన్ని పరిగణించండి.'},
    'investigations need progress updates': {'Kannada': 'ತನಿಖೆಗಳಿಗೆ ಪ್ರಗತಿ ನವೀಕರಣಗಳು ಬೇಕಾಗುತ್ತವೆ', 'Hindi': 'जांच को प्रगति अपडेट की आवश्यकता है', 'Tamil': 'விசாரணைகளுக்கு முன்னேற்ற புதுப்பிப்புகள் தேவை', 'Telugu': 'దర్యాప్తులకు పురోగతి నవీకరణలు అవసరం'},
    'These investigations have low progress and may need additional resources.': {'Kannada': 'ಈ ತನಿಖೆಗಳು ಕಡಿಮೆ ಪ್ರಗತಿಯನ್ನು ಹೊಂದಿವೆ ಮತ್ತು ಹೆಚ್ಚುವರಿ ಸಂಪನ್ಮೂಲಗಳ ಅಗತ್ಯವಿರಬಹುದು.', 'Hindi': 'इन जांचों में कम प्रगति हुई है और इन्हें अतिरिक्त संसाधनों की आवश्यकता हो सकती है।', 'Tamil': 'இந்த விசாரணைகள் குறைந்த முன்னேற்றத்தைக் கொண்டுள்ளன மற்றும் கூடுதல் வளங்கள் தேவைப்படலாம்.', 'Telugu': 'ఈ పరిశోధనలకు తక్కువ పురోగతి ఉంది మరియు అదనపు వనరులు అవసరం కావచ్చు.'},
    'Pattern analysis suggests cross-district coordination': {'Kannada': 'ಮಾದರಿ ವಿಶ್ಲೇಷಣೆ ಅಡ್ಡ-ಜಿಲ್ಲಾ ಸಮನ್ವಯವನ್ನು ಸೂಚಿಸುತ್ತದೆ', 'Hindi': 'पैटर्न विश्लेषण अंतर-जिला समन्वय का सुझाव देता है', 'Tamil': 'முறை பகுப்பாய்வு குறுக்கு மாவட்ட ஒருங்கிணைப்பை பரிந்துரைக்கிறது', 'Telugu': 'నమూనా విశ్లేషణ క్రాస్-డిస్ట్రిక్ట్ సమన్వయాన్ని సూచిస్తుంది'},
    'Similar crime patterns detected across multiple districts. Consider joint operations.': {'Kannada': 'ಬಹು ಜಿಲ್ಲೆಗಳಾದ್ಯಂತ ಒಂದೇ ರೀತಿಯ ಅಪರಾಧ ಮಾದರಿಗಳು ಕಂಡುಬಂದಿವೆ. ಜಂಟಿ ಕಾರ್ಯಾಚರಣೆಗಳನ್ನು ಪರಿಗಣಿಸಿ.', 'Hindi': 'कई जिलों में इसी तरह के अपराध पैटर्न का पता चला। संयुक्त संचालन पर विचार करें।', 'Tamil': 'பல மாவட்டங்களில் ஒரே மாதிரியான குற்ற முறைகள் கண்டறியப்பட்டுள்ளன. கூட்டு நடவடிக்கைகளை கருதுங்கள்.', 'Telugu': 'బహుళ జిల్లాలలో సారూప్య నేర నమూనాలు కనుగొనబడ్డాయి. ఉమ్మడి కార్యకలాపాలను పరిగణించండి.'},
    'Predicted:': {'Kannada': 'ಊಹಿಸಲಾಗಿದೆ:', 'Hindi': 'भविष्यवाणी की:', 'Tamil': 'கணிக்கப்பட்டது:', 'Telugu': 'అంచనా వేయబడింది:'},
    'crimes': {'Kannada': 'ಅಪರಾಧಗಳು', 'Hindi': 'अपराध', 'Tamil': 'குற்றங்கள்', 'Telugu': 'నేరాలు'},
    'Confidence:': {'Kannada': 'ವಿಶ್ವಾಸ:', 'Hindi': 'आत्मविश्वास:', 'Tamil': 'நம்பிக்கை:', 'Telugu': 'విశ్వాసం:'},
    'pred': {'Kannada': 'ಮುನ್ಸೂಚನೆ', 'Hindi': 'भविष्यवाणी', 'Tamil': 'கணிப்பு', 'Telugu': 'అంచనా'},
    'No forecast data': {'Kannada': 'ಯಾವುದೇ ಮುನ್ಸೂಚನೆ ಡೇಟಾ ಇಲ್ಲ', 'Hindi': 'कोई पूर्वानुमान डेटा नहीं', 'Tamil': 'முன்னறிவிப்பு தரவு எதுவும் இல்லை', 'Telugu': 'సూచన డేటా లేదు'},
    'No priority cases': {'Kannada': 'ಯಾವುದೇ ಆದ್ಯತೆಯ ಪ್ರಕರಣಗಳಿಲ್ಲ', 'Hindi': 'कोई प्राथमिकता मामला नहीं', 'Tamil': 'முன்னுரிமை வழக்குகள் இல்லை', 'Telugu': 'ప్రాధాన్యత కేసులు లేవు'}
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
    for k, v in translations.items():
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
print("Updated translations.js with all AI Analytics component strings successfully.")
