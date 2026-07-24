import re
import codecs

with codecs.open(r'e:\CrimeMatrix\frontend\src\components\search\caseData.js', 'r', 'utf-8') as f:
    text = f.read()

# Replace `export const cases = [` with `export const getCases = (t) => [`
text = text.replace('export const cases = [', 'export const getCases = (t) => [')

def replacer(match):
    key = match.group(1)
    val = match.group(2)
    return f"{key}: t({val})"

fields_to_wrap = ['title', 'type', 'district', 'status', 'date', 'priority', 'officer', 'description', 
                  'event', 'relation', 'notes', 'aiInsights']

for field in fields_to_wrap:
    text = re.sub(r'(' + field + r')\s*:\s*(\'[^\']*\')', replacer, text)
    # Also handle suspects.status, evidence.type, etc if they share the key name but it's already caught by the field name.

# 'status' is in fields_to_wrap
# 'type' is in fields_to_wrap

# Handle specific ID wrapping like FIR
# e.g., id: 'FIR #4521' -> id: `${t('FIR')} #4521` (Wait, id is usually not translated but for display it is used. In this case, maybe we don't translate id, but case_number which is the same.)
# Actually, the user asked to "fix the multilingual features for this content".

with codecs.open(r'e:\CrimeMatrix\frontend\src\components\search\caseData.js', 'w', 'utf-8') as f:
    f.write(text)

print("Wrapped caseData.js successfully")
