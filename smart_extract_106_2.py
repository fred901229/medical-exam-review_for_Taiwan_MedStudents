"""
Index-guided citation extraction for 民國106年第2次醫學(三).
Outputs search_results_smart_106_2.json
"""
import fitz, json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HARRISON = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Harrison's Principles of Internal Medicine, 22nd Edition.pdf"
FAMMED   = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Family Medicine Principles and Practice, 7th Edition.pdf"
OUT_FILE = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/search_results_smart_106_2.json"

print("Opening PDFs...")
doc_h = fitz.open(HARRISON)
doc_f = fitz.open(FAMMED)
print(f"Harrison: {doc_h.page_count} pages, FamMed: {doc_f.page_count} pages")

CONTEXT = 900
IDX_START = 4044

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
        pdf_idx = pg + 43 - 1
        if pdf_idx < 0 or pdf_idx >= doc_h.page_count: continue
        s = score_page(doc_h, pdf_idx, kw1, kw2, rank)
        if s > best_score: best_score = s; best_idx = pdf_idx
    if best_idx is None: return None, ''
    snip = extract_snippet(doc_h, best_idx, kw1)
    return best_idx + 1, snip

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

PLAN = {
    1:  ('H', 'metabolic alkalosis', 'compensation'),
    2:  ('H', 'vascular dementia', 'white matter'),
    3:  ('H', 'hypertensive urgency', 'nifedipine'),
    4:  ('H', 'heart failure preserved ejection fraction', 'ACE inhibitor'),
    5:  ('H', 'inferior myocardial infarction', 'right ventricular'),
    6:  ('H', 'hepatocellular jaundice', 'transaminase'),
    7:  ('H', 'hepatocellular carcinoma', 'transcatheter arterial'),
    8:  ('H', 'lupus nephritis', 'anti-double-stranded DNA'),
    9:  ('H', 'cryoglobulinemia', 'hepatitis C'),
    10: ('H', 'psoriatic arthritis', 'dactylitis'),
    11: ('H', 'warfarin', 'prothrombin time'),
    12: ('H', 'EGFR mutation', 'tyrosine kinase inhibitor'),
    13: ('H', 'asthma', 'inhaled corticosteroid'),
    14: ('H', 'hypothyroidism', 'postpartum'),
    15: ('H', 'scrub typhus', 'eschar'),
    16: ('H', 'ESBL', 'carbapenem'),
    17: ('H', 'dyspnea', 'anxiety'),
    18: ('H', 'edema', 'unilateral'),
    19: ('H', 'physician charter', 'professionalism'),
    20: ('H', 'mitral stenosis', 'murmur'),
    21: ('H', 'jugular venous pressure', 'internal jugular'),
    22: ('H', 'mitral valve prolapse', 'myxomatous'),
    23: ('H', 'STEMI', 'calcium channel blocker'),
    24: ('H', 'valve replacement', 'mortality'),
    25: ('H', 'Mallory-Weiss', 'tear'),
    26: ('H', 'bile acid', 'ileum'),
    27: ('H', 'fulminant hepatic failure', 'drug'),
    28: ('H', 'Helicobacter pylori', 'gastroesophageal reflux'),
    29: ('H', 'primary biliary cholangitis', 'antimitochondrial'),
    30: ('H', 'Ranson criteria', 'pancreatitis'),
    31: ('H', 'end-stage renal disease', 'kidney transplantation'),
    32: ('H', 'primary aldosteronism', 'hypokalemia'),
    33: ('H', 'hepatitis C', 'glomerulonephritis'),
    34: ('H', 'glomerular hematuria', 'dysmorphic'),
    35: ('H', 'ankylosing spondylitis', 'HLA-B27'),
    36: ('H', 'calcium pyrophosphate', 'shoulder'),
    37: ('H', 'lupus nephritis', 'cyclosporine'),
    38: ('H', 'Sjogren syndrome', 'anticardiolipin'),
    39: ('H', 'febrile neutropenia', 'chemotherapy'),
    40: ('H', 'nasopharyngeal carcinoma', 'biopsy'),
    41: ('H', 'T-cell lymphoblastic', 'mediastinal'),
    42: ('H', 'low molecular weight heparin', 'anti-Xa'),
    43: ('H', 'chronic myeloid leukemia', 'imatinib'),
    44: ('H', 'acute myeloid leukemia', 'etoposide'),
    45: ('H', 'multiple myeloma', 'hypercalcemia'),
    46: ('H', 'bronchiectasis', 'antibiotic'),
    47: ('H', 'mechanical ventilation', 'inspiratory flow'),
    48: ('H', 'acute respiratory distress syndrome', 'tidal volume'),
    49: ('H', 'pleural effusion', 'exudate'),
    50: ('H', 'EGFR mutation', 'adenocarcinoma'),
    51: ('H', 'acute respiratory distress syndrome', 'PEEP'),
    52: ('H', 'Kallmann syndrome', 'hypogonadism'),
    53: ('H', 'prolactinoma', 'dopamine agonist'),
    54: ('H', 'pyriform sinus', 'fistula'),
    55: ('H', 'pituitary', 'radiation'),
    56: ('H', 'Cushing syndrome', 'iatrogenic'),
    57: ('H', 'type 2 diabetes', 'metformin'),
    58: ('H', 'endocarditis prophylaxis', 'mitral valve prolapse'),
    59: ('H', 'measles', 'Koplik'),
    60: ('H', 'HPV', 'cervical cancer'),
    61: ('H', 'West Nile virus', 'mosquito'),
    62: ('H', 'Vibrio cholerae', 'infectious dose'),
    63: ('H', 'antibiotic resistance', 'subinhibitory'),
    64: ('H', 'hypothermia', 'ventricular fibrillation'),
    65: ('H', 'hypothermia', 'rewarming'),
    66: ('F', 'elderly', 'heterogeneity'),
    67: ('F', 'obesity', 'childhood'),
    68: ('H', 'atypical pneumonia', 'Mycoplasma'),
    69: ('H', 'informed consent', 'corticosteroid'),
    70: ('F', 'immunization', 'infant'),
    71: ('F', 'number needed to harm', 'hormone replacement'),
    72: ('F', 'transtheoretical model', 'preparation'),
    73: ('F', 'smoking cessation', 'quit date'),
    74: ('H', 'acute pancreatitis', 'computed tomography'),
    75: ('H', 'hepatic encephalopathy', 'grade'),
    76: ('H', 'deep vein thrombosis', 'risk factor'),
    77: ('H', 'ventricular tachycardia', 'cardioversion'),
    78: ('F', 'traveler diarrhea', 'antibiotic'),
    79: ('F', 'medical practice', 'prescription'),
    80: ('F', 'medical law', 'informed consent'),
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
            'book': book_name, 'kw1': kw1, 'kw2': kw2,
            'passages': [{'page': pdf_page, 'snippet': snip}]
        }
        print(f"Q{qnum:02d}: p.{pdf_page} — {snip[:65]}...")

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone. {80-none_count}/80 found, {none_count} got (none).")
