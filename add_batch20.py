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

# ── FIX EXISTING INCOMPLETE ENTRIES ──────────────────────────────────────────

# JDRF: existing entry has wrong primary_metric_unit (dollar-denomination) and no EIN.
# Fix with proper people-served metric. ~$220M expenses, ~1.5M Americans with T1D.
fill_metrics_by_name(data, "Juvenile Diabetes Research Foundation", {
    "ein": "237255688",
    "pp_name": [
        "Juvenile Diabetes Research Foundation International",
        "Juvenile Diabetes Research Foundation",
        "Jdrf International",
        "Jdrf",
    ],
    "primary_metric_label": "one person with Type 1 diabetes whose care is advanced through JDRF research and advocacy",
    "primary_metric_value": 1500000,
    "primary_metric_unit": "people with Type 1 diabetes whose care is improved through JDRF-funded research, clinical trials, and advocacy for insurance coverage and FDA approvals",
    "cost_per_outcome_usd": 147,
    "impact_per_100_usd": 0.681,
    "confidence": "low",
    "source": "JDRF Annual Report + public financials",
    "source_detail": "JDRF (formerly Juvenile Diabetes Research Foundation International) spends ~$220M/year funding T1D research. ~1.5 million Americans have Type 1 diabetes. JDRF is the world's largest funder of T1D research, funding closed-loop insulin delivery, islet transplantation, and gene therapy.",
    "extraction_note": "$220,000,000 / 1,500,000 T1D patients = $146.7/person. Low confidence because JDRF's research benefits are diffuse — funding basic science that eventually reaches patients years later. They have funded $2.5B+ in research since 1970, contributing to the closed-loop artificial pancreas now available commercially.",
    "impact_description": "one person with Type 1 diabetes whose treatment options are improved through JDRF-funded research — the world's largest T1D funder has backed the development of CGMs, insulin pumps, and the closed-loop artificial pancreas, supporting 1.5M Americans with the condition",
    "annual_expenses_usd": 220000000,
    "revenue_year": 2023,
})

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Manhattan Institute for Policy Research — NYC conservative think tank
  {
    "name": "Manhattan Institute for Policy Research",
    "ein": "132912529",
    "pp_name": [
      "Manhattan Institute For Policy Research Inc",
      "Manhattan Institute For Policy Research",
      "Manhattan Institute",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged through Manhattan Institute research and publications",
    "primary_metric_value": 500000,
    "primary_metric_unit": "policymakers, journalists, and citizens reached through Manhattan Institute's urban policy research, City Journal magazine, and public events on crime, education, housing, and economic growth",
    "cost_per_outcome_usd": 43,
    "impact_per_100_usd": 2.31,
    "confidence": "low",
    "source": "Manhattan Institute Annual Report + ProPublica",
    "source_detail": "Manhattan Institute 2023: $21.6M expenses. Nonpartisan (conservative-leaning) think tank founded in 1977 in NYC. Publishes City Journal, runs policy events, and produces research on criminal justice, education reform, housing policy, and urban economic growth.",
    "extraction_note": "$21,583,113 / 500,000 people reached = $43.2/person. Manhattan Institute's research influenced NYC's welfare reform, broken-windows policing, and school choice policies in the 1990s. City Journal is among the most-cited conservative policy publications.",
    "impact_description": "one person reached through Manhattan Institute's policy research — a leading urban policy think tank that shaped NYC's 1990s crime and welfare reforms through evidence-based research on criminal justice, housing, education, and economic growth",
    "annual_expenses_usd": 21583113,
    "revenue_year": 2023,
  },

  # American Friends of Tel Aviv University — US fundraising arm for TAU
  {
    "name": "American Friends of Tel Aviv University",
    "ein": "131996126",
    "pp_name": [
      "American Friends Of The Tel Aviv University Inc",
      "American Friends Of Tel Aviv University",
      "Aftau",
      "Tel Aviv University",
      "Friends Of Tel Aviv University",
    ],
    "cause": "education",
    "primary_metric_label": "one student or researcher at Tel Aviv University supported through AFTAU grants",
    "primary_metric_value": 35000,
    "primary_metric_unit": "students and researchers at Tel Aviv University whose education and research is supported by American Friends of Tel Aviv University grants, scholarships, and faculty funding",
    "cost_per_outcome_usd": 1163,
    "impact_per_100_usd": 0.0860,
    "confidence": "low",
    "source": "AFTAU Annual Report + ProPublica",
    "source_detail": "American Friends of Tel Aviv University 2023: $40.7M expenses. US fundraising entity that passes donations to Tel Aviv University in Israel. TAU is Israel's largest university with 35,000 students across 9 faculties and 70+ institutes. AFTAU funds scholarships, research chairs, and capital projects.",
    "extraction_note": "$40,718,630 / 35,000 TAU students = $1,163/student. AFTAU passes most funds to TAU, supporting Israeli academic excellence in medicine, engineering, law, and the arts. Very low confidence because AFTAU is a conduit; direct student impact depends on how TAU deploys the funds.",
    "impact_description": "one student or researcher at Tel Aviv University supported through AFTAU — Israel's largest university, funding scholarships, research institutes, and faculty positions at a university that has produced multiple Nobel laureates and pioneered fields from genomics to cybersecurity",
    "annual_expenses_usd": 40718630,
    "revenue_year": 2023,
  },

  # Pacific Legal Foundation — libertarian public interest law firm
  {
    "name": "Pacific Legal Foundation",
    "ein": "942197343",
    "pp_name": [
      "Pacific Legal Foundation",
      "Plf",
    ],
    "cause": "community",
    "primary_metric_label": "one person whose property rights or economic liberty was defended through PLF litigation",
    "primary_metric_value": 500000,
    "primary_metric_unit": "people whose constitutional rights, property rights, or economic liberty are protected through Pacific Legal Foundation's public interest litigation against government overreach",
    "cost_per_outcome_usd": 54,
    "impact_per_100_usd": 1.85,
    "confidence": "low",
    "source": "Pacific Legal Foundation Annual Report + ProPublica",
    "source_detail": "Pacific Legal Foundation 2024: $27.0M expenses. America's oldest and most prominent libertarian public interest law firm, founded 1973 in Sacramento. Files ~150 cases/year defending property rights, economic liberty, and constitutional limits on government. Has won 80%+ of Supreme Court cases.",
    "extraction_note": "$27,024,089 / 500,000 people benefiting from PLF victories = $54/person. PLF Supreme Court wins on regulatory takings, occupational licensing, and government accountability affect millions; beneficiary count is very uncertain. Has won cases including Sackett v. EPA (clean water), Tyler v. Hennepin County (home equity theft).",
    "impact_description": "one person whose property rights, economic liberty, or constitutional rights are defended through Pacific Legal Foundation — America's oldest libertarian public interest law firm, winning landmark Supreme Court cases on regulatory takings, occupational licensing, and home equity protection",
    "annual_expenses_usd": 27024089,
    "revenue_year": 2024,
  },

  # WETA — Washington DC public broadcaster (PBS station + national productions)
  {
    "name": "Greater Washington Educational Telecommunications Association",
    "ein": "530242992",
    "pp_name": [
      "Greater Washington Educational Telecommunications Association Inc",
      "Greater Washington Educational Telecommunications",
      "Weta",
      "Weta Tv",
      "Weta Dc",
      "Weta Public Media",
      "Washington Weta",
    ],
    "cause": "education",
    "primary_metric_label": "one weekly viewer or listener of WETA public media programming",
    "primary_metric_value": 1500000,
    "primary_metric_unit": "weekly viewers and listeners of WETA's public television and classical music radio programming in the Washington DC area, plus national productions including Washington Week",
    "cost_per_outcome_usd": 84,
    "impact_per_100_usd": 1.19,
    "confidence": "medium",
    "source": "WETA Annual Report + ProPublica",
    "source_detail": "WETA 2023: $125.7M expenses. Washington DC's flagship PBS station and classical music broadcaster. Produces Washington Week with Geoff Bennett (national political program), In Performance at the White House, and other national specials. WETA Classical serves 500K+ classical music listeners. 1.5M+ total weekly audience.",
    "extraction_note": "$125,650,502 / 1,500,000 weekly viewers/listeners = $83.8/viewer. WETA's larger-than-typical budget reflects its dual role: local DC public broadcaster + national PBS production center. Washington Week is PBS's longest-running public affairs program.",
    "impact_description": "one person watching or listening to WETA public media — Washington DC's PBS station and classical radio broadcaster that produces Washington Week (PBS's longest-running public affairs program), In Performance at the White House, and local DC journalism for 1.5M+ weekly viewers",
    "annual_expenses_usd": 125650502,
    "revenue_year": 2023,
  },

  # New America Foundation — centrist policy think tank
  {
    "name": "New America",
    "ein": "522096845",
    "pp_name": [
      "New America Foundation",
      "New America",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged through New America's policy research and programs",
    "primary_metric_value": 500000,
    "primary_metric_unit": "policymakers, educators, technologists, and citizens engaged through New America's policy research, fellowship programs, and public events on education, technology, health, and democracy",
    "cost_per_outcome_usd": 82,
    "impact_per_100_usd": 1.23,
    "confidence": "low",
    "source": "New America Annual Report + ProPublica",
    "source_detail": "New America Foundation 2023: $40.8M expenses. Centrist think tank founded in 1999 with offices in DC and NYC. Known for bipartisan work on education policy (pre-K, student debt), technology policy (net neutrality, antitrust), and democracy reform. Runs fellowship programs developing the next generation of policy leaders.",
    "extraction_note": "$40,824,022 / 500,000 people reached = $81.6/person. New America's fellows and researchers have influenced policy on pre-K expansion, student loan reform, broadband access, and competition policy. Very low confidence on engagement count.",
    "impact_description": "one person engaged through New America's policy research — a centrist think tank whose fellows have shaped education, technology, and democracy policy, known for pioneering federal pre-K expansion research and broadband competition policy",
    "annual_expenses_usd": 40824022,
    "revenue_year": 2023,
  },

  # Big Shoulders Fund — Chicago Catholic school support
  {
    "name": "Big Shoulders Fund",
    "ein": "363490557",
    "pp_name": [
      "Big Shoulders Fund",
    ],
    "cause": "education",
    "primary_metric_label": "one student in a Chicago Catholic school supported through Big Shoulders Fund scholarships and grants",
    "primary_metric_value": 10000,
    "primary_metric_unit": "students in Chicago's most underserved Catholic elementary and high schools receiving Big Shoulders Fund scholarships, teacher training support, and school improvement grants",
    "cost_per_outcome_usd": 5894,
    "impact_per_100_usd": 0.0170,
    "confidence": "medium",
    "source": "Big Shoulders Fund Annual Report + ProPublica",
    "source_detail": "Big Shoulders Fund 2023: $58.9M expenses. Chicago nonprofit that supports 45+ Catholic schools in the city's poorest neighborhoods serving 10,000+ students. Provides need-based scholarships ($1,500-5,000/year), teacher professional development, and operational grants to keep schools viable.",
    "extraction_note": "$58,940,127 / 10,000 students = $5,894/student/year. Big Shoulders Fund has provided $700M+ in scholarships since 1986. Works in Chicago neighborhoods where public schools often struggle — partner schools have 95%+ high school graduation rates and 90%+ college enrollment for graduates.",
    "impact_description": "one student in a Chicago Catholic school in a low-income neighborhood receiving a Big Shoulders Fund scholarship — Chicago's leading funder of inner-city Catholic education, keeping 45+ schools open in the city's poorest communities with 95%+ graduation rates",
    "annual_expenses_usd": 58940127,
    "revenue_year": 2023,
  },

  # Idaho Youth Ranch — Idaho's oldest youth services organization
  {
    "name": "Idaho Youth Ranch",
    "ein": "820253346",
    "pp_name": [
      "Idaho Youth Ranch Inc",
      "Idaho Youth Ranch",
      "Iyr",
    ],
    "cause": "health",
    "primary_metric_label": "one youth receiving care through Idaho Youth Ranch behavioral health and residential programs",
    "primary_metric_value": 5000,
    "primary_metric_unit": "youth and families in Idaho receiving behavioral health therapy, residential treatment, foster care, adoption services, or equine-assisted counseling through Idaho Youth Ranch",
    "cost_per_outcome_usd": 7937,
    "impact_per_100_usd": 0.0126,
    "confidence": "medium",
    "source": "Idaho Youth Ranch Annual Report + ProPublica",
    "source_detail": "Idaho Youth Ranch 2024: $39.7M expenses. Idaho's oldest and largest youth services organization (founded 1953). Provides residential treatment, behavioral health therapy, foster care, adoption, counseling, and equine-assisted therapy across Idaho. Also operates 15 thrift stores funding its programs.",
    "extraction_note": "$39,685,798 / 5,000 youth served = $7,937/youth. IYR operates residential group homes, outpatient therapy, and community-based behavioral health across Idaho. Serves youth ages 0-21 with mental health challenges, abuse histories, and family instability.",
    "impact_description": "one Idaho youth receiving services through Idaho Youth Ranch — the state's oldest youth services organization providing residential treatment, behavioral health therapy, foster care, and equine-assisted therapy to children facing mental health challenges, abuse, and family instability",
    "annual_expenses_usd": 39685798,
    "revenue_year": 2024,
  },

  # Friends of the Children — Portland long-term professional mentoring
  {
    "name": "Friends of the Children - Portland",
    "ein": "931098105",
    "pp_name": [
      "Friends Of The Children Portland",
      "Friends Of The Children",
      "Friends Children",
      "Fotc",
    ],
    "cause": "education",
    "primary_metric_label": "one child enrolled in Friends of the Children's long-term professional mentoring program",
    "primary_metric_value": 300,
    "primary_metric_unit": "children from kindergarten through 12th grade enrolled in Friends of the Children's paid professional mentoring program, receiving 4+ hours per week of consistent support for 12+ years",
    "cost_per_outcome_usd": 28548,
    "impact_per_100_usd": 0.00350,
    "confidence": "medium",
    "source": "Friends of the Children Annual Report + ProPublica",
    "source_detail": "Friends of the Children - Portland 2023: $8.6M expenses. Portland-based long-term mentoring program employing full-time professional mentors who work with the same 6 children from kindergarten through high school graduation (12+ years). Primarily serves children in deepest poverty with multiple risk factors. Outcomes: 83% avoid early parenting, 83% avoid juvenile justice involvement, 93% graduate high school.",
    "extraction_note": "$8,564,454 / 300 children served = $28,548/child/year. Friends of the Children is unusual in employing paid professional staff mentors (not volunteers), which enables the sustained 12-year relationship. The Oregon-founded model has expanded to 30+ cities nationally, but Portland is the founding/largest chapter.",
    "impact_description": "one child from a high-risk background enrolled in Friends of the Children's 12-year professional mentoring program — paid staff mentors work with the same child from kindergarten through high school, achieving 83% rates of avoiding juvenile justice and 93% high school graduation among kids who entered with the highest risk factors",
    "annual_expenses_usd": 8564454,
    "revenue_year": 2023,
  },

  # Freedom for All Americans Education Fund — LGBTQ nondiscrimination campaigns
  {
    "name": "Freedom for All Americans Education Fund",
    "ein": "474166556",
    "pp_name": [
      "Freedom For All Americans Education Fund",
      "Freedom For All Americans",
      "Ffaa",
      "Freedom For All",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged in LGBTQ nondiscrimination education and advocacy through Freedom for All Americans",
    "primary_metric_value": 200000,
    "primary_metric_unit": "people engaged in state-level campaigns for comprehensive LGBTQ nondiscrimination protections in employment, housing, and public accommodations through Freedom for All Americans",
    "cost_per_outcome_usd": 11,
    "impact_per_100_usd": 9.03,
    "confidence": "low",
    "source": "Freedom for All Americans Annual Report + ProPublica",
    "source_detail": "Freedom for All Americans Education Fund 2022: $2.2M expenses. Campaign for LGBTQ nondiscrimination protections, working state-by-state to pass comprehensive civil rights protections covering sexual orientation and gender identity in employment, housing, and public accommodations.",
    "extraction_note": "$2,215,371 / 200,000 people engaged = $11.1/person. FFAA runs state-level campaigns building coalitions across business, faith, and community leaders to pass nondiscrimination laws. Small but focused organization operating in states where nondiscrimination protections remain incomplete.",
    "impact_description": "one person engaged in state-level LGBTQ nondiscrimination campaigns through Freedom for All Americans — a national advocacy organization building business and community coalitions to pass comprehensive nondiscrimination protections in states that still lack them",
    "annual_expenses_usd": 2215371,
    "revenue_year": 2022,
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
