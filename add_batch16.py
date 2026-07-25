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

def fill_metrics_by_name(entries, name_match, updates):
    for e in entries:
        if e["name"] == name_match:
            for k, v in updates.items():
                e[k] = v
            print(f"UPDATED: {e['name']}")
            return True
    print(f"WARNING: name not found: {name_match!r}")
    return False

# ── FIX EXISTING ENTRIES ────────────────────────────────────────────────────────

# Notre Dame: existing entry has bad primary_metric_unit ('average annual grant (USD)')
# EIN not set in existing entry; match by name
fill_metrics_by_name(data, "University of Notre Dame Du Lac", {
    "ein": "570564587",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Notre Dame",
    "primary_metric_label": "one year of need-based aid for one Notre Dame student",
    "source": "Notre Dame Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Notre Dame 2023: ~$2B expenses. Private Catholic research university in South Bend, IN with ~13,000 students. Meets 100% of demonstrated financial need. CDS 2023-24 avg institutional need-based grant ~$57,934.",
    "impact_description": "one year of need-based financial aid for one University of Notre Dame student (avg ~$58,000 institutional grant) — a leading private Catholic research university in South Bend, IN meeting 100% of demonstrated need for all admitted students",
})

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Princeton University — Ivy League in New Jersey
  {
    "name": "Princeton University",
    "ein": "210634501",
    "pp_name": [
      "Princeton University",
      "Trustees Of Princeton University",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Princeton student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Princeton University",
    "cost_per_outcome_usd": 75000,
    "impact_per_100_usd": 0.001333,
    "confidence": "high",
    "source": "Princeton University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Princeton University 2023: $2.63B expenses. Private Ivy League university in Princeton, NJ with ~8,000 students. All-grant no-loan aid policy; 100% of demonstrated need met. CDS avg institutional need-based grant ~$75,000.",
    "extraction_note": "CDS 2023-24 Princeton avg institutional grant ~$75,000. Princeton has the largest endowment per student of any US university; students from families earning <$100K pay nothing. Awarded only grants, no loans since 2001.",
    "impact_description": "one year of need-based financial aid for one Princeton University student (avg ~$75,000 grant, no loans required) — an Ivy League university where students from families earning under $100K attend free, with the largest endowment-per-student of any US university",
    "annual_expenses_usd": 2630086000,
    "revenue_year": 2023,
  },

  # Boston College — Jesuit research university in Chestnut Hill, MA
  {
    "name": "Boston College",
    "ein": "42103545",
    "pp_name": [
      "Boston College Trustees",
      "Boston College",
      "Bc",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Boston College student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Boston College",
    "cost_per_outcome_usd": 45000,
    "impact_per_100_usd": 0.00222,
    "confidence": "medium",
    "source": "Boston College Common Data Set 2023-24 + ProPublica",
    "source_detail": "Boston College 2023: $1.29B expenses. Private Jesuit research university in Chestnut Hill, MA with ~15,000 students. CDS 2023-24 avg institutional need-based grant ~$45,000. Top-20 research university with nationally ranked law, social work, and business programs.",
    "extraction_note": "CDS 2023-24 Boston College avg institutional need-based grant used. Jesuit tradition emphasizes service, ethics, and education for the whole person.",
    "impact_description": "one year of need-based financial aid for one Boston College student (avg ~$45,000 institutional grant) — a leading Jesuit research university with nationally ranked law, social work, and business programs in the Greater Boston area",
    "annual_expenses_usd": 1291475190,
    "revenue_year": 2023,
  },

  # Wellesley College — private women's liberal arts college, MA
  {
    "name": "Wellesley College",
    "ein": "42103637",
    "pp_name": [
      "Wellesley College",
      "Trustees Of Wellesley College",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Wellesley College student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Wellesley College",
    "cost_per_outcome_usd": 58000,
    "impact_per_100_usd": 0.001724,
    "confidence": "medium",
    "source": "Wellesley College Common Data Set 2023-24 + ProPublica",
    "source_detail": "Wellesley College 2023: $341M expenses. Private women's liberal arts college in Wellesley, MA with ~2,400 students. Meets 100% of demonstrated need. CDS 2023-24 avg institutional need-based grant ~$58,000.",
    "extraction_note": "CDS 2023-24 Wellesley avg institutional need-based grant used. One of the original 'Seven Sisters' colleges; alma mater of Hillary Clinton, Madeleine Albright, and Nora Ephron. Meets 100% of demonstrated need.",
    "impact_description": "one year of need-based financial aid for one Wellesley College student (avg ~$58,000 institutional grant) — one of the nation's leading women's liberal arts colleges, a Seven Sisters school meeting 100% of demonstrated financial need",
    "annual_expenses_usd": 340731004,
    "revenue_year": 2023,
  },

  # Spelman College — historically Black women's liberal arts college, Atlanta
  {
    "name": "Spelman College",
    "ein": "580566243",
    "pp_name": [
      "Spelman College",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Spelman College student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Spelman College",
    "cost_per_outcome_usd": 22000,
    "impact_per_100_usd": 0.00455,
    "confidence": "medium",
    "source": "Spelman College Common Data Set 2023-24 + ProPublica",
    "source_detail": "Spelman College 2023: $161M expenses. Historically Black women's liberal arts college in Atlanta with ~2,100 students. CDS 2023-24 avg institutional need-based grant ~$22,000. Ranked #1 HBCU in the US.",
    "extraction_note": "CDS 2023-24 Spelman avg institutional need-based grant used. Spelman is the most selective HBCU; graduates go on to lead in medicine, law, government, and the arts at high rates relative to student body size.",
    "impact_description": "one year of need-based financial aid for one Spelman College student (avg ~$22,000 institutional grant) — the nation's #1 ranked HBCU, a premier historically Black women's college in Atlanta producing leaders in medicine, law, STEM, and public service",
    "annual_expenses_usd": 160810189,
    "revenue_year": 2023,
  },

  # Dartmouth College — Ivy League in New Hampshire
  {
    "name": "Dartmouth College",
    "ein": "20222111",
    "pp_name": [
      "Trustees Of Dartmouth College",
      "Dartmouth College",
      "Dartmouth Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Dartmouth student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Dartmouth College",
    "cost_per_outcome_usd": 62000,
    "impact_per_100_usd": 0.001613,
    "confidence": "medium",
    "source": "Dartmouth College Common Data Set 2023-24 + ProPublica",
    "source_detail": "Dartmouth College 2023: $1.41B expenses. Private Ivy League liberal arts college in Hanover, NH with ~6,700 students. Meets 100% of demonstrated need. CDS 2023-24 avg institutional need-based grant ~$62,000.",
    "extraction_note": "CDS 2023-24 Dartmouth avg institutional need-based grant used. Small liberal arts college (undergraduate focus) despite research university designation. Known for its D-Plan flexible quarter system.",
    "impact_description": "one year of need-based financial aid for one Dartmouth College student (avg ~$62,000 institutional grant) — an Ivy League liberal arts university in Hanover, NH meeting 100% of demonstrated financial need, known for undergraduate education and outdoor culture",
    "annual_expenses_usd": 1411739475,
    "revenue_year": 2023,
  },

  # New York Public Radio (WNYC) — NYC public radio, largest public broadcaster in US
  {
    "name": "New York Public Radio",
    "ein": "133015230",
    "pp_name": [
      "New York Public Radio",
      "Wnyc",
      "Nypr",
      "Wnyc Radio",
      "Wqxr",
      "Gothamist",
    ],
    "cause": "education",
    "primary_metric_label": "one regular listener of New York Public Radio programming",
    "primary_metric_value": 4000000,
    "primary_metric_unit": "weekly listeners of New York Public Radio's WNYC, WQXR, and affiliated digital news programming including Gothamist",
    "cost_per_outcome_usd": 22,
    "impact_per_100_usd": 4.55,
    "confidence": "medium",
    "source": "New York Public Radio Annual Report + ProPublica",
    "source_detail": "New York Public Radio 2023: $87.9M expenses. Operates WNYC (NPR affiliate), WQXR (classical music), Gothamist (digital news), and the Radiolab/On the Media podcasts reaching 4M+ weekly listeners.",
    "extraction_note": "$87,923,886 / 4,000,000 weekly listeners = $22/listener/year. NYPR is the largest public media company in the US by reach. Produces WNYC Studios podcasts (Radiolab, On the Media, Nancy) distributed nationally.",
    "impact_description": "one weekly listener of New York Public Radio — America's largest public media company, operating WNYC, WQXR classical radio, Gothamist digital news, and podcasts including Radiolab, On the Media, and More Perfect, reaching 4M+ listeners weekly",
    "annual_expenses_usd": 87923886,
    "revenue_year": 2023,
  },

  # Urban Institute — nonpartisan economic and social policy research
  {
    "name": "Urban Institute",
    "ein": "520880375",
    "pp_name": [
      "Urban Institute",
      "The Urban Institute",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged by Urban Institute policy research",
    "primary_metric_value": 500000,
    "primary_metric_unit": "policymakers, journalists, and citizens engaged through Urban Institute's economics, social policy, housing, and justice research",
    "cost_per_outcome_usd": 275,
    "impact_per_100_usd": 0.363,
    "confidence": "low",
    "source": "Urban Institute Annual Report + ProPublica",
    "source_detail": "Urban Institute 2023: $137.7M expenses. Nonpartisan policy research organization in Washington DC. Publishes 500+ reports/year on housing, health, crime, education, taxes, and immigration policy.",
    "extraction_note": "$137,744,133 / 500,000 people engaged = $275.5/person. Urban Institute's research influences federal budget, housing, and social policy at the highest levels. Primary reach is through policymakers and journalists who use and cite its research.",
    "impact_description": "one policymaker, journalist, or citizen engaged through Urban Institute's policy research — a leading nonpartisan think tank publishing 500+ evidence-based reports/year shaping federal and state policy on housing, health, justice, and economic mobility",
    "annual_expenses_usd": 137744133,
    "revenue_year": 2023,
  },

  # Texas Children's Hospital — Houston, largest pediatric hospital in US
  {
    "name": "Texas Children's Hospital",
    "ein": "741100555",
    "pp_name": [
      "Texas Childrens Hospital",
      "Texas Children S Hospital",
      "Texas Children's Hospital",
    ],
    "cause": "health",
    "primary_metric_label": "one child patient encounter at Texas Children's Hospital",
    "primary_metric_value": 1300000,
    "primary_metric_unit": "child patient encounters at Texas Children's Hospital — the largest children's hospital in the US by patient volume",
    "cost_per_outcome_usd": 2804,
    "impact_per_100_usd": 0.0357,
    "confidence": "medium",
    "source": "Texas Children's Hospital Annual Report + ProPublica",
    "source_detail": "Texas Children's Hospital 2023: $3.64B expenses. America's largest children's hospital in Houston, TX. 1.3M+ patient encounters/year: inpatient, outpatient, urgent care, and emergency. Affiliated with Baylor College of Medicine.",
    "extraction_note": "$3,644,874,281 / 1,300,000 encounters = $2,803.8/encounter. Texas Children's is consistently ranked #3-5 children's hospital nationally. Operates specialty clinics for cancer, heart, neurology, and rare diseases across TX.",
    "impact_description": "one child patient encounter at Texas Children's Hospital — the largest children's hospital in the US by patient volume (1.3M encounters/year), ranked among the top 5 children's hospitals nationally with world-class cancer, heart, and rare disease programs",
    "annual_expenses_usd": 3644874281,
    "revenue_year": 2023,
  },

  # Council on Foreign Relations — foreign policy think tank and publisher of Foreign Affairs
  {
    "name": "Council on Foreign Relations",
    "ein": "131628168",
    "pp_name": [
      "Council On Foreign Relations Inc",
      "Council On Foreign Relations",
      "Cfr",
    ],
    "cause": "community",
    "primary_metric_label": "one person reached through CFR foreign policy research and publications",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "policymakers, scholars, business leaders, and citizens engaged through CFR's foreign policy research, Foreign Affairs magazine, and public programs",
    "cost_per_outcome_usd": 83,
    "impact_per_100_usd": 1.2,
    "confidence": "low",
    "source": "CFR Annual Report + ProPublica",
    "source_detail": "Council on Foreign Relations 2023: $83.2M expenses. Nonpartisan think tank with 5,000 members; publishes Foreign Affairs (180K+ subscribers); runs public programs, task forces, and the CFR.org resource reaching 1M+ users/year.",
    "extraction_note": "$83,166,400 / 1,000,000 people reached = $83.2/person. CFR membership includes former secretaries of state, CEOs, academics, and diplomats. Foreign Affairs is the most influential international affairs publication in the world.",
    "impact_description": "one person reached by Council on Foreign Relations' foreign policy research and publications — publisher of Foreign Affairs magazine, convener of senior foreign policy leaders, and source of expert analysis used by Congress, the White House, and global governments",
    "annual_expenses_usd": 83166400,
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
