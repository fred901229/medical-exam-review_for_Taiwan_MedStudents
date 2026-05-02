"""
從 Harrison's 22nd Edition 擷取各章節文字，用 Gemini API 生成 Anki 閃卡
輸出：docs/flashcards.json

使用方式：
  python generate_flashcards.py                  # 處理所有章節
  python generate_flashcards.py --start 240 --end 290  # 只處理指定章節範圍
  python generate_flashcards.py --chapter 241    # 只處理單一章節
"""
import fitz, json, sys, os, re, time, argparse, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google import genai

# ── API Key ──────────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gemini_api_key.txt")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    API_KEY = input("請輸入 Gemini API Key: ").strip()

# ── 設定 ──────────────────────────────────────────────────────
HARRISON_PATH = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/教科書/醫學三/Harrison's Principles of Internal Medicine, 22nd Edition.pdf"
OUTPUT_PATH   = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/docs/flashcards.json"
PDF_OFFSET    = 43   # PDF page = book page + PDF_OFFSET (1-indexed)
PAGES_PER_CH  = 5    # 每章擷取的最大頁數（避免 token 超限）
CARDS_PER_CH  = 7    # 每章生成的閃卡數
SLEEP_BETWEEN = 8.0  # 秒（避免 rate limit）
MAX_CHARS     = 6000 # 傳給 Gemini 的最大字元數

client = genai.Client(api_key=API_KEY)
available = [
    m.name for m in client.models.list()
    if 'generateContent' in (m.supported_actions or [])
    and 'flash' in m.name.lower()
    and 'lite' not in m.name.lower()
    and 'tts' not in m.name.lower()
    and 'image' not in m.name.lower()
]
MODEL = available[0] if available else "models/gemini-2.0-flash"
print(f"使用模型: {MODEL}")

# ── 解析目錄 ────────────────────────────────────────────────
def extract_toc(doc):
    full_toc = ''
    for p in range(6, 20):
        full_toc += doc[p].get_text() + '\n'

    chapters = []
    current_part = ''
    for line in full_toc.split('\n'):
        line = line.strip()
        if re.match(r'^PART \d+', line) or re.match(r'^PART [A-Z]', line):
            current_part = line
        m = re.match(r'^(\d+)\s+(.+?)\s*\.{2,}\s*(\d+)\s*$', line)
        if m:
            chapters.append({
                'ch': int(m.group(1)),
                'title': m.group(2).strip(),
                'part': current_part,
                'book_page': int(m.group(3))
            })
    # 計算每章的結束頁
    for i in range(len(chapters) - 1):
        chapters[i]['end_book_page'] = chapters[i + 1]['book_page'] - 1
    if chapters:
        chapters[-1]['end_book_page'] = chapters[-1]['book_page'] + 10
    return chapters

# ── 擷取章節文字 ───────────────────────────────────────────
def extract_chapter_text(doc, ch):
    start_pdf = ch['book_page'] + PDF_OFFSET - 1   # 0-indexed
    end_pdf   = ch['end_book_page'] + PDF_OFFSET - 1
    end_pdf   = min(end_pdf, start_pdf + PAGES_PER_CH - 1, doc.page_count - 1)

    texts = []
    for p in range(start_pdf, end_pdf + 1):
        t = doc[p].get_text()
        t = re.sub(r'\n+', '\n', t).strip()
        texts.append(t)
    combined = '\n'.join(texts)
    return combined[:MAX_CHARS]

# ── Gemini 生成閃卡 ────────────────────────────────────────
PROMPT_TEMPLATE = """你是醫學教育專家，專門幫助台灣醫師國考（二階）學生複習。

以下是 Harrison's Principles of Internal Medicine 22nd Edition 的「{title}」章節原文。

請根據這段內容，生成 {n} 張繁體中文 Anki 閃卡。每張閃卡需符合以下原則：
- 正面(front)：一個具體的臨床問題（例如：診斷標準、機轉、治療選擇、鑑別診斷、典型表現）
- 背面(back)：簡潔的答案，2-5 句話，包含關鍵數值或要點
- 聚焦於國考常考的臨床重要知識
- 避免重複，每題考不同面向

只回傳 JSON 陣列，格式如下（不要有其他文字）：
[
  {{"front": "問題...", "back": "答案..."}},
  ...
]

章節原文：
---
{text}
---"""

