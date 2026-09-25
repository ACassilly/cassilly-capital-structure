#!/usr/bin/env python3
"""Daily public review rating/count snapshot + delta notification.

Read-only. Snapshot-only (no review text) to keep the daily run cheap.
Appends to data/daily_history.json and compares consecutive entries per platform.

Auth: Oxylabs Basic username:password via credential vault
      (custom-cred:realtime.oxylabs.io) — never in this file.
"""
import json, sys, time, random
from datetime import datetime, timezone
from pathlib import Path
import requests
import urllib3
urllib3.disable_warnings()

ENDPOINT = "https://realtime.oxylabs.io/v1/queries"
BASE = Path(__file__).resolve().parent
TARGETS = json.load(open(BASE / "targets.json"))["targets"]
HIST = BASE / "data" / "daily_history.json"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(target):
    payload = {"source": target["source"], "url": target["url"],
               "geo_location": "United States"}
    try:
        r = requests.post(ENDPOINT, json=payload, timeout=60, verify=False)
        if r.status_code != 200:
            print(f"[!] {target['platform']} HTTP {r.status_code}")
            return None
        return r.json()
    except Exception as e:
        print(f"[!] {target['platform']} error: {e}")
        return None


def main():
    history = []
    if HIST.exists():
        try:
            history = json.load(open(HIST))
        except Exception:
            history = []

    prev = {}
    for h in history:
        prev[h["platform"]] = h  # last seen per platform

    new_rows = []
    deltas = []
    for t in TARGETS:
        data = fetch(t)
        time.sleep(random.uniform(3.0, 5.0))
        # placeholder parse — confirm parser on first live run (see runbook)
        rating = None
        count = None
        row = {
            "platform": t["platform"],
            "listing_url": t["url"],
            "rating": rating,
            "review_count": count,
            "captured_at": now(),
        }
        new_rows.append(row)
        p = prev.get(t["platform"])
        if p is not None:
            dr = None if rating is None or p.get("rating") is None else round(rating - p["rating"], 2)
            dc = None if count is None or p.get("review_count") is None else count - p.get("review_count")
            if (dr is not None and abs(dr) >= 0.1) or (dc is not None and abs(dc) >= 1):
                deltas.append({
                    "platform": t["platform"],
                    "rating_before": p.get("rating"),
                    "rating_after": rating,
                    "count_before": p.get("review_count"),
                    "count_after": count,
                })

    history.extend(new_rows)
    HIST.parent.mkdir(exist_ok=True)
    json.dump(history, open(HIST, "w"), indent=2)

    if deltas:
        print(json.dumps({"changed": deltas}))
        # In scheduled background runs, follow this with the in-app notification
        # (send_notification) carrying the delta details.
    else:
        print(json.dumps({"changed": []}))


if __name__ == "__main__":
    main()