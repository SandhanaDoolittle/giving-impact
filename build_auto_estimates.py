#!/usr/bin/env python3
"""
build_auto_estimates.py — Auto-estimate impact metrics for unmatched grant recipients.

METHODOLOGY (Option B):
  For each unmatched grant recipient name that looks like a real US nonprofit:
    1. Search ProPublica Nonprofit Explorer by name
    2. Accept the match if name similarity >= 0.65 (normalized word overlap)
    3. Get the org's NTEE code + most recent annual expenses
    4. Apply a sector-average cost-per-person benchmark keyed to the NTEE code
    5. Add a metrics.json entry marked auto_estimated=True, confidence="auto"

  These estimates will be wrong for individual orgs (sector averages don't
  reflect any one org's actual efficiency), but they give a directionally
  useful signal and are always clearly labeled as estimates.

WHAT IS NOT ADDRESSED HERE (Option A context):
  ~$12-15B of the $31.4B unmatched is structurally unresolvable from 990-PF
  data alone:
    - Form artifacts: "SEE ATTACHED", "VARIOUS INDIVIDUALS", etc. — 990-PF
      rows that never named a specific recipient (~37%)
    - Foundation-to-foundation: e.g. Gates Foundation ($5.5B) is itself a
      990-PF filer; these grants are double-counted in our dataset
    - DAF re-grants: Fidelity Charitable, National Philanthropic Trust, etc. —
      pass-through vehicles where the final recipient is not disclosed
  These are not missing data — they are grants that cannot be attributed to
  a specific impact-measurable nonprofit by design.

Run:
  python3 build_auto_estimates.py [--limit N] [--min-dollars N] [--dry-run]
"""

import json, re, time, glob, os, sys, argparse
import urllib.request, urllib.parse
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed

METRICS_FILE   = "metrics.json"
CACHE_FILE     = "auto_estimate_cache.json"

# ── Normalization ──────────────────────────────────────────────────────────────

DROP_TOKENS = {'INC','INCORPORATED','CORP','CORPORATION','CO','LLC','LTD','THE',
               'OF','AND','A','AN','AT','IN','FOR','TO','BY'}

# Expand common abbreviations before normalization so "USA" matches "UNITED STATES"
ABBREV_EXPAND = {
    r'\bUSA\b': 'UNITED STATES',
    r'\bU\.S\.A\.?\b': 'UNITED STATES',
    r'\bU\.S\.\b': 'UNITED STATES',
    r'\bUS\b': 'UNITED STATES',
    r'\bST\b': 'SAINT',
    r'\bMT\b': 'MOUNT',
    r'\bUNIV\b': 'UNIVERSITY',
    r'\bASSOC\b': 'ASSOCIATION',
    r'\bFDN\b': 'FOUNDATION',
    r'\bFOUND\b': 'FOUNDATION',
    r'\bHOSP\b': 'HOSPITAL',
    r'\bMED\b': 'MEDICAL',
    r'\bCTR\b': 'CENTER',
    r'\bCNTR\b': 'CENTER',
}

def normalize(name):
    name = name.upper()
    name = name.replace('&', ' AND ')
    for pattern, replacement in ABBREV_EXPAND.items():
        name = re.sub(pattern, replacement, name)
    name = re.sub(r'[^A-Z0-9 ]', ' ', name)
    tokens = [t for t in name.split() if t not in DROP_TOKENS and len(t) > 1]
    return ' '.join(tokens)

def name_similarity(grant_name, propublica_name):
    """Word-set Jaccard + coverage similarity on normalized names."""
    a_words = set(normalize(grant_name).split())
    b_words = set(normalize(propublica_name).split())
    if not a_words or not b_words:
        return 0.0
    intersection = a_words & b_words
    union = a_words | b_words
    jaccard = len(intersection) / len(union)
    # Also check that most grant-name words appear in PP name
    coverage = len(intersection) / len(a_words) if a_words else 0
    return (jaccard + coverage) / 2

