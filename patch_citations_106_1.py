"""
Patch the 6 questions that got (none) citations in 106-1.
"""
import fitz, json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HARRISON = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Harrison's Principles of Internal Medicine, 22nd Edition.pdf"
FAMMED   = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Family Medicine Principles and Practice, 7th Edition.pdf"
NOTES_FILE = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/docs/official_notes.json"
SMART_FILE = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/search_results_smart_106_1.json"

print("Opening PDFs...")
doc_h = fitz.open(HARRISON)
doc_f = fitz.open(FAMMED)
print("Done")

CONTEXT = 900

def clean(t):
    return re.sub(r' +', ' ', t.replace('\n', ' ')).strip()

def terminate(text, max_len=CONTEXT):
    if len(text) <= max_len: return text
    chunk = text[:max_len]
    for p in ['. ', '! ', '? ']:
        idx = chunk.rfind(p)
        if idx > max_len * 0.6: return chunk[:idx+1].strip()
    return chunk.rstrip() + '…'

def snip(doc, pdf_idx_0based, kw):
    text = doc[pdf_idx_0based].get_text()
    tl = text.lower()
    kl = kw.lower()
    p = tl.find(kl)
    if p < 0: p = len(text) // 2
    raw = text[max(0, p-250): min(len(text), p+CONTEXT)]
    return terminate(clean(raw))

# Direct mappings: qnum -> (book_code, pdf_page_1based, keyword_for_snippet)
# Q45: gefitinib causes rash/diarrhea NOT neutropenia (vs. traditional chemo)
# Q57: melioidosis treatment chapter
# Q58: linezolid thrombocytopenia
# Q73: FamMed terminal/advance directive/POLST
# Q77: Harrison p.2379 mentions Heimlich for airway obstruction (not drowning)
# Q80: FamMed palliative care / terminal illness
PATCHES = {
    45: ('H', 657,  'gefitinib'),
    57: ('H', 1356, 'melioidosis'),
    58: ('H', 1247, 'linezolid'),
    73: ('F', 794,  'resuscitat'),
    77: ('H', 2379, 'Heimlich'),
    80: ('F', 789,  'terminal'),
}

print("\n--- Verifying pages ---")
for qnum, (code, pdf_p, kw) in list(PATCHES.items()):
    doc = doc_h if code == 'H' else doc_f
    idx = pdf_p - 1
    if idx >= doc.page_count:
        print(f"Q{qnum}: pdf page {pdf_p} out of range ({doc.page_count})")
        continue
    text = doc[idx].get_text().lower()
    found = kw.lower() in text
    print(f"Q{qnum} p.{pdf_p}: kw '{kw}' found={found}, len={len(text)}")

print("\n--- Extracting snippets ---")
results = {}
for qnum, (code, pdf_p, kw) in PATCHES.items():
    doc = doc_h if code == 'H' else doc_f
    idx = pdf_p - 1

    # Try the page; if kw not found, scan ±5 pages
    text = doc[idx].get_text()
    if kw.lower() not in text.lower():
        for delta in range(1, 6):
            for sign in [1, -1]:
                ni = idx + sign * delta
                if 0 <= ni < doc.page_count and kw.lower() in doc[ni].get_text().lower():
                    idx = ni
                    pdf_p = idx + 1
                    break
            else: continue
            break

    snippet = snip(doc, idx, kw)
    book_name = "Harrison's 22nd" if code == 'H' else 'FamMed 7th'
    book_full = ("Harrison's Principles of Internal Medicine, 22nd Edition"
                 if code == 'H' else
                 "Family Medicine Principles and Practice, 7th Edition")

    results[qnum] = {
        'book_full': book_full,
        'page': pdf_p,
        'snippet': snippet,
    }
    print(f"Q{qnum:02d}: p.{pdf_p} — {snippet[:80]}...")

print("\n--- Patching notes ---")
with open(NOTES_FILE, encoding='utf-8') as f:
    notes = json.load(f)
with open(SMART_FILE, encoding='utf-8') as f:
    smart = json.load(f)

def make_key(n):
    return f"民國106年_第1次_醫學(三)_{n}"

for qnum, r in results.items():
    key = make_key(qnum)
    if key not in notes:
        print(f"Q{qnum}: key not found"); continue

    citation = (
        f"【原文依據】\n"
        f"{r['book_full']}, p.{r['page']}：\n"
        f"> {r['snippet'].strip()}"
    )
    stripped = re.sub(r'\n*【原文依據】.*$', '', notes[key], flags=re.DOTALL).rstrip()
    notes[key] = stripped + "\n\n" + citation

    smart[str(qnum)]['passages'] = [{'page': r['page'], 'snippet': r['snippet']}]
    print(f"Q{qnum:02d}: patched → p.{r['page']}")

with open(NOTES_FILE, "w", encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)
with open(SMART_FILE, "w", encoding='utf-8') as f:
    json.dump(smart, f, ensure_ascii=False, indent=2)

print("\nDone.")
