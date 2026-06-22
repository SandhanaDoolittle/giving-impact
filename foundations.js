function fmtA(n) {
  if (n >= 1e9) return '$' + (n/1e9).toFixed(1) + 'B';
  if (n >= 1e6) return '$' + (n/1e6).toFixed(0) + 'M';
  if (n >= 1e3) return '$' + Math.round(n/1e3) + 'K';
  return '$' + n.toLocaleString();
}

var fData = [], gData = {}, fSearch = '', fFilter = 'all';

function drawDonut(canvasId, compliant, total) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var dpr = window.devicePixelRatio || 1;
  canvas.width = 200 * dpr; canvas.height = 200 * dpr;
  canvas.style.width = '200px'; canvas.style.height = '200px';
  ctx.scale(dpr, dpr);
  var cx = 100, cy = 100, r = 78, inner = r * 0.58;
  var pct = compliant / total;
  var TAU = Math.PI * 2, start = -Math.PI / 2;
  ctx.clearRect(0, 0, 200, 200);
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
  ctx.font = 'bold 32px Georgia, serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(Math.round((compliant/total)*100) + '%', cx, cy - 6);
  ctx.font = '14px system-ui, sans-serif';
  ctx.fillStyle = '#807868';
  ctx.fillText('compliant', cx, cy + 18);
}

function renderSummary() {
  var total = fData.length;
  var compliant = fData.filter(function(f) { return f.compliant; }).length;
  var nc = total - compliant;
  var shortfall = fData.filter(function(f) { return !f.compliant; }).reduce(function(s,f) { return s + (f.required - f.qualifying); }, 0);
  var totalAssets = fData.reduce(function(s,f) { return s + f.assets; }, 0);
  var el = document.getElementById('foundation-visual');
  if (!el) return;
  el.innerHTML =
    '<div class="fv-donut-wrap"><canvas id="donut-canvas" width="200" height="200"></canvas></div>' +
    '<div class="fv-stats">' +
    '<div class="fv-stat"><div class="fv-stat-value">' + total.toLocaleString() + '</div><div class="fv-stat-label">foundations tracked</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value" style="color:#c0392b">' + nc.toLocaleString() + '</div><div class="fv-stat-label">below legal 5% minimum</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value" style="color:#c0392b">' + fmtA(shortfall) + '</div><div class="fv-stat-label">undistributed vs legal minimum</div></div>' +
    '<div class="fv-stat"><div class="fv-stat-value">' + fmtA(totalAssets) + '</div><div class="fv-stat-label">total assets tracked</div></div>' +
    '</div>' +
    '<div class="fv-legend"><div class="fv-legend-item"><span class="fv-dot green"></span> Meeting 5%</div>' +
    '<div class="fv-legend-item"><span class="fv-dot red"></span> Below 5%</div>' +
    '<div class="fv-legend-note">Based on most recent 990-PF filing via IRS public data</div></div>';
  setTimeout(function() { drawDonut('donut-canvas', compliant, total); }, 50);
}

function confidenceBadge(conf) {
  if (conf === 'high')   return '<span class="conf-badge conf-high">verified</span>';
  if (conf === 'medium') return '<span class="conf-badge conf-medium">sourced</span>';
  if (conf === 'low')    return '<span class="conf-badge conf-low">est.</span>';
  return '';
}

