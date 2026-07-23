import codecs
import re

translations = {
    'Physical Description': {'Kannada': 'ಭೌತಿಕ ವಿವರಣೆ', 'Hindi': 'शारीरिक विवरण', 'Tamil': 'உடல் விளக்கம்', 'Telugu': 'భౌతిక వివరణ'},
    'No suspect selected': {'Kannada': 'ಯಾವುದೇ ಶಂಕಿತನನ್ನು ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ', 'Hindi': 'कोई संदिग्ध चुना नहीं गया', 'Tamil': 'சந்தேக நபர் தேர்ந்தெடுக்கப்படவில்லை', 'Telugu': 'ఏ అనుమానితుడూ ఎంపిక కాలేదు'},
    'Behavioral Patterns': {'Kannada': 'ನಡವಳಿಕೆಯ ಮಾದರಿಗಳು', 'Hindi': 'व्यवहार पैटर्न', 'Tamil': 'நடத்தை முறைகள்', 'Telugu': 'ప్రవర్తనా విధానాలు'},
    'Suspect not found': {'Kannada': 'ಶಂಕಿತ ಕಂಡುಬಂದಿಲ್ಲ', 'Hindi': 'संदिग्ध नहीं मिला', 'Tamil': 'சந்தேக நபர் கிடைக்கவில்லை', 'Telugu': 'అనుమానితుడు దొరకలేదు'},
    'Score All Suspects': {'Kannada': 'ಎಲ್ಲಾ ಶಂಕಿತರನ್ನು ಸ್ಕೋರ್ ಮಾಡಿ', 'Hindi': 'सभी संदिग्धों को स्कोर करें', 'Tamil': 'அனைத்து சந்தேக நபர்களுக்கும் மதிப்பெண் கொடுங்கள்', 'Telugu': 'అనుమానితులందరికీ స్కోర్ చేయండి'},
    'Scoring...': {'Kannada': 'ಸ್ಕೋರಿಂಗ್...', 'Hindi': 'स्कोरिंग...', 'Tamil': 'மதிப்பெண் வழங்கப்படுகிறது...', 'Telugu': 'స్కోరింగ్...'},
    'No suspect found with ID:': {'Kannada': 'ಐಡಿಯೊಂದಿಗೆ ಯಾವುದೇ ಶಂಕಿತ ಕಂಡುಬಂದಿಲ್ಲ:', 'Hindi': 'इस आईडी के साथ कोई संदिग्ध नहीं मिला:', 'Tamil': 'இந்த ஐடியுடன் சந்தேக நபர் எவரும் கிடைக்கவில்லை:', 'Telugu': 'ఈ ఐడీతో అనుమానితుడు ఎవరూ దొరకలేదు:'},
    'Select a suspect to analyze': {'Kannada': 'ವಿಶ್ಲೇಷಿಸಲು ಶಂಕಿತನನ್ನು ಆಯ್ಕೆಮಾಡಿ', 'Hindi': 'विश्लेषण करने के लिए एक संदिग्ध का चयन करें', 'Tamil': 'பகுப்பாய்வு செய்ய சந்தேக நபரைத் தேர்ந்தெடுக்கவும்', 'Telugu': 'విశ్లేషించడానికి అనుమానితుడిని ఎంచుకోండి'},
    'Risk Analysis': {'Kannada': 'ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'जोखिम विश्लेषण', 'Tamil': 'ஆபத்து பகுப்பாய்வு', 'Telugu': 'ప్రమాద విశ్లేషణ'},
    'Personality Profile': {'Kannada': 'ವ್ಯಕ್ತಿತ್ವದ ವಿವರ', 'Hindi': 'व्यक्तित्व प्रोफ़ाइल', 'Tamil': 'ஆளுமை சுயவிவரம்', 'Telugu': 'వ్యక్తిత్వ ప్రొఫైల్'},
    'Associates': {'Kannada': 'ಸಹಚರರು', 'Hindi': 'सहयोगी', 'Tamil': 'சகாக்கள்', 'Telugu': 'సహచరులు'},
    'Risk Factors': {'Kannada': 'ಅಪಾಯದ ಅಂಶಗಳು', 'Hindi': 'जोखिम कारक', 'Tamil': 'ஆபத்து காரணிகள்', 'Telugu': 'ప్రమాద కారకాలు'},
    'Suspect Risk Scoring': {'Kannada': 'ಶಂಕಿತ ಅಪಾಯದ ಸ್ಕೋರಿಂಗ್', 'Hindi': 'संदिग्ध जोखिम स्कोरिंग', 'Tamil': 'சந்தேக நபர் ஆபத்து மதிப்பெண்', 'Telugu': 'అనుమానిత రిస్క్ స్కోరింగ్'},
    'MO Matches': {'Kannada': 'MO ಹೊಂದಾಣಿಕೆಗಳು', 'Hindi': 'MO मैच', 'Tamil': 'MO பொருத்தங்கள்', 'Telugu': 'MO మ్యాచ్‌లు'},
    'Risk': {'Kannada': 'ಅಪಾಯ', 'Hindi': 'जोखिम', 'Tamil': 'ஆபத்து', 'Telugu': 'ప్రమాదం'},
    'Click "Score All" to begin': {'Kannada': 'ಪ್ರಾರಂಭಿಸಲು "ಎಲ್ಲರಿಗೂ ಸ್ಕೋರ್ ಮಾಡಿ" ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'शुरू करने के लिए "सभी को स्कोर करें" पर क्लिक करें', 'Tamil': 'தொடங்க "அனைவருக்கும் மதிப்பெண் கொடுங்கள்" என்பதைக் கிளிக் செய்யவும்', 'Telugu': 'ప్రారంభించడానికి "అందరికీ స్కోర్ చేయి" క్లిక్ చేయండి'},
    'Cases': {'Kannada': 'ಪ್ರಕರಣಗಳು', 'Hindi': 'मामले', 'Tamil': 'வழக்குகள்', 'Telugu': 'కేసులు'},
    'Known Aliases': {'Kannada': 'ತಿಳಿದಿರುವ ಅಲಿಯಾಸ್ಗಳು', 'Hindi': 'ज्ञात उपनाम', 'Tamil': 'அறியப்பட்ட மாற்றுப்பெயர்கள்', 'Telugu': 'తెలిసిన మారుపేర్లు'},
    'Age': {'Kannada': 'ವಯಸ್ಸು', 'Hindi': 'आयु', 'Tamil': 'வயது', 'Telugu': 'వయస్సు'},
    'Risk Score': {'Kannada': 'ಅಪಾಯದ ಸ್ಕೋರ್', 'Hindi': 'जोखिम स्कोर', 'Tamil': 'ஆபத்து மதிப்பெண்', 'Telugu': 'రిస్క్ స్కోర్'},
    'Last Active': {'Kannada': 'ಕೊನೆಯದಾಗಿ ಸಕ್ರಿಯ', 'Hindi': 'अंतिम बार सक्रिय', 'Tamil': 'கடைசியாக செயலில்', 'Telugu': 'చివరిగా యాక్టివ్‌గా ఉంది'},
    'Criminal Summary': {'Kannada': 'ಅಪರಾಧ ಸಾರಾಂಶ', 'Hindi': 'आपराधिक सारांश', 'Tamil': 'குற்றச் சுருக்கம்', 'Telugu': 'క్రిమినల్ సారాంశం'},
    'MO Match Score': {'Kannada': 'MO ಹೊಂದಾಣಿಕೆ ಸ್ಕೋರ್', 'Hindi': 'MO मैच स्कोर', 'Tamil': 'MO போட்டி மதிப்பெண்', 'Telugu': 'MO మ్యాచ్ స్కోర్'},
    'Network Summary': {'Kannada': 'ನೆಟ್ವರ್ಕ್ ಸಾರಾಂಶ', 'Hindi': 'नेटवर्क सारांश', 'Tamil': 'நெட்வொர்க் சுருக்கம்', 'Telugu': 'నెట్‌వర్క్ సారాంశం'},
    'Address': {'Kannada': 'ವಿಳಾಸ', 'Hindi': 'पता', 'Tamil': 'முகவரி', 'Telugu': 'చిరునామా'},
    'Contributing Factors': {'Kannada': 'ಕೊಡುಗೆ ಅಂಶಗಳು', 'Hindi': 'योगदान कारक', 'Tamil': 'பங்களிக்கும் காரணிகள்', 'Telugu': 'సహకరించే కారకాలు'},
    'Transparent, evidence-backed risk assessment engine': {'Kannada': 'ಪಾರದರ್ಶಕ, ಪುರಾವೆ-ಬೆಂಬಲಿತ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ ಎಂಜಿನ್', 'Hindi': 'पारदर्शी, साक्ष्य-समर्थित जोखिम मूल्यांकन इंजन', 'Tamil': 'வெளிப்படையான, சான்று அடிப்படையிலான இடர் மதிப்பீட்டு இயந்திரம்', 'Telugu': 'పారదర్శక, సాక్ష్యం-ఆధారిత రిస్క్ అసెస్‌మెంట్ ఇంజిన్'},
    'Modus Operandi Fingerprint': {'Kannada': 'ಮೊಡಸ್ ಆಪರೇಂಡಿ ಫಿಂಗರ್‌ಪ್ರಿಂಟ್', 'Hindi': 'मोडस ऑपरेंडी फिंगरप्रिंट', 'Tamil': 'மோடஸ் ஆப்பரெண்டி கைரேகை', 'Telugu': 'మోడస్ ఆపరేండి వేలిముద్ర'},
    'suspect': {'Kannada': 'ಶಂಕಿತ', 'Hindi': 'संदिग्ध', 'Tamil': 'சந்தேக நபர்', 'Telugu': 'అనుమానితుడు'},
    'No suspects scored yet': {'Kannada': 'ಇನ್ನೂ ಯಾವುದೇ ಶಂಕಿತರನ್ನು ಸ್ಕೋರ್ ಮಾಡಿಲ್ಲ', 'Hindi': 'अभी तक किसी संदिग्ध को स्कोर नहीं किया गया है', 'Tamil': 'இதுவரை எந்த சந்தேக நபருக்கும் மதிப்பெண் வழங்கப்படவில்லை', 'Telugu': 'ఇంకా ఏ అనుమానితులకూ స్కోర్ చేయలేదు'},
    'Full Name': {'Kannada': 'ಪೂರ್ಣ ಹೆಸರು', 'Hindi': 'पूरा नाम', 'Tamil': 'முழு பெயர்', 'Telugu': 'పూర్తి పేరు'},
    'Back to Suspects': {'Kannada': 'ಶಂಕಿತರಿಗೆ ಹಿಂತಿರುಗಿ', 'Hindi': 'संदिग्धों पर वापस जाएं', 'Tamil': 'சந்தேக நபர்களுக்குத் திரும்பு', 'Telugu': 'అనుమానితులకు తిరిగి వెళ్ళు'},
    'years': {'Kannada': 'ವರ್ಷಗಳು', 'Hindi': 'साल', 'Tamil': 'ஆண்டுகள்', 'Telugu': 'సంవత్సరాలు'},
    'Personal Information': {'Kannada': 'ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ', 'Hindi': 'व्यक्तिगत जानकारी', 'Tamil': 'தனிப்பட்ட தகவல்', 'Telugu': 'వ్యక్తిగత సమాచారం'},
    'Phone': {'Kannada': 'ದೂರವಾಣಿ', 'Hindi': 'फ़ोन', 'Tamil': 'தொலைபேசி', 'Telugu': 'ఫోన్'},
    ' ': {'Kannada': ' ', 'Hindi': ' ', 'Tamil': ' ', 'Telugu': ' '},
    'Click on a suspect from the rankings to view their detailed risk analysis': {'Kannada': 'ಅವರ ವಿವರವಾದ ಅಪಾಯ ವಿಶ್ಲೇಷಣೆಯನ್ನು ವೀಕ್ಷಿಸಲು ಶ್ರೇಯಾಂಕಗಳಿಂದ ಶಂಕಿತನ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ', 'Hindi': 'उनके विस्तृत जोखिम विश्लेषण को देखने के लिए रैंकिंग से एक संदिग्ध पर क्लिक करें', 'Tamil': 'அவர்களின் விரிவான ஆபத்து பகுப்பாய்வைக் காண தரவரிசையிலிருந்து சந்தேக நபர் மீது கிளிக் செய்யவும்', 'Telugu': 'వారి వివరణాత్మక రిస్క్ విశ్లేషణను వీక్షించడానికి ర్యాంకింగ్స్ నుండి అనుమానితుడిపై క్లిక్ చేయండి'},
    'Analyzing': {'Kannada': 'ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ', 'Hindi': 'विश्लेषण कर रहा है', 'Tamil': 'பகுப்பாய்வு செய்யப்படுகிறது', 'Telugu': 'విశ్లేషిస్తోంది'},
    'Suspect Rankings': {'Kannada': 'ಶಂಕಿತ ಶ್ರೇಯಾಂಕಗಳು', 'Hindi': 'संदिग्ध रैंकिंग', 'Tamil': 'சந்தேக நபர் தரவரிசை', 'Telugu': 'అనుమానిత ర్యాంకింగ్స్'},
    'District': {'Kannada': 'ಜಿಲ್ಲೆ', 'Hindi': 'ज़िला', 'Tamil': 'மாவட்டம்', 'Telugu': 'జిల్లా'},
    'Total Scored': {'Kannada': 'ಒಟ್ಟು ಸ್ಕೋರ್ ಮಾಡಲಾಗಿದೆ', 'Hindi': 'कुल स्कोर किया गया', 'Tamil': 'மொத்தம் மதிப்பெண் வழங்கப்பட்டது', 'Telugu': 'మొత్తం స్కోర్ చేయబడింది'},
    'Critical Risk': {'Kannada': 'ನಿರ್ಣಾಯಕ ಅಪಾಯ', 'Hindi': 'गंभीर जोखिम', 'Tamil': 'மிக அதிக ஆபத்து', 'Telugu': 'క్లిష్టమైన ప్రమాదం'},
    'High Risk': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯ', 'Hindi': 'उच्च जोखिम', 'Tamil': 'அதிக ஆபத்து', 'Telugu': 'అధిక ప్రమాదం'},
    'Average Score': {'Kannada': 'ಸರಾಸರಿ ಸ್ಕೋರ್', 'Hindi': 'औसत स्कोर', 'Tamil': 'சராசரி மதிப்பெண்', 'Telugu': 'సగటు స్కోర్'},
    'analyzed': {'Kannada': 'ವಿಶ್ಲೇಷಿಸಲಾಗಿದೆ', 'Hindi': 'विश्लेषण किया गया', 'Tamil': 'பகுப்பாய்வு செய்யப்பட்டது', 'Telugu': 'విశ్లేషించబడింది'},
    'Criminal History': {'Kannada': 'ಅಪರಾಧ ಇತಿಹಾಸ', 'Hindi': 'आपराधिक इतिहास', 'Tamil': 'குற்ற வரலாறு', 'Telugu': 'నేర చరిత్ర'},
    'Prior offense records': {'Kannada': 'ಹಿಂದಿನ ಅಪರಾಧ ದಾಖಲೆಗಳು', 'Hindi': 'पूर्व अपराध रिकॉर्ड', 'Tamil': 'முந்தைய குற்றப் பதிவுகள்', 'Telugu': 'మునుపటి నేర రికార్డులు'},
    'Offense Severity': {'Kannada': 'ಅಪರಾಧ ತೀವ್ರತೆ', 'Hindi': 'अपराध की गंभीरता', 'Tamil': 'குற்றத்தின் தீவிரம்', 'Telugu': 'నేర తీవ్రత'},
    'Severity of past crimes': {'Kannada': 'ಹಿಂದಿನ ಅಪರಾಧಗಳ ತೀವ್ರತೆ', 'Hindi': 'पिछले अपराधों की गंभीरता', 'Tamil': 'கடந்த கால குற்றங்களின் தீவிரம்', 'Telugu': 'గత నేరాల తీవ్రత'},
    'Age Factor': {'Kannada': 'ವಯಸ್ಸಿನ ಅಂಶ', 'Hindi': 'आयु कारक', 'Tamil': 'வயது காரணி', 'Telugu': 'వయస్సు కారకం'},
    'Age-related risk assessment': {'Kannada': 'ವಯಸ್ಸಿಗೆ ಸಂಬಂಧಿಸಿದ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ', 'Hindi': 'आयु-संबंधित जोखिम मूल्यांकन', 'Tamil': 'வயது தொடர்பான இடர் மதிப்பீடு', 'Telugu': 'వయస్సు-సంబంధిత ప్రమాద అంచనా'},
    'Location Risk': {'Kannada': 'ಸ್ಥಳ ಅಪಾಯ', 'Hindi': 'स्थान जोखिम', 'Tamil': 'இட ஆபத்து', 'Telugu': 'స్థాన ప్రమాదం'},
    'High-risk area indicators': {'Kannada': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ಪ್ರದೇಶದ ಸೂಚಕಗಳು', 'Hindi': 'उच्च जोखिम वाले क्षेत्र के संकेतक', 'Tamil': 'அதிக ஆபத்துள்ள பகுதி குறிகாட்டிகள்', 'Telugu': 'అధిక-ప్రమాద ప్రాంత సూచికలు'},
    'Associate Risk': {'Kannada': 'ಸಹಚರ ಅಪಾಯ', 'Hindi': 'सहयोगी जोखिम', 'Tamil': 'சகாக்கள் ஆபத்து', 'Telugu': 'సహచర ప్రమాదం'},
    'Known criminal associates': {'Kannada': 'ತಿಳಿದಿರುವ ಅಪರಾಧಿ ಸಹಚರರು', 'Hindi': 'ज्ञात आपराधिक सहयोगी', 'Tamil': 'அறியப்பட்ட குற்றவியல் சகாக்கள்', 'Telugu': 'తెలిసిన నేర సహచరులు'},
    'Recency': {'Kannada': 'ಇತ್ತೀಚಿನದು', 'Hindi': 'नवीनता', 'Tamil': 'சமீபத்தியது', 'Telugu': 'ఇటీవలిది'},
    'Time since last offense': {'Kannada': 'ಕೊನೆಯ ಅಪರಾಧದ ನಂತರದ ಸಮಯ', 'Hindi': 'अंतिम अपराध के बाद का समय', 'Tamil': 'கடைசி குற்றத்திலிருந்து நேரம்', 'Telugu': 'చివరి నేరం జరిగినప్పటి నుండి సమయం'},
    'Network Influence': {'Kannada': 'ನೆಟ್ವರ್ಕ್ ಪ್ರಭಾವ', 'Hindi': 'नेटवर्क प्रभाव', 'Tamil': 'நெட்வொர்க் செல்வாக்கு', 'Telugu': 'నెట్‌వర్క్ ప్రభావం'},
    'Criminal network connections': {'Kannada': 'ಕ್ರಿಮಿನಲ್ ನೆಟ್ವರ್ಕ್ ಸಂಪರ್ಕಗಳು', 'Hindi': 'आपराधिक नेटवर्क कनेक्शन', 'Tamil': 'குற்றவியல் நெட்வொர்க் இணைப்புகள்', 'Telugu': 'క్రిమినల్ నెట్‌వర్క్ కనెక్షన్‌లు'},
    'MO Similarity': {'Kannada': 'MO ಹೋಲಿಕೆ', 'Hindi': 'MO समानता', 'Tamil': 'MO ஒற்றுமை', 'Telugu': 'MO సారూప్యత'},
    'Modus operandi pattern match': {'Kannada': 'ಮೊಡಸ್ ಆಪರೇಂಡಿ ಮಾದರಿ ಹೊಂದಾಣಿಕೆ', 'Hindi': 'मोडस ऑपरेंडी पैटर्न मैच', 'Tamil': 'மோடஸ் ஆப்பரெண்டி முறை பொருத்தம்', 'Telugu': 'మోడస్ ఆపరేండి ప్యాటర్న్ మ్యాచ్'},
    'Investigation Links': {'Kannada': 'ತನಿಖೆ ಸಂಪರ್ಕಗಳು', 'Hindi': 'जांच लिंक', 'Tamil': 'விசாரணை இணைப்புகள்', 'Telugu': 'దర్యాప్తు లింకులు'},
    'Active investigation connections': {'Kannada': 'ಸಕ್ರಿಯ ತನಿಖೆ ಸಂಪರ್ಕಗಳು', 'Hindi': 'सक्रिय जांच कनेक्शन', 'Tamil': 'செயலில் உள்ள விசாரணை இணைப்புகள்', 'Telugu': 'క్రియాశీల దర్యాప్తు కనెక్షన్‌లు'},
    'Behavioral': {'Kannada': 'ನಡವಳಿಕೆಯ', 'Hindi': 'व्यवहारिक', 'Tamil': 'நடத்தை', 'Telugu': 'ప్రవర్తనా'},
    'Behavioral profile analysis': {'Kannada': 'ನಡವಳಿಕೆಯ ವಿವರ ವಿಶ್ಲೇಷಣೆ', 'Hindi': 'व्यवहार प्रोफ़ाइल विश्लेषण', 'Tamil': 'நடத்தை சுயவிவர பகுப்பாய்வு', 'Telugu': 'ప్రవర్తనా ప్రొఫైల్ విశ్లేషణ'},
    'Profile': {'Kannada': 'ಪ್ರೊಫೈಲ್', 'Hindi': 'प्रोफ़ाइल', 'Tamil': 'சுயவிவரம்', 'Telugu': 'ప్రొఫైల్'},
    'MO': {'Kannada': 'MO', 'Hindi': 'MO', 'Tamil': 'MO', 'Telugu': 'MO'},
    'Timeline': {'Kannada': 'ಟೈಮ್‌ಲೈನ್', 'Hindi': 'समयरेखा', 'Tamil': 'காலவரிசை', 'Telugu': 'కాలక్రమం'},
    'Wanted': {'Kannada': 'ಬೇಕಾಗಿದ್ದಾರೆ', 'Hindi': 'वांछित', 'Tamil': 'தேடப்படுபவர்', 'Telugu': 'వాంటెడ్'},
    'Arrested': {'Kannada': 'ಬಂಧಿತ', 'Hindi': 'गिरफ्तार', 'Tamil': 'கைது செய்யப்பட்டவர்', 'Telugu': 'అరెస్టయ్యాడు'},
    'Absconding': {'Kannada': 'ತಲೆಮರೆಸಿಕೊಂಡಿದ್ದಾರೆ', 'Hindi': 'फरार', 'Tamil': 'தலைமறைவானவர்', 'Telugu': 'పరారీలో ఉన్నాడు'},
    'Active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకుగా'},
    'very_high': {'Kannada': 'ಅತ್ಯಂತ ಹೆಚ್ಚು', 'Hindi': 'बहुत अधिक', 'Tamil': 'மிகவும் அதிகம்', 'Telugu': 'చాలా ఎక్కువ'},
    'high': {'Kannada': 'ಹೆಚ್ಚು', 'Hindi': 'उच्च', 'Tamil': 'அதிகம்', 'Telugu': 'ఎక్కువ'},
    'medium': {'Kannada': 'ಮಧ್ಯಮ', 'Hindi': 'मध्यम', 'Tamil': 'நடுத்தரம்', 'Telugu': 'మధ్యస్థం'},
    'low': {'Kannada': 'ಕಡಿಮೆ', 'Hindi': 'निम्न', 'Tamil': 'குறைவு', 'Telugu': 'తక్కువ'}
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
print("Updated translations.js with all Suspect component strings successfully.")
