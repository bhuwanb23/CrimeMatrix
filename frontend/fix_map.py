import codecs

def process_file(path, replacements):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
    
    for old, new in replacements:
        text = text.replace(old, new)
        
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)

process_file(r'e:\CrimeMatrix\frontend\src\components\MapPage.jsx', [
    ('import { useState, useEffect, useCallback } from \'react\'', 'import { useState, useEffect, useCallback } from \'react\'\nimport { useLanguage } from \'../context/LanguageContext\''),
    ('export default function MapPage() {', 'export default function MapPage() {\n  const { t } = useLanguage()'),
    ('Geo Intelligence', '{t(\'Geo Intelligence\')}'),
    ('{t(\'Geo Intelligence\')} from', 'Geo Intelligence from'),
    ('Stations, spatial analysis & crime mapping', '{t(\'Stations, spatial analysis & crime mapping\')}'),
    ('Refresh\n          </button>', '{t(\'Refresh\')}\n          </button>'),
    ('>{item.label}<', '>{t(item.label)}<')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapLayerControls.jsx', [
    ('import { Layers } from \'lucide-react\'', 'import { Layers } from \'lucide-react\'\nimport { useLanguage } from \'../../context/LanguageContext\''),
    ('export default function MapLayerControls({ activeLayers, onToggleLayer }) {', 'export default function MapLayerControls({ activeLayers, onToggleLayer }) {\n  const { t } = useLanguage()'),
    ('{l.label}', '{t(l.label)}')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapTimeSlider.jsx', [
    ('import { Clock } from \'lucide-react\'', 'import { Clock } from \'lucide-react\'\nimport { useLanguage } from \'../../context/LanguageContext\''),
    ('export default function MapTimeSlider({ days, onChange }) {', 'export default function MapTimeSlider({ days, onChange }) {\n  const { t } = useLanguage()'),
    ('{opt.label}', '{t(opt.label)}')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapFilterPanel.jsx', [
    ('import { Filter } from \'lucide-react\'', 'import { Filter } from \'lucide-react\'\nimport { useLanguage } from \'../../context/LanguageContext\''),
    ('export default function MapFilterPanel({ filters, onChange }) {', 'export default function MapFilterPanel({ filters, onChange }) {\n  const { t } = useLanguage()'),
    ('{type.label}', '{t(type.label)}'),
    ('{level.label}', '{t(level.label)}')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\DistrictPanel.jsx', [
    ('import { hotspots, crimeDensity } from \'./mapData\'', 'import { hotspots, crimeDensity } from \'./mapData\'\nimport { useLanguage } from \'../../context/LanguageContext\''),
    ('export default function DistrictPanel({ selectedDistrict, onClose }) {', 'export default function DistrictPanel({ selectedDistrict, onClose }) {\n  const { t } = useLanguage()'),
    ('\'Overview\'', 't(\'Overview\')'),
    ('Selected district', '{t(\'Selected district\')}'),
    ('Total cases', '{t(\'Total cases\')}'),
    ('>Hotspots<', '>{t(\'Hotspots\')}<'),
    ('Risk', '{t(\'Risk\')}'),
    ('Density', '{t(\'Density\')}'),
    ('cases</span>', '{t(\'cases\')}</span>'),
    ('{selectedDistrict.risk || selectedDistrict.risk_level || \'\'}', '{t(selectedDistrict.risk || selectedDistrict.risk_level || \'low\')}'),
    ('{d.label}', '{t(d.label)}'),
    ('Select a district on the map', '{t(\'Select a district on the map\')}')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\map\MapCanvas.jsx', [
    ('import { karnatakaOutline } from \'./mapData\'', 'import { karnatakaOutline } from \'./mapData\'\nimport { useLanguage } from \'../../context/LanguageContext\''),
    ('export default function MapCanvas({ selectedDistrict, onDistrictSelect, activeLayers, mapData, loading }) {', 'export default function MapCanvas({ selectedDistrict, onDistrictSelect, activeLayers, mapData, loading }) {\n  const { t } = useLanguage()'),
    ('>Open<', '>{t(\'Open\')}<'),
    ('>Closed<', '>{t(\'Closed\')}<'),
    ('>Pending<', '>{t(\'Pending\')}<'),
    ('>Station<', '>{t(\'Station\')}<'),
    ('<span>{crime.type}</span>', '<span>{t(crime.type)}</span>')
])
