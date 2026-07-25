"""
Patch foundations.json: add contributions_pct to all flow_through foundations.
contributions_pct = contributions received (5-yr) / qualifying distributions (5-yr),
capped at 1.0 (100%). Tells you what fraction of giving was funded by fresh inflows
from a parent company/family vs. returns on the endowment.
"""
import requests, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT  = "foundations.json"
PP     = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
YEARS  = 5
WORKERS = 7

def fetch_contributions_pct(ein):
    delay = 1.0
    for attempt in range(4):
        try:
            r = requests.get(PP.format(ein=ein), timeout=15)
        except requests.RequestException:
            time.sleep(delay); delay *= 2; continue
        if r.status_code == 200:
            try:
                d = r.json()
            except ValueError:
                return ein, None
            filings = d.get("filings_with_data", [])[:YEARS]
            contributions_5yr = sum(f.get("grscontrgifts") or 0 for f in filings)
            qualifying_5yr    = sum(f.get("totexpnsexempt") or 0 for f in filings)
            if qualifying_5yr > 0:
                pct = round(min(contributions_5yr / qualifying_5yr, 1.0) * 100, 1)
            else:
                pct = None
            return ein, pct
        if r.status_code == 404:
            return ein, None
        time.sleep(delay); delay *= 2
    return ein, None

def main():
    with open(INPUT) as f:
        data = json.load(f)

    ft = [(i, d) for i, d in enumerate(data) if d.get("flow_through")]
    print(f"Patching {len(ft)} flow-through foundations...")

    ein_to_idx = {d["ein"]: i for i, d in ft}
    eins = list(ein_to_idx.keys())

    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_contributions_pct, ein): ein for ein in eins}
        for fut in as_completed(futures):
            ein, pct = fut.result()
            done += 1
            if pct is not None:
                data[ein_to_idx[ein]]["contributions_pct"] = pct
            if done % 100 == 0 or done == len(eins):
                print(f"  [{done}/{len(eins)}] done...")
                with open(INPUT, "w") as out:
                    json.dump(data, out, indent=2)

    with open(INPUT, "w") as out:
        json.dump(data, out, indent=2)
    print(f"Done. Saved {INPUT}.")

if __name__ == "__main__":
    main()
