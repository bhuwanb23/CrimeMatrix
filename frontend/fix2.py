import codecs
import re

file_path = r'e:\CrimeMatrix\frontend\src\context\translations.js'
with codecs.open(file_path, 'r', 'utf-8') as f:
    text = f.read()

# For any quote not followed by a comma, followed by whitespace and 'Report ID', insert a comma.
text = re.sub(r"('[^']*'|\"[^\"]*\")(\s*\r?\n\s*)(['\"]Report ID['\"]\:)", r"\1,\2\3", text)

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(text)
print("Fixed missing commas before Report ID.")
