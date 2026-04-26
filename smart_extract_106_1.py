"""
Index-guided citation extraction for 民國106年第1次醫學(三).
Outputs search_results_smart_106_1.json
"""
import fitz, json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HARRISON = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Harrison's Principles of Internal Medicine, 22nd Edition.pdf"
FAMMED   = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Family Medicine Principles and Practice, 7th Edition.pdf"
OUT_FILE = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/search_results_smart_106_1.json"

print("Opening PDFs...")
doc_h = fitz.open(HARRISON)
doc_f = fitz.open(FAMMED)
print(f"Harrison: {doc_h.page_count} pages, FamMed: {doc_f.page_count} pages")

CONTEXT = 900
IDX_START = 4044   # 0-based; Harrison index starts at PDF page 4045

def clean(t):
    return re.sub(r' +', ' ', t.replace('\n', ' ')).strip()

def terminate(text, max_len=CONTEXT):
    if len(text) <= max_len: return text
    chunk = text[:max_len]
    for p in ['. ', '! ', '? ']:
        idx = chunk.rfind(p)
        if idx > max_len * 0.6: return chunk[:idx+1].strip()
    return chunk.rstrip() + '…'

def extract_snippet(doc, idx_0based, kw):
    text = doc[idx_0based].get_text()
    tl = text.lower(); kl = kw.lower()
    p = tl.find(kl)
    if p < 0: p = len(text) // 2
    raw = text[max(0, p-200): min(len(text), p+CONTEXT)]
    return terminate(clean(raw))

def parse_index_pages():
    entries = {}
    for pi in range(IDX_START, doc_h.page_count):
        text = doc_h[pi].get_text()
        for line in text.splitlines():
            m = re.search(r'(\d{3,4}(?:,\s*\d{3,4})*)\s*$', line.strip())
            if not m: continue
            term = line[:m.start()].strip().rstrip(',').lower()
            if len(term) < 3: continue
            pages = [int(x.strip()) for x in m.group(1).split(',')]
            if term not in entries:
                entries[term] = pages
            else:
                entries[term].extend(pages)
    return entries

print("Parsing Harrison index...")
index = parse_index_pages()
print(f"Index entries: {len(index)}")

def score_page(doc, idx, kw1, kw2, fallback_rank):
    text = doc[idx].get_text()
    tl = text.lower()
    kl1 = kw1.lower(); kl2 = kw2.lower() if kw2 else ''
    if kl1 not in tl: return -1000
    score = tl.count(kl1) * 2
    if kl2:
        if kl2 not in tl: score -= 20
        else: score += tl.count(kl2) * 4
    for line in text.splitlines():
        sl = line.strip().lower()
        if sl.startswith(kl1) and len(line.strip().split()) <= 8:
            score += 8; break
        if kl1 in sl and len(line.strip().split()) <= 8:
            score += 4; break
    if len(text) > 1500: score += 2
    elif len(text) > 800: score += 1
    score += 0.5 / (fallback_rank + 1)
    return score

def best_harrison_page(kw1, kw2=''):
    kl = kw1.lower()
    candidates = []
    for term, pages in index.items():
        if kl in term or term in kl:
            candidates.extend(pages)
    if not candidates:
        for term, pages in index.items():
            words = kl.split()
            if any(w in term for w in words if len(w) > 4):
                candidates.extend(pages)
    candidates = list(dict.fromkeys(candidates))
    if not candidates: return None, ''
    best_idx = None; best_score = -9999
    for rank, pg in enumerate(candidates[:30]):
        pdf_idx = pg + 43 - 1  # book page + offset - 1 for 0-based
        if pdf_idx < 0 or pdf_idx >= doc_h.page_count: continue
        s = score_page(doc_h, pdf_idx, kw1, kw2, rank)
        if s > best_score: best_score = s; best_idx = pdf_idx
    if best_idx is None: return None, ''
    snip = extract_snippet(doc_h, best_idx, kw1)
    return best_idx + 1, snip  # return 1-based PDF page

def best_fammed_page(kw1, kw2=''):
    kl = kw1.lower()
    best_idx = None; best_score = -9999
    for i in range(doc_f.page_count):
        text = doc_f[i].get_text(); tl = text.lower()
        if kl not in tl: continue
        score = tl.count(kl) * 2
        if kw2 and kw2.lower() in tl: score += 4
        for line in text.splitlines():
            sl = line.strip().lower()
            if sl.startswith(kl) and len(line.strip().split()) <= 8:
                score += 8; break
        if score > best_score: best_score = score; best_idx = i
    if best_idx is None: return None, ''
    snip = extract_snippet(doc_f, best_idx, kw1)
    return best_idx + 1, snip

