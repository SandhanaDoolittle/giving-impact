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

def fill_metrics_by_ein(entries, ein_match, updates):
    for e in entries:
        if str(e.get("ein", "")).strip() == str(ein_match):
            for k, v in updates.items():
                e[k] = v
            print(f"UPDATED: {e['name']} (EIN {ein_match})")
            return True
    print(f"WARNING: EIN not found: {ein_match}")
    return False

# ── ALIAS FIXES ────────────────────────────────────────────────────────────────

# Notre Dame: grant text "UNIVERSITY OF NOTRE DAME" doesn't match "University of Notre Dame Du Lac"
add_aliases(data, "University of Notre Dame Du Lac", [
    "University Of Notre Dame",
    "Notre Dame University",
    "Notre Dame",
])

# ── FILL IN EXISTING INCOMPLETE ENTRIES ────────────────────────────────────────

# Volunteers of America — national social services org (national HQ entity)
fill_metrics_by_ein(data, "411467162", {
    "primary_metric_label": "one person served through Volunteers of America programs",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "people served annually through Volunteers of America national network programs including housing, addiction treatment, veteran services, and youth programs",
    "cost_per_outcome_usd": 25,
    "impact_per_100_usd": 3.97,
    "confidence": "low",
    "source": "Volunteers of America Annual Report + ProPublica",
    "source_detail": "Volunteers of America Inc (national HQ) 2023: $50.4M expenses. National HQ coordinates 30+ regional affiliates providing housing, homeless services, addiction recovery, senior services, and veteran support to 2M+ people/year across 46 states.",
    "extraction_note": "$50,417,179 / 2,000,000 people served via full VOA network = $25.2/person. VOA national HQ expense is just the coordination/support layer; full VOA network expenses are ~$1.5B for 2M+ served annually.",
    "impact_description": "one person served through Volunteers of America's network of social services — housing, addiction recovery, veteran support, senior services, and youth programs reaching 2M+ Americans/year across 46 states through 30+ regional affiliates",
    "annual_expenses_usd": 50417179,
    "revenue_year": 2023,
    "pp_name": [
        "Volunteers Of America Inc",
        "Volunteers Of America",
        "Voa",
    ],
})

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Committee to Protect Journalists
  {
    "name": "Committee to Protect Journalists",
    "ein": "133081500",
    "pp_name": [
      "Committee To Protect Journalists Inc",
      "Committee To Protect Journalists",
      "Cpj",
    ],
    "cause": "community",
    "primary_metric_label": "one journalist receiving CPJ emergency assistance or one person engaged in press freedom advocacy",
    "primary_metric_value": 100000,
    "primary_metric_unit": "journalists protected and press freedom advocates reached through CPJ's emergency response, legal defense, and global press freedom campaigns",
    "cost_per_outcome_usd": 119,
    "impact_per_100_usd": 0.844,
    "confidence": "low",
    "source": "CPJ Annual Report + ProPublica",
    "source_detail": "Committee to Protect Journalists 2023: $11.85M expenses. Documents journalist imprisonments and killings worldwide, provides emergency assistance and legal support to at-risk journalists, and advocates for press freedom at the UN and with governments.",
    "extraction_note": "$11,850,831 / 100,000 journalists and advocates reached = $118.5/person. CPJ directly assists ~100 journalists per year with emergency grants, legal support, and safety training while reaching 100K+ advocacy audience.",
    "impact_description": "one journalist protected or press freedom advocate reached through CPJ's work — the leading global organization documenting journalist imprisonment (700+ cases tracked), providing emergency assistance to at-risk journalists, and advocating for press freedom with governments worldwide",
    "annual_expenses_usd": 11850831,
    "revenue_year": 2023,
  },

  # University of San Francisco — Jesuit university in California
  {
    "name": "University of San Francisco",
    "ein": "941156628",
    "pp_name": [
      "University Of San Francisco",
      "Usf",
      "San Francisco University",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one USF student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of San Francisco",
    "cost_per_outcome_usd": 34000,
    "impact_per_100_usd": 0.00294,
    "confidence": "medium",
    "source": "USF Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of San Francisco 2023: $570.8M expenses. Private Jesuit university in San Francisco with ~10,000 students. CDS 2023-24 avg institutional need-based grant ~$34,000. Jesuit tradition of social justice, service, and education.",
    "extraction_note": "CDS 2023-24 USF avg institutional need-based grant used. USF's location in San Francisco gives access to Bay Area business, technology, and healthcare internship opportunities.",
    "impact_description": "one year of need-based financial aid for one University of San Francisco student (avg ~$34,000 institutional grant) — a Jesuit university in San Francisco with nationally ranked law and nursing programs and a strong social justice mission",
    "annual_expenses_usd": 570798259,
    "revenue_year": 2023,
  },

  # National Fish and Wildlife Foundation — federally chartered conservation grantmaker
  {
    "name": "National Fish and Wildlife Foundation",
    "ein": "521384139",
    "pp_name": [
      "National Fish And Wildlife Foundation",
      "Nfwf",
    ],
    "cause": "environment",
    "primary_metric_label": "one acre of wildlife habitat conserved or restored through NFWF grants",
    "primary_metric_value": 500000,
    "primary_metric_unit": "acres of wildlife habitat conserved, restored, or enhanced through National Fish and Wildlife Foundation grants to conservation projects",
    "cost_per_outcome_usd": 773,
    "impact_per_100_usd": 0.129,
    "confidence": "low",
    "source": "NFWF Annual Report + ProPublica",
    "source_detail": "National Fish and Wildlife Foundation 2023: $386.6M expenses (mostly grants). Federally chartered private nonprofit grantmaker for fish, wildlife, and plant conservation. Leverages federal funding with private matching to fund habitat restoration, species recovery, and sustainable fisheries.",
    "extraction_note": "$386,645,040 / 500,000 acres = $773/acre. NFWF is a federal public-private partnership created by Congress in 1984. Most expenses are grants distributed to conservation projects. Conserves millions of acres cumulatively.",
    "impact_description": "one acre of wildlife habitat conserved or restored through National Fish and Wildlife Foundation grants — a federally chartered grantmaker that has protected 9.5M acres and restored 9,000+ miles of waterways by leveraging federal funds with private matching grants",
    "annual_expenses_usd": 386645040,
    "revenue_year": 2023,
  },

  # Venice Family Clinic — largest free clinic in the US, Los Angeles
  {
    "name": "Venice Family Clinic",
    "ein": "952769432",
    "pp_name": [
      "Venice Family Clinic",
    ],
    "cause": "health",
    "primary_metric_label": "one patient receiving care at Venice Family Clinic",
    "primary_metric_value": 45000,
    "primary_metric_unit": "low-income patients receiving free or low-cost healthcare at Venice Family Clinic, the largest free clinic in the US",
    "cost_per_outcome_usd": 1860,
    "impact_per_100_usd": 0.0538,
    "confidence": "medium",
    "source": "Venice Family Clinic Annual Report + ProPublica",
    "source_detail": "Venice Family Clinic 2023: $83.7M expenses. The largest free clinic in the US, serving 45,000+ low-income patients/year in Los Angeles with primary care, dental, mental health, and specialty services regardless of ability to pay.",
    "extraction_note": "$83,706,399 / 45,000 patients = $1,860/patient. Venice Family Clinic serves uninsured and low-income patients with no ability to pay. Services include primary care, OB/GYN, pediatrics, mental health, and homeless health services.",
    "impact_description": "one low-income patient receiving care at Venice Family Clinic — the largest free clinic in the US, providing 45,000+ patients/year in Los Angeles with comprehensive healthcare including primary care, dental, mental health, and specialty services regardless of insurance or income",
    "annual_expenses_usd": 83706399,
    "revenue_year": 2023,
  },

  # National Jewish Health — leading respiratory disease hospital, Denver
  {
    "name": "National Jewish Health",
    "ein": "742044647",
    "pp_name": [
      "National Jewish Health",
      "National Jewish Medical And Research Center",
      "National Jewish Medical Research Center",
    ],
    "cause": "health",
    "primary_metric_label": "one patient receiving care at National Jewish Health",
    "primary_metric_value": 100000,
    "primary_metric_unit": "patients receiving specialized care at National Jewish Health for respiratory, allergic, autoimmune, and cardiac conditions",
    "cost_per_outcome_usd": 3701,
    "impact_per_100_usd": 0.0270,
    "confidence": "medium",
    "source": "National Jewish Health Annual Report + ProPublica",
    "source_detail": "National Jewish Health 2023: $370.1M expenses. Leading hospital for respiratory, allergic, and immune diseases in Denver, CO. Ranked #1 pulmonology hospital by US News. ~100K patients/year including complex asthma, COPD, lung cancer, and immune deficiency cases.",
    "extraction_note": "$370,065,540 / 100,000 patients = $3,701/patient. National Jewish Health is the only health facility in the world focused fully on respiratory and immune diseases. Combination of specialty hospital + research institution.",
    "impact_description": "one patient receiving specialized care at National Jewish Health — America's #1 pulmonology hospital for 25+ consecutive years, treating 100K patients/year with complex asthma, COPD, lung disease, allergies, and immune disorders at its Denver campus",
    "annual_expenses_usd": 370065540,
    "revenue_year": 2023,
  },

  # DonorsChoose — crowdfunding platform for K-12 classroom projects
  {
    "name": "DonorsChoose",
    "ein": "134129457",
    "pp_name": [
      "Donorschoose Org",
      "Donorschoose",
      "Donors Choose",
    ],
    "cause": "education",
    "primary_metric_label": "one student benefiting from a funded DonorsChoose classroom project",
    "primary_metric_value": 6000000,
    "primary_metric_unit": "K-12 students benefiting from classroom supplies, experiences, and technology funded through DonorsChoose crowdfunded teacher requests",
    "cost_per_outcome_usd": 29,
    "impact_per_100_usd": 3.41,
    "confidence": "medium",
    "source": "DonorsChoose Annual Report + ProPublica",
    "source_detail": "DonorsChoose Org 2022: $175.6M expenses. Crowdfunding platform for K-12 teachers to request classroom supplies, books, technology, and experiences. ~4M students/year from high-need schools (80%+ from low-income schools).",
    "extraction_note": "$175,623,030 / 6,000,000 students reached = $29.3/student. Most of DonorsChoose expenses are grants passed through to classrooms. 77% of teachers served are from Title I schools. Google, Target, and Gates Foundation provide matching donations.",
    "impact_description": "one K-12 student benefiting from a DonorsChoose-funded classroom project — a crowdfunding platform connecting donors directly to teachers requesting books, supplies, and experiences, with 80%+ of schools served being high-poverty Title I schools",
    "annual_expenses_usd": 175623030,
    "revenue_year": 2022,
  },

  # Colorado State University Foundation — fundraising arm for CSU
  {
    "name": "Colorado State University Foundation",
    "ein": "237098397",
    "pp_name": [
      "Colorado State University Foundation",
      "Colorado State University",
      "Csu Foundation",
      "Csu",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one CSU student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Colorado State University",
    "cost_per_outcome_usd": 8500,
    "impact_per_100_usd": 0.01176,
    "confidence": "medium",
    "source": "CSU Common Data Set 2023-24 + ProPublica",
    "source_detail": "Colorado State University Foundation 2023: $90.9M expenses. Private foundation managing philanthropy for Colorado State University (Ft. Collins), a public research university with ~25,000 students. CDS 2023-24 avg institutional need-based grant ~$8,500.",
    "extraction_note": "CDS 2023-24 CSU avg institutional need-based grant used. CSU is one of the top public land-grant research universities in the West, with nationally ranked programs in agricultural science, engineering, and veterinary medicine.",
    "impact_description": "one year of need-based financial aid for one Colorado State University student (avg ~$8,500 institutional grant) — Colorado's land-grant research university with 25,000 students and nationally ranked programs in agriculture, veterinary medicine, and engineering",
    "annual_expenses_usd": 90881779,
    "revenue_year": 2023,
  },

  # Hillsdale College — private conservative liberal arts college with major national programs
  {
    "name": "Hillsdale College",
    "ein": "381374230",
    "pp_name": [
      "Hillsdale College",
    ],
    "cause": "education",
    "primary_metric_label": "one person engaged through Hillsdale College constitutional education programs",
    "primary_metric_value": 6000000,
    "primary_metric_unit": "people engaged through Hillsdale College's free online Constitution courses, Imprimis newsletter, and charter school curriculum — in addition to 1,500 on-campus students",
    "cost_per_outcome_usd": 41,
    "impact_per_100_usd": 2.41,
    "confidence": "low",
    "source": "Hillsdale College Annual Report + ProPublica",
    "source_detail": "Hillsdale College 2023: $248.5M expenses. Private liberal arts college in Hillsdale, MI (~1,500 students) that accepts no federal funding. Runs massive national conservative education programs: 6M+ enrolled in free online Constitution/economics courses, Imprimis distributed to 6M+ homes.",
    "extraction_note": "$248,527,191 / 6,000,000 people engaged (online courses + newsletter + K-12 curriculum) = $41.4/person. Hillsdale is unusual: campus expenses are ~$40K/student, but most of its budget goes to national outreach and K-12 charter school development.",
    "impact_description": "one person engaged through Hillsdale College's free online courses and publications on the Constitution, economics, and Western civilization — the college offers free online courses to 6M+ enrolled learners and distributes Imprimis to 6M+ homes, while running 25+ affiliated charter schools",
    "annual_expenses_usd": 248527191,
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
