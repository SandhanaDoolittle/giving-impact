function fmtA(n) {
  if (n >= 1e12) return '$' + (n/1e12).toFixed(1) + 'T';
  if (n >= 1e9) return '$' + (n/1e9).toFixed(1) + 'B';
  if (n >= 1e6) return '$' + (n/1e6).toFixed(0) + 'M';
  if (n >= 1e3) return '$' + Math.round(n/1e3) + 'K';
  return '$' + n.toLocaleString();
}

var SMALL_WORDS = {a:1,an:1,and:1,at:1,but:1,by:1,for:1,in:1,nor:1,of:1,on:1,or:1,so:1,the:1,to:1,up:1,yet:1,c:1,'c/o':1};
function toTitle(str) {
  if (!str) return str;
  return str.toLowerCase().replace(/[^\s-]+/g, function(word, idx) {
    return (idx > 0 && SMALL_WORDS[word]) ? word : word.charAt(0).toUpperCase() + word.slice(1);
  });
}

var fData = [], gData = {}, sData = {}, fSearch = '', fFilter = 'all';

// actualRate(f): annualized % of assets actually distributed.
// f.pct = qualifying/required * 100 works when required > 0, but operating foundations
// and some edge cases have required=0, producing pct=0. Fall back to qualifying/assets
// directly so every foundation shows a meaningful rate.
function actualRate(f) {
  var yrs = f.years_used || 1;
  if (f.assets > 0) return Math.round((f.qualifying / f.assets / yrs) * 10000) / 100;
  return 0;
}

function drawDonut(canvasId, filled, total, opts) {
  opts = opts || {};
  var colorGood = opts.colorGood || '#4a8a62';
  var colorBad  = opts.colorBad  || '#c0392b';
  var label     = opts.label     || 'COMPLIANT';
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var dpr = window.devicePixelRatio || 1;
  canvas.width = 200 * dpr; canvas.height = 200 * dpr;
  canvas.style.width = '200px'; canvas.style.height = '200px';
  ctx.scale(dpr, dpr);
  var cx = 100, cy = 100, r = 78, inner = r * 0.58;
  var pct = filled / total;
  var TAU = Math.PI * 2, start = -Math.PI / 2;
  ctx.clearRect(0, 0, 200, 200);
  ctx.beginPath();
  ctx.arc(cx, cy, r, start + pct * TAU, start + TAU);
  ctx.arc(cx, cy, inner, start + TAU, start + pct * TAU, true);
  ctx.closePath(); ctx.fillStyle = colorBad; ctx.fill();
  ctx.beginPath();
  ctx.arc(cx, cy, r, start, start + pct * TAU);
  ctx.arc(cx, cy, inner, start + pct * TAU, start, true);
  ctx.closePath(); ctx.fillStyle = colorGood; ctx.fill();
  ctx.beginPath();
  ctx.arc(cx, cy, inner * 0.88, 0, TAU);
  ctx.fillStyle = '#f3ece0'; ctx.fill();
  ctx.fillStyle = '#2c5540';
  ctx.font = '28px "DM Serif Display", Georgia, serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(Math.round((filled/total)*100) + '%', cx, cy - 7);
  ctx.font = '600 9px "DM Sans", system-ui, sans-serif';
  ctx.fillStyle = '#aca898';
  ctx.fillText(label, cx, cy + 16);
}

