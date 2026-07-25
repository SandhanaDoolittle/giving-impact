import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

print(f"Starting entries: {len(data)}")

# ── ALIAS / EIN FIXES ON EXISTING ENTRIES ─────────────────────────────────────

for e in data:
    if e["name"] == "CARE USA":
        e["pp_name"] = ["Cooperative For Assistance And Relief Everywhere", "CARE", "CARE Inc"]
        e["annual_expenses_usd"] = 929368410
        e["revenue_year"] = 2024

    elif e["name"] == "Alzheimer's Association":
        e["ein"] = "133039601"
        pp = e.get("pp_name", [])
        if isinstance(pp, str):
            pp = [pp]
        aliases = ["Alzheimers Disease And Related Disorders Association",
                   "Alzheimer's Disease and Related Disorders Association"]
        for a in aliases:
            if a not in pp:
                pp.append(a)
        e["pp_name"] = pp
        e["annual_expenses_usd"] = 460183069
        e["annual_revenue_usd"] = 460000000
        e["revenue_year"] = 2023

    elif e["name"] == "YMCA of the USA":
        e["pp_name"] = [
            "National Council of YMCA of the USA",
            "National Council Of Ymcas Of The United States Of America",
            "Ymca Of The Usa",
            "Y Usa"
        ]

    elif e["name"] == "Partners in Health":
        e["ein"] = "43567502"
        e["annual_expenses_usd"] = 232194059
        e["annual_revenue_usd"] = 250000000
        e["revenue_year"] = 2023

    elif e["name"] == "Conservation International":
        # Make sure "Conservation International" (no Foundation) also maps
        pp = e.get("pp_name", [])
        if isinstance(pp, str):
            pp = [pp]
        if "Conservation International" not in pp:
            pp.append("Conservation International")
        e["pp_name"] = pp

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────

