function fmtA(n) {
  if (n >= 1e9) return '$' + (n/1e9).toFixed(1) + 'B';
  if (n >= 1e6) return '$' + (n/1e6).toFixed(0) + 'M';
  return '$' + n.toLocaleString();
}

let fData = [], fSearch = '', fFilter = 'all';

function drawDonut(canvasId, compliant, total) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d', {willReadFrequently: true});
  const dpr = window.devicePixelRatio || 1;
  canvas.width = 200 * dpr;
  canvas.height = 200 * dpr;
  canvas.style.width = '200px';
  canvas.style.height = '200px';
  ctx.scale(dpr, dpr);
  const cx = 100, cy = 100;
  const r = 78, inner = r * 0.58;
  const pct = compliant / total;
  const TAU = Math.PI * 2, start = -Math.PI / 2;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(cx, cy, r, start + pct * TAU, start + TAU);
  ctx.arc(cx, cy, inner, start + TAU, start + pct * TAU, true);
  ctx.closePath(); ctx.fillStyle = '#c0392b'; ctx.fill();
  ctx.beginPath();
  ctx.arc(cx, cy, r, start, start + pct * TAU);
  ctx.arc(cx, cy, inner, start + pct * TAU, start, true);
  ctx.closePath(); ctx.fillStyle = '#4a8a62'; ctx.fill();
  ctx.beginPath();
  ctx.arc(cx, cy, inner * 0.88, 0, TAU);
  ctx.fillStyle = '#f3ece0'; ctx.fill();
  ctx.fillStyle = '#1a1a16';
  ctx.font = 'bold ' + Math.round(cx * 0.32) + 'px Georgia, serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(Math.round((compliant/total)*100) + '%', cx, cy - cx * 0.06);
  ctx.font = Math.round(cx * 0.14) + 'px system-ui, sans-serif';
  ctx.fillStyle = '#807868';
  ctx.fillText('compliant', cx, cy + cx * 0.18);
}

function renderSummary() {
  const total = fData.length;
  const compliant = fData.filter(f => f.compliant).length;
  const nc = total - compliant;
  const shortfall = fData.filter(f => !f.compliant).reduce((s,f) => s + (f.required - f.qualifying), 0);
  const totalAssets = fData.reduce((s,f) => s + f.assets, 0);
  const el = document.getElementById('foundation-visual');
  if (!el) return;
  el.innerHTML =
    '<div class="fv-donut-wrap"><canvas id="donut-canvas" width="200" height="200"></canvas></div>' +
    '<div class="fv-stats">' +
    '<div class="fv-stat"><div class="fv-stat-value">' + total.toLocaleString() + '</div><div class="fv-stat-label">foundations tracked</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value" style="color:#c0392b">' + nc.toLocaleString() + '</div><div class="fv-stat-label">below legal 5% minimum</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value" style="color:#c0392b">' + fmtA(shortfall) + '</div><div class="fv-stat-label">undistributed vs legal minimum</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value">' + fmtA(totalAssets) + '</div><div class="fv-stat-label">total assets tracked</div></div></div>' +
    '<div class="fv-legend"><div class="fv-legend-item"><span class="fv-dot green"></span> Meeting 5%</div>' +
    '<div class="fv-legend-item"><span class="fv-dot red"></span> Below 5%</div>' +
    '<div class="fv-legend-note">Based on most recent 990-PF filing via IRS public data</div></div>';
  setTimeout(function() { drawDonut('donut-canvas', compliant, total); }, 50);
}

function renderFoundations() {
  const list = document.getElementById('foundation-list');
  if (!list) return;
  let filtered = fData.filter(f => {
    if (fFilter === 'compliant' && !f.compliant) return false;
    if (fFilter === 'noncompliant' && f.compliant) return false;
    if (fSearch && f.name.toLowerCase().indexOf(fSearch) === -1) return false;
    return true;
  });
  filtered.sort((a,b) => a.pct - b.pct);
  if (!filtered.length) {
    list.innerHTML = '<p style="color:rgba(240,232,216,0.4);padding:40px 0;text-align:center;">No foundations match.</p>';
    return;
  }
  list.innerHTML = filtered.map(f => {
    const good = f.compliant;
    const sf = !good ? fmtA(f.required - f.qualifying) : null;
    const yr = f.year ? 'Most recent 990: ' + f.year : '';
    return '<div class="foundation-card ' + (good ? 'compliant' : 'noncompliant') + '">' +
      '<div class="foundation-info">' +
      '<div class="foundation-name">' + f.name + '</div>' +
      '<div class="foundation-meta">' + fmtA(f.assets) + ' in assets' +
      (yr ? ' &middot; <span class="year-tag">' + yr + '</span>' : '') +
      (!good ? ' &middot; <strong style="color:#c0392b">' + sf + ' short</strong>' : '') +
      '</div></div>' +
      '<div class="foundation-stats">' +
      '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.qualifying) + '</div><div class="foundation-stat-label">distributed</div></div>' +
      '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.required) + '</div><div class="foundation-stat-label">required (5%)</div></div>' +
      '<div class="foundation-stat"><div class="payout-rate ' + (good ? 'good' : 'bad') + '">' + f.pct + '%</div>' +
      '<div class="compliance-badge ' + (good ? 'good' : 'bad') + '">' + (good ? '✓ Compliant' : '✗ Below 5%') + '</div></div>' +
      '</div></div>';
  }).join('');
}

document.querySelectorAll('.nav-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

const fs = document.getElementById('foundation-search');
if (fs) fs.addEventListener('input', e => { fSearch = e.target.value.toLowerCase().trim(); renderFoundations(); });

document.querySelectorAll('[data-compliance]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-compliance]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    fFilter = btn.dataset.compliance;
    renderFoundations();
  });
});

fetch('foundations.json').then(r => r.json()).then(data => { fData = data; renderSummary(); renderFoundations(); });
