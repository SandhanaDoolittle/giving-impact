Promise.all([
  fetch('metrics.json').then(r => r.json()),
  fetch('ncf_orgs.json').then(r => r.json()).catch(() => [])
])
  .then(([baseOrgs, ncfOrgs]) => {
    let orgs = baseOrgs.concat(ncfOrgs);
    let showAll = false;          // false = NCF grantees only
    let otherLoaded = false;
    let sortMode = 'ncf';
    let shownCount = 60;          // cards rendered; "Show more" raises it
    const PAGE = 60;
    const showAllBox = document.getElementById('show-all-orgs');

    const list       = document.getElementById('org-list');
    const input      = document.getElementById('donation');
    const search     = document.getElementById('search');
    const hideBox    = document.getElementById('hide-unavailable');
    const hideEstBox = document.getElementById('hide-estimates');
    const christianBox = document.getElementById('christian-only');
    const causeGrid  = document.getElementById('cause-grid');

    let currentCause    = 'all';
    let currentSearch   = '';
    let hideUnavailable = false;
    let hideEstimates   = false;
    let christianOnly   = false;

    // ── Lookup maps ─────────────────────────────────────
    const tagClass = {
      food_security:'tag-food', workforce_dev:'tag-jobs', housing:'tag-housing',
      missions:'tag-missions', recovery:'tag-recovery', international_aid:'tag-international',
      health:'tag-health', education:'tag-education', disaster_relief:'tag-disaster',
      community:'tag-community', environment:'tag-environment', animal_welfare:'tag-animals',
      arts_culture:'tag-arts',
    };
    const tagLabel = {
      food_security:'Food', workforce_dev:'Jobs', housing:'Housing',
      missions:'Missions', recovery:'Recovery', international_aid:'International',
      health:'Health', education:'Education', disaster_relief:'Disaster Relief',
      community:'Community', environment:'Environment', animal_welfare:'Animals',
      arts_culture:'Arts & Culture',
    };
    const tileIcon = {
      food_security:'🌾', workforce_dev:'💼', housing:'🏠', missions:'✝️',
      recovery:'🌱', international_aid:'🌍', health:'❤️', education:'📚',
      disaster_relief:'⚡', community:'🤝', environment:'🌿', animal_welfare:'🐾',
      arts_culture:'🎨',
    };

    // ── Helpers ──────────────────────────────────────────
    function fmtRev(v) {
      if (!v) return null;
      if (v >= 1e9) return '$' + (v/1e9).toFixed(1) + 'B';
      if (v >= 1e6) return '$' + (v/1e6).toFixed(1) + 'M';
      if (v >= 1e3) return '$' + Math.round(v/1e3) + 'K';
      return '$' + v.toLocaleString();
    }

    function fmtNum(n, dec = 1) {
      return n.toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec });
    }

    function confBadge(org) {
      if (org.confidence === 'high')   return `<span class="badge-verified">✓ Verified</span>`;
      if (org.confidence === 'medium') return `<span class="badge-published">Sourced</span>`;
      if (org.confidence === 'low')    return `<span class="badge-estimate">~ Estimate</span>`;
      return '';
    }

    function impactText(org, donation) {
      if (org.impact_per_100_usd < 1 && org.cost_per_outcome_usd) {
        const pct  = (donation / org.cost_per_outcome_usd) * 100;
        const desc = org.impact_description || 'one outcome';
        if (pct >= 100) {
          const n = Math.floor(pct / 100);
          return `fully funds <strong>${n} ${n === 1 ? 'person' : 'people'}</strong> — ${desc}`;
        }
        const cost = Math.round(org.cost_per_outcome_usd).toLocaleString();
        return `funds <strong>${fmtNum(pct, 1)}%</strong> of ${desc} (full cost ~$${cost})`;
      }
      const n = (donation / 100) * org.impact_per_100_usd;
      return `provides approximately <strong>${Math.round(n).toLocaleString()} ${org.primary_metric_unit}</strong>`;
    }

    // ── Cause tiles ──────────────────────────────────────
    function buildCauseTiles() {
      causeGrid.innerHTML = Object.keys(tagLabel).map(cause => {
        const n = orgs.filter(o => !o.pass_through && (showAll || o.ncf) && o.cause === cause).length;
        return `
          <button class="cause-tile${cause===currentCause?' active':''}" data-cause="${cause}">
            <span class="tile-circle"><span class="tile-icon">${tileIcon[cause]}</span></span>
            <span class="tile-name">${tagLabel[cause]}</span>
            <span class="tile-count">${n} org${n!==1?'s':''}</span>
          </button>`;
      }).join('');

      causeGrid.querySelectorAll('.cause-tile').forEach(tile => {
        tile.addEventListener('click', () => {
          const next = tile.dataset.cause === currentCause ? 'all' : tile.dataset.cause;
          setActiveCause(next);
          shownCount = PAGE;
          display(Number(input.value));
          document.getElementById('browse').scrollIntoView({behavior:'smooth', block:'start'});
        });
      });
    }

    function setActiveCause(cause) {
      currentCause = cause;
      causeGrid.querySelectorAll('.cause-tile').forEach(t =>
        t.classList.toggle('active', t.dataset.cause === cause));
      document.querySelectorAll('.filter[data-cause]').forEach(b =>
        b.classList.toggle('active', b.dataset.cause === cause));
    }


    // ── Card building ────────────────────────────────────
    function esc(v) {
      return String(v == null ? '' : v).replace(/[&<>"']/g, c =>
        ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }
    const pct0   = x => (x == null ? 'n/a' : Math.round(x * 100) + '%');
    const num0   = x => (x == null ? 'n/a' : Number(x).toLocaleString());
    const money0 = x => (x == null ? 'n/a' : fmtRev(x) || '$0');
    function safeUrl(u) {
      if (!u) return null;
      u = String(u).trim();
      if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
      try { const x = new URL(u); return /^https?:$/.test(x.protocol) ? x.href : null; } catch (e) { return null; }
    }
    function tile(label, value, sub) {
      return `<div class="dt"><div class="dt-val">${value}</div><div class="dt-lab">${label}</div>${sub ? `<div class="dt-sub">${sub}</div>` : ''}</div>`;
    }
    function check(label, v) {
      const cls = v === true ? 'ck-yes' : v === false ? 'ck-no' : 'ck-na';
      const sym = v === true ? '✓' : v === false ? '✗' : '–';
      return `<li class="${cls}"><span class="ck-sym">${sym}</span>${label}</li>`;
    }

    // Many filings are typed in ALL CAPS. Show those in sentence case; trim long text.
    function tidy(s, max) {
      s = String(s || '').trim();
      if (s && s === s.toUpperCase()) {
        s = s.toLowerCase().replace(/(^|[.!?:]\s+)([a-z])/g, (m, a, b) => a + b.toUpperCase());
        // restore common proper nouns that lowercasing flattened
        s = s.replace(/\b(god|jesus|christ|christian|christians|christmas|lord|savior|bible|gospel|holy spirit|american|america|africa|african|asia|asian|india|haiti|china|israel|ukraine|sudan|mexico|latin america|u\.s\.|usa|ncf|ecfa)\b/g,
          w => w.replace(/(^|\s)([a-z])/g, (m, sp, c) => sp + c.toUpperCase()).replace('U.s.', 'U.S.').replace('Usa', 'USA').replace('Ncf', 'NCF').replace('Ecfa', 'ECFA'));
      }
      if (max && s.length > max) {
        s = s.slice(0, max);
        s = s.replace(/\s+\S*$/, '') + '…';
      }
      return s;
    }

    function hasImpact(org) { return org.data_available !== false && !!org.impact_per_100_usd; }

    // Part of the back we can show immediately from the main data file
    function backBase(org) {
      let h = '';
      if (org.ncf) {
        const rank = org.ncf_rank
          ? `Ranked <strong>#${org.ncf_rank.toLocaleString()}</strong> of ${org.ncf_rank_of.toLocaleString()} organizations NCF has granted to.` : '';
        h += `<div class="back-sec"><h3>National Christian Foundation</h3>
          <p>${rank} NCF has granted <strong>${money0(org.ncf_total_granted)}</strong> in total
          (${org.ncf_years_seen} year${org.ncf_years_seen === 1 ? '' : 's'} of grants, latest ${org.ncf_latest_year}).
          ${org.ecfa ? '<span class="badge-ecfa">ECFA member</span>' : ''}</p></div>`;
      }
      return h;
    }

    function impactBack(org) {
      if (!hasImpact(org)) return '';
      const rel = org.reliability || '';
      const extra = org.source_detail || org.extraction_note || '';
      return `<div class="back-sec"><h3>Impact estimate</h3>
        ${rel ? `<p>${esc(rel)}</p>` : ''}${extra ? `<p class="source-detail">${esc(extra)}</p>` : ''}</div>`;
    }

    function detailHtml(d, org) {
      if (!d) {
        return `<div class="back-sec"><p class="unavailable-note">Full Form 990 details are not available for this organization yet.</p></div>`;
      }
      let h = '';
      if (d.xml && d.xml !== 'ok') {
        h += d.xml.indexOf('no e-filed') === 0
          ? `<div class="back-sec"><p class="unavailable-note">No Form 990 found in the IRS electronic filing archive. Churches and many religious ministries are not required to file one, so detailed spending figures are not public for this organization.</p></div>`
          : `<div class="back-sec"><p class="unavailable-note">This organization's latest Form 990 could not be read, so spending details are not shown.</p></div>`;
      }
      // Efficiency
      if (d.program_ratio != null) {
        const p = d.program_ratio, a = d.admin_ratio || 0, f = d.fundraising_ratio || 0;
        const rest = Math.max(0, 1 - p - a - f);
        h += `<div class="back-sec"><h3>How it spends money <span class="h3-sub">${d.tax_year ? 'FY' + d.tax_year : ''}</span></h3>
          <div class="splitbar" title="Program / administration / fundraising">
            <span class="sb-prog" style="flex:${p}"></span><span class="sb-admin" style="flex:${a}"></span><span class="sb-fund" style="flex:${f}"></span>${rest > 0.005 ? `<span class="sb-rest" style="flex:${rest}"></span>` : ''}
          </div>
          <p class="splitkey"><span class="k-prog">Programs ${pct0(p)}</span><span class="k-admin">Administration ${pct0(d.admin_ratio)}</span><span class="k-fund">Fundraising ${pct0(d.fundraising_ratio)}</span></p>
          <div class="dt-grid">
            ${d.cost_to_raise != null ? tile('Cost to raise $1', '$' + d.cost_to_raise.toFixed(2)) : ''}
            ${d.eff_pct != null ? tile('Program spending share', 'Higher than ' + d.eff_pct + '%', 'of listed ' + esc(tagLabel[org.cause] || org.cause) + ' organizations') : ''}
          </div></div>`;
      }
      // Financial health
      const fin = [];
      if (d.revenue != null) fin.push(tile('Revenue', money0(d.revenue)));
      if (d.expenses_total != null) fin.push(tile('Spending', money0(d.expenses_total)));
      if (d.reserve_months != null) fin.push(tile('Cash and investments', d.reserve_months >= 36 ? Math.round(d.reserve_months / 12) + ' yrs' : d.reserve_months + ' mo.', 'of spending on hand'));
      if (d.revenue_change != null) {
        const c = Math.round(d.revenue_change * 100);
        fin.push(tile('Revenue change', c > 500 ? 'Over +500%' : (c > 0 ? '+' : '') + c + '%', d.revenue_change_years.join(' to ')));
      }
      if (d.contrib_pct != null) fin.push(tile('From gifts and grants', pct0(d.contrib_pct), 'of revenue'));
      if (d.govt_pct != null && d.govt_pct > 0.005) fin.push(tile('Government funding', pct0(d.govt_pct), 'of revenue'));
      if (d.earned_pct != null && d.earned_pct > 0.005) fin.push(tile('Fees for services', pct0(d.earned_pct), 'of revenue'));
      if (d.assets != null) fin.push(tile('Assets', money0(d.assets), d.liabilities != null ? 'liabilities ' + money0(d.liabilities) : ''));
      if (fin.length) h += `<div class="back-sec"><h3>Financial health</h3><div class="dt-grid">${fin.join('')}</div></div>`;
      // People and governance
      const ppl = [];
      if (d.founded) ppl.push(tile('Founded', esc(d.founded)));
      if (d.employees != null) ppl.push(tile('Employees', num0(d.employees)));
      if (d.volunteers != null) ppl.push(tile('Volunteers', num0(d.volunteers)));
      if (d.board != null) ppl.push(tile('Board members', num0(d.board), d.board_independent != null ? d.board_independent + ' independent' + (d.independent_pct != null ? ' (' + pct0(d.independent_pct) + ')' : '') : ''));
      if (d.salaries_pct != null) ppl.push(tile('Staff pay and benefits', pct0(d.salaries_pct), 'of spending'));
      if (d.grants_paid && d.grants_pct != null && d.grants_pct > 0.005) {
        const fg = d.grants_foreign ? ', ' + money0(d.grants_foreign) + ' abroad' : '';
        ppl.push(tile('Grants to other organizations', money0(d.grants_paid), pct0(d.grants_pct) + ' of spending' + fg));
      }
      if (d.high_paid_staff) ppl.push(tile('Staff paid over $100K', num0(d.high_paid_staff)));
      if (d.top_pay != null) ppl.push(tile('Highest officer pay', money0(d.top_pay), esc(d.top_pay_title || '') + (d.top_pay_pct != null ? ' · ' + (d.top_pay_pct * 100).toFixed(1) + '% of spending' : '')));
      const flags = [];
      if (d.audited !== undefined) flags.push(check('Audited financial statements', d.audited));
      if (d.conflict_policy !== undefined) flags.push(check('Conflict-of-interest policy', d.conflict_policy));
      if (d.whistleblower_policy !== undefined) flags.push(check('Whistleblower policy', d.whistleblower_policy));
      if (d.audit_committee !== undefined) flags.push(check('Audit committee', d.audit_committee));
      if (ppl.length || flags.length) {
        h += `<div class="back-sec"><h3>People and governance</h3>${ppl.length ? `<div class="dt-grid">${ppl.join('')}</div>` : ''}${flags.length ? `<ul class="checks">${flags.join('')}</ul>` : ''}</div>`;
      }
      // Programs
      if (d.programs && d.programs.length) {
        h += `<div class="back-sec"><h3>Programs, in its own words</h3><ul class="progs">` +
          d.programs.slice(0, 3).map(p => `<li>${esc(tidy(p.desc, 330))}${p.expense ? ` <span class="prog-cost">(${money0(p.expense)} spent${d.expenses_program ? ', ' + pct0(p.expense / d.expenses_program) + ' of program spending' : ''})</span>` : ''}</li>`).join('') +
          `</ul></div>`;
      }
      if (d.mission) h += `<div class="back-sec"><h3>Mission</h3><p>${esc(tidy(d.mission, 420))}</p></div>`;
      return h;
    }

    function linksHtml(org, d) {
      const out = [];
      const site = safeUrl((d && d.website) || org.website);
      if (site) out.push(`<a href="${esc(site)}" target="_blank" rel="noopener">Website</a>`);
      const ein = String(org.ein || '').replace(/\D/g, '');
      if (ein) out.push(`<a href="https://projects.propublica.org/nonprofits/organizations/${ein}" target="_blank" rel="noopener">Full 990 filings (ProPublica)</a>`);
      return out.length ? `<p class="back-links">${out.join(' · ')}</p>` : '';
    }

    // Filing details load from small files split by the last digit of the EIN
    const shardCache = {};
    function loadShard(ein) {
      const k = String(ein || '').replace(/\D/g, '').padStart(9, '0').slice(-1);
      if (!shardCache[k]) shardCache[k] = fetch('details/d' + k + '.json').then(r => (r.ok ? r.json() : {})).catch(() => ({}));
      return shardCache[k].then(m => m[String(ein).replace(/\D/g, '').padStart(9, '0')]);
    }

    function fillDetails(card) {
      if (card.dataset.filled) return;
      card.dataset.filled = '1';
      const org = card._org, slot = card.querySelector('.detail-slot');
      const done = d => { slot.innerHTML = detailHtml(d, org) + impactBack(org) + linksHtml(org, d); };
      if (!org.ein) { done(null); return; }
      loadShard(org.ein).then(done);
    }

    function buildCard(org, donation) {
      const card = document.createElement('div');
      const impact = hasImpact(org);
      card.className = 'card flip-card' + (impact ? '' : ' card-unavailable');
      card._org = org;
      const tag = `<span class="tag ${tagClass[org.cause] || 'tag-community'}">${tagLabel[org.cause] || esc(org.cause)}</span>`;
      const chip = org.ncf_rank
        ? `<span class="ncf-chip" title="Rank among ${org.ncf_rank_of.toLocaleString()} organizations NCF has granted to, 2013 to 2024">NCF #${org.ncf_rank.toLocaleString()}</span>` : '';
      let body;
      if (impact) {
        body = `<p>Your $${donation} ${impactText(org, donation)}</p>`;
      } else {
        let contact = '';
        if (org.website)    contact = `<p class="unavailable-note">Learn more at <a href="https://${esc(org.website)}" target="_blank" rel="noopener">${esc(org.website)}</a></p>`;
        else if (org.email) contact = `<p class="unavailable-note">Contact: <a href="mailto:${esc(org.email)}">${esc(org.email)}</a></p>`;
        const badge = org.church_exempt ? `<span class="badge-church">⛪ No 990 required</span>` : `<p class="unavailable-note">Impact estimate not available.</p>`;
        body = badge + contact;
      }
      card.innerHTML = `
        <div class="flip-card-inner">
          <div class="flip-card-front">
            <div class="card-header-row">${tag}${chip}<button class="flip-btn" aria-label="Show details">ⓘ</button></div>
            <h2>${org.name}</h2>${body}
          </div>
          <div class="flip-card-back">
            <div class="card-header-row">${tag}${confBadge(org)}<button class="flip-btn" aria-label="Back to summary">✕</button></div>
            <h2>${org.name}</h2>
            <div class="back-body">${backBase(org)}<div class="detail-slot"><p class="unavailable-note">Loading filing details…</p></div></div>
          </div>
        </div>`;
      return card;
    }

    function flipCard(card) {
      const inner = card.querySelector('.flip-card-inner');
      const swap = () => {
        card.classList.toggle('flipped');
        if (card.classList.contains('flipped')) fillDetails(card);
      };
      if (!inner.animate || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { swap(); return; }
      inner.animate([{ transform: 'rotateY(0deg)' }, { transform: 'rotateY(90deg)' }], { duration: 170, easing: 'ease-in' })
        .onfinish = () => {
          swap();
          inner.animate([{ transform: 'rotateY(-90deg)' }, { transform: 'rotateY(0deg)' }], { duration: 170, easing: 'ease-out' });
        };
    }

    // ── Display ──────────────────────────────────────────
    function display(donation) {
      list.innerHTML = '';

      let filtered = orgs.filter(org => {
        if (org.pass_through) return false;
        if (!showAll && !org.ncf) return false;
        if (hideUnavailable && org.data_available === false) return false;
        if (hideEstimates && org.data_available !== false && org.confidence === 'low') return false;
        if (christianOnly && !org.is_christian) return false;
        if (currentCause !== 'all' && org.cause !== currentCause) return false;
        if (currentSearch && !org.name.toLowerCase().includes(currentSearch)) return false;
        return true;
      });

      const nm = (a, b) => (a.name || '').localeCompare(b.name || '');
      const hi = o => hasImpact(o);
      filtered.sort((a, b) => {
        if (sortMode === 'name') return nm(a, b);
        if (sortMode === 'ncf') {
          const ra = a.ncf_rank || 1e9, rb = b.ncf_rank || 1e9;
          return ra - rb || nm(a, b);
        }
        if (sortMode === 'eff') {
          const pa = a.program_ratio, pb = b.program_ratio;
          if (pa == null && pb == null) return nm(a, b);
          if (pa == null) return 1;
          if (pb == null) return -1;
          return pb - pa || nm(a, b);
        }
        // impact per dollar
        if (hi(a) && !hi(b)) return -1;
        if (!hi(a) && hi(b)) return 1;
        if (!hi(a) && !hi(b)) return nm(a, b);
        return (b.impact_per_100_usd || 0) - (a.impact_per_100_usd || 0);
      });

      if (filtered.length === 0) {
        list.innerHTML = '<p style="color:#C2B69D;font-style:italic;padding:20px 0;">No organizations match your search.</p>';
        return;
      }

      const total = filtered.length;
      filtered.slice(0, shownCount).forEach(org => list.appendChild(buildCard(org, donation)));

      if (total > shownCount) {
        const more = document.createElement('button');
        more.className = 'show-more-btn';
        more.textContent = `Show more (${(total - shownCount).toLocaleString()} more organizations)`;
        more.addEventListener('click', () => { shownCount += PAGE; display(Number(input.value)); });
        list.appendChild(more);
      }
    }

    // ── Init ─────────────────────────────────────────────
    buildCauseTiles();
    display(100);

    // Flip cards (front summary / back detail)
    list.addEventListener('click', e => {
      const btn = e.target.closest('.flip-btn');
      if (!btn) return;
      const card = btn.closest('.flip-card');
      if (card) flipCard(card);
    });

    // Donation
    input.addEventListener('input', () => {
      const v = Number(input.value);
      if (!v || v < 1) return;
      display(v);
    });
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') input.blur();
    });

    // Search
    search.addEventListener('input', () => {
      currentSearch = search.value.toLowerCase().trim();
      shownCount = PAGE;
      display(Number(input.value));
    });

    // Show all organizations (not just NCF grantees). Loads the extra file on first use.
    showAllBox.addEventListener('change', async () => {
      showAll = showAllBox.checked;
      if (showAll && !otherLoaded) {
        try {
          const other = await fetch('metrics_other.json').then(r => r.json());
          orgs = orgs.concat(other);
          otherLoaded = true;
        } catch (e) { showAll = false; showAllBox.checked = false; return; }
      }
      shownCount = PAGE;
      buildCauseTiles();
      display(Number(input.value));
    });

    // Sort
    document.getElementById('sort-by').addEventListener('change', e => {
      sortMode = e.target.value;
      shownCount = PAGE;
      display(Number(input.value));
    });

    // Hide unavailable toggle
    hideBox.addEventListener('change', () => {
      hideUnavailable = hideBox.checked;
      display(Number(input.value));
    });

    // Hide estimates toggle
    hideEstBox.addEventListener('change', () => {
      hideEstimates = hideEstBox.checked;
      display(Number(input.value));
    });

    // Christian orgs only toggle
    christianBox.addEventListener('change', () => {
      christianOnly = christianBox.checked;
      display(Number(input.value));
    });

    // Filter pills
    document.querySelectorAll('.filter[data-cause]').forEach(btn => {
      btn.addEventListener('click', () => {
        const next = btn.dataset.cause === currentCause ? 'all' : btn.dataset.cause;
        setActiveCause(next);
        shownCount = PAGE;
        display(Number(input.value));
      });
    });

    // Layout toggle
    const layoutBtn = document.getElementById('layout-btn');
    let layoutMode = 0;
    const icons  = ['⊞','▦','☰'];
    const titles = ['Switch to 2-column grid','Switch to 3-column grid','Switch to list view'];
    layoutBtn.addEventListener('click', () => {
      layoutMode = (layoutMode + 1) % 3;
      list.classList.remove('grid-layout','grid-layout-dense');
      if (layoutMode === 1) list.classList.add('grid-layout');
      if (layoutMode === 2) list.classList.add('grid-layout-dense');
      layoutBtn.textContent = icons[layoutMode];
      layoutBtn.title = titles[layoutMode];
      layoutBtn.classList.toggle('grid-active', layoutMode > 0);
    });

    // Back to top
    const backToTop = document.getElementById('back-to-top');
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
