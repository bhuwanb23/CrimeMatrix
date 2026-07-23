import os
import re
import codecs

src_dir = r"e:\CrimeMatrix\frontend\src"
trans_file = r"e:\CrimeMatrix\frontend\src\context\translations.js"

# 1. Read existing keys
existing_keys = set()
with codecs.open(trans_file, "r", "utf-8") as f:
    content = f.read()
    # Find English block
    eng_block = re.search(r"English:\s*\{([^}]*)\}", content)
    if eng_block:
        # Match keys like 'Key Name': or "Key Name":
        keys = re.findall(r"['\"](.*?)['\"]\s*:", eng_block.group(1))
        existing_keys.update(keys)

# 2. Extract t('...') or t("...") from code
found_keys = set()
pattern = re.compile(r"t\(\s*['\"](.*?)['\"]\s*\)")

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith((".jsx", ".js")):
            with codecs.open(os.path.join(root, file), "r", "utf-8") as f:
                code = f.read()
                matches = pattern.findall(code)
                found_keys.update(matches)

missing_keys = found_keys - existing_keys
print("Found %d missing keys" % len(missing_keys))
for k in sorted(missing_keys):
    print("- " + k)