function grantPanel(ein) {
  var g = gData[ein];
  if (!g || !g.matched_detail || g.matched_detail.length === 0) return '';
  var matchPct = g.match_pct || 0;
  var top = g.matched_detail.slice(0, 5);
  return '<div class="grant-panel">' +
    '<div class="grant-panel-header">' +
      '<span class="grant-panel-title">Grant Impact</span>' +
      '<span class="grant-match-pct">' + matchPct + '% of grants matched to impact data</span>' +
    '</div>' +
    '<div class="grant-list">' +
    top.map(function(grant) {
      var typeLabel = grant.recipient_type === 'university' ? '🎓 University' :
                      grant.recipient_type === 'intermediary' ? '↪ Re-grantor' : '';
      return '<div class="grant-row">' +
        '<div class="grant-row-left">' +
          '<div class="grant-recipient">' + grant.recipient + '</div>' +
          (typeLabel ? '<span class="grant-type-tag">' + typeLabel + '</span>' : '') +
          (grant.metric_unit ? '<div class="grant-metric">' + grant.metric_unit + '</div>' : '') +
        '</div>' +
        '<div class="grant-row-right">' +
          '<div class="grant-amount">' + fmtA(grant.amount) + '</div>' +
          confidenceBadge(grant.confidence) +
        '</div>' +
      '</div>';
    }).join('') +
    (g.matched_detail.length > 5 ? '<div class="grant-more">+ ' + (g.matched_detail.length - 5) + ' more matched grants</div>' : '') +
    '</div></div>';
}

function renderFoundations() {
  var list = document.getElementById('foundation-list');
  if (!list) return;
  var filtered = fData.filter(function(f) {
    if (fFilter === 'compliant' && !f.compliant) return false;
    if (fFilter === 'noncompliant' && f.compliant) return false;
    if (fSearch && f.name.toLowerCase().indexOf(fSearch) === -1) return false;
    return true;
  });
  filtered.sort(function(a, b) { return a.pct - b.pct; });
  if (!filtered.length) {
    list.innerHTML = '<p style="color:rgba(240,232,216,0.4);padding:40px 0;text-align:center;">No foundations match.</p>';
    return;
  }
  list.innerHTML = filtered.map(function(f) {
    var good = f.compliant;
    var sf = !good ? fmtA(f.required - f.qualifying) : null;
    var yr = f.year ? 'Most recent 990: ' + f.year : '';
    var grants = grantPanel(f.ein);
    return '<div class="foundation-card ' + (good ? 'compliant' : 'noncompliant') + '">' +
      '<div class="foundation-card-main">' +
        '<div class="foundation-info">' +
          '<div class="foundation-name">' + f.name + '</div>' +
          '<div class="foundation-meta">' + fmtA(f.assets) + ' in assets' +
          (yr ? ' &middot; <span class="year-tag">' + yr + '</span>' : '') +
          (!good ? ' &middot; <strong style="color:#c0392b">' + sf + ' short</strong>' : '') +
          '</div>' +
        '</div>' +
        '<div class="foundation-stats">' +
          '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.qualifying) + '</div><div class="foundation-stat-label">distributed</div></div>' +
          '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.required) + '</div><div class="foundation-stat-label">required (5%)</div></div>' +
          '<div class="foundation-stat">' +
            '<div class="payout-rate ' + (good ? 'good' : 'bad') + '">' + f.pct + '%</div>' +
            '<div class="compliance-badge ' + (good ? 'good' : 'bad') + '">' + (good ? '✓ Compliant' : '✗ Below 5%') + '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      grants +
    '</div>';
  }).join('');
}

document.querySelectorAll('.nav-tab').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.nav-tab').forEach(function(b) { b.classList.remove('active'); });
    document.querySelectorAll('.tab-content').forEach(function(t) { t.classList.remove('active'); });
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

var fsEl = document.getElementById('foundation-search');
if (fsEl) fsEl.addEventListener('input', function(e) { fSearch = e.target.value.toLowerCase().trim(); renderFoundations(); });

document.querySelectorAll('[data-compliance]').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('[data-compliance]').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    fFilter = btn.dataset.compliance;
    renderFoundations();
  });
});

var chunkFetches = [fetch('foundations.json').then(function(r) { return r.json(); })];
for (var i = 0; i < 8; i++) {
  chunkFetches.push(
    fetch('foundation_grants_' + i + '.json')
      .then(function(r) { return r.json(); })
      .catch(function() { return []; })
  );
}
Promise.all(chunkFetches).then(function(results) {
  fData = results[0];
  for (var i = 1; i < results.length; i++) {
    results[i].forEach(function(g) { gData[g.ein] = g; });
  }
  console.log('Loaded', fData.length, 'foundations and', Object.keys(gData).length, 'grant records');
  renderSummary();
  renderFoundations();
});
