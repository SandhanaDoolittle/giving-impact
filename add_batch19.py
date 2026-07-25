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

  # Drexel University — private research university in Philadelphia
  {
    "name": "Drexel University",
    "ein": "231352630",
    "pp_name": [
      "Drexel University",
      "Drexel Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Drexel University student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Drexel University",
    "cost_per_outcome_usd": 30000,
    "impact_per_100_usd": 0.00333,
    "confidence": "medium",
    "source": "Drexel University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Drexel University 2023: $1.4B expenses. Private research university in Philadelphia with ~25,000 students. CDS 2023-24 avg institutional need-based grant ~$30,000. Known for co-op education program, law school, and engineering.",
    "extraction_note": "CDS 2023-24 Drexel avg institutional need-based grant used. Drexel's co-op program places students in paid professional work experiences, often generating more lifetime earnings than comparable universities.",
    "impact_description": "one year of need-based financial aid for one Drexel University student (avg ~$30,000 institutional grant) — a Philadelphia private research university known for its co-op program that places students in paid industry work and has nationally ranked engineering, nursing, and law programs",
    "annual_expenses_usd": 1405662980,
    "revenue_year": 2023,
  },

  # Texas Tech Foundation — fundraising arm for Texas Tech University
  {
    "name": "Texas Tech Foundation",
    "ein": "756043842",
    "pp_name": [
      "Texas Tech Foundation Inc",
      "Texas Tech Foundation",
      "Texas Tech University Foundation",
      "Texas Tech University",
      "Texas Tech Univ",
      "Ttu Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Texas Tech student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Texas Tech University",
    "cost_per_outcome_usd": 7000,
    "impact_per_100_usd": 0.01429,
    "confidence": "medium",
    "source": "Texas Tech University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Texas Tech Foundation 2023: $97M expenses. Private foundation managing philanthropy for Texas Tech University (Lubbock), a public research university with ~40,000 students. CDS 2023-24 avg institutional need-based grant ~$7,000.",
    "extraction_note": "CDS 2023-24 Texas Tech avg institutional need-based grant used. TTU is a major public research university with nationally ranked programs in agricultural science, engineering, and business.",
    "impact_description": "one year of need-based financial aid for one Texas Tech University student (avg ~$7,000 institutional grant) — a public research university in Lubbock with 40,000+ students and nationally ranked programs in agriculture, engineering, and business",
    "annual_expenses_usd": 97007634,
    "revenue_year": 2023,
  },

  # University of Montana Foundation
  {
    "name": "University of Montana Foundation",
    "ein": "810362989",
    "pp_name": [
      "University Of Montana Foundation",
      "University Of Montana",
      "Umt Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one University of Montana student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Montana",
    "cost_per_outcome_usd": 5500,
    "impact_per_100_usd": 0.01818,
    "confidence": "medium",
    "source": "University of Montana Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Montana Foundation 2023: $35.2M expenses. Private foundation for University of Montana (Missoula), the state's flagship university with ~10,000 students. CDS 2023-24 avg institutional need-based grant ~$5,500.",
    "extraction_note": "CDS 2023-24 UM avg institutional need-based grant used. Montana is known for its natural resource management, law, and journalism programs, and its stunning surroundings near Glacier and Yellowstone.",
    "impact_description": "one year of need-based financial aid for one University of Montana student (avg ~$5,500 institutional grant) — Montana's flagship public university in Missoula with nationally ranked programs in creative writing, journalism, and environmental law",
    "annual_expenses_usd": 35180976,
    "revenue_year": 2023,
  },

  # UC Santa Barbara Foundation — fundraising arm for UC Santa Barbara
  {
    "name": "UC Santa Barbara Foundation",
    "ein": "237314834",
    "pp_name": [
      "Uc Santa Barbara Foundation",
      "University Of California Santa Barbara",
      "Ucsb Foundation",
      "Ucsb",
      "Uc Santa Barbara",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one UCSB student",
    "primary_metric_unit": "student-year of need-based financial aid funded at UC Santa Barbara",
    "cost_per_outcome_usd": 17000,
    "impact_per_100_usd": 0.00588,
    "confidence": "medium",
    "source": "UCSB Common Data Set 2023-24 + ProPublica",
    "source_detail": "UC Santa Barbara Foundation 2023: $35.1M expenses. Private foundation supporting UC Santa Barbara, a top-15 public research university with ~26,000 students. CDS 2023-24 avg institutional need-based grant ~$17,000.",
    "extraction_note": "CDS 2023-24 UCSB avg institutional need-based grant used. UCSB has 7 Nobel laureates, world-class physics, materials science, and marine biology programs, and is consistently ranked #7-10 among public universities.",
    "impact_description": "one year of need-based financial aid for one UC Santa Barbara student (avg ~$17,000 institutional grant) — a top-10 public research university with 7 Nobel laureates among faculty and nationally ranked physics, engineering, and environmental science programs",
    "annual_expenses_usd": 35122690,
    "revenue_year": 2023,
  },

  # California Science Center Foundation — science museum in LA (free admission)
  {
    "name": "California Science Center Foundation",
    "ein": "952210527",
    "pp_name": [
      "California Science Center Foundation",
      "California Science Center",
      "Cal Science Center",
    ],
    "cause": "education",
    "primary_metric_label": "one visitor to the California Science Center",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "visitors to the California Science Center in Los Angeles including Space Shuttle Endeavour exhibit, IMAX Theater, and science education programs (free admission)",
    "cost_per_outcome_usd": 47,
    "impact_per_100_usd": 2.14,
    "confidence": "medium",
    "source": "California Science Center Annual Report + ProPublica",
    "source_detail": "California Science Center Foundation 2023: $93.7M expenses. Free admission science museum in Los Angeles operating the Space Shuttle Endeavour exhibit, IMAX Theater, and education programs. 2M+ visitors/year.",
    "extraction_note": "$93,669,765 / 2,000,000 visitors = $46.8/visitor. California Science Center offers free general admission and is the only place in the world to see a complete Space Shuttle Orbiter standing in launch position. Also operates IMAX and extensive school programs.",
    "impact_description": "one person visiting the California Science Center — a free science museum in Los Angeles housing Space Shuttle Endeavour standing in launch position, serving 2M+ visitors/year with exhibits on ecosystems, technology, and the history of space exploration",
    "annual_expenses_usd": 93669765,
    "revenue_year": 2023,
  },

  # Educate Girls — mobilizing Indian communities to enroll girls in school
  {
    "name": "Educate Girls",
    "ein": "464493359",
    "pp_name": [
      "Educate Girls",
    ],
    "cause": "education",
    "primary_metric_label": "one girl enrolled in school through Educate Girls programs in India",
    "primary_metric_value": 400000,
    "primary_metric_unit": "girls enrolled or retained in school in rural Rajasthan, Madhya Pradesh, and Uttar Pradesh through Educate Girls community mobilization programs",
    "cost_per_outcome_usd": 75,
    "impact_per_100_usd": 1.33,
    "confidence": "medium",
    "source": "Educate Girls Annual Report + ProPublica",
    "source_detail": "Educate Girls 2024: $30M expenses (US entity). Trains community volunteers (Team Balika) to enroll out-of-school girls and improve learning. Works in 30,000+ villages across rural India with 400K+ girls impacted annually.",
    "extraction_note": "$30,029,529 / 400,000 girls = $75.1/girl. Educate Girls operates through community volunteers ('Team Balika') who identify out-of-school girls and advocate for their enrollment. High multiplier effect from volunteer model. GiveWell has reviewed this org positively.",
    "impact_description": "one girl enrolled in school in rural India through Educate Girls' community volunteer program — mobilizing 65,000+ community members to identify, enroll, and retain girls in school in 30,000+ villages across Rajasthan, Madhya Pradesh, and Uttar Pradesh",
    "annual_expenses_usd": 30029529,
    "revenue_year": 2024,
  },

  # Camp Twin Lakes — free summer camp for children with serious illnesses, disabilities, and challenges
  {
    "name": "Camp Twin Lakes",
    "ein": "581826782",
    "pp_name": [
      "Camp Twin Lakes Inc",
      "Camp Twin Lakes",
    ],
    "cause": "health",
    "primary_metric_label": "one child attending Camp Twin Lakes",
    "primary_metric_value": 5000,
    "primary_metric_unit": "children with serious illnesses, disabilities, and other life challenges attending Camp Twin Lakes at no cost to their families",
    "cost_per_outcome_usd": 1509,
    "impact_per_100_usd": 0.0663,
    "confidence": "medium",
    "source": "Camp Twin Lakes Annual Report + ProPublica",
    "source_detail": "Camp Twin Lakes 2023: $7.5M expenses. Free summer camp in Georgia for children with serious illnesses (cancer, sickle cell, diabetes, HIV), developmental disabilities, and other challenges. ~5,000 campers/year at no cost to families.",
    "extraction_note": "$7,545,573 / 5,000 campers = $1,509/camper. Camp Twin Lakes provides therapeutic recreation and respite care for children whose conditions often prevent participation in traditional summer camps.",
    "impact_description": "one child with cancer, diabetes, sickle cell disease, or another serious condition attending Camp Twin Lakes — Georgia's premier therapeutic camp providing 5,000+ children/year the joy and growth of summer camp at no cost to their families",
    "annual_expenses_usd": 7545573,
    "revenue_year": 2023,
  },

  # Jewish Federations of North America — umbrella for 146 local Jewish federations
  {
    "name": "Jewish Federations of North America",
    "ein": "131624240",
    "pp_name": [
      "The Jewish Federations Of North America Inc",
      "Jewish Federations Of North America",
      "Jfna",
      "United Jewish Communities",
    ],
    "cause": "community",
    "primary_metric_label": "one person served through JFNA's federated Jewish community programs",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "people served through Jewish Federations of North America's 146 member federations providing social services, emergency aid, Jewish education, and global Jewish rescue",
    "cost_per_outcome_usd": 283,
    "impact_per_100_usd": 0.354,
    "confidence": "low",
    "source": "JFNA Annual Report + ProPublica",
    "source_detail": "Jewish Federations of North America 2023: $283M expenses. Umbrella for 146 local Jewish federations collectively raising $3B+/year. Coordinates global Israel emergency response, overseas rescue operations, and local Jewish social services.",
    "extraction_note": "$282,969,683 / 1,000,000 people served = $282.97/person. JFNA coordinates Holocaust survivor services, Israel emergency funds, and the Global Jewish network. Most impact is through federated local community programs not captured in JFNA's own 990.",
    "impact_description": "one person served through the Jewish Federations of North America system — the collective fundraising backbone for 146 local Jewish federations raising $3B+/year for Holocaust survivor care, Israel emergency response, Jewish education, and global Jewish community rescue",
    "annual_expenses_usd": 282969683,
    "revenue_year": 2023,
  },

  # University of Houston Foundation — fundraising for UH system
  {
    "name": "University of Houston Foundation",
    "ein": "746041411",
    "pp_name": [
      "University Of Houston Foundation",
      "University Of Houston",
      "Uh Foundation",
      "Uhf",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one University of Houston student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Houston",
    "cost_per_outcome_usd": 9000,
    "impact_per_100_usd": 0.01111,
    "confidence": "medium",
    "source": "University of Houston Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Houston Foundation 2023: $10.5M expenses. Private foundation raising gifts for University of Houston, a public research university with ~47,000 students (Houston's flagship institution). CDS 2023-24 avg institutional need-based grant ~$9,000.",
    "extraction_note": "CDS 2023-24 UH avg institutional need-based grant used. UH is Houston's flagship public research university with nationally ranked programs in engineering, business, and pharmacy. Highly diverse student body (one of the most ethnically diverse universities in the US).",
    "impact_description": "one year of need-based financial aid for one University of Houston student (avg ~$9,000 institutional grant) — Houston's flagship public research university with 47,000+ students, one of America's most ethnically diverse universities, with nationally ranked engineering and business programs",
    "annual_expenses_usd": 10476449,
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