function renderSummary() {
  // Exclude operating foundations — they're judged by an income test, not the 5% asset rule
  var grantmaking = fData.filter(function(f) { return !f.operating_foundation; });
  var total = grantmaking.length;
  var compliant = grantmaking.filter(function(f) { return f.compliant; }).length;
  var nc = total - compliant;
  var shortfall = grantmaking.filter(function(f) { return !f.compliant; }).reduce(function(s,f) { return s + (f.required - f.qualifying); }, 0);
  var totalAssets = fData.reduce(function(s,f) { return s + f.assets; }, 0);

  // Grant transparency: foundations with at least one named recipient in their filing
  var withAnyGrant = grantmaking.filter(function(f) {
    var g = gData[f.ein];
    return g && g.top_grants && g.top_grants.length > 0;
  }).length;

  // Matched grants: foundations with at least one grant matched to our impact database
  var withMatched = grantmaking.filter(function(f) {
    var g = gData[f.ein];
    return g && g.matched_detail && g.matched_detail.length > 0;
  }).length;

  var el = document.getElementById('foundation-visual');
  if (!el) return;
  el.innerHTML =
    '<div class="fv-donuts">' +
      '<div class="fv-donut-wrap"><canvas id="donut-canvas" width="200" height="200"></canvas>' +
        '<div class="fv-donut-label">Compliance</div></div>' +
      '<div class="fv-donut-wrap"><canvas id="donut-canvas-2" width="200" height="200"></canvas>' +
        '<div class="fv-donut-label">Grant Transparency</div></div>' +
      '<div class="fv-donut-wrap"><canvas id="donut-canvas-3" width="200" height="200"></canvas>' +
        '<div class="fv-donut-label">Impact Matched</div></div>' +
    '</div>' +
    '<div class="fv-stats">' +
      '<div class="fv-stat"><div class="fv-stat-value">' + total.toLocaleString() + '</div><div class="fv-stat-label">grantmaking foundations tracked</div></div>' +
      '<div class="fv-stat"><div class="fv-stat-value" style="color:#c07840">' + nc.toLocaleString() + '</div><div class="fv-stat-label">below legal 5% minimum</div></div>' +
      '<div class="fv-stat"><div class="fv-stat-value" style="color:#c07840">' + fmtA(shortfall) + '</div><div class="fv-stat-label">undistributed vs legal minimum</div></div>' +
      '<div class="fv-stat"><div class="fv-stat-value">' + fmtA(totalAssets) + '</div><div class="fv-stat-label">total assets tracked</div></div>' +
      '<div class="fv-stat"><div class="fv-stat-value">' + withMatched.toLocaleString() + '</div><div class="fv-stat-label">foundations with grants matched to impact data</div></div>' +
    '</div>' +
    '<div class="fv-legend">' +
      '<div class="fv-legend-note">Compliance excludes operating foundations (museums, research institutes, etc.) which are judged by an income test, not the 5% asset rule. Reflects a 5-year rolling average of qualifying distributions vs. the IRC §4942 minimum. Grant transparency = disclosed at least one named recipient in their public 990-PF. Impact matched = at least one recipient in our outcome database. Source: IRS 990-PF via ProPublica.</div>' +
    '</div>';
  setTimeout(function() {
    var opts = { colorGood: '#4a8a62', colorBad: '#c8bfb4' };
    drawDonut('donut-canvas', compliant, total, Object.assign({}, opts, { label: 'COMPLIANT' }));
    drawDonut('donut-canvas-2', withAnyGrant, total, Object.assign({}, opts, { label: 'TRANSPARENT' }));
    drawDonut('donut-canvas-3', withMatched, total, Object.assign({}, opts, { label: 'MATCHED' }));
  }, 50);
}

function renderRankings() {
  var el = document.getElementById('foundation-summary');
  if (!el) return;
  // Exclude flow-through foundations (funded by fresh annual injections from a parent
  // company/family rather than a real investment endowment — e.g. ExxonMobil Foundation,
  // Ford Motor Company Fund) since "% of assets" is structurally meaningless for them.
  // The pct <= 500 cap is a secondary safety net for anything the flow-through check misses
  // (e.g. pharma "patient assistance" foundations passing through in-kind drug donations).
  var sizable = fData.filter(function(f) { return f.assets >= 100000000 && f.pct <= 500 && !f.flow_through; });

  var mostGenerous = sizable.slice().sort(function(a, b) { return actualRate(b) - actualRate(a); }).slice(0, 10);
  var biggestShortfalls = fData.filter(function(f) { return !f.compliant; }).slice()
    .sort(function(a, b) { return (b.required - b.qualifying) - (a.required - a.qualifying); })
    .slice(0, 10);

  function rankRow(f, idx, valueHtml) {
    return '<div class="ranking-row">' +
      '<span class="ranking-num">' + (idx + 1) + '</span>' +
      '<span class="ranking-name">' + toTitle(f.name) + '</span>' +
      '<span class="ranking-value">' + valueHtml + '</span>' +
    '</div>';
  }

  el.innerHTML =
    '<div class="ranking-col">' +
      '<div class="ranking-title">Most Generous <span class="ranking-sub">% of legal minimum given, $100M+ assets</span></div>' +
      mostGenerous.map(function(f, i) { return rankRow(f, i, actualRate(f) + '% of assets'); }).join('') +
    '</div>' +
    '<div class="ranking-col">' +
      '<div class="ranking-title">Biggest Shortfalls <span class="ranking-sub">dollars below the legal minimum, 5-yr</span></div>' +
      biggestShortfalls.map(function(f, i) { return rankRow(f, i, fmtA(f.required - f.qualifying) + ' short'); }).join('') +
    '</div>';

  renderPriorityRanking();
  renderEffectivenessRanking();
}

