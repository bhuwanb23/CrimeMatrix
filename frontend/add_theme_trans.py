import codecs
import re

translations = {
    'light': {'Kannada': 'ಲೈಟ್', 'Hindi': 'लाइट', 'Tamil': 'லைட்', 'Telugu': 'లైట్'},
    'dark': {'Kannada': 'ಡಾರ್ಕ್', 'Hindi': 'डार्क', 'Tamil': 'டார்க்', 'Telugu': 'డార్క్'},
    'system': {'Kannada': 'ಸಿಸ್ಟಮ್', 'Hindi': 'सिस्टम', 'Tamil': 'சிஸ்டம்', 'Telugu': 'సిస్టమ్'}
}

trans_file = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(trans_file, 'r', 'utf-8') as f:
    t_content = f.read()

languages = ['English', 'Kannada', 'Hindi', 'Tamil', 'Telugu']
for lang in languages:
    new_entries = []
    for eng_key, trans_dict in translations.items():
        if f"'{eng_key}':" in t_content:
            continue
        val = eng_key.capitalize() if lang == 'English' else trans_dict[lang]
        new_entries.append(f"'{eng_key}': '{val}'")
    
    if new_entries:
        entries_str = ',\n    '.join(new_entries)
        
        if lang != 'Telugu':
            next_lang = {'English': 'Kannada', 'Kannada': 'Hindi', 'Hindi': 'Tamil', 'Tamil': 'Telugu'}[lang]
            pattern = f"\n  }},\n  {next_lang}:"
            t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }},\n  {next_lang}:")
        else:
            pattern = f"\n  }}\n}}"
            t_content = t_content.replace(pattern, f",\n    {entries_str}\n  }}\n}}")

with codecs.open(trans_file, 'w', 'utf-8') as f:
    f.write(t_content)

print('Translations added')
