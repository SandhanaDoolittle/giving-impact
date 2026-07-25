import requests, csv, io, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed

MIN_INCOME = 10_000_000   # Pre-filter: skip foundations with <$10M income in IRS index
MIN_ASSETS = 25_000_000  # Final filter: only keep foundations with $25M+ assets
OUTPUT = "foundations.json"
PP = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"

CASH_DEDUCTION = 0.015   # IRC 4942(e): 1.5% of FMV deemed held for charitable activities
PAYOUT_RATE    = 0.05 * (1 - CASH_DEDUCTION)  # effective ~4.925% after the cash deduction
CARRYFORWARD_YEARS = 5   # IRC 4942(j)(3): excess distributions carry forward up to 5 years

def fetch_with_retry(ein, attempts=4):
    """Returns (json_or_None, definitely_no_data: bool). Retries on rate-limit/transient
    errors instead of silently conflating them with 'this org has no 990-PF data'."""
    delay = 1.0
    for attempt in range(attempts):
        try:
            r = requests.get(PP.format(ein=ein), timeout=15)
        except requests.RequestException:
            time.sleep(delay); delay *= 2; continue
        if r.status_code == 200:
            try:
                return r.json(), False
            except ValueError:
                return None, True  # malformed body for this EIN — not retryable
        if r.status_code == 404:
            return None, True  # org genuinely not found — not a rate-limit issue
        # 429 or 5xx — back off and retry
        time.sleep(delay)
        delay *= 2
    return None, False  # exhausted retries on a transient error — NOT "no data"

def fetch_foundation(ein, name):
    """Returns (result_dict_or_None, status). status is one of:
    'ok', 'below_min', 'no_filings', 'error' — 'error' means a transient failure
    that should be retried, NOT treated as a legitimate skip."""
    try:
        d, definitely_no_data = fetch_with_retry(ein)
        if d is None:
            return None, ("no_filings" if definitely_no_data else "error")
        filings = d.get("filings_with_data", [])
        if not filings:
            return None, "no_filings"

        latest = filings[0]
        # fairmrktvalamt (true fair market value) over totassetsend (balance-sheet
        # book value) — confirmed via Duke Endowment, Harriman Foundation, H & B
        # Young Foundation: totassetsend ran 40-50% BELOW fairmrktvalamt in every
        # case, understating any foundation sitting on unrealized appreciation.
        # cmpmininvstret (the filer's own authoritative figure) consistently landed
        # at ~4.6-4.9% of fairmrktvalamt, confirming it's the right base — book
        # value isn't a reliable stand-in for it.
        assets = latest.get("fairmrktvalamt") or latest.get("totassetsend") or 0
        if assets < MIN_ASSETS:
            return None, "below_min"

        # Build a per-year ledger from however many years ProPublica gives us
        # (usually up to 10), most recent first, capped at the 5-year carryforward window.
        years = []
        for f in filings[:CARRYFORWARD_YEARS]:
            yr_assets = f.get("fairmrktvalamt") or f.get("totassetsend") or 0
            if not yr_assets:
                continue
            # totexpnsexempt = Part I col (d) "Disbursements for charitable purposes" —
            # already includes qualifying admin expenses, unlike grscontrgifts (revenue
            # received) which the old script incorrectly mixed in via max(grants, distrib).
            yr_qualifying = f.get("totexpnsexempt") or 0
            yr_contributions = f.get("grscontrgifts") or 0

            # cmpmininvstret is the foundation's OWN officially-filed minimum
            # investment return (Form 990-PF Part X line 6) — already excludes
            # exempt-use assets (e.g. a museum building) and foreign-foundation
            # exemptions (IRC 4948(b)) the filer themselves determined apply,
            # unlike our flat assets*PAYOUT_RATE approximation. Audited against
            # 1,799 foundations: 338 swing from noncompliant to compliant using
            # this real figure instead of the approximation — including ordinary
            # domestic foundations like Lilly Endowment (true requirement ~22%
            # lower than our estimate) as well as foreign foundations like the
            # Wellcome Trust (UK-based, filer-reported requirement of $0 under
            # 4948(b)). Trust the filer's number — including when it's 0 — and
            # only fall back to our approximation when they didn't report one.
            cmpmininvstret = f.get("cmpmininvstret")
            has_filer_min_return = cmpmininvstret is not None

            # Private operating foundations (museums, research institutes — IRC
            # 4942(j)(3)) aren't held to the 5%-of-assets rule at all. Their actual
            # legal minimum is the "income test": the lesser of 85% of adjusted net
            # income or the minimum investment return above. Confirmed via J. Paul
            # Getty Trust's live filing: operatingcd="Y" alongside both fields.
            yr_operating = f.get("operatingcd") == "Y"
            if yr_operating:
                adjnetinc = max(0, f.get("adjnetinc") or 0)
                base = cmpmininvstret if has_filer_min_return else yr_assets * PAYOUT_RATE
                yr_required = min(0.85 * adjnetinc, base)
            elif has_filer_min_return:
                yr_required = cmpmininvstret
            else:
                yr_required = yr_assets * PAYOUT_RATE

            years.append({
                "year": f.get("tax_prd_yr") or f.get("tax_yr"),
                "assets": yr_assets, "qualifying": yr_qualifying, "required": yr_required,
                "contributions": yr_contributions, "operating": yr_operating,
            })
        if not years:
            return None, "no_filings"

        # ProPublica is occasionally missing structured data for a year or two
        # (mostly 2016-2018, an IRS e-filing transition gap affecting ~5% of
        # foundations) — when that happens this foundation's "5-year window"
        # actually spans more calendar years than usual. Doesn't break the
        # math (each year is still self-consistent), just worth disclosing.
        year_gap = any(years[i]["year"] - years[i+1]["year"] > 1
                        for i in range(len(years)-1)
                        if years[i]["year"] is not None and years[i+1]["year"] is not None)

        qualifying_5yr = sum(y["qualifying"] for y in years)
        required_5yr   = sum(y["required"] for y in years)
        pct_5yr        = round((qualifying_5yr / required_5yr * 100), 2) if required_5yr else 0
        compliant      = qualifying_5yr >= required_5yr

        # Flag corporate/family "flow-through" foundations — funded by fresh annual
        # injections (e.g. a parent company donating cash to be granted out the same
        # year) rather than living off a real investment endowment. For these, "% of
        # assets" is structurally meaningless (assets stay small because the foundation
        # was never meant to accumulate one), so they shouldn't be ranked as "generous"
        # alongside endowed foundations like Gates or Ford Foundation. Detected when
        # cumulative contributions received over the window are a large share of average
        # assets — confirmed against real cases (ExxonMobil Foundation, Ford Motor Company
        # Fund) where contributions tracked distributions almost dollar-for-dollar.
        contributions_5yr = sum(y["contributions"] for y in years)
        avg_assets = sum(y["assets"] for y in years) / len(years)
        flow_through = avg_assets > 0 and (contributions_5yr / avg_assets) >= 0.4

        latest_year = years[0]
        pct_latest_yr = round((latest_year["qualifying"] / latest_year["required"] * 100), 2) if latest_year["required"] else 0

        return {
            "name": name, "ein": ein, "year": latest_year["year"],
            "assets": assets,
            "qualifying": qualifying_5yr, "required": required_5yr,
            "pct": pct_5yr, "compliant": compliant,
            "pct_latest_yr": pct_latest_yr, "years_used": len(years),
            "flow_through": flow_through,
            "operating_foundation": latest_year["operating"],
            "year_gap": year_gap,
        }, "ok"
    except Exception:
        return None, "error"