# Q -> (book, kw1, kw2)
# book: 'H' = Harrison's, 'F' = FamMed
PLAN = {
    1:  ('H', 'depression', 'elderly'),
    2:  ('H', 'constrictive pericarditis', 'Kussmaul'),
    3:  ('H', 'adenosine', 'supraventricular tachycardia'),
    4:  ('H', 'iron deficiency anemia', 'colonoscopy'),
    5:  ('H', 'alcoholic hepatitis', 'transaminase'),
    6:  ('H', 'nephrotic syndrome', 'effective circulating volume'),
    7:  ('H', 'nephrogenic diabetes insipidus', 'thiazide'),
    8:  ('H', 'psoriatic arthritis', 'distal interphalangeal'),
    9:  ('H', 'acute promyelocytic leukemia', 'ATRA'),
    10: ('H', 'multiple myeloma', 'globulin'),
    11: ('H', 'lung cancer', 'weight loss'),
    12: ('H', 'bronchiectasis', 'purulent sputum'),
    13: ('H', 'hypogonadism', 'prolactin'),
    14: ('H', 'thyrotoxic periodic paralysis', 'hypokalemia'),
    15: ('H', 'secondary syphilis', 'palmar rash'),
    16: ('H', 'urinary tract infection', 'Staphylococcus epidermidis'),
    17: ('H', 'stable angina', 'duration'),
    18: ('H', 'innocent murmur', 'functional'),
    19: ('H', 'ventricular fibrillation', 'sudden cardiac death'),
    20: ('H', 'atherosclerosis', 'risk factor'),
    21: ('H', 'mitral valve prolapse', 'midsystolic click'),
    22: ('H', 'thrombolytic therapy', 'NSTEMI'),
    23: ('H', 'mitral stenosis', 'hemoptysis'),
    24: ('H', 'heart failure', 'S4'),
    25: ('H', 'hepatitis C', 'interferon ribavirin'),
    26: ('H', 'liver abscess', 'Klebsiella'),
    27: ('H', 'hepatocellular carcinoma', 'rupture'),
    28: ('H', 'hepatocellular carcinoma', 'transcatheter arterial chemoembolization'),
    29: ('H', 'Helicobacter pylori', 'gastric lymphoma'),
    30: ('H', 'antacid', 'H2 receptor antagonist'),
    31: ('H', 'dumping syndrome', 'dietary'),
    32: ('H', 'chronic kidney disease', 'ACE inhibitor'),
    33: ('H', 'uremic pericarditis', 'dialysis'),
    34: ('H', 'minimal change disease', 'complement'),
    35: ('H', 'anti-citrullinated protein', 'rheumatoid arthritis'),
    36: ('H', 'Sjogren syndrome', 'anti-Ro'),
    37: ('H', 'eosinophilic granulomatosis', 'asthma'),
    38: ('H', 'Behcet disease', 'pathergy'),
    39: ('H', 'chronic urticaria', 'allergen'),
    40: ('H', 'breast mass', 'mammography'),
    41: ('H', 'mediastinal germ cell tumor', 'alpha-fetoprotein'),
    42: ('H', 'Lynch syndrome', 'mismatch repair'),
    43: ('H', 'folate deficiency', 'alcohol'),
    44: ('H', 'thrombocytopenia', 'platelet antibody'),
    45: ('H', 'gefitinib', 'neutropenia'),
    46: ('H', 'COPD', 'ventilation perfusion'),
    47: ('H', 'obstructive sleep apnea', 'polysomnography'),
    48: ('H', 'EGFR mutation', 'tyrosine kinase inhibitor'),
    49: ('H', 'persistent asthma', 'inhaled corticosteroid'),
    50: ('H', 'rapid shallow breathing index', 'weaning'),
    51: ('H', 'multiple endocrine neoplasia', 'RET'),
    52: ('H', 'vitamin D', '25-hydroxyvitamin'),
    53: ('H', 'lipoprotein lipase deficiency', 'triglyceride'),
    54: ('H', 'maturity-onset diabetes', 'insulin secretion'),
    55: ('H', 'granuloma inguinale', 'Klebsiella granulomatis'),
    56: ('H', 'vertebral osteomyelitis', 'Staphylococcus aureus'),
    57: ('H', 'melioidosis', 'Burkholderia pseudomallei'),
    58: ('H', 'linezolid', 'thrombocytopenia'),
    59: ('H', 'bacterial meningitis', 'cerebrospinal fluid glucose'),
    60: ('H', 'pyogenic liver abscess', 'Klebsiella'),
    61: ('H', 'fever of unknown origin', 'classification'),
    62: ('H', 'radiation', 'Prussian blue'),
    63: ('H', 'radiation exposure', 'lymphocyte'),
    64: ('H', 'lung cancer', 'brain metastasis'),
    65: ('H', 'SIADH', 'hyponatremia'),
    66: ('H', 'pneumonia', 'elderly atypical'),
    67: ('H', 'LDL cholesterol', 'statin'),
    68: ('H', 'osteoporosis', 'T-score'),
    69: ('F', 'travel medicine', 'hypertension'),
    70: ('H', 'suicidal ideation', 'hospitalization'),
    71: ('F', 'primary care', 'United States'),
    72: ('F', 'elder abuse', 'social worker'),
    73: ('F', 'do not resuscitate', 'terminal'),
    74: ('H', 'pneumothorax', 'chest radiograph'),
    75: ('H', 'digoxin', 'nitroglycerin'),
    76: ('H', 'pulseless electrical activity', 'hyperkalemia'),
    77: ('H', 'drowning', 'resuscitation'),
    78: ('H', 'cardiopulmonary resuscitation', 'ventilation rate'),
    79: ('H', 'medical record', 'falsification'),
    80: ('F', 'do not resuscitate', 'terminal cancer'),
}

results = {}
none_count = 0

for qnum in range(1, 81):
    book_code, kw1, kw2 = PLAN[qnum]
    if book_code == 'H':
        pdf_page, snip = best_harrison_page(kw1, kw2)
        book_name = "Harrison's 22nd"
    else:
        pdf_page, snip = best_fammed_page(kw1, kw2)
        book_name = "FamMed 7th"

    if pdf_page is None:
        results[str(qnum)] = {'book': book_name, 'kw1': kw1, 'kw2': kw2, 'passages': []}
        print(f"Q{qnum:02d}: (none)")
        none_count += 1
    else:
        results[str(qnum)] = {
            'book': book_name,
            'kw1': kw1,
            'kw2': kw2,
            'passages': [{'page': pdf_page, 'snippet': snip}]
        }
        print(f"Q{qnum:02d}: p.{pdf_page} — {snip[:70]}...")

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone. {80 - none_count}/80 found, {none_count} got (none).")
print(f"Output: {OUT_FILE}")
