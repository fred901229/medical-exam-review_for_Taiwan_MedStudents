#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
醫師國考考古題 PDF 解析工具
用法: python parse_exams.py [PDF資料夾路徑]
若不指定路徑，預設使用腳本所在資料夾
"""

import json
import logging
import pdfplumber
import re
import csv
import sys
from pathlib import Path

logging.getLogger('pdfminer').setLevel(logging.ERROR)


def to_halfwidth(text):
    result = []
    for c in text:
        code = ord(c)
        if 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        elif c == '\u3000':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)


def extract_page_text(page):
    """
    使用字元層級提取，偵測上下標並標記為 <sup>/<sub>。
    若無法取得字元資料則退回一般文字提取。
    """
    chars = [c for c in page.chars if c.get('text', '')]
    if not chars:
        return page.extract_text() or ''

    # 以頁面中位數字型大小決定分行容忍度
    sizes = sorted([c['size'] for c in chars if c.get('size', 0) > 0])
    if not sizes:
        return page.extract_text() or ''
    median_size = sizes[len(sizes) // 2]
    line_tol = max(2, median_size * 0.5)

    # 依 y 座標分行
    chars_sorted = sorted(chars, key=lambda c: c['top'])
    lines, cur = [], [chars_sorted[0]]
    for c in chars_sorted[1:]:
        if abs(c['top'] - cur[0]['top']) <= line_tol:
            cur.append(c)
        else:
            lines.append(cur)
            cur = [c]
    lines.append(cur)

    result = []
    for line in lines:
        line.sort(key=lambda c: c['x0'])
        lsizes = [c['size'] for c in line if c.get('size', 0) > 0]
        ltops  = [c['top'] for c in line]
        if not lsizes:
            continue
        body_size = max(lsizes)
        body_top  = sorted(ltops)[len(ltops) // 2]

        html, tag = '', None
        for c in line:
            ch = c.get('text', '')
            if not ch:
                continue
            ratio    = (c.get('size', body_size) / body_size) if body_size else 1
            top_diff = c.get('top', body_top) - body_top
            if ratio < 0.8 and top_diff < -body_size * 0.15:
                new_tag = 'sup'
            elif ratio < 0.8 and top_diff > body_size * 0.1:
                new_tag = 'sub'
            else:
                new_tag = None
            if new_tag != tag:
                if tag:     html += f'</{tag}>'
                if new_tag: html += f'<{new_tag}>'
                tag = new_tag
            html += ch.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if tag:
            html += f'</{tag}>'
        if html.strip():
            result.append(html)

    return '\n'.join(result)


def read_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            t = extract_page_text(page)
            if t:
                # 插入頁碼標記，供 parse_questions 追蹤每題所在頁面
                pages.append(f'<<<PAGE:{i}>>>\n{t}')
    text = '\n'.join(pages)

    # 部分 PDF 使用自訂字型編碼圓圈數字（①②③④），導致提取出超出 BMP 的特殊字元
    special_chars = sorted(set(c for c in text if ord(c) > 0xFFFF))
    circled = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
    for i, char in enumerate(special_chars[:len(circled)]):
        text = text.replace(char, circled[i])

    return text


def parse_questions(raw):
    text = to_halfwidth(raw)
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    questions = []
    cur = None
    field = None
    prev_num = 0
    current_page = 0

    page_re = re.compile(r'^<<<PAGE:(\d+)>>>$')
    q_re    = re.compile(r'^(\d{1,2})\s*[.．)）]\s*(.*)$')
    opt_re  = re.compile(r'^([A-D])\s*[.．)）]\s*(.*)$')

    for line in lines:
        pm = page_re.match(line)
        if pm:
            current_page = int(pm.group(1))
            continue

        qm = q_re.match(line)
        if qm:
            num = int(qm.group(1))
            if num == prev_num + 1:
                if cur:
                    questions.append(cur)
                cur = {
                    'num': num,
                    'question': qm.group(2),
                    'A': '', 'B': '', 'C': '', 'D': '',
                    'page': current_page,
                }
                field = 'question'
                prev_num = num
                continue

        om = opt_re.match(line)
        if om and cur:
            letter = om.group(1)
            cur[letter] = om.group(2)
            field = letter
            continue

        if cur and field and len(line) > 2:
            cur[field] += ' ' + line

    if cur:
        questions.append(cur)

    return questions


def extract_images(pdf_path, questions, output_dir, prefix):
    """
    從試題 PDF 提取圖片，依題號與頁碼對應。
    回傳 {題號: [相對路徑, ...]}
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 建立 page → [question_nums] 的對應
    page_qs = {}
    for q in questions:
        page_qs.setdefault(q.get('page', 0), []).append(q['num'])

    result = {}
    scale = 150 / 72  # 150 DPI 渲染比例

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            if not page.images:
                continue

            try:
                pil_img = page.to_image(resolution=150).original
            except Exception as e:
                print(f'    無法渲染第{page_num+1}頁: {e}')
                continue

            # 找出此頁各題號的 y 座標（從頁面頂部往下）
            qs_on_page = page_qs.get(page_num, [])
            q_y = []  # [(question_num, y_top)]
            try:
                q_word_re = re.compile(r'^(\d{1,2})[.．)）]$')
                for word in page.extract_words():
                    m = q_word_re.match(to_halfwidth(word['text']))
                    if m and int(m.group(1)) in qs_on_page:
                        q_y.append((int(m.group(1)), word['top']))
            except Exception:
                pass

            # 合併相鄰/重疊的圖片條（PDF 常將一張圖拆成多個橫條儲存）
            def merge_img_boxes(imgs, tol=8):
                boxes = [(i['x0'], i['top'], i['x1'], i['bottom']) for i in imgs]
                merged = []
                used = [False] * len(boxes)
                for i, b in enumerate(boxes):
                    if used[i]:
                        continue
                    x0, y0, x1, y1 = b
                    changed = True
                    while changed:
                        changed = False
                        for j, b2 in enumerate(boxes):
                            if used[j] or j == i:
                                continue
                            # 水平重疊且垂直相鄰
                            if b2[0] < x1 + tol and b2[2] > x0 - tol and b2[1] < y1 + tol and b2[3] > y0 - tol:
                                x0 = min(x0, b2[0]); y0 = min(y0, b2[1])
                                x1 = max(x1, b2[2]); y1 = max(y1, b2[3])
                                used[j] = True
                                changed = True
                    used[i] = True
                    merged.append({'x0': x0, 'top': y0, 'x1': x1, 'bottom': y1})
                return merged

            merged_imgs = merge_img_boxes(page.images)

            for img_idx, img in enumerate(merged_imgs):
                # 決定此圖屬於哪一題（找位置最接近且在圖上方的題號）
                target_q = None
                if q_y:
                    img_top = img.get('top', 0)
                    for q_num, q_top in sorted(q_y, key=lambda x: x[1]):
                        if q_top <= img_top:
                            target_q = q_num
                    if target_q is None:
                        target_q = min(q_y, key=lambda x: x[1])[0]
                elif qs_on_page:
                    target_q = min(qs_on_page)

                if target_q is None:
                    continue

                try:
                    left  = max(0, int(img['x0']     * scale) - 4)
                    upper = max(0, int(img['top']    * scale) - 4)
                    right = min(pil_img.width,  int(img['x1']     * scale) + 4)
                    lower = min(pil_img.height, int(img['bottom'] * scale) + 4)

                    if right <= left or lower <= upper:
                        continue

                    fname = f'{prefix}_q{target_q:03d}_i{img_idx}.jpg'
                    cropped = pil_img.crop((left, upper, right, lower)).convert('RGB')
                    cropped.save(output_dir / fname, 'JPEG', quality=75, optimize=True)
                    result.setdefault(target_q, []).append(f'images/{fname}')
                    print(f'    圖片: 第{target_q}題 → {fname}')
                except Exception as e:
                    print(f'    圖片提取失敗 (p{page_num}, img{img_idx}): {e}')

    return result


