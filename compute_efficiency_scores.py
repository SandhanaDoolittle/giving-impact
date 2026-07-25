import json
from match_grants import normalize

METRICS_FILE = "metrics.json"
CHUNK_FILES = [f"foundation_grants_{i}.json" for i in range(8)]
OUTPUT_FILE = "foundation_scores.json"

# Only causes with an exact, citable number from Rethink Priorities' Pulse survey
# (~5,000 US adults, 0-10 personal-importance scale). "Global Health and Development"
# (-> international_aid) was reported only as "rated in the middle of causes" with no
# exact figure given -- NOT included here, since inventing a specific number from a
# vague qualitative description would be fabrication, not sourcing. All other causes
# (food_security, workforce_dev, housing, missions, recovery, education,
# disaster_relief, community, arts_culture, international_aid) are pending the
# supplementary poll.
PULSE_IMPORTANCE = {
    "health": (8.9 + 8.6) / 2,  # average of Cancer Research (8.9) and Mental Health (8.6)
    "environment": 7.4,          # Climate Change
    "animal_welfare": 7.4,       # Farmed Animal Welfare
}

CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.7, "low": 0.4}

# Below this in matched dollars, a foundation's score is too noisy to be meaningful
# (could be a single $500 grant deciding the whole score).
MIN_MATCHED_DOLLARS = 50_000
MIN_MATCHED_GRANTS = 2

def build_lookup():
    with open(METRICS_FILE) as f:
        metrics = json.load(f)
    by_norm = {}
    for e in metrics:
        pp_name = e.get("pp_name")
        pp_names = pp_name if isinstance(pp_name, list) else [pp_name]
        for raw_name in {e.get("name"), *pp_names} - {None}:
            by_norm.setdefault(normalize(raw_name), e)
    return by_norm

def score_foundation(g, by_norm):
    matched = g.get("matched_detail", [])
    total_amount = g.get("total_amount") or 0

    # Documentation/transparency score: confidence-weighted share of ALL grant
    # dollars (not just top_grants) backed by a real, verifiable impact metric.
    doc_numerator = sum(d["amount"] * CONFIDENCE_WEIGHT.get(d["confidence"], 0.4) for d in matched)
    documentation_score = round(doc_numerator / total_amount, 4) if total_amount else None

    # Importance score: dollar-weighted average Pulse importance rating, but only
    # across the slice of matched dollars whose cause has a confident Pulse number.
    importance_numerator = 0.0
    importance_dollars = 0.0
    importance_grant_count = 0
    for d in matched:
        entry = by_norm.get(normalize(d["recipient"]))
        if not entry:
            continue  # shouldn't happen -- matched_detail came from this same lookup
        weight = PULSE_IMPORTANCE.get(entry.get("cause"))
        if weight is None:
            continue  # this cause is still pending poll data
        importance_numerator += d["amount"] * weight
        importance_dollars += d["amount"]
        importance_grant_count += 1

    if importance_dollars >= MIN_MATCHED_DOLLARS and importance_grant_count >= MIN_MATCHED_GRANTS:
        importance_score = round(importance_numerator / importance_dollars, 3)
        importance_status = "ok"
    elif importance_grant_count > 0:
        importance_score = None
        importance_status = "insufficient_data"
    else:
        importance_score = None
        importance_status = "no_pulse_covered_causes_matched"

    return {
        "ein": g["ein"], "name": g["name"],
        "documentation_score": documentation_score,
        "documentation_dollars_basis": round(doc_numerator, 2),
        "total_amount": total_amount,
        "importance_score": importance_score,
        "importance_status": importance_status,
        "importance_dollars_basis": round(importance_dollars, 2),
        "importance_grant_count": importance_grant_count,
    }

def main():
    by_norm = build_lookup()
    results = []
    for chunk_file in CHUNK_FILES:
        with open(chunk_file) as f:
            data = json.load(f)
        for g in data:
            if not g.get("matched_detail"):
                continue
            results.append(score_foundation(g, by_norm))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    ok = sum(1 for r in results if r["importance_status"] == "ok")
    insufficient = sum(1 for r in results if r["importance_status"] == "insufficient_data")
    no_pulse = sum(1 for r in results if r["importance_status"] == "no_pulse_covered_causes_matched")

    print(f"Scored {len(results)} foundations with at least one matched grant")
    print(f"  Importance score computable today (health/environment/animal_welfare only): {ok}")
    print(f"  Has matched grants but not enough in Pulse-covered causes yet: {insufficient}")
    print(f"  No matched grants in any Pulse-covered cause at all (blocked on poll data): {no_pulse}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
