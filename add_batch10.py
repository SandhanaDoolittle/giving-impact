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

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Massachusetts General Hospital (The General Hospital Corporation)
  {
    "name": "Massachusetts General Hospital",
    "ein": "42767019",
    "pp_name": [
      "Massachusetts General Hospital",
      "The General Hospital Corporation",
      "Mgh",
      "Mass General Hospital",
      "Massachusetts General Hospital Fund",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Massachusetts General Hospital",
    "primary_metric_value": 1550000,
    "primary_metric_unit": "patient encounters at Massachusetts General Hospital (inpatient + outpatient visits)",
    "cost_per_outcome_usd": 2065,
    "impact_per_100_usd": 0.0484,
    "confidence": "medium",
    "source": "Mass General Brigham Annual Report + IRS 990 (2022 filing)",
    "source_detail": "Massachusetts General Hospital 2022: ~$3.2B expenses. Flagship hospital of Mass General Brigham system. ~50K inpatient admissions + 1.5M outpatient visits/year.",
    "extraction_note": "$3,200,000,000 / 1,550,000 encounters = $2,064.5/encounter. MGH is a Harvard Medical School teaching hospital and top-ranked research institution. Expenses estimated from 2022 990 data.",
    "impact_description": "one patient encounter at Massachusetts General Hospital — the #1 ranked hospital in the US, a Harvard Medical School teaching hospital with 1.5M outpatient visits and 50K inpatient admissions per year",
    "annual_expenses_usd": 3200000000,
    "revenue_year": 2022,
  },

  # Tides Center — fiscal sponsor for progressive social change projects
  {
    "name": "Tides Center",
    "ein": "943213100",
    "pp_name": [
      "Tides Center",
      "TIDES CENTER",
    ],
    "cause": "community",
    "primary_metric_label": "one person reached through Tides Center-housed social change projects",
    "primary_metric_value": 10000000,
    "primary_metric_unit": "people reached through Tides Center's 2,000+ fiscally-sponsored social change projects in environment, social justice, and health equity",
    "cost_per_outcome_usd": 31,
    "impact_per_100_usd": 3.25,
    "confidence": "low",
    "source": "Tides Center Annual Report + ProPublica",
    "source_detail": "Tides Center 2023: $307.3M expenses. Fiscal sponsor for 2,000+ projects in environmental justice, social justice, health equity, human rights, and civic engagement.",
    "extraction_note": "$307,289,944 / 10,000,000 people estimated reached = $30.7/person. Tides Center operates as a legal and administrative home for progressive nonprofit projects.",
    "impact_description": "one person reached through Tides Center's 2,000+ fiscally-sponsored social change projects, spanning environmental justice, civil rights, health equity, and civic engagement across the US",
    "annual_expenses_usd": 307289944,
    "revenue_year": 2023,
  },

  # Windward Fund — environmental and climate fiscal sponsor
  {
    "name": "Windward Fund",
    "ein": "473522162",
    "pp_name": [
      "Windward Fund",
      "WINDWARD FUND",
    ],
    "cause": "environment",
    "primary_metric_label": "one person engaged in climate and environmental advocacy through Windward Fund projects",
    "primary_metric_value": 5000000,
    "primary_metric_unit": "people engaged in climate, clean energy, and environmental advocacy through Windward Fund's fiscally-sponsored campaigns",
    "cost_per_outcome_usd": 42,
    "impact_per_100_usd": 2.36,
    "confidence": "low",
    "source": "Windward Fund Annual Report + ProPublica",
    "source_detail": "Windward Fund 2023: $211.8M expenses. Environmental/climate fiscal sponsor (Arabella Advisors network) housing campaigns on clean energy policy, climate advocacy, conservation, and public health.",
    "extraction_note": "$211,847,409 / 5,000,000 people = $42.37/person. Windward Fund's housed projects include major climate policy campaigns reaching millions through media, legislation, and grassroots organizing.",
    "impact_description": "one person engaged in climate action or environmental advocacy through Windward Fund's housed campaigns on clean energy, conservation, and climate justice",
    "annual_expenses_usd": 211847409,
    "revenue_year": 2023,
  },

  # University of Kentucky (Research Foundation handles external grants)
  {
    "name": "University of Kentucky",
    "ein": "616033693",
    "pp_name": [
      "University Of Kentucky",
      "University Of Kentucky Research Foundation",
      "Univ Of Kentucky",
      "Uky",
      "University Of Kentucky Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one University of Kentucky student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Kentucky",
    "cost_per_outcome_usd": 9000,
    "impact_per_100_usd": 0.0111,
    "confidence": "medium",
    "source": "UKY Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Kentucky Research Foundation 2023: $447M expenses (research pass-throughs). Flagship state university in Lexington, KY with ~34K students. CDS 2023-24 avg institutional need-based grant ~$9,000.",
    "extraction_note": "CDS avg need-based institutional grant used as cost_per_outcome. UKY Research Foundation's expenses are mostly external research grants managed on behalf of the university.",
    "impact_description": "one year of need-based financial aid for one University of Kentucky student (avg ~$9,000 institutional grant) — Kentucky's flagship public research university",
    "annual_expenses_usd": 447136661,
    "revenue_year": 2023,
  },

  # University of Tulsa — private university in Tulsa, OK
  {
    "name": "University of Tulsa",
    "ein": "730579298",
    "pp_name": [
      "University Of Tulsa",
      "Univ Of Tulsa",
      "Tu Tulsa",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one University of Tulsa student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Tulsa",
    "cost_per_outcome_usd": 26000,
    "impact_per_100_usd": 0.00385,
    "confidence": "medium",
    "source": "University of Tulsa Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Tulsa 2023: $311.4M expenses. Private research university in Tulsa, OK with ~4,400 students. CDS 2023-24 avg institutional need-based grant ~$26,000.",
    "extraction_note": "CDS 2023-24 UTulsa: avg need-based institutional grant used. Private university with strong petroleum engineering, law, and cybersecurity programs.",
    "impact_description": "one year of need-based financial aid for one University of Tulsa student (avg ~$26,000 institutional grant) — a private research university with nationally ranked law and petroleum engineering programs",
    "annual_expenses_usd": 311397344,
    "revenue_year": 2023,
  },

  # University of Louisville Foundation — fundraising arm for UofL
  {
    "name": "University of Louisville Foundation",
    "ein": "237078461",
    "pp_name": [
      "University Of Louisville Foundation Inc",
      "University Of Louisville Foundation",
      "University Of Louisville",
      "Uofl Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one University of Louisville student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Louisville",
    "cost_per_outcome_usd": 8500,
    "impact_per_100_usd": 0.01176,
    "confidence": "medium",
    "source": "UofL Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Louisville Foundation 2023: $79.4M expenses. Manages private giving for University of Louisville (public research university, ~22K students). CDS avg institutional need-based grant ~$8,500.",
    "extraction_note": "CDS 2023-24 UofL avg need-based institutional grant used as cost_per_outcome. Foundation supports UofL's academic programs, scholarships, and research.",
    "impact_description": "one year of need-based financial aid for one University of Louisville student (avg ~$8,500 institutional grant) — Kentucky's leading metropolitan research university",
    "annual_expenses_usd": 79408065,
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