# ── NTEE → sector metric table ─────────────────────────────────────────────────
# (ntee_prefix): (cause, generic_metric_unit, cost_per_person_usd, metric_label)
#
# Cost benchmarks are sector-wide averages from published research:
#   Education: $5K avg (mix of K-12 orgs, tutoring, adult ed)
#   Health hospital: $2K per encounter (AHA data)
#   Food security: $350 per person per year (Feeding America, FoodFirst data)
#   Housing: $8K per person assisted (NLIHC estimates)
#   International aid: $250 (GiveWell, USAID program cost data)
#   etc.

NTEE_MAP = {
    'A': ('arts_culture',
          'visitors, participants, or audience members served through arts, cultural, or humanities programs',
          35,
          'one visitor, participant, or audience member served'),
    'B': ('education',
          'students or learners served through educational programs, services, or institutions',
          5000,
          'one student or learner served'),
    'C': ('environment',
          'people engaged in or benefiting from environmental conservation, restoration, or education programs',
          75,
          'one person reached through environmental programs'),
    'D': ('animal_welfare',
          'animals cared for, rescued, treated, or protected through animal welfare programs',
          400,
          'one animal cared for or protected'),
    'E': ('health',
          'patients or community members receiving healthcare, hospital, or medical services',
          1500,
          'one patient or community member receiving health services'),
    'F': ('health',
          'people receiving mental health treatment, substance use recovery, or crisis intervention services',
          2500,
          'one person receiving mental health or behavioral health services'),
    'G': ('health',
          'people living with a specific disease or health condition supported through research, education, or patient services',
          300,
          'one person with a specific health condition served through research or patient programs'),
    'H': ('health',
          'people whose health outcomes are improved through medical research, clinical trials, or biomedical innovation',
          800,
          'one person whose care is advanced through medical research'),
    'I': ('community',
          'people served through crime prevention, legal aid, public defender services, or criminal justice reform programs',
          2000,
          'one person served through crime or legal services'),
    'J': ('workforce_dev',
          'people served through job training, career counseling, apprenticeship, or workforce placement programs',
          3500,
          'one person trained or placed through workforce development programs'),
    'K': ('food_security',
          'people receiving food assistance, agricultural support, nutrition education, or hunger relief services',
          350,
          'one person receiving food assistance or nutrition services'),
    'L': ('housing',
          'people receiving affordable housing development, shelter, rental assistance, or housing counseling services',
          7500,
          'one person receiving housing assistance or shelter'),
    'M': ('community',
          'people served through public safety, disaster preparedness, search and rescue, or emergency management programs',
          400,
          'one person served through public safety or emergency preparedness programs'),
    'N': ('community',
          'people served through recreation, sports, fitness, or community leisure programs',
          200,
          'one person served through recreation or sports programs'),
    'O': ('community',
          'youth served through mentoring, leadership development, after-school, or youth empowerment programs',
          1500,
          'one youth served through development or mentoring programs'),
    'P': ('community',
          'people served through human services including social services, family support, domestic violence programs, and community assistance',
          1200,
          'one person served through human services or social support programs'),
    'Q': ('international_aid',
          'people served through international development, humanitarian relief, refugee assistance, or cross-cultural programs',
          250,
          'one person served through international programs'),
    'R': ('community',
          'people engaged through civil rights advocacy, voter rights, anti-discrimination, or social action programs',
          100,
          'one person engaged or protected through civil rights and advocacy programs'),
    'S': ('community',
          'community members served through neighborhood revitalization, economic development, or community improvement programs',
          400,
          'one community member served through community development programs'),
    'U': ('education',
          'people benefiting from science and technology research, STEM education, or innovation and entrepreneurship programs',
          600,
          'one person benefiting from science, technology, or innovation programs'),
    'V': ('community',
          'people reached through social science research, public policy analysis, or civic education programs',
          500,
          'one person engaged through policy research or civic programs'),
    'W': ('community',
          'people served through public and societal benefit programs including advocacy, government effectiveness, and civic institutions',
          500,
          'one person served through public benefit programs'),
    'X': ('missions',
          'congregation members and community members served through religious worship, spiritual care, and faith-based social services',
          600,
          'one person served through religious or faith-based programs'),
}

