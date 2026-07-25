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

# "UNIVERSITY OF LOUISVILLE" (without "Foundation") also appears in grants
add_aliases(data, "University of Louisville Foundation", [
    "University Of Louisville",
    "University Of Louisville Research Foundation",
    "Uofl",
    "U Of Louisville",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Jewish Federation of Cincinnati — community federation for Greater Cincinnati Jewish community
  {
    "name": "Jewish Federation of Cincinnati",
    "ein": "310537174",
    "pp_name": [
      "Jewish Federation Of Cincinnati",
      "Jewish Federation Of Cincinnati Inc",
      "Cincinnati Jewish Federation",
    ],
    "cause": "community",
    "primary_metric_label": "one community member served through Jewish Federation of Cincinnati programs",
    "primary_metric_value": 100000,
    "primary_metric_unit": "community members served through Jewish Federation of Cincinnati's local agency grants and global partnership programs",
    "cost_per_outcome_usd": 267,
    "impact_per_100_usd": 0.375,
    "confidence": "low",
    "source": "Jewish Federation of Cincinnati Annual Report + ProPublica",
    "source_detail": "Jewish Federation of Cincinnati 2023: $26.7M expenses. Community federation allocating funds to 40+ Jewish agencies in Cincinnati, Israel emergency aid, and global Jewish rescue missions.",
    "extraction_note": "$26,686,419 / 100,000 people reached (local services + global) = $266.9/person. Federation funds senior care, Jewish education, social services, Israel programs, and global rescue.",
    "impact_description": "one person served through Jewish Federation of Cincinnati's network of 40+ agencies providing Jewish senior care, education, social services, Israel emergency aid, and overseas Jewish rescue",
    "annual_expenses_usd": 26686419,
    "revenue_year": 2023,
  },

  # Council of Independent Colleges — membership org for private liberal arts colleges
  {
    "name": "Council of Independent Colleges",
    "ein": "16004776",
    "pp_name": [
      "Council Of Independent Colleges",
      "CIC",
    ],
    "cause": "education",
    "primary_metric_label": "one student at a CIC member private college or university",
    "primary_metric_value": 1700000,
    "primary_metric_unit": "students at CIC's 700+ member private colleges and universities benefiting from CIC programs, advocacy, and professional development",
    "cost_per_outcome_usd": 10,
    "impact_per_100_usd": 9.94,
    "confidence": "low",
    "source": "CIC Annual Report + ProPublica",
    "source_detail": "Council of Independent Colleges 2023: $17.1M expenses. Membership organization for 700+ private non-profit colleges collectively serving 1.7M+ students. Provides workshops, grants, advocacy, and peer-learning programs.",
    "extraction_note": "$17,098,412 / 1,700,000 students = $10.06/student indirect benefit. CIC's programs strengthen member institutions through professional development, grant programs, and collaborative initiatives.",
    "impact_description": "one student at a Council of Independent Colleges member institution — CIC's 700+ private non-profit college members collectively serve 1.7M students through programs supported by CIC advocacy and capacity-building",
    "annual_expenses_usd": 17098412,
    "revenue_year": 2023,
  },

  # Birthright Israel Foundation — funds free trips to Israel for Jewish young adults
  {
    "name": "Birthright Israel Foundation",
    "ein": "134092050",
    "pp_name": [
      "Birthright Israel Foundation",
      "The Birthright Israel Foundation",
      "Taglit-Birthright Israel Foundation",
      "Taglit Birthright Israel Foundation",
      "Birthright Israel",
    ],
    "cause": "education",
    "primary_metric_label": "one young Jewish adult on a Birthright Israel trip",
    "primary_metric_value": 50000,
    "primary_metric_unit": "young Jewish adults (ages 18-26) experiencing free 10-day educational trips to Israel through Birthright",
    "cost_per_outcome_usd": 1858,
    "impact_per_100_usd": 0.0538,
    "confidence": "medium",
    "source": "Birthright Israel Foundation Annual Report + ProPublica",
    "source_detail": "Birthright Israel Foundation 2023: $92.9M expenses. US fundraising arm co-funding free 10-day Israel trips for ~50,000 young Jewish adults (ages 18-26) annually.",
    "extraction_note": "$92,850,953 / 50,000 participants = $1,857/participant (US Foundation share). Total program costs ~$250M globally; US Foundation co-funds with Israeli government and diaspora communities.",
    "impact_description": "one young Jewish adult (18-26) on a free 10-day Birthright Israel trip to explore Jewish heritage, culture, and people — a transformational experiential education program proven to strengthen Jewish identity and Israel connection",
    "annual_expenses_usd": 92850953,
    "revenue_year": 2023,
  },

  # Sealaska Heritage Institute — Southeast Alaskan Native cultural preservation
  {
    "name": "Sealaska Heritage Institute",
    "ein": "920081844",
    "pp_name": [
      "Sealaska Heritage Institute",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged in Southeast Alaska Native cultural preservation",
    "primary_metric_value": 30000,
    "primary_metric_unit": "people engaged in Tlingit, Haida, and Tsimshian cultural preservation programs, language nests, arts, and community events through SHI",
    "cost_per_outcome_usd": 772,
    "impact_per_100_usd": 0.129,
    "confidence": "low",
    "source": "Sealaska Heritage Institute Annual Report + ProPublica",
    "source_detail": "Sealaska Heritage Institute 2023: $23.2M expenses. Preserves the cultures of the Tlingit, Haida, and Tsimshian peoples through arts, language revitalization, cultural events, archival research, and education.",
    "extraction_note": "$23,160,357 / 30,000 people engaged (events + language programs + digital + archival access) = $772/person. SHI hosts major cultural events drawing thousands, runs language nests for children, and maintains extensive archives of Indigenous Alaskan culture.",
    "impact_description": "one person engaged in Sealaska Heritage Institute's cultural preservation programs — protecting the living heritage of the Tlingit, Haida, and Tsimshian peoples of Southeast Alaska through arts, language nests, cultural events, and archival research",
    "annual_expenses_usd": 23160357,
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
