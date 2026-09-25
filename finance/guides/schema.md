# Review Aggregator Schema

Two layers: a **snapshot** for daily rating/count monitoring, and an **append-only review ledger** for the one-time backfill. All timestamps UTC ISO-8601. Names abbreviated (first name + last initial) per the privacy rule.

## Snapshot (daily history)

File: `data/daily_history.json` — append one entry per platform per capture.

```json
{
  "platform": "google_business",
  "listing_url": "https://www.google.com/maps/...",
  "rating": 2.8,
  "review_count": 9,
  "captured_at": "2026-09-18T17:00:00Z"
}
```

| field | type | notes |
|---|---|---|
| platform | string | enum: `google_business`, `trustpilot`, `yelp`, `bbb`, `judgeme`, `trustshop` |
| listing_url | string | canonical public listing URL |
| rating | number | current star average (0–5), nullable if platform doesn't publish it |
| review_count | number | integer count |
| captured_at | string | UTC ISO-8601 timestamp of the capture |

## Review ledger (backfill)

File: `data/backfill_rows.csv` + `data/backfill_<timestamp>.json` — one row per review.

| field | type | notes |
|---|---|---|
| platform | string | as above |
| listing_url | string | source listing |
| review_id | string | platform-native id or hash; dedupe key |
| author | string | abbreviated (`John S.`); empty for anonymous |
| rating | number | 1–5 |
| review_text | string | public review body (may be empty) |
| review_date | string | published date, `YYYY-MM-DD` (partial dates ok) |
| response_present | boolean | whether the business has posted a public owner response |
| captured_at | string | UTC capture time |

## Aggregated view (derived, not stored)

The `/pages/review-us` aggregator renders from these two layers:
- **Rating + count** per platform → the public-facing "our reviews" widget.
- **Feed** → time-sorted merge of the review ledger across platforms.
- **Owner-response flag** → marks reviews still needing a reply (routed for response review, never removed unless a genuine platform violation).

## Integrity rules

- Dedupe on `(platform, review_id)`; a re-pull must not create duplicate rows.
- Rating/count snapshots are pure append — no in-place edits; deltas are computed by diffing consecutive entries per platform.
- A change of ≥ 0.1★ or ≥ 1 count triggers the daily notification.