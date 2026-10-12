#!/usr/bin/env python3
"""
rank_ncf.py - Add NCF rank to every NCF organization.

  python3 rank_ncf.py ~/Downloads/ncf_grantees.csv

Rank 1 = the grantee NCF has given the most to (2013-2024 total), counted across
ALL grantees in the file (including churches and small ones that are not listed
in the app), so the rank is a true NCF rank. Adds to metrics.json and ncf_orgs.json:
  ncf_rank, ncf_rank_of
Safe to rerun.
"""
import bisect, csv, json, sys

path = sys.argv[1] if len(sys.argv) > 1 else "ncf_grantees.csv"
totals = sorted(int(r["total_granted"]) for r in csv.DictReader(open(path)))
N = len(totals)

for fn in ("metrics.json", "ncf_orgs.json"):
    data = json.load(open(fn))
    k = 0
    for o in data:
        t = o.get("ncf_total_granted")
        if o.get("ncf") and t:
            o["ncf_rank"] = N - bisect.bisect_right(totals, t) + 1   # 1 + number strictly greater
            o["ncf_rank_of"] = N
            k += 1
    json.dump(data, open(fn, "w"), separators=(",", ":"))
    print(f"{fn}: ranked {k} organizations (of {N} NCF grantees)")
