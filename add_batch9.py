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

# Grant text "MEMORIAL SLOAN KETTERING CANCER" (without "Center") needs alias
add_aliases(data, "Memorial Sloan Kettering Cancer Center", [
    "Memorial Sloan Kettering Cancer",
    "Memorial Sloan-Kettering Cancer",
    "Msk Cancer Center",
    "Mskcc",
])

# "HARVARD GRADUATE SCHOOL OF EDUCATION" needs alias on existing Harvard entry
add_aliases(data, "Harvard University", [
    "Harvard Graduate School Of Education",
    "Harvard T H Chan School Of Public Health",
    "Harvard Business School",
    "Harvard Law School",
    "Harvard Kennedy School",
    "Harvard Medical School",
    "Harvard John A Paulson School Of Engineering And Applied Sciences",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Anti-Defamation League
  {
    "name": "Anti-Defamation League",
    "ein": "131818723",
    "pp_name": [
      "Anti Defamation League",
      "Anti-Defamation League",
      "ADL",
      "Anti Defamation League Adl",
    ],
    "cause": "community",
    "primary_metric_label": "one person reached through ADL anti-bias education or advocacy",
    "primary_metric_value": 3000000,
    "primary_metric_unit": "people reached through ADL anti-bias education, law enforcement training, and hate crime advocacy programs",
    "cost_per_outcome_usd": 19,
    "impact_per_100_usd": 5.18,
    "confidence": "low",
    "source": "ADL Annual Report + ProPublica",
    "source_detail": "Anti-Defamation League 2023: $57.9M expenses. Runs 'A World of Difference' anti-bias training, law enforcement programs reaching 80K+ officers/year, and civil rights advocacy reaching ~3M people total.",
    "extraction_note": "$57,939,187 / 3,000,000 people = $19.3/person. Estimates include A World of Difference trainings, law enforcement workshops, Never Is Now conference, and digital anti-hate resources.",
    "impact_description": "one person reached through ADL's anti-bias education programs, law enforcement training, or civil rights advocacy — including 'A World of Difference Institute' and hate crime reporting resources",
    "annual_expenses_usd": 57939187,
    "revenue_year": 2023,
  },

  # New York Public Library
  {
    "name": "New York Public Library",
    "ein": "131887440",
    "pp_name": [
      "The New York Public Library Astor Lenox And Tilden Foundations",
      "New York Public Library",
      "New York Public Library Astor Lenox And Tilden Foun",
      "New York Public Library Astor Lenox And Tilden Foundation",
      "Nypl",
    ],
    "cause": "education",
    "primary_metric_label": "one visit to the New York Public Library",
    "primary_metric_value": 7500000,
    "primary_metric_unit": "physical and digital visits to New York Public Library branches and research centers",
    "cost_per_outcome_usd": 52,
    "impact_per_100_usd": 1.9,
    "confidence": "medium",
    "source": "NYPL Annual Report + ProPublica",
    "source_detail": "New York Public Library 2023: $393.5M expenses. 4 research centers + 88 branch libraries. ~7.5M physical branch visits/year plus digital services reaching millions more.",
    "extraction_note": "$393,521,704 / 7,500,000 visits = $52.5/visit. NYPL 2023 annual report cites 7.6M in-person visits. Also 1.9M card holders and millions of digital interactions.",
    "impact_description": "one visit to the New York Public Library — one of the world's great free public institutions, with 88 branches, 4 research libraries, and free programs for all New Yorkers",
    "annual_expenses_usd": 393521704,
    "revenue_year": 2023,
  },

  # Whitney Museum of American Art
  {
    "name": "Whitney Museum of American Art",
    "ein": "131789318",
    "pp_name": [
      "Whitney Museum Of American Art",
      "Whitney Museum",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one visitor to the Whitney Museum of American Art",
    "primary_metric_value": 500000,
    "primary_metric_unit": "visitors to the Whitney Museum of American Art (paid + free community programs)",
    "cost_per_outcome_usd": 173,
    "impact_per_100_usd": 0.578,
    "confidence": "medium",
    "source": "Whitney Museum Annual Report + ProPublica",
    "source_detail": "Whitney Museum of American Art 2023: $86.7M expenses. Flagship NYC museum of American art in the Meatpacking District. ~400-500K visitors/year.",
    "extraction_note": "$86,708,000 / 500,000 visitors = $173.4/visitor. Whitney is a major cultural institution featuring 20th-21st century American art, including permanent collection and temporary exhibitions.",
    "impact_description": "one visitor experiencing American art at the Whitney Museum — featuring the most significant collection of 20th and 21st century American art including works by Edward Hopper, Georgia O'Keeffe, and contemporary artists",
    "annual_expenses_usd": 86708000,
    "revenue_year": 2023,
  },

  # Northwell Health Foundation
  {
    "name": "Northwell Health Foundation",
    "ein": "112965575",
    "pp_name": [
      "Northwell Health Foundation",
      "Northwell Health Foundation Ns Lij Health Systems Foundation",
      "Northwell Health Foundation Formerly North Shore Lij",
      "North Shore Lij Health System Foundation",
      "North Shore Lij",
      "North Shore University Hospital Foundation",
    ],
    "cause": "health",
    "primary_metric_label": "one patient interaction at Northwell Health",
    "primary_metric_value": 8000000,
    "primary_metric_unit": "patient interactions supported at Northwell Health across 21 hospitals and 900+ outpatient facilities in New York",
    "cost_per_outcome_usd": 14,
    "impact_per_100_usd": 7.2,
    "confidence": "low",
    "source": "Northwell Health Foundation Annual Report + ProPublica",
    "source_detail": "Northwell Health Foundation 2023: $111M expenses. Fundraising and grant arm for Northwell Health, New York's largest health system with 21 hospitals serving 8M+ patients/year.",
    "extraction_note": "$111,039,521 / 8,000,000 patient interactions = $13.88/interaction. Foundation funds cancer care, pediatric programs, research, and community health initiatives across the Northwell system.",
    "impact_description": "one patient interaction at Northwell Health — New York's largest health system with 21 hospitals, serving 8M+ patients/year in cancer care, heart care, pediatrics, behavioral health, and emergency medicine",
    "annual_expenses_usd": 111039521,
    "revenue_year": 2023,
  },

  # Dana-Farber Cancer Institute
  {
    "name": "Dana-Farber Cancer Institute",
    "ein": "42263040",
    "pp_name": [
      "Dana Farber Cancer Institute",
      "Dana-Farber Cancer Institute",
      "Dana Farber",
      "Dana-Farber",
      "Dana Farber Institute",
    ],
    "cause": "health",
    "primary_metric_label": "one cancer patient encounter at Dana-Farber",
    "primary_metric_value": 100000,
    "primary_metric_unit": "outpatient cancer patient encounters at Dana-Farber Cancer Institute, one of the world's top cancer centers",
    "cost_per_outcome_usd": 30028,
    "impact_per_100_usd": 0.00333,
    "confidence": "medium",
    "source": "Dana-Farber Cancer Institute Annual Report + ProPublica",
    "source_detail": "Dana-Farber Cancer Institute 2023: $3B expenses (includes extensive NIH research funding). ~100K cancer patients treated annually. One of 56 NCI-designated Comprehensive Cancer Centers.",
    "extraction_note": "$3,002,803,859 / 100,000 patient encounters = $30,028/encounter. Dana-Farber expenses include ~$600M+ in research grants. Specializes in adult and pediatric cancer treatment and research.",
    "impact_description": "one outpatient encounter for a cancer patient at Dana-Farber Cancer Institute in Boston — a world-leading NCI Comprehensive Cancer Center conducting 450+ active clinical trials and treating rare and complex cancers",
    "annual_expenses_usd": 3002803859,
    "revenue_year": 2023,
  },

  # California Institute of Technology (Caltech)
  {
    "name": "California Institute of Technology",
    "ein": "951643307",
    "pp_name": [
      "California Institute Of Technology",
      "Caltech",
      "Caltech Beckman Institute",
      "California Institute Of Technology Caltech",
      "Cal Tech",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Caltech student",
    "primary_metric_unit": "student-year of need-based financial aid funded at California Institute of Technology",
    "cost_per_outcome_usd": 61000,
    "impact_per_100_usd": 0.00164,
    "confidence": "medium",
    "source": "Caltech Common Data Set 2023-24 + ProPublica",
    "source_detail": "Caltech 2023: $3.7B total expenses (includes JPL managed for NASA, ~$2.9B). Avg institutional need-based grant ~$61K. ~2,300 students, 90%+ on some form of aid.",
    "extraction_note": "CDS 2023-24 Caltech: avg institutional need-based grant = $60,879. University expenses excluding JPL: ~$800M, but total 990 includes JPL. Using CDS grant figure as cost-per-outcome.",
    "impact_description": "one year of need-based financial aid for one Caltech student (avg ~$61,000) — a top-5 research university with 31 Nobel laureates among its faculty and alumni, known for physics, engineering, and planetary science",
    "annual_expenses_usd": 3704492000,
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
