import os
import re

directories = [
    r"e:\CrimeMatrix\frontend\src\components\proactive",
    r"e:\CrimeMatrix\frontend\src\components\recommendations",
    r"e:\CrimeMatrix\frontend\src\components\reports",
    r"e:\CrimeMatrix\frontend\src\components\search"
]

strings = set()

for d in directories:
    if not os.path.exists(d): continue
    for file in os.listdir(d):
        if file.endswith(".jsx") or file.endswith(".js"):
            with open(os.path.join(d, file), 'r', encoding='utf-8') as f:
                content = f.read()
                # Exclude caseData.js from AST extraction if it's just raw data
                if file == 'caseData.js':
                    # Maybe extract 'status', 'priority' etc if they are string literals
                    matches = re.findall(r"[\"'](High|Medium|Low|Critical|Open|Closed|Active|Resolved)[\"']", content)
                    for m in matches: strings.add(m)
                    continue

                # Match >Text<
                matches = re.findall(r'>([^<>{]+?)<', content)
                for m in matches:
                    m = m.strip()
                    if m and not m.startswith('import') and not m.startswith('export'):
                        strings.add(m)
                
                # Match title="Text", placeholder="Text", label="Text"
                matches2 = re.findall(r'(?:title|placeholder|label)="([^"]+?)"', content)
                for m in matches2:
                    strings.add(m.strip())
                    
                # Match label: 'Text' inside objects
                matches3 = re.findall(r'label:\s*[\'"]([^\'"]+)[\'"]', content)
                for m in matches3:
                    strings.add(m.strip())
                
                # Also check common things like 'Generating...' or 'Loading...'
                matches4 = re.findall(r"[\"']([^\"']*(?:ing\.\.\.|Error|Found|Results|Saved)[\"'])", content)
                for m in matches4:
                    if len(m) < 40 and "{" not in m:
                        strings.add(m.strip("'\""))

print("Found Strings:")
for s in sorted(strings):
    print(s)
