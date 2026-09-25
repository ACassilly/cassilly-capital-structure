# Review Aggregation Runbook — Legitimate Scraper (Oxylabs Web Scraper API)

System of record: **Riven ERP**. This pipeline collects **public** reviews and ratings about Portlandia Electric Supply / PES Supply for aggregation and daily monitoring. It does NOT post, fabricate, or influence reviews — read-only collection of what is already public.

## Verified API surface (as of 2026-09-18)

- **Endpoint (realtime):** `POST https://realtime.oxylabs.io/v1/queries`
- **Auth:** HTTP Basic — `username:password` (minted in the Oxylabs dashboard under **Account → Create API user**; separate from the Microsoft SSO login).
- **Content-Type:** `application/json`
- **Minimal payload:**

```json
{
  "source": "google",
  "url": "https://www.google.com/maps/search/<place>",
  "geo_location": "United States"
}
```

- `source` values confirmed by vendor docs: `google` (any Google page, incl. review surfaces) and `universal` (any URL). For non-Google platforms (Trustpilot/Yelp/BBB), use `universal`.
- `geo_location` pins results to a country (e.g. `"United States"`) — use country, not city, to match a regional US customer base and avoid thin geos.
- Google review data pricing is on a per-1K-results basis; watch usage in the dashboard.

## Proxy / IP decisions (already made)

| Choice | Pick | Rationale |
|---|---|---|
| Pool | **Residential** | Datacenter IPs are hard-blocked on Google review surfaces |
| Geo | **US, country-pinned** (`geo_location: "United States"`) | Regional US footprint; no thin-geo city pinning |
| Session | **Sticky** for GBP/Maps lookups · **rotating** for broad SERP | Sticky keeps a Maps profile session coherent |
| Cadence | **Low + jittered** — 1 req per 3–5s per host, ±1s random | Stays under both Oxylabs and Google bot heuristics |

Sticky/rotating and session control are set per-request via Oxylabs parameters; confirm the exact flag names against the current docs on the first live run (sandbox test below).

## Targets (configure in `targets.json`)

A target = `{platform, name, url, source}`. Current placeholders that need the operator to fill the real listing URLs before the first pull:

- **Google Business Profile** — the 2.8★ / 9-review GBP listing (fill `source="google"` with the GBP share/search URL).
- **Trustpilot** — `universal`
- **Yelp** — `universal`
- **BBB (Better Business Bureau)** — `universal`
- **Judge.me** — reviews widget on `portlandiaelectricsupply.myshopify.com` (public page); `universal`
- **TrustShop** — same storefront; `universal`

Do NOT target the customer `review-us` funnel login pages or anything requiring auth — public pages only.

## One-time backfill pull

Script: `review_backfill.py`
- Reads `targets.json`, POSTs each to the realtime endpoint, extracts rating + review_count + (where available) individual reviews, writes `data/backfill_<timestamp>.json` and `data/backfill_rows.csv`.
- Respects the jittered cadence; idempotent (overwrites the same output key so reruns don't double-count).

## Daily monitoring

Script: `daily_monitor.py`
- Same targets, snapshot-only: `rating`, `review_count`, `captured_at`.
- Compares against the last snapshot in `data/daily_history.json`; if rating changed by ≥ 0.1★ or count changed by ≥ 1, records the delta and emits an in-app notification with the change.
- Silent end when nothing changed.

## Safety rules (non-negotiable)

1. Read-only collection of **public** data. No posting, no accounts, no manufactured reviews, no geo-spoofing to dodge enforcement.
2. Never store the Oxylabs `username:password` in any file — it lives only in the platform credential vault (`custom-cred:realtime.oxylabs.io`), injected at request time.
3. Rate limits: single-digit requests per day after the one-time backfill. The daily monitor is a few requests per day, never a recursive crawl.
4. If a request returns a CAPTCHA/block or non-200, back off and report — do not hammer.

## First-run sandbox test

Before the full backfill, run ONE request against the sandbox target to confirm params (`source`, `geo_location`, any session flags) and cost:

```bash
# after credential is registered: review_backfill.py --dry-run
```

Then review the returned HTML/JSON, confirm the review source value against the current Oxylabs docs, and only then run the full pull.