# ── Noise filters ──────────────────────────────────────────────────────────────

# These fragments in a grant recipient name indicate it is NOT a real matchable nonprofit
NOISE_FRAGMENTS = [
    # Form artifacts — match any "STATEMENT X", "ATTACHMENT X", "SCHEDULE X"
    'SEE ','ATTACHED','ATTACHMENT','STATEMENT ','STATEMENT\x00',
    'SCHEDULE ','SCHEDULE\x00','VARIOUS INDIVIDUALS','INDIVIDUAL PATIENT',
    'ELIGIBLE PATIENT','VARIOUS STOCK','TOTAL GRANTS','CASH GRANTS','GRANTS PAID',
    'NOT REQUIRED','PART XV','NA - SECTION','SECTION 4948','HIPA AND LIPA',
    'VARIOUS ORGANIZATIONS','VARIOUS UNIVERSITIES','VARIOUS - SEE','VARIOUS \x00',
    'UNDER THE HEALTH INSURANCE','HEALTH INSURANCE PORTABILITY',
    'FULL SCHEDULE','KEPT ON FILE','SEE SCHEDULE',
    # Noise single words
    'TOTAL\x00', 'GRANTS\x00',
    # DAFs and community foundations
    'FIDELITY CHARITABLE','FIDELITY INVESTMENTS CHARITABLE',
    'NATIONAL PHILANTHROPIC TRUST','VANGUARD CHARITABLE ENDOWMENT',
    'SCHWAB CHARITABLE','SCHWAB FUND FOR CHARITABLE',
    'NATIONAL CHRISTIAN FOUNDATION','JP MORGAN CHARITABLE',
    'AMERICAN ONLINE GIVING FOUNDATION','IMPACTASSETS',
    'ROCKEFELLER PHILANTHROPY ADVISORS','COMMUNITY FOUNDATION',
    'GIVING FUND','DONOR ADVISED','JEWISH COMMUNAL FUND',
    'AMALGAMATED CHARITABLE FOUNDATION','CENTRAL INDIANA COMMUNITY FOUND',
    'GREATER HOUSTON COMMUNITY','OMAHA COMMUNITY FOUNDATION',
    'MINNEAPOLIS FOUNDATION','BOSTON FOUNDATION','CHICAGO COMMUNITY TRUST',
    'SILICON VALLEY COMMUNITY','NEW YORK COMMUNITY TRUST',
    'GREATER KANSAS CITY','CLEVELAND FOUNDATION','SAN FRANCISCO FOUNDATION',
    'OREGON COMMUNITY FOUNDATION','COMMUNITY FOUN','COMMUNITY FDN',
    'VANGUARD CHARITABLE FUND','GENERAL DONATIONS','EDUCATIONAL MATCHING GIFT',
    'GRANTS APPROVED','NA REGULATION','FULL SCHEDULE KEPT',
    'LONGYEAR MUSEUM',
    'FIDELITY INVESTMENT CHARITABLE','FIDELITY INVESTMENT GIFT',
    'SCHOLARSHIP RECIPIENTS','GENERAL PHILANTHROPIC','CYBERGRANTS',
    'MATCHING DONATIONS','VARIOUS GRANTS','VARIOUS DONATIONS',
    # Other foundations / grantmakers
    'GATES FOUNDATION','KELLOGG FOUNDATION','WALTON FAMILY FOUNDATION',
    'WALTON FOUNDATION','FORD FOUNDATION','MACARTHUR FOUNDATION',
    'HEWLETT FOUNDATION','SOROS ECONOMIC','OPEN SOCIETY FOUNDATION',
    'RF CATALYTIC CAPITAL','GATES PHILANTHROPY PARTNERS','BAILEY CHARITABLE TRUST',
    'SCHUSTERMAN FAMILY FOUNDATION','BADER PHILANTHROPIES',
    'Z SMITH REYNOLDS FOUNDATION','GE FORCE FUND','IMBUTO FOUNDATION',
    'XIAOMI FOUNDATION','TONY BLAIR INSTITUTE',
    'INTERNATIONAL FINANCE CORPORATION','INTERNATIONAL BANK FOR RECONSTRUCTION',
    'INTER-AMERICAN DEVELOPMENT BANK','WOMEN IN INFORMAL EMPLOYMENT',
    'SCI FOUNDATION','DOWNTOWN RIVERFRONT TRUST','1318 LAND TRUST',
    'BLANDIN FOUNDATION','GATES INSTITUTE','CROWN FAMILY FOUNDATION',
    'GLICK FAMILY','EQUITY GROUP FOUNDATION','FOUNDATION FOR DETROIT',
    'ABF FUND','GLOBAL FINANCING FACILITY','NATIONAL FUND FOR CHRISTIAN',
    'GRAND RIVER DAM','NATIONAL CHRISTIAN CHARITABLE FOUNDATION',
    'ALICE L WALTON FOUNDATION','C K BLANDIN FOUNDATION',
    'LTEF-UK','LTEF','BAKAR BIOENGUINUTY',
    # Government
    'STATE OF ','CITY OF ','COUNTY OF ','DEPT OF EDU','DEPARTMENT OF EDUCATION',
    'PARKS&REC','PARKS AND REC','UTRGV','IN DEPT OF EDU',
    # Foreign / international finance bodies
    'UNIVERSITY OF OXFORD','UNIVERSITY OF CAMBRIDGE','UNIVERSITY OF TORONTO',
    'UNIVERSITY OF MANITOBA','LONDON SCHOOL','UK REGISTERED','-UK','(UK)',
    'MANDEL SCHOOL FOR EDUCATIONAL LEADERSHIP',
    # Other catch-alls
    'BAKAR BIOENGUINUTY HUB','US IAS MEMBERS TRUST','HUDSON VALLEY FARM HUB',
    'INDEPENDENT COLLEGES OF INDIANA','INDIANAPOLIS CTR FOR CONGREGATIONS',
    'CITY SEMINARY OF NEW YORK','UOP\x00',
]

