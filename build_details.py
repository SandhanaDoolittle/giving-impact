#!/usr/bin/env python3
"""
build_details.py - Turn ncf_990_raw.json into what the cards show.

  python3 build_details.py

Reads   ncf_990_raw.json (from fetch_990_details.py), metrics.json, ncf_orgs.json,
        and ecfa_members.csv if present (columns: ein,name).
Writes  details/d0.json ... d9.json   full back-of-card data, keyed by EIN
                                      (split by last digit so a card only loads ~1MB)
        metrics.json, ncf_orgs.json   get small summary fields used on the front:
                                      program_ratio, eff_pct, ecfa
Safe to rerun.

Metrics (all from the organization's own Form 990, most recent year):
  program_ratio     program spending / total spending
  admin_ratio       management and general / total spending
  fundraising_ratio fundraising / total spending
  cost_to_raise     fundraising spending per $1 of contributions
  reserve_months    cash + savings + investments, in months of spending
  revenue_change    revenue change across the years ProPublica lists (up to 6)
  independent_pct   independent board members / voting board members
  top_pay_pct       highest officer pay / total spending
  eff_pct           where program_ratio ranks among listed organizations in the same
                    cause (100 = best), shown only when 20+ organizations have data
"""
import csv, json, os, re

CAUSE_MIN = 20


def ein9(v):
    d = re.sub(r"\D", "", str(v or ""))
    return d.zfill(9) if d else ""


def norm(s):
    s = re.sub(r"\(.*?\)", " ", (s or "").upper()).replace("&", " AND ")
    drop = {"INC", "THE", "OF", "AND", "A", "AN", "CORP", "CO", "LLC", "LTD", "FOR", "IN", "TO"}
    return " ".join(t for t in re.sub(r"[^A-Z0-9 ]", " ", s).split() if t not in drop)


def ratio(a, b):
    if a is None or not b or b <= 0:
        return None
    r = a / b
    return round(r, 4) if 0 <= r <= 1.5 else None


def derive(raw):
    d = dict(raw)
    tot = raw.get("expenses_total")
    d["program_ratio"] = ratio(raw.get("expenses_program"), tot)
    d["admin_ratio"] = ratio(raw.get("expenses_admin"), tot)
    d["fundraising_ratio"] = ratio(raw.get("expenses_fundraising"), tot)
    fr, co = raw.get("expenses_fundraising"), raw.get("contributions")
    d["cost_to_raise"] = round(fr / co, 3) if fr is not None and co and co > 0 and fr / co <= 2 else None
    if raw.get("liquid_assets") is not None and tot and tot > 0:
        d["reserve_months"] = round(raw["liquid_assets"] / (tot / 12), 1)
    ser = [s for s in raw.get("series", []) if s.get("revenue") and s.get("year")]
    if len(ser) >= 2:
        new, old = ser[0], ser[-1]
        if old["revenue"] > 0 and new["year"] > old["year"]:
            d["revenue_change"] = round((new["revenue"] - old["revenue"]) / old["revenue"], 3)
            d["revenue_change_years"] = [old["year"], new["year"]]
    if raw.get("board") and raw.get("board_independent") is not None:
        d["independent_pct"] = round(raw["board_independent"] / raw["board"], 3) if raw["board"] else None
    if raw.get("top_pay") and tot and tot > 0:
        d["top_pay_pct"] = round(raw["top_pay"] / tot, 4)
    return {k: v for k, v in d.items() if v is not None}


def main():
    raw = json.load(open("ncf_990_raw.json"))
    files = {fn: json.load(open(fn)) for fn in ("metrics.json", "ncf_orgs.json") if os.path.exists(fn)}

    ecfa_ein, ecfa_name = set(), set()
    if os.path.exists("ecfa_members.csv"):
        for r in csv.DictReader(open("ecfa_members.csv")):
            if ein9(r.get("ein")):
                ecfa_ein.add(ein9(r["ein"]))
            if r.get("name"):
                ecfa_name.add(norm(r["name"]))
        print(f"ECFA list: {len(ecfa_ein)} EINs, {len(ecfa_name)} names")

    det = {e: derive(r) for e, r in raw.items() if r.get("found") is not False}

    # efficiency percentile within cause
    by_cause = {}
    for data in files.values():
        for o in data:
            e = ein9(o.get("ein"))
            if o.get("ncf") and e in det and det[e].get("program_ratio") is not None:
                by_cause.setdefault(o.get("cause"), {})[e] = det[e]["program_ratio"]
    pct = {}
    for cause, m in by_cause.items():
        if len(m) < CAUSE_MIN:
            continue
        vals = sorted(m.values())
        for e, v in m.items():
            below = sum(1 for x in vals if x < v)
            pct[e] = round(100 * below / (len(vals) - 1)) if len(vals) > 1 else 50

    n_ecfa = n_sum = 0
    for fn, data in files.items():
        for o in data:
            e = ein9(o.get("ein"))
            is_ecfa = e in ecfa_ein or (not e and norm(o.get("name")) in ecfa_name) or norm(o.get("name")) in ecfa_name
            if is_ecfa and (ecfa_ein or ecfa_name):
                o["ecfa"] = True
                n_ecfa += 1
                if e in det:
                    det[e]["ecfa"] = True
            if e in det:
                dd = det[e]
                if dd.get("program_ratio") is not None:
                    o["program_ratio"] = dd["program_ratio"]
                    n_sum += 1
                if e in pct:
                    o["eff_pct"] = pct[e]
                    dd["eff_pct"] = pct[e]
        json.dump(data, open(fn, "w"), separators=(",", ":"))

    os.makedirs("details", exist_ok=True)
    shards = {str(i): {} for i in range(10)}
    for e, dd in det.items():
        shards[e[-1]][e] = dd
    for k, v in shards.items():
        json.dump(v, open(f"details/d{k}.json", "w"), separators=(",", ":"))
    print(f"{len(det)} organizations with detail; {n_sum} with a program ratio; "
          f"{len(pct)} with an efficiency percentile; {n_ecfa} marked ECFA")
    print("Wrote details/d0.json ... d9.json and updated metrics.json, ncf_orgs.json")


if __name__ == "__main__":
    main()
