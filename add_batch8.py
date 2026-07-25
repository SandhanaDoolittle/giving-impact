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

  # NAF Hotline Fund — financial assistance for abortion access
  {
    "name": "NAF Hotline Fund",
    "ein": "264703759",
    "pp_name": [
      "Naf Hotline Fund",
      "NAF Hotline Fund",
      "National Abortion Federation Hotline Fund",
    ],
    "cause": "health",
    "primary_metric_label": "one patient receiving abortion financial assistance",
    "primary_metric_value": 167000,
    "primary_metric_unit": "patients receiving financial assistance through NAF Hotline Fund for reproductive healthcare",
    "cost_per_outcome_usd": 400,
    "impact_per_100_usd": 0.25,
    "confidence": "medium",
    "source": "NAF Hotline Fund Annual Report + ProPublica",
    "source_detail": "NAF Hotline Fund 2023: $66.8M expenses. Provides financial and logistical support to patients seeking abortion care, averaging ~$400 per patient served.",
    "extraction_note": "$66,775,813 / ~167,000 patients = ~$400/patient. NAF Hotline answers 1M+ calls/year; financial assistance provided to a subset.",
    "impact_description": "one patient receiving financial assistance and support through the NAF Hotline Fund to access reproductive healthcare services",
    "annual_expenses_usd": 66775813,
    "revenue_year": 2023,
  },

  # National Network of Abortion Funds
  {
    "name": "National Network of Abortion Funds",
    "ein": "43236982",
    "pp_name": [
      "National Network Of Abortion Funds",
      "National Network of Abortion Funds",
    ],
    "cause": "health",
    "primary_metric_label": "one person receiving abortion fund support",
    "primary_metric_value": 60000,
    "primary_metric_unit": "people receiving financial assistance through NNAF member abortion funds",
    "cost_per_outcome_usd": 548,
    "impact_per_100_usd": 0.182,
    "confidence": "low",
    "source": "NNAF Annual Report + ProPublica",
    "source_detail": "National Network of Abortion Funds 2023: $32.9M expenses. Umbrella network of 100+ local abortion funds that collectively helped ~60K people access abortion care.",
    "extraction_note": "$32,868,169 / 60,000 people = $547.8/person. NNAF provides grants to member funds and capacity building.",
    "impact_description": "one person receiving financial assistance from NNAF's member abortion funds network to access reproductive healthcare services",
    "annual_expenses_usd": 32868169,
    "revenue_year": 2023,
  },

  # Hillel International
  {
    "name": "Hillel International",
    "ein": "521844823",
    "pp_name": [
      "Hillel The Foundation For Jewish Campus Life",
      "Hillel International",
      "Hillel International Charles And Lynn Schusterman",
      "Hillel International Charles And Lynn Schusterman International Center",
    ],
    "cause": "education",
    "primary_metric_label": "one Jewish college student engaged in campus Jewish life",
    "primary_metric_value": 100000,
    "primary_metric_unit": "Jewish college students meaningfully engaged through Hillel chapters at 550+ campus communities",
    "cost_per_outcome_usd": 614,
    "impact_per_100_usd": 0.163,
    "confidence": "low",
    "source": "Hillel International Annual Report + ProPublica",
    "source_detail": "Hillel International HQ 2023: $61.4M expenses. Supports 550+ Hillel chapters serving 500K+ Jewish students. HQ provides grants, training, and resources.",
    "extraction_note": "$61.4M / ~100K deeply engaged students = $614/student. Full network serves 500K but HQ serves as capacity-builder.",
    "impact_description": "one Jewish college student meaningfully engaged in Jewish learning, community, and identity through Hillel's network of 550+ campus organizations",
    "annual_expenses_usd": 61438103,
    "revenue_year": 2023,
  },

  # Purpose Built Communities
  {
    "name": "Purpose Built Communities",
    "ein": "454056587",
    "pp_name": [
      "Purpose Built Communities Foundation Inc",
      "Purpose Built Communities",
    ],
    "cause": "community",
    "primary_metric_label": "one resident in a Purpose Built Communities partner neighborhood",
    "primary_metric_value": 200000,
    "primary_metric_unit": "residents in neighborhoods being transformed through Purpose Built Communities holistic revitalization model",
    "cost_per_outcome_usd": 53,
    "impact_per_100_usd": 1.87,
    "confidence": "low",
    "source": "Purpose Built Communities Annual Report + ProPublica",
    "source_detail": "Purpose Built Communities 2023: $10.7M expenses. Guides community partners in 12+ cities using integrated housing, education, and health approach serving ~200K residents.",
    "extraction_note": "$10,679,953 / 200,000 residents = $53.4/resident. PBC's model combines mixed-income housing, cradle-to-college education, and wellness in underserved neighborhoods.",
    "impact_description": "one resident in a community transformed by Purpose Built Communities' integrated model combining affordable housing, cradle-to-college education, and community health",
    "annual_expenses_usd": 10679953,
    "revenue_year": 2023,
  },

  # University of Georgia Foundation
  {
    "name": "University of Georgia",
    "ein": "586033837",
    "pp_name": [
      "University Of Georgia Foundation",
      "University Of Georgia",
      "Univ Of Georgia",
      "Uga Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one UGA student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 8000,
    "impact_per_100_usd": 0.0125,
    "confidence": "medium",
    "source": "UGA Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24 UGA: avg institutional grant ~$8K. Foundation expenses $160.6M. ~38K students.",
    "extraction_note": "UGA Foundation manages fundraising for the flagship Georgia public university. CDS grant data used for impact metric.",
    "impact_description": "one year of need-based financial aid for one University of Georgia student (avg ~$8,000 institutional grant)",
    "annual_expenses_usd": 160632346,
    "revenue_year": 2024,
  },

  # Facing History and Ourselves
  {
    "name": "Facing History and Ourselves",
    "ein": "42761636",
    "pp_name": [
      "Facing History And Ourselves Inc",
      "Facing History And Ourselves",
      "Facing History & Ourselves Inc",
    ],
    "cause": "education",
    "primary_metric_label": "one student impacted by Facing History curriculum",
    "primary_metric_value": 5000000,
    "primary_metric_unit": "students reached through Facing History and Ourselves teacher training and anti-bias curriculum",
    "cost_per_outcome_usd": 7,
    "impact_per_100_usd": 15.0,
    "confidence": "medium",
    "source": "Facing History Annual Report + ProPublica",
    "source_detail": "Facing History and Ourselves 2023: $33.3M expenses. Trains 50,000+ teachers annually who each reach 100+ students, totaling ~5M students reached/year.",
    "extraction_note": "$33,309,516 / 5,000,000 students = $6.66/student. Teacher-multiplier model: training one teacher impacts 100+ students over career.",
    "impact_description": "one student learning about historical prejudice, civic responsibility, and anti-bias through a Facing History trained teacher's classroom curriculum",
    "annual_expenses_usd": 33309516,
    "revenue_year": 2023,
  },

  # Massachusetts League of Community Health Centers
  {
    "name": "Massachusetts League of Community Health Centers",
    "ein": "42507409",
    "pp_name": [
      "Massachusetts League Of Community Health Centers Inc",
      "Massachusetts League Of Community Health Centers",
    ],
    "cause": "health",
    "primary_metric_label": "one patient served through MA community health centers",
    "primary_metric_value": 1500000,
    "primary_metric_unit": "patients served through Massachusetts community health centers supported by MLCHC advocacy and capacity-building",
    "cost_per_outcome_usd": 35,
    "impact_per_100_usd": 2.87,
    "confidence": "low",
    "source": "MLCHC Annual Report + ProPublica",
    "source_detail": "MLCHC 2023: $52.3M expenses. Advocacy and capacity-building for 51 MA community health centers collectively serving ~1.5M patients/year.",
    "extraction_note": "$52,333,127 / 1,500,000 patients = $34.9/patient. MLCHC provides training, advocacy, and shared services to member CHCs.",
    "impact_description": "one patient receiving primary care, dental, behavioral health, or other services at a Massachusetts community health center supported by MLCHC",
    "annual_expenses_usd": 52333127,
    "revenue_year": 2023,
  },

  # Thomas Jefferson University (+ Jefferson Hospital)
  {
    "name": "Thomas Jefferson University",
    "ein": "231352651",
    "pp_name": [
      "Thomas Jefferson University",
      "Thomas Jefferson University Hospital",
      "Jefferson Health",
      "Jefferson University Physicians",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Jefferson Health",
    "primary_metric_value": 250000,
    "primary_metric_unit": "patient encounters at Thomas Jefferson University Hospital and Jefferson Health system",
    "cost_per_outcome_usd": 6598,
    "impact_per_100_usd": 0.01516,
    "confidence": "medium",
    "source": "Jefferson Health Annual Report + ProPublica",
    "source_detail": "Thomas Jefferson University 2023: $1.65B expenses (university + Jefferson hospital). ~250K inpatient and major outpatient encounters/year at flagship Philadelphia hospital.",
    "extraction_note": "$1,649,493,276 / 250,000 = $6,597.97/encounter. TJU includes Sidney Kimmel Medical College and Jefferson Health system.",
    "impact_description": "one patient encounter at Thomas Jefferson University Hospital or Jefferson Health system in Philadelphia — a leading academic medical center with nationally ranked cancer and neurology programs",
    "annual_expenses_usd": 1649493276,
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
