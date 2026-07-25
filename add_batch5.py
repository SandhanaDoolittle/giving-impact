import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

print(f"Starting entries: {len(data)}")

def add_aliases(entries, name_match, new_aliases):
    for e in entries:
        if e["name"] == name_match:
            pp = e.get("pp_name", [])
            if isinstance(pp, str):
                pp = [pp] if pp else []
            for a in new_aliases:
                if a not in pp:
                    pp.append(a)
            e["pp_name"] = pp
            return True
    print(f"WARNING: Could not find entry '{name_match}'")
    return False

# ── ALIAS FIX ─────────────────────────────────────────────────────────────────
# University of Nebraska Foundation: grant text "UNIVERSITY OF NEBRASKA-OMAHA"
# normalizes to "UNIVERSITY OF NEBRASKA OMAHA" — add that alias
add_aliases(data, "University of Nebraska", [
    "University Of Nebraska Omaha",
    "University Of Nebraska At Omaha",
    "University Of Nebraska Lincoln",
    "University Of Nebraska Foundation",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Memorial Sloan Kettering Cancer Center
  {
    "name": "Memorial Sloan Kettering Cancer Center",
    "ein": "131924236",
    "pp_name": [
      "Memorial Sloan Kettering Cancer Center",
      "Memorial Sloan-Kettering Cancer Center",
      "Memorial Hospital For Cancer And Allied Diseases",
      "Sloan Kettering Institute For Cancer Research",
      "Msk Cancer Center",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at MSK",
    "primary_metric_value": 530000,
    "primary_metric_unit": "patient encounters at Memorial Sloan Kettering Cancer Center",
    "cost_per_outcome_usd": 2845,
    "impact_per_100_usd": 0.035,
    "confidence": "medium",
    "source": "MSK Annual Report 2023 + ProPublica",
    "source_detail": "MSK 2023: $1.51B total expenses; ~530K patient encounters (28K inpatient + ~500K outpatient visits) per year",
    "extraction_note": "$1,507,732,713 / 530,000 = $2,845/encounter. MSK treats ~500 new patients per day across inpatient and outpatient settings.",
    "impact_description": "one patient encounter at Memorial Sloan Kettering Cancer Center, one of the world's premier cancer treatment and research institutions",
    "annual_expenses_usd": 1507732713,
    "revenue_year": 2023,
  },

  # Musical Arts Association (Cleveland Orchestra)
  {
    "name": "Musical Arts Association",
    "ein": "340714468",
    "pp_name": [
      "The Musical Arts Association",
      "Musical Arts Association",
      "Cleveland Orchestra",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one Cleveland Orchestra performance attendee",
    "primary_metric_value": 300000,
    "primary_metric_unit": "attendees at Cleveland Orchestra concerts and educational programs",
    "cost_per_outcome_usd": 222,
    "impact_per_100_usd": 0.45,
    "confidence": "medium",
    "source": "Cleveland Orchestra Annual Report + ProPublica",
    "source_detail": "Musical Arts Association 2023: $66.6M expenses. ~150 concerts/year at Severance Hall (2,000 seats) + Blossom Music Center + touring = ~300K attendees.",
    "extraction_note": "$66,565,856 / 300,000 = $221.9/attendee. Includes Blossom summer season and education programs.",
    "impact_description": "one person attending a Cleveland Orchestra concert or educational program, one of the world's top-ranked orchestras",
    "annual_expenses_usd": 66565856,
    "revenue_year": 2023,
  },

  # Monterey Bay Aquarium Foundation
  {
    "name": "Monterey Bay Aquarium",
    "ein": "942487469",
    "pp_name": [
      "Monterey Bay Aquarium Foundation",
      "Monterey Bay Aquarium",
    ],
    "cause": "environment",
    "primary_metric_label": "one aquarium visitor",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "visitors to Monterey Bay Aquarium plus ocean conservation program reach",
    "cost_per_outcome_usd": 54,
    "impact_per_100_usd": 1.84,
    "confidence": "medium",
    "source": "Monterey Bay Aquarium Annual Report 2023 + ProPublica",
    "source_detail": "MBA Foundation 2023: $108.8M expenses. ~2M visitors/year. Also operates Seafood Watch and global ocean conservation programs.",
    "extraction_note": "$108,770,852 / 2,000,000 = $54.4/visitor. MBA also funds MBARI (separate org) and Seafood Watch impact.",
    "impact_description": "one visitor experiencing Monterey Bay Aquarium's exhibits plus Monterey Bay Aquarium's ocean conservation science and Seafood Watch sustainability program",
    "annual_expenses_usd": 108770852,
    "revenue_year": 2023,
  },

  # Monterey Bay Aquarium Research Institute
  {
    "name": "Monterey Bay Aquarium Research Institute",
    "ein": "770150580",
    "pp_name": [
      "Monterey Bay Aquarium Research Institute",
      "Mbari",
    ],
    "cause": "environment",
    "primary_metric_label": "one ocean science publication or technology deployment",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "people benefiting from MBARI ocean science research and open-access educational resources",
    "cost_per_outcome_usd": 33,
    "impact_per_100_usd": 3.0,
    "confidence": "low",
    "source": "MBARI Annual Report 2023 + ProPublica",
    "source_detail": "MBARI 2023: $66.5M expenses. Publishes ~100 peer-reviewed papers/year; open-access datasets and tools used by millions worldwide.",
    "extraction_note": "MBARI's peer-reviewed publications and open-access tools reach ~2M researchers/students/public globally. $66.5M / 2M = $33.25/person. Confidence low — indirect impact.",
    "impact_description": "one person benefiting from MBARI's deep-sea research, open-access oceanographic data, and technology (ROVs, ocean sensors) that advances global understanding of the ocean",
    "annual_expenses_usd": 66546177,
    "revenue_year": 2023,
  },

  # Regenstrief Institute
  {
    "name": "Regenstrief Institute",
    "ein": "300007730",
    "pp_name": [
      "Regenstrief Institute Inc",
      "Regenstrief Institute",
    ],
    "cause": "health",
    "primary_metric_label": "one patient with better-coordinated care through Regenstrief systems",
    "primary_metric_value": 6000000,
    "primary_metric_unit": "Indiana patients with health records in Regenstrief-powered Indiana Health Information Exchange",
    "cost_per_outcome_usd": 5,
    "impact_per_100_usd": 21.5,
    "confidence": "low",
    "source": "Regenstrief Institute Annual Report + ProPublica",
    "source_detail": "Regenstrief 2023: $27.9M expenses. Manages Indiana Health Information Exchange (IHIE) covering ~6M patient records statewide.",
    "extraction_note": "$27,941,801 / 6,000,000 = $4.65/patient. IHIE is one of the largest health information exchanges in the US.",
    "impact_description": "one Indiana patient with health records coordinated through the Regenstrief-powered Indiana Health Information Exchange, enabling better-coordinated care across providers",
    "annual_expenses_usd": 27941801,
    "revenue_year": 2023,
  },

  # University of Nebraska Foundation
  {
    "name": "University of Nebraska",
    "ein": "470379839",
    "pp_name": [
      "University Of Nebraska Foundation",
      "University Of Nebraska",
      "University Of Nebraska Omaha",
      "University Of Nebraska At Omaha",
      "University Of Nebraska Lincoln",
      "University Of Nebraska Medical Center",
      "Univ Of Nebraska",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one NU student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 7000,
    "impact_per_100_usd": 0.01429,
    "confidence": "medium",
    "source": "University of Nebraska Lincoln CDS 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24 UNL: avg institutional grant ~$7K. UNF covers all NU campuses (Lincoln, Omaha, Kearney, Medical Center). Foundation expenses $338.5M.",
    "extraction_note": "UNF is the 990-filing entity for all NU campuses' fundraising. CDS avg grant from UNL used as proxy.",
    "impact_description": "one year of need-based financial aid for one University of Nebraska student across any NU campus (avg ~$7,000 institutional grant at UNL)",
    "annual_expenses_usd": 338546603,
    "revenue_year": 2023,
  },

  # Community Catalyst
  {
    "name": "Community Catalyst",
    "ein": "43355127",
    "pp_name": [
      "Community Catalyst Inc",
      "Community Catalyst",
    ],
    "cause": "health",
    "primary_metric_label": "one person with improved healthcare access through advocacy",
    "primary_metric_value": 5000000,
    "primary_metric_unit": "people with improved healthcare access through Community Catalyst policy advocacy",
    "cost_per_outcome_usd": 8,
    "impact_per_100_usd": 11.9,
    "confidence": "low",
    "source": "Community Catalyst Annual Report + ProPublica",
    "source_detail": "Community Catalyst 2023: $42.1M expenses. Advocacy on ACA enrollment, Medicaid expansion, and health equity reaching ~5M people.",
    "extraction_note": "Policy advocacy org. Estimated reach of healthcare access improvements through legislative wins. $42.1M / 5M = $8.42/person.",
    "impact_description": "one person gaining improved healthcare access through Community Catalyst's advocacy on ACA enrollment, Medicaid policy, and health system equity",
    "annual_expenses_usd": 42128281,
    "revenue_year": 2023,
  },

  # Discovery Park of America
  {
    "name": "Discovery Park of America",
    "ein": "262726861",
    "pp_name": [
      "Discovery Park Of America Inc",
      "Discovery Park Of America",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one museum visitor",
    "primary_metric_value": 200000,
    "primary_metric_unit": "visitors to Discovery Park of America museum and educational exhibits",
    "cost_per_outcome_usd": 40,
    "impact_per_100_usd": 2.48,
    "confidence": "low",
    "source": "Discovery Park of America Annual Report + ProPublica",
    "source_detail": "Discovery Park 2023: $8.1M expenses. World-class museum in Union City, TN. ~200K annual visitors from across the region.",
    "extraction_note": "$8,069,838 / 200,000 = $40.3/visitor. 100,000+ artifact museum with nature park.",
    "impact_description": "one visitor experiencing Discovery Park of America's exhibits spanning science, history, technology, and nature in Union City, Tennessee",
    "annual_expenses_usd": 8069838,
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
