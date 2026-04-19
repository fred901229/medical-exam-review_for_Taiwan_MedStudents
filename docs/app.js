let allQuestions = [];
let filtered = [];

// 深色模式
if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark');

// 字體大小
const FONT_SIZES = [13, 15, 16, 18, 20];
let fontIdx = parseInt(localStorage.getItem('fontIdx') ?? '2');
function applyFont() {
  document.documentElement.style.fontSize = FONT_SIZES[fontIdx] + 'px';
}
applyFont();

document.addEventListener('DOMContentLoaded', () => {
  // 返回頂部按鈕
  const topBtn = document.getElementById('back-to-top');
  window.addEventListener('scroll', () => {
    topBtn.style.display = window.scrollY > 400 ? 'block' : 'none';
  });
  topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  document.getElementById('theme-btn').addEventListener('click', () => {
    const dark = document.body.classList.toggle('dark');
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    document.getElementById('theme-btn').textContent = dark ? '☀️' : '🌙';
  });
  if (localStorage.getItem('theme') === 'dark')
    document.getElementById('theme-btn').textContent = '☀️';

  document.getElementById('font-up').addEventListener('click', () => {
    if (fontIdx < FONT_SIZES.length - 1) { fontIdx++; applyFont(); localStorage.setItem('fontIdx', fontIdx); }
  });
  document.getElementById('font-down').addEventListener('click', () => {
    if (fontIdx > 0) { fontIdx--; applyFont(); localStorage.setItem('fontIdx', fontIdx); }
  });
});

/* ── Progress ── */

const progress  = JSON.parse(localStorage.getItem('progress')  || '{}');
const notes     = JSON.parse(localStorage.getItem('notes')     || '{}');
const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '{}');

/* ── 官方解析 ── */

const isAdmin = new URLSearchParams(window.location.search).has('admin');
let officialNotes = {};
let officialDraft = JSON.parse(localStorage.getItem('officialDraft') || '{}');

fetch('official_notes.json')
  .then(r => r.json())
  .then(data => { officialNotes = { ...data, ...officialDraft }; })
  .catch(() => { officialNotes = { ...officialDraft }; });

if (isAdmin) {
  document.addEventListener('DOMContentLoaded', () => {
    const banner = document.createElement('div');
    banner.className = 'admin-banner';
    banner.textContent = '🔧 管理員編輯模式';
    document.body.prepend(banner);

    const exportBtn = document.createElement('button');
    exportBtn.className = 'admin-export-btn';
    exportBtn.textContent = '匯出解析 JSON';
    exportBtn.addEventListener('click', exportOfficialNotes);
    document.body.appendChild(exportBtn);
  });
}

function saveOfficialNote(qidStr, text) {
  if (text.trim()) { officialNotes[qidStr] = text; officialDraft[qidStr] = text; }
  else { delete officialNotes[qidStr]; delete officialDraft[qidStr]; }
  localStorage.setItem('officialDraft', JSON.stringify(officialDraft));
}