function renderEffectivenessRanking() {
  var el = document.getElementById('foundation-effectiveness');
  if (!el) return;

  // Only rank foundations where we actually have matched grant data — if we
  // don't have complete impact data for their grants, they don't appear here.
  // Require ≥$1M in matched dollars so a single small grant doesn't skew the %.
  var MIN_DOLLARS = 1000000;
  var ranked = fData
    .map(function(f) { return { f: f, s: sData[f.ein] }; })
    .filter(function(x) {
      return x.s &&
             x.s.documentation_score > 0 &&
             x.s.documentation_dollars_basis >= MIN_DOLLARS;
    })
    .sort(function(a, b) {
      return (b.s.documentation_score - a.s.documentation_score) ||
             (b.s.documentation_dollars_basis - a.s.documentation_dollars_basis);
    })
    .slice(0, 10);

  if (!ranked.length) { el.innerHTML = ''; return; }

  el.innerHTML =
    '<div class="ranking-title">Most Grants to Impact-Verified Organizations' +
      '<span class="ranking-sub">% of grant dollars matched to orgs with published impact metrics — foundations with no data are excluded</span>' +
    '</div>' +
    ranked.map(function(x, i) {
      var pct = Math.round(x.s.documentation_score * 100);
      var basis = fmtA(x.s.documentation_dollars_basis) + ' matched';
      return '<div class="ranking-row">' +
        '<span class="ranking-num">' + (i + 1) + '</span>' +
        '<span class="ranking-name">' + toTitle(x.f.name) + '</span>' +
        '<span class="ranking-value">' + pct + '% of grants' +
          '<div class="ranking-subvalue">' + basis + '</div>' +
        '</span>' +
      '</div>';
    }).join('') +
    '<div class="foundation-priority-note">Only foundations with at least $1M in grants matched to our impact database appear here. A higher % means more of their grant dollars flow to organizations where we can independently verify real-world outcomes from published 990 filings and program reports.</div>';
}

function renderPriorityRanking() {
  var el = document.getElementById('foundation-priority');
  if (!el) return;

  // importance_score comes from compute_efficiency_scores.py: a dollar-weighted
  // average of how important the public rates the causes this foundation's matched
  // grants actually went to (Rethink Priorities' Pulse survey, 0-10 scale). Only
  // "ok" status foundations have enough matched dollars in a Pulse-covered cause
  // (currently just health/environment/animal_welfare) to be meaningfully scored --
  // everything else is correctly left out rather than guessed at.
  var ranked = fData
    .map(function(f) { return { f: f, s: sData[f.ein] }; })
    .filter(function(x) { return x.s && x.s.importance_status === 'ok'; })
    .sort(function(a, b) {
      return (b.s.importance_score - a.s.importance_score) || (b.s.importance_dollars_basis - a.s.importance_dollars_basis);
    })
    .slice(0, 10);

  if (!ranked.length) { el.innerHTML = ''; return; }

  el.innerHTML =
    '<div class="ranking-title">Funding the Causes Rated Most Important' +
      '<span class="ranking-sub">dollar-weighted public-importance rating of matched grants, 0&ndash;10 scale</span>' +
    '</div>' +
    ranked.map(function(x, i) {
      var doc = x.s.documentation_score != null ? Math.round(x.s.documentation_score * 100) + '% documented' : '';
      return '<div class="ranking-row">' +
        '<span class="ranking-num">' + (i + 1) + '</span>' +
        '<span class="ranking-name">' + toTitle(x.f.name) + '</span>' +
        '<span class="ranking-value">' + x.s.importance_score.toFixed(2) + '/10' +
          (doc ? '<div class="ranking-subvalue">' + doc + '</div>' : '') +
        '</span>' +
      '</div>';
    }).join('') +
    '<div class="foundation-priority-note">Based on a public survey (Rethink Priorities’ Pulse, ~5,000 US adults) rating how important different causes are to address. Currently only covers grants to health, environment, and animal welfare causes — more cause areas will appear here once our own supplementary survey results are in.</div>';
}

