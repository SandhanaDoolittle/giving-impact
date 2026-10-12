#!/usr/bin/env python3
"""
fetch_990_details.py - For each NCF organization in the app, download its most
recent full Form 990 and pull out the numbers that show how it spends money.

  python3 fetch_990_details.py --limit 20      # TEST FIRST on the 20 biggest
  python3 fetch_990_details.py                 # everything, biggest NCF grantees first

Needs metrics.json and ncf_orgs.json in the same folder (the repo files).
Saves to ncf_990_raw.json every 50 organizations. Safe to stop (Control-C) and
rerun: finished organizations are skipped; ones that failed are retried.

For each organization it makes two requests to ProPublica:
  1. the organization record (gives the newest filing id + 6 years of totals)
  2. the filing's XML (gives program / admin / fundraising split, staff, board, etc.)
If ProPublica refuses the XML it tries the IRS public copy.

Pulled from the filing (all public):
  program / management / fundraising spending, total revenue and expenses,
  contributions, assets and liabilities, cash + investments, employees, volunteers,
  board size and independent members, conflict-of-interest / whistleblower /
  audit flags, highest officer pay (title and amount only), website, mission,
  and the organization's own description of its top programs with their costs.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

API = "https://projects.propublica.org/nonprofits/api/v2/organizations/{}.json"
XML_URLS = [
    "https://projects.propublica.org/nonprofits/download-xml?object_id={}",
    "https://s3.amazonaws.com/irs-form-990/{}_public.xml",
]
OUT = "ncf_990_raw.json"
UA = {"User-Agent": "giving-impact/1.0 (research; contact via github.com/SandhanaDoolittle/giving-impact)"}


def get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch(url, tries=3):
    """Return (bytes|None, status). status: 'ok', '404', or 'err:<why>'."""
    why = ""
    for i in range(tries):
        try:
            return get(url), "ok"
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 410):
                return None, str(e.code)
            why = f"http{e.code}"
            time.sleep(3 * (i + 1))
        except Exception as e:
            why = type(e).__name__
            time.sleep(2 * (i + 1))
    return None, "err:" + why


# ----------------------------------------------------------------- XML parsing
def local(tag):
    return tag.split("}", 1)[-1]


def to_int(s):
    try:
        return int(float(re.sub(r"[^\d.\-]", "", s)))
    except (ValueError, TypeError):
        return None


def truthy(s):
    return (s or "").strip().lower() in ("1", "true", "x", "yes")


class Filing:
    def __init__(self, xml_bytes):
        self.root = ET.fromstring(xml_bytes)
        self.by = {}
        for el in self.root.iter():
            self.by.setdefault(local(el.tag), []).append(el)

    def first(self, *names):
        for n in names:
            for el in self.by.get(n, []):
                return el
        return None

    def text(self, *names):
        for n in names:
            for el in self.by.get(n, []):
                if el.text and el.text.strip():
                    return el.text.strip()
        return None

    def num(self, *names):
        return to_int(self.text(*names))

    def flag(self, *names):
        t = self.text(*names)
        return None if t is None else truthy(t)

    @staticmethod
    def child_text(el, *names):
        if el is None:
            return None
        for c in el.iter():
            if local(c.tag) in names and c.text and c.text.strip():
                return c.text.strip()
        return None

    def child_num(self, el, *names):
        return to_int(self.child_text(el, *names))


def parse_filing(xml_bytes):
    f = Filing(xml_bytes)
    d = {}
    d["form"] = f.text("ReturnTypeCd")
    d["tax_year"] = to_int(f.text("TaxYr") or (f.text("TaxPeriodEndDt") or "")[:4])
    d["mission"] = (f.text("ActivityOrMissionDesc", "MissionDesc", "PrimaryExemptPurposeTxt", "Desc") or "")[:600] or None
    d["website"] = f.text("WebsiteAddressTxt", "WebSiteAddress")
    d["employees"] = f.num("TotalEmployeeCnt", "EmployeeCnt")
    d["volunteers"] = f.num("TotalVolunteersCnt", "VolunteersCnt")
    d["board"] = f.num("VotingMembersGoverningBodyCnt", "GoverningBodyVotingMembersCnt")
    d["board_independent"] = f.num("VotingMembersIndependentCnt", "IndependentVotingMemberCnt")
    d["conflict_policy"] = f.flag("ConflictOfInterestPolicyInd")
    d["whistleblower_policy"] = f.flag("WhistleblowerPolicyInd")
    d["audited"] = f.flag("FSAuditedInd", "FinancialStatementsAuditedInd", "AuditedFinancialStmtInd",
                          "IndependentAuditFinclStmtInd")

    fx = f.first("TotalFunctionalExpensesGrp", "TotalFunctionalExpenses")
    d["expenses_total"] = f.child_num(fx, "TotalAmt") or f.num("CYTotalExpensesAmt", "TotalExpensesAmt")
    d["expenses_program"] = f.child_num(fx, "ProgramServicesAmt") or f.num("TotalProgramServiceExpensesAmt")
    d["expenses_admin"] = f.child_num(fx, "ManagementAndGeneralAmt")
    d["expenses_fundraising"] = f.child_num(fx, "FundraisingAmt")
    rg = f.first("TotalRevenueGrp")
    d["revenue"] = f.child_num(rg, "TotalRevenueColumnAmt") or f.num("CYTotalRevenueAmt", "TotalRevenueAmt")
    d["contributions"] = f.num("CYContributionsGrantsAmt", "TotalContributionsAmt")
    d["assets"] = f.num("TotalAssetsEOYAmt")
    d["liabilities"] = f.num("TotalLiabilitiesEOYAmt")
    d["net_assets"] = f.num("NetAssetsOrFundBalancesEOYAmt")
    liquid = 0
    have_liquid = False
    for g in ("CashNonInterestBearingGrp", "SavingsAndTempCashInvstGrp", "PublicInvestmentsGrp"):
        v = f.child_num(f.first(g), "EOYAmt")
        if v is not None:
            liquid += v
            have_liquid = True
    d["liquid_assets"] = liquid if have_liquid else None

    best = None                                   # highest-paid officer row (title + amount only)
    for row in f.by.get("Form990PartVIISectionAGrp", []):
        amt = (f.child_num(row, "ReportableCompFromOrgAmt") or 0) + (f.child_num(row, "OtherCompensationAmt") or 0)
        if best is None or amt > best[1]:
            best = (f.child_text(row, "TitleTxt"), amt)
    if best and best[1]:
        d["top_pay_title"], d["top_pay"] = best

    progs = []
    for name in ("ProgramSrvcAccomplishmentGrp", "ProgramServiceAccomplishmentGrp"):
        for row in f.by.get(name, []):
            desc = f.child_text(row, "DescriptionProgramSrvcAccomTxt", "Desc", "DescriptionTxt")
            if not desc:
                parts = [c.text.strip() for c in row.iter()
                         if "Desc" in local(c.tag) and c.text and c.text.strip()]
                desc = " ".join(parts)
            if desc:
                progs.append({"desc": re.sub(r"\s+", " ", desc)[:700],
                              "expense": f.child_num(row, "ExpenseAmt"),
                              "grants": f.child_num(row, "GrantAmt")})
    d["programs"] = progs[:3]
    return {k: v for k, v in d.items() if v not in (None, "", [])}


# ------------------------------------------------------------------- per-org
def process(ein):
    raw, st = fetch(API.format(ein.lstrip("0")))
    if raw is None:
        return ein, ({"found": False} if st in ("404",) else None), st
    api = json.loads(raw)
    org = api.get("organization", {})
    out = {"found": True, "ntee": org.get("ntee_code") or "", "subsection": org.get("subsection_code"),
           "ruling_year": (org.get("ruling_date") or "")[:4] or None}
    out["series"] = [
        {"year": x.get("tax_prd_yr"), "revenue": x.get("totrevenue"), "expenses": x.get("totfuncexpns"),
         "assets": x.get("totassetsend"), "contributions": x.get("totcntrbgfts")}
        for x in (api.get("filings_with_data") or [])[:6]
    ]
    oid = org.get("latest_object_id")
    if not oid:
        out["xml"] = "no filing id"
        return ein, out, "ok"
    xml, why = None, ""
    for tmpl in XML_URLS:
        body, st = fetch(tmpl.format(oid))
        if body:
            xml = body
            break
        why += f" {st}"
    if xml is None:
        out["xml"] = "unavailable:" + why.strip()
        return ein, out, "ok"
    try:
        out.update(parse_filing(xml))
        out["xml"] = "ok"
    except ET.ParseError:
        out["xml"] = "unparseable"
    return ein, out, "ok"


def targets():
    seen, rows = set(), []
    for fn in ("metrics.json", "ncf_orgs.json"):
        if not os.path.exists(fn):
            continue
        for o in json.load(open(fn)):
            e = re.sub(r"\D", "", str(o.get("ein") or ""))
            if o.get("ncf") and e and e.zfill(9) not in seen:
                seen.add(e.zfill(9))
                rows.append((e.zfill(9), o.get("ncf_total_granted") or 0, o.get("name")))
    rows.sort(key=lambda r: -r[1])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    done = json.load(open(OUT)) if os.path.exists(OUT) else {}
    rows = [r for r in targets() if r[0] not in done]
    if a.limit:
        rows = rows[:a.limit]
    print(f"{len(done)} already done, {len(rows)} to fetch")
    names = {r[0]: r[2] for r in rows}

    n = bad = 0
    with ThreadPoolExecutor(a.workers) as ex:
        for ein, res, st in ex.map(process, [r[0] for r in rows]):
            n += 1
            if res is None:
                bad += 1
                print(f"  retry later: {ein} {names.get(ein)} ({st})")
            else:
                done[ein] = res
                if a.limit and a.limit <= 25:
                    keys = [k for k in ("expenses_program", "expenses_admin", "expenses_fundraising", "employees",
                                        "volunteers", "board", "audited", "programs", "website") if k in res]
                    print(f"  {names.get(ein)}: xml={res.get('xml')} fields={keys}")
            if n % 50 == 0:
                json.dump(done, open(OUT, "w"))
                print(f"  {n}/{len(rows)}")
            time.sleep(0.1)
    json.dump(done, open(OUT, "w"))
    ok = sum(1 for v in done.values() if v.get("xml") == "ok")
    print(f"\nDone. {len(done)} saved, {ok} with full 990 detail, {bad} to retry. Saved {OUT}")


if __name__ == "__main__":
    main()
