import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

print(f"Starting entries: {len(data)}")

def add_aliases(entries, name_match, new_aliases):
    for e in entries:
        if e["name"] == name_match:
            pp = e.get("pp_name") or []
            if isinstance(pp, str): pp = [pp]
            for a in new_aliases:
                if a not in pp: pp.append(a)
            e["pp_name"] = pp
            return True
    print(f"WARNING: not found: {name_match!r}")
    return False

def fill_metrics(entries, ein_match, updates):
    """Fill in missing metric fields on an existing entry by EIN."""
    for e in entries:
        if str(e.get("ein", "")).strip() == str(ein_match):
            for k, v in updates.items():
                e[k] = v
            print(f"UPDATED: {e['name']} (EIN {ein_match})")
            return True
    print(f"WARNING: EIN not found: {ein_match}")
    return False

# ── FILL IN EXISTING INCOMPLETE ENTRIES ────────────────────────────────────────

# Earthjustice — environmental litigation ($148M expenses, 2023)
fill_metrics(data, "941730465", {
    "primary_metric_label": "one person protected by Earthjustice environmental litigation",
    "primary_metric_value": 100000000,
    "primary_metric_unit": "people protected by Earthjustice's environmental lawsuits defending clean air, clean water, climate, and wildlife — winning 80%+ of cases",
    "cost_per_outcome_usd": 1.48,
    "impact_per_100_usd": 67.6,
    "confidence": "low",
    "source": "Earthjustice Annual Report + ProPublica",
    "source_detail": "Earthjustice 2023: $148M expenses. America's largest nonprofit environmental law firm, with 800+ active cases protecting air quality, water, climate, and wildlife from government and corporate rollbacks.",
    "extraction_note": "$148,016,730 / 100,000,000 estimated people protected = $1.48/person. Earthjustice wins 80%+ of cases; many are nationwide rulings (EPA air standards, Clean Water Act) protecting 300M+ Americans. Low-confidence estimate due to difficulty quantifying beneficiaries of legal wins.",
    "impact_description": "one person protected by Earthjustice's environmental litigation — America's largest nonprofit environmental law firm, winning 80%+ of 800+ active cases defending clean air standards, clean water regulations, climate policy, and threatened wildlife",
    "annual_expenses_usd": 148016730,
    "revenue_year": 2023,
    "pp_name": [
        "Earthjustice",
        "Earthjustice Legal Defense Fund",
        "Sierra Club Legal Defense Fund",
    ],
})

# Natural Resources Defense Council (NRDC) — environmental advocacy ($226.9M expenses, 2023)
fill_metrics(data, "132654926", {
    "primary_metric_label": "one person engaged in NRDC environmental advocacy and campaigns",
    "primary_metric_value": 5000000,
    "primary_metric_unit": "people engaged through NRDC's environmental advocacy reaching 3M+ members plus millions more through policy campaigns on climate, clean air, and ocean protection",
    "cost_per_outcome_usd": 45,
    "impact_per_100_usd": 2.2,
    "confidence": "low",
    "source": "NRDC Annual Report + ProPublica",
    "source_detail": "Natural Resources Defense Council 2023: $226.9M expenses. 3M+ members. Combines litigation, science, policy advocacy, and communications to protect environment and public health at federal and state level.",
    "extraction_note": "$226,866,168 / 5,000,000 people engaged = $45.4/person. NRDC's policy wins on clean air, climate, and water benefit far more than direct members — including landmark EPA rulemakings and international climate negotiations.",
    "impact_description": "one person engaged by NRDC's environmental advocacy — with 3M members and a team of 700+ lawyers, scientists, and policy experts, NRDC shapes clean air, clean water, and climate policy at the highest levels of government",
    "annual_expenses_usd": 226866168,
    "revenue_year": 2023,
    "pp_name": [
        "Natural Resources Defense Council",
        "Natural Resources Defense Council Inc",
        "Nrdc",
    ],
})

# Feeding America — national food bank network ($4.93B expenses, 2023)
fill_metrics(data, "363673599", {
    "primary_metric_label": "one person receiving food assistance through the Feeding America network",
    "primary_metric_value": 40000000,
    "primary_metric_unit": "Americans receiving food assistance through Feeding America's 200+ food banks and 60,000+ food pantries — providing 6.6 billion meals/year",
    "cost_per_outcome_usd": 123,
    "impact_per_100_usd": 0.811,
    "confidence": "medium",
    "source": "Feeding America Annual Report + ProPublica",
    "source_detail": "Feeding America 2023: $4.93B expenses (mostly in-kind food). Largest hunger relief org in the US: 200+ food banks, 60,000+ partner agencies, serving 40M+ Americans/year including 12M children and 7M seniors.",
    "extraction_note": "$4,933,690,967 / 40,000,000 people served = $123.3/person. Most expenses are in-kind food donations passed through; cash cost per person is ~$8-10. Feeding America coordinates national food rescue, government commodity distribution, and emergency hunger response.",
    "impact_description": "one American receiving food assistance through Feeding America's 200+ food bank network — the nation's largest hunger-relief organization providing 6.6 billion meals/year to 40M people including 12M children",
    "annual_expenses_usd": 4933690967,
    "revenue_year": 2023,
    "pp_name": [
        "Feeding America",
        "America Second Harvest",
        "Second Harvest",
    ],
})

