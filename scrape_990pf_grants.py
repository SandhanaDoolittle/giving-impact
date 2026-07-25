#!/usr/bin/env python3
"""
scrape_990pf_grants.py — Extract Schedule I grant data from IRS 990-PF XML filings.

Uses range requests to read individual XML files from IRS ZIP batches without
downloading the full ZIP. Processes all foundations in our index that lack grant data.
"""

import json, struct, zlib, re, urllib.request, urllib.error, glob, os, time, sys, csv, io
import http.client, ssl
import xml.etree.ElementTree as ET
from collections import defaultdict

SCRATCHPAD = '/private/tmp/claude-501/-Users-cmd-Documents-Phoenix-Code/a44fdf35-c083-417c-a738-319a3f5fbf50/scratchpad'
INDEX_FILE = f'{SCRATCHPAD}/irs_index_matches.json'
GRANT_SHARD_PATTERN = 'foundation_grants_{}.json'
N_SHARDS = 8
IRS_HOST  = 'apps.irs.gov'
IRS_ZIP_BASE = f'https://{IRS_HOST}/pub/epostcard/990/xml'

DELAY = 0.05  # seconds between requests (connection reuse means less overhead)

# ── Persistent HTTPS connection ────────────────────────────────────────────────

_conn = None

def _get_conn():
    """Return a persistent HTTPS connection to the IRS server, reconnecting if needed."""
    global _conn
    try:
        if _conn is None:
            raise Exception("no connection")
        _conn.request('HEAD', '/', headers={'User-Agent': 'Mozilla/5.0'})
        _conn.getresponse().read()
    except Exception:
        ctx = ssl.create_default_context()
        _conn = http.client.HTTPSConnection(IRS_HOST, timeout=120, context=ctx)
    return _conn

def range_get(path, start, end, retries=4):
    """Download a byte range from an IRS path using a persistent connection."""
    for attempt in range(retries):
        try:
            conn = _get_conn()
            conn.request('GET', path, headers={
                'User-Agent': 'Mozilla/5.0 (research/educational use)',
                'Range':      f'bytes={start}-{end}',
                'Connection': 'keep-alive',
            })
            resp = conn.getresponse()
            data = resp.read()
            if resp.status in (206, 200):
                return data
            raise Exception(f"HTTP {resp.status}")
        except Exception as e:
            global _conn
            _conn = None  # Force reconnect on next call
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return b''

def range_get_url(url, start, end, retries=4):
    """Convenience: range_get for a full URL (must be on IRS_HOST)."""
    path = url.replace(f'https://{IRS_HOST}', '')
    return range_get(path, start, end, retries)

def get_size(url):
    """Get the total size of a URL via Content-Range header."""
    path = url.replace(f'https://{IRS_HOST}', '')
    conn = _get_conn()
    conn.request('GET', path, headers={
        'User-Agent': 'Mozilla/5.0',
        'Range': 'bytes=0-0',
    })
    resp = conn.getresponse()
    cr = resp.getheader('Content-Range', '')
    resp.read()
    return int(cr.split('/')[-1]) if '/' in cr else 0

# ── ZIP range reader ───────────────────────────────────────────────────────────

def get_central_directory(url):
    """Download and parse a ZIP file's central directory using range requests.
    Returns dict mapping filename → {local_offset, comp_size, uncomp_size, comp_method}
    """
    total = get_size(url)
    time.sleep(DELAY)

    # Read last 64KB to find End-of-Central-Directory record
    tail_start = max(0, total - 65536)
    tail = range_get_url(url, tail_start, total - 1)
    time.sleep(DELAY)

    pos = tail.rfind(b'PK\x05\x06')
    if pos == -1:
        raise ValueError(f"EOCD not found in {url}")

    eocd = tail[pos:]
    cd_size   = struct.unpack_from('<I', eocd, 12)[0]
    cd_offset = struct.unpack_from('<I', eocd, 16)[0]

    # Download the central directory
    cd_data = range_get_url(url, cd_offset, cd_offset + cd_size - 1)
    time.sleep(DELAY)

    entries = {}
    p = 0
    sig = b'PK\x01\x02'
    while p < len(cd_data) - 46:
        if cd_data[p:p+4] != sig:
            break
        comp_method = struct.unpack_from('<H', cd_data, p + 10)[0]
        comp_size   = struct.unpack_from('<I', cd_data, p + 20)[0]
        uncomp_size = struct.unpack_from('<I', cd_data, p + 24)[0]
        fname_len   = struct.unpack_from('<H', cd_data, p + 28)[0]
        extra_len   = struct.unpack_from('<H', cd_data, p + 30)[0]
        comment_len = struct.unpack_from('<H', cd_data, p + 32)[0]
        local_off   = struct.unpack_from('<I', cd_data, p + 42)[0]

        fname = cd_data[p+46 : p+46+fname_len].decode('utf-8', errors='replace')
        entries[fname] = {
            'local_offset': local_off,
            'comp_size':    comp_size,
            'uncomp_size':  uncomp_size,
            'comp_method':  comp_method,
        }
        p += 46 + fname_len + extra_len + comment_len

    return entries

