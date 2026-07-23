import codecs

path = r'e:\CrimeMatrix\frontend\src\components\SuspectDetailPage.jsx'
with codecs.open(path, 'r', 'utf-8') as f:
    text = f.read()

text = text.replace('{suspect.status}', '{t(suspect.status)}')
text = text.replace('{suspect.age} years • {suspect.district} • ID: {suspect.id}', "{suspect.age} {t('years')} • {t(suspect.district)} • ID: {suspect.id}")
text = text.replace('{tab.label}', '{t(tab.label)}')
text = text.replace('No suspect found with ID: {id}', "{t('No suspect found with ID:')} {id}")

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(text)


path2 = r'e:\CrimeMatrix\frontend\src\components\SuspectRiskPage.jsx'
with codecs.open(path2, 'r', 'utf-8') as f:
    text2 = f.read()

text2 = text2.replace("{scoring ? 'Scoring...' : 'Score All Suspects'}", "{scoring ? t('Scoring...') : t('Score All Suspects')}")
text2 = text2.replace('<span className="text-xs text-slate-400 font-medium">{card.label}</span>', '<span className="text-xs text-slate-400 font-medium">{t(card.label)}</span>')
text2 = text2.replace('{selectedScore ? `Analyzing ${rankings.find(r => r.suspect_id === selectedSuspect)?.name || \'suspect\'}` : \'Select a suspect to analyze\'}', "{selectedScore ? `${t('Analyzing')} ${rankings.find(r => r.suspect_id === selectedSuspect)?.name || t('suspect')}` : t('Select a suspect to analyze')}")
text2 = text2.replace('<span className="text-[9px] font-bold uppercase tracking-wider opacity-80">{selectedScore.risk_level}</span>', '<span className="text-[9px] font-bold uppercase tracking-wider opacity-80">{t(selectedScore.risk_level)}</span>')
text2 = text2.replace('<span>{exp}</span>', '<span>{t(exp)}</span>')
text2 = text2.replace('<span className="text-xs font-medium text-slate-600">{factor.label}</span>', '<span className="text-xs font-medium text-slate-600">{t(factor.label)}</span>')
text2 = text2.replace('<span className="text-[10px] text-slate-400 mt-0.5 block">{factor.desc}</span>', '<span className="text-[10px] text-slate-400 mt-0.5 block">{t(factor.desc)}</span>')
text2 = text2.replace('<span className="block text-[10px] font-semibold uppercase" style={{ color }}>{r.risk_level}</span>', '<span className="block text-[10px] font-semibold uppercase" style={{ color }}>{t(r.risk_level)}</span>')

with codecs.open(path2, 'w', 'utf-8') as f:
    f.write(text2)

print("Fixed variables in SuspectRiskPage and SuspectDetailPage")
