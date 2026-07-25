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

# MD Anderson Cancer Center — UT System state entity, no independent 990.
# Match grant "MD ANDERSON CANCER CENTER" → add as alias to a new entry below.

# Smithsonian — federal agency, private giving goes to Smithsonian Institution Foundation.
# "SMITHSONIAN INSTITUTION" in grants → add alias to Smithsonian entry below.

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Institute for Justice — libertarian civil liberties law firm
  {
    "name": "Institute for Justice",
    "ein": "521744337",
    "pp_name": [
      "Institute For Justice",
      "IJ",
    ],
    "cause": "community",
    "primary_metric_label": "one person benefiting from Institute for Justice legal advocacy",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "people benefiting from Institute for Justice litigation wins protecting economic liberty, property rights, free speech, and school choice",
    "cost_per_outcome_usd": 22,
    "impact_per_100_usd": 4.51,
    "confidence": "low",
    "source": "Institute for Justice Annual Report + ProPublica",
    "source_detail": "Institute for Justice 2024: $44.3M expenses. Public interest law firm fighting government overreach through strategic litigation. Wins create systemic policy change benefiting millions.",
    "extraction_note": "$44,264,308 / 2,000,000 people = $22.1/person. IJ's wins in cases like Kelo (eminent domain), occupational licensing, and civil forfeiture create lasting policy change for millions of Americans.",
    "impact_description": "one person benefiting from Institute for Justice's strategic litigation protecting economic liberty, private property rights, free speech, and school choice — a public interest law firm that has won landmark US Supreme Court cases",
    "annual_expenses_usd": 44264308,
    "revenue_year": 2024,
  },

  # Planned Parenthood Federation of America
  {
    "name": "Planned Parenthood Federation of America",
    "ein": "131644147",
    "pp_name": [
      "Planned Parenthood Federation Of America",
      "Planned Parenthood",
      "Planned Parenthood Federation",
      "Ppfa",
    ],
    "cause": "health",
    "primary_metric_label": "one patient receiving reproductive healthcare at Planned Parenthood",
    "primary_metric_value": 2400000,
    "primary_metric_unit": "patients receiving reproductive and preventive healthcare through Planned Parenthood health centers nationwide",
    "cost_per_outcome_usd": 186,
    "impact_per_100_usd": 0.538,
    "confidence": "medium",
    "source": "Planned Parenthood Annual Report + ProPublica",
    "source_detail": "Planned Parenthood Federation of America 2023: $446M expenses. National organization for 600+ health centers providing contraception, STI testing, cancer screening, and abortion to 2.4M patients/year.",
    "extraction_note": "$445,964,327 / 2,400,000 patients = $185.8/patient. PPFA provides organizational support, public affairs, training, and grants to affiliate health centers across all 50 states.",
    "impact_description": "one patient receiving reproductive healthcare (contraception, STI testing, cancer screening, or abortion) at one of Planned Parenthood's 600+ health centers — serving 2.4M patients/year, 75% of whom have incomes below 150% of the federal poverty level",
    "annual_expenses_usd": 445964327,
    "revenue_year": 2023,
  },

  # Oregon State University Foundation
  {
    "name": "Oregon State University",
    "ein": "936022772",
    "pp_name": [
      "Oregon State University Foundation",
      "Oregon State University",
      "Osu Foundation",
      "Oregon State Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Oregon State student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Oregon State University",
    "cost_per_outcome_usd": 11000,
    "impact_per_100_usd": 0.00909,
    "confidence": "medium",
    "source": "OSU Common Data Set 2023-24 + ProPublica",
    "source_detail": "Oregon State University Foundation 2023: $139.6M expenses. Fundraising arm for Oregon State University (Corvallis, OR), a land-grant research university with ~33,000 students. CDS avg institutional need-based grant ~$11,000.",
    "extraction_note": "CDS 2023-24 OSU avg institutional need-based grant used. OSU Foundation manages $1B+ endowment supporting scholarships, research, and faculty positions.",
    "impact_description": "one year of need-based financial aid for one Oregon State University student (avg ~$11,000 institutional grant) — Oregon's flagship land-grant research university with nationally ranked programs in engineering, forestry, and marine science",
    "annual_expenses_usd": 139562869,
    "revenue_year": 2023,
  },

  # Beth Israel Deaconess Medical Center
  {
    "name": "Beth Israel Deaconess Medical Center",
    "ein": "42103881",
    "pp_name": [
      "Beth Israel Deaconess Medical Center",
      "Beth Israel Deaconess Medical Center Inc",
      "BIDMC",
      "Beth Israel Deaconess",
      "Beth Israel Hospital",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Beth Israel Deaconess Medical Center",
    "primary_metric_value": 1180000,
    "primary_metric_unit": "patient encounters at Beth Israel Deaconess Medical Center (Harvard teaching hospital, Boston)",
    "cost_per_outcome_usd": 2181,
    "impact_per_100_usd": 0.0459,
    "confidence": "medium",
    "source": "BIDMC Annual Report + ProPublica",
    "source_detail": "Beth Israel Deaconess Medical Center 2023: $2.57B expenses. Harvard Medical School teaching hospital with ~80K inpatient admissions + 1.1M outpatient encounters/year. Part of Beth Israel Lahey Health.",
    "extraction_note": "$2,574,202,267 / 1,180,000 encounters = $2,181/encounter. BIDMC is known for cardiac, cancer, orthopedic, and transplant care.",
    "impact_description": "one patient encounter at Beth Israel Deaconess Medical Center — a leading Harvard Medical School teaching hospital in Boston offering cardiac, cancer, and transplant care with world-class research programs",
    "annual_expenses_usd": 2574202267,
    "revenue_year": 2023,
  },

  # Brigham Young University
  {
    "name": "Brigham Young University",
    "ein": "870217280",
    "pp_name": [
      "Brigham Young University",
      "Byu",
      "Brigham Young Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one BYU student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Brigham Young University",
    "cost_per_outcome_usd": 5000,
    "impact_per_100_usd": 0.02,
    "confidence": "medium",
    "source": "BYU Common Data Set 2023-24",
    "source_detail": "Brigham Young University (Provo, UT): ~$800M expenses. Church of Jesus Christ of Latter-day Saints university with ~35,000 students. Very low tuition ($6,120/year for LDS members). CDS avg institutional need-based grant ~$5,000.",
    "extraction_note": "BYU's expenses are ~$800M (estimated 2023). LDS Church heavily subsidizes operations, keeping tuition at ~1/3 of comparable universities. CDS avg institutional grant reflects the already-reduced tuition.",
    "impact_description": "one year of need-based financial aid for one BYU student (avg ~$5,000 grant on top of already heavily LDS-subsidized tuition of $6,120/year) — a major private research university in Provo, UT serving 35,000 students",
    "annual_expenses_usd": 800000000,
    "revenue_year": 2023,
  },

  # Cleveland Clinic Foundation
  {
    "name": "Cleveland Clinic Foundation",
    "ein": "912153073",
    "pp_name": [
      "Cleveland Clinic Foundation",
      "Cleveland Clinic",
      "Cleveland Clinic Health System",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Cleveland Clinic",
    "primary_metric_value": 13000000,
    "primary_metric_unit": "patient interactions at Cleveland Clinic Foundation system across 17+ hospitals and 200+ outpatient facilities",
    "cost_per_outcome_usd": 1137,
    "impact_per_100_usd": 0.0879,
    "confidence": "medium",
    "source": "Cleveland Clinic Annual Report + ProPublica",
    "source_detail": "Cleveland Clinic Foundation 2023: $14.8B expenses. Major nonprofit health system with 17 hospitals, 200+ outpatient locations, 13M+ patient interactions/year. Consistently ranked #1 in cardiology.",
    "extraction_note": "$14,776,307,706 / 13,000,000 patient interactions = $1,136.6/interaction. Cleveland Clinic is internationally recognized for heart care, neurological, and urological care.",
    "impact_description": "one patient encounter at Cleveland Clinic — a world-renowned health system ranked #1 in cardiology for 30+ years, serving 13M patients/year across 17 hospitals with specialties in heart, brain, and orthopedic care",
    "annual_expenses_usd": 14776307706,
    "revenue_year": 2023,
  },

  # City of Hope National Medical Center — cancer research and treatment
  {
    "name": "City of Hope",
    "ein": "951683875",
    "pp_name": [
      "City Of Hope National Medical Center",
      "City Of Hope",
      "City Of Hope Cancer Center",
      "City Of Hope Inc",
    ],
    "cause": "health",
    "primary_metric_label": "one cancer patient encounter at City of Hope",
    "primary_metric_value": 630000,
    "primary_metric_unit": "cancer patient encounters at City of Hope — a leading NCI Comprehensive Cancer Center specializing in blood cancers, transplants, and diabetes",
    "cost_per_outcome_usd": 3797,
    "impact_per_100_usd": 0.0263,
    "confidence": "medium",
    "source": "City of Hope Annual Report + ProPublica",
    "source_detail": "City of Hope National Medical Center 2023: $2.4B expenses. One of America's leading NCI-designated cancer centers. ~600K outpatient + 30K inpatient encounters/year in cancer treatment and research.",
    "extraction_note": "$2,391,958,398 / 630,000 patient encounters = $3,797.6/encounter. City of Hope was among the first NCI Comprehensive Cancer Centers and specializes in hematologic cancers, bone marrow transplants, and diabetes.",
    "impact_description": "one cancer patient encounter at City of Hope — a founding NCI Comprehensive Cancer Center in Duarte, CA specializing in leukemia, lymphoma, bone marrow transplants, and innovative cancer research with 1M+ patients enrolled in clinical trials",
    "annual_expenses_usd": 2391958398,
    "revenue_year": 2023,
  },

  # Kauffman Center for the Performing Arts
  {
    "name": "Kauffman Center for the Performing Arts",
    "ein": "431866550",
    "pp_name": [
      "Kauffman Center For The Performing Arts",
      "Kauffman Center",
      "Muriel Kauffman Center",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one attendee at Kauffman Center for the Performing Arts",
    "primary_metric_value": 400000,
    "primary_metric_unit": "attendees at Kauffman Center for the Performing Arts (Kansas City Symphony, Lyric Opera, KC Ballet, and other performances)",
    "cost_per_outcome_usd": 63,
    "impact_per_100_usd": 1.6,
    "confidence": "medium",
    "source": "Kauffman Center Annual Report + ProPublica",
    "source_detail": "Kauffman Center for the Performing Arts 2023: $25M expenses. Premier performing arts venue in Kansas City, MO with two halls hosting the KC Symphony, Lyric Opera, and KC Ballet. ~400K attendees/year.",
    "extraction_note": "$25,038,603 / 400,000 attendees = $62.6/attendee. Kauffman Center was a major gift from Muriel McBrien Kauffman and the Kauffman Foundation. Houses three resident companies.",
    "impact_description": "one person attending a performance at Kauffman Center for the Performing Arts in Kansas City — the home of Kansas City Symphony, Lyric Opera of Kansas City, and Kansas City Ballet, hosting 250+ performances/year",
    "annual_expenses_usd": 25038603,
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
