import codecs
import re

file_path = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(file_path, 'r', 'utf-8') as f:
    text = f.read()

# Fix the broken quote
text = text.replace("'results found,'", "'results found'")

# Now fix the missing commas correctly for all languages
# Just find all occurrences of a string closing quote followed by newlines and a new key without a comma
text = re.sub(r"('[^']*'|\"[^\"]*\")(\s*\r?\n\s*)(['\"]Reports & Documentation['\"]\:)", r"\1,\2\3", text)

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(text)
print("Fixed commas.")
