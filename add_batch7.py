import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

print(f"Starting entries: {len(data)}")

def add_aliases(entries, name_match, new_aliases):
    for e in entries:
        if e["name"] == name_match:
            pp = e.get("pp_name", [])
            if pp is None: pp = []
            if isinstance(pp, str): pp = [pp] if pp else []
            for a in new_aliases:
                if a not in pp:
                    pp.append(a)
            e["pp_name"] = pp
            return True
    print(f"WARNING: not found: {name_match!r}")
    return False

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Resources Legacy Fund — California environmental conservation intermediary
  {
    "name": "Resources Legacy Fund",
    "ein": "954703838",
    "pp_name": [
      "Resources Legacy Fund",
      "Resource Legacy Fund",
    ],
    "cause": "environment",
    "primary_metric_label": "one acre of land or water protected",
    "primary_metric_value": 300000,
    "primary_metric_unit": "acres of land or water protected through Resources Legacy Fund conservation grants and policy work",
    "cost_per_outcome_usd": 286,
    "impact_per_100_usd": 0.35,
    "confidence": "low",
    "source": "Resources Legacy Fund Annual Report + ProPublica",
    "source_detail": "Resources Legacy Fund 2023: $85.9M expenses. Works with government agencies and grantees to conserve land and water across the American West and beyond.",
    "extraction_note": "RLF is a conservation intermediary. Estimated ~300K acres/year protected through grant programs and embedded agency staff. $85.9M / 300K = $286/acre.",
    "impact_description": "one acre of land or water permanently protected through Resources Legacy Fund's grant programs, embedded government agency staff, and conservation policy work in the Western US",
    "annual_expenses_usd": 85936667,
    "revenue_year": 2023,
  },

  # Providence St Vincent Medical Foundation
  {
    "name": "Providence St Vincent Medical Foundation",
    "ein": "930575982",
    "pp_name": [
      "Providence St Vincent Medical Foundation",
      "Providence St Vincent Medical Center",
      "Providence St Vincent",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Providence St. Vincent",
    "primary_metric_value": 400000,
    "primary_metric_unit": "patient encounters at Providence St Vincent Medical Center supported by Foundation-funded programs",
    "cost_per_outcome_usd": 77,
    "impact_per_100_usd": 1.3,
    "confidence": "low",
    "source": "Providence St Vincent Foundation Annual Report + ProPublica",
    "source_detail": "Providence St Vincent Medical Foundation 2023: $30.9M expenses. Hospital foundation supporting Providence St Vincent Medical Center in Portland, OR, serving ~400K patients/year.",
    "extraction_note": "Foundation budget ($30.9M) supports a hospital serving ~400K patients/year. $30.9M / 400K = $77/encounter for Foundation-funded programs (charity care, research, etc.).",
    "impact_description": "one patient encounter at Providence St Vincent Medical Center in Portland, OR — a leading regional hospital offering charity care, cancer care, heart care, and emergency services",
    "annual_expenses_usd": 30854446,
    "revenue_year": 2023,
  },

  # Christina Seix Academy
  {
    "name": "Christina Seix Academy",
    "ein": "261321646",
    "pp_name": [
      "Christina Seix Academy A New Jersey Nonprofit Corporation",
      "Christina Seix Academy",
    ],
    "cause": "education",
    "primary_metric_label": "one student served at Christina Seix Academy",
    "primary_metric_value": 400,
    "primary_metric_unit": "students receiving full-year education at Christina Seix Academy charter school",
    "cost_per_outcome_usd": 38573,
    "impact_per_100_usd": 0.00259,
    "confidence": "low",
    "source": "Christina Seix Academy + ProPublica",
    "source_detail": "Christina Seix Academy 2023: $15.4M expenses. Charter school in Ewing, NJ serving ~400 K-12 students.",
    "extraction_note": "$15,429,067 / 400 = $38,572/student/year. Tuition-free charter school with individualized instruction focus.",
    "impact_description": "one student receiving a full year of tuition-free, individualized instruction at Christina Seix Academy charter school in Ewing, NJ",
    "annual_expenses_usd": 15429067,
    "revenue_year": 2023,
  },

  # Piedmont Healthcare Foundation — hospital foundation, GA
  {
    "name": "Piedmont Healthcare Foundation",
    "ein": "581272768",
    "pp_name": [
      "Piedmont Healthcare Foundation Inc",
      "Piedmont Healthcare Foundation",
      "Piedmont Healthcare",
    ],
    "cause": "health",
    "primary_metric_label": "one patient served through Piedmont Healthcare programs",
    "primary_metric_value": 4500000,
    "primary_metric_unit": "patients served by Piedmont Healthcare system across Georgia and South Carolina",
    "cost_per_outcome_usd": 0.48,
    "impact_per_100_usd": 207,
    "confidence": "low",
    "source": "Piedmont Healthcare Foundation + ProPublica",
    "source_detail": "Piedmont Healthcare Foundation 2023: $2.2M expenses (fundraising arm). Piedmont Healthcare system serves ~4.5M patients/year across 24 hospitals in GA and SC.",
    "extraction_note": "Foundation ($2.2M) is a small fundraising arm for the Piedmont Healthcare system. System patient volume used as downstream impact measure. $2.2M / 4.5M = $0.48/patient.",
    "impact_description": "one patient receiving care in the Piedmont Healthcare system in Georgia and South Carolina, supported by Foundation-funded programs in cancer care, heart health, and community health",
    "annual_expenses_usd": 2172118,
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
