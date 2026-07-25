import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

print(f"Starting entries: {len(data)}")

# ── ALIAS FIXES ON EXISTING ENTRIES ───────────────────────────────────────────

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
    return False

# Stanford: grant text "BOARD OF TRUSTEES OF LELAND STANFORD JUNIOR UNIVERSITY"
add_aliases(data, "Stanford University", [
    "Board of Trustees of Leland Stanford Junior University",
    "Board Of Trustees Leland Stanford Junior University",
])

# U of Minnesota: grant text "UNIVERSITY OF MINNESOTA FOUNDATION BELL MUSEUM AND PLANETARIUM"
add_aliases(data, "University of Minnesota", [
    "University Of Minnesota Foundation Bell Museum And Planetarium",
    "University Of Minnesota Bell Museum",
])

# Columbia University: grant text "TRUSTEES OF COLUMBIA UNIVERSITY IN CITY OF NEW YORK"
add_aliases(data, "Columbia University", [
    "Trustees Of Columbia University In City Of New York",
    "Trustees Of Columbia University In The City Of New York",
])

# Salvation Army: grant text just "SALVATION ARMY"
# The existing "Salvation Army National Corp" normalizes to "SALVATION ARMY NATIONAL"
# We need "Salvation Army" as standalone alias on one entry
add_aliases(data, "The Salvation Army USA", ["Salvation Army", "Salvation Army Usa"])

