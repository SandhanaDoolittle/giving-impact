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

# PPFA: existing entry has pp_name as a string; grants say "PLANNED PARENTHOOD" (no "Federation")
add_aliases(data, "Planned Parenthood Federation of America", [
    "Planned Parenthood",
    "Planned Parenthood Federation",
    "Ppfa",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Loyola Marymount University — Jesuit university in Los Angeles
  {
    "name": "Loyola Marymount University",
    "ein": "951643334",
    "pp_name": [
      "Loyola Marymount University",
      "Lmu",
      "Loyola Marymount Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one LMU student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Loyola Marymount University",
    "cost_per_outcome_usd": 35000,
    "impact_per_100_usd": 0.00286,
    "confidence": "medium",
    "source": "LMU Common Data Set 2023-24 + ProPublica",
    "source_detail": "Loyola Marymount University 2023: $600M total expenses. Private Jesuit university in Los Angeles with ~10,000 students. CDS 2023-24 avg institutional need-based grant ~$35,000.",
    "extraction_note": "CDS 2023-24 LMU avg institutional need-based grant used as cost_per_outcome. Jesuit tradition emphasizes service and education for underserved communities.",
    "impact_description": "one year of need-based financial aid for one Loyola Marymount University student (avg ~$35,000 institutional grant) — a top-ranked Jesuit liberal arts university in Los Angeles with nationally recognized film, business, and engineering programs",
    "annual_expenses_usd": 600006604,
    "revenue_year": 2023,
  },

  # Chicago Symphony Orchestra
  {
    "name": "Chicago Symphony Orchestra",
    "ein": "362167823",
    "pp_name": [
      "Chicago Symphony Orchestra",
      "Chicago Symphony Orchestra Association",
      "Cso",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one person experiencing the Chicago Symphony Orchestra",
    "primary_metric_value": 700000,
    "primary_metric_unit": "people experiencing Chicago Symphony Orchestra concerts and education programs at Symphony Center and Millennium Park",
    "cost_per_outcome_usd": 122,
    "impact_per_100_usd": 0.82,
    "confidence": "medium",
    "source": "Chicago Symphony Orchestra Annual Report + ProPublica",
    "source_detail": "Chicago Symphony Orchestra 2023: $85.6M expenses. One of the 'Big Five' American orchestras. ~200K paid concert attendees + 500K at free Millennium Park concerts + 65K+ education program participants.",
    "extraction_note": "$85,601,183 / 700,000 people = $122.3/person. CSO runs free Millennium Park concerts reaching 500K+, plus MusicNOW, Civic Orchestra for professional training, and in-school programs.",
    "impact_description": "one person experiencing the Chicago Symphony Orchestra — one of the world's great orchestras at Symphony Center on Michigan Avenue, also presenting 500K+ free concerts at Millennium Park each summer and running Chicago's largest orchestral education program",
    "annual_expenses_usd": 85601183,
    "revenue_year": 2023,
  },

  # Texas Christian University
  {
    "name": "Texas Christian University",
    "ein": "750827465",
    "pp_name": [
      "Texas Christian University",
      "Tcu",
      "Texas Christian Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one TCU student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Texas Christian University",
    "cost_per_outcome_usd": 38000,
    "impact_per_100_usd": 0.00263,
    "confidence": "medium",
    "source": "TCU Common Data Set 2023-24 + ProPublica",
    "source_detail": "Texas Christian University 2023: $961M expenses. Private Christian university in Fort Worth, TX with ~12,500 students. CDS 2023-24 avg institutional need-based grant ~$38,000.",
    "extraction_note": "CDS 2023-24 TCU avg institutional need-based grant used. TCU has grown into a major research university while maintaining its foundational Christian values and NCAA Division I athletics.",
    "impact_description": "one year of need-based financial aid for one Texas Christian University student (avg ~$38,000 institutional grant) — a private Christian research university in Fort Worth, TX with nationally ranked business, nursing, and fine arts programs",
    "annual_expenses_usd": 960941889,
    "revenue_year": 2023,
  },

  # ProPublica — independent investigative journalism nonprofit
  {
    "name": "ProPublica",
    "ein": "142007220",
    "pp_name": [
      "Pro Publica Inc",
      "Propublica",
      "Pro Publica",
      "Propublica Inc",
    ],
    "cause": "community",
    "primary_metric_label": "one ProPublica investigative story read",
    "primary_metric_value": 30000000,
    "primary_metric_unit": "reads of original investigative journalism by ProPublica — the largest U.S. nonprofit newsroom, winner of 8 Pulitzer Prizes",
    "cost_per_outcome_usd": 1.47,
    "impact_per_100_usd": 68,
    "confidence": "low",
    "source": "ProPublica Annual Report + ProPublica",
    "source_detail": "Pro Publica Inc 2023: $44.1M expenses. ~300 major investigative stories/year, ~20M unique monthly web visitors. 8 Pulitzer Prizes. Investigative work has prompted congressional hearings, firings, and legislation.",
    "extraction_note": "$44,080,009 / 30,000,000 estimated reads = $1.47/read. ProPublica's major investigations (IRS audit bias, abortion laws, jails, nursing homes) each reach millions; secondary reach via NYT, AP partnerships is far larger.",
    "impact_description": "one read of a ProPublica original investigation — the nation's largest nonprofit newsroom, with 8 Pulitzer Prizes, whose investigations have changed laws, fired officials, and revealed government failures in healthcare, justice, and taxation",
    "annual_expenses_usd": 44080009,
    "revenue_year": 2023,
  },

  # American Jewish Joint Distribution Committee (JDC)
  {
    "name": "American Jewish Joint Distribution Committee",
    "ein": "131656634",
    "pp_name": [
      "American Jewish Joint Distribution Committee Inc",
      "American Jewish Joint Distribution Committee",
      "Jdc",
      "The Joint",
      "Joint Distribution Committee",
    ],
    "cause": "community",
    "primary_metric_label": "one person served through JDC's global Jewish humanitarian programs",
    "primary_metric_value": 1400000,
    "primary_metric_unit": "people served through JDC's hunger relief, elder care, community development, and emergency response in 70+ countries",
    "cost_per_outcome_usd": 263,
    "impact_per_100_usd": 0.38,
    "confidence": "medium",
    "source": "JDC Annual Report + ProPublica",
    "source_detail": "American Jewish Joint Distribution Committee 2023: $368.4M expenses. Provides food security, elder care, community infrastructure, and emergency response to ~1.4M Jews in poverty and crisis in 70+ countries. Leads global Jewish emergency response.",
    "extraction_note": "$368,439,711 / 1,400,000 people served = $263.2/person. JDC operates in FSU countries supporting elderly Holocaust survivors, evacuating Jews from conflict zones, and sustaining Jewish communities in Africa, South America, and Asia.",
    "impact_description": "one person served through JDC's global Jewish humanitarian programs — providing food, elder care, community infrastructure, and emergency rescue to 1.4M Jews in poverty across 70+ countries, including Holocaust survivors, Ethiopian Jewish communities, and conflict-zone evacuations",
    "annual_expenses_usd": 368439711,
    "revenue_year": 2023,
  },

  # University of Florida Foundation
  {
    "name": "University of Florida Foundation",
    "ein": "590974739",
    "pp_name": [
      "University Of Florida Foundation Inc",
      "University Of Florida Foundation",
      "University Of Florida",
      "Uf Foundation",
      "Ufl Foundation",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one UF student",
    "primary_metric_unit": "student-year of need-based financial aid funded at University of Florida",
    "cost_per_outcome_usd": 11500,
    "impact_per_100_usd": 0.00870,
    "confidence": "medium",
    "source": "UF Common Data Set 2023-24 + ProPublica",
    "source_detail": "University of Florida Foundation 2023: $244M expenses. Private fundraising arm for University of Florida (Gainesville), Florida's flagship public research university with ~55,000 students. CDS 2023-24 avg institutional need-based grant ~$11,500.",
    "extraction_note": "CDS 2023-24 UF avg institutional need-based grant used. UF is a Top 5 public university by US News rankings, with nationally ranked engineering, pharmacy, law, and business schools.",
    "impact_description": "one year of need-based financial aid for one University of Florida student (avg ~$11,500 institutional grant) — Florida's flagship public research university, one of the top 5 public universities in the US, with 55,000 students in Gainesville",
    "annual_expenses_usd": 244045991,
    "revenue_year": 2023,
  },

  # American Enterprise Institute
  {
    "name": "American Enterprise Institute",
    "ein": "530218495",
    "pp_name": [
      "American Enterprise Institute For Public Policy Research",
      "American Enterprise Institute",
      "Aei",
    ],
    "cause": "community",
    "primary_metric_label": "one person reached through AEI policy research and public engagement",
    "primary_metric_value": 500000,
    "primary_metric_unit": "policymakers, journalists, academics, and citizens engaged through AEI's economic, defense, education, and governance research",
    "cost_per_outcome_usd": 134,
    "impact_per_100_usd": 0.748,
    "confidence": "low",
    "source": "AEI Annual Report + ProPublica",
    "source_detail": "American Enterprise Institute 2023: $66.8M expenses. Right-of-center think tank producing 600+ publications/year. Hosts 200+ events including congressional testimony and major policy conferences reaching 500K+ policy influencers.",
    "extraction_note": "$66,819,074 / 500,000 people reached = $133.6/person. AEI scholars advise on tax policy, defense, education reform, and economic regulation; their work shapes legislation and executive policy across administrations.",
    "impact_description": "one policymaker, journalist, or citizen engaged through AEI's free-market economic and social policy research — a major Washington think tank producing 600+ publications/year on economics, defense, education, and governance",
    "annual_expenses_usd": 66819074,
    "revenue_year": 2023,
  },

  # WGBH Educational Foundation (now GBH) — Boston PBS station producing national programming
  {
    "name": "WGBH Educational Foundation",
    "ein": "42104397",
    "pp_name": [
      "Wgbh Educational Foundation",
      "Wgbh",
      "Gbh Educational Foundation",
      "Gbh",
      "Wgbh Tv",
    ],
    "cause": "education",
    "primary_metric_label": "one viewer reached by WGBH-produced national PBS programming",
    "primary_metric_value": 300000000,
    "primary_metric_unit": "American viewers reached through WGBH/GBH-produced PBS programming including Frontline, NOVA, American Experience, and Masterpiece",
    "cost_per_outcome_usd": 0.75,
    "impact_per_100_usd": 133,
    "confidence": "low",
    "source": "GBH Annual Report + ProPublica",
    "source_detail": "WGBH Educational Foundation (now GBH) 2023: $225.6M expenses. America's largest producer of PBS content: Frontline (4M viewers/episode), NOVA (4M viewers), American Experience, Masterpiece, Antiques Roadshow. Reach of 300M+ across all platforms annually.",
    "extraction_note": "$225,572,032 / 300,000,000 viewers = $0.752/viewer. GBH produces 30%+ of PBS's national programming, making it far more impactful than a single local station. Reach includes TV, streaming, podcasts, and educational resources.",
    "impact_description": "one person reached by WGBH/GBH-produced PBS content — America's largest public media producer, responsible for Frontline, NOVA, American Experience, and Masterpiece, reaching 300M+ Americans/year through television, streaming, and digital platforms",
    "annual_expenses_usd": 225572032,
    "revenue_year": 2023,
  },

  # Frist Art Museum — Nashville's premier free-admission art museum
  {
    "name": "Frist Art Museum",
    "ein": "621731492",
    "pp_name": [
      "Frist Art Museum",
      "Frist Center For The Visual Arts",
      "Frist Center For Visual Arts",
      "Frist Museum",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one visitor to the Frist Art Museum",
    "primary_metric_value": 300000,
    "primary_metric_unit": "visitors to the Frist Art Museum in Nashville including free community admission days and education programs",
    "cost_per_outcome_usd": 44,
    "impact_per_100_usd": 2.25,
    "confidence": "medium",
    "source": "Frist Art Museum Annual Report + ProPublica",
    "source_detail": "Frist Art Museum 2023: $13.3M expenses. Nashville's premier art museum in a renovated 1934 Art Deco building (former post office). ~300K visitors/year; hosts major traveling exhibitions; free admission for children under 18 and Nashville Metro Schools.",
    "extraction_note": "$13,314,347 / 300,000 visitors = $44.4/visitor. Frist is privately-funded but serves as a civic cultural anchor; offers extensive education programs and community partnership gallery for Nashville area nonprofits.",
    "impact_description": "one visitor to the Frist Art Museum in Nashville — Tennessee's premier art museum showcasing major national and international traveling exhibitions in a stunning 1934 Art Deco building, with free admission for all children",
    "annual_expenses_usd": 13314347,
    "revenue_year": 2023,
  },

  # Start Early — early childhood education advocacy and direct services (formerly Ounce of Prevention Fund)
  {
    "name": "Start Early",
    "ein": "363186328",
    "pp_name": [
      "Start Early",
      "Ounce Of Prevention Fund",
      "Ounce Prevention Fund",
      "The Ounce Of Prevention Fund",
    ],
    "cause": "education",
    "primary_metric_label": "one child receiving high-quality early childhood education through Start Early",
    "primary_metric_value": 60000,
    "primary_metric_unit": "children (birth to age 5) receiving evidence-based early childhood education and family support through Start Early programs including Early Head Start and home visiting",
    "cost_per_outcome_usd": 1802,
    "impact_per_100_usd": 0.0555,
    "confidence": "medium",
    "source": "Start Early Annual Report + ProPublica",
    "source_detail": "Start Early (formerly Ounce of Prevention Fund) 2023: $108.1M expenses. Provides Early Head Start, home visiting, coaching, and policy advocacy for high-quality early childhood education. Serves ~60K children/year in IL and partners nationally.",
    "extraction_note": "$108,099,164 / 60,000 children = $1,802/child. Start Early serves children from birth to age 5 with evidence-based programs that narrow the achievement gap. Also advocates for policy change at state and federal level.",
    "impact_description": "one child (birth to age 5) receiving high-quality early childhood education through Start Early's Early Head Start, home visiting, and family support programs — serving 60K+ children in Illinois and nationally to close the achievement gap before kindergarten",
    "annual_expenses_usd": 108099164,
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
