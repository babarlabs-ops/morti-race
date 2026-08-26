#!/usr/bin/env python3
"""Fetch the FOMC meeting calendar (free, scrape federalreserve.gov) -> data/calendar.json.

The one macro calendar that reliably moves the tape. Parses the "2026 FOMC
Meetings" table (month | day-range cells) and flags the next upcoming meeting.
Graceful: scrape failure degrades to a note, never a crash.
"""
import json, os, re, html as _html, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
UA = "Morti morti@morti.capital"
MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"])}
MEET_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"[\s|]*(\d{1,2})-(\d{1,2})")


def main():
    out = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "meetings": [], "summary": ""}
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        text = re.sub(r"<[^>]+>", "|", raw)
        text = _html.unescape(text)
        text = re.sub(r"\|+", "|", text)
        i = text.find("2026 FOMC Meetings")
        j = text.find("2025 FOMC Meetings", i + 1)
        sec = text[i:j] if (i >= 0 and j > i) else (text[i:i + 6000] if i >= 0 else "")
        seen, meetings = set(), []
        for m in MEET_RE.finditer(sec):
            label = f"{m.group(1)} {m.group(2)}-{m.group(3)}"
            if label in seen:
                continue
            seen.add(label)
            meetings.append({"month": MONTHS[m.group(1)], "label": label})
        meetings.sort(key=lambda x: x["month"])
        out["meetings"] = meetings
    except Exception as e:
        out["errors"] = {"fomc": str(e)[:160]}

    if out["meetings"]:
        now = datetime.now()
        nxt = next((m for m in out["meetings"] if m["month"] >= now.month), out["meetings"][0])
        out["summary"] = ("ECONOMIC CALENDAR — 2026 FOMC meetings: "
                          + ", ".join(m["label"] for m in out["meetings"])
                          + f"\nNext upcoming: {nxt['label']}")
    else:
        out["summary"] = "(FOMC calendar unavailable)"

    path = os.path.join(ROOT, "data", "calendar.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])


if __name__ == "__main__":
    main()
