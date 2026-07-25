import requests, json, time

FOUNDATIONS = [
    {"name": "Gates Foundation",          "ein": "562618866"},
    {"name": "Ford Foundation",            "ein": "131684331"},
    {"name": "Rockefeller Foundation",     "ein": "131659629"},
    {"name": "Hewlett Foundation",         "ein": "941655673"},
    {"name": "MacArthur Foundation",       "ein": "237093598"},
    {"name": "Kellogg Foundation",         "ein": "381359264"},
    {"name": "Walton Family Foundation",   "ein": "133441466"},
    {"name": "Bloomberg Philanthropies",   "ein": "205602483"},
    {"name": "Packard Foundation",         "ein": "942278431"},
    {"name": "Robert Wood Johnson Found.", "ein": "226029397"},
]

PP = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"

def fetch_foundation(ein, name):
    print(f"\n→ {name}")
    r = requests.get(PP.format(ein=ein), timeout=15)
    d = r.json()
    filings = d.get("filings_with_data", [])
    if not filings:
        print("  ⚠️  No filing data"); return None

    f = filings[0]
    assets   = f.get("totassetsend") or f.get("fairmrktvalamt") or 0
    grants   = f.get("grscontrgifts") or 0
    distrib  = f.get("totexpnsexempt") or f.get("distribamt") or 0
    qualifying = max(grants, distrib)
    year     = f.get("tax_prd_yr") or f.get("tax_yr")
    required = assets * 0.05
    pct      = (qualifying / assets * 100) if assets else 0
    compliant = qualifying >= required

    print(f"  Year:        {year}")
    print(f"  Assets:      ${assets:>15,.0f}")
    print(f"  Qualifying:  ${qualifying:>15,.0f}")
    print(f"  Required 5%: ${required:>15,.0f}")
    print(f"  Payout:      {pct:.1f}%  {'✅' if compliant else '❌'}")

    return {
        "name": name, "ein": ein, "year": year,
        "assets": assets, "grants": grants,
        "qualifying": qualifying, "required": required,
        "pct": round(pct, 2), "compliant": compliant,
    }

def main():
    print("Fetching foundation data...\n")
    results = []
    for f in FOUNDATIONS:
        r = fetch_foundation(f["ein"], f["name"])
        if r: results.append(r)
        time.sleep(0.4)

    print("\n" + "="*65)
    print(f"{'Foundation':<35} {'Assets':>10} {'Payout':>8} {'OK':>4}")
    print("-"*65)
    for r in results:
        a = r['assets']
        s = f"${a/1e9:.1f}B" if a >= 1e9 else f"${a/1e6:.0f}M"
        print(f"{r['name']:<35} {s:>10} {r['pct']:>7.1f}% {'✅' if r['compliant'] else '❌'}")

    with open("foundations.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Saved {len(results)} foundations → foundations.json")

if __name__ == "__main__":
    main()
