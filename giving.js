fetch('metrics.json')
  .then(r => r.json())
  .then(orgs => {

    const list       = document.getElementById('org-list');
    const input      = document.getElementById('donation');
    const search     = document.getElementById('search');
    const hideBox    = document.getElementById('hide-unavailable');
    const hideEstBox = document.getElementById('hide-estimates');
    const causeGrid  = document.getElementById('cause-grid');
    const heroEx     = document.getElementById('hero-examples');

    let currentCause    = 'all';
    let currentSearch   = '';
    let hideUnavailable = false;
    let hideEstimates   = false;

    // ── Lookup maps ─────────────────────────────────────
    const tagClass = {
      food_security:'tag-food', workforce_dev:'tag-jobs', housing:'tag-housing',
      missions:'tag-missions', recovery:'tag-recovery', international_aid:'tag-international',
      health:'tag-health', education:'tag-education', disaster_relief:'tag-disaster',
      community:'tag-community', environment:'tag-environment', animal_welfare:'tag-animals',
    };
    const tagLabel = {
      food_security:'Food', workforce_dev:'Jobs', housing:'Housing',
      missions:'Missions', recovery:'Recovery', international_aid:'International',
      health:'Health', education:'Education', disaster_relief:'Disaster Relief',
      community:'Community', environment:'Environment', animal_welfare:'Animals',
    };
    const tileIcon = {
      food_security:'🌾', workforce_dev:'💼', housing:'🏠', missions:'✝️',
      recovery:'🌱', international_aid:'🌍', health:'❤️', education:'📚',
      disaster_relief:'⚡', community:'🤝', environment:'🌿', animal_welfare:'🐾',
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

    function impactPlain(org, donation) {
      if (org.impact_per_100_usd < 1 && org.cost_per_outcome_usd) {
        const pct = (donation / org.cost_per_outcome_usd) * 100;
        if (pct >= 100) {
          const n = Math.floor(pct / 100);
          return `${n} ${n===1?'person':'people'} — ${org.impact_description||'helped'}`;
        }
        return `${fmtNum(pct, 1)}% toward ${org.impact_description||'one outcome'}`;
      }
      const n = (donation / 100) * org.impact_per_100_usd;
      return `${Math.round(n).toLocaleString()} ${org.primary_metric_unit}`;
    }

    // ── Hero examples ────────────────────────────────────
    const heroCauses = ['food_security','international_aid','health','education','workforce_dev','housing'];

    function updateHeroExamples(donation) {
      const examples = heroCauses
        .map(c => orgs
          .filter(o => !o.pass_through && o.cause===c && o.data_available!==false && o.impact_per_100_usd && o.impact_per_100_usd >= 1)
          .sort((a,b) => b.impact_per_100_usd - a.impact_per_100_usd)[0])
        .filter(Boolean)
        .slice(0, 3);

      heroEx.innerHTML = examples.map(org => `
        <div class="ex-chip">
          <span class="ex-chip-icon">${tileIcon[org.cause]||'•'}</span>
          <div class="ex-chip-text">
            <strong>${impactPlain(org, donation)}</strong>
            <span>${org.name}</span>
          </div>
        </div>
      `).join('');
    }

    // ── Cause tiles ──────────────────────────────────────
    function buildCauseTiles() {
      causeGrid.innerHTML = Object.keys(tagLabel).map(cause => {
        const n = orgs.filter(o => !o.pass_through && o.cause === cause).length;
        return `
          <button class="cause-tile${cause===currentCause?' active':''}" data-cause="${cause}">
            <span class="tile-icon">${tileIcon[cause]}</span>
            <span class="tile-name">${tagLabel[cause]}</span>
            <span class="tile-count">${n} org${n!==1?'s':''}</span>
            <span class="tile-best" data-cause="${cause}"></span>
          </button>`;
      }).join('');

      causeGrid.querySelectorAll('.cause-tile').forEach(tile => {
        tile.addEventListener('click', () => {
          const next = tile.dataset.cause === currentCause ? 'all' : tile.dataset.cause;
          setActiveCause(next);
          display(Number(input.value));
          document.getElementById('browse').scrollIntoView({behavior:'smooth', block:'start'});
        });
      });
    }

    function updateTileBests(donation) {
      Object.keys(tagLabel).forEach(cause => {
        const el = causeGrid.querySelector(`.tile-best[data-cause="${cause}"]`);
        if (!el) return;
        const best = orgs
          .filter(o => !o.pass_through && o.cause===cause && o.data_available!==false && o.impact_per_100_usd && o.impact_per_100_usd >= 1)
          .sort((a,b) => b.impact_per_100_usd - a.impact_per_100_usd)[0];
        if (best) {
          const n = (donation / 100) * best.impact_per_100_usd;
          el.textContent = `Up to ${Math.round(n).toLocaleString()} ${best.primary_metric_unit}`;
        } else {
          const total = orgs.filter(o => !o.pass_through && o.cause===cause).length;
          el.textContent = `${total} organizations`;
        }
      });
    }

    function setActiveCause(cause) {
      currentCause = cause;
      causeGrid.querySelectorAll('.cause-tile').forEach(t =>
        t.classList.toggle('active', t.dataset.cause === cause));
      document.querySelectorAll('.filter').forEach(b =>
        b.classList.toggle('active', b.dataset.cause === cause));
    }

    // ── Display ──────────────────────────────────────────
    function display(donation) {
      list.innerHTML = '';

      let filtered = orgs.filter(org => {
        if (org.pass_through) return false;
        if (hideUnavailable && org.data_available === false) return false;
        if (hideEstimates && org.data_available !== false && org.confidence === 'low') return false;
        if (currentCause !== 'all' && org.cause !== currentCause) return false;
        if (currentSearch && !org.name.toLowerCase().includes(currentSearch)) return false;
        return true;
      });

      filtered.sort((a, b) => {
        const aD = a.data_available !== false && a.impact_per_100_usd;
        const bD = b.data_available !== false && b.impact_per_100_usd;
        if (aD && !bD) return -1;
        if (!aD && bD) return 1;
        if (!aD && !bD) return (a.name||'').localeCompare(b.name||'');
        if (currentCause === 'all') return (a.name||'').localeCompare(b.name||'');
        return (b.impact_per_100_usd||0) - (a.impact_per_100_usd||0);
      });

      if (filtered.length === 0) {
        list.innerHTML = '<p style="color:#C2B69D;font-style:italic;padding:20px 0;">No organizations match your search.</p>';
        return;
      }

      filtered.forEach(org => {
        const card = document.createElement('div');
        const rev  = org.annual_revenue_usd ? `<p class="org-revenue">Annual revenue: ${fmtRev(org.annual_revenue_usd)}${org.revenue_year ? ' ('+org.revenue_year+')' : ''}</p>` : '';

        if (org.data_available === false) {
          card.className = 'card card-unavailable';
          let contact = '';
          if (org.website)     contact = `<p class="unavailable-note">Learn more at <a href="https://${org.website}" target="_blank">${org.website}</a></p>`;
          else if (org.email)  contact = `<p class="unavailable-note">Contact: <a href="mailto:${org.email}">${org.email}</a></p>`;
          const badge = org.church_exempt
            ? `<span class="badge-church">⛪ No 990 required</span>`
            : `<p class="unavailable-note">Impact data not yet available.</p>`;
          card.innerHTML = `
            <span class="tag ${tagClass[org.cause]||'tag-community'}">${tagLabel[org.cause]||org.cause}</span>
            <h2>${org.name}</h2>
            ${badge}${contact}${rev}`;
        } else if (org.impact_per_100_usd) {
          card.className = 'card';
          const reliability = org.reliability || 'Based on published reports — verify before sharing';
          card.innerHTML = `
            <div class="card-header-row">
              <span class="tag ${tagClass[org.cause]}">${tagLabel[org.cause]}</span>${confBadge(org)}
            </div>
            <h2>${org.name}</h2>
            <p>Your $${donation} ${impactText(org, donation)}</p>
            <p class="reliability">${reliability}</p>${rev}`;
        }

        if (card.innerHTML) list.appendChild(card);
      });
    }

    // ── Init ─────────────────────────────────────────────
    buildCauseTiles();
    updateTileBests(100);
    updateHeroExamples(100);
    display(100);

    // Donation
    input.addEventListener('input', () => {
      const v = Number(input.value);
      if (!v || v < 1) return;
      updateHeroExamples(v);
      updateTileBests(v);
      display(v);
    });

    // Search
    search.addEventListener('input', () => {
      currentSearch = search.value.toLowerCase().trim();
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

    // Filter pills
    document.querySelectorAll('.filter').forEach(btn => {
      btn.addEventListener('click', () => {
        const next = btn.dataset.cause === currentCause ? 'all' : btn.dataset.cause;
        setActiveCause(next);
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
