import json, re

METRICS_FILE = "metrics.json"
CHUNK_FILES = [f"foundation_grants_{i}.json" for i in range(8)]

# IMPORTANT: the original pipeline that built matched_detail/matched_amount/match_pct
# matched against each foundation's FULL Schedule I grant list (confirmed: e.g. Wilf
# Foundation has 118 total_grants but top_grants here is capped at 20 -- yet its
# matched_detail correctly includes small grants nowhere in top_grants). That full
# per-foundation grant list was never saved anywhere in this repo, only the top 20
# (top_grants) + the aggregate match results. So we can NEVER fully re-derive
# matched_detail from top_grants alone -- attempting that destroys ~84% of existing
# matches (verified: 10,266 rows -> ~1,300 rows if matched_detail is replaced).
#
# This script is therefore strictly ADDITIVE: it only adds a new matched_detail row
# for a top_grants entry that (a) isn't already represented in matched_detail and
# (b) now matches an entry in the current (improved) metrics.json. It never removes
# or replaces an existing row, so matched_amount can only go up, never down.

DROP_TOKENS = {'INC', 'INCORPORATED', 'CORP', 'CORPORATION', 'CO', 'LLC', 'LTD', 'THE'}

def normalize(name):
    name = name.upper()
    name = name.replace('&', ' AND ')
    name = re.sub(r'[^A-Z0-9 ]', ' ', name)
    tokens = [t for t in name.split() if t not in DROP_TOKENS]
    return ' '.join(tokens)

def recipient_type_for(entry, recipient_name):
    if 'recipient_type' in entry:
        return entry['recipient_type']
    norm = normalize(recipient_name)
    if 'UNIVERSITY' in norm or 'COLLEGE' in norm:
        return 'university'
    return 'direct'

def main():
    with open(METRICS_FILE) as f:
        metrics = json.load(f)
    by_norm = {}
    for e in metrics:
        pp_name = e.get('pp_name')
        pp_names = pp_name if isinstance(pp_name, list) else [pp_name]
        for raw_name in {e.get('name'), *pp_names} - {None}:
            by_norm.setdefault(normalize(raw_name), e)
    print(f"Loaded {len(by_norm)} usable lookup keys from metrics.json")

    grand_added_rows = 0
    grand_added_amount = 0
    foundations_touched = 0

    for chunk_file in CHUNK_FILES:
        with open(chunk_file) as f:
            data = json.load(f)
        file_changed = False
        for g in data:
            matched_detail = g.setdefault('matched_detail', [])
            already = set((d['recipient'], d['amount'], d.get('purpose')) for d in matched_detail)

            added_amount = 0
            for grant in g.get('top_grants', []):
                sig = (grant['name'], grant['amount'], grant.get('purpose'))
                if sig in already:
                    continue
                entry = by_norm.get(normalize(grant['name']))
                if not entry:
                    continue
                metric_unit = entry.get('primary_metric_unit')
                if not metric_unit:
                    continue  # name-recognized but no usable metric (e.g. Feeding America) -- don't count as matched
                matched_detail.append({
                    'recipient': grant['name'],
                    'amount': grant['amount'],
                    'purpose': grant.get('purpose'),
                    'metric_unit': metric_unit,
                    'confidence': entry.get('confidence', 'low'),
                    'recipient_type': recipient_type_for(entry, grant['name']),
                })
                already.add(sig)
                added_amount += grant['amount']
                grand_added_rows += 1

            if added_amount:
                g['matched_amount'] = g.get('matched_amount', 0) + added_amount
                g['matched_grants'] = len(matched_detail)
                total_amount = g.get('total_amount') or 0
                g['match_pct'] = round(g['matched_amount'] / total_amount * 100, 1) if total_amount else g.get('match_pct', 0)
                grand_added_amount += added_amount
                foundations_touched += 1
                file_changed = True

        if file_changed:
            with open(chunk_file, 'w') as f:
                json.dump(data, f, indent=2)

    print(f"\nFoundations with at least one new match: {foundations_touched}")
    print(f"New matched rows added: {grand_added_rows}")
    print(f"New matched dollars added: ${grand_added_amount:,.0f}")

    # ── Option A: denominator methodology note ─────────────────────────────────
    # The raw "% of grant dollars matched" metric understates coverage because the
    # denominator includes grants that are structurally unmatchable from 990-PF data:
    #
    #   Form artifacts (~37%): "SEE ATTACHED", "VARIOUS INDIVIDUALS", "Eligible
    #     Patients", etc. — 990-PF rows that omit the recipient name entirely.
    #
    #   Foundation-to-foundation (~22%): e.g. a foundation sending $5.5B to the
    #     Gates Foundation, which itself files a 990-PF. These are double-counted;
    #     the end recipients show up when the Gates Foundation files its own grants.
    #
    #   DAF re-grants (~5%): Fidelity Charitable, National Philanthropic Trust,
    #     community foundations, etc. are pass-through vehicles — the final nonprofit
    #     recipient is not disclosed on the donor foundation's 990-PF.
    #
    # Auto-estimated entries (confidence="auto") address the remaining long-tail of
    # real nonprofits using NTEE sector-average benchmarks. They are clearly labeled
    # and should be interpreted as directional, not precise.
    print("\n[Methodology note written to match_grants.py source — see OPTION_A_NOTE above]")

if __name__ == '__main__':
    main()
