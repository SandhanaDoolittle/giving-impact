import json, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from scale_foundations import fetch_with_retry, CARRYFORWARD_YEARS, OUTPUT

ASSET_THRESHOLD = 100_000_000
MAX_OBJECT_IDS_TO_SCAN = 12  # comfortably covers a 5-year window + the occasional gap

def get_object_ids(ein):
    r = requests.get(f"https://projects.propublica.org/nonprofits/organizations/{ein}", timeout=20)
    seen, ordered = set(), []
    for m in re.finditer(rf"/organizations/{ein}/(\d+)/IRS990PF", r.text):
        oid = m.group(1)
        if oid not in seen:
            seen.add(oid)
            ordered.append(oid)
    return ordered  # preserves page order = most recent first

def get_fiscal_year(ein, object_id):
    r = requests.get(f"https://projects.propublica.org/nonprofits/organizations/{ein}/{object_id}/IRS990PF", timeout=20)
    m = re.search(r"fiscal year ending [A-Za-z]+\. (\d{4})", r.text)
    return int(m.group(1)) if m else None

def get_line_value(window, label_token):
    """The rendered table is pipe-delimited as: | <line label> | | <value> |
    (exactly two pipes between the line-number label and its value, confirmed
    against Ford Foundation and Gates Foundation filings). Line labels like
    "1b"/"3a" contain digits themselves, so matching them precisely with pipe
    boundaries is required — a naive 'first number after this label' regex
    grabs the line number itself instead of the value two cells over.
    Single-digit labels like "2" (no sub-letter) also appear a SECOND time as
    a row marker preceding their own description, before the real value cell —
    take the LAST match, which consistently lands on the value, not the label."""
    pattern = rf"\|\s*{re.escape(label_token)}\s*\|\s*\|\s*([^|]*?)\s*\|"
    matches = re.findall(pattern, window)
    if not matches:
        return 0
    digits = re.sub(r"[^\d]", "", matches[-1])
    return int(digits) if digits else 0

def get_pri_setaside_addon(object_id):
    """Returns (line_1b_pri + line_2_assets + line_3a/3b_setaside), or None if unparseable."""
    r = requests.get(f"https://projects.propublica.org/nonprofits/full_text/{object_id}/IRS990PF", timeout=90)
    html = r.text
    text = re.sub("<[^>]+>", "|", html)
    text = re.sub(r"\|+", " | ", text)
    text = re.sub(r"\s+", " ", text)
    idx = text.find("Expenses, contributions, gifts, etc.")
    if idx == -1:
        return None
    window = text[idx:idx+2500]

    pri = get_line_value(window, "1b")
    assets_acquired = get_line_value(window, "2")
    setaside_a = get_line_value(window, "3a")
    setaside_b = get_line_value(window, "3b")
    return pri + assets_acquired + setaside_a + setaside_b

def patch_one(entry):
    ein, name = entry["ein"], entry["name"]
    d, _ = fetch_with_retry(ein)
    if d is None:
        return entry, "fetch_failed"
    filings = d.get("filings_with_data", [])
    if not filings:
        return entry, "no_filings"

    # Rebuild the same 5-year window scale_foundations.py would use
    target_years = []
    for f in filings[:CARRYFORWARD_YEARS]:
        yr = f.get("tax_prd_yr") or f.get("tax_yr")
        if yr:
            target_years.append(yr)
    if not target_years:
        return entry, "no_usable_years"

    try:
        object_ids = get_object_ids(ein)[:MAX_OBJECT_IDS_TO_SCAN]
    except Exception:
        return entry, "object_id_fetch_failed"

    target_year_set = set(target_years)
    year_to_oid = {}
    for oid in object_ids:
        if target_year_set.issubset(year_to_oid.keys()):
            break
        try:
            yr = get_fiscal_year(ein, oid)
        except Exception:
            continue
        if yr is not None and yr not in year_to_oid:
            year_to_oid[yr] = oid

    total_addon = 0
    years_patched = 0
    for yr in target_years:
        oid = year_to_oid.get(yr)
        if not oid:
            continue
        try:
            addon = get_pri_setaside_addon(oid)
        except Exception:
            addon = None
        if addon:
            total_addon += addon
            years_patched += 1

    if total_addon == 0:
        return entry, "no_addon_found"

    new_qualifying = entry["qualifying"] + total_addon
    new_pct = round(new_qualifying / entry["required"] * 100, 2) if entry["required"] else entry["pct"]
    new_compliant = new_qualifying >= entry["required"]
    updated = dict(entry)
    updated["qualifying"] = new_qualifying
    updated["pct"] = new_pct
    updated["compliant"] = new_compliant
    updated["pri_setaside_addon"] = total_addon
    return updated, f"patched(+{total_addon:,}, {years_patched}yrs)"

def main():
    data = json.load(open(OUTPUT))
    big = [d for d in data if d["assets"] >= ASSET_THRESHOLD]
    print(f"Checking {len(big):,} foundations with assets >= ${ASSET_THRESHOLD:,}...")

    by_ein = {d["ein"]: d for d in data}
    done = 0
    flips = 0
    addons_found = 0
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(patch_one, e): e for e in big}
        for fut in as_completed(futures):
            done += 1
            updated, status = fut.result()
            if status.startswith("patched"):
                addons_found += 1
                old = by_ein[updated["ein"]]
                if old["compliant"] != updated["compliant"]:
                    flips += 1
                    print(f"[{done}/{len(big)}] FLIP {updated['name'][:45]:<45} {old['compliant']}->{updated['compliant']}  {status}")
                else:
                    print(f"[{done}/{len(big)}] {updated['name'][:45]:<45} {status}")
                by_ein[updated["ein"]] = updated
            if done % 200 == 0:
                print(f"  ...{done}/{len(big)} checked, {addons_found} had a real addon, {flips} flipped compliance")

    out = [by_ein[d["ein"]] for d in data]
    with open(OUTPUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Checked: {len(big):,}  |  Found a real PRI/set-aside addon: {addons_found}  |  Compliance flipped: {flips}")
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
