import json

METRICS_FILE = "metrics.json"

with open(METRICS_FILE) as f:
    data = json.load(f)

def add_aliases(entries, name_match, new_aliases):
    for e in entries:
        if e["name"] == name_match:
            pp = e.get("pp_name", [])
            if pp is None:
                pp = []
            if isinstance(pp, str):
                pp = [pp] if pp else []
            for a in new_aliases:
                if a not in pp:
                    pp.append(a)
            e["pp_name"] = pp
            return True
    print(f"WARNING: not found: {name_match!r}")
    return False

# MSK: grant text has hyphen -> "SLOANKETTERING" (merged)
# Adding the hyphenated alias normalizes the SAME way, enabling the match
add_aliases(data, "Memorial Sloan Kettering Cancer Center", [
    "Memorial Sloan-Kettering Cancer Center",  # hyphenated form in grant data
])

# University of Nebraska: grant texts have "NEBRASKA-OMAHA" and "NEBRASKA-LINCOLN"
# Hyphenated forms normalize the same as the grant text
add_aliases(data, "University of Nebraska", [
    "University Of Nebraska-Omaha",   # grant: "UNIVERSITY OF NEBRASKA-OMAHA"
    "University Of Nebraska-Lincoln", # grant: "UNIVERSITY OF NEBRASKA-LINCOLN"
])

# BRAC: grant text "BRAC-USA" merges to "BRACUSA"
add_aliases(data, "BRAC", [
    "Brac-Usa",  # grant: "BRAC-USA" -> normalizes to "BRACUSA"
])

with open(METRICS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Hyphen alias fixes applied.")
