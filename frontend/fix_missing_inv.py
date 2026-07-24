import codecs
import os

def replace_in_file(path, replacements):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)

d = r'e:\CrimeMatrix\frontend\src\components\investigation'

# CaseListPanel.jsx
replace_in_file(os.path.join(d, 'CaseListPanel.jsx'), [
    ("Active ({activeCount})", "{t('Active')} ({activeCount})"),
    ("Saved ({savedCount})", "{t('Saved')} ({savedCount})"),
    ("{inv.priority}", "{t(inv.priority)}"),
    ("{inv.status}", "{t(inv.status)}")
])

# WorkspacePanel.jsx
replace_in_file(os.path.join(d, 'WorkspacePanel.jsx'), [
    ("{tab.label}", "{t(tab.label)}"),
    ("{investigation.status}", "{t(investigation.status)}"),
    ("{investigation.priority}", "{t(investigation.priority)}"),
    ("{investigation.district}", "{t(investigation.district)}"),
    ("{investigation.progress}% complete", "{investigation.progress}% {t('complete')}")
])

# NotesTab.jsx
replace_in_file(os.path.join(d, 'NotesTab.jsx'), [
    ("{submitting ? 'Adding...' : 'Add Note'}", "{submitting ? t('Adding...') : t('Add Note')}")
])

# ToolsPanel.jsx
replace_in_file(os.path.join(d, 'ToolsPanel.jsx'), [
    ("{isSaved ? 'Resume' : 'Save'}", "{isSaved ? t('Resume') : t('Save')}"),
    ("{toggling ? 'Updating...' : (isSaved ? 'Resume Investigation' : 'Save Investigation')}", "{toggling ? t('Updating...') : (isSaved ? t('Resume Investigation') : t('Save Investigation'))}"),
    ("{scoringPriority ? 'Scoring...' : 'Score'}", "{scoringPriority ? t('Scoring...') : t('Score')}")
])

print("Fixed missing texts.")
