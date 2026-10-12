#!/usr/bin/env python3
"""
build_ncf_entries.py - Turn ncf_new.json + ncf_enriched.json into app-ready
entries in ncf_orgs.json (same fields the Giving Impact cards already use).

  python3 build_ncf_entries.py

Rules
  - Category (NTEE) maps to a sector AND expenses >= $500K  -> auto-estimated
    impact, clearly labeled, same method as build_auto_estimates.py.
  - Grantmakers (NTEE T), no category, small, or not on ProPublica -> listed with
    data_available=false, so they are searchable but show no impact number.
"""
import importlib.util, json, re

spec = importlib.util.spec_from_file_location("bae", "build_auto_estimates.py")
bae = importlib.util.module_from_spec(spec); spec.loader.exec_module(bae)
NTEE_MAP = bae.NTEE_MAP
MIN_EXP = 500_000
SMALL = {"a", "an", "and", "at", "for", "in", "of", "on", "or", "the", "to", "by"}


def title(s):
    if s != s.upper():
        return s
    out = []
    for i, w in enumerate(s.lower().split()):
        out.append(w if (i and w in SMALL) else w[:1].upper() + w[1:])
    return re.sub(r"\b(Inc|Llc|Usa|Ymca|Ywca|Cru)\b", lambda m: m.group(1).upper() if m.group(1) != "Inc" else "Inc", " ".join(out))


def main():
    new = json.load(open("ncf_new.json"))
    enr = json.load(open("ncf_enriched.json"))
    out, est, nodata = [], 0, 0
    for n in new:
        e = enr.get(n["ein"])
        if e is None:
            continue                                     # not looked up yet
        found = e.get("found")
        name = title(e.get("name") or n["name"]) if found else title(n["name"])
        base = {"name": name, "ein": n["ein"],
                "state": (e.get("state") if found else "") or n["state"],
                "ncf": True, "ncf_total_granted": n["ncf_total_granted"],
                "ncf_years_seen": n["ncf_years_seen"], "ncf_latest_year": n["ncf_latest_year"]}
        ntee = ((e.get("ntee") or "") if found else "").strip()
        key = ntee[:1].upper()
        exp = e.get("expenses") if found else None
        if found and key in NTEE_MAP and key not in ("T", "Y") and exp and exp >= MIN_EXP:
            cause, unit, cpp, label = NTEE_MAP[key]
            base.update({
                "cause": cause, "pass_through": False,
                "primary_metric_label": label,
                "primary_metric_value": int(exp / cpp),
                "primary_metric_unit": unit,
                "cost_per_outcome_usd": cpp,
                "impact_per_100_usd": round(100 / cpp, 6),
                "confidence": "auto", "auto_estimated": True,
                "source": "ProPublica Nonprofit Explorer + NTEE sector benchmarks",
                "source_detail": f"{name}. Annual expenses ${exp:,.0f} ({e.get('year') or 'recent'}). "
                                 f"NTEE {ntee}; sector benchmark ${cpp:,.0f}/person.",
                "extraction_note": f"AUTO-ESTIMATED, not hand-researched. Uses the ${cpp:,.0f}/person "
                                   f"sector average for NTEE {ntee}. Actual impact per dollar may differ a lot.",
                "impact_description": f"one person reached through {name}'s programs (sector-estimated, {unit})",
                "annual_expenses_usd": exp, "revenue_year": e.get("year"),
            })
            est += 1
        else:
            cause = NTEE_MAP[key][0] if key in NTEE_MAP and key not in ("T", "Y") else "community"
            base.update({"cause": cause, "data_available": False, "impact_per_100_usd": None,
                         "pass_through": key == "T",
                         "reliability": "NCF grantee. No impact estimate available. Contact the organization directly."})
            if exp:
                base["annual_expenses_usd"] = exp
                base["revenue_year"] = e.get("year")
            nodata += 1
        out.append(base)
    json.dump(out, open("ncf_orgs.json", "w"), separators=(",", ":"))
    print(f"{len(out)} orgs: {est} auto-estimated, {nodata} listed with no estimate")


if __name__ == "__main__":
    main()