def extract_file(url, entry):
    """Extract and decompress a single file from a ZIP in one range request.
    Downloads local header + compressed data together to avoid a round-trip.
    """
    lo = entry['local_offset']
    cs = entry['comp_size']

    # Download: 30 (header) + 100 (fname+extra buffer) + comp_size (data)
    # We'll parse the actual header fields to find where the data starts.
    buf = range_get_url(url, lo, lo + 30 + 100 + cs - 1)
    time.sleep(DELAY)

    fname_len = struct.unpack_from('<H', buf, 26)[0]
    extra_len = struct.unpack_from('<H', buf, 28)[0]
    data_offset = 30 + fname_len + extra_len

    comp_data = buf[data_offset : data_offset + cs]

    if entry['comp_method'] == 8:
        return zlib.decompress(comp_data, -15)
    elif entry['comp_method'] == 0:
        return comp_data
    else:
        raise ValueError(f"Unknown compression: {entry['comp_method']}")

# ── 990-PF XML parser ──────────────────────────────────────────────────────────

def strip_ns(tag):
    """Remove XML namespace prefix."""
    return tag.split('}')[-1] if '}' in tag else tag

def find_text(elem, *tags):
    """Search for the first matching tag at any depth, returning stripped text."""
    for tag in tags:
        for el in elem.iter():
            if strip_ns(el.tag) == tag and el.text and el.text.strip():
                return el.text.strip()
    return ''

def parse_990pf_xml(xml_bytes):
    """
    Parse a 990-PF XML filing and extract grant data.
    Returns dict with: year, total_grants, total_amount, top_grants
    Returns None if no grant data found.

    IRS 990-PF XML structure (2022v5.0+ schema):
      /Return/ReturnData/IRS990PF/SupplementaryInformationGrp
        /GrantOrContributionPdDurYrGrp  (one per grant)
          /BusinessNameLine1Txt         (recipient name)
          /Amt                          (amount)
          /GrantOrContributionPurposeTxt
        /TotalGrantOrContriPdDurYrAmt   (total paid)
    """
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return None

    # ── Tax year ──────────────────────────────────────────────────────────────
    year = ''
    for el in root.iter():
        tag = strip_ns(el.tag)
        if tag in ('TaxPeriodEndDt', 'TaxYr', 'TaxPeriodEndDate'):
            year = (el.text or '')[:4]
            if year:
                break

    # ── Find grant section (multiple schema versions) ─────────────────────────
    # The parent container element varies by schema year
    SUPP_TAGS = {'SupplementaryInformationGrp', 'PartXV', 'PartXvSection'}
    # The individual grant group element varies by schema year
    GRANT_TAGS = {
        'GrantOrContributionPdDurYrGrp',  # 2020+ schema (most common)
        'GrntAsstDomOrgsGvtsGrp',          # older alias
        'StmtOfGrntAsstDomestcOrgsGrp',    # another older alias
        'DistributionInformationGrp',       # 2017 and earlier
        'Recipient',                        # very old
    }
    # Amount field within each grant group
    AMT_TAGS = {'Amt', 'CashGrantAmt', 'AmountPdDuringYrAmt', 'AmountPdDurYrAmt',
                'AmountPaidDuringYearAmt', 'GrantAmt'}
    # Total amount field in the section
    TOTAL_TAGS = {'TotalGrantOrContriPdDurYrAmt', 'TotalGrantsAmt',
                  'TotalDistributionsAmt', 'GrntAsstDomOrgsGvtsTotalAmt'}

    grants = []
    total_amount = 0.0
    found_total = None

    # Search all elements for grant groups
    for el in root.iter():
        tag = strip_ns(el.tag)

        # Capture totals
        if tag in TOTAL_TAGS and el.text:
            try:
                found_total = float(el.text.strip().replace(',', ''))
            except ValueError:
                pass
            continue

        if tag not in GRANT_TAGS:
            continue

        # Extract recipient name
        name = ''
        for child in el.iter():
            ctag = strip_ns(child.tag)
            if ctag in ('BusinessNameLine1Txt', 'BusinessNameLine1',
                        'RecipientPersonNm', 'PersonNm', 'NameLine1Txt'):
                if child.text and child.text.strip():
                    name = child.text.strip()
                    break

        # Extract amount
        amount = 0.0
        for child in el.iter():
            ctag = strip_ns(child.tag)
            if ctag in AMT_TAGS:
                try:
                    amount = float((child.text or '').replace(',', ''))
                    break
                except ValueError:
                    pass

        # Extract purpose
        purpose = ''
        for child in el.iter():
            ctag = strip_ns(child.tag)
            if ctag in ('GrantOrContributionPurposeTxt', 'PurposeOfGrantTxt',
                        'PurposeOfGrant', 'RelationshipWithDonorTxt'):
                if child.text and child.text.strip():
                    purpose = child.text.strip()[:200]
                    break

        if name:
            grants.append({
                'name': name.upper(),
                'amount': amount,
                'purpose': purpose.upper(),
            })
            total_amount += amount

    if not grants:
        return None

    # Deduplicate
    seen = set()
    unique = []
    for g in grants:
        key = (g['name'], g['amount'])
        if key not in seen:
            seen.add(key)
            unique.append(g)

    unique.sort(key=lambda x: x['amount'], reverse=True)

    return {
        'year':         year,
        'total_grants': len(unique),
        'total_amount': round(found_total if found_total is not None else total_amount, 2),
        'top_grants':   unique[:20],
    }