function exportOfficialNotes() {
  const clean = Object.fromEntries(Object.entries(officialNotes).filter(([, v]) => v.trim()));
  const blob = new Blob([JSON.stringify(clean, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'official_notes.json';
  a.click();
}

let noteTimers = {};
function saveNote(qidStr, text) {
  clearTimeout(noteTimers[qidStr]);
  noteTimers[qidStr] = setTimeout(() => {
    if (text.trim()) notes[qidStr] = text;
    else delete notes[qidStr];
    localStorage.setItem('notes', JSON.stringify(notes));
  }, 500);
}

function showNoteBox(id, qidStr) {
  const existing = document.getElementById(`${id}-note`);
  if (existing) return;

  const ansDiv = document.getElementById(`${id}-ans`);
  const officialContent = officialNotes[qidStr] || '';
  let lastEl = ansDiv;

  // 官方解析（有內容或管理員模式才顯示）
  if (officialContent || isAdmin) {
    const officialBox = document.createElement('div');
    officialBox.className = 'official-note-box';
    if (isAdmin) {
      officialBox.innerHTML = `
        <div class="official-note-label">📖 官方解析 <span class="admin-badge">編輯中</span></div>
        <textarea id="${id}-official" class="official-note-textarea" placeholder="輸入這題的解析或重點...">${officialContent}</textarea>`;
      lastEl.insertAdjacentElement('afterend', officialBox);
      lastEl = officialBox;
      document.getElementById(`${id}-official`).addEventListener('input', e => saveOfficialNote(qidStr, e.target.value));
    } else {
      officialBox.innerHTML = `
        <div class="official-note-label">📖 官方解析</div>
        <div class="official-note-text">${officialContent.split('\n').map(l => escHtml(l)).join('<br>')}</div>`;
      lastEl.insertAdjacentElement('afterend', officialBox);
      lastEl = officialBox;
    }
  }

  // 個人筆記
  const box = document.createElement('div');
  box.className = 'note-box';
  box.innerHTML = `
    <div class="note-label">📝 我的筆記</div>
    <textarea id="${id}-note" class="note-textarea" placeholder="寫下解析或筆記...">${notes[qidStr] || ''}</textarea>`;
  lastEl.insertAdjacentElement('afterend', box);
  document.getElementById(`${id}-note`).addEventListener('input', e => saveNote(qidStr, e.target.value));
}

function qid(q) {
  return `${q['年份']}_${q['考次']}_${q['考科']}_${q['題號']}`;
}

function toggleBookmark(event, id, qidStr) {
  event.stopPropagation();
  if (bookmarks[qidStr]) {
    delete bookmarks[qidStr];
  } else {
    bookmarks[qidStr] = true;
  }
  localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
  const btn = document.getElementById(`${id}-bm`);
  if (btn) btn.textContent = bookmarks[qidStr] ? '★' : '☆';
}

function saveProgress(q, result) {
  progress[qid(q)] = result;
  localStorage.setItem('progress', JSON.stringify(progress));
  updateProgressStats();
}

function renderQuizHistory() {
  const el = document.getElementById('quiz-history');
  if (!el) return;
  const history = JSON.parse(localStorage.getItem('quizHistory') || '[]');
  if (!history.length) { el.innerHTML = ''; return; }
  el.innerHTML = '<div class="history-title">測驗紀錄</div>' +
    history.map(h => `
      <div class="history-row">
        <span class="history-date">${h.date}</span>
        <span class="history-info">${h.total} 題　<span style="color:${h.rate>=60?'#22C55E':'#EF4444'}">${h.rate}%</span></span>
      </div>`).join('');
}

function updateProgressStats() {
  const total    = allQuestions.length;
  const answered = Object.keys(progress).length;
  const correct  = Object.values(progress).filter(v => v === 'correct').length;
  const rate     = answered ? Math.round(correct / answered * 100) : 0;
  const el = document.getElementById('progress-stats');
  if (el) el.textContent = `已答 ${answered}／${total} 題　答對率 ${rate}%`;
}

/* ── Quiz Mode ── */

let quizMode = false;
let quizQuestions = [];
let quizResults = {};

function enterQuizMode(questions) {
  quizMode = true;
  quizQuestions = questions;
  quizResults = {};
  filtered = questions;
  render();
  updateQuizBar();
  document.getElementById('quiz-bar').style.display = 'flex';
  document.getElementById('quiz-summary').style.display = 'none';
  document.getElementById('question-list').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function exitQuizMode() {
  quizMode = false;
  quizQuestions = [];
  quizResults = {};
  document.getElementById('quiz-bar').style.display = 'none';
  document.getElementById('quiz-summary').style.display = 'none';
  applyFilters();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateQuizBar() {
  const answered = Object.keys(quizResults).length;
  const total    = quizQuestions.length;
  document.getElementById('quiz-progress-text').textContent =
    `測驗模式　已答 ${answered} / ${total} 題`;
  const pct = total ? (answered / total * 100) : 0;
  document.getElementById('quiz-progress-bar').style.width = pct + '%';
}

function recordQuizResult(q, result) {
  quizResults[qid(q)] = result;
  updateQuizBar();
  if (Object.keys(quizResults).length === quizQuestions.length) {
    setTimeout(showQuizSummary, 600);
  }
}

function showQuizSummary() {
  const total   = quizQuestions.length;
  const correct = Object.values(quizResults).filter(v => v === 'correct').length;
  const wrong   = total - correct;
  const rate    = Math.round(correct / total * 100);

  // 儲存測驗紀錄
  const history = JSON.parse(localStorage.getItem('quizHistory') || '[]');
  history.unshift({ date: new Date().toLocaleDateString('zh-TW'), total, correct, rate });
  if (history.length > 10) history.pop();
  localStorage.setItem('quizHistory', JSON.stringify(history));
  renderQuizHistory();

  const summary = document.getElementById('quiz-summary');
  summary.innerHTML = `
    <div class="summary-card">
      <div class="summary-title">測驗結果</div>
      <div class="summary-stats">
        <div class="summary-stat summary-stat-correct">
          <div class="summary-num">${correct}</div>
          <div class="summary-label">答對</div>
        </div>
        <div class="summary-stat summary-stat-wrong">
          <div class="summary-num">${wrong}</div>
          <div class="summary-label">答錯</div>
        </div>
        <div class="summary-stat summary-stat-rate">
          <div class="summary-num">${rate}%</div>
          <div class="summary-label">答對率</div>
        </div>
      </div>
      <button onclick="exitQuizMode()" class="btn-secondary" style="margin-top:16px;width:100%">結束測驗</button>
    </div>`;
  summary.style.display = 'block';
  summary.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function init() {
  try {
    const res = await fetch('questions.json');
    if (!res.ok) throw new Error('無法載入');
    allQuestions = await res.json();
    setupFilters();
    applyFilters();
    updateProgressStats();
    renderQuizHistory();
    document.getElementById('loading').style.display = 'none';
  } catch {
    document.getElementById('loading').textContent =
      '⚠ 載入失敗。請先執行 parse_exams.py 產生 questions.json，' +
      '並用本機伺服器開啟（在 docs 資料夾執行：python -m http.server）。';
  }
}

/* ── Filters ── */

function setupFilters() {
  const get = key => [...new Set(allQuestions.map(q => q[key]))].sort();
  populate('filter-year',    get('年份'));
  populate('filter-session', get('考次'));
  populate('filter-subject', get('考科'));

  ['filter-year', 'filter-session', 'filter-subject', 'filter-status'].forEach(id =>
    document.getElementById(id).addEventListener('change', applyFilters));
  document.getElementById('search').addEventListener('input', applyFilters);
  document.getElementById('reset-btn').addEventListener('click', resetFilters);
  document.getElementById('random-btn').addEventListener('click', randomQuestion);
  document.getElementById('clear-progress-btn').addEventListener('click', clearProgress);
}

function populate(id, options) {
  const sel = document.getElementById(id);
  options.forEach(v => {
    const o = document.createElement('option');
    o.value = o.textContent = v;
    sel.appendChild(o);
  });
}

function applyFilters() {
  if (quizMode) return;
  const year    = document.getElementById('filter-year').value;
  const session = document.getElementById('filter-session').value;
  const subject = document.getElementById('filter-subject').value;
  const status  = document.getElementById('filter-status').value;
  const kw      = document.getElementById('search').value.trim().toLowerCase();

  filtered = allQuestions.filter(q => {
    if (year    && q['年份'] !== year)    return false;
    if (session && q['考次'] !== session) return false;
    if (subject && q['考科'] !== subject) return false;
    if (kw) {
      const haystack = [q['題目'], q['選項A'], q['選項B'], q['選項C'], q['選項D']]
        .join(' ').toLowerCase();
      if (!haystack.includes(kw)) return false;
    }
    if (status) {
      const p = progress[qid(q)];
      if (status === 'unanswered' && p)                return false;
      if (status === 'correct'    && p !== 'correct')  return false;
      if (status === 'wrong'      && p !== 'wrong')    return false;
      if (status === 'bookmarked' && !bookmarks[qid(q)]) return false;
    }
    return true;
  });

  render();
  document.getElementById('stats').textContent =
    `顯示 ${filtered.length} / ${allQuestions.length} 題`;
  document.getElementById('filter-stats').textContent =
    `共 ${filtered.length} 題`;
}

function randomQuestion() {
  if (!filtered.length) return;
  const count = Math.min(
    Math.max(1, parseInt(document.getElementById('random-count').value) || 1),
    filtered.length
  );
  const pool = [...filtered];
  const selected = [];
  for (let i = 0; i < count; i++) {
    const pick = Math.floor(Math.random() * pool.length);
    selected.push(pool.splice(pick, 1)[0]);
  }
  enterQuizMode(selected);
}

function resetFilters() {
  ['filter-year', 'filter-session', 'filter-subject', 'filter-status'].forEach(id =>
    document.getElementById(id).value = '');
  document.getElementById('search').value = '';
  applyFilters();
}

function clearProgress() {
  if (!confirm('確定要清除所有作答紀錄嗎？')) return;
  Object.keys(progress).forEach(k => delete progress[k]);
  localStorage.removeItem('progress');
  updateProgressStats();
  applyFilters();
}

/* ── Render ── */

function render() {
  const list = document.getElementById('question-list');
  if (!filtered.length) {
    list.innerHTML = '<div class="empty">沒有符合條件的題目</div>';
    return;
  }
  list.innerHTML = filtered.map((q, i) => cardHTML(q, i)).join('');
  // 測驗模式：展開所有題目，隱藏預覽
  if (quizMode) {
    filtered.forEach((q, i) => {
      const body = document.getElementById(`q${i}-body`);
      const icon = document.getElementById(`q${i}-icon`);
      const card = document.getElementById(`q${i}`);
      if (body) body.style.display = 'block';
      if (icon) icon.textContent = '▲';
      if (card) card.classList.add('expanded');
      const preview = card?.querySelector('.question-preview');
      if (preview) preview.style.display = 'none';
    });
  }
}

function cardHTML(q, i) {
  const id    = `q${i}`;
  const isMod = q['答案來源'] === '申覆後';
  const preview = stripHtml(q['題目']).replace(/\s+/g, ' ').slice(0, 55);
  const state = quizMode ? null : progress[qid(q)];
  const statusDot = state === 'correct' ? '<span class="dot dot-correct"></span>'
                  : state === 'wrong'   ? '<span class="dot dot-wrong"></span>'
                  : '';

  const ans = escAttr(q['正確答案']);
  const opts = ['A', 'B', 'C', 'D'].map(l => `
    <div class="option" id="${id}-${l}" onclick="selectOption('${id}','${l}','${ans}')">
      <span class="option-label">${l}</span>
      <span class="option-text">${renderText(q['選項' + l])}</span>
    </div>`).join('');

  const qidStr = qid(q);
  const bmStar = bookmarks[qidStr] ? '★' : '☆';

  return `
  <div class="question-card" id="${id}">
    <div class="question-header" onclick="toggle('${id}')">
      ${statusDot}
      <span class="question-meta">${q['年份']} ${q['考次']} ${q['考科']}</span>
      <span class="question-num">第 ${q['題號']} 題</span>
      ${isMod ? '<span class="badge-mod">申覆更正</span>' : ''}
      <button id="${id}-bm" class="bm-btn${bookmarks[qidStr] ? ' bm-active' : ''}" onclick="toggleBookmark(event,'${id}','${escAttr(qidStr)}')" title="收藏">${bmStar}</button>
      <span class="toggle-icon" id="${id}-icon">▼</span>
    </div>
    <div class="question-preview">${escHtml(preview)}${stripHtml(q['題目']).length > 55 ? '…' : ''}</div>
    <div class="question-body" id="${id}-body" style="display:none">
      <p class="question-text">${renderText(q['題目'])}</p>
      ${imgsHTML(q['圖片'])}
      <div class="options">${opts}</div>
      <div class="answer-reveal" id="${id}-ans" style="display:none"></div>
    </div>
  </div>`;
}

function toggle(id) {
  const body = document.getElementById(`${id}-body`);
  const icon = document.getElementById(`${id}-icon`);
  const card = document.getElementById(id);
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  icon.textContent   = open ? '▼' : '▲';
  card.classList.toggle('expanded', !open);

  if (!open) {
    const idx = parseInt(id.replace('q', ''));
    const q   = filtered[idx];
    if (q && !quizMode && progress[qid(q)]) restoreAnswer(id, q);
  }
}

function restoreAnswer(id, q) {
  const state  = progress[qid(q)];
  const answer = q['正確答案'];
  const correctLetters = answer.split('');

  correctLetters.forEach(l => {
    const el = document.getElementById(`${id}-${l}`);
    if (el) el.classList.add('correct');
  });
  ['A','B','C','D'].forEach(l => {
    const el = document.getElementById(`${id}-${l}`);
    if (el) el.style.cursor = 'default';
  });

  const div   = document.getElementById(`${id}-ans`);
  const isMod = div.closest('.question-card').querySelector('.badge-mod');
  div.style.display = 'flex';
  div.className = 'answer-reveal ' + (state === 'correct' ? 'answer-correct' : 'answer-wrong');
  div.innerHTML = state === 'correct'
    ? `✓ 答對了！正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '')
    : `✗ 答錯了。正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '');
  showNoteBox(id, qid(q));
}

function selectOption(id, chosen, answer) {
  if (document.getElementById(`${id}-ans`).style.display !== 'none') return;

  const correctLetters = answer.split('');
  const isCorrect = correctLetters.includes(chosen);

  const chosenEl = document.getElementById(`${id}-${chosen}`);
  if (chosenEl) chosenEl.classList.add(isCorrect ? 'correct' : 'wrong');

  if (!isCorrect) {
    correctLetters.forEach(l => {
      const el = document.getElementById(`${id}-${l}`);
      if (el) el.classList.add('correct');
    });
  }

  ['A','B','C','D'].forEach(l => {
    const el = document.getElementById(`${id}-${l}`);
    if (el) el.style.cursor = 'default';
  });

  const div   = document.getElementById(`${id}-ans`);
  const isMod = div.closest('.question-card').querySelector('.badge-mod');
  div.style.display = 'flex';
  div.className = 'answer-reveal ' + (isCorrect ? 'answer-correct' : 'answer-wrong');
  div.innerHTML = isCorrect
    ? `✓ 答對了！正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '')
    : `✗ 答錯了。正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '');

  const idx = parseInt(id.replace('q', ''));
  const q   = filtered[idx];
  if (q) {
    saveProgress(q, isCorrect ? 'correct' : 'wrong');
    showNoteBox(id, qid(q));
    if (quizMode) {
      recordQuizResult(q, isCorrect ? 'correct' : 'wrong');
    } else {
      const card = document.getElementById(id);
      const dot  = card.querySelector('.dot');
      if (dot) {
        dot.className = 'dot ' + (isCorrect ? 'dot-correct' : 'dot-wrong');
      } else {
        const header = card.querySelector('.question-header');
        const newDot = document.createElement('span');
        newDot.className = 'dot ' + (isCorrect ? 'dot-correct' : 'dot-wrong');
        header.insertBefore(newDot, header.firstChild);
      }
    }
  }
}

function imgsHTML(imgs) {
  if (!imgs || !imgs.length) return '';
  return '<div class="question-images">' +
    imgs.map(src => `<img src="${escAttr(src)}" alt="題目圖片" class="question-img" onclick="this.classList.toggle('zoomed')">`).join('') +
    '</div>';
}

/* ── Utilities ── */

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderText(s) {
  return String(s).split(/(<\/?(?:sup|sub)>)/).map(part =>
    /^<\/?(?:sup|sub)>$/.test(part) ? part : escHtml(part)
  ).join('');
}

function stripHtml(s) {
  return String(s).replace(/<\/?(?:sup|sub)>/g, '');
}

function escAttr(s) {
  return String(s).replace(/'/g, '&#39;');
}

init();