def is_noise(name: str) -> bool:
    if not name or not name.strip():
        return True
    stripped = name.strip()
    # Very short names are usually abbreviations or codes
    if len(stripped) <= 4:
        return True
    # All-digit / punctuation names
    if re.match(r'^[\d\s\-\.\,\#\/]+$', stripped):
        return True
    # Fewer than 2 real words (catches "GRANTS", "TOTAL", "STATEMENT D")
    real_words = [w for w in stripped.upper().split() if len(w) > 2]
    if len(real_words) < 2:
        return True
    nu = stripped.upper()
    # Exact match single-word noise
    if nu in {'GRANTS', 'TOTAL', 'VARIOUS', 'NA', 'NONE', 'CASH GRANTS',
              'SEE ATTACHED', 'SEE ATTACHMENT', 'SEE SCHEDULE'}:
        return True
    # Fragment matches
    for frag in NOISE_FRAGMENTS:
        clean_frag = frag.rstrip('\x00')
        if frag.endswith('\x00'):
            if nu == clean_frag:
                return True
        else:
            if clean_frag in nu:
                return True
    return False

# ── ProPublica API helpers ─────────────────────────────────────────────────────

PP_BASE = "https://projects.propublica.org/nonprofits/api/v2"

def pp_search(query: str, retries=2) -> list:
    """Search ProPublica for nonprofits matching query. Returns list of org dicts."""
    q = urllib.parse.quote(query[:80])
    url = f"{PP_BASE}/search.json?q={q}"
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=8) as r:
                return json.loads(r.read()).get('organizations', [])
        except Exception:
            if attempt < retries:
                time.sleep(1.5)
    return []

