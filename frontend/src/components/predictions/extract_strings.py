import os
import re

directory = r"e:\CrimeMatrix\frontend\src\components\predictions"

files = os.listdir(directory)
strings = set()

for file in files:
    if file.endswith(".jsx"):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            content = f.read()
            # Match <h3>Text</h3>, <p>Text</p>, <span>Text</span>
            matches = re.findall(r'>([^<>{]+?)<', content)
            for m in matches:
                m = m.strip()
                if m and not m.startswith('import') and not m.startswith('export'):
                    strings.add(m)
            
            # Match title="Text", placeholder="Text"
            matches2 = re.findall(r'(?:title|placeholder|label)="([^"]+?)"', content)
            for m in matches2:
                strings.add(m.strip())
                
            # Match label: 'Text' inside objects
            matches3 = re.findall(r'label:\s*[\'"]([^\'"]+)[\'"]', content)
            for m in matches3:
                strings.add(m.strip())

print("Found Strings:")
for s in sorted(strings):
    print(s)
