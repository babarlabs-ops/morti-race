#!/usr/bin/env python3
"""Fetch SEC EDGAR signals (free, no key) -> data/edgar.json.

Two high-signal, low-noise feeds from the SEC's public browse-edgar ATOM output:
  - Form 4 (insider buys/sells) — the classic "smart money" edge.
  - 8-K (material events: M&A, guidance, restatements, leadership).
Graceful: SEC rate-limits; failures degrade to an empty summary, never a crash.
"""
import json, os, re, urllib.request, urllib.error, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Morti morti@morti.capital"  # SEC requires a contact UA
COMPANY_RE = re.compile(r"^(?:4(?:/A)?|8-K)\s*-\s*([^(]+)")


def fetch_atom(type_code):
    url = (f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type={type_code}"
           f"&dateb=&owner=include&count=30&output=atom")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read()
    root = ET.fromstring(data)
    # Atom namespace: {http://www.w3.org/2005/Atom}
    ns = "{http://www.w3.org/2005/Atom}"
    rows = []
    for entry in root.iter(ns + "entry"):
        title = entry.findtext(ns + "title") or ""
        updated = entry.findtext(ns + "updated") or ""
        m = COMPANY_RE.match(title.strip())
        company = m.group(1).strip() if m else title.strip()
        rows.append({"company": company[:40], "date": updated[:10]})
    return rows


def main():
    out = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "insider": [], "material": [], "summary": ""}
    for key, code in (("insider", "4"), ("material", "8-K")):
        try:
            out[key] = fetch_atom(code)[:15]
        except Exception as e:
            out.setdefault("errors", {})[code] = str(e)[:120]
    lines = ["SEC EDGAR — recent insider (Form 4) filings:"]
    lines += [f"- {r['company']} ({r['date']})" for r in out["insider"]] or ["  (none)"]
    lines.append("SEC EDGAR — recent material events (8-K):")
    lines += [f"- {r['company']} ({r['date']})" for r in out["material"]] or ["  (none)"]
    out["summary"] = "\n".join(lines)
    path = os.path.join(ROOT, "data", "edgar.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])


if __name__ == "__main__":
    main()
