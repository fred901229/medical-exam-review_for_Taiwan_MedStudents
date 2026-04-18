let allQuestions = [];
let filtered = [];

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
  const preview = q['題目'].replace(/\s+/g, ' ').slice(0, 55);

  const opts = ['A', 'B', 'C', 'D'].map(l => `
    <div class="option" id="${id}-${l}">
      <span class="option-label">${l}</span>
      <span class="option-text">${escHtml(q['選項' + l])}</span>
    </div>`).join('');

  return `
  <div class="question-card" id="${id}">
    <div class="question-header" onclick="toggle('${id}')">
      <span class="question-meta">${q['年份']} ${q['考次']} ${q['考科']}</span>
      <span class="question-num">第 ${q['題號']} 題</span>
      ${isMod ? '<span class="badge-mod">申覆更正</span>' : ''}
      <span class="toggle-icon" id="${id}-icon">▼</span>
    </div>
    <div class="question-preview">${escHtml(preview)}${q['題目'].length > 55 ? '…' : ''}</div>
    <div class="question-body" id="${id}-body" style="display:none">
      <p class="question-text">${escHtml(q['題目'])}</p>
      <div class="options">${opts}</div>
      <div class="answer-section">
        <button class="btn-answer" id="${id}-btn" onclick="reveal('${id}','${escAttr(q['正確答案'])}')">
          顯示答案
        </button>
        <div class="answer-reveal" id="${id}-ans" style="display:none"></div>
      </div>
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

function reveal(id, answer) {
  const btn = document.getElementById(`${id}-btn`);
  const div = document.getElementById(`${id}-ans`);
  btn.style.display = 'none';
  div.style.display = 'flex';

  const letters = answer.split('');
  letters.forEach(l => {
    const el = document.getElementById(`${id}-${l}`);
    if (el) el.classList.add('correct');
  });

  const isMod = div.closest('.question-card').querySelector('.badge-mod');
  div.innerHTML =
    `正確答案：<strong>${escHtml(answer)}</strong>` +
    (isMod ? ' <span class="badge-mod-small">申覆更正</span>' : '');
}

/* ── Utilities ── */

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function escAttr(s) {
  return String(s).replace(/'/g, '&#39;');
}

init();
