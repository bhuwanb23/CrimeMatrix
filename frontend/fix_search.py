import codecs

def process_file(path, replacements):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
    
    for old, new in replacements:
        text = text.replace(old, new)
        
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)

process_file(r'e:\CrimeMatrix\frontend\src\components\search\FilterChips.jsx', [
    ('{f.label}', '{t(f.label)}'),
    ('Clear all', "{t('Clear all')}")
])

process_file(r'e:\CrimeMatrix\frontend\src\components\search\SavedSearches.jsx', [
    ('Saved Searches', "{t('Saved Searches')}"),
    ('Save current', "{t('Save current')}"),
    ('No saved searches', "{t('No saved searches')}"),
    ('<span className="tooltip">Run search</span>', '<span className="tooltip">{t(\'Run search\')}</span>'),
    ('<span className="tooltip">Delete</span>', '<span className="tooltip">{t(\'Delete\')}</span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\search\SearchBar.jsx', [
    ('placeholder="Search crimes, suspects, FIRs, evidence..."', 'placeholder={t("Search crimes, suspects, FIRs, evidence...")}'),
    ('Press <kbd>Enter</kbd> to search', "Press <kbd>Enter</kbd> {t('to search')}"),
    ('Recent Searches', "{t('Recent Searches')}"),
    ('Suggestions', "{t('Suggestions')}"),
    ('<span className="tooltip">Clear search</span>', '<span className="tooltip">{t(\'Clear search\')}</span>'),
    ('<span className="tooltip">Save search</span>', '<span className="tooltip">{t(\'Save search\')}</span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\search\SearchHistory.jsx', [
    ('import { Clock, Play } from \'lucide-react\'', "import { Clock, Play } from 'lucide-react'\nimport { useLanguage } from '../../context/LanguageContext'"),
    ('export default function SearchHistory({ history, onRunSearch }) {', 'export default function SearchHistory({ history, onRunSearch }) {\n  const { t } = useLanguage()'),
    ('Search History\n      </h3>', "{t('Search History')}\n      </h3>"),
    ('No search history</p>', "{t('No search history')}</p>"),
    ('<span className="tooltip">Run search</span>', '<span className="tooltip">{t(\'Run search\')}</span>')
])

process_file(r'e:\CrimeMatrix\frontend\src\components\search\SearchResults.jsx', [
    ('{results.length} results found', "{results.length} {t('results found')}"),
    ('<th>Crime ID</th>', "<th>{t('Crime ID')}</th>"),
    ('<th>Title</th>', "<th>{t('Title')}</th>"),
    ('<th>Type</th>', "<th>{t('Type')}</th>"),
    ('<th>District</th>', "<th>{t('District')}</th>"),
    ('<th>Status</th>', "<th>{t('Status')}</th>"),
    ('<th>Date</th>', "<th>{t('Date')}</th>"),
    ('<th>Actions</th>', "<th>{t('Actions')}</th>"),
    ('{item.status}', "{t(item.status)}"),
    ('No results found', "{t('No results found')}"),
    ('Try adjusting your search or filters.', "{t('Try adjusting your search or filters.')}")
])
