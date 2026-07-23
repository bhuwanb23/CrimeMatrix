import codecs
import re

translations = {
    'Type': {'Kannada': 'ಪ್ರಕಾರ', 'Hindi': 'प्रकार', 'Tamil': 'வகை', 'Telugu': 'రకం'},
    'Accuracy:': {'Kannada': 'ನಿಖರತೆ:', 'Hindi': 'सटीकता:', 'Tamil': 'துல்லியம்:', 'Telugu': 'ఖచ్చితత్వం:'},
    'Overall confidence:': {'Kannada': 'ಒಟ್ಟಾರೆ ವಿಶ್ವಾಸ:', 'Hindi': 'समग्र विश्वास:', 'Tamil': 'ஒட்டுமொத்த நம்பிக்கை:', 'Telugu': 'మొత్తం విశ్వాసం:'},
    'High reliability': {'Kannada': 'ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸಾರ್ಹತೆ', 'Hindi': 'उच्च विश्वसनीयता', 'Tamil': 'அதிக நம்பகத்தன்மை', 'Telugu': 'అధిక విశ్వసనీయత'},
    'Moderate reliability': {'Kannada': 'ಮಧ್ಯಮ ವಿಶ್ವಾಸಾರ್ಹತೆ', 'Hindi': 'मध्यम विश्वसनीयता', 'Tamil': 'மிதமான நம்பகத்தன்மை', 'Telugu': 'మితమైన విశ్వసనీయత'},
    'Low reliability': {'Kannada': 'ಕಡಿಮೆ ವಿಶ್ವಾಸಾರ್ಹತೆ', 'Hindi': 'कम विश्वसनीयता', 'Tamil': 'குறைந்த நம்பகத்தன்மை', 'Telugu': 'తక్కువ విశ్వసనీయత'},
    'stable': {'Kannada': 'ಸ್ಥಿರ', 'Hindi': 'स्थिर', 'Tamil': 'நிலையான', 'Telugu': 'స్థిరమైన'},
    'increasing': {'Kannada': 'ಹೆಚ್ಚಾಗುತ್ತಿದೆ', 'Hindi': 'बढ़ रही है', 'Tamil': 'அதிகரித்து வருகிறது', 'Telugu': 'పెరుగుతున్నది'},
    'decreasing': {'Kannada': 'ಕಡಿಮೆಯಾಗುತ್ತಿದೆ', 'Hindi': 'घट रही है', 'Tamil': 'குறைந்து வருகிறது', 'Telugu': 'తగ్గుతున్నది'},
    'Data points:': {'Kannada': 'ಡೇಟಾ ಪಾಯಿಂಟ್ಸ್:', 'Hindi': 'डेटा बिंदु:', 'Tamil': 'தரவு புள்ளிகள்:', 'Telugu': 'డేటా పాయింట్లు:'},
    'active': {'Kannada': 'ಸಕ್ರಿಯ', 'Hindi': 'सक्रिय', 'Tamil': 'செயலில்', 'Telugu': 'చురుకుగా'},
    'Bengaluru Urban': {'Kannada': 'ಬೆಂಗಳೂರು ನಗರ', 'Hindi': 'बेंगलुरु शहरी', 'Tamil': 'பெங்களூரு நகர்ப்புறம்', 'Telugu': 'బెంగళూరు అర్బన్'},
    'Bengaluru Rural': {'Kannada': 'ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ', 'Hindi': 'बेंगलुरु ग्रामीण', 'Tamil': 'பெங்களூரு ஊரகம்', 'Telugu': 'బెంగళూరు రూరల్'},
    'Mysuru': {'Kannada': 'ಮೈಸೂರು', 'Hindi': 'मैसूरु', 'Tamil': 'மைசூரு', 'Telugu': 'మైసూరు'},
    'Mangaluru': {'Kannada': 'ಮಂಗಳೂರು', 'Hindi': 'मंगलुरु', 'Tamil': 'மங்களூரு', 'Telugu': 'మంగళూరు'},
    'Hubballi-Dharwad': {'Kannada': 'ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ', 'Hindi': 'हुबली-धारवाड़', 'Tamil': 'ஹுப்பள்ளி-தார்வாட்', 'Telugu': 'హుబ్బళ్లి-ధార్వాడ్'},
    'Kalaburagi': {'Kannada': 'ಕಲಬುರಗಿ', 'Hindi': 'कलबुर्गी', 'Tamil': 'கலபுர்கி', 'Telugu': 'కలబురగి'},
    'Ballari': {'Kannada': 'ಬಳ್ಳಾರಿ', 'Hindi': 'बल्लारी', 'Tamil': 'பல்லாரி', 'Telugu': 'బళ్లారి'},
    'Vijayapura': {'Kannada': 'ವಿಜಯಪುರ', 'Hindi': 'विजयपुरा', 'Tamil': 'விஜயபுரா', 'Telugu': 'విజయపుర'},
    'Shivamogga': {'Kannada': 'ಶಿವಮೊಗ್ಗ', 'Hindi': 'शिवमोग्गा', 'Tamil': 'சிவமொக்கா', 'Telugu': 'శివమొగ్గ'},
    'Davangere': {'Kannada': 'ದಾವಣಗೆರೆ', 'Hindi': 'दावणगेरे', 'Tamil': 'தாவணகெரே', 'Telugu': 'దావణగెరె'},
    'Hassan': {'Kannada': 'ಹಾಸನ', 'Hindi': 'हासन', 'Tamil': 'ஹாசன்', 'Telugu': 'హాసన్'},
    'Mandya': {'Kannada': 'ಮಂಡ್ಯ', 'Hindi': 'मांड्या', 'Tamil': 'மாண்டியா', 'Telugu': 'మాండ్య'},
    'Tumakuru': {'Kannada': 'ತುಮಕೂರು', 'Hindi': 'तुमकुरु', 'Tamil': 'துமகூரு', 'Telugu': 'తుమకూరు'},
    'Kolar': {'Kannada': 'ಕೋಲಾರ', 'Hindi': 'कोलार', 'Tamil': 'கோலார்', 'Telugu': 'కోలార్'},
    'Chikkaballapur': {'Kannada': 'ಚಿಕ್ಕಬಳ್ಳಾಪುರ', 'Hindi': 'चिक्कबल्लापुर', 'Tamil': 'சிக்கபல்லாபூர்', 'Telugu': 'చిక్కబల్లాపూర్'},
    'Ramanagara': {'Kannada': 'ರಾಮನಗರ', 'Hindi': 'रामनगर', 'Tamil': 'ராமநகர', 'Telugu': 'రామనగర'},
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
print("Updated translations.js with all AI Predictions component strings successfully.")