def pp_org_details(ein: str, retries=2) -> dict:
    """Get org details + latest filing from ProPublica. Returns dict or {}."""
    ein_clean = str(ein).lstrip('0').replace('-','')
    url = f"{PP_BASE}/organizations/{ein_clean}.json"
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=8) as r:
                d = json.loads(r.read())
                org = d.get('organization', {})
                filings = d.get('filings_with_data', [])
                latest = filings[0] if filings else {}
                return {
                    'ein': str(org.get('ein','')),
                    'name': org.get('name',''),
                    'ntee_code': org.get('ntee_code',''),
                    'state': org.get('state',''),
                    'city': org.get('city',''),
                    'expenses': latest.get('totfuncexpns'),
                    'year': latest.get('tax_prd_yr'),
                }
        except Exception:
            if attempt < retries:
                time.sleep(1.5)
    return {}

# ── Core matching logic ────────────────────────────────────────────────────────

def search_query_for(grant_name: str) -> str:
    """Build a cleaner ProPublica search query from a grant name."""
    q = grant_name.upper()
    for pattern, replacement in ABBREV_EXPAND.items():
        q = re.sub(pattern, replacement, q)
    # Lowercase for ProPublica (works better)
    return q.lower()

# Words that indicate institution type — if these appear in PP result but NOT
# in grant name, the match is likely a false positive
TYPE_WORDS = {'COLLEGE','UNIVERSITY','HOSPITAL','MEDICAL','SCHOOL',
              'TECHNICAL','SEMINARY','POLYTECHNIC'}

def find_best_match(grant_name: str) -> tuple[dict, float]:
    """
    Search ProPublica for grant_name. Return (org_details, similarity_score).
    org_details is {} if no confident match found.
    """
    # Try expanded query first, fall back to raw name
    results = pp_search(search_query_for(grant_name))
    if not results:
        results = pp_search(grant_name)
    if not results:
        return {}, 0.0

    grant_words_upper = set(re.sub(r'[^A-Z ]', ' ', grant_name.upper()).split())

    best_score = 0.0
    best_result = None
    for r in results[:5]:
        pp_name = r.get('name','')
        score = name_similarity(grant_name, pp_name)

        # Penalize if PP name has institution-type words the grant name lacks
        pp_words_upper = set(re.sub(r'[^A-Z ]', ' ', pp_name.upper()).split())
        type_conflicts = TYPE_WORDS & pp_words_upper - grant_words_upper
        if type_conflicts:
            score *= 0.6  # heavy penalty for type mismatch

        if score > best_score:
            best_score = score
            best_result = r

    if best_score < 0.60:
        return {}, best_score

    # Get detailed financials for the best match
    ein = str(best_result.get('ein',''))
    if not ein:
        return {}, best_score

    details = pp_org_details(ein)
    details['pp_search_name'] = best_result.get('name','')
    return details, best_score

# ── Metrics entry generation ───────────────────────────────────────────────────

