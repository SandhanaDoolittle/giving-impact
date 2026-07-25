#!/usr/bin/env python3
"""
tag_unresolvable.py — Tag unmatched top_grants with the reason they can't be resolved.

Three tags:
  form_artifact         — 990-PF form placeholder, not a real recipient name
  daf_regrant           — Donor-advised fund or community foundation (final recipient not disclosed)
  foundation_to_foundation — Recipient is another private grantmaking foundation

Unmatched grants that don't fit any category are left untagged (real nonprofits
we simply don't have metrics for yet).
"""

import json, re, glob

# ── Helpers ──────────────────────────────────────────────────────────────────

def norm(name):
    return re.sub(r'[^A-Z0-9 ]', ' ', name.upper()).split()

def contains_any(name_upper, fragments):
    return any(f in name_upper for f in fragments)

# ── Form artifact signals ─────────────────────────────────────────────────────
# These appear in 990-PF Schedule I when the filer didn't name individual recipients.

FORM_ARTIFACT_FRAGMENTS = [
    'SEE ATTACHED', 'SEE STATEMENT', 'SEE SCHEDULE', 'SEE ABOVE', 'SEE BELOW',
    'SEE PART', 'SEE CONTINUATION', 'SEE EXHIBIT', 'SEE LIST', 'SEE PAGE',
    'ATTACHMENT', 'VARIOUS INDIVIDUALS', 'VARIOUS ORGANIZATIONS', 'VARIOUS UNIVERSITIES',
    'VARIOUS NONPROFITS', 'VARIOUS CHARITIES', 'VARIOUS GRANTS', 'VARIOUS DONATIONS',
    'VARIOUS - SEE', 'VARIOUS \x00',
    'INDIVIDUAL PATIENT', 'ELIGIBLE PATIENT',
    'TOTAL GRANTS', 'TOTAL CONTRIBUTIONS', 'CASH GRANTS', 'GRANTS PAID',
    'GRANTS APPROVED', 'GRANT PAYMENTS', 'GENERAL DONATIONS', 'GENERAL PHILANTHROPIC',
    'MATCHING DONATIONS', 'MATCHING GIFT', 'EDUCATIONAL MATCHING',
    'NOT REQUIRED', 'KEPT ON FILE', 'FULL SCHEDULE',
    'PART XV', 'NA - SECTION', 'SECTION 4948', 'NA REGULATION',
    'UNDER THE HEALTH INSURANCE', 'HEALTH INSURANCE PORTABILITY',
    'HIPA AND LIPA', 'CYBERGRANTS',
    'SCHOLARSHIP RECIPIENTS', 'SCHOLARSHIP FUND',  # generic pooled
    'VARIOUS STOCK', 'STOCK GRANTS',
]

FORM_ARTIFACT_EXACT = {
    'TOTAL', 'GRANTS', 'GRANT', 'CONTRIBUTIONS', 'N/A', 'NA', 'NONE',
    'VARIOUS', 'SEE ATTACHED', 'SEE STATEMENT', 'ATTACHED',
    '2019 GRANTS', '2020 GRANTS', '2021 GRANTS', '2022 GRANTS', '2023 GRANTS',
    '2024 GRANTS',
}

def is_form_artifact(name):
    u = name.upper().strip()
    # Very short / coded
    if len(u) <= 4:
        return True
    # All digits / punctuation
    if re.match(r'^[\d\s\-\.\,\#\/\(\)]+$', u):
        return True
    # Fewer than 2 real words (after stripping noise tokens)
    words = [w for w in re.sub(r'[^A-Z0-9 ]', ' ', u).split() if len(w) > 1]
    if len(words) < 2:
        return True
    if u in FORM_ARTIFACT_EXACT:
        return True
    if contains_any(u, FORM_ARTIFACT_FRAGMENTS):
        return True
    # Year-prefixed generic names ("2021 GRANTS", "FY2022 DISTRIBUTIONS")
    if re.match(r'^(FY)?\d{4}\s+(GRANTS|DISTRIBUTIONS|CONTRIBUTIONS|GIVING)', u):
        return True
    return False

# ── DAF / community foundation signals ────────────────────────────────────────
# These are pass-through vehicles — the final nonprofit recipient is not disclosed.