# Oprah Winfrey Leadership Academy Foundation: grant text "OPRAH WINFREY LEADERSHIP ACADEMY FDN"
# "FDN" is not in DROP_TOKENS, so it won't match "FOUNDATION"
add_aliases(data, "Oprah Winfrey Leadership Academy Foundation", [
    "Oprah Winfrey Leadership Academy Fdn",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────

new_entries = [

  # University of Pennsylvania ($9.26B — full university + Penn Medicine)
  {
    "name": "University of Pennsylvania",
    "ein": "231352685",
    "pp_name": [
      "Trustees Of The University Of Pennsylvania",
      "University Of Pennsylvania",
      "Upenn",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 57000,
    "impact_per_100_usd": 0.001754,
    "confidence": "medium",
    "source": "UPenn Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$57K. Combined university+Penn Medicine expenses $9.26B.",
    "extraction_note": "UPenn CDS average need-based grant from section G. Penn Medicine included in 990 expenses.",
    "impact_description": "one year of need-based financial aid for one University of Pennsylvania student (avg ~$57,000 institutional grant)",
    "annual_expenses_usd": 9264364000,
    "revenue_year": 2023,
  },

  # Northwestern Memorial Healthcare (Palos Hospital parent)
  {
    "name": "Northwestern Memorial Healthcare",
    "ein": "362169179",
    "pp_name": [
      "Northwestern Memorial Healthcare",
      "Northwestern Medicine Palos Hospital",
      "Northwestern Medicine",
      "Northwestern Memorial Hospital",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Northwestern Medicine",
    "primary_metric_value": 3000000,
    "primary_metric_unit": "patient encounters at Northwestern Medicine hospitals",
    "cost_per_outcome_usd": 155,
    "impact_per_100_usd": 0.645,
    "confidence": "low",
    "source": "Northwestern Medicine Annual Report + ProPublica",
    "source_detail": "Northwestern Memorial Healthcare $465M (2020); serves ~3M patients/year across system",
    "extraction_note": "2020 data; system has grown significantly. Cost per patient encounter est. $155 based on 2020 figures.",
    "impact_description": "one patient encounter at Northwestern Medicine hospitals including Palos Hospital, Northwestern Memorial, and affiliated facilities",
    "annual_expenses_usd": 465184122,
    "revenue_year": 2020,
  },

  # Perelman Performing Arts Center / World Trade Center Performing Arts Center
  {
    "name": "Perelman Performing Arts Center",
    "ein": "455316035",
    "pp_name": [
      "World Trade Center Performing Arts Center Inc",
      "World Trade Center Performing Arts Center",
      "Perelman Performing Arts Center",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one performance attendee at the WTC PAC",
    "primary_metric_value": 100000,
    "primary_metric_unit": "attendees at Perelman Performing Arts Center performances",
    "cost_per_outcome_usd": 89,
    "impact_per_100_usd": 1.12,
    "confidence": "low",
    "source": "Perelman PAC Annual Report + ProPublica",
    "source_detail": "WTC PAC: $8.9M expenses (2022, pre-opening). Opened 2023. Estimated 100K attendees/year at capacity.",
    "extraction_note": "2022 expenses are pre-opening (construction/planning). Operational attendance est. 100K/year. Confidence low.",
    "impact_description": "one person attending a performance at the Perelman Performing Arts Center at the World Trade Center",
    "annual_expenses_usd": 8927388,
    "revenue_year": 2022,
  },

  # Advanced Education Research and Development Fund (AERDF)
  {
    "name": "Advanced Education Research and Development Fund",
    "ein": "853624930",
    "pp_name": [
      "Advanced Education Research And Development Fund",
      "Advanced Education Research And Development Fund Inc",
      "Aerdf",
    ],
    "cause": "education",
    "primary_metric_label": "one student benefiting from education R&D",
    "primary_metric_value": 200000,
    "primary_metric_unit": "students benefiting from learning-science research programs",
    "cost_per_outcome_usd": 154,
    "impact_per_100_usd": 0.649,
    "confidence": "low",
    "source": "AERDF Annual Report + ProPublica",
    "source_detail": "AERDF 2023: $30.8M expenses. Funds R&D into evidence-based learning approaches reaching ~200K students.",
    "extraction_note": "Estimated student reach from program descriptions. Confidence low — impact is indirect through research.",
    "impact_description": "one student benefiting from AERDF-funded learning-science research programs in math, literacy, or science education",
    "annual_expenses_usd": 30804615,
    "revenue_year": 2023,
  },

  # Rensselaer Polytechnic Institute
  {
    "name": "Rensselaer Polytechnic Institute",
    "ein": "141340095",
    "pp_name": [
      "Rensselaer Polytechnic Institute",
      "Rensselaer Polytechnic Inst",
      "Rpi",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 41000,
    "impact_per_100_usd": 0.00244,
    "confidence": "medium",
    "source": "RPI Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$41K. Expenses $642M. ~7,500 students.",
    "extraction_note": "RPI need-based grant average from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Rensselaer Polytechnic Institute student (avg ~$41,000 institutional grant)",
    "annual_expenses_usd": 642598495,
    "revenue_year": 2023,
  },

  # Indiana University Foundation
  {
    "name": "Indiana University",
    "ein": "356018940",
    "pp_name": [
      "Indiana University Foundation",
      "Indiana University",
      "Indiana Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 10000,
    "impact_per_100_usd": 0.01,
    "confidence": "medium",
    "source": "Indiana University Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24 IUB: avg institutional grant ~$10K. Foundation expenses $261M. ~90K students system-wide.",
    "extraction_note": "Indiana University Foundation is the 990-filing entity for IU fundraising.",
    "impact_description": "one year of need-based financial aid for one Indiana University student (avg ~$10,000 institutional grant)",
    "annual_expenses_usd": 261097805,
    "revenue_year": 2023,
  },

  # America Achieves
  {
    "name": "America Achieves",
    "ein": "273238471",
    "pp_name": ["America Achieves Inc", "America Achieves"],
    "cause": "education",
    "primary_metric_label": "one student impacted through education advocacy",
    "primary_metric_value": 500000,
    "primary_metric_unit": "students impacted through education policy and workforce development advocacy",
    "cost_per_outcome_usd": 32,
    "impact_per_100_usd": 3.15,
    "confidence": "low",
    "source": "America Achieves Annual Report + ProPublica",
    "source_detail": "America Achieves 2023: $15.9M expenses. Works on teacher quality, workforce credentials, education equity affecting ~500K students.",
    "extraction_note": "Policy and advocacy org. Indirect impact on students estimated at $15.9M / 500K = $31.8/student.",
    "impact_description": "one student benefiting from America Achieves' work on teacher quality, workforce readiness, and educational equity policy",
    "annual_expenses_usd": 15879559,
    "revenue_year": 2023,
  },

  # Theodore Roosevelt Presidential Library Foundation
  {
    "name": "Theodore Roosevelt Presidential Library Foundation",
    "ein": "471324043",
    "pp_name": [
      "Theodore Roosevelt Presidential Library Foundation",
      "Theodore Roosevelt Presidential Library Fdn",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one visitor to Theodore Roosevelt Presidential Library",
    "primary_metric_value": 100000,
    "primary_metric_unit": "visitors to Theodore Roosevelt Presidential Library",
    "cost_per_outcome_usd": 52,
    "impact_per_100_usd": 1.92,
    "confidence": "low",
    "source": "TRPLF Annual Report + ProPublica",
    "source_detail": "TRPLF 2023: $5.2M expenses (pre-opening). Library opens in Medora, ND ~2026. Projected 100K visitors/year.",
    "extraction_note": "Currently in construction/fundraising phase. Impact metric is projected post-opening. Confidence low.",
    "impact_description": "one visitor experiencing the Theodore Roosevelt Presidential Library in Medora, North Dakota",
    "annual_expenses_usd": 5223363,
    "revenue_year": 2023,
  },

  # University of Hawaii Foundation
  {
    "name": "University of Hawaii",
    "ein": "990085260",
    "pp_name": [
      "University Of Hawaii Foundation",
      "University Of Hawaii",
      "Univ Of Hawaii",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 9500,
    "impact_per_100_usd": 0.01053,
    "confidence": "medium",
    "source": "University of Hawaii Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$9,500. Foundation expenses $68.5M. ~18K students.",
    "extraction_note": "University of Hawaii Foundation is the 990-filing entity for UH fundraising.",
    "impact_description": "one year of need-based financial aid for one University of Hawaii student (avg ~$9,500 institutional grant)",
    "annual_expenses_usd": 68484452,
    "revenue_year": 2023,
  },

  # Atlanta Police Foundation
  {
    "name": "Atlanta Police Foundation",
    "ein": "113655936",
    "pp_name": ["Atlanta Police Foundation Inc", "Atlanta Police Foundation"],
    "cause": "community",
    "primary_metric_label": "one Atlantan served through police programs",
    "primary_metric_value": 500000,
    "primary_metric_unit": "Atlanta residents served through foundation-funded public safety programs",
    "cost_per_outcome_usd": 28,
    "impact_per_100_usd": 3.62,
    "confidence": "low",
    "source": "Atlanta Police Foundation Annual Report + ProPublica",
    "source_detail": "APF 2023: $13.8M expenses. Funds police technology, training, and community safety for ~500K Atlantans.",
    "extraction_note": "Estimated reach of funded programs across Atlanta. $13.8M / 500K = $27.6/resident.",
    "impact_description": "one Atlanta resident benefiting from Atlanta Police Foundation-funded public safety technology, officer training, and community programs",
    "annual_expenses_usd": 13791808,
    "revenue_year": 2023,
  },

  # Atrium Health Foundation
  {
    "name": "Atrium Health Foundation",
    "ein": "566060481",
    "pp_name": "Atrium Health Foundation",
    "cause": "health",
    "primary_metric_label": "one patient served through Atrium programs",
    "primary_metric_value": 500000,
    "primary_metric_unit": "patients served through Atrium Health Foundation-funded programs",
    "cost_per_outcome_usd": 129,
    "impact_per_100_usd": 0.775,
    "confidence": "low",
    "source": "Atrium Health Foundation Annual Report + ProPublica",
    "source_detail": "Atrium Health Foundation 2023: $64.5M expenses. Atrium Health serves ~2M patients/year in Carolinas.",
    "extraction_note": "Foundation funds programs above base operations. Est. 500K patients reached through funded programs.",
    "impact_description": "one patient benefiting from Atrium Health Foundation-funded programs in cancer care, community health, or cardiovascular services",
    "annual_expenses_usd": 64503775,
    "revenue_year": 2023,
  },

  # New York-Presbyterian Hospital
  {
    "name": "New York-Presbyterian Hospital",
    "ein": "133957095",
    "pp_name": [
      "The New York And Presbyterian Hospital",
      "New York Presbyterian Hospital",
      "New York Presbyteran Hospital",
      "Newyork Presbyterian Hospital",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at NYP",
    "primary_metric_value": 2500000,
    "primary_metric_unit": "patient encounters at NewYork-Presbyterian hospital system",
    "cost_per_outcome_usd": 3902,
    "impact_per_100_usd": 0.0256,
    "confidence": "medium",
    "source": "NYP Annual Report + ProPublica",
    "source_detail": "NYP 2023: $9.76B expenses; ~2.5M patient encounters across NYP system including Weill Cornell and Columbia campuses",
    "extraction_note": "$9.76B / 2.5M encounters = $3,902/encounter. One of the largest hospital systems in the US.",
    "impact_description": "one patient encounter at NewYork-Presbyterian, one of the nation's largest and most comprehensive academic medical centers",
    "annual_expenses_usd": 9755790336,
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
