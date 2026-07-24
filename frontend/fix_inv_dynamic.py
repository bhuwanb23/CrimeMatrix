import codecs

path = r'e:\CrimeMatrix\frontend\src\components\InvestigationPage.jsx'
with codecs.open(path, 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('<span>{investigations.length} investigations</span>', '<span>{investigations.length} {t(\'investigations\')}</span>')
text = text.replace('Viewing #{selectedId}', '{t(\'Viewing\')} #{selectedId}')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(text)
print("Fixed dynamic text in InvestigationPage")