new_entries = [

  # ── ARTS & CULTURE ──────────────────────────────────────────────────────────

  {
    "name": "American Museum of Natural History",
    "ein": "136162659",
    "pp_name": "American Museum Of Natural History",
    "cause": "arts_culture",
    "primary_metric_label": "one museum visitor",
    "primary_metric_value": 3000000,
    "primary_metric_unit": "museum visitors",
    "cost_per_outcome_usd": 76,
    "impact_per_100_usd": 1.32,
    "confidence": "medium",
    "source": "AMNH Annual Report + ProPublica",
    "source_detail": "AMNH 2023: ~3M visitors; 990 expenses $227.6M",
    "extraction_note": "$227.6M / 3M visitors = $76/visitor",
    "impact_description": "one visitor experiencing AMNH exhibits, education, and scientific collections",
    "annual_expenses_usd": 227654071,
    "revenue_year": 2023
  },

  {
    "name": "Metropolitan Opera",
    "ein": "131624087",
    "pp_name": ["Metropolitan Opera Association Inc", "Metropolitan Opera Association"],
    "cause": "arts_culture",
    "primary_metric_label": "one audience member (live or Live in HD)",
    "primary_metric_value": 750000,
    "primary_metric_unit": "performance audience members (live and HD broadcast)",
    "cost_per_outcome_usd": 443,
    "impact_per_100_usd": 0.226,
    "confidence": "medium",
    "source": "Met Opera Annual Report + ProPublica",
    "source_detail": "2023: ~250K live + ~500K Live in HD; $332M expenses",
    "extraction_note": "$332M / 750K combined audience = $443/person",
    "impact_description": "one person experiencing a Metropolitan Opera performance — live at Lincoln Center or via Live in HD cinema broadcast",
    "annual_expenses_usd": 332251527,
    "revenue_year": 2023
  },

  {
    "name": "Frick Collection",
    "ein": "131624012",
    "pp_name": ["The Frick Collection", "Frick Collection"],
    "cause": "arts_culture",
    "primary_metric_label": "one museum visitor",
    "primary_metric_value": 200000,
    "primary_metric_unit": "art museum visitors",
    "cost_per_outcome_usd": 146,
    "impact_per_100_usd": 0.685,
    "confidence": "medium",
    "source": "Frick Collection Annual Report + ProPublica",
    "source_detail": "Frick 2023: $29.2M expenses; ~200K visitors/year (reopened renovated space 2024)",
    "extraction_note": "$29.2M / 200K = $146/visitor",
    "impact_description": "one visitor experiencing the Frick Collection's masterworks of European painting and decorative arts",
    "annual_expenses_usd": 29233056,
    "revenue_year": 2023
  },

  {
    "name": "Philadelphia Museum of Art",
    "ein": "231365388",
    "pp_name": "Philadelphia Museum Of Art",
    "cause": "arts_culture",
    "primary_metric_label": "one museum visitor",
    "primary_metric_value": 650000,
    "primary_metric_unit": "art museum visitors",
    "cost_per_outcome_usd": 120,
    "impact_per_100_usd": 0.833,
    "confidence": "medium",
    "source": "PMA Annual Report + ProPublica",
    "source_detail": "PMA 2023: $77.9M expenses; ~650K visitors annually",
    "extraction_note": "$77.9M / 650K = $120/visitor",
    "impact_description": "one person visiting one of the largest art museums in the US, home to 240,000+ objects",
    "annual_expenses_usd": 77863110,
    "revenue_year": 2023
  },

  {
    "name": "YoungArts",
    "ein": "592141837",
    "pp_name": ["National Foundation For Advancement In The Arts Inc",
                "National Foundation For Advancement In The Arts",
                "Young Arts Foundation"],
    "cause": "arts_culture",
    "primary_metric_label": "one young artist awarded recognition",
    "primary_metric_value": 700,
    "primary_metric_unit": "young artists receiving YoungArts national recognition and support",
    "cost_per_outcome_usd": 14490,
    "impact_per_100_usd": 0.0069,
    "confidence": "medium",
    "source": "YoungArts Annual Report + ProPublica",
    "source_detail": "NFAA 2023: $10.1M expenses; ~700 YoungArts national award winners selected from ~12K applicants",
    "extraction_note": "$10.1M / 700 award winners = $14,490/winner. Also serves ~12K semifinalists.",
    "impact_description": "one young artist receiving YoungArts national recognition, college scholarship opportunities, and professional development",
    "annual_expenses_usd": 10143410,
    "revenue_year": 2023
  },

  # ── INTERNATIONAL AID ────────────────────────────────────────────────────────

  {
    "name": "One Acre Fund",
    "ein": "203668110",
    "pp_name": ["One Acre Fund", "One Acre Fund Us"],
    "cause": "international_aid",
    "primary_metric_label": "one farm family with improved yields",
    "primary_metric_value": 1800000,
    "primary_metric_unit": "smallholder farm families served with seeds, training, and financing",
    "cost_per_outcome_usd": 126,
    "impact_per_100_usd": 0.794,
    "confidence": "high",
    "source": "One Acre Fund Annual Report 2022 + ProPublica",
    "source_detail": "1.8M farm families served; $227M expenses; avg 40% crop yield increase per family",
    "extraction_note": "$227M / 1.8M families = $126/family. Families gain ~$143 additional income on average.",
    "impact_description": "one smallholder farm family in East/Southern Africa receiving seeds, fertilizer training, and microfinancing to increase crop yields by ~40%",
    "annual_expenses_usd": 227055100,
    "revenue_year": 2023
  },

  {
    "name": "AMREF Health Africa",
    "ein": "131867411",
    "pp_name": ["Amref Health Africa Inc", "African Medical And Research Foundation",
                "Amref Health Africa"],
    "cause": "international_aid",
    "primary_metric_label": "one patient contact in East Africa",
    "primary_metric_value": 300000,
    "primary_metric_unit": "patient contacts in underserved East African communities",
    "cost_per_outcome_usd": 38,
    "impact_per_100_usd": 2.63,
    "confidence": "medium",
    "source": "AMREF Annual Report + ProPublica",
    "source_detail": "AMREF Health Africa Inc (US entity) $11.4M; funds healthcare programs in Kenya, Tanzania, Uganda, Ethiopia",
    "extraction_note": "US entity funds ~$11.4M; estimated patient contacts funded 300K; $38/contact",
    "impact_description": "one patient contact in underserved communities in East Africa through AMREF-funded health programs",
    "annual_expenses_usd": 11442364,
    "revenue_year": 2023
  },

  {
    "name": "Teach For All",
    "ein": "262122566",
    "pp_name": "Teach For All Inc",
    "cause": "international_aid",
    "primary_metric_label": "one student reached by a TFA corps member",
    "primary_metric_value": 500000,
    "primary_metric_unit": "students taught by Teach For All corps members in underserved communities",
    "cost_per_outcome_usd": 85,
    "impact_per_100_usd": 1.17,
    "confidence": "medium",
    "source": "Teach For All Annual Report + ProPublica",
    "source_detail": "Teach For All 2023: $42.7M expenses; supports corps in 60 countries reaching ~500K students",
    "extraction_note": "$42.7M / 500K students = $85/student. Each corps member teaches ~30 students.",
    "impact_description": "one student in an underserved community taught by a Teach For All network corps member",
    "annual_expenses_usd": 42711002,
    "revenue_year": 2023
  },

  # ── ENVIRONMENT ──────────────────────────────────────────────────────────────

  {
    "name": "The Conservation Fund",
    "ein": "521388917",
    "pp_name": ["The Conservation Fund A Nonprofit Corporation",
                "Conservation Fund",
                "The Conservation Fund"],
    "cause": "environment",
    "primary_metric_label": "one acre of land protected",
    "primary_metric_value": 500000,
    "primary_metric_unit": "acres of forests, wetlands, and working lands protected",
    "cost_per_outcome_usd": 619,
    "impact_per_100_usd": 0.162,
    "confidence": "medium",
    "source": "The Conservation Fund Annual Report + ProPublica",
    "source_detail": "Conservation Fund 2023: $309M expenses; ~500K+ acres protected/year through leveraged transactions",
    "extraction_note": "$309M / 500K acres = $618/acre. Leverages federal and state funding — effective per-acre cost is lower.",
    "impact_description": "one acre of forests, wetlands, or working lands permanently protected from development",
    "annual_expenses_usd": 309335935,
    "revenue_year": 2023
  },

  {
    "name": "Nia Tero Foundation",
    "ein": "821949563",
    "pp_name": "Nia Tero Foundation",
    "cause": "environment",
    "primary_metric_label": "one Indigenous person supported in land stewardship",
    "primary_metric_value": 300000,
    "primary_metric_unit": "Indigenous people supported in stewarding ancestral lands and waters",
    "cost_per_outcome_usd": 144,
    "impact_per_100_usd": 0.694,
    "confidence": "medium",
    "source": "Nia Tero Annual Report + ProPublica",
    "source_detail": "Nia Tero 2023: $43M expenses; partners with 200+ Indigenous-led orgs protecting ~550M acres",
    "extraction_note": "~300K Indigenous people directly supported. $43M / 300K = $143/person.",
    "impact_description": "one Indigenous person supported in stewarding ancestral lands and waters, protecting biodiversity and cultural heritage",
    "annual_expenses_usd": 43070792,
    "revenue_year": 2023
  },

  {
    "name": "The Trustees of Reservations",
    "ein": "42105780",
    "pp_name": ["Trustees Of Reservations", "The Trustees",
                "Trustees Of Reservations Inc"],
    "cause": "environment",
    "primary_metric_label": "one visitor to protected Massachusetts landscapes",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "visitors to protected Massachusetts open spaces and historic properties",
    "cost_per_outcome_usd": 55,
    "impact_per_100_usd": 1.81,
    "confidence": "medium",
    "source": "The Trustees Annual Report + ProPublica",
    "source_detail": "Trustees 2023: $55.3M expenses; manages 27,000+ acres at 120+ properties; ~1M visitors/year",
    "extraction_note": "America's oldest land trust (est. 1891). $55.3M / 1M visitors = $55/visitor.",
    "impact_description": "one person visiting or experiencing one of 120+ protected landscapes and historic properties across Massachusetts",
    "annual_expenses_usd": 55281050,
    "revenue_year": 2023
  },

  {
    "name": "Maine Coast Heritage Trust",
    "ein": "237099105",
    "pp_name": "Maine Coast Heritage Trust",
    "cause": "environment",
    "primary_metric_label": "one acre of Maine coast permanently protected",
    "primary_metric_value": 2000,
    "primary_metric_unit": "acres of Maine coastline and islands permanently protected",
    "cost_per_outcome_usd": 10361,
    "impact_per_100_usd": 0.00965,
    "confidence": "medium",
    "source": "Maine Coast Heritage Trust Annual Report + ProPublica",
    "source_detail": "MCHT 2023: $20.7M expenses; 185,000+ total acres protected; ~2,000 new acres/year",
    "extraction_note": "$20.7M / 2K new acres/year = $10,350/acre. Major coastal conservation transactions.",
    "impact_description": "one acre of Maine's iconic coastal lands, islands, or working waterfronts permanently protected from development",
    "annual_expenses_usd": 20722142,
    "revenue_year": 2023
  },

  # ── HEALTH ───────────────────────────────────────────────────────────────────

  {
    "name": "La Jolla Institute for Immunology",
    "ein": "330328688",
    "pp_name": ["La Jolla Institute For Immunology",
                "La Jolla Institute For Allergy And Immunology",
                "Lji"],
    "cause": "health",
    "primary_metric_label": "one peer-reviewed publication advancing immune disease research",
    "primary_metric_value": 200,
    "primary_metric_unit": "peer-reviewed research publications advancing immune disease treatment",
    "cost_per_outcome_usd": 418457,
    "impact_per_100_usd": 0.000239,
    "confidence": "medium",
    "source": "LJI Annual Report + ProPublica",
    "source_detail": "LJI 2023: $83.7M expenses; ~200 peer-reviewed publications/year in immunology",
    "extraction_note": "$83.7M / 200 publications = $418K/publication. Leading independent immunology research institute.",
    "impact_description": "one peer-reviewed publication advancing understanding of HIV, autoimmune diseases, allergies, or cancer immunology",
    "annual_expenses_usd": 83691328,
    "revenue_year": 2023
  },

  {
    "name": "Hoag Hospital Foundation",
    "ein": "953222343",
    "pp_name": "Hoag Hospital Foundation",
    "cause": "health",
    "primary_metric_label": "one patient served through foundation-funded programs",
    "primary_metric_value": 350000,
    "primary_metric_unit": "patients benefiting from Hoag Hospital Foundation-funded programs",
    "cost_per_outcome_usd": 144,
    "impact_per_100_usd": 0.694,
    "confidence": "low",
    "source": "Hoag Hospital Foundation Annual Report + ProPublica",
    "source_detail": "Foundation 2023: $50.2M expenses; Hoag Memorial Hospital serves ~350K patients/year",
    "extraction_note": "$50.2M / 350K patients = $143/patient. Foundation funds cancer care, heart programs, community health.",
    "impact_description": "one patient benefiting from Hoag Hospital Foundation programs in oncology, cardiology, or community health at Newport Beach's Hoag system",
    "annual_expenses_usd": 50247050,
    "revenue_year": 2023
  },

  {
    "name": "Loma Linda University Health",
    "ein": "953804495",
    "pp_name": "Loma Linda University Health",
    "cause": "health",
    "primary_metric_label": "one patient served at Loma Linda health system",
    "primary_metric_value": 400000,
    "primary_metric_unit": "patients served at Loma Linda University Medical Center",
    "cost_per_outcome_usd": 100,
    "impact_per_100_usd": 1.0,
    "confidence": "low",
    "source": "Loma Linda University Health Annual Report + ProPublica",
    "source_detail": "LLUH system serves ~400K patients/year; ProPublica entity ($40M) is the holding company for a $4B+ health system",
    "extraction_note": "990 entity is holding company — system-level patient metric used. Confidence low.",
    "impact_description": "one patient served at Loma Linda University Medical Center, an academic Seventh-day Adventist health system in Southern California",
    "annual_expenses_usd": 40006208,
    "revenue_year": 2023
  },

  {
    "name": "Public Health Institute",
    "ein": "941646278",
    "pp_name": "Public Health Institute",
    "cause": "health",
    "primary_metric_label": "one person reached through public health programs",
    "primary_metric_value": 7500000,
    "primary_metric_unit": "people reached through public health, HIV/AIDS, nutrition, and health equity programs",
    "cost_per_outcome_usd": 38,
    "impact_per_100_usd": 2.65,
    "confidence": "medium",
    "source": "PHI Annual Report + ProPublica",
    "source_detail": "PHI 2023: $283.5M expenses across 200+ programs in HIV/AIDS, maternal health, food security, health equity",
    "extraction_note": "Estimated 7.5M people served across all programs globally. $283M / 7.5M = $38/person.",
    "impact_description": "one person reached through PHI programs including HIV/AIDS prevention, maternal health, nutrition support, or health equity research",
    "annual_expenses_usd": 283476651,
    "revenue_year": 2023
  },

  {
    "name": "Lucile Packard Foundation for Children's Health",
    "ein": "770440090",
    "pp_name": ["Lucile Packard Foundation For Childrens Health",
                "Lucile Packard Foundation"],
    "cause": "health",
    "primary_metric_label": "one child served through funded programs",
    "primary_metric_value": 200000,
    "primary_metric_unit": "children served through Lucile Packard Children's Hospital and funded programs",
    "cost_per_outcome_usd": 1038,
    "impact_per_100_usd": 0.096,
    "confidence": "low",
    "source": "LPFCH Annual Report + ProPublica",
    "source_detail": "LPFCH 2023: $207.7M expenses; funds LPCH operations, child health policy, and community health programs serving ~200K children",
    "extraction_note": "$207.7M / 200K children = $1,038/child. Foundation funds hospital programs and child health advocacy.",
    "impact_description": "one child receiving care or benefits through Lucile Packard Children's Hospital programs and LPFCH-funded pediatric health advocacy",
    "annual_expenses_usd": 207676582,
    "revenue_year": 2023
  },

  # ── EDUCATION ────────────────────────────────────────────────────────────────

  {
    "name": "Davidson College",
    "ein": "560529961",
    "pp_name": "Davidson College",
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 55000,
    "impact_per_100_usd": 0.00182,
    "confidence": "medium",
    "source": "Davidson College Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant to need-based recipients ~$55K. No-loan guarantee for all. Expenses $193M.",
    "extraction_note": "Davidson has a no-loan policy. $55K average need-based grant from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Davidson College student (avg ~$55,000 institutional grant, no-loan guarantee)",
    "annual_expenses_usd": 193121536,
    "revenue_year": 2023
  },

  {
    "name": "Baylor University",
    "ein": "741159753",
    "pp_name": ["Baylor University", "Baylor Univ"],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 19500,
    "impact_per_100_usd": 0.00513,
    "confidence": "medium",
    "source": "Baylor University Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$19,500. Expenses $1.29B. ~22K students.",
    "extraction_note": "Baylor need-based grant average from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Baylor University student (avg ~$19,500 institutional grant)",
    "annual_expenses_usd": 1287015356,
    "revenue_year": 2023
  },

  {
    "name": "Pepperdine University",
    "ein": "951644037",
    "pp_name": "Pepperdine University",
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 33000,
    "impact_per_100_usd": 0.00303,
    "confidence": "medium",
    "source": "Pepperdine University Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$33K. Expenses $649M.",
    "extraction_note": "Pepperdine need-based grant average from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Pepperdine University student (avg ~$33,000 institutional grant)",
    "annual_expenses_usd": 649440096,
    "revenue_year": 2023
  },

  {
    "name": "Skidmore College",
    "ein": "141338562",
    "pp_name": "Skidmore College",
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 44000,
    "impact_per_100_usd": 0.00227,
    "confidence": "medium",
    "source": "Skidmore College Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$44K. Expenses $247M.",
    "extraction_note": "Skidmore need-based grant average from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Skidmore College student (avg ~$44,000 institutional grant)",
    "annual_expenses_usd": 246552284,
    "revenue_year": 2023
  },

  {
    "name": "Babson College",
    "ein": "42103544",
    "pp_name": "Babson College",
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 39000,
    "impact_per_100_usd": 0.00256,
    "confidence": "medium",
    "source": "Babson College Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$39K. Expenses $305M.",
    "extraction_note": "Babson need-based grant average from CDS section G.",
    "impact_description": "one year of need-based financial aid for one Babson College student (avg ~$39,000 institutional grant)",
    "annual_expenses_usd": 305464086,
    "revenue_year": 2023
  },

  {
    "name": "Ohio University",
    "ein": "316402269",
    "pp_name": ["Ohio University Foundation", "Ohio Univ", "Ohio University"],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 8500,
    "impact_per_100_usd": 0.01176,
    "confidence": "medium",
    "source": "Ohio University Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$8,500. Foundation expenses $51M. ~24K students.",
    "extraction_note": "Ohio University Foundation funds scholarships for a public university.",
    "impact_description": "one year of need-based financial aid for one Ohio University student (avg ~$8,500 institutional grant)",
    "annual_expenses_usd": 51237015,
    "revenue_year": 2023
  },

  {
    "name": "University of Iowa",
    "ein": "420796760",
    "pp_name": ["State University Of Iowa Foundation",
                "University Of Iowa Foundation",
                "University Of Iowa"],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one student",
    "primary_metric_unit": "student-year of need-based financial aid funded",
    "cost_per_outcome_usd": 9000,
    "impact_per_100_usd": 0.01111,
    "confidence": "medium",
    "source": "University of Iowa Common Data Set 2023-24 + ProPublica",
    "source_detail": "CDS 2023-24: avg institutional grant ~$9K. Foundation expenses $210M. ~32K students.",
    "extraction_note": "State University of Iowa Foundation is the 990-filing entity for U of Iowa fundraising.",
    "impact_description": "one year of need-based financial aid for one University of Iowa student (avg ~$9,000 institutional grant)",
    "annual_expenses_usd": 210154022,
    "revenue_year": 2024
  },

  {
    "name": "Gradient Learning",
    "ein": "352645251",
    "pp_name": "Gradient Learning",
    "cause": "education",
    "primary_metric_label": "one student on personalized learning platform",
    "primary_metric_value": 100000,
    "primary_metric_unit": "students accessing personalized learning programs",
    "cost_per_outcome_usd": 289,
    "impact_per_100_usd": 0.346,
    "confidence": "medium",
    "source": "Gradient Learning Annual Report + ProPublica",
    "source_detail": "Gradient Learning 2023: $28.8M expenses; ~100K students through Summit Learning platform",
    "extraction_note": "$28.8M / 100K students = $288/student",
    "impact_description": "one student accessing personalized, mastery-based learning through Gradient Learning's Summit Learning platform",
    "annual_expenses_usd": 28829269,
    "revenue_year": 2023
  },

  # ── COMMUNITY ────────────────────────────────────────────────────────────────

  {
    "name": "American Civil Liberties Union Foundation",
    "ein": "136213516",
    "pp_name": ["American Civil Liberties Union Foundation Inc",
                "ACLU Foundation",
                "Aclu Foundation Inc",
                "American Civil Liberties Union Fdn"],
    "cause": "community",
    "primary_metric_label": "one person served through civil liberties work",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "people protected through civil liberties litigation and policy advocacy",
    "cost_per_outcome_usd": 202,
    "impact_per_100_usd": 0.495,
    "confidence": "low",
    "source": "ACLU Foundation Annual Report + ProPublica",
    "source_detail": "ACLU Foundation 2024: $201.7M expenses; ~1,000 active legal cases + major policy affecting millions",
    "extraction_note": "Civil liberties impact is diffuse. Estimated ~1M people protected through cases and policy wins. $202M / 1M = $202/person.",
    "impact_description": "one person's civil liberties protected through ACLU Foundation legal representation, policy advocacy, or rights-education programs",
    "annual_expenses_usd": 201684585,
    "revenue_year": 2024
  },

  {
    "name": "The Aspen Institute",
    "ein": "840399006",
    "pp_name": ["The Aspen Institute Inc", "Aspen Institute"],
    "cause": "community",
    "primary_metric_label": "one leader engaged in Aspen programs",
    "primary_metric_value": 60000,
    "primary_metric_unit": "leaders and policymakers engaged through Aspen Institute programs",
    "cost_per_outcome_usd": 3762,
    "impact_per_100_usd": 0.0266,
    "confidence": "low",
    "source": "Aspen Institute Annual Report + ProPublica",
    "source_detail": "Aspen Institute 2023: $225.7M expenses; ~1,000 programs/events reaching ~60K participants",
    "extraction_note": "$225.7M / 60K participants = $3,762/person",
    "impact_description": "one leader, policymaker, or executive participating in Aspen Institute programs on society's most complex challenges",
    "annual_expenses_usd": 225738675,
    "revenue_year": 2023
  },

  {
    "name": "Center for Community Change",
    "ein": "520888113",
    "pp_name": ["Center For Community Change", "Center For Community Change Inc"],
    "cause": "community",
    "primary_metric_label": "one person mobilized through organizing",
    "primary_metric_value": 350000,
    "primary_metric_unit": "people mobilized through community organizing and advocacy campaigns",
    "cost_per_outcome_usd": 96,
    "impact_per_100_usd": 1.04,
    "confidence": "low",
    "source": "Center for Community Change Annual Report + ProPublica",
    "source_detail": "CCC 2023: $33.5M expenses; mobilizes low-income communities on immigration, housing, economic justice",
    "extraction_note": "Estimated 350K people engaged. $33.5M / 350K = $96/person.",
    "impact_description": "one person mobilized through community organizing campaigns for economic justice, immigration rights, or affordable housing",
    "annual_expenses_usd": 33544558,
    "revenue_year": 2023
  },

  {
    "name": "Institute for New Economic Thinking",
    "ein": "271916040",
    "pp_name": ["The Institute For New Economic Thinking Inc",
                "Institute For New Economic Thinking",
                "Inet"],
    "cause": "community",
    "primary_metric_label": "one economist or policymaker engaged",
    "primary_metric_value": 5000,
    "primary_metric_unit": "researchers and policymakers engaged through heterodox economics research",
    "cost_per_outcome_usd": 1198,
    "impact_per_100_usd": 0.0835,
    "confidence": "low",
    "source": "INET Annual Report + ProPublica",
    "source_detail": "INET 2023: $6M expenses; funds heterodox economics research and conferences with ~5K participants",
    "extraction_note": "$6M / 5K participants = $1,198/researcher",
    "impact_description": "one economist, researcher, or policymaker engaged in new approaches to economic thinking and policy reform",
    "annual_expenses_usd": 5988488,
    "revenue_year": 2023
  },

  {
    "name": "United Way of Greater Atlanta",
    "ein": "580566194",
    "pp_name": ["United Way Of Greater Atlanta Inc", "United Way Greater Atlanta"],
    "cause": "community",
    "primary_metric_label": "one person helped in the Atlanta region",
    "primary_metric_value": 400000,
    "primary_metric_unit": "people in the Atlanta region helped with education, health, or financial stability",
    "cost_per_outcome_usd": 264,
    "impact_per_100_usd": 0.379,
    "confidence": "medium",
    "source": "UWGA Annual Report + ProPublica",
    "source_detail": "UWGA 2023: $105.7M expenses; serves ~400K people across 9-county metro Atlanta region",
    "extraction_note": "$105.7M / 400K = $264/person",
    "impact_description": "one person in greater Atlanta accessing education support, health programs, or economic mobility resources through United Way",
    "annual_expenses_usd": 105745557,
    "revenue_year": 2023
  },

  {
    "name": "Boys & Girls Clubs of Metro Atlanta",
    "ein": "580566123",
    "pp_name": ["Boys And Girls Clubs Of Metro Atlanta Inc",
                "Boys And Girls Clubs Of Metro Atlanta"],
    "cause": "community",
    "primary_metric_label": "one year of programming for one youth",
    "primary_metric_value": 8000,
    "primary_metric_unit": "youth members receiving after-school and summer programming",
    "cost_per_outcome_usd": 3270,
    "impact_per_100_usd": 0.0306,
    "confidence": "medium",
    "source": "BGCMA Annual Report + ProPublica",
    "source_detail": "BGCMA 2023: $26.2M expenses; ~8,000 youth members across Atlanta clubs",
    "extraction_note": "$26.2M / 8K youth = $3,270/youth-year",
    "impact_description": "one year of after-school and summer programming for one young person in the Atlanta metro area",
    "annual_expenses_usd": 26161570,
    "revenue_year": 2023
  },

  {
    "name": "Nuclear Threat Initiative",
    "ein": "522289435",
    "pp_name": ["Nuclear Threat Initiative Inc", "NTI"],
    "cause": "international_aid",
    "primary_metric_label": "one policy engagement on nuclear or bio security",
    "primary_metric_value": 500,
    "primary_metric_unit": "senior policymakers engaged on nuclear and biological security risk reduction",
    "cost_per_outcome_usd": 37951,
    "impact_per_100_usd": 0.00264,
    "confidence": "low",
    "source": "NTI Annual Report + ProPublica",
    "source_detail": "NTI 2023: $19M expenses; works with ~40 countries on nuclear, bio, chem security policy",
    "extraction_note": "Estimated 500 senior policy officials engaged. $19M / 500 = $37,951/official. Policy impact highly diffuse.",
    "impact_description": "one senior policymaker or government official engaged through NTI's work to reduce global nuclear, biological, or chemical threats",
    "annual_expenses_usd": 18975625,
    "revenue_year": 2023
  },

  # ── WORKFORCE ────────────────────────────────────────────────────────────────

  {
    "name": "Generation",
    "ein": "471073442",
    "pp_name": ["Generation You Employed Inc", "Generation You Employed",
                "Generation Inc"],
    "cause": "workforce_dev",
    "primary_metric_label": "one person placed in sustainable employment",
    "primary_metric_value": 17000,
    "primary_metric_unit": "graduates placed in sustainable employment",
    "cost_per_outcome_usd": 1698,
    "impact_per_100_usd": 0.0589,
    "confidence": "medium",
    "source": "Generation Annual Report + ProPublica",
    "source_detail": "Generation 2023: $28.9M expenses; ~17K graduates/year placed in tech, healthcare, skilled trades",
    "extraction_note": "$28.9M / 17K graduates = $1,700/graduate placed",
    "impact_description": "one person completing Generation's job training program and securing sustainable employment in technology, healthcare, or skilled trades",
    "annual_expenses_usd": 28860128,
    "revenue_year": 2023
  },

]

# De-duplicate against existing entries by EIN
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
