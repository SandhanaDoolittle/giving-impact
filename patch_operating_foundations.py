import json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scale_foundations import fetch_foundation, WORKERS, OUTPUT

def main():
    with open(OUTPUT) as f:
        existing = json.load(f)
    print(f"Re-checking {len(existing):,} existing foundations for operating-foundation status...")

    results = {}
    errored = []
    done = 0
    op_count = 0

    def run_batch(entries, workers):
        nonlocal done, op_count
        local_errored = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(fetch_foundation, e["ein"], e["name"]): e for e in entries}
            for fut in as_completed(futures):
                done += 1
                e = futures[fut]
                result, status = fut.result()
                if status == "ok":
                    results[e["ein"]] = result
                    if result.get("operating_foundation"):
                        op_count += 1
                        print(f"[{done}/{len(existing)}] 🏛  OPERATING: {result['name'][:50]:<50} {result['pct']}% (was {e['pct']}%)")
                elif status == "error":
                    local_errored.append(e)
                # "below_min"/"no_filings" shouldn't happen for EINs we already kept,
                # but if it does, just keep the old entry below rather than drop it.
        return local_errored

    errored = run_batch(existing, WORKERS)
    retry_round = 1
    while errored and retry_round <= 3:
        print(f"\nRetry round {retry_round}: re-checking {len(errored)} foundations...")
        errored = run_batch(errored, 2)
        retry_round += 1

    if errored:
        print(f"\n⚠️  {len(errored)} foundations failed after retries — keeping their existing values unchanged:")
        for e in errored[:20]:
            print(f"   {e['name']} (EIN {e['ein']})")

    updated = [results.get(e["ein"], e) for e in existing]

    with open(OUTPUT, "w") as out:
        json.dump(updated, out, indent=2)

    compliant = sum(1 for r in updated if r.get("compliant"))
    print(f"\n{'='*60}")
    print(f"Total foundations: {len(updated)}")
    print(f"Operating foundations found: {op_count}")
    print(f"Compliant: {compliant}  Non-compliant: {len(updated)-compliant}")
    print(f"Unresolved errors (kept old values): {len(errored)}")
    print(f"✅ Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
