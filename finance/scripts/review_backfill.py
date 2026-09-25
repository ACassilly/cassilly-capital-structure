#!/usr/bin/env python3
"""One-time public review backfill via Oxylabs Web Scraper API (realtime endpoint).

Read-only: collects public rating/count/review text. Never posts or fabricates.

Auth: Oxylabs Basic username:password is injected at request time via the
      platform credential vault (custom-cred:realtime.oxylabs.io). Do NOT put
      the secret in this file.

Run once creds are registered:
    python3 review_backfill.py            # full pull
    python3 review_backfill.py --dry-run  # sandbox single request, no writes
"""
import json, sys, time, random, hashlib, csv
from datetime import datetime, timezone
from pathlib import Path
import requests
import urllib3
urllib3.disable_warnings()

ENDPOINT = "https://realtime.oxylabs.io/v1/queries"
BASE = Path(__file__).resolve().parent
TARGETS = json.load(open(BASE / "targets.json"))["targets"]
OUT = BASE / "data"
OUT.mkdir(exist_ok=True)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jitter():
    time.sleep(random.uniform(3.0, 5.0))


def fetch(target, dry=False):
    """POST one target to the realtime endpoint. Returns parsed JSON or None."""
    payload = {
        "source": target["source"],
        "url": target["url"],
        "geo_location": "United States",
        # sticky sessions for GBP; confirm exact flag on live run per runbook
    }
    if dry:
        print(f"[dry] would POST {target['source']} -> {target['url']}")
        return None
    r = requests.post(ENDPOINT, json=payload, timeout=60, verify=False)
    if r.status_code != 200:
        print(f"[!] {target['platform']} HTTP {r.status_code}: {r.text[:200]}")
        return None
    return r.json()


def extract(target, data):
    """Best-effort parse. HTML may need OxyParser post-processing (see runbook)."""
    url = target["url"]
    # Raw results arrive as HTML in results[0].content (Oxylabs realtime shape).
    result = data.get("results", [{}])
    content = result[0].get("content", "") if result else ""
    # Placeholder extraction — replace with parsed rating/count once HTML shape
    # is confirmed on the first live pull. Preserve raw for downstream OxyParser.
    return {
        "platform": target["platform"],
        "name": target["name"],
        "listing_url": url,
        "rating": None,
        "review_count": None,
        "captured_at": now(),
        "raw_available": bool(content),
        "raw_len": len(content) if isinstance(content, str) else 0,
    }


def main():
    dry = "--dry-run" in sys.argv
    rows = []
    for t in TARGETS:
        data = fetch(t, dry=dry)
        jitter()
        if data is None:
            continue
        rows.append(extract(t, data))

    if dry:
        print("dry run complete — no files written")
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json.dump(rows, open(OUT / f"backfill_{ts}.json", "w"), indent=2)
    # append-ish CSV for the review ledger
    cvs = OUT / "backfill_rows.csv"
    existed = cvs.exists()
    with open(cvs, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "platform", "name", "listing_url", "rating", "review_count",
            "captured_at", "raw_available", "raw_len"])
        if not existed:
            w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT / f'backfill_{ts}.json'} and {cvs} ({len(rows)} targets)")


if __name__ == "__main__":
    main()