def make_entry(grant_name: str, details: dict, score: float) -> tuple[dict | None, str]:
    """
    Generate a metrics.json entry from ProPublica org details.
    Returns (entry_or_None, reason_string).
    """
    ntee = (details.get('ntee_code') or '').strip()
    ntee_key = ntee[0].upper() if ntee else ''

    # T-codes = Philanthropy/grantmakers (foundations, DAFs, federated fundraising)
    # Y-codes = Mutual Benefit (credit unions, insurance, etc.) — skip both
    if ntee_key in ('T', 'Y', ''):
        return None, f"NTEE={ntee or 'none'} (grantmaker/mutual-benefit — skip)"

    if ntee_key not in NTEE_MAP:
        return None, f"NTEE={ntee} (no sector mapping)"

    expenses = details.get('expenses')
    if not expenses or expenses < 500_000:
        return None, f"NTEE={ntee} (expenses ${expenses or 0:,.0f} < $500K threshold)"

    cause, metric_unit, cost_per_person, metric_label = NTEE_MAP[ntee_key]
    pp_name = details.get('name','') or details.get('pp_search_name','')
    city = details.get('city','')
    state = details.get('state','')
    location = f"{city}, {state}" if city and state else (state or '')
    year = details.get('year') or 'recent'

    # Estimated people served = expenses / sector benchmark
    est_served = int(expenses / cost_per_person)
    if est_served < 1:
        return None
    impact_per_100 = round(100 / cost_per_person, 6)

    # Build aliases — include both the grant text form and ProPublica legal name
    aliases = []
    if pp_name and pp_name != grant_name:
        aliases.append(pp_name)
    # Add the grant text form as an alias if different from ProPublica name
    if grant_name not in aliases:
        aliases.append(grant_name)

    entry = {
        "name": pp_name or grant_name,
        "ein": details.get('ein',''),
        "pp_name": aliases,
        "cause": cause,
        "primary_metric_label": metric_label,
        "primary_metric_value": est_served,
        "primary_metric_unit": metric_unit,
        "cost_per_outcome_usd": cost_per_person,
        "impact_per_100_usd": impact_per_100,
        "confidence": "auto",
        "auto_estimated": True,
        "source": "ProPublica Nonprofit Explorer + NTEE sector benchmarks",
        "source_detail": (
            f"{pp_name or grant_name} ({location}). "
            f"Annual expenses: ${expenses:,.0f} ({year}). "
            f"NTEE code: {ntee}. "
            f"Impact estimated using sector-average cost-per-person benchmark "
            f"for NTEE '{ntee_key}' organizations (${cost_per_person:,.0f}/person). "
            f"ProPublica name match similarity: {score:.0%}."
        ),
        "extraction_note": (
            f"AUTO-ESTIMATED — not hand-researched. "
            f"Uses ${cost_per_person:,.0f}/person sector average for NTEE code {ntee} organizations. "
            f"Actual impact per dollar may differ significantly from this estimate. "
            f"Matched from grant text '{grant_name}' to ProPublica record '{pp_name}' "
            f"(name similarity {score:.0%})."
        ),
        "impact_description": (
            f"one person reached through {pp_name or grant_name}'s programs "
            f"(sector-estimated — {metric_unit})"
        ),
        "annual_expenses_usd": expenses,
        "revenue_year": year,
    }
    return entry, "ok"

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto-estimate impact metrics for unmatched grant recipients")
    parser.add_argument('--limit', type=int, default=500, help='Max orgs to process per run (default 500)')
    parser.add_argument('--min-dollars', type=int, default=100_000, help='Min total grant dollars to consider (default $100K)')
    parser.add_argument('--min-similarity', type=float, default=0.60, help='Min name similarity to accept match (default 0.60)')
    parser.add_argument('--dry-run', action='store_true', help='Preview what would be added without writing')
    parser.add_argument('--delay', type=float, default=0.4, help='Seconds between API requests (default 0.4)')
    args = parser.parse_args()

    print(f"Loading metrics.json...")
    with open(METRICS_FILE) as f:
        metrics = json.load(f)

    # Build lookup sets
    existing_eins = {str(e.get('ein','')).strip() for e in metrics if e.get('ein')}
    existing_normalized = set()
    for m in metrics:
        if not m.get('primary_metric_unit'):
            continue
        pp = m.get('pp_name') or []
        if isinstance(pp, str): pp = [pp]
        for n in [m['name']] + pp:
            existing_normalized.add(normalize(str(n)))

    print(f"  {len(metrics)} existing entries, {len(existing_eins)} EINs, {len(existing_normalized)} name keys")

    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        print(f"  Loaded {len(cache)} cached lookups from {CACHE_FILE}")

    # Collect unmatched grant names
    print(f"\nCollecting unmatched grant names...")
    unmatched: dict[str, float] = {}
    for fn in sorted(glob.glob('foundation_grants_*.json')):
        with open(fn) as f:
            foundations = json.load(f)
        for fnd in foundations:
            for g in fnd.get('top_grants', []):
                n = g.get('name','')
                amt = g.get('amount', 0)
                if not n or not amt:
                    continue
                if normalize(n) in existing_normalized:
                    continue
                if is_noise(n):
                    continue
                unmatched[n] = unmatched.get(n, 0) + amt

    # Filter and rank
    candidates = [(n, v) for n, v in unmatched.items() if v >= args.min_dollars]
    candidates.sort(key=lambda x: -x[1])
    print(f"  {len(candidates):,} unique candidates with >= ${args.min_dollars:,} in grants")
    print(f"  Processing up to {args.limit} orgs (use --limit to change)\n")

    # Process candidates
    added_entries = []
    processed = 0
    skipped_noise = 0
    skipped_no_match = 0
    skipped_no_ntee = 0
    skipped_dup_ein = 0

    for grant_name, total_amt in candidates:
        if processed >= args.limit:
            break

        processed += 1
        print(f"[{processed}/{min(args.limit, len(candidates))}] ${total_amt/1e6:.1f}M  {grant_name[:60]}", end='  ')

        # Check cache first
        cache_key = normalize(grant_name)
        if cache_key in cache:
            cached = cache[cache_key]
            if cached is None:
                print("→ cached: no match")
                skipped_no_match += 1
                continue
            details = cached['details']
            score = cached['score']
            print(f"→ cached: {details.get('name','')[:40]} ({score:.0%})", end='  ')
        else:
            # Live API lookup
            details, score = find_best_match(grant_name)
            cache[cache_key] = {'details': details, 'score': score} if details else None
            # Save cache periodically
            if processed % 20 == 0:
                with open(CACHE_FILE, 'w') as f:
                    json.dump(cache, f)
            time.sleep(args.delay)

        if not details:
            print("→ no match")
            skipped_no_match += 1
            continue

        if score < args.min_similarity:
            print(f"→ low similarity ({score:.0%})")
            skipped_no_match += 1
            continue

        # Check EIN dedup
        ein = str(details.get('ein','')).strip()
        if ein and ein in existing_eins:
            print(f"→ EIN {ein} already in metrics")
            skipped_dup_ein += 1
            continue

        # Generate entry
        entry, reason = make_entry(grant_name, details, score)
        if not entry:
            print(f"→ skip: {reason}")
            skipped_no_ntee += 1
            continue

        added_entries.append(entry)
        existing_eins.add(ein)
        existing_normalized.add(normalize(entry['name']))
        for alias in (entry.get('pp_name') or []):
            existing_normalized.add(normalize(str(alias)))

        ntee = details.get('ntee_code','?')
        expenses = details.get('expenses',0)
        cost = entry['cost_per_outcome_usd']
        est = entry.get('primary_metric_value',0)
        print(f"→ ADDED  NTEE={ntee}  exp=${expenses/1e6:.1f}M  ~{est:,} people @ ${cost}/person")

    # Save cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f"\nCache saved to {CACHE_FILE}")

    # Write results
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Candidates processed:   {processed}")
    print(f"  Entries generated:      {len(added_entries)}")
    print(f"  No ProPublica match:    {skipped_no_match}")
    print(f"  EIN already in metrics: {skipped_dup_ein}")
    print(f"  No NTEE mapping:        {skipped_no_ntee}")

    if not added_entries:
        print("\nNothing new to add.")
        return

    if args.dry_run:
        print(f"\n--dry-run: would add {len(added_entries)} entries. Not writing.")
        print("Entries:")
        for e in added_entries:
            print(f"  {e['name'][:50]}  EIN={e['ein']}  cause={e['cause']}  ~{e.get('primary_metric_value',0):,} @ ${e['cost_per_outcome_usd']}/person")
        return

    # Write to metrics.json
    metrics.extend(added_entries)
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\nWrote {len(added_entries)} new auto-estimated entries to {METRICS_FILE}")
    print(f"Total entries now: {len(metrics)}")
    print(f"\nNext: run match_grants.py && compute_efficiency_scores.py")

if __name__ == '__main__':
    main()