DAF_FRAGMENTS = [
    'FIDELITY CHARITABLE', 'FIDELITY INVESTMENTS CHARITABLE', 'FIDELITY INVESTMENT CHARITABLE',
    'FIDELITY INVESTMENT GIFT',
    'NATIONAL PHILANTHROPIC TRUST',
    'VANGUARD CHARITABLE', 'VANGUARD CHARITABLE FUND', 'VANGUARD CHARITABLE ENDOWMENT',
    'SCHWAB CHARITABLE', 'SCHWAB FUND FOR CHARITABLE',
    'JP MORGAN CHARITABLE', 'JPMORGAN CHARITABLE',
    'NATIONAL CHRISTIAN FOUNDATION', 'NATIONAL CHRISTIAN CHARITABLE',
    'AMERICAN ONLINE GIVING FOUNDATION',
    'IMPACTASSETS',
    'JEWISH COMMUNAL FUND',
    'AMALGAMATED CHARITABLE FOUNDATION',
    'DONOR ADVISED',
    'GIVING FUND',
    # Community foundations (primarily DAF operators)
    'COMMUNITY FOUNDATION',
    'COMMUNITY FOUN',
    'COMMUNITY FDN',
    'SILICON VALLEY COMMUNITY',
    'NEW YORK COMMUNITY TRUST',
    'CHICAGO COMMUNITY TRUST',
    'GREATER KANSAS CITY COMMUNITY',
    'CLEVELAND FOUNDATION',
    'SAN FRANCISCO FOUNDATION',
    'MINNEAPOLIS FOUNDATION',
    'BOSTON FOUNDATION',
    'GREATER HOUSTON COMMUNITY',
    'OMAHA COMMUNITY FOUNDATION',
    'CENTRAL INDIANA COMMUNITY',
    'OREGON COMMUNITY FOUNDATION',
    'ROCKEFELLER PHILANTHROPY ADVISORS',
    'ABF FUND',
    'GLOBAL FINANCING FACILITY',
]

def is_daf(name):
    u = name.upper().strip()
    return contains_any(u, DAF_FRAGMENTS)

# ── Foundation-to-foundation signals ─────────────────────────────────────────
# Recipient is itself a private grantmaking foundation (also files a 990-PF).

F2F_FRAGMENTS = [
    # Household-name foundations (definitely 990-PF filers)
    'GATES FOUNDATION', 'GATES PHILANTHROPY',
    'FORD FOUNDATION',
    'MACARTHUR FOUNDATION',
    'HEWLETT FOUNDATION',
    'KELLOGG FOUNDATION',
    'WALTON FAMILY FOUNDATION', 'WALTON FOUNDATION',
    'OPEN SOCIETY FOUNDATION', 'SOROS ECONOMIC DEVELOPMENT',
    'SCHUSTERMAN FAMILY FOUNDATION',
    'BADER PHILANTHROPIES',
    'Z SMITH REYNOLDS FOUNDATION',
    'BLANDIN FOUNDATION', 'C K BLANDIN FOUNDATION',
    'RF CATALYTIC CAPITAL',
    'BAILEY CHARITABLE TRUST',
    'CROWN FAMILY FOUNDATION',
    'GLICK FAMILY FOUNDATION', 'GLICK FAMILY PHILANTHROPIES',
    'EQUITY GROUP FOUNDATION',
    'FOUNDATION FOR DETROIT',
    'ALICE L WALTON FOUNDATION',
    'TONY BLAIR INSTITUTE',
    'IMBUTO FOUNDATION',
    'BAKAR BIOENGUINUTY',
    'XIAOMI FOUNDATION',
    'LONGYEAR MUSEUM',
    # Government / quasi-gov bodies (not matchable nonprofits)
    'STATE OF ',
    'CITY OF ',
    'COUNTY OF ',
    'DEPT OF EDU',
    'DEPARTMENT OF EDUCATION',
    'INTERNATIONAL FINANCE CORPORATION',
    'INTERNATIONAL BANK FOR RECONSTRUCTION',
    'INTER-AMERICAN DEVELOPMENT BANK',
    'WOMEN IN INFORMAL EMPLOYMENT',
    # Foreign / international entities
    'UNIVERSITY OF OXFORD', 'UNIVERSITY OF CAMBRIDGE', 'UNIVERSITY OF TORONTO',
    'UNIVERSITY OF MANITOBA', 'LONDON SCHOOL',
    '-UK', '(UK)', 'UK REGISTERED',
    'LTEF-UK', 'LTEF',
    'STICHTING ',  # Dutch foundation prefix
    'BAOBAB FUNDO',
]