function confidenceBadge(conf) {
  if (conf === 'high')   return '<span class="conf-badge conf-high">verified</span>';
  if (conf === 'medium') return '<span class="conf-badge conf-medium">sourced</span>';
  if (conf === 'low')    return '<span class="conf-badge conf-low">est.</span>';
  return '';
}

var UNRESOLVABLE_LABELS = {
  form_artifact:           { label: 'Form artifact',            title: '990-PF form placeholder — no specific recipient was named in the filing' },
  daf_regrant:             { label: 'DAF / Community Fdn',      title: 'Donor-advised fund or community foundation — the final nonprofit recipient is not disclosed' },
  foundation_to_foundation:{ label: 'Foundation-to-Foundation', title: 'Recipient is itself a private grantmaking foundation that files its own 990-PF' },
};

function grantPanel(ein) {
  var g = gData[ein];
  if (!g) return '';
  var hasMatched = g.matched_detail && g.matched_detail.length > 0;
  var hasTop = g.top_grants && g.top_grants.length > 0;
  if (!hasMatched && !hasTop) return '';

  var matchPct = g.match_pct || 0;

  // ── Matched grants ─────────────────────────────────────────────────────────
  // Collapse exact repeats (same recipient+amount+purpose listed multiple times
  // in the raw 990-PF filing — verified real phenomenon, not a parse artifact).
  var grouped = [];
  var byKey = {};
  (g.matched_detail || []).forEach(function(grant) {
    var key = grant.recipient + '|' + grant.amount + '|' + grant.purpose;
    if (byKey[key]) {
      byKey[key].count++;
      byKey[key].amount += grant.amount;
    } else {
      var copy = {};
      for (var k in grant) copy[k] = grant[k];
      copy.count = 1;
      byKey[key] = copy;
      grouped.push(copy);
    }
  });

  var topMatched = grouped.slice(0, 5);
  var matchedHtml = topMatched.map(function(grant) {
    var typeLabel = grant.recipient_type === 'university' ? '🎓 University' :
                    grant.recipient_type === 'intermediary' ? '↪ Re-grantor' : '';
    return '<div class="grant-row">' +
      '<div class="grant-row-left">' +
        '<div class="grant-recipient">' + grant.recipient + '</div>' +
        (typeLabel ? '<span class="grant-type-tag">' + typeLabel + '</span>' : '') +
        (grant.count > 1 ? '<span class="grant-type-tag" title="The filer\'s own 990 lists this exact recipient, amount, and purpose ' + grant.count + ' separate times for the year.">&times;' + grant.count + '</span>' : '') +
        (grant.metric_unit ? '<div class="grant-metric">' + grant.metric_unit + '</div>' : '') +
      '</div>' +
      '<div class="grant-row-right">' +
        '<div class="grant-amount">' + fmtA(grant.amount) + '</div>' +
        confidenceBadge(grant.confidence) +
      '</div>' +
    '</div>';
  }).join('');

  var moreMatchedHtml = grouped.length > 5
    ? '<div class="grant-more">+ ' + (grouped.length - 5) + ' more matched grants</div>'
    : '';

  // ── Unresolvable grants ────────────────────────────────────────────────────
  // Collect top_grants that carry an unresolvable_reason tag, excluding any
  // that are already represented in matched_detail.
  var matchedSigs = {};
  (g.matched_detail || []).forEach(function(d) {
    matchedSigs[d.recipient + '|' + d.amount + '|' + (d.purpose || '')] = true;
  });

  var unresolvable = (g.top_grants || []).filter(function(gr) {
    var sig = gr.name + '|' + gr.amount + '|' + (gr.purpose || '');
    return gr.unresolvable_reason && !matchedSigs[sig];
  });

  var shownUnresolvable = unresolvable.slice(0, 4);
  var unresolvedHtml = '';
  if (unresolvable.length > 0) {
    var rows = shownUnresolvable.map(function(gr) {
      var info = UNRESOLVABLE_LABELS[gr.unresolvable_reason] || { label: gr.unresolvable_reason, title: '' };
      return '<div class="grant-row grant-row-unresolvable">' +
        '<div class="grant-row-left">' +
          '<div class="grant-recipient grant-recipient-dim">' + gr.name + '</div>' +
          '<span class="grant-reason-badge grant-reason-' + gr.unresolvable_reason + '" title="' + info.title + '">' + info.label + '</span>' +
        '</div>' +
        '<div class="grant-row-right">' +
          '<div class="grant-amount grant-amount-dim">' + fmtA(gr.amount) + '</div>' +
        '</div>' +
      '</div>';
    }).join('');

    var moreUnresolvable = unresolvable.length > 4
      ? '<div class="grant-more">+ ' + (unresolvable.length - 4) + ' more unresolvable grants</div>'
      : '';

    unresolvedHtml =
      '<div class="grant-section-divider">Unresolvable grants</div>' +
      rows + moreUnresolvable;
  }

  if (!hasMatched && !unresolvedHtml) return '';

  return '<div class="grant-panel">' +
    '<div class="grant-panel-header">' +
      '<span class="grant-panel-title">Grant Impact</span>' +
      (hasMatched ? '<span class="grant-match-pct">' + matchPct + '% of grants matched to impact data</span>' : '') +
    '</div>' +
    '<div class="grant-list">' +
      matchedHtml + moreMatchedHtml + unresolvedHtml +
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
  filtered.sort(function(a, b) { return a.name.localeCompare(b.name); });
  if (!filtered.length) {
    list.innerHTML = '<p style="color:rgba(240,232,216,0.4);padding:40px 0;text-align:center;">No foundations match.</p>';
    return;
  }
  list.innerHTML = filtered.map(function(f) {
    var good = f.compliant;
    var sf = !good ? fmtA(f.required - f.qualifying) : null;
    var yrs = f.years_used || 1;
    var yr = f.year ? 'Most recent 990: ' + f.year + ' (' + yrs + '-yr window)' : '';
    var rate = actualRate(f);
    var hasGrants = gData[f.ein] && (
      (gData[f.ein].matched_detail && gData[f.ein].matched_detail.length) ||
      (gData[f.ein].top_grants && gData[f.ein].top_grants.some(function(g) { return g.unresolvable_reason; }))
    );
    var grantTag = '';
    if (hasGrants) {
      grantTag = ' &middot; <span class="year-tag" title="Click to see which organizations this foundation funded.">→ See who they funded</span>';
    } else if (f.operating_foundation) {
      grantTag = '';
    } else {
      var fg = gData[f.ein];
      if (!fg) {
        grantTag = ' &middot; <span class="year-tag" style="color:rgba(160,120,60,0.9);border-color:rgba(160,120,60,0.3)" title="This foundation filed their 990-PF on paper rather than electronically. Paper filings are not included in the IRS public database, so we can\'t see who received their grants.">⚑ Paper filing — recipients unknown</span>';
      } else if (!fg.top_grants || !fg.top_grants.length) {
        grantTag = ' &middot; <span class="year-tag" style="color:#b83c32;border-color:rgba(180,60,50,0.3)" title="This foundation filed electronically but left the grant recipients section of their 990-PF blank. They distributed money but did not publicly disclose who received it.">⚑ Didn\'t disclose recipients</span>';
      }
    }
    return '<div class="foundation-card ' + (good ? 'compliant' : 'noncompliant') + '" data-ein="' + f.ein + '">' +
      '<div class="foundation-card-main">' +
        '<div class="foundation-info">' +
          '<div class="foundation-name">' + toTitle(f.name) + '</div>' +
          '<div class="foundation-meta">' + fmtA(f.assets) + ' in assets' +
          (yr ? ' &middot; <span class="year-tag" title="Most recent IRS tax filing year, averaged over up to 5 years to smooth out one-time spikes.">Filed ' + f.year + '</span>' : '') +
          (f.operating_foundation ? ' &middot; <span class="year-tag" title="This foundation runs its own charitable programs (like a museum, research institute, or hospital) instead of writing grants to other organizations. It\'s judged by a different IRS standard than the 5% rule.">🏛 Runs its own programs</span>' : '') +
          (f.flow_through ? (function() {
            var cp = f.contributions_pct;
            var isPassThru = cp == null || cp >= 95;
            return ' &middot; <span class="year-tag" title="' +
              (isPassThru
                ? 'This foundation has no real endowment. A parent company or family donates money each year and the foundation passes it directly to grantees — it doesn\'t accumulate or invest its own wealth.'
                : Math.round(cp) + '% of this foundation\'s giving was funded by donations from a parent company or family, rather than from returns on its own invested endowment.') +
              '">' + (isPassThru ? '↻ Channels parent donations' : Math.round(cp) + '% funded by parent donations') + '</span>';
          })() : '') +
          grantTag +
          (f.year_gap ? ' &middot; <span class="year-tag" title="We\'re missing data for one or more years in this foundation\'s 5-year window, so the numbers here cover a wider time range than usual.">⚠ Incomplete data window</span>' : '') +
          (!good ? ' &middot; <strong style="color:#c07840">' + sf + ' below the legal minimum</strong>' : '') +
          '</div>' +
        '</div>' +
        '<div class="foundation-stats">' +
          '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.qualifying) + '</div><div class="foundation-stat-label">given to charity (' + yrs + ' yrs)</div></div>' +
          '<div class="foundation-stat"><div class="foundation-stat-value">' + fmtA(f.required) + '</div><div class="foundation-stat-label">legal minimum (' + yrs + ' yrs)</div></div>' +
          '<div class="foundation-stat">' +
            (f.flow_through ? (function() {
              var cp = f.contributions_pct;
              var isPassThru = cp == null || cp >= 95;
              return isPassThru
                ? '<div class="payout-rate good">—</div><div class="foundation-stat-label">gives what it receives</div>'
                : '<div class="payout-rate good">' + Math.round(cp) + '%</div><div class="foundation-stat-label">funded by parent donations</div>';
            })()
              : '<div class="payout-rate ' + (good ? 'good' : 'bad') + '">' + rate + '%</div><div class="foundation-stat-label">of assets given per year</div>') +
            '<div class="compliance-badge ' + (good ? 'good' : 'bad') + '">' + (good ? '✓ Meets legal minimum' : '✗ Below legal minimum') + '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

// ── Grant drawer ──────────────────────────────────────────────────────────────

function openGrantDrawer(ein) {
  var f = fData.find(function(x) { return x.ein === ein; });
  var g = gData[ein];
  if (!f) return;

  document.getElementById('grant-drawer-title').textContent = toTitle(f.name);
  document.getElementById('grant-drawer-meta').textContent =
    fmtA(f.assets) + ' in assets · ' + (f.qualifying ? fmtA(f.qualifying) + ' distributed' : '') +
    (f.year ? ' · ' + f.year + ' filing' : '');

  var body = document.getElementById('grant-drawer-body');
  var html = '';

  var hasNoData = !g || ((!g.top_grants || !g.top_grants.length) && (!g.matched_detail || !g.matched_detail.length));
  if (hasNoData) {
    var badge, badgeStyle, noDataReason;
    if (f.operating_foundation) {
      badge = 'Operating Foundation';
      badgeStyle = 'background:rgba(120,120,120,0.12);color:#888';
      noDataReason = '<strong>Operating foundation</strong> — spends on its own direct charitable programs rather than making grants to other organizations. Schedule I (grants to others) is typically empty or absent on their 990-PF.';
    } else if (!g) {
      badge = 'Filing Not Accessible';
      badgeStyle = 'background:rgba(160,120,60,0.1);color:rgba(140,100,40,0.9)';
      noDataReason = '<strong>Electronic filing not available</strong> — this foundation\'s 990-PF is not in the IRS electronic filing database. They may have filed on paper, which is excluded from the public bulk data. Grant recipients cannot be independently verified.';
    } else {
      badge = 'No Grants Disclosed';
      badgeStyle = 'background:rgba(180,60,50,0.1);color:#b83c32';
      noDataReason = '<strong>No grant recipients listed</strong> — this foundation distributed ' + fmtA(f.qualifying) + ' but left Schedule I (grants to others) empty in their public 990-PF electronic filing. Where this money went is not disclosed in any machine-readable record.';
    }
    body.innerHTML = '<div style="padding:16px 0">' +
      '<div class="grant-reason-badge" style="font-size:10px;padding:3px 8px;' + badgeStyle + ';margin-bottom:10px">' + badge + '</div>' +
      '<p style="font-size:13px;color:var(--ink-muted);line-height:1.6;margin:0">' + noDataReason + '</p>' +
    '</div>';
  } else {
    // Build matched signature set
    var matchedSigs = {};
    (g.matched_detail || []).forEach(function(d) {
      matchedSigs[d.recipient + '|' + d.amount + '|' + (d.purpose || '')] = d;
    });

    // All top grants, sorted by amount desc
    var topGrants = (g.top_grants || []).slice().sort(function(a, b) { return b.amount - a.amount; });

    var matched = [], unresolvable = [], unmatched = [];
    topGrants.forEach(function(gr) {
      var sig = gr.name + '|' + gr.amount + '|' + (gr.purpose || '');
      if (matchedSigs[sig]) {
        matched.push({ grant: gr, detail: matchedSigs[sig] });
      } else if (gr.unresolvable_reason) {
        unresolvable.push(gr);
      } else {
        unmatched.push(gr);
      }
    });

    // Matched section
    if (matched.length) {
      html += '<div class="drawer-section-title">Tracked grants (' + matched.length + ')</div>';
      matched.forEach(function(item) {
        var gr = item.grant, d = item.detail;
        html += '<div class="drawer-grant-row">' +
          '<div class="drawer-grant-left">' +
            '<div class="drawer-grant-name">' + gr.name + '</div>' +
            (d.metric_unit ? '<div class="drawer-grant-impact">' + d.metric_unit + '</div>' : '') +
            (gr.purpose ? '<div class="drawer-grant-purpose">' + gr.purpose + '</div>' : '') +
          '</div>' +
          '<div class="drawer-grant-right">' +
            '<div class="drawer-grant-amount">' + fmtA(gr.amount) + '</div>' +
            confidenceBadge(d.confidence) +
          '</div>' +
        '</div>';
      });
    }

    // Unresolvable section
    if (unresolvable.length) {
      html += '<div class="drawer-section-title">Unresolvable grants (' + unresolvable.length + ')</div>';
      unresolvable.forEach(function(gr) {
        var info = UNRESOLVABLE_LABELS[gr.unresolvable_reason] || { label: gr.unresolvable_reason, title: '' };
        html += '<div class="drawer-grant-row dim">' +
          '<div class="drawer-grant-left">' +
            '<div class="drawer-grant-name muted">' + gr.name + '</div>' +
            '<span class="grant-reason-badge grant-reason-' + gr.unresolvable_reason + '" title="' + info.title + '">' + info.label + '</span>' +
            (gr.purpose ? '<div class="drawer-grant-purpose">' + gr.purpose + '</div>' : '') +
          '</div>' +
          '<div class="drawer-grant-right">' +
            '<div class="drawer-grant-amount muted">' + fmtA(gr.amount) + '</div>' +
          '</div>' +
        '</div>';
      });
    }

    // Unmatched section
    if (unmatched.length) {
      html += '<div class="drawer-section-title">No impact data yet (' + unmatched.length + ')</div>';
      unmatched.forEach(function(gr) {
        html += '<div class="drawer-grant-row dim">' +
          '<div class="drawer-grant-left">' +
            '<div class="drawer-grant-name muted">' + gr.name + '</div>' +
            (gr.purpose ? '<div class="drawer-grant-purpose">' + gr.purpose + '</div>' : '') +
            '<div class="drawer-no-match">Not yet in our impact database</div>' +
          '</div>' +
          '<div class="drawer-grant-right">' +
            '<div class="drawer-grant-amount muted">' + fmtA(gr.amount) + '</div>' +
          '</div>' +
        '</div>';
      });
    }

    if (!html) html = '<p style="color:var(--ink-muted);font-size:13px;padding:20px 0">No grant detail available.</p>';
    body.innerHTML = html;
  }

  document.getElementById('grant-drawer').classList.add('open');
  document.getElementById('grant-drawer-overlay').classList.add('open');
}

function closeGrantDrawer() {
  document.getElementById('grant-drawer').classList.remove('open');
  document.getElementById('grant-drawer-overlay').classList.remove('open');
}

document.getElementById('grant-drawer-close').addEventListener('click', closeGrantDrawer);
document.getElementById('grant-drawer-overlay').addEventListener('click', closeGrantDrawer);
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeGrantDrawer(); });

document.addEventListener('click', function(e) {
  var card = e.target.closest('.foundation-card');
  if (card && card.dataset.ein) openGrantDrawer(card.dataset.ein);
});

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
chunkFetches.push(
  fetch('foundation_scores.json')
    .then(function(r) { return r.json(); })
    .catch(function() { return []; })
);
Promise.all(chunkFetches).then(function(results) {
  fData = results[0];
  for (var i = 1; i <= 8; i++) {
    results[i].forEach(function(g) { gData[g.ein] = g; });
  }
  results[9].forEach(function(s) { sData[s.ein] = s; });
  console.log('Loaded', fData.length, 'foundations,', Object.keys(gData).length, 'grant records, and', Object.keys(sData).length, 'priority scores');
  renderRankings();
  renderSummary();
  renderFoundations();
});