def generate_cards(ch, text):
    prompt = PROMPT_TEMPLATE.format(
        title=ch['title'],
        n=CARDS_PER_CH,
        text=text
    )
    try:
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        raw = resp.text.strip()
        # 去掉 markdown code blocks
        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'^```\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
        cards_data = json.loads(raw)
        result = []
        for i, c in enumerate(cards_data):
            if 'front' in c and 'back' in c:
                result.append({
                    'id':      f"h22_{ch['ch']:04d}_{i+1:02d}",
                    'ch':      ch['ch'],
                    'chapter': ch['title'],
                    'part':    ch.get('part', ''),
                    'front':   c['front'].strip(),
                    'back':    c['back'].strip(),
                    'source':  f"Harrison's 22nd, Ch.{ch['ch']}, p.{ch['book_page']}"
                })
        return result
    except Exception as e:
        print(f"    錯誤: {e}")
        return []

# ── 主程式 ──────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start',   type=int, default=None, help='起始章節編號')
    parser.add_argument('--end',     type=int, default=None, help='結束章節編號')
    parser.add_argument('--chapter', type=int, default=None, help='單一章節編號')
    parser.add_argument('--output',  default=OUTPUT_PATH)
    args = parser.parse_args()

    print("載入 Harrison's PDF（可能需要幾秒）...")
    doc = fitz.open(HARRISON_PATH)
    print(f"共 {doc.page_count} 頁")

    chapters = extract_toc(doc)
    print(f"解析到 {len(chapters)} 個章節")

    # 讀取現有進度
    if os.path.exists(args.output):
        with open(args.output, encoding='utf-8') as f:
            existing = json.load(f)
        all_cards = existing.get('cards', [])
        done_chs  = {c['ch'] for c in all_cards}
        print(f"已有 {len(all_cards)} 張閃卡，跳過已完成的 {len(done_chs)} 章")
    else:
        all_cards = []
        done_chs  = set()

    # 篩選要處理的章節
    if args.chapter:
        target = [c for c in chapters if c['ch'] == args.chapter]
    elif args.start or args.end:
        s = args.start or 1
        e = args.end or 999
        target = [c for c in chapters if s <= c['ch'] <= e]
    else:
        target = chapters

    todo = [c for c in target if c['ch'] not in done_chs]
    print(f"待處理: {len(todo)} 章節")

    def save():
        all_cards.sort(key=lambda x: (x['ch'], x['id']))
        out = {
            'version':   2,
            'generated': time.strftime('%Y-%m-%d'),
            'total':     len(all_cards),
            'cards':     all_cards
        }
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    for i, ch in enumerate(todo):
        print(f"[{i+1}/{len(todo)}] Ch.{ch['ch']} {ch['title'][:50]}  (p.{ch['book_page']})")
        text = extract_chapter_text(doc, ch)
        if len(text) < 200:
            print(f"  ⚠ 文字過少，跳過")
            continue

        t0 = time.time()
        cards = generate_cards(ch, text)
        elapsed = time.time() - t0

        if cards:
            all_cards.extend(cards)
            print(f"  ✓ 生成 {len(cards)} 張閃卡（{elapsed:.1f}s）")
        else:
            print(f"  ✗ 生成失敗")

        # 每 10 章存一次
        if (i + 1) % 10 == 0:
            save()
            print(f"  [已儲存 {len(all_cards)} 張閃卡]")

        if i < len(todo) - 1:
            time.sleep(SLEEP_BETWEEN)

    save()
    print(f"\n完成！共 {len(all_cards)} 張閃卡 → {args.output}")

if __name__ == '__main__':
    main()
