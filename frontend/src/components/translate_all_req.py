import os
import re
import codecs

# Define the strings to translate
translations = {
    'Actions': {'Kannada': 'ಕ್ರಿಯೆಗಳು', 'Hindi': 'कार्रवाइयां', 'Tamil': 'செயல்கள்', 'Telugu': 'చర్యలు'},
    'Active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకుగా'},
    'All': {'Kannada': 'ಎಲ್ಲಾ', 'Hindi': 'सभी', 'Tamil': 'அனைத்தும்', 'Telugu': 'అన్ని'},
    'Assault': {'Kannada': 'ಹಲ್ಲೆ', 'Hindi': 'हमला', 'Tamil': 'தாக்குதல்', 'Telugu': 'దాడి'},
    'Assign': {'Kannada': 'ನಿಯೋಜಿಸಿ', 'Hindi': 'सौंपें', 'Tamil': 'ஒதுக்கு', 'Telugu': 'కేటాయించండి'},
    'Bengaluru': {'Kannada': 'ಬೆಂಗಳೂರು', 'Hindi': 'बेंगलुरु', 'Tamil': 'பெங்களூரு', 'Telugu': 'బెంగళూరు'},
    'Case': {'Kannada': 'ಪ್ರಕರಣ', 'Hindi': 'मामला', 'Tamil': 'வழக்கு', 'Telugu': 'కేసు'},
    'Cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'Clear all': {'Kannada': 'ಎಲ್ಲವನ್ನೂ ತೆರವುಗೊಳಿಸಿ', 'Hindi': 'सभी साफ़ करें', 'Tamil': 'அனைத்தையும் அழி', 'Telugu': 'అన్నీ క్లియర్ చేయండి'},
    'Close': {'Kannada': 'ಮುಚ್ಚಿ', 'Hindi': 'बंद करें', 'Tamil': 'மூடு', 'Telugu': 'మూసివేయు'},
    'Court Report': {'Kannada': 'ನ್ಯಾಯಾಲಯದ ವರದಿ', 'Hindi': 'न्यायालय रिपोर्ट', 'Tamil': 'நீதிமன்ற அறிக்கை', 'Telugu': 'కోర్టు నివేదిక'},
    'Crime No': {'Kannada': 'ಅಪರಾಧ ಸಂಖ್ಯೆ', 'Hindi': 'अपराध संख्या', 'Tamil': 'குற்ற எண்', 'Telugu': 'క్రైమ్ నంబర్'},
    'Crime Type': {'Kannada': 'ಅಪರಾಧ ಪ್ರಕಾರ', 'Hindi': 'अपराध प्रकार', 'Tamil': 'குற்ற வகை', 'Telugu': 'నేర రకం'},
    'Cross-District': {'Kannada': 'ಅಂತರ-ಜಿಲ್ಲೆ', 'Hindi': 'अंतर-ज़िला', 'Tamil': 'மாவட்டங்களுக்கு இடையிலான', 'Telugu': 'క్రాస్-జిల్లా'},
    'Current Week': {'Kannada': 'ಪ್ರಸ್ತುತ ವಾರ', 'Hindi': 'वर्तमान सप्ताह', 'Tamil': 'நடப்பு வாரம்', 'Telugu': 'ప్రస్తుత వారం'},
    'Cybercrime': {'Kannada': 'ಸೈಬರ್ ಅಪರಾಧ', 'Hindi': 'साइबर अपराध', 'Tamil': 'சைபர் குற்றம்', 'Telugu': 'సైబర్ క్రైమ్'},
    'Date': {'Kannada': 'ದಿನಾಂಕ', 'Hindi': 'दिनांक', 'Tamil': 'தேதி', 'Telugu': 'తేదీ'},
    'Delete': {'Kannada': 'ಅಳಿಸಿ', 'Hindi': 'हटाएं', 'Tamil': 'நீக்கு', 'Telugu': 'తొలగించు'},
    'Dismiss': {'Kannada': 'ವಜಾಗೊಳಿಸಿ', 'Hindi': 'खारिज करें', 'Tamil': 'நிராகரி', 'Telugu': 'తిరస్కరించండి'},
    'District': {'Kannada': 'ಜಿಲ್ಲೆ', 'Hindi': 'ज़िला', 'Tamil': 'மாவட்டம்', 'Telugu': 'జిల్లా'},
    'Download': {'Kannada': 'ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ', 'Hindi': 'डाउनलोड करें', 'Tamil': 'பதிவிறக்க', 'Telugu': 'డౌన్‌లోడ్ చేయండి'},
    'Draft': {'Kannada': 'ಕರಡು', 'Hindi': 'मसौदा', 'Tamil': 'வரைவு', 'Telugu': 'డ్రాఫ్ట్'},
    'Escalation': {'Kannada': 'ಉಲ್ಬಣ', 'Hindi': 'वृद्धि', 'Tamil': 'தீவிரமடைதல்', 'Telugu': 'తీవ్రతరం'},
    'Events will appear here as new data comes in': {'Kannada': 'ಹೊಸ ಡೇಟಾ ಬಂದಂತೆ ಈವೆಂಟ್‌ಗಳು ಇಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತವೆ', 'Hindi': 'नया डेटा आने पर इवेंट यहां दिखाई देंगे', 'Tamil': 'புதிய தரவு வரும்போது நிகழ்வுகள் இங்கே தோன்றும்', 'Telugu': 'కొత్త డేటా వచ్చినప్పుడు ఈవెంట్‌లు ఇక్కడ కనిపిస్తాయి'},
    'Evidence': {'Kannada': 'ಸಾಕ್ಷ್ಯ', 'Hindi': 'सबूत', 'Tamil': 'ஆதாரம்', 'Telugu': 'సాక్ష్యం'},
    'Evidence Review': {'Kannada': 'ಸಾಕ್ಷ್ಯ ವಿಮರ್ಶೆ', 'Hindi': 'साक्ष्य समीक्षा', 'Tamil': 'ஆதார மதிப்பாய்வு', 'Telugu': 'సాక్ష్యం సమీక్ష'},
    'Export': {'Kannada': 'ರಫ್ತು ಮಾಡಿ', 'Hindi': 'निर्यात', 'Tamil': 'ஏற்றுமதி செய்', 'Telugu': 'ఎగుమతి చేయండి'},
    'Export CSV': {'Kannada': 'CSV ರಫ್ತು ಮಾಡಿ', 'Hindi': 'CSV निर्यात करें', 'Tamil': 'CSV ஏற்றுமதி செய்', 'Telugu': 'CSV ఎగుమతి చేయండి'},
    'FIR': {'Kannada': 'ಎಫ್‌ಐಆರ್', 'Hindi': 'एफआईआर', 'Tamil': 'முதல் தகவல் அறிக்கை (FIR)', 'Telugu': 'ఎఫ్ఐఆర్'},
    'Filed': {'Kannada': 'ದಾಖಲಿಸಲಾಗಿದೆ', 'Hindi': 'दायर', 'Tamil': 'தாக்கல் செய்யப்பட்டது', 'Telugu': 'దాఖలు చేయబడింది'},
    'Final': {'Kannada': 'ಅಂತಿಮ', 'Hindi': 'अंतिम', 'Tamil': 'இறுதி', 'Telugu': 'చివరి'},
    'Fraud': {'Kannada': 'ವಂಚನೆ', 'Hindi': 'धोखाधड़ी', 'Tamil': 'மோசடி', 'Telugu': 'మోసం'},
    'Generating...': {'Kannada': 'ರಚಿಸಲಾಗುತ್ತಿದೆ...', 'Hindi': 'जनरेट हो रहा है...', 'Tamil': 'உருவாக்குகிறது...', 'Telugu': 'ఉత్పత్తి చేస్తోంది...'},
    'High': {'Kannada': 'ಹೆಚ್ಚಿನ', 'Hindi': 'उच्च', 'Tamil': 'உயர்', 'Telugu': 'అధిక'},
    'In Queue': {'Kannada': 'ಸರತಿಯಲ್ಲಿದೆ', 'Hindi': 'कतार में', 'Tamil': 'வரிசையில் உள்ளது', 'Telugu': 'క్యూలో ఉంది'},
    'Investigation': {'Kannada': 'ತನಿಖೆ', 'Hindi': 'जांच', 'Tamil': 'விசாரணை', 'Telugu': 'దర్యాప్తు'},
    'Live Activity Feed': {'Kannada': 'ಲೈವ್ ಚಟುವಟಿಕೆ ಫೀಡ್', 'Hindi': 'लाइव गतिविधि फ़ीड', 'Tamil': 'நேரடி செயல்பாடு ஊட்டம்', 'Telugu': 'ప్రత్యక్ష కార్యాచరణ ఫీడ్'},
    'Loading...': {'Kannada': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...', 'Hindi': 'लोड हो रहा है...', 'Tamil': 'ஏற்றுகிறது...', 'Telugu': 'లోడ్ అవుతోంది...'},
    'Low': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'निम्न', 'Tamil': 'குறைந்த', 'Telugu': 'తక్కువ'},
    'MO Pattern': {'Kannada': 'MO ಮಾದರಿ', 'Hindi': 'एमओ पैटर्न', 'Tamil': 'MO மாதிரி', 'Telugu': 'MO ప్యాటర్న్'},
    'Medium': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தர', 'Telugu': 'మధ్యస్థ'},
    'Mysuru': {'Kannada': 'ಮೈಸೂರು', 'Hindi': 'मैसूर', 'Tamil': 'மைசூர்', 'Telugu': 'మైసూరు'},
    'Needs attention': {'Kannada': 'ಗಮನ ಹರಿಸಬೇಕಾಗಿದೆ', 'Hindi': 'ध्यान देने की आवश्यकता है', 'Tamil': 'கவனம் தேவை', 'Telugu': 'శ్రద్ధ అవసరం'},
    'No notifications': {'Kannada': 'ಯಾವುದೇ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ', 'Hindi': 'कोई अधिसूचना नहीं', 'Tamil': 'அறிவிப்புகள் இல்லை', 'Telugu': 'నోటిఫికేషన్‌లు లేవు'},
    'No recent activity': {'Kannada': 'ಯಾವುದೇ ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ ಇಲ್ಲ', 'Hindi': 'कोई हालिया गतिविधि नहीं', 'Tamil': 'சமீபத்திய செயல்பாடு இல்லை', 'Telugu': 'ఇటీవలి కార్యాచరణ లేదు'},
    'No results found': {'Kannada': 'ಯಾವುದೇ ಫಲಿತಾಂಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'कोई परिणाम नहीं मिला', 'Tamil': 'முடிவுகள் எதுவும் கிடைக்கவில்லை', 'Telugu': 'ఎటువంటి ఫలితాలు కనుగొనబడలేదు'},
    'No saved searches': {'Kannada': 'ಉಳಿಸಿದ ಹುಡುಕಾಟಗಳಿಲ್ಲ', 'Hindi': 'कोई सहेजी गई खोज नहीं', 'Tamil': 'சேமிக்கப்பட்ட தேடல்கள் இல்லை', 'Telugu': 'సేవ్ చేసిన శోధనలు లేవు'},
    'No search history': {'Kannada': 'ಯಾವುದೇ ಹುಡುಕಾಟ ಇತಿಹಾಸವಿಲ್ಲ', 'Hindi': 'कोई खोज इतिहास नहीं', 'Tamil': 'தேடல் வரலாறு இல்லை', 'Telugu': 'శోధన చరిత్ర లేదు'},
    'Not useful': {'Kannada': 'ಉಪಯುಕ್ತವಲ್ಲ', 'Hindi': 'उपयोगी नहीं', 'Tamil': 'பயனுள்ளதாக இல்லை', 'Telugu': 'ఉపయోగకరం కాదు'},
    'Notifications': {'Kannada': 'ಅಧಿಸೂಚನೆಗಳು', 'Hindi': 'सूचनाएं', 'Tamil': 'அறிவிப்புகள்', 'Telugu': 'నోటిఫికేషన్‌లు'},
    'Officer': {'Kannada': 'ಅಧಿಕಾರಿ', 'Hindi': 'अधिकारी', 'Tamil': 'அதிகாரி', 'Telugu': 'అధికారి'},
    'Officer Assignment': {'Kannada': 'ಅಧಿಕಾರಿ ನಿಯೋಜನೆ', 'Hindi': 'अधिकारी असाइनमेंट', 'Tamil': 'அதிகாரி பணி ஒதுக்கீடு', 'Telugu': 'అధికారి కేటాయింపు'},
    'Open': {'Kannada': 'ತೆರೆದ', 'Hindi': 'खुला', 'Tamil': 'திறந்த', 'Telugu': 'తెరిచి ఉంది'},
    'Pages': {'Kannada': 'ಪುಟಗಳು', 'Hindi': 'पृष्ठ', 'Tamil': 'பக்கங்கள்', 'Telugu': 'పేజీలు'},
    'Pending': {'Kannada': 'ಬಾಕಿ ಉಳಿದಿದೆ', 'Hindi': 'लंबित', 'Tamil': 'நிலுவையில் உள்ளது', 'Telugu': 'పెండింగ్‌లో ఉంది'},
    'Priority Escalation': {'Kannada': 'ಆದ್ಯತೆಯ ಉಲ್ಬಣ', 'Hindi': 'प्राथमिकता वृद्धि', 'Tamil': 'முன்னுரிமை தீவிரமடைதல்', 'Telugu': 'ప్రాధాన్యత తీవ్రతరం'},
    'Processed': {'Kannada': 'ಸಂಸ್ಕರಿಸಲಾಗಿದೆ', 'Hindi': 'संसाधित', 'Tamil': 'செயலாக்கப்பட்டது', 'Telugu': 'ప్రాసెస్ చేయబడింది'},
    'Related': {'Kannada': 'ಸಂಬಂಧಿತ', 'Hindi': 'संबंधित', 'Tamil': 'தொடர்புடைய', 'Telugu': 'సంబంధిత'},
    'Related Investigation': {'Kannada': 'ಸಂಬಂಧಿತ ತನಿಖೆ', 'Hindi': 'संबंधित जांच', 'Tamil': 'தொடர்புடைய விசாரணை', 'Telugu': 'సంబంధిత దర్యాప్తు'},
    'Report ID': {'Kannada': 'ವರದಿ ಐಡಿ', 'Hindi': 'रिपोर्ट आईडी', 'Tamil': 'அறிக்கை ஐடி', 'Telugu': 'నివేదిక ID'},
    'Report Statistics': {'Kannada': 'ವರದಿ ಅಂಕಿಅಂಶಗಳು', 'Hindi': 'रिपोर्ट सांख्यिकी', 'Tamil': 'அறிக்கை புள்ளிவிவரங்கள்', 'Telugu': 'నివేదిక గణాంకాలు'},
    'Reports': {'Kannada': 'ವರದಿಗಳು', 'Hindi': 'रिपोर्ट', 'Tamil': 'அறிக்கைகள்', 'Telugu': 'నివేదికలు'},
    'Run search': {'Kannada': 'ಹುಡುಕಾಟ ಚಲಾಯಿಸಿ', 'Hindi': 'खोज चलाएं', 'Tamil': 'தேடலை இயக்கு', 'Telugu': 'శోధనను అమలు చేయండి'},
    'Save current search': {'Kannada': 'ಪ್ರಸ್ತುತ ಹುಡುಕಾಟವನ್ನು ಉಳಿಸಿ', 'Hindi': 'वर्तमान खोज सहेजें', 'Tamil': 'தற்போதைய தேடலைச் சேமி', 'Telugu': 'ప్రస్తుత శోధనను సేవ్ చేయండి'},
    'Save search': {'Kannada': 'ಹುಡುಕಾಟವನ್ನು ಉಳಿಸಿ', 'Hindi': 'खोज सहेजें', 'Tamil': 'தேடலைச் சேமி', 'Telugu': 'శోధనను సేవ్ చేయండి'},
    'Saved Searches': {'Kannada': 'ಉಳಿಸಿದ ಹುಡುಕಾಟಗಳು', 'Hindi': 'सहेजी गई खोजें', 'Tamil': 'சேமிக்கப்பட்ட தேடல்கள்', 'Telugu': 'సేవ్ చేసిన శోధనలు'},
    'Search History': {'Kannada': 'ಹುಡುಕಾಟ ಇತಿಹಾಸ', 'Hindi': 'खोज इतिहास', 'Tamil': 'தேடல் வரலாறு', 'Telugu': 'శోధన చరిత్ర'},
    'Search by report ID, title, case...': {'Kannada': 'ವರದಿ ಐಡಿ, ಶೀರ್ಷಿಕೆ, ಪ್ರಕರಣದ ಮೂಲಕ ಹುಡುಕಿ...', 'Hindi': 'रिपोर्ट आईडी, शीर्षक, मामले के आधार पर खोजें...', 'Tamil': 'அறிக்கை ஐடி, தலைப்பு, வழக்கு மூலம் தேடுக...', 'Telugu': 'నివేదిక ID, శీర్షిక, కేసు ద్వారా శోధించండి...'},
    'Search crimes, suspects, FIRs, evidence...': {'Kannada': 'ಅಪರಾಧಗಳು, ಶಂಕಿತರು, ಎಫ್‌ಐಆರ್‌ಗಳು, ಸಾಕ್ಷ್ಯಗಳನ್ನು ಹುಡುಕಿ...', 'Hindi': 'अपराधों, संदिग्धों, एफआईआर, सबूतों की खोज करें...', 'Tamil': 'குற்றங்கள், சந்தேக நபர்கள், FIRகள், ஆதாரங்களை தேடுக...', 'Telugu': 'నేరాలు, అనుమానితులు, FIRలు, సాక్ష్యాలను శోధించండి...'},
    'Search naturally — e.g. "thefts in Bengaluru last month"': {'Kannada': 'ಸಹಜವಾಗಿ ಹುಡುಕಿ — ಉದಾ. "ಕಳೆದ ತಿಂಗಳು ಬೆಂಗಳೂರಿನಲ್ಲಿ ಕಳ್ಳತನಗಳು"', 'Hindi': 'स्वाभाविक रूप से खोजें - उदा. "पिछले महीने बेंगलुरु में चोरी"', 'Tamil': 'இயல்பாக தேடுக — எ.கா. "கடந்த மாதம் பெங்களூருவில் திருட்டுகள்"', 'Telugu': 'సహజంగా శోధించండి — ఉదా. "గత నెల బెంగళూరులో దొంగతనాలు"'},
    'Searching...': {'Kannada': 'ಹುಡುಕಲಾಗುತ್ತಿದೆ...', 'Hindi': 'खोज हो रही है...', 'Tamil': 'தேடுகிறது...', 'Telugu': 'శోధిస్తోంది...'},
    'Similar Case': {'Kannada': 'ಇದೇ ರೀತಿಯ ಪ್ರಕರಣ', 'Hindi': 'समान मामला', 'Tamil': 'இதே போன்ற வழக்கு', 'Telugu': 'సారూప్య కేసు'},
    'Status': {'Kannada': 'ಸ್ಥಿತಿ', 'Hindi': 'स्थिति', 'Tamil': 'நிலை', 'Telugu': 'స్థితి'},
    'Suspect Alert': {'Kannada': 'ಶಂಕಿತ ಎಚ್ಚರಿಕೆ', 'Hindi': 'संदिग्ध अलर्ट', 'Tamil': 'சந்தேக நபர் எச்சரிக்கை', 'Telugu': 'అనుమానిత హెచ్చరిక'},
    'Suspects': {'Kannada': 'ಶಂಕಿತರು', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்கள்', 'Telugu': 'అనుమానితులు'},
    'Theft': {'Kannada': 'ಕಳ್ಳತನ', 'Hindi': 'चोरी', 'Tamil': 'திருட்டு', 'Telugu': 'దొంగతనం'},
    'Title': {'Kannada': 'ಶೀರ್ಷಿಕೆ', 'Hindi': 'शीर्षक', 'Tamil': 'தலைப்பு', 'Telugu': 'శీర్షిక'},
    'Today': {'Kannada': 'ಇಂದು', 'Hindi': 'आज', 'Tamil': 'இன்று', 'Telugu': 'నేడు'},
    'Total Events': {'Kannada': 'ಒಟ್ಟು ಈವೆಂಟ್‌ಗಳು', 'Hindi': 'कुल इवेंट', 'Tamil': 'மொத்த நிகழ்வுகள்', 'Telugu': 'మొత్తం ఈవెంట్‌లు'},
    'Try adjusting your search or filters': {'Kannada': 'ನಿಮ್ಮ ಹುಡುಕಾಟ ಅಥವಾ ಫಿಲ್ಟರ್‌ಗಳನ್ನು ಸರಿಹೊಂದಿಸಲು ಪ್ರಯತ್ನಿಸಿ', 'Hindi': 'अपनी खोज या फ़िल्टर समायोजित करने का प्रयास करें', 'Tamil': 'உங்கள் தேடல் அல்லது வடிப்பான்களை சரிசெய்ய முயற்சிக்கவும்', 'Telugu': 'మీ శోధన లేదా ఫిల్టర్‌లను సర్దుబాటు చేయడానికి ప్రయత్నించండి'},
    'Type': {'Kannada': 'ಪ್ರಕಾರ', 'Hindi': 'प्रकार', 'Tamil': 'வகை', 'Telugu': 'రకం'},
    'Useful': {'Kannada': 'ಉಪಯುಕ್ತ', 'Hindi': 'उपयोगी', 'Tamil': 'பயனுள்ள', 'Telugu': 'ఉపయోగకరం'},
    'View': {'Kannada': 'ವೀಕ್ಷಿಸಿ', 'Hindi': 'देखें', 'Tamil': 'காண்க', 'Telugu': 'వీక్షించండి'}
}

trans_file = r"e:\CrimeMatrix\frontend\src\context\translations.js"
with codecs.open(trans_file, "r", "utf-8") as f:
    t_content = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']
for lang in languages:
    new_entries = []
    for eng_key, trans_dict in translations.items():
        # Check if already present to avoid duplicates
        if f"'{eng_key.replace(chr(39), chr(92)+chr(39))}':" in t_content:
            continue
        val = eng_key if lang == 'English' else trans_dict[lang]
        eng_key_esc = eng_key.replace("'", "\\'")
        val_esc = val.replace("'", "\\'")
        new_entries.append(f"'{eng_key_esc}': '{val_esc}'")
    
    if new_entries:
        entries_str = ",\n    ".join(new_entries)
        
        if lang != 'Telugu':
            next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}[lang]
            pattern = f"\n  }},\n  {next_lang}:"
            t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }},\n  {next_lang}:")
        else:
            pattern = f"\n  }}\n}}"
            t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }}\n}}")

