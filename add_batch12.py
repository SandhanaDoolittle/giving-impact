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

# ── ALIAS FIXES ────────────────────────────────────────────────────────────────

# Tides Center: "TIDES FOUNDATION" is related but separate. Check grants for "TIDES FOUNDATION"
add_aliases(data, "Tides Center", [
    "Tides Foundation",  # separate org often confused with Tides Center in grant lists
])

# NEO Philanthropy — fiscal sponsor appearing in many grants. Not in metrics yet (new entry below)
# but checking if already there
# (Adding as new entry)

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Vanderbilt University
  {
    "name": "Vanderbilt University",
    "ein": "620476822",
    "pp_name": [
      "Vanderbilt University",
      "Vanderbilt University Medical Center",
      "Vanderbilt Univ",
      "Vanderbilt University Nashville",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Vanderbilt student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Vanderbilt University",
    "cost_per_outcome_usd": 68000,
    "impact_per_100_usd": 0.00147,
    "confidence": "medium",
    "source": "Vanderbilt University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Vanderbilt University 2023: $2.03B expenses. Private research university in Nashville, TN with ~14K students. CDS 2023-24 avg institutional need-based grant ~$68,000. Vanderbilt meets 100% of demonstrated need.",
    "extraction_note": "CDS 2023-24 avg institutional need-based grant = ~$68K. Vanderbilt is one of the most generous need-blind private universities in the US.",
    "impact_description": "one year of need-based financial aid for one Vanderbilt University student (avg ~$68,000 institutional grant) — a top-15 research university in Nashville with need-blind admissions and full demonstrated need coverage",
    "annual_expenses_usd": 2025948154,
    "revenue_year": 2023,
  },

  # Boston Medical Center — Boston's largest safety-net hospital
  {
    "name": "Boston Medical Center",
    "ein": "43314093",
    "pp_name": [
      "Boston Medical Center",
      "Boston Medical Center Corporation",
      "BMC",
      "Bmc Health System",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Boston Medical Center",
    "primary_metric_value": 600000,
    "primary_metric_unit": "patient encounters at Boston Medical Center, Boston's largest safety-net hospital serving predominantly low-income and uninsured patients",
    "cost_per_outcome_usd": 4032,
    "impact_per_100_usd": 0.0248,
    "confidence": "medium",
    "source": "Boston Medical Center Annual Report + ProPublica",
    "source_detail": "Boston Medical Center 2023: $2.4B expenses. Boston's largest safety-net hospital with ~550K outpatient visits + 46K inpatient discharges. 70%+ of patients covered by Medicaid or uninsured.",
    "extraction_note": "$2,418,812,155 / 600,000 patient encounters = $4,031.4/encounter. BMC provides a disproportionate share of charity care and serves Boston's most vulnerable populations.",
    "impact_description": "one patient encounter at Boston Medical Center — Boston's primary safety-net hospital where 70%+ of patients are on Medicaid or uninsured, offering cancer care, trauma center, and comprehensive services regardless of ability to pay",
    "annual_expenses_usd": 2418812155,
    "revenue_year": 2023,
  },

  # Boston Children's Hospital
  {
    "name": "Boston Children's Hospital",
    "ein": "42774441",
    "pp_name": [
      "Childrens Hospital Corporation",
      "Boston Children S Hospital",
      "Boston Childrens Hospital",
      "Boston Children's Hospital",
      "Children S Hospital Boston",
      "Childrens Hospital Boston",
    ],
    "cause": "health",
    "primary_metric_label": "one child receiving care at Boston Children's Hospital",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "child patient encounters at Boston Children's Hospital including inpatient, outpatient, and emergency visits",
    "cost_per_outcome_usd": 2875,
    "impact_per_100_usd": 0.0348,
    "confidence": "medium",
    "source": "Boston Children's Hospital Annual Report + ProPublica",
    "source_detail": "Children's Hospital Corporation (Boston Children's Hospital) 2023: $2.9B expenses. World's leading pediatric hospital: 28K inpatient discharges, 600K+ emergency/urgent care, 400K+ outpatient visits annually.",
    "extraction_note": "$2,874,957,146 / 1,000,000 encounters = $2,875/encounter. Boston Children's is consistently ranked #1 children's hospital in the US.",
    "impact_description": "one child patient encounter at Boston Children's Hospital — ranked #1 children's hospital in the US for 30+ years, offering specialized care for rare and complex pediatric conditions and advancing child health through research",
    "annual_expenses_usd": 2874957146,
    "revenue_year": 2023,
  },

  # Tufts University
  {
    "name": "Tufts University",
    "ein": "42103634",
    "pp_name": [
      "Trustees Of Tufts College",
      "Tufts University",
      "Tufts Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Tufts student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Tufts University",
    "cost_per_outcome_usd": 58000,
    "impact_per_100_usd": 0.001724,
    "confidence": "medium",
    "source": "Tufts University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Tufts University 2023: $1.32B expenses. Private research university in Medford, MA with ~12,000 students. CDS 2023-24 avg institutional need-based grant ~$58,000. Tufts meets 100% of demonstrated need.",
    "extraction_note": "CDS 2023-24 avg institutional need-based grant ~$58K. Tufts includes schools of Arts & Sciences, Fletcher School of Law & Diplomacy, Cummings School of Veterinary Medicine, and Medical School.",
    "impact_description": "one year of need-based financial aid for one Tufts University student (avg ~$58,000 institutional grant) — a top-30 private research university in Massachusetts with nationally ranked international affairs, veterinary, and engineering programs",
    "annual_expenses_usd": 1323001574,
    "revenue_year": 2023,
  },

  # Los Angeles Philharmonic Association
  {
    "name": "Los Angeles Philharmonic Association",
    "ein": "951696734",
    "pp_name": [
      "Los Angeles Philharmonic Association",
      "Los Angeles Philharmonic",
      "La Philharmonic",
      "La Phil",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one person engaged by the Los Angeles Philharmonic",
    "primary_metric_value": 800000,
    "primary_metric_unit": "people experiencing the LA Philharmonic through concerts, education programs, and media at Walt Disney Concert Hall",
    "cost_per_outcome_usd": 245,
    "impact_per_100_usd": 0.408,
    "confidence": "medium",
    "source": "LA Philharmonic Annual Report + ProPublica",
    "source_detail": "Los Angeles Philharmonic Association 2023: $196.2M expenses. World-class orchestra at Walt Disney Concert Hall serving ~600K concert attendees + 200K+ through education programs.",
    "extraction_note": "$196,153,186 / 800,000 engagements = $245.2/person. LA Phil hosts 200+ concerts/year under Gustavo Dudamel plus free education programs serving 200K+ children/year.",
    "impact_description": "one person experiencing the Los Angeles Philharmonic — one of the world's great orchestras, led by Gustavo Dudamel, performing 200+ concerts/year at Walt Disney Concert Hall and running LA's largest arts education program",
    "annual_expenses_usd": 196153186,
    "revenue_year": 2023,
  },

  # Children's Hospital Los Angeles
  {
    "name": "Children's Hospital Los Angeles",
    "ein": "951690977",
    "pp_name": [
      "Childrens Hospital Los Angeles",
      "Children S Hospital Los Angeles",
      "Children's Hospital Los Angeles",
      "CHLA",
    ],
    "cause": "health",
    "primary_metric_label": "one child patient encounter at Children's Hospital Los Angeles",
    "primary_metric_value": 500000,
    "primary_metric_unit": "child patient encounters at Children's Hospital Los Angeles serving complex pediatric cases in Southern California",
    "cost_per_outcome_usd": 3306,
    "impact_per_100_usd": 0.0302,
    "confidence": "medium",
    "source": "CHLA Annual Report + ProPublica",
    "source_detail": "Children's Hospital Los Angeles 2023: $1.65B expenses. One of the nation's top pediatric hospitals, serving 500K+ child patients/year with highly specialized care.",
    "extraction_note": "$1,652,929,444 / 500,000 encounters = $3,305.9/encounter. CHLA is consistently ranked among the top 10 children's hospitals and is a leading pediatric research center affiliated with USC Keck School of Medicine.",
    "impact_description": "one child patient encounter at Children's Hospital Los Angeles — a top-10 pediatric hospital affiliated with USC Keck School of Medicine, serving 500K+ children/year with care for cancer, heart disease, neurological disorders, and rare diseases",
    "annual_expenses_usd": 1652929444,
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