def parse_answers(raw):
    """
    回傳 dict: {題號(int): 答案(str)}
    答案格式: 'A'/'B'/'C'/'D'、'送分'、'CD'（多重答案）等

    # 的含義: 備註佔位符，實際答案由下方備註行決定
    備註格式範例:
      第64題答C、D給分  → 答案為 'CD'
      第64題送分        → 答案為 '送分'
    """
    text = to_halfwidth(raw)
    answers_seq = []
    notes = {}  # {題號: 答案} 來自備註的明確說明

    # 備註解析：對全文搜尋，允許題號與說明之間有換行或空格
    # 多重答案：「第64題答C、D給分」
    for m in re.finditer(r'第(\d+)題[\s，,]*答([A-D](?:[、，,][A-D])*)給分', text):
        qnum = int(m.group(1))
        letters = sorted(set(re.findall(r'[A-D]', m.group(2))))
        notes[qnum] = ''.join(letters)

    # 多重答案：「第36題，答A或D或AD者均給分」
    for m in re.finditer(r'第(\d+)題[\s，,]*答([^。\n]{1,30})均給分', text):
        qnum = int(m.group(1))
        letters = sorted(set(re.findall(r'[A-D]', m.group(2))))
        if letters:
            notes[qnum] = ''.join(letters)

    # 送分：各種格式，允許題號後有換行
    for m in re.finditer(r'第(\d+)題[\s，,]*(?:送分|一律給分)', text):
        notes[int(m.group(1))] = '送分'

    for line in text.splitlines():
        line = line.strip()

        # 從「答案」行取出答案序列，# 保留為佔位符
        # 第一個字元必須是 A/B/C/D/# 才算真正的答案行（排除「標準答案：答案標註#者...」等說明文字）
        if '答案' in line:
            after = re.sub(r'^.*?答案', '', line)
            if '備註' in after:
                after = after[:after.index('備註')]
            after = after.strip()
            if after and after[0] in 'ABCD#':
                found = re.findall(r'[A-D#]', after)
                answers_seq.extend(found)

    # 建立序號對應（# 先保留，等備註解析後決定）
    result = {}
    hash_positions = []
    for i, ans in enumerate(answers_seq, 1):
        if ans == '#':
            result[i] = None  # 待備註補充
            hash_positions.append(i)
        else:
            result[i] = ans

    # 用備註覆蓋（包含所有 # 的題目）
    result.update(notes)

    # 確認所有 # 都已被備註解析
    for qnum in hash_positions:
        if result.get(qnum) is None:
            print(f'    注意: 第{qnum}題有 # 標記但找不到對應備註，將使用原始答案')
            result[qnum] = '?'

    return result