with codecs.open(trans_file, "w", "utf-8") as f:
    f.write(t_content)

print("Translations updated successfully.")

directories = [
    r"e:\CrimeMatrix\frontend\src\components\proactive",
    r"e:\CrimeMatrix\frontend\src\components\recommendations",
    r"e:\CrimeMatrix\frontend\src\components\reports",
    r"e:\CrimeMatrix\frontend\src\components\search"
]

files_to_process = [
    "ActivityFeed.jsx", "IntelligenceSummaryCards.jsx", "NotificationCenter.jsx", 
    "RecommendationsPanel.jsx", "ReportFilters.jsx", "ReportStats.jsx", 
    "ReportTable.jsx", "FilterChips.jsx", "caseData.js", "NaturalLanguageSearch.jsx", 
    "SavedSearches.jsx", "SearchBar.jsx", "SearchResults.jsx"
]

for d in directories:
    if not os.path.exists(d): continue
    for root, _, files in os.walk(d):
        for file in files:
            if file not in files_to_process: continue
            
            filepath = os.path.join(root, file)
            with codecs.open(filepath, "r", "utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Very special handling for caseData.js (just replace strings, no useLanguage)
            if file == 'caseData.js':
                for s in translations.keys():
                    content = content.replace(f"'{s}'", f"'{s}'") # We don't inject t() into mock data
                continue

            for s in translations.keys():
                # Fix specific long strings
                if s == 'Search naturally — e.g. "thefts in Bengaluru last month"':
                    # Need regex because the long string in NaturalLanguageSearch might have curly quotes or similar
                    content = re.sub(r'placeholder="Search naturally [^"]+"', rf'placeholder={{t(\'{s}\')}}', content)

                content = content.replace(f">{s}<", f">{{t('{s}')}}<")
                content = re.sub(rf'title="{s}"', rf"title={{t('{s}')}}", content)
                content = re.sub(rf'placeholder="{s}"', rf"placeholder={{t('{s}')}}", content)
                content = re.sub(rf'label="{s}"', rf"label={{t('{s}')}}", content)
                
                # Replace string in js arrays like `label: 'Search History'` -> `label: t('Search History')`
                content = re.sub(rf"label:\s*'{s}'", rf"label: t('{s}')", content)

            if content != original_content:
                if 'useLanguage' not in content:
                    imp = "import { useLanguage } from '../../context/LanguageContext'\n"
                    # Try to see if we need one more level of ../
                    if "import " in content:
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
