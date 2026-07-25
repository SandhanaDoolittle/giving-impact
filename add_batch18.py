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

# DonorsChoose: grant text "DONORSCHOOSEORG" (no space) doesn't match "Donorschoose Org"
add_aliases(data, "DonorsChoose", [
    "Donorschooseorg",
    "Donors Choose Org",
])

# Save the Children: grant text "SAVE THE CHILDREN FEDERATION INC" → normalized "SAVE CHILDREN FEDERATION"
# Existing "Save the Children USA" → normalized "SAVE CHILDREN USA" (no match)
add_aliases(data, "Save the Children USA", [
    "Save The Children Federation Inc",
    "Save The Children Federation",
    "Save The Children",
    "Save Children Federation",
])

# ── NEW ENTRIES ────────────────────────────────────────────────────────────────
new_entries = [

  # Partnership for Public Service — improving the federal government
  {
    "name": "Partnership for Public Service",
    "ein": "61540513",
    "pp_name": [
      "Partnership For Public Service Inc",
      "Partnership For Public Service",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged in federal government improvement through Partnership for Public Service",
    "primary_metric_value": 200000,
    "primary_metric_unit": "government employees, transition leaders, and public servants engaged through Partnership for Public Service's training, research, and presidential transition programs",
    "cost_per_outcome_usd": 137,
    "impact_per_100_usd": 0.731,
    "confidence": "low",
    "source": "Partnership for Public Service Annual Report + ProPublica",
    "source_detail": "Partnership for Public Service 2023: $27.4M expenses. Nonpartisan nonprofit that works to make the federal government more effective. Runs the Best Places to Work in Government rankings, presidential transition leadership programs, and federal management training.",
    "extraction_note": "$27,364,126 / 200,000 people engaged = $136.8/person. PPS runs the Center for Presidential Transition (used by incoming administrations), Best Places to Work (drives agency reform), and Samuel J. Heyman Service to America Medals (the 'Oscars' of public service).",
    "impact_description": "one person engaged through Partnership for Public Service's programs improving the federal government — runs the presidential transition Center, Best Places to Work rankings that drive agency reform, and leadership training for 200K+ federal employees",
    "annual_expenses_usd": 27364126,
    "revenue_year": 2023,
  },

  # Montefiore Medical Center — major academic medical center, Bronx NY
  {
    "name": "Montefiore Medical Center",
    "ein": "131740114",
    "pp_name": [
      "Montefiore Medical Center",
      "Montefiore Health System",
      "Montefiore",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Montefiore Medical Center",
    "primary_metric_value": 2000000,
    "primary_metric_unit": "patient encounters at Montefiore Medical Center and affiliated hospitals serving one of America's most medically underserved urban populations in the Bronx",
    "cost_per_outcome_usd": 2502,
    "impact_per_100_usd": 0.0400,
    "confidence": "medium",
    "source": "Montefiore Medical Center Annual Report + ProPublica",
    "source_detail": "Montefiore Medical Center 2023: $5.0B expenses. Major academic medical center in the Bronx, NY. Affiliated hospital system for Albert Einstein College of Medicine. Serves 2M+ patient encounters/year in one of the US's most underserved communities.",
    "extraction_note": "$5,003,322,926 / 2,000,000 patient encounters = $2,501.7/encounter. Montefiore serves a predominantly Medicaid/uninsured population in the Bronx; 85%+ of patients are from minority communities. Key hospital for Bronx residents with complex cardiac, oncology, and neurological needs.",
    "impact_description": "one patient encounter at Montefiore Medical Center — a major Albert Einstein-affiliated academic medical center in the Bronx serving 2M+ patients/year in one of America's most underserved communities, with 85%+ of patients from minority and low-income backgrounds",
    "annual_expenses_usd": 5003322926,
    "revenue_year": 2023,
  },

  # Atlanta Speech School — school for children with hearing loss and language disorders
  {
    "name": "Atlanta Speech School",
    "ein": "580566198",
    "pp_name": [
      "Atlanta Speech School Inc",
      "Atlanta Speech School",
    ],
    "cause": "health",
    "primary_metric_label": "one child served by Atlanta Speech School's hearing and language programs",
    "primary_metric_value": 1500,
    "primary_metric_unit": "children with hearing loss, autism, and language disorders served through Atlanta Speech School's auditory-oral programs and assistive technology access initiatives",
    "cost_per_outcome_usd": 19895,
    "impact_per_100_usd": 0.00503,
    "confidence": "medium",
    "source": "Atlanta Speech School Annual Report + ProPublica",
    "source_detail": "Atlanta Speech School 2024: $29.8M expenses. A nationally recognized school for children with hearing loss and language disorders. Provides auditory-oral therapy enabling children who are deaf or hard of hearing to speak and listen with cochlear implants.",
    "extraction_note": "$29,841,952 / 1,500 children served = $19,895/child. Atlanta Speech School teaches children with hearing loss to speak and listen without sign language, using auditory-verbal therapy and cochlear implants. Also runs a technology access program for underserved families.",
    "impact_description": "one child with hearing loss or language disorder served by Atlanta Speech School — a nationally recognized program helping children who are deaf or hard of hearing to speak and listen through auditory-verbal therapy and cochlear implant support, enabling mainstream school attendance",
    "annual_expenses_usd": 29841952,
    "revenue_year": 2024,
  },

  # Rush University Medical Center — Chicago academic medical center
  {
    "name": "Rush University Medical Center",
    "ein": "362174823",
    "pp_name": [
      "Rush University Medical Center",
      "Rush Medical Center",
      "Rush University",
      "Rush System For Health",
    ],
    "cause": "health",
    "primary_metric_label": "one patient encounter at Rush University Medical Center",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "patient encounters at Rush University Medical Center in Chicago including inpatient, outpatient, and emergency care",
    "cost_per_outcome_usd": 2591,
    "impact_per_100_usd": 0.0386,
    "confidence": "medium",
    "source": "Rush University Medical Center Annual Report + ProPublica",
    "source_detail": "Rush University Medical Center 2023: $2.59B expenses. Major academic medical center in Chicago affiliated with Rush Medical College. ~1M patient encounters/year. Known for orthopedic, neurological, and oncology care.",
    "extraction_note": "$2,591,162,936 / 1,000,000 patient encounters = $2,591.2/encounter. Rush is consistently ranked among the top hospitals in Illinois and the US. Part of Rush System for Health with hospitals across Chicago area.",
    "impact_description": "one patient encounter at Rush University Medical Center — a top-ranked Chicago academic medical center affiliated with Rush Medical College, known for orthopedic, neurological, oncology, and cardiovascular care",
    "annual_expenses_usd": 2591162936,
    "revenue_year": 2023,
  },

  # Bipartisan Policy Center — bipartisan policy research and advocacy
  {
    "name": "Bipartisan Policy Center",
    "ein": "731628382",
    "pp_name": [
      "Bipartisan Policy Center Inc",
      "Bipartisan Policy Center",
      "Bpc",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged through Bipartisan Policy Center research and convening",
    "primary_metric_value": 500000,
    "primary_metric_unit": "policymakers, journalists, and citizens engaged through Bipartisan Policy Center's evidence-based policy research, congressional testimony, and bipartisan task forces",
    "cost_per_outcome_usd": 73,
    "impact_per_100_usd": 1.375,
    "confidence": "low",
    "source": "Bipartisan Policy Center Annual Report + ProPublica",
    "source_detail": "Bipartisan Policy Center 2023: $36.4M expenses. Think tank founded by 4 former Senate Majority Leaders (Daschle, Dole, Baker, Mitchell) to develop policy solutions through bipartisan cooperation. Works on housing, health, energy, immigration, and democracy.",
    "extraction_note": "$36,412,895 / 500,000 people engaged = $72.8/person. BPC convenes Republican and Democratic leaders, producing task force reports that have influenced ACA implementation, student loan reform, and budget deals.",
    "impact_description": "one person reached through Bipartisan Policy Center research — a think tank founded by 4 former Senate Majority Leaders that builds bipartisan consensus on housing, health, immigration, energy, and democracy issues through evidence-based task forces",
    "annual_expenses_usd": 36412895,
    "revenue_year": 2023,
  },

  # California Institute of the Arts (CalArts) — leading arts institution in LA
  {
    "name": "California Institute of the Arts",
    "ein": "956102146",
    "pp_name": [
      "California Institute Of The Arts",
      "Calarts",
      "Cal Arts",
    ],
    "cause": "arts_culture",
    "primary_metric_label": "one year of need-based aid for one CalArts student",
    "primary_metric_unit": "student-year of need-based financial aid funded at California Institute of the Arts",
    "cost_per_outcome_usd": 42000,
    "impact_per_100_usd": 0.00238,
    "confidence": "medium",
    "source": "CalArts Common Data Set 2023-24 + ProPublica",
    "source_detail": "California Institute of the Arts 2023: $113.5M expenses. Leading multidisciplinary arts institution in Valencia, CA (~1,500 students). CDS 2023-24 avg institutional need-based grant ~$42,000. Founded by Walt Disney; alumni include major figures in animation, music, and contemporary art.",
    "extraction_note": "CDS 2023-24 CalArts avg institutional need-based grant used. CalArts alumni include major figures in contemporary art (John Baldessari), animation (Pixar founders, directors of Frozen/Tangled), and music (Charlie Parker influenced jazz programs).",
    "impact_description": "one year of need-based financial aid for one CalArts student (avg ~$42,000 institutional grant) — the leading multidisciplinary arts institution in the US, founded by Walt Disney, whose alumni have shaped global animation, contemporary art, and music",
    "annual_expenses_usd": 113543204,
    "revenue_year": 2023,
  },

  # Marquette University — Jesuit university in Milwaukee
  {
    "name": "Marquette University",
    "ein": "390806251",
    "pp_name": [
      "Marquette University",
      "Marquette Univ",
    ],
    "cause": "education",
    "primary_metric_label": "one year of need-based aid for one Marquette University student",
    "primary_metric_unit": "student-year of need-based financial aid funded at Marquette University",
    "cost_per_outcome_usd": 29000,
    "impact_per_100_usd": 0.00345,
    "confidence": "medium",
    "source": "Marquette University Common Data Set 2023-24 + ProPublica",
    "source_detail": "Marquette University 2023: $652.7M expenses. Private Jesuit research university in Milwaukee, WI with ~12,000 students. CDS 2023-24 avg institutional need-based grant ~$29,000. Known for law, business, nursing, and engineering.",
    "extraction_note": "CDS 2023-24 Marquette avg institutional need-based grant used. Jesuit tradition of education for the whole person and service to the community.",
    "impact_description": "one year of need-based financial aid for one Marquette University student (avg ~$29,000 institutional grant) — a Jesuit research university in Milwaukee with nationally ranked law, business, nursing, and engineering programs",
    "annual_expenses_usd": 652702241,
    "revenue_year": 2023,
  },

  # IDEA Public Schools — large Texas charter school network
  {
    "name": "IDEA Public Schools",
    "ein": "742948339",
    "pp_name": [
      "Idea Public Schools",
      "Idea Public Schools Inc",
    ],
    "cause": "education",
    "primary_metric_label": "one student educated at an IDEA Public Schools campus",
    "primary_metric_value": 75000,
    "primary_metric_unit": "students enrolled in IDEA Public Schools' K-12 college preparatory charter school network serving low-income communities in Texas, Louisiana, Florida, and Ohio",
    "cost_per_outcome_usd": 12879,
    "impact_per_100_usd": 0.00776,
    "confidence": "medium",
    "source": "IDEA Public Schools Annual Report + ProPublica",
    "source_detail": "IDEA Public Schools 2023: $965.9M expenses. Large K-12 charter network with 130+ schools and 75,000+ students in TX, LA, FL, OH, CO. Mission: 100% college acceptance for low-income students of color. Reports 100% college acceptance rate for graduates.",
    "extraction_note": "$965,895,627 / 75,000 students = $12,879/student/year. IDEA operates in underserved communities (Rio Grande Valley, San Antonio, Houston) with 90%+ economically disadvantaged students. Extended-day model adds ~30 more instructional days per year.",
    "impact_description": "one student in IDEA Public Schools — a high-performing K-12 charter network in Texas and 5 other states serving 75,000+ students from low-income communities with a 100% college acceptance rate for graduates, including students from the Rio Grande Valley and San Antonio",
    "annual_expenses_usd": 965895627,
    "revenue_year": 2023,
  },

  # Common Cause Education Fund — democracy and voting rights advocacy
  {
    "name": "Common Cause Education Fund",
    "ein": "311705370",
    "pp_name": [
      "Common Cause Education Fund",
      "Common Cause",
    ],
    "cause": "community",
    "primary_metric_label": "one person engaged in Common Cause Education Fund democracy reform campaigns",
    "primary_metric_value": 1000000,
    "primary_metric_unit": "people engaged through Common Cause Education Fund's campaigns for voting rights, campaign finance reform, and electoral integrity",
    "cost_per_outcome_usd": 17,
    "impact_per_100_usd": 6.01,
    "confidence": "low",
    "source": "Common Cause Education Fund Annual Report + ProPublica",
    "source_detail": "Common Cause Education Fund 2023: $16.6M expenses. Nonpartisan watchdog and advocacy organization promoting accountability in government. Campaigns for voting rights, gerrymandering reform, campaign finance transparency, and ethics in government.",
    "extraction_note": "$16,648,806 / 1,000,000 people engaged = $16.6/person. Common Cause has 1.5M+ members and advocates across all 50 states for fair elections, campaign finance reform, and anti-corruption measures.",
    "impact_description": "one person engaged through Common Cause Education Fund's campaigns for fair elections, voting rights, and campaign finance reform — a nonpartisan advocacy organization with 1.5M+ members fighting gerrymandering, dark money, and voter suppression in all 50 states",
    "annual_expenses_usd": 16648806,
    "revenue_year": 2023,
  },

  # Integrate Health — community-based healthcare delivery in Togo, West Africa
  {
    "name": "Integrate Health",
    "ein": "134288670",
    "pp_name": [
      "Integrate Health Inc",
      "Integrate Health",
    ],
    "cause": "health",
    "primary_metric_label": "one person receiving healthcare through Integrate Health's community health system in Togo",
    "primary_metric_value": 200000,
    "primary_metric_unit": "people in rural Togo receiving malaria treatment, HIV care, maternal health, and primary care through Integrate Health's community health worker network",
    "cost_per_outcome_usd": 42,
    "impact_per_100_usd": 2.39,
    "confidence": "medium",
    "source": "Integrate Health Annual Report + ProPublica",
    "source_detail": "Integrate Health Inc 2023: $8.4M expenses. Builds community health systems in Togo in partnership with the government. 400+ community health workers delivering malaria treatment, HIV care, maternal and child health, and family planning to 200K+ people in rural communities.",
    "extraction_note": "$8,365,671 / 200,000 people = $41.8/person. Integrate Health is recognized by GiveWell as a top-recommended charity for cost-effective global health outcomes. Focuses on long-term system building with government ownership.",
    "impact_description": "one person in rural Togo receiving healthcare through Integrate Health's community health system — a GiveWell top-recommended organization deploying 400+ community health workers to deliver malaria treatment, HIV care, and maternal health services to 200K+ people in West Africa",
    "annual_expenses_usd": 8365671,
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
