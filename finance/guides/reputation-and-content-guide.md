# Marketing Playbook — Reputation, Reviews, and Content

Owner: Growth / Marketing. Read before running any review campaign.

## The review problem is a fulfillment problem

The Google Business Profile sits at **2.8★ with 9 reviews** — but the reason isn't a missing review ask, it's that **172 of 283 paid customers are unfulfilled** and only 32 are genuinely happy. Soliciting reviews now harvests 1-stars.

Sequence (never skip):
1. Clear the 172 unfulfilled (Ops owns the fix).
2. Solicit only the **fulfilled + paid** set — `review_solicitation_segments.csv` (32 happy names).
3. Route sub-5★ through the `review-us` funnel privately; never suppress a legitimate negative.

## Legitimate review aggregation (staged, not live)

The scraper scaffold is ready but the Oxylabs API credential was **declined**, so it's inert. Files: `review-ops/runbook.md` (verified endpoint + IP decisions), `schema.md`, `targets.json`, `review_backfill.py`, `daily_monitor.py`.

To resume: mint the Oxylabs Scraper API user in the dashboard, then feed it through the secure credential form. Config already decided — residential pool, US country-pinned, sticky sessions for Maps / rotating for SERP, jittered 3–5s cadence.

## Hard no-gos

- No manufactured or fabricated reviews (illegal under FTC rules; against Google/Judge.me/TrustShop terms).
- No aged-account + rotating-IP posting to dodge detection.
- Only *policy-violating* negative reviews (spam, fake, off-topic) get takedown flags; legitimate negatives get a strong owner response + remediation, not removal.

## Content rails

- Brand is PES (Portlandia Electric Supply); storefront is the headless catalog.
- Shopify is demoted to catalog; orders book in Riven ERP. Any "buy now" copy must point at the live ordering path (phone/manual until checkout is built).

## Files

- `review_solicitation_segments.csv` — who to solicit vs remediate.
- `review-ops/` — the full legitimate scraper scaffold.