# Rocky Mountain Institute — clean energy transition think tank ($141.2M expenses, 2023)
fill_metrics(data, "742244146", {
    "primary_metric_label": "one person in a community transitioning to clean energy with RMI technical assistance",
    "primary_metric_value": 50000000,
    "primary_metric_unit": "people in communities and markets transitioning to clean energy through Rocky Mountain Institute's technical assistance, policy research, and coalition-building with utilities, corporations, and governments",
    "cost_per_outcome_usd": 2.82,
    "impact_per_100_usd": 35.4,
    "confidence": "low",
    "source": "RMI Annual Report + ProPublica",
    "source_detail": "Rocky Mountain Institute 2023: $141.2M expenses. Influential clean energy think tank founded by Amory Lovins. Works with 500+ corporations, utilities, and governments globally to accelerate the clean energy transition across buildings, transportation, and electricity.",
    "extraction_note": "$141,157,018 / 50,000,000 people in served markets = $2.82/person. RMI's work is multiplied through government adoption of its research (IRA provisions, utility filings, building codes) affecting many millions. Very low confidence in beneficiary count.",
    "impact_description": "one person in a market or community benefiting from Rocky Mountain Institute's clean energy transition work — a globally influential think tank advising 500+ utilities, corporations, and governments on eliminating fossil fuel use in electricity, buildings, and transportation",
    "annual_expenses_usd": 141157018,
    "revenue_year": 2023,
    "pp_name": [
        "Rocky Mountain Institute",
        "Rmi",
    ],
})

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Chapman University — private university in Orange, CA
  {
    "name": "Chapman University",
    "ein": "951643992",
    "pp_name": [
      "Chapman University",
      "Chapman Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Chapman University student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Chapman University",
    "cost_per_outcome_usd": 37000,
    "impact_per_100_usd": 0.00270,
    "confidence": "medium",
    "source": "Chapman University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Chapman University 2023: $650M expenses. Private university in Orange, CA with ~9,500 students. Known for film, business, law, and health sciences. CDS 2023-24 avg institutional need-based grant ~$37,000.",
    "extraction_note": "CDS 2023-24 Chapman avg institutional need-based grant used. Chapman's Dodge College of Film and Media Arts is among the top-ranked film schools in the US.",
    "impact_description": "one year of need-based financial aid for one Chapman University student (avg ~$37,000 institutional grant) — a private university in Orange County, CA with a top-ranked film school, law school, and health sciences programs",
    "annual_expenses_usd": 650111702,
    "revenue_year": 2023,
  },

  # Temple University — Philadelphia public research university
  {
    "name": "Temple University",
    "ein": "231365971",
    "pp_name": [
      "Temple University Of The Commonwealth System Of Higher Educ",
      "Temple University",
      "Temple Univ",
      "Temple University Commonwealth",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Temple University student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Temple University",
    "cost_per_outcome_usd": 14000,
    "impact_per_100_usd": 0.00714,
    "confidence": "medium",
    "source": "Temple University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Temple University 2023: $1.48B expenses. Public research university in Philadelphia with ~35,000 students. CDS 2023-24 avg institutional need-based grant ~$14,000. Known for law, medicine, pharmacy, and education.",
    "extraction_note": "CDS 2023-24 Temple avg institutional need-based grant used. Temple serves a highly diverse urban student body; ~70% receive some form of financial aid. Temple's medical school and law school are among the largest in the US.",
    "impact_description": "one year of need-based financial aid for one Temple University student (avg ~$14,000 institutional grant) — Philadelphia's flagship public research university with 35,000 students and nationally ranked programs in law, medicine, pharmacy, and business",
    "annual_expenses_usd": 1479634000,
    "revenue_year": 2023,
  },

  # myAgro Farms — mobile savings platform for smallholder African farmers
  {
    "name": "myAgro Farms",
    "ein": "455267449",
    "pp_name": [
      "Myagro Farms",
      "Myagro",
      "My Agro",
    ],
    "cause": "community",
    "primary_metric_label": "one smallholder African farmer enrolled in myAgro's mobile savings and inputs program",
    "primary_metric_value": 100000,
    "primary_metric_unit": "smallholder farmers in Mali, Senegal, and Tanzania receiving affordable inputs and training through myAgro's layaway mobile savings platform",
    "cost_per_outcome_usd": 90,
    "impact_per_100_usd": 1.11,
    "confidence": "medium",
    "source": "myAgro Annual Report + ProPublica",
    "source_detail": "myAgro Farms 2023: $9M expenses. Enables smallholder farmers to save incrementally via mobile payments for certified seeds, fertilizer, and training, boosting yields by 50-100% and income by ~$125/season for ~100K+ farmers.",
    "extraction_note": "$9,020,869 / 100,000 farmers = $90.2/farmer. myAgro targets rural women farmers in West Africa with no credit history; the layaway model avoids debt and MFI-style risks. GiveWell has recommended myAgro for cost-effective rural poverty reduction.",
    "impact_description": "one smallholder farmer in Mali, Senegal, or Tanzania enrolled in myAgro's mobile savings program — a layaway platform providing certified seeds, fertilizer, and farming training that increases crop yields by 50-100% and family income by ~$125/season",
    "annual_expenses_usd": 9020869,
    "revenue_year": 2023,
  },

]

# De-duplicate by EIN
existing_eins = {str(e.get("ein", "")).strip() for e in data}
added = 0
for entry in new_entries:
    ein = str(entry.get("ein", "")).strip()
    if ein and ein in existing_eins:
        print(f"SKIP (EIN exists): {entry['name']} ({ein})")
        continue
    data.append(entry)
    existing_eins.add(ein)
    added += 1

with open(METRICS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"New entries added: {added}")
print(f"Total entries now: {len(data)}")