# ── Shard helpers ──────────────────────────────────────────────────────────────

def load_shards():
    """Load all foundation_grants shards into a dict keyed by EIN."""
    by_ein = {}
    for fp in sorted(glob.glob(GRANT_SHARD_PATTERN.format('*'))):
        with open(fp) as f:
            data = json.load(f)
        for entry in data:
            by_ein[entry['ein']] = entry
    return by_ein

def save_shards(by_ein):
    """Save the combined grant data back to N_SHARDS shard files."""
    all_entries = sorted(by_ein.values(), key=lambda x: x['ein'])
    shards = [[] for _ in range(N_SHARDS)]
    for i, entry in enumerate(all_entries):
        shards[i % N_SHARDS].append(entry)
    for i, shard in enumerate(shards):
        fp = GRANT_SHARD_PATTERN.format(i)
        with open(fp, 'w') as f:
            json.dump(shard, f, indent=2)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading IRS index matches...")
    with open(INDEX_FILE) as f:
        index = json.load(f)  # ein → {ein, name, tax_period, year, object_id, batch_id}

    print("Loading existing grant data...")
    existing = load_shards()
    print(f"  {len(existing):,} foundations already have grant data")

    # Filter to foundations that need grant data
    needed = {ein: info for ein, info in index.items() if ein not in existing}
    print(f"  {len(needed):,} foundations need grant data")

    # Group by batch_id (normalize case)
    by_batch = defaultdict(list)
    for ein, info in needed.items():
        batch = info['batch_id'].upper() if info['batch_id'] else ''
        by_batch[batch].append(info)

    # Handle foundations with no batch_id separately
    no_batch = by_batch.pop('', [])
    print(f"  {len(no_batch)} with no batch_id (will try 2023 scan)")

    # Sort batches by count descending (tackle biggest first)
    batches = sorted(by_batch.items(), key=lambda x: len(x[1]), reverse=True)
    print(f"\nBatches to process: {len(batches)}")
    for b, entries in batches:
        print(f"  {b}: {len(entries)} foundations")

    progress_file = f'{SCRATCHPAD}/scrape_progress.json'
    done_batches = set()
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            done_batches = set(json.load(f).get('done_batches', []))
        print(f"\nResuming — {len(done_batches)} batches already done")

    total_added = 0
    total_failed = 0

    for batch_id, foundations in batches:
        if batch_id in done_batches:
            print(f"\n[SKIP] {batch_id} (already done)")
            continue

        year_part = batch_id[:4]
        zip_url = f'{IRS_ZIP_BASE}/{year_part}/{batch_id}.zip'
        print(f"\n{'='*60}")
        print(f"Batch: {batch_id} ({len(foundations)} foundations)")
        print(f"ZIP: {zip_url}")

        try:
            print("  Reading central directory...", flush=True)
            cd = get_central_directory(zip_url)
            print(f"  CD has {len(cd):,} files")
        except Exception as e:
            print(f"  ERROR reading CD: {e}")
            continue

        batch_added = 0
        batch_failed = 0

        for i, info in enumerate(foundations):
            ein = info['ein']
            oid = info['object_id']
            fname = f"{batch_id}/{oid}_public.xml"

            if ein in existing:
                continue  # already have it from a previous run

            if fname not in cd:
                # Try case variants
                fname_alt = f"{batch_id.lower()}/{oid}_public.xml"
                if fname_alt in cd:
                    fname = fname_alt
                else:
                    print(f"  [{i+1}/{len(foundations)}] {info['name'][:40]} — NOT FOUND in CD")
                    batch_failed += 1
                    continue

            try:
                xml_bytes = extract_file(zip_url, cd[fname])
                parsed = parse_990pf_xml(xml_bytes)

                if parsed is None:
                    print(f"  [{i+1}/{len(foundations)}] {info['name'][:40]} — no grants in XML")
                    # Still add an entry so we know we looked
                    existing[ein] = {
                        'ein': ein, 'name': info['name'],
                        'year': info['tax_period'][:4],
                        'total_grants': 0, 'total_amount': 0,
                        'matched_grants': 0, 'matched_amount': 0, 'match_pct': 0,
                        'top_grants': [],
                    }
                    batch_added += 1
                else:
                    existing[ein] = {
                        'ein': ein, 'name': info['name'],
                        'year': parsed['year'] or info['tax_period'][:4],
                        'total_grants': parsed['total_grants'],
                        'total_amount': parsed['total_amount'],
                        'matched_grants': 0, 'matched_amount': 0, 'match_pct': 0,
                        'top_grants': parsed['top_grants'],
                    }
                    batch_added += 1
                    if (i + 1) % 50 == 0:
                        n_grants = len(parsed['top_grants'])
                        print(f"  [{i+1}/{len(foundations)}] {info['name'][:40]}: {n_grants} grants, ${parsed['total_amount']/1e6:.1f}M")

            except Exception as e:
                print(f"  [{i+1}/{len(foundations)}] {info['name'][:40]} — ERROR: {e}")
                batch_failed += 1

        print(f"  Batch done: +{batch_added} added, {batch_failed} failed")
        total_added += batch_added
        total_failed += batch_failed

        # Save after each batch
        save_shards(existing)
        done_batches.add(batch_id)
        with open(progress_file, 'w') as f:
            json.dump({'done_batches': list(done_batches)}, f)
        print(f"  Saved. Total so far: {len(existing):,} foundations with grant data")

    # Handle no-batch foundations
    if no_batch:
        print(f"\n{'='*60}")
        print(f"Handling {len(no_batch)} foundations with no batch_id...")
        # These have valid object_ids but we need to scan 2023 ZIPs for them
        # Build a lookup map of object_id -> info
        oid_map = {info['object_id']: info for info in no_batch}
        print(f"  Object_ids to find: {list(oid_map.keys())[:3]}...")

        # Try 2023 batch ZIPs (most likely location)
        for month in range(1, 13):
            if not oid_map:
                break
            batch_id = f'2023_TEOS_XML_{month:02d}A'
            zip_url = f'{IRS_ZIP_BASE}/2023/{batch_id}.zip'

            if batch_id in done_batches:
                continue

            try:
                req = urllib.request.Request(zip_url, headers={
                    'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-0'
                })
                with urllib.request.urlopen(req, timeout=10) as r:
                    pass  # Just checking it exists
            except:
                continue

            print(f"  Scanning {batch_id}...")
            try:
                cd = get_central_directory(zip_url)
                for oid, info in list(oid_map.items()):
                    fname = f"{batch_id}/{oid}_public.xml"
                    if fname not in cd:
                        continue
                    try:
                        xml_bytes = extract_file(zip_url, cd[fname])
                        parsed = parse_990pf_xml(xml_bytes)
                        ein = info['ein']
                        if parsed:
                            existing[ein] = {
                                'ein': ein, 'name': info['name'],
                                'year': parsed['year'] or info['tax_period'][:4],
                                'total_grants': parsed['total_grants'],
                                'total_amount': parsed['total_amount'],
                                'matched_grants': 0, 'matched_amount': 0, 'match_pct': 0,
                                'top_grants': parsed['top_grants'],
                            }
                        else:
                            existing[ein] = {
                                'ein': ein, 'name': info['name'],
                                'year': info['tax_period'][:4],
                                'total_grants': 0, 'total_amount': 0,
                                'matched_grants': 0, 'matched_amount': 0, 'match_pct': 0,
                                'top_grants': [],
                            }
                        del oid_map[oid]
                        total_added += 1
                    except Exception as e:
                        print(f"    Error for {info['name'][:40]}: {e}")

                if oid_map:
                    print(f"    {len(oid_map)} still not found")
            except Exception as e:
                print(f"  Error scanning {batch_id}: {e}")

        # Save final
        save_shards(existing)
        with open(progress_file, 'w') as f:
            json.dump({'done_batches': list(done_batches)}, f)

    print(f"\n{'='*60}")
    print(f"DONE. Total added: {total_added}, Failed: {total_failed}")
    print(f"Total foundations with grant data: {len(existing):,}")

if __name__ == '__main__':
    main()
