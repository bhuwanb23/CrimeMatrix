import codecs
import re

translations = {
    'Priority Queue': {'Kannada': 'ಆದ್ಯತೆಯ ಸರತಿ', 'Hindi': 'प्राथमिकता कतार', 'Tamil': 'முன்னுரிமை வரிசை', 'Telugu': 'ప్రాధాన్యత క్యూ'},
    'No timeline events': {'Kannada': 'ಯಾವುದೇ ಟೈಮ್‌ಲೈನ್ ಘಟನೆಗಳಿಲ್ಲ', 'Hindi': 'कोई टाइमलाइन ईवेंट नहीं', 'Tamil': 'காலவரிசை நிகழ்வுகள் இல்லை', 'Telugu': 'టైమ్‌లైన్ ఈవెంట్‌లు లేవు'},
    'Court': {'Kannada': 'ನ್ಯಾಯಾಲಯ', 'Hindi': 'न्यायालय', 'Tamil': 'நீதிமன்றம்', 'Telugu': 'కోర్టు'},
    'Real-time crime monitoring and risk detection': {'Kannada': 'ನೈಜ ಸಮಯದ ಅಪರಾಧ ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ಅಪಾಯ ಪತ್ತೆ', 'Hindi': 'रीयल-टाइम अपराध निगरानी और जोखिम का पता लगाना', 'Tamil': 'நிகழ்நேர குற்ற கண்காணிப்பு மற்றும் அபாய கண்டறிதல்', 'Telugu': 'రియల్-టైమ్ క్రైమ్ పర్యవేక్షణ మరియు రిస్క్ గుర్తింపు'},
    'Crime Head': {'Kannada': 'ಅಪರಾಧದ ಮುಖ್ಯಸ್ಥ', 'Hindi': 'अपराध प्रमुख', 'Tamil': 'குற்றப் பிரிவு', 'Telugu': 'క్రైమ్ హెడ్'},
    'Officer': {'Kannada': 'ಅಧಿಕಾರಿ', 'Hindi': 'अधिकारी', 'Tamil': 'அதிகாரி', 'Telugu': 'అధికారి'},
    'Critical': {'Kannada': 'ನಿರ್ಣಾಯಕ', 'Hindi': 'गंभीर', 'Tamil': 'சிக்கலான', 'Telugu': 'క్లిష్టమైన'},
    'Loading timeline...': {'Kannada': 'ಟೈಮ್‌ಲೈನ್ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'टाइमलाइन लोड हो रही है...', 'Tamil': 'காலவரிசை ஏற்றப்படுகிறது...', 'Telugu': 'టైమ్‌లైన్ లోడ్ అవుతోంది...'},
    'No suspects identified': {'Kannada': 'ಯಾವುದೇ ಶಂಕಿತರನ್ನು ಗುರುತಿಸಲಾಗಿಲ್ಲ', 'Hindi': 'किसी भी संदिग्ध की पहचान नहीं हुई', 'Tamil': 'சந்தேகநபர்கள் அடையாளம் காணப்படவில்லை', 'Telugu': 'ఎటువంటి అనుమానితులను గుర్తించలేదు'},
    'Crime No': {'Kannada': 'ಅಪರಾಧ ಸಂಖ್ಯೆ', 'Hindi': 'अपराध संख्या', 'Tamil': 'குற்ற எண்', 'Telugu': 'క్రైమ్ నంబర్'},
    'Bookmarks': {'Kannada': 'ಬುಕ್‌ಮಾರ್ಕ್‌ಗಳು', 'Hindi': 'बुकमार्क', 'Tamil': 'புக்மார்க்குகள்', 'Telugu': 'బుక్‌మార్క్‌లు'},
    'Officer Workload': {'Kannada': 'ಅಧಿಕಾರಿಗಳ ಕೆಲಸದ ಹೊರೆ', 'Hindi': 'अधिकारी कार्यभार', 'Tamil': 'அதிகாரியின் பணிச்சுமை', 'Telugu': 'అధికారి పనిభారం'},
    'Intelligence Alerts': {'Kannada': 'ಗುಪ್ತಚರ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'खुफिया अलर्ट', 'Tamil': 'உளவுத்துறை எச்சரிக்கைகள்', 'Telugu': 'ఇంటెలిజెన్స్ హెచ్చరికలు'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'सबूत', 'Tamil': 'சான்று', 'Telugu': 'సాక్ష్యం'},
    'Early Warning Alerts': {'Kannada': 'ಆರಂಭಿಕ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'प्रारंभिक चेतावनी अलर्ट', 'Tamil': 'ஆரம்ப எச்சரிக்கைகள்', 'Telugu': 'ముందస్తు హెచ్చరికలు'},
    'Gravity Offence': {'Kannada': 'ಗಂಭೀರ ಅಪರಾಧ', 'Hindi': 'गंभीर अपराध', 'Tamil': 'கடுமையான குற்றம்', 'Telugu': 'తీవ్రమైన నేరం'},
    'Crime Analytics': {'Kannada': 'ಅಪರಾಧ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'अपराध एनालिटिक्स', 'Tamil': 'குற்ற பகுப்பாய்வு', 'Telugu': 'క్రైమ్ అనలిటిక్స్'},
    'Criminal Timeline': {'Kannada': 'ಕ್ರಿಮಿನಲ್ ಟೈಮ್‌ಲೈನ್', 'Hindi': 'आपराधिक टाइमलाइन', 'Tamil': 'குற்ற காலவரிசை', 'Telugu': 'క్రిమినల్ టైమ్‌లైన్'},
    'Alert Trend': {'Kannada': 'ಎಚ್ಚರಿಕೆ ಪ್ರವೃತ್ತಿ', 'Hindi': 'अलर्ट ट्रेंड', 'Tamil': 'எச்சரிக்கை போக்கு', 'Telugu': 'హెచ్చరిక ట్రెండ్'},
    'Case Category': {'Kannada': 'ಪ್ರಕರಣದ ವರ್ಗ', 'Hindi': 'मामला श्रेणी', 'Tamil': 'வழக்கு வகை', 'Telugu': 'కేసు వర్గం'},
    'Loading alerts...': {'Kannada': 'ಎಚ್ಚರಿಕೆಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...', 'Hindi': 'अलर्ट लोड हो रहे हैं...', 'Tamil': 'எச்சரிக்கைகள் ஏற்றப்படுகின்றன...', 'Telugu': 'హెచ్చరికలు లోడ్ అవుతున్నాయి...'},
    'Station': {'Kannada': 'ಠಾಣೆ', 'Hindi': 'स्टेशन', 'Tamil': 'நிலையம்', 'Telugu': 'స్టేషన్'},
    'Description': {'Kannada': 'ವಿವರಣೆ', 'Hindi': 'विवरण', 'Tamil': 'விளக்கம்', 'Telugu': 'వివరణ'},
    'Case No': {'Kannada': 'ಪ್ರಕರಣ ಸಂಖ್ಯೆ', 'Hindi': 'मामला संख्या', 'Tamil': 'வழக்கு எண்', 'Telugu': 'కేసు నంబర్'},
    'Case Information': {'Kannada': 'ಪ್ರಕರಣದ ಮಾಹಿತಿ', 'Hindi': 'मामले की जानकारी', 'Tamil': 'வழக்கு தகவல்', 'Telugu': 'కేసు సమాచారం'},
    'Pending Review': {'Kannada': 'ವಿಮರ್ಶೆ ಬಾಕಿ ಇದೆ', 'Hindi': 'समीक्षा लंबित', 'Tamil': 'மதிப்பாய்வு நிலுவையில் உள்ளது', 'Telugu': 'సమీక్ష పెండింగ్‌లో ఉంది'},
    'Recent Alerts': {'Kannada': 'ಇತ್ತೀಚಿನ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'हाल के अलर्ट', 'Tamil': 'சமீபத்திய எச்சரிக்கைகள்', 'Telugu': 'ఇటీవలి హెచ్చరికలు'},
    'Search': {'Kannada': 'ಹುಡುಕಾಟ', 'Hindi': 'खोज', 'Tamil': 'தேடல்', 'Telugu': 'శోధన'},
    'Case prioritization engine and AI-powered proactive monitoring': {'Kannada': 'ಪ್ರಕರಣ ಆದ್ಯತೆ ಎಂಜಿನ್ ಮತ್ತು AI ಪೂರ್ವಭಾವಿ ಮೇಲ್ವಿಚಾರಣೆ', 'Hindi': 'केस प्राथमिकता इंजन और एआई सक्रिय निगरानी', 'Tamil': 'வழக்கு முன்னுரிமை இயந்திரம் மற்றும் AI செயல்திறன் கண்காணிப்பு', 'Telugu': 'కేసు ప్రాధాన్యత ఇంజిన్ మరియు AI చురుకైన పర్యవేక్షణ'},
    'Loading bookmarks...': {'Kannada': 'ಬುಕ್‌ಮಾರ್ಕ್‌ಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...', 'Hindi': 'बुकमार्क लोड हो रहे हैं...', 'Tamil': 'புக்மார்க்குகள் ஏற்றப்படுகின்றன...', 'Telugu': 'బుక్‌మార్క్‌లు లోడ్ అవుతున్నాయి...'},
    'Alerts By Type': {'Kannada': 'ಪ್ರಕಾರದ ಮೂಲಕ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'प्रकार द्वारा अलर्ट', 'Tamil': 'வகை வாரியாக எச்சரிக்கைகள்', 'Telugu': 'రకం ద్వారా హెచ్చరికలు'},
    'No alerts found': {'Kannada': 'ಯಾವುದೇ ಎಚ್ಚರಿಕೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई अलर्ट नहीं मिला', 'Tamil': 'எச்சரிக்கைகள் எதுவும் காணப்படவில்லை', 'Telugu': 'హెచ్చరికలు ఏవీ కనుగొనబడలేదు'},
    'Refresh': {'Kannada': 'ರಿಫ್ರೆಶ್ ಮಾಡಿ', 'Hindi': 'रिफ्रेश करें', 'Tamil': 'புதுப்பிக்கவும்', 'Telugu': 'రిఫ్రెష్ చేయండి'},
    'Type': {'Kannada': 'ಪ್ರಕಾರ', 'Hindi': 'प्रकार', 'Tamil': 'வகை', 'Telugu': 'రకం'},
    'Case not found': {'Kannada': 'ಪ್ರಕರಣ ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'मामला नहीं मिला', 'Tamil': 'வழக்கு காணப்படவில்லை', 'Telugu': 'కేసు కనుగొనబడలేదు'},
    'All Districts': {'Kannada': 'ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು', 'Hindi': 'सभी जिले', 'Tamil': 'அனைத்து மாவட்டங்கள்', 'Telugu': 'అన్ని జిల్లాలు'},
    'High': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'Active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకైన'},
    'No evidence collected': {'Kannada': 'ಯಾವುದೇ ಸಾಕ್ಷ್ಯ ಸಂಗ್ರಹಿಸಿಲ್ಲ', 'Hindi': 'कोई सबूत एकत्र नहीं किया गया', 'Tamil': 'எந்த சான்றும் சேகரிக்கப்படவில்லை', 'Telugu': 'ఎటువంటి సాక్ష్యం సేకరించబడలేదు'},
    'Monitor and respond to proactive intelligence': {'Kannada': 'ಪೂರ್ವಭಾವಿ ಗುಪ್ತಚರವನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ ಮತ್ತು ಪ್ರತಿಕ್ರಿಯಿಸಿ', 'Hindi': 'सक्रिय खुफिया निगरानी और प्रतिक्रिया', 'Tamil': 'செயல்திறன் மிக்க உளவுத்துறையை கண்காணிக்கவும் மற்றும் பதிலளிக்கவும்', 'Telugu': 'చురుకైన ఇంటెలిజెన్స్‌ను పర్యవేక్షించండి మరియు ప్రతిస్పందించండి'},
    'Timeline': {'Kannada': 'ಟೈಮ್‌ಲೈನ್', 'Hindi': 'टाइमलाइन', 'Tamil': 'காலவரிசை', 'Telugu': 'టైమ్‌లైన్'},
    'Priority & Proactive Intelligence': {'Kannada': 'ಆದ್ಯತೆ ಮತ್ತು ಪೂರ್ವಭಾವಿ ಗುಪ್ತಚರ', 'Hindi': 'प्राथमिकता और सक्रिय खुफिया', 'Tamil': 'முன்னுரிமை மற்றும் செயல்திறன் மிக்க உளவுத்துறை', 'Telugu': 'ప్రాధాన్యత మరియు చురుకైన ఇంటెలిజెన్స్'},
    'Total Events': {'Kannada': 'ಒಟ್ಟು ಘಟನೆಗಳು', 'Hindi': 'कुल ईवेंट', 'Tamil': 'மொத்த நிகழ்வுகள்', 'Telugu': 'మొత్తం ఈవెంట్‌లు'},
    'Priority': {'Kannada': 'ಆದ್ಯತೆ', 'Hindi': 'प्राथमिकता', 'Tamil': 'முன்னுரிமை', 'Telugu': 'ప్రాధాన్యత'},
    'Suspects': {'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேகநபர்கள்', 'Telugu': 'అనుమానితులు'},
    'District': {'Kannada': 'ಜಿಲ್ಲೆ', 'Hindi': 'जिला', 'Tamil': 'மாவட்டம்', 'Telugu': 'జిల్లా'},
    'Incident Details': {'Kannada': 'ಘಟನೆಯ ವಿವರಗಳು', 'Hindi': 'घटना का विवरण', 'Tamil': 'நிகழ்வின் விவரங்கள்', 'Telugu': 'సంఘటన వివరాలు'},
    'Back to Search': {'Kannada': 'ಹುಡುಕಾಟಕ್ಕೆ ಹಿಂತಿರುಗಿ', 'Hindi': 'खोज पर वापस जाएं', 'Tamil': 'தேடலுக்குத் திரும்பு', 'Telugu': 'శోధనకు తిరిగి వెళ్ళు'},
    'Loading prediction analytics...': {'Kannada': 'ಮುನ್ಸೂಚನೆ ವಿಶ್ಲೇಷಣೆ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'भविष्यवाणी एनालिटिक्स लोड हो रहा है...', 'Tamil': 'கணிப்பு பகுப்பாய்வு ஏற்றப்படுகிறது...', 'Telugu': 'ప్రిడిక్షన్ అనలిటిక్స్ లోడ్ అవుతోంది...'},
    'Brief Facts': {'Kannada': 'ಸಂಕ್ಷಿಪ್ತ ಸಂಗತಿಗಳು', 'Hindi': 'संक्षिप्त तथ्य', 'Tamil': 'சுருக்கமான உண்மைகள்', 'Telugu': 'సంక్షిప్త వాస్తవాలు'},
    'No bookmarks yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಬುಕ್‌ಮಾರ್ಕ್‌ಗಳಿಲ್ಲ', 'Hindi': 'अभी तक कोई बुकमार्क नहीं', 'Tamil': 'இதுவரை புக்மார்க்குகள் இல்லை', 'Telugu': 'ఇంకా బుక్‌మార్క్‌లు లేవు'},
    'New Alerts': {'Kannada': 'ಹೊಸ ಎಚ್ಚರಿಕೆಗಳು', 'Hindi': 'नए अलर्ट', 'Tamil': 'புதிய எச்சரிக்கைகள்', 'Telugu': 'కొత్త హెచ్చరికలు'},
    'Resolved': {'Kannada': 'ಪರಿಹರಿಸಲಾಗಿದೆ', 'Hindi': 'हल किया गया', 'Tamil': 'தீர்க்கப்பட்டது', 'Telugu': 'పరిష్కరించబడింది'},
    'AI Insights': {'Kannada': 'AI ಒಳನೋಟಗಳು', 'Hindi': 'एआई अंतर्दृष्टि', 'Tamil': 'AI நுண்ணறிவு', 'Telugu': 'AI అంతర్దృష్టులు'},
    'Date Filed': {'Kannada': 'ದಾಖಲಿಸಿದ ದಿನಾಂಕ', 'Hindi': 'दर्ज की गई तिथि', 'Tamil': 'தாக்கல் செய்யப்பட்ட தேதி', 'Telugu': 'దాఖలు చేసిన తేదీ'},
    'Alert Performance Summary': {'Kannada': 'ಎಚ್ಚರಿಕೆ ಕಾರ್ಯಕ್ಷಮತೆ ಸಾರಾಂಶ', 'Hindi': 'अलर्ट प्रदर्शन सारांश', 'Tamil': 'எச்சரிக்கை செயல்திறன் சுருக்கம்', 'Telugu': 'హెచ్చరిక పనితీరు సారాంశం'},
    'Alert Distribution': {'Kannada': 'ಎಚ್ಚರಿಕೆ ವಿತರಣೆ', 'Hindi': 'अलर्ट वितरण', 'Tamil': 'எச்சரிக்கை விநியோகம்', 'Telugu': 'హెచ్చరిక పంపిణీ'},
    'Investigations': {'Kannada': 'ತನಿಖೆಗಳು', 'Hindi': 'जांच', 'Tamil': 'விசாரணைகள்', 'Telugu': 'దర్యాప్తులు'},
    'Location': {'Kannada': 'ಸ್ಥಳ', 'Hindi': 'स्थान', 'Tamil': 'இடம்', 'Telugu': 'స్థానం'},
    'No workload data available': {'Kannada': 'ಯಾವುದೇ ಕೆಲಸದ ಹೊರೆ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ', 'Hindi': 'कोई कार्यभार डेटा उपलब्ध नहीं', 'Tamil': 'பணிச்சுமை தரவு எதுவும் கிடைக்கவில்லை', 'Telugu': 'ఎటువంటి పనిభారం డేటా అందుబాటులో లేదు'},
    'Classification': {'Kannada': 'ವರ್ಗೀಕರಣ', 'Hindi': 'वर्गीकरण', 'Tamil': 'வகைப்பாடு', 'Telugu': 'వర్గీకరణ'}
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
text = re.sub(r"('[^']*'|\"[^\"]*\")(\s*\r?\n\s*)(['\"][a-zA-Z\s]+['\"]\:)", r"\1,\2\3", text)

with codecs.open(trans_file, 'w', 'utf-8') as f:
    f.write(text)
print("Updated translations.js with all component strings successfully.")
