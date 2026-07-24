import os
import codecs
d = r'e:\CrimeMatrix\frontend\src\components'
files = ['InvestigationPage.jsx'] + [f'investigation/{f}' for f in os.listdir(d+'/investigation') if f.endswith('.jsx')]
for f in files:
    path = os.path.join(d, f)
    with codecs.open(path, 'r', 'utf-8') as file:
        content = file.read()
    
    # undo the specific bad ones
    bad_strings = [
        ") : filtered.length === 0 ? (",
        ") : (\r\n          notes.map((note) => (",
        ") : (\n          notes.map((note) => (",
        "if (line.startsWith('#### ')) return",
        "if (line.trim() === '') return",
        "return",
        ") : (\r\n          filtered.map((inv) => (",
        ") : (\n          filtered.map((inv) => (",
        "if (line.startsWith('### ')) return",
        "if (line.startsWith('- ')) return"
    ]
    for b in bad_strings:
        escaped_b = b.replace("'", "\\'")
        # Also try replacing newlines to match the text correctly
        content = content.replace(f"{{t('{escaped_b}')}}", b)
    
    with codecs.open(path, 'w', 'utf-8') as file:
        file.write(content)
print("Undone bad strings.")