# Strong name signals that the recipient is a private grantmaking foundation
F2F_NAME_SIGNALS = [
    'FAMILY FOUNDATION',
    'PRIVATE FOUNDATION',
    'CHARITABLE TRUST',
    'PHILANTHROPY PARTNERS',
    'PHILANTHROPIES',
    'FAMILY PHILANTHROPIES',
    'CHARITABLE FOUNDATION',  # careful — "AIDS Healthcare Foundation" is a service org
]

def is_foundation_to_foundation(name, foundation_names_set):
    u = name.upper().strip()
    if contains_any(u, F2F_FRAGMENTS):
        return True
    # Name-matched against our known 990-PF filers
    words = [w for w in re.sub(r'[^A-Z ]', ' ', u).split() if len(w) > 2]
    norm_name = ' '.join(words)
    if norm_name in foundation_names_set:
        return True
    # Strong naming signal
    if contains_any(u, F2F_NAME_SIGNALS):
        return True
    return False

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Build a set of normalized foundation names from our grant data (known 990-PF filers)
    print("Building foundation name index...")
    foundation_names_set = set()
    for fp in sorted(glob.glob('foundation_grants_*.json')):
        with open(fp) as f:
            data = json.load(f)
        for fnd in data:
            n = fnd.get('name', '')
            if n:
                words = [w for w in re.sub(r'[^A-Z ]', ' ', n.upper()).split() if len(w) > 2]
                foundation_names_set.add(' '.join(words))
    print(f"  {len(foundation_names_set):,} foundation names indexed")

    # Also build matched signature set per foundation for fast lookup
    total_tagged = {'form_artifact': 0, 'daf_regrant': 0, 'foundation_to_foundation': 0}
    total_untagged_unmatched = 0
    total_already_matched = 0

    for fp in sorted(glob.glob('foundation_grants_*.json')):
        with open(fp) as f:
            data = json.load(f)

        changed = False
        for fnd in data:
            matched_sigs = set(
                (d['recipient'], d['amount'], d.get('purpose'))
                for d in fnd.get('matched_detail', [])
            )

            for grant in fnd.get('top_grants', []):
                sig = (grant['name'], grant['amount'], grant.get('purpose'))
                if sig in matched_sigs:
                    # Already matched — remove any stale tag
                    if 'unresolvable_reason' in grant:
                        del grant['unresolvable_reason']
                        changed = True
                    total_already_matched += 1
                    continue

                name = grant.get('name', '')
                if is_form_artifact(name):
                    reason = 'form_artifact'
                elif is_daf(name):
                    reason = 'daf_regrant'
                elif is_foundation_to_foundation(name, foundation_names_set):
                    reason = 'foundation_to_foundation'
                else:
                    reason = None
                    total_untagged_unmatched += 1

                if reason:
                    total_tagged[reason] += 1
                    if grant.get('unresolvable_reason') != reason:
                        grant['unresolvable_reason'] = reason
                        changed = True
                else:
                    if 'unresolvable_reason' in grant:
                        del grant['unresolvable_reason']
                        changed = True

        if changed:
            with open(fp, 'w') as f:
                json.dump(data, f, indent=2)

    print(f"\nTagging complete:")
    print(f"  Already matched:          {total_already_matched:,}")
    print(f"  form_artifact:            {total_tagged['form_artifact']:,}")
    print(f"  daf_regrant:              {total_tagged['daf_regrant']:,}")
    print(f"  foundation_to_foundation: {total_tagged['foundation_to_foundation']:,}")
    print(f"  Untagged (real nonprofits, no metrics): {total_untagged_unmatched:,}")
    total_unmatched = sum(total_tagged.values()) + total_untagged_unmatched
    print(f"  Total unmatched top_grants: {total_unmatched:,}")

if __name__ == '__main__':
    main()
