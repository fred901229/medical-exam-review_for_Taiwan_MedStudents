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

async function init() {
  try {
    const res = await fetch('questions.json');
    if (!res.ok) throw new Error('無法載入');
    allQuestions = await res.json();
    setupFilters();
    applyFilters();
    document.getElementById('loading').style.display = 'none';
  } catch {
    document.getElementById('loading').textContent =
      '⚠ 載入失敗。請先執行 parse_exams.py 產生 questions.json，' +
      '並用本機伺服器開啟（在 website 資料夾執行：python -m http.server）。';
  }
}

/* ── Filters ── */

function setupFilters() {
  const get = key => [...new Set(allQuestions.map(q => q[key]))].sort();
  populate('filter-year',    get('年份'));
  populate('filter-session', get('考次'));
  populate('filter-subject', get('考科'));

  ['filter-year', 'filter-session', 'filter-subject'].forEach(id =>
    document.getElementById(id).addEventListener('change', applyFilters));
  document.getElementById('search').addEventListener('input', applyFilters);
  document.getElementById('reset-btn').addEventListener('click', resetFilters);
  document.getElementById('random-btn').addEventListener('click', randomQuestion);
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
  const year    = document.getElementById('filter-year').value;
  const session = document.getElementById('filter-session').value;
  const subject = document.getElementById('filter-subject').value;
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
  const idx = Math.floor(Math.random() * filtered.length);
  const id = `q${idx}`;
  const body = document.getElementById(`${id}-body`);
  if (body && body.style.display === 'none') toggle(id);
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function resetFilters() {
  ['filter-year', 'filter-session', 'filter-subject'].forEach(id =>
    document.getElementById(id).value = '');
  document.getElementById('search').value = '';
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
}

function cardHTML(q, i) {
  const id   = `q${i}`;
  const isMod = q['答案來源'] === '申覆後';
  const preview = stripHtml(q['題目']).replace(/\s+/g, ' ').slice(0, 55);

  const ans = escAttr(q['正確答案']);
  const opts = ['A', 'B', 'C', 'D'].map(l => `
    <div class="option" id="${id}-${l}" onclick="selectOption('${id}','${l}','${ans}')">
      <span class="option-label">${l}</span>
      <span class="option-text">${renderText(q['選項' + l])}</span>
    </div>`).join('');

  return `
  <div class="question-card" id="${id}">
    <div class="question-header" onclick="toggle('${id}')">
      <span class="question-meta">${q['年份']} ${q['考次']} ${q['考科']}</span>
      <span class="question-num">第 ${q['題號']} 題</span>
      ${isMod ? '<span class="badge-mod">申覆更正</span>' : ''}
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
}

function selectOption(id, chosen, answer) {
  // 已作答則不重複處理
  if (document.getElementById(`${id}-ans`).style.display !== 'none') return;

  const correctLetters = answer.split('');
  const isCorrect = correctLetters.includes(chosen);

  // 標記選到的選項
  const chosenEl = document.getElementById(`${id}-${chosen}`);
  if (chosenEl) chosenEl.classList.add(isCorrect ? 'correct' : 'wrong');

  // 若答錯，另外標出正確選項
  if (!isCorrect) {
    correctLetters.forEach(l => {
      const el = document.getElementById(`${id}-${l}`);
      if (el) el.classList.add('correct');
    });
  }

  // 讓所有選項變成不可點擊
  ['A','B','C','D'].forEach(l => {
    const el = document.getElementById(`${id}-${l}`);
    if (el) el.style.cursor = 'default';
  });

  // 顯示結果
  const div = document.getElementById(`${id}-ans`);
  const isMod = div.closest('.question-card').querySelector('.badge-mod');
  div.style.display = 'flex';
  div.className = 'answer-reveal ' + (isCorrect ? 'answer-correct' : 'answer-wrong');
  div.innerHTML = isCorrect
    ? `✓ 答對了！正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '')
    : `✗ 答錯了。正確答案：<strong>${escHtml(answer)}</strong>` +
      (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '');
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
