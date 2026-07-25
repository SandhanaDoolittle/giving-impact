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

# ── ALIAS FIXES ────────────────────────────────────────────────────────────────

# Mayo Clinic: grant text "MAYO FOUNDATION"
add_aliases(data, "Mayo Clinic", [
    "Mayo Foundation",
    "Mayo Foundation For Medical Education And Research",
    "Mayo Clinic Rochester",
])

# National Academy of Sciences: grant text "NATIONAL ACAD OF SCIS"
add_aliases(data, "National Academy of Sciences", [
    "National Acad Of Scis",
    "National Academies Of Sciences Engineering And Medicine",
    "National Academy Of Sciences Engineering And Medicine",
])

# University of Maryland: grant text "UNIVERSITY OF MARYLAND COLLEGE PARK"
add_aliases(data, "University of Maryland", [
    "University Of Maryland College Park",
    "University Of Maryland College Park Inc",
])

# Rensselaer: grant text "RENSSELAER POLYTECHNIC INSTITUTE FROM DOCTRINA"
add_aliases(data, "Rensselaer Polytechnic Institute", [
    "Rensselaer Polytechnic Institute From Doctrina",
])

# Conservation International: typo "CONSERVATION INTERATIONAL FOUNDATION"
add_aliases(data, "Conservation International", [
    "Conservation Interational Foundation",  # typo as appears in grant data
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────

new_entries = [

  # Michelson Found Animals Foundation
  {
    "name": "Found Animals Foundation",
    "ein": "203944602",
    "pp_name": [
      "The Michelson Found Animals Foundation Inc",
      "Michelson Found Animals Foundation",
      "Found Animals Foundation",
    ],
    "cause": "animal_welfare",
    "primary_metric_label": "one shelter animal spayed or neutered",
    "primary_metric_value": 200000,
    "primary_metric_unit": "pets spayed/neutered or shelter animals supported through Found Animals programs",
    "cost_per_outcome_usd": 39,
    "impact_per_100_usd": 2.58,
    "confidence": "medium",
    "source": "Found Animals Annual Report + ProPublica",
    "source_detail": "Found Animals Foundation 2023: $7.7M expenses; funds spay/neuter and pet homelessness elimination programs reaching ~200K animals",
    "extraction_note": "$7.7M / 200K animals = $38.7/animal. Michelson Found Animals works to end pet homelessness.",
    "impact_description": "one shelter animal spayed or neutered, or one pet owner receiving affordable veterinary care through Found Animals programs",
    "annual_expenses_usd": 7740700,
    "revenue_year": 2023,
  },

  # PolicyLink
  {
    "name": "PolicyLink",
    "ein": "943297479",
    "pp_name": "Policylink",
    "cause": "community",
    "primary_metric_label": "one person impacted through equity policy work",
    "primary_metric_value": 750000,
    "primary_metric_unit": "people impacted through health equity, economic inclusion, and housing policy advocacy",
    "cost_per_outcome_usd": 59,
    "impact_per_100_usd": 1.69,
    "confidence": "low",
    "source": "PolicyLink Annual Report + ProPublica",
    "source_detail": "PolicyLink 2023: $44.4M expenses. Research and advocacy on equity in health, economy, housing reaching ~750K people through policy wins.",
    "extraction_note": "Policy impact diffuse. Estimated reach of advocacy campaigns. $44.4M / 750K = $59/person.",
    "impact_description": "one person benefiting from PolicyLink's research and advocacy work on racial and economic equity in health systems, housing, and economic opportunity",
    "annual_expenses_usd": 44354056,
    "revenue_year": 2023,
  },

  # Tippet Rise Art Center / Foundation
  {
    "name": "Tippet Rise Art Center",
    "ein": "356933159",
    "pp_name": [
      "Tippet Rise Foundation",
      "Tippet Rise Art Center",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one visitor to Tippet Rise",
    "primary_metric_value": 15000,
    "primary_metric_unit": "visitors experiencing art and music at Tippet Rise Art Center",
    "cost_per_outcome_usd": 674,
    "impact_per_100_usd": 0.148,
    "confidence": "low",
    "source": "Tippet Rise Annual Report + ProPublica",
    "source_detail": "Tippet Rise Foundation 2023: $10.1M expenses. Montana art and music ranch serving ~15K visitors per season.",
    "extraction_note": "$10.1M / 15K visitors = $673/visitor. Remote Montana ranch presenting chamber music and large-scale sculpture.",
    "impact_description": "one visitor experiencing chamber music performances and monumental sculpture installations at Tippet Rise Art Center in Fishtail, Montana",
    "annual_expenses_usd": 10107344,
    "revenue_year": 2023,
  },

  # Research Foundation of CUNY
  {
    "name": "City University of New York",
    "ein": "131988190",
    "pp_name": [
      "Research Foundation Of The City University Of New York",
      "Research Foundation Of City University Of New York",
      "Research Foundation Of Cuny",
      "City University Of New York",
      "Cuny",
    ],
    "cause": "education",
    "primary_metric_label": "one CUNY student benefiting from research programs",
    "primary_metric_value": 275000,
    "primary_metric_unit": "CUNY students in research-enhanced academic programs",
    "cost_per_outcome_usd": 2156,
    "impact_per_100_usd": 0.0464,
    "confidence": "medium",
    "source": "CUNY Research Foundation + ProPublica",
    "source_detail": "Research Foundation CUNY 2023: $592.8M expenses managing sponsored research. CUNY serves ~275K students across 25 campuses.",
    "extraction_note": "Research Foundation manages $600M+ in grants enhancing education for 275K CUNY students. $593M / 275K = $2,156/student.",
    "impact_description": "one City University of New York student benefiting from research grants, fellowships, and sponsored programs through the CUNY Research Foundation",
    "annual_expenses_usd": 592838098,
    "revenue_year": 2023,
  },

  # University of Utah (Research Foundation as proxy)
  {
    "name": "University of Utah",
    "ein": "237112869",
    "pp_name": [
      "University Of Utah Research Foundation",
      "University Of Utah",
      "Univ Of Utah",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 8000,
    "impact_per_100_usd": 0.0125,
    "confidence": "medium",
    "source": "University of Utah Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$8K. Public flagship in Salt Lake City with ~34K students.",
    "extraction_note": "Research Foundation is the 990-filing entity. State university does not file 990. CDS grant used for impact.",
    "impact_description": "one year of need-based financial aid for one University of Utah student (avg ~$8,000 institutional grant)",
    "annual_expenses_usd": 16675326,
    "revenue_year": 2023,
  },

  # Kansas City Zoo
  {
    "name": "Kansas City Zoo",
    "ein": "811483719",
    "pp_name": [
      "Friends Of The Zoo Of Kansas City Foundation",
      "Kansas City Zoo",
      "Kansas City Zoological Park",
      "Kansas City Zoo And Aquarium",
    ],
    "cause": "animal_welfare",
    "primary_metric_label": "one zoo visitor",
    "primary_metric_value": 800000,
    "primary_metric_unit": "visitors to Kansas City Zoo",
    "cost_per_outcome_usd": 12,
    "impact_per_100_usd": 8.22,
    "confidence": "low",
    "source": "Friends of the Zoo + ProPublica",
    "source_detail": "Friends of Zoo 2023: $9.7M expenses (fundraising arm). KC Zoo serves ~800K visitors/year. Foundation funds conservation and education programs.",
    "extraction_note": "Friends Foundation ($9.7M) is the 990 entity; main zoo ops funded separately. Cost per visitor based on foundation budget vs. total visitation.",
    "impact_description": "one visitor experiencing the Kansas City Zoo's conservation programs, animal exhibits, and wildlife education",
    "annual_expenses_usd": 9718542,
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