def parse_folder_name(path):
    """
    從檔案路徑中的資料夾名稱（如 '110-1考畢題答'）解析年份和考次。
    回傳 ('民國110年', '第1次')，若無法解析則回傳 (None, None)。
    """
    folder_re = re.compile(r'(\d{3})-(\d+)考畢題答')
    for part in Path(path).parts:
        m = folder_re.match(part)
        if m:
            return f'民國{m.group(1)}年', f'第{m.group(2)}次'
    return None, None


def scan_folder(folder):
    """
    掃描資料夾，回傳每個考科的試題、原始答案、申覆答案路徑。
    """
    folder = Path(folder)
    questions = {}
    ans_orig = {}
    ans_mod = {}

    q_re = re.compile(r'^(\d+)_(\d+)_(醫學[(（][三四五六][)）])', re.IGNORECASE)
    a_re = re.compile(r'^(\d+)_ANS(\d+)_(醫學[(（][三四五六][)）])', re.IGNORECASE)
    m_re = re.compile(r'^(\d+)_MOD(\d+)_(醫學[(（][三四五六][)）])', re.IGNORECASE)

    for f in sorted(folder.rglob('*.pdf')):
        name = f.name

        mm = m_re.match(name)
        if mm:
            ans_mod[(mm.group(1), mm.group(3))] = f
            continue

        am = a_re.match(name)
        if am:
            ans_orig[(am.group(1), am.group(3))] = f
            continue

        qm = q_re.match(name)
        if qm:
            questions[(qm.group(1), qm.group(3))] = f

    exams = []
    for key, q_path in questions.items():
        exam_code, subject = key

        if key not in ans_orig and key not in ans_mod:
            print(f'  警告: 找不到 {q_path.name} 的答案檔，略過')
            continue

        year, session = parse_folder_name(q_path)
        if not year:
            year, session = f'民國{exam_code[:3]}年', f'第?次'
        exams.append({
            'year': year,
            'session': session,
            'subject': subject,
            'q_path': q_path,
            'ans_orig_path': ans_orig.get(key),
            'ans_mod_path': ans_mod.get(key),
        })

    return sorted(exams, key=lambda x: (x['year'], x['session'], x['subject']))


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent
    print(f'掃描資料夾: {folder}\n')

    exams = scan_folder(folder)
    if not exams:
        print('找不到符合格式的 PDF 檔案！')
        print('請確認檔名格式如: 110020_11_醫學(三)...pdf')
        return

    print(f'找到 {len(exams)} 個考科檔案\n')

    all_rows = []
    fields = ['年份', '考次', '考科', '題號', '題目', '選項A', '選項B', '選項C', '選項D', '正確答案', '答案來源', '圖片']
    docs_dir = Path(folder) / 'docs'
    images_dir  = docs_dir / 'images'

    for exam in exams:
        label = f"{exam['year']} {exam['session']} {exam['subject']}"
        has_mod = exam['ans_mod_path'] is not None
        print(f'  處理: {label}  ({"ANS+MOD" if has_mod else "ANS"})')

        try:
            q_text = read_pdf(exam['q_path'])
            questions = parse_questions(q_text)

            answers_orig = parse_answers(read_pdf(exam['ans_orig_path'])) if exam['ans_orig_path'] else {}
            answers_mod  = parse_answers(read_pdf(exam['ans_mod_path']))  if exam['ans_mod_path']  else {}

            # 提取圖片
            parts = exam['q_path'].stem.split('_')
            img_prefix = f'{parts[0]}_{parts[1]}' if len(parts) >= 2 else exam['q_path'].stem[:15]
            question_images = extract_images(exam['q_path'], questions, images_dir, img_prefix)

            for q in questions:
                num = q['num']
                orig = answers_orig.get(num, '?')
                mod  = answers_mod.get(num)

                if mod and mod not in ('?', orig):
                    answer = f'送分(原:{orig})' if mod == '送分' else mod
                    ans_source = '申覆後'
                else:
                    answer = orig
                    ans_source = '原始'

                all_rows.append({
                    '年份': exam['year'],
                    '考次': exam['session'],
                    '考科': exam['subject'],
                    '題號': num,
                    '題目': q['question'].strip(),
                    '選項A': q['A'].strip(),
                    '選項B': q['B'].strip(),
                    '選項C': q['C'].strip(),
                    '選項D': q['D'].strip(),
                    '正確答案': answer,
                    '答案來源': ans_source,
                    '圖片': question_images.get(num, []),
                })

            changed = sum(1 for q in questions if answers_mod.get(q['num']) and answers_mod.get(q['num']) != answers_orig.get(q['num'], '?'))
            imgs = sum(len(v) for v in question_images.values())
            print(f'    → {len(questions)} 題' + (f'，申覆更正: {changed} 題' if has_mod else '') + (f'，圖片: {imgs} 張' if imgs else ''))

        except Exception as e:
            print(f'    錯誤: {e}')

    # 輸出 CSV
    output = Path(folder) / 'exam_questions.csv'
    with open(output, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_rows)

    # 輸出 JSON（供網站使用）
    docs_dir = Path(folder) / 'docs'
    docs_dir.mkdir(exist_ok=True)
    json_output = docs_dir / 'questions.json'
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)

    print(f'\n完成！共 {len(all_rows)} 題')
    print(f'CSV:  {output}')
    print(f'JSON: {json_output}')


if __name__ == '__main__':
    main()
