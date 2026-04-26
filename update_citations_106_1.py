"""
Apply citations from search_results_smart_106_1.json to official_notes.json
for 民國106年第1次醫學(三).
"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTES_FILE  = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/docs/official_notes.json"
SMART_FILE  = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/search_results_smart_106_1.json"

with open(NOTES_FILE, encoding='utf-8') as f:
    notes = json.load(f)
with open(SMART_FILE, encoding='utf-8') as f:
    smart = json.load(f)

def make_key(n):
    return f"民國106年_第1次_醫學(三)_{n}"

def build_citation(entry):
    if not entry or not entry.get('passages'):
        return "【原文依據】\n（原文教科書中未找到直接相關段落）"
    book = entry['book']
    if book == "Harrison's 22nd":
        book_full = "Harrison's Principles of Internal Medicine, 22nd Edition"
    elif book == "FamMed 7th":
        book_full = "Family Medicine Principles and Practice, 7th Edition"
    else:
        book_full = book
    p = entry['passages'][0]
    snip = p['snippet'].strip()
    return (
        f"【原文依據】\n"
        f"{book_full}, p.{p['page']}：\n"
        f"> {snip}"
    )

updated = 0
for qnum in range(1, 81):
    key = make_key(qnum)
    if key not in notes:
        print(f"Q{qnum:02d}: key not found")
        continue
    entry = smart.get(str(qnum))
    new_citation = build_citation(entry)
    stripped = re.sub(r'\n*【原文依據】.*$', '', notes[key], flags=re.DOTALL).rstrip()
    notes[key] = stripped + "\n\n" + new_citation
    updated += 1
    pg = entry['passages'][0]['page'] if entry and entry.get('passages') else 'N/A'
    print(f"Q{qnum:02d}: p.{pg}")

with open(NOTES_FILE, "w", encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print(f"\nDone. Updated {updated}/80 notes.")
