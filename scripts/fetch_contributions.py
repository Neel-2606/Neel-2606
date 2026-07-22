#!/usr/bin/env python3
"""Scrape the public contribution calendar (no token) and write data/contributions.json."""
import json, os, sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER", "Neel-2606")
URL = f"https://github.com/users/{USER}/contributions"

def main():
    r = requests.get(URL, headers={"User-Agent": "profile-art/1.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        if not date:
            continue
        lvl = int(cell.get("data-level", 0))
        days.append({"date": date, "level": lvl})

    # counts live in tool-tips table in some layouts; level is enough for coloring.
    days.sort(key=lambda d: d["date"])

    # streaks based on level>0
    cur = longest = run = 0
    for d in days:
        if d["level"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    # current streak = trailing run
    for d in reversed(days):
        if d["level"] > 0:
            cur += 1
        else:
            break

    total_text = ""
    h2 = soup.find("h2")
    if h2:
        total_text = " ".join(h2.get_text().split())

    out = {
        "user": USER,
        "generated": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "stats": {
            "current_streak": cur,
            "longest_streak": longest,
            "total_text": total_text,
        },
    }
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote data/contributions.json ({len(days)} days) for {USER}")

if __name__ == "__main__":
    main()