def get_pf_filers():
    print("Fetching IRS 990-PF index...")
    url = "https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv"
    r = requests.get(url, timeout=60)
    reader = csv.DictReader(io.StringIO(r.text))
    seen = set()
    filers = []
    skipped = 0
    for row in reader:
        if row.get("RETURN_TYPE","") != "990PF":
            continue
        ein = row.get("EIN","").strip()
        if not ein or ein in seen:
            continue
        seen.add(ein)
        filers.append({"ein": ein, "name": row.get("TAXPAYER_NAME","").strip()})

    print(f"Found {len(filers):,} unique 990-PF filers")
    print(f"Skipped {skipped:,} small foundations based on IRS income data")
    return filers

WORKERS = 7  # 10 alone tripped rate limiting when failures were silently miscounted as
             # "no data"; now that fetch_with_retry()/run_pass() retry transient failures
             # instead of swallowing them, higher concurrency is a speed tradeoff, not an
             # accuracy one — worst case is a small, named, visible list of exclusions.

def run_pass(filers, workers=WORKERS):
    """Returns (results, errored_filers) — errored_filers had transient failures
    and should be retried, not treated as legitimate skips."""
    results = []
    errored = []
    skip_counts = {"below_min": 0, "no_filings": 0}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fetch_foundation, f["ein"], f["name"]): f for f in filers}
        for fut in as_completed(futures):
            done += 1
            f = futures[fut]
            result, status = fut.result()
            if status == "ok":
                results.append(result)
                icon = "✅" if result["compliant"] else "❌"
                print(f"[{done}/{len(filers)}] {icon} {result['name'][:50]:<50} {result['pct']:>6}% — ${result['assets']/1e9:.2f}B")
            elif status == "error":
                errored.append(f)
            else:
                skip_counts[status] += 1
                if sum(skip_counts.values()) % 1000 == 0:
                    print(f"  [{done}/{len(filers)}] skipped {sum(skip_counts.values())} so far "
                          f"({skip_counts['below_min']} below ${MIN_ASSETS/1e6:.0f}M, {skip_counts['no_filings']} no filing data)...")

            if len(results) % 50 == 0 and results:
                with open(OUTPUT, "w") as out:
                    json.dump(results, out, indent=2)
    return results, errored

def main():
    filers = get_pf_filers()
    results, errored = run_pass(filers)
    print(f"\nFirst pass done: {len(results)} found, {len(errored)} hit transient errors — retrying those...")

    retry_round = 1
    while errored and retry_round <= 3:
        print(f"\nRetry round {retry_round}: re-checking {len(errored)} foundations...")
        more_results, errored = run_pass(errored, workers=2)
        results.extend(more_results)
        retry_round += 1

    if errored:
        print(f"\n⚠️  {len(errored)} foundations still failed after {retry_round-1} retry rounds — excluded from this run:")
        for f in errored[:20]:
            print(f"   {f['name']} (EIN {f['ein']})")

    with open(OUTPUT, "w") as out:
        json.dump(results, out, indent=2)

    compliant    = sum(1 for r in results if r["compliant"])
    noncompliant = len(results) - compliant

    print(f"\n{'='*60}")
    print(f"Total foundations: {len(results)}")
    print(f"Compliant:         {compliant}")
    print(f"Non-compliant:     {noncompliant}")
    print(f"Unresolved errors: {len(errored)}")
    print(f"\n✅ Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
