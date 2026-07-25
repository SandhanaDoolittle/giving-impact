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

# YoungArts: grant text has "(YOUNGARTS)" in parens which survive normalize() as an extra token
# "NATIONAL FOUNDATION FOR ADVANCEMENT IN THE ARTS INC (YOUNGARTS)"
# normalizes to "NATIONAL FOUNDATION FOR ADVANCEMENT IN ARTS YOUNGARTS" (INC + THE dropped)
add_aliases(data, "YoungArts", [
    "National Foundation For Advancement In The Arts Inc Youngarts",
    "National Foundation For Advancement In The Arts Youngarts",
    "Youngarts Foundation",
])

# Junior Achievement USA: grant text "JUNIOR ACHIEVEMENT NORTH" (a MN regional chapter)
# JA North is part of the JA network — same mission as national org
add_aliases(data, "Junior Achievement USA", [
    "Junior Achievement North",
    "Junior Achievement Of Greater St Paul",
    "Junior Achievement Minnesota",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Tampa Bay Performing Arts Center (Straz Center)
  {
    "name": "Straz Center for the Performing Arts",
    "ein": "592037085",
    "pp_name": [
      "Tampa Bay Performing Arts Center",
      "Tampa Bay Performing Arts Center David A Straz Jr Center For The Per",
      "Tampa Bay Performing Arts Center Foundation",
      "David A Straz Jr Center For The Performing Arts",
      "Straz Center For The Performing Arts",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one performance attendee at Straz Center",
    "primary_metric_value": 550000,
    "primary_metric_unit": "attendees at Straz Center for the Performing Arts performances and programs",
    "cost_per_outcome_usd": 99,
    "impact_per_100_usd": 1.01,
    "confidence": "medium",
    "source": "Straz Center Annual Report + ProPublica",
    "source_detail": "Tampa Bay Performing Arts Center 2023: $54.2M expenses. One of the Southeast's largest performing arts centers, ~550K attendees/year.",
    "extraction_note": "$54,182,479 / 550,000 = $98.5/attendee. Straz Center hosts Broadway shows, opera, ballet, and education programs.",
    "impact_description": "one person attending a performance or educational program at Straz Center for the Performing Arts in Tampa, FL — one of the largest performing arts centers in the Southeast",
    "annual_expenses_usd": 54182479,
    "revenue_year": 2023,
  },

  # Robertson Scholars Leadership Program
  {
    "name": "Robertson Scholars Leadership Program",
    "ein": "202479103",
    "pp_name": [
      "The Robertson Scholars Leadership Program",
      "Robertson Scholars Leadership Program",
      "Robertson Scholars Program",
    ],
    "cause": "education",
    "primary_metric_label": "one Robertson Scholar funded for one year",
    "primary_metric_value": 56,
    "primary_metric_unit": "Robertson Scholars receiving full-ride scholarships to Duke or UNC-Chapel Hill",
    "cost_per_outcome_usd": 161000,
    "impact_per_100_usd": 0.000621,
    "confidence": "medium",
    "source": "Robertson Scholars Annual Report + ProPublica",
    "source_detail": "Robertson Scholars 2023: $9M expenses. Awards ~56 full-ride scholarships/year to Duke or UNC-Chapel Hill with cross-campus leadership training.",
    "extraction_note": "$9,022,046 / 56 scholars = $161,108/scholar (full scholarship including leadership programs). Programs include summer experiences and leadership development.",
    "impact_description": "one Robertson Scholar receiving a full-ride scholarship and leadership development at Duke University or UNC-Chapel Hill, with programs in Africa and summer experiences",
    "annual_expenses_usd": 9022046,
    "revenue_year": 2023,
  },

  # FWDUS Education Fund
  {
    "name": "FWDUS Education Fund",
    "ein": "820962378",
    "pp_name": [
      "Fwdus Education Fund Inc",
      "Fwdus Education Fund",
      "FWD.us Education Fund",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged through immigration reform advocacy",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "people engaged through immigration policy advocacy and civic education",
    "cost_per_outcome_usd": 17,
    "impact_per_100_usd": 5.86,
    "confidence": "low",
    "source": "FWDUS Annual Report + ProPublica",
    "source_detail": "FWDUS Education Fund 2023: $17.1M expenses. Technology-sector-led immigration reform advocacy reaching ~1M people through civic engagement.",
    "extraction_note": "Policy advocacy org supporting DACA, immigration pathways. Diffuse impact estimated at 1M people engaged. $17.1M / 1M = $17.1/person.",
    "impact_description": "one person engaged through FWD.us Education Fund's immigration policy reform work, including support for DACA recipients and bipartisan immigration legislation",
    "annual_expenses_usd": 17073154,
    "revenue_year": 2023,
  },

  # Foundation for Jewish Camp
  {
    "name": "Foundation for Jewish Camp",
    "ein": "223551013",
    "pp_name": [
      "Foundation For Jewish Camp Inc",
      "Foundation For Jewish Camp",
    ],
    "cause": "education",
    "primary_metric_label": "one Jewish youth funded to attend summer camp",
    "primary_metric_value": 5000,
    "primary_metric_unit": "Jewish youth receiving camp scholarships or attending camp through FJC programs",
    "cost_per_outcome_usd": 2800,
    "impact_per_100_usd": 0.0357,
    "confidence": "low",
    "source": "Foundation for Jewish Camp Annual Report + ProPublica",
    "source_detail": "Foundation for Jewish Camp 2023: $14M expenses. Provides scholarships and capacity support for ~5,000 Jewish youth per year to attend Jewish overnight camps.",
    "extraction_note": "$13,992,784 / 5,000 = $2,799/camper. FJC's Camper Scholarship Program and other initiatives fuel access to Jewish summer camp.",
    "impact_description": "one Jewish youth receiving a scholarship or camp support to attend Jewish overnight summer camp — a proven vehicle for Jewish identity, leadership, and community",
    "annual_expenses_usd": 13992784,
    "revenue_year": 2023,
  },

  # Avalon Nature Preserve (Stony Brook, NY)
  {
    "name": "Avalon Nature Preserve",
    "ein": "753165488",
    "pp_name": [
      "Avalon Nature Preserve Inc",
      "Avalon Nature Preserve",
    ],
    "cause": "environment",
    "primary_metric_label": "one acre of Long Island nature preserve stewarded",
    "primary_metric_value": 2000,
    "primary_metric_unit": "acres of Long Island nature preserve protected and stewarded",
    "cost_per_outcome_usd": 2876,
    "impact_per_100_usd": 0.0348,
    "confidence": "low",
    "source": "Avalon Nature Preserve Annual Report + ProPublica",
    "source_detail": "Avalon Nature Preserve 2023: $5.75M expenses. Manages ~2,000 acres of preserved open space in Stony Brook, NY (Long Island).",
    "extraction_note": "$5,751,089 / 2,000 acres = $2,875.5/acre stewarded per year. Long Island land preservation is high-cost due to land values.",
    "impact_description": "one acre of open space and wildlife habitat at Avalon Nature Preserve in Stony Brook, NY permanently protected and actively stewarded",
    "annual_expenses_usd": 5751089,
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
